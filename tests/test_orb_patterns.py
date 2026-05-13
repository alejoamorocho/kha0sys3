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
