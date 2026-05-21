"""ORB pattern definitions: state classifiers + event detectors.

State (categorical context at OR close):
  - or_position_vs_pd: 5 values from DataEnricher (ABOVE_PD_HIGH, etc.)
  - or_atr_bucket: 3 values (compressed <= 0.3, normal, expanded >= 0.7)
  - pd_or_overlap_bucket: 3 values (gap_up, gap_down, inside)

Events (dynamic post-OR triggers, detected on M1):
  - BREAK_UP / BREAK_DOWN
  - FALSE_BREAK_UP / FALSE_BREAK_DOWN
  - MITIG_PD_MID / MITIG_PD_CLOSE
  - REENTRY_PD_OR_HIGH / REENTRY_PD_OR_LOW

Pattern ID format: f"{EVENT}_{or_position}_{or_atr_bucket}_{pd_or_bucket}"
"""
from __future__ import annotations

import polars as pl

OR_ATR_BUCKETS = ["compressed", "normal", "expanded"]
PD_OR_BUCKETS = ["gap_up", "gap_down", "inside"]

EVENTS = [
    "BREAK_UP", "BREAK_DOWN",
    "FALSE_BREAK_UP", "FALSE_BREAK_DOWN",
    "MITIG_PD_MID", "MITIG_PD_CLOSE",
    "REENTRY_PD_OR_HIGH", "REENTRY_PD_OR_LOW",
]


BUCKET_ROLLING_WINDOW_DAYS = 90
BUCKET_MIN_SAMPLES = 20
BUCKET_FALLBACK_Q30 = 0.3
BUCKET_FALLBACK_Q70 = 0.7


def add_state_columns(
    df: pl.DataFrame,
    bucket_window: int = BUCKET_ROLLING_WINDOW_DAYS,
    bucket_min_samples: int = BUCKET_MIN_SAMPLES,
) -> pl.DataFrame:
    """Add `or_atr_bucket` and `pd_or_overlap_bucket` columns.

    `or_atr_bucket` is computed against a CAUSAL rolling-percentile threshold
    per symbol (bottom 30% = compressed, top 30% = expanded). This avoids the
    bias of fixed absolute thresholds when the symbol's ATR baseline shifts
    between regimes (e.g., between historical backtest data and current
    Vantage live data, where atr_14 magnitudes can differ ~10x for the same
    symbol despite similar OR widths).

    Falls back to fixed 0.3 / 0.7 thresholds during warm-up (when the rolling
    window has fewer than `bucket_min_samples` daily observations).

    Assumes `df` already has `or_atr_ratio`, `or_high`, `or_low`,
    `pd_or_high`, `pd_or_low`, `trade_date` from
    `DataEnricher.enrich_with_opening_range`.
    """
    # Reduce to one row per trade_date (or_atr_ratio is constant within a day)
    daily = (
        df.filter(pl.col("or_atr_ratio").is_not_null())
          .group_by("trade_date")
          .agg(pl.col("or_atr_ratio").first().alias("_daily_ratio"))
          .sort("trade_date")
    )
    # Causal rolling thresholds — shift(1) ensures we never use today's value
    daily = daily.with_columns([
        pl.col("_daily_ratio")
          .rolling_quantile(0.30, window_size=bucket_window, min_samples=bucket_min_samples)
          .shift(1)
          .alias("_q30"),
        pl.col("_daily_ratio")
          .rolling_quantile(0.70, window_size=bucket_window, min_samples=bucket_min_samples)
          .shift(1)
          .alias("_q70"),
    ])
    df = df.join(daily.select(["trade_date", "_q30", "_q70"]), on="trade_date", how="left")

    out = df.with_columns([
        # Use rolling threshold when available, fall back to fixed 0.3/0.7
        pl.when(pl.col("or_atr_ratio").is_null())
          .then(pl.lit(None, dtype=pl.Utf8))
          .when(pl.col("or_atr_ratio") <= pl.coalesce(pl.col("_q30"), pl.lit(BUCKET_FALLBACK_Q30)))
          .then(pl.lit("compressed"))
          .when(pl.col("or_atr_ratio") >= pl.coalesce(pl.col("_q70"), pl.lit(BUCKET_FALLBACK_Q70)))
          .then(pl.lit("expanded"))
          .otherwise(pl.lit("normal"))
          .alias("or_atr_bucket"),

        pl.when(pl.col("pd_or_high").is_null() | pl.col("pd_or_low").is_null())
          .then(pl.lit(None, dtype=pl.Utf8))
          .when(pl.col("or_low") > pl.col("pd_or_high"))
          .then(pl.lit("gap_up"))
          .when(pl.col("or_high") < pl.col("pd_or_low"))
          .then(pl.lit("gap_down"))
          .otherwise(pl.lit("inside"))
          .alias("pd_or_overlap_bucket"),
    ]).drop(["_q30", "_q70"])
    return out


import numpy as np


_BREAK_LOOKAHEAD_BARS = 30  # false-break window
_FALSE_BREAK_EXTENSION = 0.5  # multiple of or_width


def detect_events_for_day(
    or_close_ts,
    or_high: float,
    or_low: float,
    pd_mid: float | None,
    pd_close: float | None,
    pd_or_high: float | None,
    pd_or_low: float | None,
    atr_at_setup: float,
    m1: dict,
) -> list[dict]:
    """Scan M1 bars strictly after `or_close_ts` for the 8 ORB events.

    Returns list of dicts: {event_type, trigger_ts, trigger_close, atr_at_setup}.
    Each event fires at most once per day (first occurrence).

    Look-ahead guarantee: all detection uses M1 bars where time > or_close_ts.
    The `or_close_ts` bar itself is excluded (strict inequality).
    """
    times = m1["times"]
    highs = m1["highs"]
    lows = m1["lows"]
    closes = m1["closes"]
    n = len(times)
    if n == 0:
        return []

    start = 0
    while start < n and times[start] <= or_close_ts:
        start += 1
    if start >= n:
        return []

    or_width = or_high - or_low
    fb_up_threshold = or_high + _FALSE_BREAK_EXTENSION * or_width
    fb_dn_threshold = or_low - _FALSE_BREAK_EXTENSION * or_width

    events: list[dict] = []
    seen = set()

    def _emit(event_type, idx):
        if event_type in seen:
            return
        seen.add(event_type)
        events.append({
            "event_type": event_type,
            "trigger_ts": times[idx],
            "trigger_close": float(closes[idx]),
            "atr_at_setup": float(atr_at_setup),
        })

    break_up_idx = None
    break_dn_idx = None

    for j in range(start, n):
        hi = highs[j]
        lo = lows[j]

        if break_up_idx is None and hi > or_high:
            break_up_idx = j
            _emit("BREAK_UP", j)
        if break_dn_idx is None and lo < or_low:
            break_dn_idx = j
            _emit("BREAK_DOWN", j)

        if pd_mid is not None and "MITIG_PD_MID" not in seen:
            if lo <= pd_mid <= hi:
                _emit("MITIG_PD_MID", j)
        if pd_close is not None and "MITIG_PD_CLOSE" not in seen:
            if lo <= pd_close <= hi:
                _emit("MITIG_PD_CLOSE", j)
        if pd_or_high is not None and "REENTRY_PD_OR_HIGH" not in seen:
            if lo <= pd_or_high <= hi:
                _emit("REENTRY_PD_OR_HIGH", j)
        if pd_or_low is not None and "REENTRY_PD_OR_LOW" not in seen:
            if lo <= pd_or_low <= hi:
                _emit("REENTRY_PD_OR_LOW", j)

    if break_up_idx is not None:
        end_look = min(n, break_up_idx + 1 + _BREAK_LOOKAHEAD_BARS)
        extended = False
        retraced_idx = None
        for k in range(break_up_idx + 1, end_look):
            if highs[k] >= fb_up_threshold:
                extended = True
                break
            if lows[k] < or_high and retraced_idx is None:
                retraced_idx = k
        if not extended and retraced_idx is not None:
            _emit("FALSE_BREAK_UP", retraced_idx)

    if break_dn_idx is not None:
        end_look = min(n, break_dn_idx + 1 + _BREAK_LOOKAHEAD_BARS)
        extended = False
        retraced_idx = None
        for k in range(break_dn_idx + 1, end_look):
            if lows[k] <= fb_dn_threshold:
                extended = True
                break
            if highs[k] > or_low and retraced_idx is None:
                retraced_idx = k
        if not extended and retraced_idx is not None:
            _emit("FALSE_BREAK_DOWN", retraced_idx)

    return events
