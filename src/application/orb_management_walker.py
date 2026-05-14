"""M1 management walker for Phase B and Phase D.

Given a fill price + TP/SL/MAX_HOLD, walk minute-by-minute and return
realized R-multiple + exit reason. SL-first conservative on intra-bar ties.
Friction (in R) deducted from realized R.
"""
from __future__ import annotations

from datetime import timedelta


def simulate_trade(
    fill_ts,
    entry: float,
    direction: str,
    tp: float,
    sl: float,
    max_hold_min: int,
    m1: dict,
    risk_per_r: float,
    friction_r: float,
) -> dict:
    """Simulate a trade and return {exit_reason, exit_ts, exit_price, realized_r}.

    risk_per_r is the price-unit distance equivalent to 1R (typically
    0.5*ATR_at_setup). It MUST be > 0.
    """
    if risk_per_r <= 0:
        raise ValueError("risk_per_r must be positive")

    times = m1["times"]
    highs = m1["highs"]
    lows = m1["lows"]
    closes = m1["closes"]
    n = len(times)

    start = 0
    while start < n and times[start] <= fill_ts:
        start += 1
    if start >= n:
        return {"exit_reason": "NO_BARS", "exit_ts": None, "exit_price": entry, "realized_r": 0.0}

    horizon_end = fill_ts + timedelta(minutes=max_hold_min)

    sign = 1.0 if direction == "LONG" else -1.0
    last_idx = start - 1
    for j in range(start, n):
        if times[j] > horizon_end:
            break
        last_idx = j
        hi = highs[j]
        lo = lows[j]
        tp_hit = (direction == "LONG" and hi >= tp) or (direction == "SHORT" and lo <= tp)
        sl_hit = (direction == "LONG" and lo <= sl) or (direction == "SHORT" and hi >= sl)
        if tp_hit and sl_hit:
            return _exit("SL", times[j], sl, entry, sign, risk_per_r, friction_r)
        if sl_hit:
            return _exit("SL", times[j], sl, entry, sign, risk_per_r, friction_r)
        if tp_hit:
            return _exit("TP", times[j], tp, entry, sign, risk_per_r, friction_r)

    if last_idx < start:
        return {"exit_reason": "NO_BARS", "exit_ts": None, "exit_price": entry, "realized_r": 0.0}
    exit_price = float(closes[last_idx])
    return _exit("MAX_HOLD", times[last_idx], exit_price, entry, sign, risk_per_r, friction_r)


def _exit(reason, ts, exit_price, entry, sign, risk_per_r, friction_r):
    pnl_price = sign * (float(exit_price) - float(entry))
    realized_r = pnl_price / risk_per_r - float(friction_r)
    return {
        "exit_reason": reason,
        "exit_ts": ts,
        "exit_price": float(exit_price),
        "realized_r": float(realized_r),
    }
