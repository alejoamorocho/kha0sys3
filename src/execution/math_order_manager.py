"""
Math Order Manager — Kha0sys3 parallel MATH runner
Magic 1338 — isolated from FADE (magic 1337).

Responsibilities:
  - detect_and_place: given enriched M15 bars, run the setup's detector on the
    LAST bar, and if fires today with no existing pending/open for this
    (symbol, setup_type) pair today, place a STOP order in the FLIPPED direction
    (INVERTED portfolio) at close +/- 0.5 * ATR, with expiration at +5 bars.
  - tick_pending: re-evaluate the direction guard on each pending MATH order;
    cancel if the ORIGINAL setup's guard indicator weakens
    (|guard| < 0.5 * |guard_at_placement|) or flips sign.
  - has_pending_or_open_today: dedup gate.

DRY_RUN=True (default): never calls mt5.order_send / orders_get mutations —
only logs "[DRY] would place STOP ..." and broadcasts to Telegram prefixed
with "[MATH][DRY]". A parallel in-memory pending-store is used so tick_pending
and dedup behave correctly during the DRY observation window.

IMPORTANT: Every MT5 read filters by magic=MAGIC_NUMBER_MATH so this manager
never touches or observes FADE state.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Optional

import polars as pl

from src.domain.constants import (
    MAGIC_NUMBER_MATH,
    MATH_WAIT_BARS,
    MATH_STOP_ATR_OFFSET,
    MATH_GUARD_WEAKEN_THRESHOLD,
)
from src.engine.run_math_momentum import detect_setups, _guard_indicator_col

try:
    import MetaTrader5 as mt5  # type: ignore
except Exception:  # pragma: no cover - allow tests without MT5 installed
    mt5 = None  # type: ignore


# Setup-type → original direction source column (for live direction guard)
# (delegates to the already-validated mapping in run_math_momentum)


def _flip(direction: str) -> str:
    """Invert LONG↔SHORT (INVERTED portfolio semantics)."""
    return "SHORT" if direction == "LONG" else "LONG"


@dataclass
class PendingMathOrder:
    ticket: int                 # -1 in DRY_RUN
    symbol: str                 # broker symbol (sym)
    internal_sym: str
    setup_type: str
    original_direction: str     # LONG/SHORT per detector
    flipped_direction: str      # what we actually placed
    stop_price: float
    tp_price: float
    sl_price: float
    atr: float
    guard_value_at_placement: float
    expiration_utc: datetime
    placed_date: str            # YYYY-MM-DD UTC
    dry_run: bool = True


class MathOrderManager:
    """Manages STOP orders for the MATH parallel runner (magic 1338)."""

    def __init__(self, client, magic: int = MAGIC_NUMBER_MATH,
                 dry_run: bool = True, telegram=None):
        self.client = client
        self.magic = magic
        self.dry_run = dry_run
        self.telegram = telegram

        # In-memory pending registry (source of truth in DRY, shadow in LIVE)
        self._pending: dict[str, PendingMathOrder] = {}
        # Dedup: (symbol, setup_type) → date string
        self._fired_today: dict[tuple[str, str], str] = {}

    # ─── Telegram helpers ─────────────────────────────────────────

    def _tg(self, msg: str):
        if self.telegram is None:
            return
        tag = "[MATH][DRY] " if self.dry_run else "[MATH] "
        try:
            if hasattr(self.telegram, "send_sync"):
                self.telegram.send_sync(tag + msg)
            elif hasattr(self.telegram, "_broadcast"):
                self.telegram._broadcast(tag + msg)
        except Exception as e:
            print(f"[MATH][TG] notify error: {e}")

    # ─── Dedup (1 trade per (sym, setup_type) per day) ────────────

    @staticmethod
    def _today_utc() -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")

    def has_pending_or_open_today(self, symbol: str, setup_type: str) -> bool:
        """True if we already placed / filled a MATH order for this pair today."""
        today = self._today_utc()
        if self._fired_today.get((symbol, setup_type)) == today:
            return True
        # Also check any live pending registered for this pair today
        for p in self._pending.values():
            if (p.symbol == symbol and p.setup_type == setup_type
                    and p.placed_date == today):
                return True
        # In LIVE mode, also sweep MT5 for magic=1338 orders/positions
        if not self.dry_run and mt5 is not None:
            try:
                orders = mt5.orders_get(symbol=symbol) or []
                for o in orders:
                    if getattr(o, "magic", 0) == self.magic \
                            and setup_type[:8] in (o.comment or ""):
                        return True
                positions = mt5.positions_get(symbol=symbol) or []
                for p in positions:
                    if getattr(p, "magic", 0) == self.magic \
                            and setup_type[:8] in (p.comment or ""):
                        return True
            except Exception:
                pass
        return False

    def _mark_fired(self, symbol: str, setup_type: str):
        self._fired_today[(symbol, setup_type)] = self._today_utc()

    # ─── Core placement ──────────────────────────────────────────

    def detect_and_place(self, setup_cfg: dict, bars: pl.DataFrame) -> Optional[PendingMathOrder]:
        """Run detector on `bars` (already math-enriched + session-filtered);
        if the LATEST bar fires and dedup allows, place an INVERTED STOP.

        Returns the PendingMathOrder record if placed, else None.
        """
        symbol = setup_cfg["sym"]
        internal = setup_cfg.get("internal_sym", symbol)
        setup_type = setup_cfg["setup_type"]

        if self.has_pending_or_open_today(symbol, setup_type):
            return None

        if bars is None or len(bars) == 0:
            return None

        try:
            sigs = detect_setups(bars, setup_type)
        except Exception as e:
            print(f"[MATH] detect_setups error {symbol}/{setup_type}: {e}")
            return None

        if len(sigs) == 0:
            return None

        # Only act on the most recent fired bar (last closed M15 bar)
        last_bar_time = bars["time"].max()
        latest = sigs.filter(pl.col("time") == last_bar_time)
        if len(latest) == 0:
            return None

        row = latest.row(-1, named=True)
        atr = row["atr_14"]
        if atr is None or atr <= 0:
            return None
        close = row["close"]
        orig_dir = row["direction"]
        guard_value = row["guard_value"]
        if guard_value is None:
            return None

        # INVERTED: flip direction
        flipped = _flip(orig_dir)

        # STOP placement = close +/- 0.5*ATR in the FLIPPED direction
        if flipped == "LONG":
            stop_price = close + MATH_STOP_ATR_OFFSET * atr
            tp_price = stop_price + setup_cfg["tp_atr_mult"] * atr
            sl_price = stop_price - setup_cfg["sl_atr_mult"] * atr
            order_type = "BUY_STOP"
        else:
            stop_price = close - MATH_STOP_ATR_OFFSET * atr
            tp_price = stop_price - setup_cfg["tp_atr_mult"] * atr
            sl_price = stop_price + setup_cfg["sl_atr_mult"] * atr
            order_type = "SELL_STOP"

        # Expiration: 5 M15 bars = 75 minutes
        expiration = datetime.now(timezone.utc) + timedelta(minutes=15 * MATH_WAIT_BARS)

        ticket = self._submit_stop(
            symbol=symbol, order_type=order_type, stop_price=stop_price,
            sl=sl_price, tp=tp_price, setup_type=setup_type,
            session=setup_cfg["session"], expiration=expiration,
        )
        if ticket is None:
            return None

        pending = PendingMathOrder(
            ticket=ticket, symbol=symbol, internal_sym=internal,
            setup_type=setup_type,
            original_direction=orig_dir, flipped_direction=flipped,
            stop_price=stop_price, tp_price=tp_price, sl_price=sl_price,
            atr=atr, guard_value_at_placement=float(guard_value),
            expiration_utc=expiration, placed_date=self._today_utc(),
            dry_run=self.dry_run,
        )
        key = f"{symbol}|{setup_type}|{self._today_utc()}"
        self._pending[key] = pending
        self._mark_fired(symbol, setup_type)

        msg = (
            f"{order_type} {symbol} @ {stop_price:.5f} "
            f"TP={tp_price:.5f} SL={sl_price:.5f} "
            f"(setup={setup_type} orig={orig_dir}→INVERTED={flipped} atr={atr:.5f})"
        )
        print(f"[MATH]{'[DRY]' if self.dry_run else ''} {msg}")
        self._tg(msg)
        return pending

    def _submit_stop(self, symbol: str, order_type: str, stop_price: float,
                     sl: float, tp: float, setup_type: str, session: str,
                     expiration: datetime) -> Optional[int]:
        """Send STOP to MT5 unless DRY_RUN. Returns ticket (or -1 in DRY)."""
        if self.dry_run:
            return -1

        if mt5 is None:
            print("[MATH] mt5 not available — treating as DRY")
            return -1

        try:
            sym_info = mt5.symbol_info(symbol)
            if sym_info is None:
                print(f"[MATH] symbol_info None for {symbol}")
                return None

            lot_min = getattr(sym_info, "volume_min", 0.01)
            volume = float(lot_min)  # Minimal viable — real sizing TBD in live phase

            type_map = {
                "BUY_STOP": mt5.ORDER_TYPE_BUY_STOP,
                "SELL_STOP": mt5.ORDER_TYPE_SELL_STOP,
            }
            req = {
                "action": mt5.TRADE_ACTION_PENDING,
                "symbol": symbol,
                "volume": volume,
                "type": type_map[order_type],
                "price": float(stop_price),
                "sl": float(sl),
                "tp": float(tp),
                "deviation": 10,
                "magic": self.magic,
                "comment": f"M|{setup_type[:8]}|{session[:6]}",
                "type_time": mt5.ORDER_TIME_SPECIFIED,
                "expiration": int(expiration.timestamp()),
                "type_filling": mt5.ORDER_FILLING_RETURN,
            }
            res = mt5.order_send(req)
            if res is None:
                print(f"[MATH] order_send None: {mt5.last_error()}")
                return None
            if res.retcode != mt5.TRADE_RETCODE_DONE:
                print(f"[MATH] order_send retcode={res.retcode}")
                return None
            return int(res.order)
        except Exception as e:
            print(f"[MATH] _submit_stop error: {e}")
            return None

    # ─── Direction guard (tick) ──────────────────────────────────

    def tick_pending(self, setup_cfg: dict, bars: pl.DataFrame) -> int:
        """Check guard indicator on the newest bar for every pending MATH order
        matching this setup. Cancel if the ORIGINAL guard weakens.
        Returns number of orders cancelled this tick.
        """
        symbol = setup_cfg["sym"]
        setup_type = setup_cfg["setup_type"]

        if bars is None or len(bars) == 0:
            return 0

        guard_col = _guard_indicator_col(setup_type)
        try:
            latest_guard = bars.sort("time")[guard_col][-1]
        except Exception:
            return 0
        if latest_guard is None:
            return 0

        cancelled = 0
        now = datetime.now(timezone.utc)

        for key in list(self._pending.keys()):
            p = self._pending[key]
            if p.symbol != symbol or p.setup_type != setup_type:
                continue

            # Expiration → drop from registry
            if now >= p.expiration_utc:
                self._pending.pop(key, None)
                continue

            g0 = p.guard_value_at_placement
            g0_sign = 1.0 if g0 > 0 else (-1.0 if g0 < 0 else 0.0)
            if g0_sign == 0:
                continue

            gv_aligned = float(latest_guard) * g0_sign
            weaken_thresh = MATH_GUARD_WEAKEN_THRESHOLD * abs(g0)
            if gv_aligned < weaken_thresh:
                # Guard weakened: cancel the pending STOP
                self._cancel(p)
                cancelled += 1
                self._pending.pop(key, None)
                self._tg(
                    f"guard-cancel {p.symbol} {p.setup_type} "
                    f"(g0={g0:.5f} now={latest_guard:.5f})"
                )
        return cancelled

    def _cancel(self, p: PendingMathOrder) -> bool:
        if self.dry_run or p.ticket < 0:
            print(f"[MATH][DRY] would cancel STOP ticket={p.ticket} {p.symbol}")
            return True
        if mt5 is None:
            return False
        try:
            req = {
                "action": mt5.TRADE_ACTION_REMOVE,
                "order": p.ticket,
                "symbol": p.symbol,
            }
            res = mt5.order_send(req)
            return bool(res and res.retcode == mt5.TRADE_RETCODE_DONE)
        except Exception as e:
            print(f"[MATH] cancel error: {e}")
            return False

    # ─── Housekeeping ────────────────────────────────────────────

    def sweep_expired(self) -> int:
        """Remove pending records whose expiration has passed (LIVE broker
        auto-expires the real order via ORDER_TIME_SPECIFIED)."""
        now = datetime.now(timezone.utc)
        dropped = 0
        for key in list(self._pending.keys()):
            if now >= self._pending[key].expiration_utc:
                self._pending.pop(key, None)
                dropped += 1
        return dropped

    def reset_daily_if_needed(self):
        """Clear dedup map when UTC date rolls over."""
        today = self._today_utc()
        # drop stale entries
        for k, v in list(self._fired_today.items()):
            if v != today:
                self._fired_today.pop(k, None)
