"""
Live Trader Engine — Kha0sys3
Motor principal de trading ORB con lógica idéntica al backtester.

Consistencia con backtest:
  - ATR14 filter: or_atr_ratio in [0.1, 0.8]
  - Un trade por activo por día (first_break_dir)
  - Cancelar pierna opuesta al detectar fill
  - Position sizing sobre BALANCE
  - OR calculado desde barra M15 CERRADA
  - Timezone UTC consistente
"""

import MetaTrader5 as mt5
import time
import threading
from datetime import datetime, timezone

from src.execution.mt5_client import MT5Client
from src.execution.risk_manager import DynamicRiskAllocator
from src.execution.order_manager import OrderManager
from src.monitoring.telegram_bot import TelegramCommandBot
from src.monitoring.mt5_reporter import MT5Reporter
from src.monitoring.system_health import SystemHealthMonitor


class LiveTraderEngine:
    """Motor de trading ORB con bot Telegram interactivo."""

    HEARTBEAT_INTERVAL = 900         # 15 min entre heartbeats/reportes
    HEALTH_CHECK_INTERVAL = 300      # 5 min entre chequeos de salud
    POSITION_CHECK_INTERVAL = 10     # 10s entre chequeos de posiciones (para OCO cancel)
    STALE_ORDER_CHECK_INTERVAL = 3600  # 1h entre limpieza de órdenes rancias
    RECONNECT_CHECK_INTERVAL = 60    # 1 min entre chequeos de conexión MT5

    def __init__(self, config_path: str = "src/execution/bot_config.json"):
        import json
        with open(config_path, "r") as f:
            cfg = json.load(f)

        self.risk_percent = cfg.get("risk_percent_per_trade", 0.035)
        self.target_symbols = cfg.get("trinity_portfolio", [])

        self.client = MT5Client()
        self.risk = DynamicRiskAllocator(risk_percent_per_trade=self.risk_percent)
        self.reporter = MT5Reporter()
        self.health_monitor = SystemHealthMonitor()

        # Bot Telegram con callbacks de control
        self.telegram = TelegramCommandBot(
            stop_callback=self._on_stop_command,
            resume_callback=self._on_resume_command,
        )

        self.om = None

        # Thread safety
        self._control_lock = threading.Lock()
        self._paused = False

        # Timestamps
        self._start_time = None
        self._last_heartbeat = 0
        self._last_health_check = 0
        self._last_position_check = 0
        self._last_stale_check = 0
        self._last_reconnect_check = 0

        # Dedup: un fire por magic_time por día
        self._last_fired: dict[str, str] = {}  # sym -> "YYYY-MM-DD HH:MM"

        # Position tracking
        self._known_positions: set[int] = set()
        self._trades_today = 0
        self._last_trade_day = ""

    # ─── Control callbacks (thread-safe) ──────────────────────────

    def _on_stop_command(self):
        with self._control_lock:
            self._paused = True

    def _on_resume_command(self):
        with self._control_lock:
            self._paused = False

    @property
    def _is_paused(self) -> bool:
        with self._control_lock:
            return self._paused

    # ─── Time helpers (UTC consistente) ───────────────────────────

    def _utc_now(self) -> datetime:
        return datetime.now(timezone.utc)

    def _reset_daily_counters(self):
        today = self._utc_now().strftime("%Y-%m-%d")
        if today != self._last_trade_day:
            self._trades_today = 0
            self._last_fired.clear()
            self._last_trade_day = today

    # ─── Dedup: un fire por magic_time ────────────────────────────

    def _should_execute(self, setup: dict) -> bool:
        """Verifica si es el magic_time Y no se ha ejecutado ya hoy."""
        now = self._utc_now()
        now_hhmm = now.strftime("%H:%M")
        sym = setup["sym"]

        if now_hhmm != setup["magic_time"]:
            return False

        # Dedup key: symbol + fecha + hora
        dedup_key = f"{now.strftime('%Y-%m-%d')} {now_hhmm}"
        if self._last_fired.get(sym) == dedup_key:
            return False

        return True

    def _mark_fired(self, sym: str):
        now = self._utc_now()
        dedup_key = f"{now.strftime('%Y-%m-%d')} {now.strftime('%H:%M')}"
        self._last_fired[sym] = dedup_key

    # ─── ATR14 Filter (consistente con backtest) ──────────────────

    def _passes_atr_filter(self, symbol: str, or_width: float) -> bool:
        """Filtra OR width: debe estar entre 10% y 80% del ATR14.

        Idéntico al backtest: or_atr_ratio.is_between(0.1, 0.8)
        """
        atr14 = self.client.calculate_atr14(symbol)
        if atr14 is None or atr14 <= 0:
            print(f"[ATR] No se pudo calcular ATR14 para {symbol}. Skipping.")
            return False

        ratio = or_width / atr14
        if not (0.1 <= ratio <= 0.8):
            print(f"[ATR] {symbol}: or_atr_ratio={ratio:.3f} fuera de [0.1, 0.8]. Skipping.")
            if self.telegram:
                self.telegram.notify_order_rejected(
                    symbol,
                    f"or_atr_ratio={ratio:.3f} fuera de rango [0.1, 0.8]"
                )
            return False

        return True

    # ─── Monitoreo periódico ──────────────────────────────────────

    def _send_periodic_report(self):
        """Reporte cada 15 min con balance, equity, PnL del día."""
        now = time.time()
        if now - self._last_heartbeat < self.HEARTBEAT_INTERVAL:
            return
        self._last_heartbeat = now

        uptime_hours = (now - self._start_time) / 3600
        self.telegram.notify_heartbeat(uptime_hours, self._trades_today)

    def _check_system_health(self):
        now = time.time()
        if now - self._last_health_check < self.HEALTH_CHECK_INTERVAL:
            return
        self._last_health_check = now

        alerts = self.health_monitor.get_critical_alerts()
        if alerts:
            self.telegram.notify_system_alert(alerts)

    def _check_mt5_connection(self):
        """Verifica conexión MT5 periódicamente y reconecta si es necesario."""
        now = time.time()
        if now - self._last_reconnect_check < self.RECONNECT_CHECK_INTERVAL:
            return
        self._last_reconnect_check = now

        if not self.client.ensure_connected():
            self.telegram.notify_error("MT5 desconectado. Reconexión fallida.", "Connection")

    def _wipe_stale_orders(self):
        now = time.time()
        if now - self._last_stale_check < self.STALE_ORDER_CHECK_INTERVAL:
            return
        self._last_stale_check = now
        self.om.wipe_stale_orders()

    # ─── Detección de fills y cancelar pierna opuesta ─────────────

    def _check_positions_and_fills(self):
        """Detecta nuevas posiciones (fills) y cierre de posiciones.

        Al detectar un fill:
          - Cancela la pierna opuesta (OCO en software)
          - Marca el activo como "traded today"

        Al detectar un cierre:
          - Notifica con mariposas/explosiones
        """
        now = time.time()
        if now - self._last_position_check < self.POSITION_CHECK_INTERVAL:
            return
        self._last_position_check = now

        current_positions = mt5.positions_get()
        if current_positions is None:
            # MT5 desconectado — NO tocar _known_positions
            return

        current_tickets = {p.ticket for p in current_positions}

        # --- Detectar NUEVOS fills (para cancelar pierna opuesta) ---
        new_tickets = current_tickets - self._known_positions
        for ticket in new_tickets:
            for p in current_positions:
                if p.ticket == ticket and p.magic == 1337:
                    # Nueva posición del bot — cancelar pierna opuesta
                    self.om.cancel_opposite_leg(p.symbol)
                    self.om.mark_traded_today(p.symbol)
                    break

        # --- Detectar posiciones CERRADAS ---
        closed_tickets = self._known_positions - current_tickets
        if closed_tickets:
            from_date = self._utc_now().replace(hour=0, minute=0, second=0, microsecond=0)
            deals = mt5.history_deals_get(from_date, self._utc_now())

            for ticket in closed_tickets:
                if deals is None:
                    continue
                close_deals = [
                    d for d in deals
                    if d.position_id == ticket and d.entry == mt5.DEAL_ENTRY_OUT
                ]
                if not close_deals:
                    continue

                deal = close_deals[-1]
                profit = deal.profit + deal.commission + deal.swap

                if profit >= 0:
                    emoji_line = "🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋"
                    result_text = "GANANCIA"
                    result_emoji = "🦋"
                else:
                    emoji_line = "💥💥💥💥💥💥💥💥💥💥"
                    result_text = "PERDIDA"
                    result_emoji = "💥"

                msg = (
                    f"{emoji_line}\n"
                    "━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"   {result_emoji} <b>TRADE CERRADO</b>\n"
                    "━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"  Simbolo   │ {deal.symbol}\n"
                    f"  Resultado │ <b>{result_text}</b>\n"
                    f"  P&L       │ <b>${profit:+,.2f}</b>\n"
                    f"  Volumen   │ {deal.volume} lots\n"
                    f"  Precio    │ {deal.price:.5f}\n"
                    f"  Comision  │ ${deal.commission:,.2f}\n"
                    f"  Swap      │ ${deal.swap:,.2f}\n"
                    "━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"  <i>{self._utc_now().strftime('%H:%M')} UTC</i>\n"
                    f"{emoji_line}"
                )
                self.telegram.send_sync(msg)

        self._known_positions = current_tickets

    # ─── Procesamiento de símbolo ─────────────────────────────────

    def _process_symbol(self, setup: dict):
        """Procesa un símbolo en su magic_time. Aislado con try/except."""
        sym = setup["sym"]

        if not self._should_execute(setup):
            return

        # Marcar como fired inmediatamente (dedup)
        self._mark_fired(sym)

        # Un trade por día
        if self.om.has_traded_today(sym):
            return

        print(f"[TICKER] Ventana abierta para {sym}")

        # OR desde barras CERRADAS (soporta multi-vela)
        or_data = self.client.get_or_from_closed_bars(sym, duration_mins=setup.get("dur", 15))
        if or_data is None:
            self.telegram.notify_error(f"Sin datos M15 para {sym}", "DataFeed")
            return

        range_high = or_data["high"]
        range_low = or_data["low"]
        rng = or_data["width"]

        if rng <= 0:
            self.telegram.notify_order_rejected(sym, "Rango cero o negativo")
            return

        # ATR14 filter (idéntico al backtest: or_atr_ratio in [0.1, 0.8])
        if not self._passes_atr_filter(sym, rng):
            return

        self.telegram.notify_orb_detected(sym, range_high, range_low, rng)

        # Dynamic TP Calculation (Adaptive TP)
        tp_config = setup.get("tp_opt", 1.5)
        selected_tp = 1.5 # Default

        if isinstance(tp_config, dict):
            # Obtener ATR14 para calcular el ratio del día
            atr = self.client.calculate_atr14(sym)
            if atr:
                ratio = rng / atr
                if ratio < 0.3: selected_tp = tp_config.get("narrow", 1.5)
                elif ratio < 0.6: selected_tp = tp_config.get("normal", 1.0)
                else: selected_tp = tp_config.get("wide", 0.5)
                print(f"[ADAPTIVE] Ratio: {ratio:.2f} | TP Seleccionado: {selected_tp}x")
            else:
                selected_tp = tp_config.get("normal", 1.0)
        else:
            selected_tp = float(tp_config)

        sl_up = range_low
        sl_dw = range_high
        tp_up = range_high + (rng * selected_tp)
        tp_dw = range_low - (rng * selected_tp)

        placed = self.om.place_breakout_stop_orders(
            symbol=sym,
            range_high=range_high,
            range_low=range_low,
            sl_up=sl_up,
            sl_dw=sl_dw,
            tp_up=tp_up,
            tp_dw=tp_dw,
        )

        if placed:
            self._trades_today += 1

    # ─── Main loop ────────────────────────────────────────────────

    def run(self):
        if not self.client.connect():
            self.telegram.notify_error("MT5 initialize() fallo", "Startup")
            return

        self.om = OrderManager(self.client, self.risk, self.telegram)
        self._start_time = time.time()
        self._last_heartbeat = self._start_time
        self._last_health_check = self._start_time
        self._last_position_check = self._start_time
        self._last_stale_check = self._start_time
        self._last_reconnect_check = self._start_time
        self._last_trade_day = self._utc_now().strftime("%Y-%m-%d")

        # Inicializar posiciones conocidas
        initial_positions = mt5.positions_get()
        if initial_positions:
            self._known_positions = {p.ticket for p in initial_positions}

        # Iniciar bot Telegram interactivo
        self.telegram.start_polling()
        time.sleep(2)

        self.telegram.notify_bot_started(self.target_symbols)
        print("Kha0sys3 Bot Iniciado. Modo Espera...")

        try:
            while True:
                self._reset_daily_counters()

                if not self._is_paused and self.telegram.is_active:
                    for setup in self.target_symbols:
                        try:
                            self._process_symbol(setup)
                        except Exception as e:
                            sym = setup.get("sym", "UNKNOWN")
                            self.telegram.notify_error(
                                f"{sym}: {type(e).__name__}: {e}", "ProcessSymbol"
                            )
                            print(f"[ERROR] {sym} skipped: {e}")

                # Monitoreo continuo (incluso en pausa)
                self._check_positions_and_fills()
                self._wipe_stale_orders()
                self._send_periodic_report()
                self._check_system_health()
                self._check_mt5_connection()

                time.sleep(10)

        except KeyboardInterrupt:
            self.telegram.notify_bot_stopped("KeyboardInterrupt")
            print("\nBot finalizado manualmente.")
        except Exception as e:
            self.telegram.notify_error(str(e), "MainLoop")
            raise
        finally:
            self.telegram.stop_polling()
            self.client.disconnect()


if __name__ == "__main__":
    bot = LiveTraderEngine()
    bot.run()
