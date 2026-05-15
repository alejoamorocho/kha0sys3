"""Four management modes for ORB pattern testing.

Mode 1 (ATR): SL = sl_atr × ATR, TP = rr × SL
Mode 2 (OR-FIXED): SL = sl_or × OR_width, TP = rr × SL
Mode 3 (DOC): Partial exits + breakeven shift + time-conditional exit
  - SL = 1.0 × OR_width
  - TP1 = 1.0 × OR_width → close 50%, SL → entry (BE)
  - TP2 = 2.0 × OR_width → close remaining 50%
  - Mid-time check (max_hold/2): if MFE < 0.5R, close at market
  - Hard stop: max_hold_min
Mode 4 (SWING): Traders Swing portfolio style adapted to intraday
  - SL = 1.0 × ATR (Qulla HTF style)
  - Partial 25% at 2R, partial 25% at 4R, BE after first partial
  - Trail remaining 50% with SMA(20) on M1 below price (long) or above (short)
  - Hard time-stop: max_hold_min

All modes return realized_r per trigger. Same M1 walking discipline as Phase B.
"""
from __future__ import annotations

from datetime import timedelta


def _trade_atr_or_fixed(
    fill_ts, entry: float, direction: str,
    sl: float, tp: float, max_hold_min: int,
    m1: dict, risk_per_r: float, friction_r: float,
) -> dict:
    """Single-target TP/SL/MAX_HOLD walker. Used by modes 1 and 2."""
    from src.application.orb_management_walker import simulate_trade
    return simulate_trade(
        fill_ts=fill_ts, entry=entry, direction=direction,
        tp=tp, sl=sl, max_hold_min=max_hold_min, m1=m1,
        risk_per_r=risk_per_r, friction_r=friction_r,
    )


def simulate_doc_partial(
    fill_ts,
    entry: float,
    direction: str,
    sl_distance: float,        # absolute price distance from entry
    tp1_distance: float,       # absolute price distance favorable
    tp2_distance: float,       # absolute price distance favorable (> tp1)
    max_hold_min: int,
    m1: dict,
    risk_per_r: float,
    friction_r: float,
    tp1_fraction: float = 0.5,
    midpoint_mfe_min_r: float = 0.5,
) -> dict:
    """Partial-exits walker: TP1 (50%) + TP2 (50%) + BE shift + time-conditional close.

    Returns dict: realized_r (total, friction-deducted), exit_reason (last hit),
    exits (list of partials), tp1_hit, tp2_hit, time_stopped.
    SL-first conservative on intra-bar ties (matches K3M1 convention).
    """
    if risk_per_r <= 0:
        raise ValueError("risk_per_r must be positive")

    times = m1["times"]
    highs = m1["highs"]
    lows = m1["lows"]
    closes = m1["closes"]
    n = len(times)
    sign = 1.0 if direction == "LONG" else -1.0

    # Initial levels
    sl_price = entry - sign * sl_distance
    tp1_price = entry + sign * tp1_distance
    tp2_price = entry + sign * tp2_distance
    current_sl = sl_price

    # Position fraction tracking
    remaining = 1.0
    tp1_hit = False
    tp2_hit = False
    exits: list[dict] = []
    mfe_price = 0.0  # tracks favorable MFE in PRICE units from entry

    # Skip bars at/before fill
    start = 0
    while start < n and times[start] <= fill_ts:
        start += 1
    if start >= n:
        return {
            "realized_r": -friction_r if remaining > 0 else 0.0,
            "exit_reason": "NO_BARS",
            "exits": [],
            "tp1_hit": False,
            "tp2_hit": False,
            "time_stopped": False,
        }

    horizon_end = fill_ts + timedelta(minutes=max_hold_min)
    midpoint = fill_ts + timedelta(minutes=max_hold_min // 2)
    midpoint_checked = False
    last_idx = start - 1
    time_stopped = False

    for j in range(start, n):
        if times[j] > horizon_end:
            break
        last_idx = j
        hi = highs[j]
        lo = lows[j]

        # Update MFE in price units (favorable direction)
        if direction == "LONG":
            mfe_price = max(mfe_price, hi - entry)
        else:
            mfe_price = max(mfe_price, entry - lo)

        # Mid-time conditional check: if not enough MFE, close remainder
        if not midpoint_checked and times[j] >= midpoint:
            midpoint_checked = True
            if not tp1_hit:
                min_mfe_needed = midpoint_mfe_min_r * risk_per_r
                if mfe_price < min_mfe_needed:
                    exit_price = closes[j]
                    pnl_price = sign * (exit_price - entry)
                    r = (pnl_price / risk_per_r) * remaining
                    exits.append({
                        "exit_reason": "TIME_STOP_LOW_MFE",
                        "exit_ts": times[j],
                        "fraction": remaining,
                        "realized_r": r,
                    })
                    remaining = 0.0
                    time_stopped = True
                    break

        # SL / TP detection (SL-first on tie)
        sl_hit_now = (direction == "LONG" and lo <= current_sl) \
                     or (direction == "SHORT" and hi >= current_sl)
        tp1_hit_now = (not tp1_hit) and (
            (direction == "LONG" and hi >= tp1_price)
            or (direction == "SHORT" and lo <= tp1_price)
        )
        tp2_hit_now = tp1_hit and (
            (direction == "LONG" and hi >= tp2_price)
            or (direction == "SHORT" and lo <= tp2_price)
        )

        if sl_hit_now:
            # SL closes remaining position at SL price
            pnl_price = sign * (current_sl - entry)
            r = (pnl_price / risk_per_r) * remaining
            exits.append({
                "exit_reason": "SL_BE" if (tp1_hit and current_sl == entry) else "SL",
                "exit_ts": times[j],
                "fraction": remaining,
                "realized_r": r,
            })
            remaining = 0.0
            break

        if tp1_hit_now:
            # Close tp1_fraction at TP1, shift SL to entry (BE)
            pnl_price = sign * (tp1_price - entry)
            r = (pnl_price / risk_per_r) * tp1_fraction
            exits.append({
                "exit_reason": "TP1",
                "exit_ts": times[j],
                "fraction": tp1_fraction,
                "realized_r": r,
            })
            tp1_hit = True
            current_sl = entry  # BE shift
            remaining -= tp1_fraction

        if tp2_hit_now and remaining > 0:
            pnl_price = sign * (tp2_price - entry)
            r = (pnl_price / risk_per_r) * remaining
            exits.append({
                "exit_reason": "TP2",
                "exit_ts": times[j],
                "fraction": remaining,
                "realized_r": r,
            })
            tp2_hit = True
            remaining = 0.0
            break

    # If still holding remainder at horizon_end, close at last bar's close
    if remaining > 0 and last_idx >= start:
        exit_price = float(closes[last_idx])
        pnl_price = sign * (exit_price - entry)
        r = (pnl_price / risk_per_r) * remaining
        exits.append({
            "exit_reason": "MAX_HOLD",
            "exit_ts": times[last_idx],
            "fraction": remaining,
            "realized_r": r,
        })
        remaining = 0.0

    total_r = sum(e["realized_r"] for e in exits) - float(friction_r)
    last_reason = exits[-1]["exit_reason"] if exits else "NO_BARS"
    return {
        "realized_r": total_r,
        "exit_reason": last_reason,
        "exits": exits,
        "tp1_hit": tp1_hit,
        "tp2_hit": tp2_hit,
        "time_stopped": time_stopped,
    }


def simulate_swing_traders(
    fill_ts,
    entry: float,
    direction: str,
    sl_distance: float,        # 1.0 × ATR
    max_hold_min: int,
    m1: dict,
    risk_per_r: float,
    friction_r: float,
    tp1_r: float = 2.0,
    tp2_r: float = 4.0,
    tp1_fraction: float = 0.25,
    tp2_fraction: float = 0.25,
    trail_sma_period: int = 20,
) -> dict:
    """Traders Swing-style management adapted to intraday horizon.

    Rules:
      - SL = 1.0 × ATR (passed as sl_distance in price)
      - TP1 at +2R → close 25%, shift SL to entry (BE)
      - TP2 at +4R → close another 25%, shift SL to entry+1R (locked profit)
      - Remaining 50% trails SMA(20) on M1: exit when M1 close crosses SMA against trade
      - Hard time-stop at max_hold_min: close any remainder at last close
      - SL-first conservative on intra-bar ties

    Returns dict with realized_r (total, friction-deducted), exit_reason, exits,
    tp1_hit, tp2_hit, trail_hit, time_stopped.
    """
    import numpy as np

    if risk_per_r <= 0:
        raise ValueError("risk_per_r must be positive")

    times = m1["times"]
    highs = m1["highs"]
    lows = m1["lows"]
    closes = m1["closes"]
    n = len(times)
    sign = 1.0 if direction == "LONG" else -1.0

    # Levels (in price)
    sl_price = entry - sign * sl_distance
    tp1_price = entry + sign * (tp1_r * risk_per_r)
    tp2_price = entry + sign * (tp2_r * risk_per_r)
    current_sl = sl_price

    remaining = 1.0
    tp1_hit = False
    tp2_hit = False
    trail_hit = False
    time_stopped = False
    exits: list[dict] = []

    # Skip bars at/before fill
    start = 0
    while start < n and times[start] <= fill_ts:
        start += 1
    if start >= n:
        return {
            "realized_r": -friction_r,
            "exit_reason": "NO_BARS",
            "exits": [], "tp1_hit": False, "tp2_hit": False,
            "trail_hit": False, "time_stopped": False,
        }

    horizon_end = fill_ts + timedelta(minutes=max_hold_min)
    last_idx = start - 1

    # Rolling SMA buffer
    sma_window: list[float] = []

    for j in range(start, n):
        if times[j] > horizon_end:
            break
        last_idx = j
        hi = highs[j]
        lo = lows[j]
        cl = closes[j]

        # Update SMA buffer
        sma_window.append(cl)
        if len(sma_window) > trail_sma_period:
            sma_window.pop(0)
        sma = sum(sma_window) / len(sma_window) if sma_window else None

        # SL-first
        sl_hit_now = (direction == "LONG" and lo <= current_sl) \
                     or (direction == "SHORT" and hi >= current_sl)
        if sl_hit_now:
            pnl_price = sign * (current_sl - entry)
            r = (pnl_price / risk_per_r) * remaining
            reason = "SL"
            if tp1_hit and current_sl == entry:
                reason = "SL_BE"
            elif tp2_hit:
                reason = "SL_LOCKED"
            exits.append({
                "exit_reason": reason,
                "exit_ts": times[j], "fraction": remaining, "realized_r": r,
            })
            remaining = 0.0
            break

        # TP1
        tp1_hit_now = (not tp1_hit) and (
            (direction == "LONG" and hi >= tp1_price)
            or (direction == "SHORT" and lo <= tp1_price)
        )
        if tp1_hit_now:
            pnl_price = sign * (tp1_price - entry)
            r = (pnl_price / risk_per_r) * tp1_fraction
            exits.append({
                "exit_reason": "TP1",
                "exit_ts": times[j], "fraction": tp1_fraction, "realized_r": r,
            })
            tp1_hit = True
            current_sl = entry  # BE
            remaining -= tp1_fraction

        # TP2
        tp2_hit_now = tp1_hit and (not tp2_hit) and (
            (direction == "LONG" and hi >= tp2_price)
            or (direction == "SHORT" and lo <= tp2_price)
        )
        if tp2_hit_now:
            pnl_price = sign * (tp2_price - entry)
            r = (pnl_price / risk_per_r) * tp2_fraction
            exits.append({
                "exit_reason": "TP2",
                "exit_ts": times[j], "fraction": tp2_fraction, "realized_r": r,
            })
            tp2_hit = True
            # Move SL to entry + 1R (locked profit)
            current_sl = entry + sign * (1.0 * risk_per_r)
            remaining -= tp2_fraction

        # Trail after TP2: exit when close crosses SMA against trade direction
        if tp2_hit and sma is not None and remaining > 0:
            sma_cross = (direction == "LONG" and cl < sma) \
                        or (direction == "SHORT" and cl > sma)
            if sma_cross:
                pnl_price = sign * (cl - entry)
                r = (pnl_price / risk_per_r) * remaining
                exits.append({
                    "exit_reason": "TRAIL_SMA",
                    "exit_ts": times[j], "fraction": remaining, "realized_r": r,
                })
                remaining = 0.0
                trail_hit = True
                break

    # MAX_HOLD: close remainder at last close inside horizon
    if remaining > 0 and last_idx >= start:
        exit_price = float(closes[last_idx])
        pnl_price = sign * (exit_price - entry)
        r = (pnl_price / risk_per_r) * remaining
        exits.append({
            "exit_reason": "MAX_HOLD",
            "exit_ts": times[last_idx], "fraction": remaining, "realized_r": r,
        })
        remaining = 0.0
        time_stopped = True

    total_r = sum(e["realized_r"] for e in exits) - float(friction_r)
    last_reason = exits[-1]["exit_reason"] if exits else "NO_BARS"
    return {
        "realized_r": total_r,
        "exit_reason": last_reason,
        "exits": exits,
        "tp1_hit": tp1_hit,
        "tp2_hit": tp2_hit,
        "trail_hit": trail_hit,
        "time_stopped": time_stopped,
    }
