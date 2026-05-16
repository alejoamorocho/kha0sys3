"""K3M1 Telegram Notifier — formato consistente con TradersNotifier.

Reemplaza los mensajes _tg() inline de math_order_manager / live_math_trader
con un layout uniforme:
  - <b>[K3M1] EVENT_TYPE</b> header
  - ID:       <code>strategy_id</code>
  - Source:   indicator family (display friendly)
  - Tier:     K3M1  (magic 1338)
  - Symbol:   internal -> broker
  - ... resto especifico del evento
  - Time:     YYYY-MM-DD HH:MM UTC

Convive con el TelegramNotifier base existente — solo cambia FORMATO,
no token / chat_id.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from src.monitoring.telegram_notifier import TelegramNotifier
from src.domain.constants import MAGIC_NUMBER_MATH


# Display friendly de cada familia de indicadores math
SETUP_DISPLAY = {
    "HURST_TREND_MOM":     "Hurst exponent (R/S trend fade)",
    "KALMAN_INNOV_EXPAND": "Kalman innovation expand (fade)",
    "SPECTRAL_TREND_MOM":  "Spectral ratio trend (fade)",
    "VELOCITY_ACCEL_GO":   "Velocity + acceleration (fade)",
    "KAMA_CROSS_MOM":      "KAMA slope cross (fade)",
    "OLS_SLOPE_STRONG":    "OLS slope strong (fade)",
}

# Tag corto para el ID (mismos que SETUP_TAG en math_order_manager)
SETUP_TAG = {
    "KAMA_CROSS_MOM":      "KAMA",
    "SPECTRAL_TREND_MOM":  "SPECTRAL",
    "VELOCITY_ACCEL_GO":   "VELOCITY",
    "KALMAN_INNOV_EXPAND": "KALMAN",
    "HURST_TREND_MOM":     "HURST",
    "OLS_SLOPE_STRONG":    "OLS",
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _setup_display(setup_type: str) -> str:
    return SETUP_DISPLAY.get(setup_type, setup_type)


class MathNotifier:
    """Wrapper sobre TelegramNotifier para eventos K3M1-75 (magic 1338)."""

    def __init__(self, base: Optional[TelegramNotifier] = None):
        try:
            self.base = base or TelegramNotifier(risk_percent=0.001)
            self.enabled = True
        except Exception as e:
            print(f"[MathNotifier] DISABLED: {e}")
            self.base = None
            self.enabled = False

    def send(self, text: str) -> bool:
        if not self.enabled or not self.base:
            return False
        try:
            return self.base._broadcast(text)
        except Exception as e:
            print(f"[MathNotifier] send error: {e}")
            return False

    # ── Strategy identification block ────────────────────────────────────

    def _strategy_block(self, *, strategy_id: str, setup_type: str,
                         tf: str, session: str, dir_mode: str,
                         broker_sym: str, internal_sym: str,
                         robustness: str = "") -> str:
        src = _setup_display(setup_type)
        rob = f"  [{robustness}]" if robustness else ""
        return (
            f"ID:       <code>{strategy_id}</code>{rob}\n"
            f"Source:   {src}\n"
            f"Setup:    {setup_type}  |  {tf}  |  {session}  |  {dir_mode}\n"
            f"Tier:     K3M1-75  (magic {MAGIC_NUMBER_MATH})\n"
            f"Symbol:   {internal_sym} -&gt; {broker_sym}"
        )

    # ── Engine lifecycle ─────────────────────────────────────────────────

    def engine_started(self, *, mode: str, n_setups: int, by_tf: dict,
                        by_setup: dict, avg_wr: float, avg_pf_oos: float,
                        risk_pct: float, by_symbol: dict | None = None) -> None:
        tf_str = " | ".join(f"{t}: {n}" for t, n in sorted(by_tf.items()))
        setup_str = " | ".join(f"{SETUP_TAG.get(s,s[:5])}: {n}"
                                for s, n in sorted(by_setup.items(), key=lambda x: -x[1]))
        n_syms = len(by_symbol) if by_symbol else 0
        sym_str = ""
        if by_symbol:
            top_syms = " | ".join(
                f"{s}: {n}" for s, n in sorted(by_symbol.items(), key=lambda x: -x[1])[:8]
            )
            sym_str = f"Top symbols:  {top_syms}\n"
        self.send(
            f"<b>[K3M1] ENGINE STARTED</b>\n"
            f"Mode:         {mode}\n"
            f"Magic:        {MAGIC_NUMBER_MATH}\n"
            f"<b>Pairs operating: {n_setups}</b> (across {n_syms} symbols)\n"
            f"TF mix:       {tf_str}\n"
            f"Setups:       {setup_str}\n"
            f"{sym_str}"
            f"Avg WR:       {avg_wr*100:.1f}%\n"
            f"Avg PF OOS:   {avg_pf_oos:.2f}\n"
            f"Risk/trade:   {risk_pct*100:.2f}%\n"
            f"Time:         {_now_iso()}"
        )

    def engine_stopped(self, reason: str) -> None:
        self.send(
            f"<b>[K3M1] ENGINE STOPPED</b>\n"
            f"Reason: {reason}\n"
            f"Time:   {_now_iso()}"
        )

    def engine_paused(self) -> None:
        self.send(
            f"<b>[K3M1] ENGINE PAUSED</b>\n"
            f"No new placements\n"
            f"Time: {_now_iso()}"
        )

    def engine_resumed(self) -> None:
        self.send(
            f"<b>[K3M1] ENGINE RESUMED</b>\n"
            f"Time: {_now_iso()}"
        )

    # ── Order lifecycle ──────────────────────────────────────────────────

    def order_placed(self, *, strategy_id: str, setup_type: str, tf: str,
                      session: str, dir_mode: str, broker_sym: str,
                      internal_sym: str, robustness: str,
                      order_type: str, entry: float, sl: float, tp: float,
                      atr: float, rr: float, risk_pct: float,
                      expected_wr: float, pf_oos: float,
                      ticket: int, lots: float = 0.0) -> None:
        fmt = ".5f"
        if "JPY" in internal_sym:
            fmt = ".3f"
        risk_price = abs(entry - sl)
        ticket_str = "DRY" if ticket == -1 else str(ticket)
        self.send(
            f"<b>[K3M1] ORDER PLACED  [{robustness}]</b>\n"
            f"{self._strategy_block(strategy_id=strategy_id, setup_type=setup_type, tf=tf, session=session, dir_mode=dir_mode, broker_sym=broker_sym, internal_sym=internal_sym)}\n"
            f"Type:     {order_type}\n"
            f"Entry:    {entry:{fmt}}\n"
            f"SL:       {sl:{fmt}}  (risk {risk_price:{fmt}})\n"
            f"TP:       {tp:{fmt}}  (R:R {rr:.2f})\n"
            f"ATR:      {atr:.5f}\n"
            f"Lots:     {lots}\n"
            f"Risk:     {risk_pct*100:.2f}%  (expected WR {expected_wr:.2f})\n"
            f"PF OOS:   {pf_oos:.2f}\n"
            f"Ticket:   {ticket_str}\n"
            f"Time:     {_now_iso()}"
        )

    def fill(self, *, strategy_id: str, setup_type: str, tf: str,
              session: str, dir_mode: str, broker_sym: str,
              internal_sym: str, entry: float, lots: float,
              ticket: int) -> None:
        fmt = ".3f" if "JPY" in internal_sym else ".5f"
        self.send(
            f"<b>[K3M1] LIVE FILL</b>\n"
            f"{self._strategy_block(strategy_id=strategy_id, setup_type=setup_type, tf=tf, session=session, dir_mode=dir_mode, broker_sym=broker_sym, internal_sym=internal_sym)}\n"
            f"Entry:    {entry:{fmt}}\n"
            f"Lots:     {lots}\n"
            f"Ticket:   {ticket}\n"
            f"Time:     {_now_iso()}"
        )

    def position_closed(self, *, strategy_id: str, setup_type: str, tf: str,
                          session: str, dir_mode: str, broker_sym: str,
                          internal_sym: str, exit_price: float,
                          reason: str, r_multiple: Optional[float] = None,
                          hold_minutes: Optional[int] = None,
                          profit: Optional[float] = None) -> None:
        fmt = ".3f" if "JPY" in internal_sym else ".5f"
        emoji = ""
        if r_multiple is not None:
            emoji = f"+{r_multiple:.2f}R" if r_multiple > 0 else f"{r_multiple:.2f}R"
        text = (
            f"<b>[K3M1] LIVE CLOSE  {emoji}</b>\n"
            f"{self._strategy_block(strategy_id=strategy_id, setup_type=setup_type, tf=tf, session=session, dir_mode=dir_mode, broker_sym=broker_sym, internal_sym=internal_sym)}\n"
            f"Exit:     {exit_price:{fmt}}\n"
            f"Reason:   {reason}\n"
        )
        if profit is not None:
            text += f"P/L:      {profit:+.2f}\n"
        if hold_minutes is not None:
            if hold_minutes < 60:
                h = f"{hold_minutes}min"
            elif hold_minutes < 1440:
                h = f"{hold_minutes/60:.1f}h"
            else:
                h = f"{hold_minutes/1440:.1f}d"
            text += f"Hold:     {h}\n"
        text += f"Time:     {_now_iso()}"
        self.send(text)

    def guard_cancel(self, *, strategy_id: str, setup_type: str, tf: str,
                       broker_sym: str, internal_sym: str, ticket: int,
                       reason: str) -> None:
        self.send(
            f"<b>[K3M1] GUARD CANCEL</b>\n"
            f"ID:       <code>{strategy_id}</code>\n"
            f"Setup:    {setup_type}  |  {tf}\n"
            f"Symbol:   {internal_sym} -&gt; {broker_sym}\n"
            f"Ticket:   {ticket}\n"
            f"Reason:   {reason}\n"
            f"Time:     {_now_iso()}"
        )

    def order_rejected(self, *, strategy_id: str, setup_type: str,
                        broker_sym: str, retcode: int, reason: str) -> None:
        self.send(
            f"<b>[K3M1] ORDER REJECTED</b>\n"
            f"ID:       <code>{strategy_id}</code>\n"
            f"Setup:    {setup_type}\n"
            f"Symbol:   {broker_sym}\n"
            f"Retcode:  {retcode}\n"
            f"Reason:   {reason}\n"
            f"Time:     {_now_iso()}"
        )

    # ── Heartbeat + maintenance ──────────────────────────────────────────

    def heartbeat(self, *, balance: float, equity: float, margin: float,
                    free_margin: float, n_open: int, n_pending: int,
                    by_tf: dict, uptime_hours: float) -> None:
        tf_str = " | ".join(f"{t}: {n}" for t, n in sorted(by_tf.items()))
        self.send(
            f"<b>[K3M1] HEARTBEAT</b>\n"
            f"Open:        {n_open}\n"
            f"Pending:     {n_pending}\n"
            f"TF mix:      {tf_str}\n"
            f"Balance:     {balance:.2f}\n"
            f"Equity:      {equity:.2f}\n"
            f"Margin:      {margin:.2f}\n"
            f"Free mgn:    {free_margin:.2f}\n"
            f"Uptime:      {uptime_hours:.1f}h\n"
            f"Time:        {_now_iso()}"
        )

    def stale_sweep(self, *, cancelled: int, age_minutes: int) -> None:
        self.send(
            f"<b>[K3M1] STALE SWEEP</b>\n"
            f"Cancelled:  {cancelled} STOP orders\n"
            f"Age limit:  {age_minutes} min\n"
            f"Time:       {_now_iso()}"
        )

    def session_end_cancel(self, *, broker_sym: str, session: str,
                            ticket: int) -> None:
        self.send(
            f"<b>[K3M1] SESSION-END CANCEL</b>\n"
            f"Symbol:   {broker_sym}\n"
            f"Session:  {session} (ended)\n"
            f"Ticket:   {ticket}\n"
            f"Time:     {_now_iso()}"
        )

    def sl_guardian_close(self, *, broker_sym: str, ticket: int,
                           reason: str) -> None:
        self.send(
            f"<b>[K3M1] SL GUARDIAN CLOSE</b>\n"
            f"Symbol:   {broker_sym}\n"
            f"Ticket:   {ticket}\n"
            f"Reason:   {reason}\n"
            f"Action:   closed at market\n"
            f"Time:     {_now_iso()}"
        )

    def error(self, context: str, msg: str) -> None:
        self.send(
            f"<b>[K3M1] ERROR</b>\n"
            f"Context:  {context}\n"
            f"Msg:      {msg[:300]}\n"
            f"Time:     {_now_iso()}"
        )

    def fatal(self, msg: str) -> None:
        self.send(
            f"<b>[K3M1] ENGINE FATAL</b>\n"
            f"{msg}\n"
            f"Time:     {_now_iso()}"
        )
