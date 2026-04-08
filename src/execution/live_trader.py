"""
Live Trader Engine — Kha0sys3 v2
Motor de trading con 36 estrategias FADE/MOMENTUM/SHAKEOUT.
Riesgo dinamico 1-6% escalado por win rate historico.
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
    """Motor de trading ORB v2 con riesgo dinamico y multiples arquetipos."""

    HEARTBEAT_INTERVAL = 900
    HEALTH_CHECK_INTERVAL = 300
    POSITION_CHECK_INTERVAL = 10
    STALE_ORDER_CHECK_INTERVAL = 3600
    RECONNECT_CHECK_INTERVAL = 60

    def __init__(self, config_path: str = "src/execution/bot_config.json"):
        import json
        with open(config_path, "r") as f:
            cfg = json.load(f)

        # Risk scaling from config
        rs = cfg.get("risk_scaling", {})
        self.risk = DynamicRiskAllocator(
            min_risk=rs.get("min_risk", 0.01),
            max_risk=rs.get("max_risk", 0.06),
            min_wr=rs.get("min_wr", 0.57),
            max_wr=rs.get("max_wr", 0.91),
        )

        self.setups = cfg.get("portfolio", [])

        self.client = MT5Client()
        self.sl_guardian = SLGuardian()
        self.reporter = MT5Reporter()
        self.health_monitor = SystemHealthMonitor()

        self.telegram = TelegramCommandBot(
            stop_callback=self._on_stop_command,
            resume_callback=self._on_resume_command,
        )

        self.om = None

        self._control_lock = threading.Lock()
        self._paused = False

        self._start_time = None
        self._last_heartbeat = 0
        self._last_health_check = 0
        self._last_position_check = 0
        self._last_stale_check = 0
        self._last_reconnect_check = 0

        self._last_fired: dict[str, str] = {}
        self._known_positions: set[int] = set()
        self._trades_today = 0
        self._last_trade_day = ""

    # ─── Control ──────────────────────────────────────────────────

    def _on_stop_command(self):
        with self._control_lock:
            self._paused = True
        if self.om:
            try:
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
            self._last_trade_day = today

    # ─── Execution timing ────────────────────────────────────────

    def _get_exec_time(self, setup: dict) -> str:
        """Calcula HH:MM de ejecucion = magic_time + duration."""
        h, m = map(int, setup["magic_time"].split(":"))
        total_mins = h * 60 + m + setup["duration"]
        return f"{(total_mins // 60) % 24:02d}:{total_mins % 60:02d}"

    def _should_execute(self, setup: dict) -> bool:
        exec_time = self._get_exec_time(setup)
        now_hhmm = self._utc_now().strftime("%H:%M")
        if now_hhmm != exec_time:
            return False

        dedup_key = self._dedup_key(setup)
        if self._last_fired.get(dedup_key) == self._utc_now().strftime("%Y-%m-%d"):
            return False
        return True

    def _dedup_key(self, setup: dict) -> str:
        return f"{setup['sym']}_{setup['edge']}_{setup.get('session', '')}_{setup['duration']}"

    def _mark_fired(self, setup: dict):
        self._last_fired[self._dedup_key(setup)] = self._utc_now().strftime("%Y-%m-%d")

    # ─── ATR Filter ───────────────────────────────────────────────

    def _passes_atr_filter(self, symbol: str, or_width: float) -> bool:
        atr14 = self.client.calculate_atr14(symbol)
        if atr14 is None or atr14 <= 0:
            print(f"[ATR] No ATR14 para {symbol}. Skip.")
            return False

        ratio = or_width / atr14
        if not (0.1 <= ratio <= 0.8):
            print(f"[ATR] {symbol}: ratio={ratio:.3f} fuera de [0.1, 0.8]. Skip.")
            if self.telegram:
                self.telegram.notify_order_rejected(symbol, f"or_atr_ratio={ratio:.3f}")
            return False
        return True

    # ─── Monitoring ───────────────────────────────────────────────

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

    # ─── Fill & Position detection ────────────────────────────────

    def _check_positions_and_fills(self):
        now = time.time()
        if now - self._last_position_check < self.POSITION_CHECK_INTERVAL:
            return
        self._last_position_check = now

        # Check shakeout monitors
        self.om.check_shakeout_monitors()

        current_positions = mt5.positions_get()
        if current_positions is None:
            return

        current_tickets = {p.ticket for p in current_positions}

        # New fills
        new_tickets = current_tickets - self._known_positions
        for ticket in new_tickets:
            for p in current_positions:
                if p.ticket == ticket and p.magic == 1337:
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
                    result_text, emoji = "GANANCIA", "🦋"
                else:
                    result_text, emoji = "PERDIDA", "💥"

                risk_pct = self.risk.get_risk_percent(0.60)  # approximate
                msg = (
                    f"{emoji*10}\n"
                    "━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"   {emoji} <b>TRADE CERRADO</b>\n"
                    "━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"  Simbolo   | {deal.symbol}\n"
                    f"  Edge      | {comment}\n"
                    f"  Resultado | <b>{result_text}</b>\n"
                    f"  P&L       | <b>${profit:+,.2f}</b>\n"
                    f"  Volumen   | {deal.volume} lots\n"
                    f"  Precio    | {deal.price:.5f}\n"
                    "━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"  <i>{self._utc_now().strftime('%H:%M')} UTC</i>\n"
                    f"{emoji*10}"
                )
                self.telegram.send_sync(msg)

        # SL Guardian
        try:
            breached = self.sl_guardian.find_breached_positions(current_positions)
            for p in breached:
                self._emergency_close_position(p)
        except Exception as e:
            print(f"[SL_GUARDIAN] Error: {e}")

        self._known_positions = current_tickets

    def _emergency_close_position(self, position):
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
                f"  SL: {position.sl} | Precio: {position.price_current}"
            )

    # ─── Setup processing ─────────────────────────────────────────

    def _process_setup(self, setup: dict):
        """Procesa un setup cuando llega su ventana de ejecucion."""
        if not self._should_execute(setup):
            return

        self._mark_fired(setup)

        sym = setup["sym"]
        edge = setup["edge"]
        duration = setup["duration"]
        win_rate = setup.get("win_rate", 0.60)
        session = setup.get("session", "")

        if self.om.has_traded_today(sym, edge, session):
            return

        # Get OR data
        or_data = self.client.get_or_from_closed_bars(sym, duration_mins=duration)
        if or_data is None:
            self.telegram.notify_error(f"Sin datos M15 para {sym}", "DataFeed")
            return

        or_high = or_data["high"]
        or_low = or_data["low"]
        or_width = or_data["width"]

        if or_width <= 0:
            return

        if not self._passes_atr_filter(sym, or_width):
            return

        risk_pct = self.risk.get_risk_percent(win_rate)
        self.telegram.notify_orb_detected(sym, or_high, or_low, or_width)
        print(f"[EXEC] {sym} {edge} {session} {duration}m | WR={win_rate:.1%} Risk={risk_pct:.1%}")

        # Route to correct order type
        if edge == "FADE_UP":
            self.om.place_fade_up(sym, or_high, or_low, or_width, win_rate, session)

        elif edge == "FADE_DOWN":
            self.om.place_fade_down(sym, or_high, or_low, or_width, win_rate, session)

        elif edge == "MOMENTUM_UP":
            self.om.place_momentum_up(sym, or_high, or_low, or_width, win_rate, session)

        elif edge == "MOMENTUM_DOWN":
            self.om.place_momentum_down(sym, or_high, or_low, or_width, win_rate, session)

        elif edge in ("SHAKEOUT_UP", "SHAKEOUT_DOWN"):
            self.om.setup_shakeout_monitor(sym, edge, or_high, or_low, or_width, win_rate, session)

        else:
            print(f"[ERROR] Edge desconocido: {edge}")

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

        initial_positions = mt5.positions_get()
        if initial_positions:
            self._known_positions = {p.ticket for p in initial_positions}

        self.telegram.start_polling()
        time.sleep(2)

        # Startup summary
        n_setups = len(self.setups)
        symbols = list(set(s["sym"] for s in self.setups))
        edges = list(set(s["edge"] for s in self.setups))
        self.telegram.send_sync(
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "   🚀 <b>KHA0SYS3 v2 INICIADO</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  Setups    | {n_setups}\n"
            f"  Simbolos  | {len(symbols)}\n"
            f"  Edges     | {', '.join(edges)}\n"
            f"  Riesgo    | 1%-6% dinamico\n"
            "━━━━━━━━━━━━━━━━━━━━━━"
        )
        print(f"Kha0sys3 v2 Iniciado. {n_setups} setups, {len(symbols)} simbolos.")

        try:
            while True:
                self._reset_daily_counters()

                if not self._is_paused and self.telegram.is_active:
                    for setup in self.setups:
                        try:
                            self._process_setup(setup)
                        except Exception as e:
                            sym = setup.get("sym", "?")
                            self.telegram.notify_error(f"{sym}: {e}", "ProcessSetup")
                            print(f"[ERROR] {sym}: {e}")

                self._check_positions_and_fills()
                self._wipe_stale_orders()
                self._send_periodic_report()
                self._check_system_health()
                self._check_mt5_connection()

                Path("logs/bot_heartbeat").touch()
                time.sleep(10)

        except KeyboardInterrupt:
            try:
                self.telegram.send_sync("🛑 <b>Bot detenido manualmente</b>")
                time.sleep(1)
            except Exception:
                pass
            print("\nBot finalizado.")
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
