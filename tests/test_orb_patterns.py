import polars as pl
import pytest

from src.application.orb_patterns import (
    add_state_columns,
    OR_ATR_BUCKETS,
    PD_OR_BUCKETS,
)


def _toy_frame():
    return pl.DataFrame({
        "trade_date": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"],
        "or_atr_ratio": [0.2, 0.5, 0.9, None],
        "or_high": [1.10, 1.20, 1.30, 1.40],
        "or_low":  [1.05, 1.15, 1.25, 1.35],
        "pd_or_high": [1.04, 1.21, 1.20, None],
        "pd_or_low":  [1.00, 1.18, 1.15, None],
    }).with_columns(pl.col("trade_date").str.to_date())


def test_or_atr_bucket_compressed_normal_expanded():
    df = add_state_columns(_toy_frame())
    buckets = df["or_atr_bucket"].to_list()
    assert buckets[0] == "compressed"
    assert buckets[1] == "normal"
    assert buckets[2] == "expanded"
    assert buckets[3] is None


def test_pd_or_overlap_bucket_gap_up_gap_down_inside():
    df = add_state_columns(_toy_frame())
    buckets = df["pd_or_overlap_bucket"].to_list()
    assert buckets[0] == "gap_up"
    assert buckets[1] == "inside"
    assert buckets[2] == "gap_up"
    assert buckets[3] is None


def test_bucket_constants_exposed():
    assert OR_ATR_BUCKETS == ["compressed", "normal", "expanded"]
    assert PD_OR_BUCKETS == ["gap_up", "gap_down", "inside"]


import numpy as np
from datetime import datetime, timedelta

from src.application.orb_patterns import detect_events_for_day


def _build_m1(start: datetime, count: int, highs, lows, closes):
    times = [start + timedelta(minutes=i) for i in range(count)]
    return {
        "times": np.array(times, dtype="object"),
        "highs": np.asarray(highs, dtype=float),
        "lows": np.asarray(lows, dtype=float),
        "closes": np.asarray(closes, dtype=float),
    }


def test_break_up_detected_after_or_close():
    or_close = datetime(2026, 1, 1, 8, 0)
    or_high, or_low = 1.10, 1.05
    pd_mid, pd_close = 1.08, 1.07
    pd_or_high, pd_or_low = 1.12, 1.06
    atr = 0.01
    m1 = _build_m1(
        start=datetime(2026, 1, 1, 8, 1),
        count=10,
        highs=[1.09, 1.09, 1.11, 1.12, 1.10, 1.09, 1.08, 1.08, 1.07, 1.07],
        lows= [1.08, 1.08, 1.09, 1.10, 1.09, 1.07, 1.07, 1.07, 1.06, 1.06],
        closes=[1.085]*10,
    )
    events = detect_events_for_day(
        or_close_ts=or_close, or_high=or_high, or_low=or_low,
        pd_mid=pd_mid, pd_close=pd_close,
        pd_or_high=pd_or_high, pd_or_low=pd_or_low,
        atr_at_setup=atr, m1=m1,
    )
    breakups = [e for e in events if e["event_type"] == "BREAK_UP"]
    assert len(breakups) == 1
    assert breakups[0]["trigger_ts"] == m1["times"][2]


def test_false_break_up_when_retraces_below_or_high_within_30_bars():
    or_close = datetime(2026, 1, 1, 8, 0)
    or_high, or_low = 1.10, 1.05
    atr = 0.01
    m1 = _build_m1(
        start=datetime(2026, 1, 1, 8, 1),
        count=10,
        highs=[1.09, 1.09, 1.11, 1.11, 1.10, 1.09, 1.09, 1.08, 1.08, 1.07],
        lows= [1.08, 1.08, 1.09, 1.09, 1.08, 1.07, 1.06, 1.06, 1.06, 1.06],
        closes=[1.085]*10,
    )
    events = detect_events_for_day(
        or_close_ts=or_close, or_high=or_high, or_low=or_low,
        pd_mid=1.08, pd_close=1.07, pd_or_high=1.12, pd_or_low=1.06,
        atr_at_setup=atr, m1=m1,
    )
    fbu = [e for e in events if e["event_type"] == "FALSE_BREAK_UP"]
    assert len(fbu) == 1


def test_no_look_ahead_events_only_after_or_close_ts():
    or_close = datetime(2026, 1, 1, 8, 0)
    times = [
        datetime(2026, 1, 1, 7, 59),
        datetime(2026, 1, 1, 8, 0),
        datetime(2026, 1, 1, 8, 1),
    ]
    m1 = {
        "times": np.array(times, dtype="object"),
        "highs": np.array([1.11, 1.12, 1.09]),
        "lows": np.array([1.09, 1.10, 1.08]),
        "closes": np.array([1.10, 1.11, 1.085]),
    }
    events = detect_events_for_day(
        or_close_ts=or_close, or_high=1.10, or_low=1.05,
        pd_mid=1.08, pd_close=1.07, pd_or_high=1.12, pd_or_low=1.06,
        atr_at_setup=0.01, m1=m1,
    )
    assert not any(e["event_type"] == "BREAK_UP" for e in events)
