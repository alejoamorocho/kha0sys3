"""MFE/MAE walker for Phase A edge scoring.

Given a trigger timestamp and M1 arrays, walk strictly forward up to a
horizon and report max-favorable / max-adverse excursions for both long and
short interpretations. Pure numpy hotpath.

No look-ahead: bars where time <= trigger_ts are excluded.
"""
from __future__ import annotations

from datetime import timedelta

import numpy as np


def mfe_mae_walk(
    trigger_ts,
    entry: float,
    m1: dict,
    horizon_min: int = 480,
) -> dict:
    """Compute MFE/MAE for long and short over [trigger_ts+1min, trigger_ts+horizon_min].

    Returns dict with keys: mfe_long, mae_long, mfe_short, mae_short, bars_walked.
    All values in price units (caller normalizes to R).
    """
    times = m1["times"]
    highs = m1["highs"]
    lows = m1["lows"]
    n = len(times)
    if n == 0:
        return {"mfe_long": 0.0, "mae_long": 0.0, "mfe_short": 0.0, "mae_short": 0.0, "bars_walked": 0}

    horizon_end = trigger_ts + timedelta(minutes=horizon_min)

    start = 0
    while start < n and times[start] <= trigger_ts:
        start += 1
    end = start
    while end < n and times[end] <= horizon_end:
        end += 1

    if end <= start:
        return {"mfe_long": 0.0, "mae_long": 0.0, "mfe_short": 0.0, "mae_short": 0.0, "bars_walked": 0}

    window_high = highs[start:end].max()
    window_low = lows[start:end].min()

    mfe_long = float(window_high - entry)
    mae_long = float(entry - window_low)
    mfe_short = float(entry - window_low)
    mae_short = float(window_high - entry)

    return {
        "mfe_long": max(mfe_long, 0.0),
        "mae_long": max(mae_long, 0.0),
        "mfe_short": max(mfe_short, 0.0),
        "mae_short": max(mae_short, 0.0),
        "bars_walked": int(end - start),
    }
