"""AMO8 Order Manager — Kha0sys3 parallel ORB runner.

Magic 8338 — isolated from MATH (1338). Filters every MT5 read by magic so
it never touches MATH state.

Responsibilities:
  - has_pending_or_open_today(symbol, pattern_id, direction): dedup gate per day
  - place_market(strategy_cfg, entry_price, atr_at_setup, or_width): MARKET
    order with TP/SL precomputed by mode (ATR or OR_FIXED → single-shot).
  - place_partial(strategy_cfg, entry_price, atr_at_setup, or_width): MARKET
    order for DOC/SWING modes; registers position in the state machine for
    subsequent partial-exit management.
  - partial_exit_tick(...): per-poll iteration over live partial positions;
    queries ticks + last M1, evaluates state machine, executes partial
    closes / SL modifications.
  - sweep_max_hold(): force-close positions older than max_hold_min (also
    handled by partial_exit_tick for DOC/SWING but ATR/OR_FIXED rely on this).
  - DRY_RUN preserves all logic but skips order_send/position_close.

V2 supports ATR, OR_FIXED, DOC, SWING.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

try:
    import MetaTrader5 as mt5  # type: ignore
except Exception:  # pragma: no cover
    mt5 = None  # type: ignore

from src.execution.amo_position_state import (
    Action,
    AmoPosition,
    Decision,
    PositionStateStore,
    apply_decision,
    evaluate,
)


MAGIC_NUMBER_AMO8 = 8338
DEFAULT_STATE_DIR = r"C:\ProgramData\Kha0sysAmo8\state"

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

    def __init__(self, dry_run: bool = True, telegram=None,
                 state_dir: Optional[str] = None):
        self.dry_run = dry_run
        self.telegram = telegram
        # In-memory dedup: {(internal_sym, pattern_id, direction, trade_date): True}
        self._fired_today: dict[tuple, str] = {}
        # In-memory pending tracking for DRY mode and max-hold sweep
        self._pending: list[PendingAmoOrder] = []
        # Partial-exit state (DOC + SWING modes)
        state_dir = state_dir or DEFAULT_STATE_DIR
        try:
            self.state_store = PositionStateStore(state_dir)
            self.state_positions: dict[int, AmoPosition] = self.state_store.load()
            if self.state_positions:
                print(f"[AMO8] loaded {len(self.state_positions)} partial-exit "
                      f"positions from {state_dir}")
        except Exception as e:
            print(f"[AMO8] state store init error ({state_dir}): {e}; "
                  f"falling back to in-memory only")
            self.state_store = None
            self.state_positions = {}

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
                self.telegram._send(
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
        bid = float(tick.bid)
        ask = float(tick.ask)
        spread = max(ask - bid, 0.0)

        # Stops_level guard — same logic as TRADERS_ORB. Avoid INVALID_STOPS
        # (10016) when SL/TP distance from entry is below broker's minimum.
        # Use max of (2x stops_level*point, 3x spread, 0.1% of price).
        sym_info = mt5.symbol_info(broker_sym)
        if sym_info is not None:
            point = float(getattr(sym_info, "point", 0) or 0)
            stops_lvl_pts = float(getattr(sym_info, "trade_stops_level", 0) or 0)
            min_stop_dist = max(
                2.0 * stops_lvl_pts * point,
                3.0 * spread,
                0.001 * float(price),
            )
            if min_stop_dist > 0:
                orig_sl, orig_tp = sl_price, tp_price
                if direction == "LONG":
                    if (price - sl_price) < min_stop_dist:
                        sl_price = price - min_stop_dist
                    if (tp_price - price) < min_stop_dist:
                        tp_price = price + min_stop_dist
                else:  # SHORT
                    if (sl_price - price) < min_stop_dist:
                        sl_price = price + min_stop_dist
                    if (price - tp_price) < min_stop_dist:
                        tp_price = price - min_stop_dist
                if sl_price != orig_sl or tp_price != orig_tp:
                    print(f"[AMO8] {broker_sym} min_dist={min_stop_dist:.5f} "
                          f"(stops_lvl*pt={stops_lvl_pts*point:.5f} "
                          f"spread={spread:.5f} 0.1%price={0.001*price:.5f}) "
                          f"-> sl={sl_price:.5f} tp={tp_price:.5f}", flush=True)

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
            print(f"[AMO8] order_send returned None for {broker_sym}", flush=True)
            return -1, False
        rc = int(getattr(result, "retcode", 0))
        if rc not in (_RETCODE_DONE, _RETCODE_DONE_PARTIAL):
            print(f"[AMO8] order_send retcode={rc} for {broker_sym} "
                  f"({getattr(result, 'comment', '')})", flush=True)
            return -1, False
        return int(getattr(result, "order", -1)), True

    # ───────────────────────── Partial-exit placement ─────────────────────────

    def place_partial(
        self,
        strategy: dict,
        entry_price: float,
        atr_at_setup: float,
        or_width: float,
        risk_per_trade: float,
        account_balance: float,
    ) -> Optional[AmoPosition]:
        """Place a MARKET order for DOC or SWING mode and register state.

        Computes initial SL/TP distances from the exit_rules and stores an
        AmoPosition in the state machine for subsequent partial management.
        Returns the registered AmoPosition (with ticket=-1 in DRY) or None.
        """
        internal_sym = strategy["internal_sym"]
        broker_sym = strategy["broker_sym"]
        direction = strategy["direction"]
        rules = strategy["exit_rules"]
        mode = rules["mode"]

        if mode not in ("DOC", "SWING"):
            raise ValueError(f"place_partial requires DOC or SWING, got {mode}")

        sign = 1.0 if direction == "LONG" else -1.0
        risk_per_r = 0.5 * atr_at_setup

        if mode == "DOC":
            sl_dist = float(rules["sl_or_frac"]) * or_width
            tp1_dist = float(rules["tp1_or_frac"]) * or_width
            tp2_dist = float(rules["tp2_or_frac"]) * or_width
            tp1_frac = float(rules.get("tp1_fraction", 0.5))
            tp2_frac = 1.0 - tp1_frac
            mid_mfe_r = float(rules.get("midpoint_mfe_min_r", 0.5))
            sma_period = 0
            swing_tp2_lock_r = 0.0
        else:  # SWING
            sl_dist = float(rules["sl_atr_mult"]) * atr_at_setup
            tp1_dist = float(rules["tp1_r"]) * risk_per_r
            tp2_dist = float(rules["tp2_r"]) * risk_per_r
            tp1_frac = float(rules.get("tp1_fraction", 0.25))
            tp2_frac = float(rules.get("tp2_fraction", 0.25))
            mid_mfe_r = 0.5  # unused
            sma_period = int(rules.get("trail_sma_period", 20))
            swing_tp2_lock_r = 1.0

        if sl_dist <= 0 or tp1_dist <= 0 or tp2_dist <= tp1_dist:
            print(f"[AMO8] skip {strategy['id']}: invalid distances "
                  f"sl={sl_dist:.6f} tp1={tp1_dist:.6f} tp2={tp2_dist:.6f}")
            return None

        # Initial broker-level SL: at sl_dist; TP1: at tp1_dist (broker handles
        # SL natively; TP is managed by our state machine, so we DO NOT set a
        # broker TP — leave it at 0 / no TP).
        sl_price = entry_price - sign * sl_dist

        volume = self._compute_volume(
            broker_sym, sl_dist, risk_per_trade, account_balance
        )
        if volume <= 0:
            print(f"[AMO8] skip {strategy['id']}: computed volume <= 0")
            return None

        comment = make_order_comment(strategy["id"], mode, strategy["event_type"])

        if self.dry_run:
            print(f"[AMO8][DRY] would place {mode} MARKET {direction} {broker_sym} "
                  f"vol={volume} entry≈{entry_price:.5f} sl={sl_price:.5f} "
                  f"tp1≈{entry_price + sign*tp1_dist:.5f} "
                  f"tp2≈{entry_price + sign*tp2_dist:.5f}  comment='{comment}'")
            ticket = -1 * (len(self.state_positions) + 1)  # unique negative for DRY
            ok = True
        else:
            ticket, ok = self._send_market_order(
                broker_sym, direction, volume, sl_price,
                tp_price=0.0,   # no broker TP — managed by state machine
                comment=comment,
            )
            if not ok:
                print(f"[AMO8] order_send failed for {strategy['id']}")
                return None

        pos = AmoPosition(
            ticket=ticket,
            strategy_id=strategy["id"],
            mode=mode,
            direction=direction,
            broker_sym=broker_sym,
            internal_sym=internal_sym,
            entry_price=float(entry_price),
            initial_volume=float(volume),
            placed_at_iso=datetime.now(timezone.utc).isoformat(),
            max_hold_min=int(rules.get("max_hold_min", 600)),
            atr_at_setup=float(atr_at_setup),
            or_width=float(or_width),
            sl_distance_initial=float(sl_dist),
            tp1_distance=float(tp1_dist),
            tp2_distance=float(tp2_dist),
            tp1_fraction=float(tp1_frac),
            tp2_fraction=float(tp2_frac),
            midpoint_mfe_min_r=float(mid_mfe_r),
            sma_period=int(sma_period),
            swing_tp2_lock_r=float(swing_tp2_lock_r),
        )
        pos.init_levels()
        self.state_positions[ticket] = pos
        if self.state_store is not None:
            try:
                self.state_store.save(self.state_positions)
            except Exception as e:
                print(f"[AMO8] state save error: {e}")

        self._mark_fired(internal_sym, strategy["pattern_id"], direction)

        if self.telegram is not None:
            try:
                self.telegram._send(
                    f"[AMO8] ORDER PLACED [{mode}]\n"
                    f"strategy: {strategy['id']}\n"
                    f"symbol: {broker_sym} ({internal_sym})\n"
                    f"dir: {direction}\n"
                    f"entry: {entry_price:.5f}  sl: {sl_price:.5f}\n"
                    f"tp1: {pos.tp1_price:.5f} ({tp1_frac*100:.0f}%)\n"
                    f"tp2: {pos.tp2_price:.5f} ({tp2_frac*100:.0f}%)\n"
                    f"vol: {volume}  comment: {comment}\n"
                    f"expected: PF={strategy.get('expected_pf', '?')} "
                    f"WR={strategy.get('expected_wr', '?')}"
                )
            except Exception as e:
                print(f"[AMO8] telegram error: {e}")

        return pos

    # ───────────────────────── Partial-exit tick ─────────────────────────

    def partial_exit_tick(self, bars_by_symbol: dict[str, dict]) -> None:
        """Per-poll: iterate state-machine positions and execute transitions.

        `bars_by_symbol` is {broker_sym: {"bid": .., "ask": .., "m1_high": ..,
        "m1_low": .., "m1_close": ..}} — caller provides latest data.

        Positions with mode != DOC/SWING are ignored (broker manages them).
        Positions whose remaining_volume == 0 are removed from state.
        """
        if not self.state_positions:
            return
        now = datetime.now(timezone.utc)
        to_remove: list[int] = []
        for ticket, pos in list(self.state_positions.items()):
            if pos.remaining_volume <= 0:
                to_remove.append(ticket)
                continue
            data = bars_by_symbol.get(pos.broker_sym)
            if data is None:
                continue
            decision = evaluate(
                pos,
                now=now,
                bid=float(data["bid"]),
                ask=float(data["ask"]),
                last_m1_high=float(data["m1_high"]),
                last_m1_low=float(data["m1_low"]),
                last_m1_close=float(data["m1_close"]),
            )
            if decision.action == Action.HOLD:
                continue
            ok = self._execute_decision(pos, decision)
            if ok:
                apply_decision(pos, decision)
                if pos.remaining_volume <= 0:
                    to_remove.append(ticket)
                self._emit_decision_telegram(pos, decision)

        for t in to_remove:
            self.state_positions.pop(t, None)

        if self.state_store is not None and (to_remove or self.state_positions):
            try:
                self.state_store.save(self.state_positions)
            except Exception as e:
                print(f"[AMO8] state save error: {e}")

    def _execute_decision(self, pos: AmoPosition, decision: Decision) -> bool:
        """Translate state-machine decision into MT5 orders.

        - PARTIAL_CLOSE(fraction, new_sl_price): close fraction × initial_volume
          then modify SL on the remaining position.
        - CLOSE_ALL: close pos.remaining_volume at market.
        - MODIFY_SL: only update SL.

        Returns True if the broker action succeeded (or DRY).
        """
        if self.dry_run or mt5 is None:
            return True

        if decision.action == Action.CLOSE_ALL:
            return self._close_position_market(pos.ticket, pos.broker_sym,
                                                pos.direction, pos.remaining_volume,
                                                comment=f"A8|{decision.reason[:23]}")
        if decision.action == Action.PARTIAL_CLOSE:
            close_vol = decision.fraction * pos.initial_volume
            close_vol = self._snap_to_step(pos.broker_sym, close_vol)
            if close_vol <= 0 or close_vol > pos.remaining_volume:
                return False
            ok_close = self._close_position_market(
                pos.ticket, pos.broker_sym, pos.direction, close_vol,
                comment=f"A8|{decision.reason[:23]}",
            )
            if not ok_close:
                return False
            if decision.new_sl_price is not None:
                self._modify_position_sl(pos.ticket, pos.broker_sym,
                                          decision.new_sl_price)
            return True
        if decision.action == Action.MODIFY_SL and decision.new_sl_price is not None:
            return self._modify_position_sl(pos.ticket, pos.broker_sym,
                                             decision.new_sl_price)
        return False

    def _snap_to_step(self, broker_sym: str, volume: float) -> float:
        if mt5 is None:
            return volume
        info = mt5.symbol_info(broker_sym)
        if info is None:
            return volume
        vol_step = float(info.volume_step or 0.01)
        vol_min = float(info.volume_min or 0.01)
        snapped = math.floor(volume / vol_step) * vol_step
        return max(0.0, max(vol_min if snapped > 0 else 0.0, round(snapped, 2)))

    def _close_position_market(
        self, ticket: int, broker_sym: str, direction: str,
        volume: float, comment: str,
    ) -> bool:
        if mt5 is None:
            return False
        tick = mt5.symbol_info_tick(broker_sym)
        if tick is None:
            return False
        is_long = direction == "LONG"
        close_type = mt5.ORDER_TYPE_SELL if is_long else mt5.ORDER_TYPE_BUY
        price = tick.bid if is_long else tick.ask
        req = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": broker_sym,
            "volume": float(volume),
            "type": close_type,
            "position": int(ticket),
            "price": float(price),
            "deviation": 20,
            "magic": MAGIC_NUMBER_AMO8,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(req)
        if result is None:
            return False
        return int(getattr(result, "retcode", 0)) in (_RETCODE_DONE, _RETCODE_DONE_PARTIAL)

    def _modify_position_sl(self, ticket: int, broker_sym: str,
                            new_sl: float) -> bool:
        if mt5 is None:
            return False
        # SLTP modification doesn't change TP — read current TP and preserve
        positions = mt5.positions_get(symbol=broker_sym) or []
        current_tp = 0.0
        for p in positions:
            if int(getattr(p, "ticket", -1)) == ticket:
                current_tp = float(getattr(p, "tp", 0.0))
                break
        req = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": int(ticket),
            "symbol": broker_sym,
            "sl": float(new_sl),
            "tp": float(current_tp),
            "magic": MAGIC_NUMBER_AMO8,
        }
        result = mt5.order_send(req)
        if result is None:
            return False
        return int(getattr(result, "retcode", 0)) in (_RETCODE_DONE, _RETCODE_DONE_PARTIAL)

    def _emit_decision_telegram(self, pos: AmoPosition, decision: Decision) -> None:
        if self.telegram is None:
            return
        try:
            if decision.action == Action.PARTIAL_CLOSE:
                self.telegram._send(
                    f"[AMO8] PARTIAL CLOSE [{decision.reason}]\n"
                    f"strategy: {pos.strategy_id}\n"
                    f"ticket: {pos.ticket}  symbol: {pos.broker_sym}\n"
                    f"closed: {decision.fraction*100:.0f}% × initial_volume\n"
                    f"remaining: {pos.remaining_volume - decision.fraction*pos.initial_volume:.2f}\n"
                    f"new SL: {decision.new_sl_price}"
                )
            elif decision.action == Action.CLOSE_ALL:
                self.telegram._send(
                    f"[AMO8] FULL CLOSE [{decision.reason}]\n"
                    f"strategy: {pos.strategy_id}\n"
                    f"ticket: {pos.ticket}  symbol: {pos.broker_sym}\n"
                    f"closed remaining: {pos.remaining_volume:.2f}"
                )
            elif decision.action == Action.MODIFY_SL:
                self.telegram._send(
                    f"[AMO8] SL MOVED [{decision.reason}]\n"
                    f"strategy: {pos.strategy_id}  ticket: {pos.ticket}\n"
                    f"new SL: {decision.new_sl_price}"
                )
        except Exception as e:
            print(f"[AMO8] telegram error: {e}")

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
                        self.telegram._send(
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
