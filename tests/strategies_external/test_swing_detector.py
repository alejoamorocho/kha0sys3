# tests/strategies_external/test_swing_detector.py
from datetime import datetime, timedelta

import polars as pl
import pytest

from src.strategies_external.strategies.swings import find_swings


def test_find_swings_basic(synthetic_w_df):
    """Find at least one local min near idx 10 (L1) and idx 35 (L2)."""
    swing_lows, swing_highs = find_swings(synthetic_w_df, prominence_factor=0.3, min_distance=5)
    # swing_lows is a list of (idx, price); we expect L1 around idx 10, L2 around idx 35
    low_idxs = [idx for idx, _ in swing_lows]
    assert any(8 <= i <= 12 for i in low_idxs), f"Expected L1 around idx 10, got {low_idxs}"
    assert any(33 <= i <= 37 for i in low_idxs), f"Expected L2 around idx 35, got {low_idxs}"


@pytest.fixture
def synthetic_w_df():
    base = datetime(2024, 1, 1)
    rows = []
    for i in range(50):
        if i <= 10:
            v = 110.0 - i * 1.0
        elif i <= 25:
            v = 100.0 + (i - 10) * 0.7
        elif i <= 35:
            v = 100.0 + 15 * 0.7 - (i - 25) * 0.95
        else:
            v = 101.0 + (i - 35) * 0.5
        rows.append((base + timedelta(days=i), v, v + 0.5, v - 0.5, v + 0.1, 1000.0))
    return pl.DataFrame(
        {"time": [r[0] for r in rows],
         "open": [r[1] for r in rows], "high": [r[2] for r in rows],
         "low": [r[3] for r in rows], "close": [r[4] for r in rows],
         "volume": [r[5] for r in rows]},
        schema={"time": pl.Datetime, "open": pl.Float64, "high": pl.Float64,
                "low": pl.Float64, "close": pl.Float64, "volume": pl.Float64},
    )


def test_find_swings_empty():
    df = pl.DataFrame(schema={"time": pl.Datetime, "open": pl.Float64,
                              "high": pl.Float64, "low": pl.Float64,
                              "close": pl.Float64, "volume": pl.Float64})
    lows, highs = find_swings(df, prominence_factor=0.5, min_distance=5)
    assert lows == [] and highs == []
