"""AMO8 Order Manager — Kha0sys3 parallel ORB runner.

Magic 8338 — isolated from MATH (1338). Filters every MT5 read by magic so
it never touches MATH state.

Responsibilities:
  - has_pending_or_open_today(symbol, pattern_id, direction): dedup gate per day
  - place_market(strategy_cfg, entry_price, atr_at_setup, or_width): submits a
    MARKET order with TP/SL precomputed by mode (ATR or OR_FIXED).
  - sweep_max_hold(): force-close positions older than max_hold_min.
  - DRY_RUN preserves all logic but skips order_send/position_close.

V1 supports only MARKET entries with single TP/SL (modes ATR and OR_FIXED).
V2 will add partial exits (DOC + SWING modes).
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

try:
    import MetaTrader5 as mt5  # type: ignore
except Exception:  # pragma: no cover
    mt5 = None  # type: ignore


MAGIC_NUMBER_AMO8 = 8338

# MT5 retcodes handled gracefully
_RETCODE_INVALID_PRICE = 10015
_RETCODE_INVALID_STOPS = 10016
_RETCODE_MARKET_CLOSED = 10018
_RETCODE_CLIENT_DISABLES_AT = 10027
_RETCODE_INVALID_FILL = 10030
_RETCODE_DONE = 10009
_RETCODE_DONE_PARTIAL = 10010

_TICK_MAX_AGE_SEC = 120


# Pattern_id → short tag for MT5 comment (max 31 chars total in comment)
_EVENT_TAG = {
    "FALSE_BREAK_UP":   "FBU",
    "FALSE_BREAK_DOWN": "FBD",
    "BREAK_UP":         "BU",
    "BREAK_DOWN":       "BD",
    "MITIG_PD_MID":     "MPM",
    "MITIG_PD_CLOSE":   "MPC",
    "REENTRY_PD_OR_HIGH": "RPH",
    "REENTRY_PD_OR_LOW":  "RPL",
}


def make_order_comment(strategy_id: str, mode: str, event_type: str) -> str:
    """MT5 order comment: 'A8|<MODE>|<EVENT>|<id_tail>'. <= 31 chars.

    Single source of truth — placement + sweep matching use this.
    """
    event_tag = _EVENT_TAG.get(event_type, event_type[:3])
    # Take last 12 chars of strategy_id for uniqueness (e.g. "_OR_FIXED_42")
    id_tail = strategy_id.split("_")[-1][:8]
    return f"A8|{mode[:3]}|{event_tag}|{id_tail}"


@dataclass
class PendingAmoOrder:
    """Lightweight tracking for DRY mode + max-hold sweeps."""
    ticket: int                  # -1 in DRY
    symbol: str                  # broker symbol
    internal_sym: str
    strategy_id: str
    pattern_id: str
    direction: str               # LONG / SHORT
    entry_price: float
    sl: float
    tp: float
    placed_at: datetime          # UTC
    max_hold_min: int
    atr_at_setup: float
    or_width: float
    mode: str


class AmoOrderManager:
    """Order manager for the AMO8 portfolio (magic 8338)."""

    def __init__(self, dry_run: bool = True, telegram=None):
        self.dry_run = dry_run
        self.telegram = telegram
        # In-memory dedup: {(internal_sym, pattern_id, direction, trade_date): True}
        self._fired_today: dict[tuple, str] = {}
        # In-memory pending tracking for DRY mode and max-hold sweep
        self._pending: list[PendingAmoOrder] = []

    # ───────────────────────── Dedup ─────────────────────────

    @staticmethod
    def _today_utc() -> str:
        return datetime.now(timezone.utc).date().isoformat()

    def has_fired_today(self, internal_sym: str, pattern_id: str, direction: str) -> bool:
        """Has this exact pattern slot already fired today (live OR DRY)?"""
        today = self._today_utc()
        key = (internal_sym, pattern_id, direction)
        if self._fired_today.get(key) == today:
            return True
        # Also check live MT5 for any AMO8 position on this slot today
        if mt5 is not None and not self.dry_run:
            comment_prefix = "A8|"  # ours
            for getter in (mt5.positions_get, mt5.orders_get):
                try:
                    items = getter() or []
                    for it in items:
                        if int(getattr(it, "magic", 0)) != MAGIC_NUMBER_AMO8:
                            continue
                        if not str(getattr(it, "comment", "")).startswith(comment_prefix):
                            continue
                        # We don't try to parse the exact slot from comment;
                        # if ANY AMO8 position is open on this symbol+pattern+dir
                        # within the last 24h, treat as fired.
                        op_time = datetime.fromtimestamp(
                            int(getattr(it, "time_setup", 0)), tz=timezone.utc
                        )
                        if (datetime.now(timezone.utc) - op_time).days == 0:
                            # Match by symbol (broker_sym alignment happens upstream)
                            broker_sym = getattr(it, "symbol", "")
                            if broker_sym == self._broker_sym_for(internal_sym):
                                return True
                except Exception:
                    pass
        return False

    def _mark_fired(self, internal_sym: str, pattern_id: str, direction: str) -> None:
        self._fired_today[(internal_sym, pattern_id, direction)] = self._today_utc()

    def _broker_sym_for(self, internal_sym: str) -> str:
        """Lookup helper: relies on caller to pass broker_sym, but kept for sanity."""
        # In practice the caller supplies broker_sym; this is a fallback.
        return internal_sym

    # ───────────────────────── Placement ─────────────────────────

    def place_market(
        self,
        strategy: dict,
        entry_price: float,
        atr_at_setup: float,
        or_width: float,
        risk_per_trade: float,
        account_balance: float,
    ) -> Optional[PendingAmoOrder]:
        """Place a MARKET order for an AMO8 strategy.

        TP/SL computed from strategy.exit_rules.mode:
          - ATR: SL = sl_atr_mult * atr,  TP = tp_atr_mult * atr
          - OR_FIXED: SL = sl_or_frac * or_width, TP = tp_or_frac * or_width
        """
        internal_sym = strategy["internal_sym"]
        broker_sym = strategy["broker_sym"]
        direction = strategy["direction"]
        rules = strategy["exit_rules"]
        mode = rules["mode"]

        sign = 1.0 if direction == "LONG" else -1.0

        if mode == "ATR":
            sl_dist = rules["sl_atr_mult"] * atr_at_setup
            tp_dist = rules["tp_atr_mult"] * atr_at_setup
        elif mode == "OR_FIXED":
            sl_dist = rules["sl_or_frac"] * or_width
            tp_dist = rules["tp_or_frac"] * or_width
        else:
            raise ValueError(f"AMO8 V1 only supports ATR and OR_FIXED; got {mode}")

        if sl_dist <= 0 or tp_dist <= 0:
            print(f"[AMO8] skip {strategy['id']}: invalid sl/tp distances "
                  f"sl={sl_dist:.6f} tp={tp_dist:.6f}")
            return None

        sl_price = entry_price - sign * sl_dist
        tp_price = entry_price + sign * tp_dist

        # Volume sizing: risk_per_trade × balance / (sl_dist × tick_value / tick_size × vol_min_step)
        volume = self._compute_volume(
            broker_sym, sl_dist, risk_per_trade, account_balance
        )
        if volume <= 0:
            print(f"[AMO8] skip {strategy['id']}: computed volume <= 0")
            return None

        comment = make_order_comment(strategy["id"], mode, strategy["event_type"])

        if self.dry_run:
            print(f"[AMO8][DRY] would place MARKET {direction} {broker_sym} "
                  f"vol={volume} entry≈{entry_price:.5f} sl={sl_price:.5f} "
                  f"tp={tp_price:.5f} comment='{comment}'")
            ticket = -1
            ok = True
        else:
            ticket, ok = self._send_market_order(
                broker_sym, direction, volume, sl_price, tp_price, comment
            )
            if not ok:
                print(f"[AMO8] order_send failed for {strategy['id']}")
                return None

        order = PendingAmoOrder(
            ticket=ticket,
            symbol=broker_sym,
            internal_sym=internal_sym,
            strategy_id=strategy["id"],
            pattern_id=strategy["pattern_id"],
            direction=direction,
            entry_price=entry_price,
            sl=sl_price,
            tp=tp_price,
            placed_at=datetime.now(timezone.utc),
            max_hold_min=int(rules["max_hold_min"]),
            atr_at_setup=atr_at_setup,
            or_width=or_width,
            mode=mode,
        )
        self._pending.append(order)
        self._mark_fired(internal_sym, strategy["pattern_id"], direction)

        if self.telegram is not None:
            try:
                self.telegram.send_message(
                    f"[AMO8] ORDER PLACED\n"
                    f"strategy: {strategy['id']}\n"
                    f"symbol: {broker_sym} ({internal_sym})\n"
                    f"dir: {direction} mode: {mode}\n"
                    f"entry: {entry_price:.5f}  sl: {sl_price:.5f}  tp: {tp_price:.5f}\n"
                    f"vol: {volume}  comment: {comment}\n"
                    f"expected: PF={strategy.get('expected_pf', '?')} "
                    f"WR={strategy.get('expected_wr', '?')}"
                )
            except Exception as e:
                print(f"[AMO8] telegram error: {e}")

        return order

    # ───────────────────────── Sizing ─────────────────────────

    def _compute_volume(
        self, broker_sym: str, sl_distance_price: float,
        risk_per_trade: float, account_balance: float,
    ) -> float:
        """Compute lot volume so loss == risk_per_trade × balance at SL hit."""
        if mt5 is None:
            return 0.01  # placeholder for DRY without MT5
        info = mt5.symbol_info(broker_sym)
        if info is None:
            print(f"[AMO8] symbol_info({broker_sym}) returned None")
            return 0.0
        tick_size = float(info.trade_tick_size or info.point or 0.00001)
        tick_value = float(info.trade_tick_value or 1.0)
        vol_min = float(info.volume_min or 0.01)
        vol_step = float(info.volume_step or 0.01)
        vol_max = float(info.volume_max or 100.0)
        risk_usd = risk_per_trade * account_balance
        if tick_size <= 0 or tick_value <= 0:
            return 0.0
        usd_per_lot_per_price_unit = tick_value / tick_size
        lots = risk_usd / (sl_distance_price * usd_per_lot_per_price_unit)
        # Snap to vol_step
        lots = math.floor(lots / vol_step) * vol_step
        lots = max(vol_min, min(lots, vol_max))
        return round(lots, 2)

    # ───────────────────────── MT5 order_send ─────────────────────────

    def _send_market_order(
        self, broker_sym: str, direction: str, volume: float,
        sl_price: float, tp_price: float, comment: str,
    ) -> tuple[int, bool]:
        """Submit MARKET order. Returns (ticket, ok)."""
        if mt5 is None:
            return -1, False
        # Tick freshness check
        tick = mt5.symbol_info_tick(broker_sym)
        if tick is None or int(tick.time) == 0:
            print(f"[AMO8] no tick for {broker_sym}, skip")
            return -1, False
        age = (datetime.now(timezone.utc).timestamp() - int(tick.time))
        if abs(age) > _TICK_MAX_AGE_SEC:
            print(f"[AMO8] stale tick for {broker_sym} ({age:.0f}s), skip")
            return -1, False

        order_type = mt5.ORDER_TYPE_BUY if direction == "LONG" else mt5.ORDER_TYPE_SELL
        price = tick.ask if direction == "LONG" else tick.bid

        req = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": broker_sym,
            "volume": float(volume),
            "type": order_type,
            "price": float(price),
            "sl": float(sl_price),
            "tp": float(tp_price),
            "deviation": 10,
            "magic": MAGIC_NUMBER_AMO8,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(req)
        if result is None:
            print(f"[AMO8] order_send returned None for {broker_sym}")
            return -1, False
        rc = int(getattr(result, "retcode", 0))
        if rc not in (_RETCODE_DONE, _RETCODE_DONE_PARTIAL):
            print(f"[AMO8] order_send retcode={rc} for {broker_sym} "
                  f"({getattr(result, 'comment', '')})")
            return -1, False
        return int(getattr(result, "order", -1)), True

    # ───────────────────────── Max-hold sweep ─────────────────────────

    def sweep_max_hold(self) -> int:
        """Force-close any AMO8 position older than its max_hold_min.

        Returns count of positions force-closed.
        """
        if self.dry_run or mt5 is None:
            return 0
        now = datetime.now(timezone.utc)
        try:
            positions = mt5.positions_get() or []
        except Exception:
            return 0
        closed = 0
        for p in positions:
            if int(getattr(p, "magic", 0)) != MAGIC_NUMBER_AMO8:
                continue
            opened = datetime.fromtimestamp(int(getattr(p, "time", 0)), tz=timezone.utc)
            comment = str(getattr(p, "comment", ""))
            # Find max_hold from our local tracking; fallback to 600 min default
            max_hold_min = 600
            for po in self._pending:
                if po.ticket == int(getattr(p, "ticket", -1)):
                    max_hold_min = po.max_hold_min
                    break
            age_min = (now - opened).total_seconds() / 60
            if age_min < max_hold_min:
                continue
            ok = self._force_close(p)
            if ok:
                closed += 1
                if self.telegram is not None:
                    try:
                        self.telegram.send_message(
                            f"[AMO8] MAX_HOLD CLOSE\n"
                            f"ticket: {int(p.ticket)}  symbol: {p.symbol}\n"
                            f"age: {age_min:.0f}min (limit {max_hold_min}min)\n"
                            f"profit_R: see broker"
                        )
                    except Exception:
                        pass
        return closed

    def _force_close(self, position) -> bool:
        """Close a position at market."""
        if mt5 is None:
            return False
        sym = position.symbol
        tick = mt5.symbol_info_tick(sym)
        if tick is None:
            return False
        is_long = int(position.type) == 0  # BUY = 0
        close_type = mt5.ORDER_TYPE_SELL if is_long else mt5.ORDER_TYPE_BUY
        price = tick.bid if is_long else tick.ask
        req = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": sym,
            "volume": float(position.volume),
            "type": close_type,
            "position": int(position.ticket),
            "price": float(price),
            "deviation": 20,
            "magic": MAGIC_NUMBER_AMO8,
            "comment": "A8|MAXHOLD",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(req)
        if result is None:
            return False
        return int(getattr(result, "retcode", 0)) in (_RETCODE_DONE, _RETCODE_DONE_PARTIAL)
