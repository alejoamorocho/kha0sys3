"""Traders Telegram Notifier — wraps TelegramNotifier para Tier 1 Swing + Tier 2 ORB.

Eventos:
  ENGINE_STARTED        — bot arranca con resumen del portfolio
  SETUP_DETECTED        — setup D1 swing nuevo (informativo, antes de fill)
  ORDER_PLACED          — STOP buy colocado en pivot
  ORDER_REJECTED        — fallo broker (retcode)
  FILL                  — STOP triggered, posicion abierta
  PARTIAL_CLOSE         — partial 30%/50% cerrado
  TRAIL_UPDATE          — SL movido up por SMA D1
  TIME_STOP             — cerrado por time-stop (Zanger 2-3d sin TP1)
  MAX_HOLD              — cerrado por timeout (swing 30-60d / ORB 4-8h)
  POSITION_CLOSED       — cierre detectado en broker (TP/SL/manual)
  HEARTBEAT             — snapshot periodico (open positions + pendings)
  ERROR                 — excepcion no recuperable

Todos los mensajes prefijo "[TRADERS]" + sufijo magic para distinguir
de los eventos del K3M1-75 (magic 1338).
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from src.monitoring.telegram_notifier import TelegramNotifier
from src.domain.constants import (
    MAGIC_NUMBER_TRADERS_SWING, MAGIC_NUMBER_TRADERS_ORB,
)


TRADER_DISPLAY = {
    "Minervini": "Mark Minervini (SEPA + VCP)",
    "Zanger": "Dan Zanger (Flag/Cup&Handle)",
    "Qulla": "Kristjan Qullamaggie (HTF / EP / ORB)",
    "Ryan": "David Ryan (CAN SLIM + Ants)",
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _tier_label(magic: int) -> str:
    if magic == MAGIC_NUMBER_TRADERS_SWING:
        return "T1-SWING"
    if magic == MAGIC_NUMBER_TRADERS_ORB:
        return "T2-ORB"
    return f"M{magic}"


class TradersNotifier:
    """Wrapper sobre TelegramNotifier para eventos del traders bot."""

    def __init__(self, base: Optional[TelegramNotifier] = None,
                 risk_percent: float = 0.001):
        try:
            self.base = base or TelegramNotifier(risk_percent=risk_percent)
            self.enabled = True
        except Exception as e:
            print(f"[TradersNotifier] DISABLED — telegram unavailable: {e}")
            self.base = None
            self.enabled = False

    def _send(self, text: str) -> bool:
        if not self.enabled or not self.base:
            return False
        try:
            return self.base._broadcast(text)
        except Exception as e:
            print(f"[TradersNotifier] send error: {e}")
            return False

    # ── Engine lifecycle ─────────────────────────────────────────────────

    def engine_started(self, mode: str, swing_n: int, orb_n: int,
                        risk_pct: float, broker_offset_h: int,
                        symbols: list[str]) -> None:
        text = (
            f"<b>[TRADERS] ENGINE STARTED</b>\n"
            f"Mode:           {mode}\n"
            f"T1-SWING:       {swing_n} estrategias (magic {MAGIC_NUMBER_TRADERS_SWING})\n"
            f"T2-ORB:         {orb_n} estrategias (magic {MAGIC_NUMBER_TRADERS_ORB})\n"
            f"Risk/trade:     {risk_pct*100:.2f}%\n"
            f"Broker offset:  {broker_offset_h:+d}h vs UTC\n"
            f"Symbols ({len(symbols)}): {', '.join(symbols)}\n"
            f"Time:           {_now_iso()}"
        )
        self._send(text)

    def engine_stopped(self, reason: str = "Manual") -> None:
        self._send(
            f"<b>[TRADERS] ENGINE STOPPED</b>\n"
            f"Reason: {reason}\n"
            f"Time:   {_now_iso()}"
        )

    def error(self, context: str, msg: str) -> None:
        self._send(
            f"<b>[TRADERS] ERROR</b>\n"
            f"Context: {context}\n"
            f"Msg:     {msg[:300]}\n"
            f"Time:    {_now_iso()}"
        )

    # ── Strategy identification ──────────────────────────────────────────

    def _strategy_block(self, *, strategy_id: str, trader: str, setup_type: str,
                         variant: str, magic: int, broker_sym: str,
                         internal_sym: str) -> str:
        trader_disp = TRADER_DISPLAY.get(trader, trader)
        return (
            f"ID:       <code>{strategy_id}</code>\n"
            f"Trader:   {trader_disp}\n"
            f"Setup:    {setup_type} ({variant})\n"
            f"Tier:     {_tier_label(magic)}  (magic {magic})\n"
            f"Symbol:   {internal_sym} -> {broker_sym}"
        )

    # ── Setup / order lifecycle ──────────────────────────────────────────

    def setup_detected(self, *, strategy_id: str, trader: str, setup_type: str,
                        variant: str, magic: int, broker_sym: str,
                        internal_sym: str, pivot: float, atr_d1: float,
                        valid_until: str, n_active: int) -> None:
        self._send(
            f"<b>[TRADERS] SETUP DETECTED</b>\n"
            f"{self._strategy_block(strategy_id=strategy_id, trader=trader, setup_type=setup_type, variant=variant, magic=magic, broker_sym=broker_sym, internal_sym=internal_sym)}\n"
            f"Pivot:    {pivot:.5f}\n"
            f"ATR D1:   {atr_d1:.5f}\n"
            f"Valid:    hasta {valid_until} ({n_active} setup{'s' if n_active != 1 else ''} activo{'s' if n_active != 1 else ''})\n"
            f"Time:     {_now_iso()}"
        )

    def order_placed(self, *, strategy_id: str, trader: str, setup_type: str,
                      variant: str, magic: int, broker_sym: str,
                      internal_sym: str, entry: float, sl: float, tp: float,
                      lots: float, ticket: int, expiration_minutes: int) -> None:
        risk_R = abs(entry - sl)
        rr = abs(tp - entry) / risk_R if risk_R > 0 else 0
        self._send(
            f"<b>[TRADERS] ORDER PLACED</b>\n"
            f"{self._strategy_block(strategy_id=strategy_id, trader=trader, setup_type=setup_type, variant=variant, magic=magic, broker_sym=broker_sym, internal_sym=internal_sym)}\n"
            f"Type:     BUY_STOP\n"
            f"Entry:    {entry:.5f}\n"
            f"SL:       {sl:.5f}  (risk {risk_R:.5f})\n"
            f"TP1:      {tp:.5f}  (R:R {rr:.2f})\n"
            f"Lots:     {lots}\n"
            f"Ticket:   {ticket}\n"
            f"Expires:  {expiration_minutes} min\n"
            f"Time:     {_now_iso()}"
        )

    def order_rejected(self, *, strategy_id: str, magic: int,
                        broker_sym: str, reason: str) -> None:
        self._send(
            f"<b>[TRADERS] ORDER REJECTED</b>\n"
            f"ID:       <code>{strategy_id}</code>\n"
            f"Tier:     {_tier_label(magic)}\n"
            f"Symbol:   {broker_sym}\n"
            f"Reason:   {reason}\n"
            f"Time:     {_now_iso()}"
        )

    def fill(self, *, strategy_id: str, trader: str, setup_type: str,
              variant: str, magic: int, broker_sym: str, internal_sym: str,
              entry: float, lots: float, ticket: int) -> None:
        self._send(
            f"<b>[TRADERS] FILL</b>\n"
            f"{self._strategy_block(strategy_id=strategy_id, trader=trader, setup_type=setup_type, variant=variant, magic=magic, broker_sym=broker_sym, internal_sym=internal_sym)}\n"
            f"Entry:    {entry:.5f}\n"
            f"Lots:     {lots}\n"
            f"Ticket:   {ticket}\n"
            f"Time:     {_now_iso()}"
        )

    def partial_close(self, *, strategy_id: str, trader: str, magic: int,
                       broker_sym: str, internal_sym: str, partial_idx: int,
                       trigger: str, trigger_value, fill_price: float,
                       closed_lots: float, remaining_lots: float,
                       r_multiple: float) -> None:
        emoji = "+" if r_multiple > 0 else "-"
        self._send(
            f"<b>[TRADERS] PARTIAL CLOSE {emoji}{abs(r_multiple):.2f}R</b>\n"
            f"ID:       <code>{strategy_id}</code>\n"
            f"Trader:   {trader}\n"
            f"Tier:     {_tier_label(magic)}\n"
            f"Symbol:   {internal_sym} -> {broker_sym}\n"
            f"Partial:  #{partial_idx+1}  ({trigger}={trigger_value})\n"
            f"Price:    {fill_price:.5f}\n"
            f"Closed:   {closed_lots} lots\n"
            f"Remain:   {remaining_lots} lots\n"
            f"Time:     {_now_iso()}"
        )

    def trail_update(self, *, strategy_id: str, magic: int,
                      broker_sym: str, old_sl: float, new_sl: float,
                      sma_period: int) -> None:
        self._send(
            f"<b>[TRADERS] TRAIL UPDATE</b>\n"
            f"ID:       <code>{strategy_id}</code>\n"
            f"Tier:     {_tier_label(magic)}\n"
            f"Symbol:   {broker_sym}\n"
            f"SL:       {old_sl:.5f} -> <b>{new_sl:.5f}</b>\n"
            f"Source:   SMA{sma_period} D1\n"
            f"Time:     {_now_iso()}"
        )

    def position_closed(self, *, strategy_id: str, trader: str, setup_type: str,
                          variant: str, magic: int, broker_sym: str,
                          internal_sym: str, reason: str,
                          final_r: Optional[float] = None,
                          hold_minutes: Optional[int] = None) -> None:
        emoji = ""
        if final_r is not None:
            emoji = (f"+{final_r:.2f}R" if final_r > 0
                     else f"{final_r:.2f}R")
        text = (
            f"<b>[TRADERS] POSITION CLOSED  {emoji}</b>\n"
            f"{self._strategy_block(strategy_id=strategy_id, trader=trader, setup_type=setup_type, variant=variant, magic=magic, broker_sym=broker_sym, internal_sym=internal_sym)}\n"
            f"Reason:   {reason}\n"
        )
        if hold_minutes is not None:
            if hold_minutes < 60:
                hold_str = f"{hold_minutes}min"
            elif hold_minutes < 1440:
                hold_str = f"{hold_minutes/60:.1f}h"
            else:
                hold_str = f"{hold_minutes/1440:.1f}d"
            text += f"Hold:     {hold_str}\n"
        text += f"Time:     {_now_iso()}"
        self._send(text)

    def heartbeat(self, *, swing_open: int, swing_pending: int,
                    orb_open: int, orb_pending: int,
                    balance: float, equity: float) -> None:
        self._send(
            f"<b>[TRADERS] HEARTBEAT</b>\n"
            f"T1-SWING:  {swing_open} open, {swing_pending} pending\n"
            f"T2-ORB:    {orb_open} open, {orb_pending} pending\n"
            f"Balance:   {balance:.2f}\n"
            f"Equity:    {equity:.2f}\n"
            f"Time:      {_now_iso()}"
        )
