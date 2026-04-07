"""
Live Trader Engine — Kha0sys3
Motor principal de trading ORB con paridad exacta al backtester.

Paridad con backtest (portfolio_compounder.py):
  - ATR14 filter: or_atr_ratio in [0.1, 0.8]
  - TREND_UP: solo BUY_STOP, monitoreo software si DOWN rompe primero
  - MAGNET_CLOSE: direccion dada por pd_close vs OR
  - TP fijo: 1.5R para TREND, pd_close para MAGNET
  - Waterfall duraciones: 15m primero, 30m si ATR falla
  - Dedup: 1 trade por (simbolo, edge) por dia
  - Position sizing: 3% del BALANCE
  - OR desde barras M15 CERRADAS
  - Timezone UTC
"""

import MetaTrader5 as mt5
import time
import threading
from datetime import datetime, timezone
from pathlib import Path

from src.execution.mt5_client import MT5Client
from src.execution.risk_manager import DynamicRiskAllocator, SLGuardian
from src.execution.order_manager import OrderManager
from src.monitoring.telegram_bot import TelegramCommandBot
from src.monitoring.mt5_reporter import MT5Reporter
from src.monitoring.system_health import SystemHealthMonitor


class LiveTraderEngine:
    """Motor de trading ORB con paridad backtest y bot Telegram interactivo."""

    HEARTBEAT_INTERVAL = 900
    HEALTH_CHECK_INTERVAL = 300
    POSITION_CHECK_INTERVAL = 10
    STALE_ORDER_CHECK_INTERVAL = 3600
    RECONNECT_CHECK_INTERVAL = 60

    # TP fijo para TREND (paridad con backtest)
    TREND_TP_MULTIPLIER = 1.5

    def __init__(self, config_path: str = "src/execution/bot_config.json"):
        import json
        with open(config_path, "r") as f:
            cfg = json.load(f)

        self.risk_percent = cfg.get("risk_percent_per_trade", 0.03)
        self.target_symbols = cfg.get("portfolio", cfg.get("trinity_portfolio", []))

        self.client = MT5Client()
        self.risk = DynamicRiskAllocator(risk_percent_per_trade=self.risk_percent)
        self.sl_guardian = SLGuardian()
        self.reporter = MT5Reporter()
        self.health_monitor = SystemHealthMonitor()

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

        # Dedup: un fire por (sym, edge, duration) por dia
        self._last_fired: dict[str, str] = {}

        # Waterfall state: tracks which duration index each setup is at
        # key = "sym_edge" -> current duration index (0 = first, 1 = second, etc.)
        self._waterfall_state: dict[str, int] = {}

        # Position tracking
        self._known_positions: set[int] = set()
        self._trades_today = 0
        self._last_trade_day = ""

    # ─── Control callbacks ────────────────────────────────────────

    def _on_stop_command(self):
        with self._control_lock:
            self._paused = True
        # Cancel all pending bot orders for safety
        if self.om:
            try:
                import MetaTrader5 as mt5
                orders = mt5.orders_get()
                if orders:
                    for o in orders:
                        if o.magic == 1337:
                            self.om.cancel_order_by_ticket(o.ticket, o.symbol)
            except Exception as e:
                print(f"[STOP] Error cancelando ordenes: {e}")

    def _on_resume_command(self):
        with self._control_lock:
            self._paused = False

    @property
    def _is_paused(self) -> bool:
        with self._control_lock:
            return self._paused

    # ─── Time helpers ─────────────────────────────────────────────

    def _utc_now(self) -> datetime:
        return datetime.now(timezone.utc)

    def _reset_daily_counters(self):
        today = self._utc_now().strftime("%Y-%m-%d")
        if today != self._last_trade_day:
            self._trades_today = 0
            self._last_fired.clear()
            self._waterfall_state.clear()
            self._last_trade_day = today

    # ─── Waterfall scheduling ─────────────────────────────────────

    def _get_execution_time(self, setup: dict) -> str:
        """Calcula el HH:MM de ejecucion basado en waterfall state."""
        sym = setup["sym"]
        edge = setup["edge"]
        wf_key = f"{sym}_{edge}"
        durations = setup.get("durations", [15])

        # Current duration index
        dur_idx = self._waterfall_state.get(wf_key, 0)
        if dur_idx >= len(durations):
            return ""  # All durations exhausted

        dur = durations[dur_idx]
        h, m = map(int, setup["magic_time"].split(":"))
        total_mins = h * 60 + m + dur
        exec_h = (total_mins // 60) % 24
        exec_m = total_mins % 60
        return f"{exec_h:02d}:{exec_m:02d}"

    def _should_execute(self, setup: dict) -> bool:
        """Verifica si es el momento de ejecutar (magic_time + duration)."""
        exec_time = self._get_execution_time(setup)
        if not exec_time:
            return False

        now = self._utc_now()
        now_hhmm = now.strftime("%H:%M")

        if now_hhmm != exec_time:
            return False

        sym = setup["sym"]
        edge = setup["edge"]
        wf_key = f"{sym}_{edge}"
        dur_idx = self._waterfall_state.get(wf_key, 0)

        dedup_key = f"{now.strftime('%Y-%m-%d')} {exec_time} {wf_key}_{dur_idx}"
        if self._last_fired.get(wf_key) == dedup_key:
            return False

        return True

    def _mark_fired(self, setup: dict):
        sym = setup["sym"]
        edge = setup["edge"]
        wf_key = f"{sym}_{edge}"
        dur_idx = self._waterfall_state.get(wf_key, 0)
        exec_time = self._get_execution_time(setup)
        now = self._utc_now()
        dedup_key = f"{now.strftime('%Y-%m-%d')} {exec_time} {wf_key}_{dur_idx}"
        self._last_fired[wf_key] = dedup_key

    def _advance_waterfall(self, setup: dict):
        """Avanza al siguiente duration en el waterfall (ATR fallo)."""
        wf_key = f"{setup['sym']}_{setup['edge']}"
        current = self._waterfall_state.get(wf_key, 0)
        self._waterfall_state[wf_key] = current + 1

    # ─── ATR14 Filter ─────────────────────────────────────────────

    def _passes_atr_filter(self, symbol: str, or_width: float) -> bool:
        """Filtra OR width: debe estar entre 10% y 80% del ATR14."""
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

    # ─── Monitoreo periodico ──────────────────────────────────────

    def _send_periodic_report(self):
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
        now = time.time()
        if now - self._last_reconnect_check < self.RECONNECT_CHECK_INTERVAL:
            return
        self._last_reconnect_check = now
        if not self.client.ensure_connected():
            self.telegram.notify_error("MT5 desconectado. Reconexion fallida.", "Connection")

    def _wipe_stale_orders(self):
        now = time.time()
        if now - self._last_stale_check < self.STALE_ORDER_CHECK_INTERVAL:
            return
        self._last_stale_check = now
        self.om.wipe_stale_orders()

    # ─── Fill detection + trend monitors ──────────────────────────

    def _check_positions_and_fills(self):
        """Detecta fills, cierre de posiciones, y monitorea TREND_UP."""
        now = time.time()
        if now - self._last_position_check < self.POSITION_CHECK_INTERVAL:
            return
        self._last_position_check = now

        # 1. Check TREND_UP monitors (cancel BUY if DOWN breaks first)
        self.om.check_trend_monitors()

        # 2. Detect new fills
        current_positions = mt5.positions_get()
        if current_positions is None:
            return

        current_tickets = {p.ticket for p in current_positions}

        # New fills
        new_tickets = current_tickets - self._known_positions
        for ticket in new_tickets:
            for p in current_positions:
                if p.ticket == ticket and p.magic == 1337:
                    comment = p.comment or ""
                    # Determine edge from comment
                    if "TREND" in comment:
                        edge = "TREND_UP"
                    elif "MAGNET" in comment:
                        edge = "MAGNET_CLOSE"
                    else:
                        edge = ""

                    self.om.cancel_opposite_leg(p.symbol)
                    self.om.mark_traded_today(p.symbol, edge)
                    self._trades_today += 1
                    break

        # Closed positions
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
                comment = deal.comment or ""

                if profit >= 0:
                    emoji_line = "🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋"
                    result_text = "GANANCIA"
                    result_emoji = "🦋"
                else:
                    emoji_line = "💥💥💥💥💥💥💥💥💥💥"
                    result_text = "PERDIDA"
                    result_emoji = "💥"

                # Identify edge from comment
                edge_label = ""
                if "TREND" in comment:
                    edge_label = "TREND_UP"
                elif "MAGNET" in comment:
                    edge_label = "MAGNET"

                msg = (
                    f"{emoji_line}\n"
                    "━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"   {result_emoji} <b>TRADE CERRADO</b>\n"
                    "━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"  Simbolo   │ {deal.symbol}\n"
                    f"  Edge      │ {edge_label}\n"
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

        # SL Guardian: cierra posiciones donde el precio paso el SL (flash crash/slippage)
        try:
            breached = self.sl_guardian.find_breached_positions(current_positions)
            for p in breached:
                self._emergency_close_position(p)
        except Exception as e:
            print(f"[SL_GUARDIAN] Error checking: {e}")

        self._known_positions = current_tickets

    # ─── Emergency close ────────────────────────────────────────

    def _emergency_close_position(self, position):
        """Cierra UNA posicion cuyo SL fue saltado por slippage/gap."""
        close_type = mt5.ORDER_TYPE_SELL if position.type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY
        req = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": position.symbol,
            "volume": position.volume,
            "type": close_type,
            "position": position.ticket,
            "deviation": 50,
            "magic": 1337,
            "comment": "SL_GUARDIAN",
            "type_filling": self.om._get_filling_mode(position.symbol) if self.om else mt5.ORDER_FILLING_FOK,
        }
        result = mt5.order_send(req)
        if result and result.retcode == mt5.TRADE_RETCODE_DONE:
            self.telegram.send_sync(
                f"🚨 <b>SL SALTADO — CIERRE FORZADO</b>\n"
                f"  {position.symbol} | {position.volume} lots\n"
                f"  SL: {position.sl} | Precio: {position.price_current}\n"
                f"  Cerrado @ {result.price}"
            )
        else:
            self.telegram.send_sync(
                f"🚨 <b>SL GUARDIAN FALLO</b>: {position.symbol} - "
                f"retcode {result.retcode if result else 'None'}"
            )

    # ─── Symbol processing ────────────────────────────────────────

    def _process_symbol(self, setup: dict):
        """Procesa un setup en su ventana de ejecucion."""
        sym = setup["sym"]
        edge = setup["edge"]
        durations = setup.get("durations", [15])
        wf_key = f"{sym}_{edge}"

        if not self._should_execute(setup):
            return

        self._mark_fired(setup)

        # Dedup: un trade por (symbol, edge) por dia
        if self.om.has_traded_today(sym, edge):
            return

        # Current duration from waterfall
        dur_idx = self._waterfall_state.get(wf_key, 0)
        if dur_idx >= len(durations):
            return
        duration = durations[dur_idx]

        print(f"[TICKER] {sym} {edge} dur={duration}m")

        # OR desde barras CERRADAS
        or_data = self.client.get_or_from_closed_bars(sym, duration_mins=duration)
        if or_data is None:
            self.telegram.notify_error(f"Sin datos M15 para {sym}", "DataFeed")
            return

        range_high = or_data["high"]
        range_low = or_data["low"]
        rng = or_data["width"]

        if rng <= 0:
            self.telegram.notify_order_rejected(sym, "Rango cero o negativo")
            return

        # ATR14 filter
        if not self._passes_atr_filter(sym, rng):
            # Waterfall: advance to next duration
            self._advance_waterfall(setup)
            remaining = len(durations) - dur_idx - 1
            if remaining > 0:
                next_dur = durations[dur_idx + 1]
                print(f"[WATERFALL] {sym} {edge}: ATR fallo en {duration}m, intentara {next_dur}m")
            else:
                print(f"[WATERFALL] {sym} {edge}: ATR fallo en todas las duraciones. Skip day.")
            return

        self.telegram.notify_orb_detected(sym, range_high, range_low, rng)

        # ─── Edge routing ─────────────────────────────────────────
        if edge == "TREND_UP":
            tp_up = range_high + (rng * self.TREND_TP_MULTIPLIER)
            placed = self.om.place_trend_up_orders(sym, range_high, range_low, tp_up)

        elif edge == "MAGNET_CLOSE":
            pd_close = self.client.get_previous_day_close(sym)
            if pd_close is None:
                self.telegram.notify_error(f"Sin pd_close para {sym}", "DataFeed")
                return

            # Skip if pd_close inside OR (backtest parity)
            if range_low <= pd_close <= range_high:
                print(f"[MAGNET] {sym}: pd_close={pd_close:.5f} dentro del OR. Skip.")
                self.telegram.notify_order_rejected(sym, "MAGNET: pd_close dentro del OR")
                return

            placed = self.om.place_magnet_order(sym, range_high, range_low, pd_close)

        else:
            print(f"[ERROR] Edge desconocido: {edge}")
            return

        # _trades_today is incremented in _check_positions_and_fills on actual fill

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

                Path("logs/bot_heartbeat").touch()

                time.sleep(10)

        except KeyboardInterrupt:
            try:
                self.telegram.notify_bot_stopped("KeyboardInterrupt")
                time.sleep(1)
            except Exception:
                pass
            print("\nBot finalizado manualmente.")
        except Exception as e:
            try:
                self.telegram.notify_error(str(e), "MainLoop")
            except Exception:
                pass
            raise
        finally:
            try:
                self.telegram.stop_polling()
            except Exception:
                pass
            self.client.disconnect()


if __name__ == "__main__":
    bot = LiveTraderEngine()
    bot.run()
