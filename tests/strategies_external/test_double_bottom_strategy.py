# tests/strategies_external/test_double_bottom_strategy.py
from datetime import datetime, timedelta

import polars as pl
import pytest

from src.strategies_external.strategies.double_bottom import DoubleBottomStrategy


@pytest.fixture
def double_bottom_df():
    """W pattern with neckline + post-breakout consolidation + breakout trigger."""
    base = datetime(2024, 1, 1)
    rows = []
    # idx 0-10: ramp down to L1 = 100
    for i in range(11):
        v = 110.0 - i * 1.0
        rows.append((base + timedelta(days=i), v, v + 0.4, v - 0.4, v, 1000.0))
    # idx 11-25: rally to neckline ~107
    for i in range(11, 26):
        v = 100.0 + (i - 10) * 0.45
        rows.append((base + timedelta(days=i), v, v + 0.4, v - 0.4, v, 1000.0))
    # idx 26-35: pullback to L2 = 101 (within 2% of L1=100)
    for i in range(26, 36):
        v = 107.0 - (i - 25) * 0.6
        rows.append((base + timedelta(days=i), v, v + 0.4, v - 0.4, v, 1000.0))
    # idx 36-45: rally back through neckline
    for i in range(36, 46):
        v = 101.0 + (i - 35) * 0.7
        rows.append((base + timedelta(days=i), v, v + 0.4, v - 0.4, v, 1000.0))
    # idx 46-50: consolidation just above neckline
    for i in range(46, 51):
        rows.append((base + timedelta(days=i), 108.0, 108.4, 107.6, 108.0, 1000.0))
    return pl.DataFrame(
        {"time": [r[0] for r in rows],
         "open": [r[1] for r in rows], "high": [r[2] for r in rows],
         "low": [r[3] for r in rows], "close": [r[4] for r in rows],
         "volume": [r[5] for r in rows]},
        schema={"time": pl.Datetime, "open": pl.Float64, "high": pl.Float64,
                "low": pl.Float64, "close": pl.Float64, "volume": pl.Float64},
    )


def test_double_bottom_detects_pattern(double_bottom_df):
    strat = DoubleBottomStrategy(tolerance=0.02, min_separation=15, max_separation=80,
                                 consol_min_bars=3, consol_max_atr_mult=1.5)
    sigs = strat.generate_signals(double_bottom_df, symbol="XAUUSD")
    assert len(sigs) >= 1
    s = sigs[-1]
    assert s.side == "long"
    for k in ("L1", "L2", "neckline", "altura_patron", "atr14"):
        assert k in s.indicator_anchors


def test_double_bottom_no_signal_when_distant():
    """L1 and L2 too far apart in price (>tolerance) -> no signal."""
    base = datetime(2024, 1, 1)
    rows = []
    for i in range(50):
        v = 100.0 + i * 0.1  # monotone up, no W
        rows.append((base + timedelta(days=i), v, v + 0.3, v - 0.3, v, 1000.0))
    df = pl.DataFrame(
        {"time": [r[0] for r in rows],
         "open": [r[1] for r in rows], "high": [r[2] for r in rows],
         "low": [r[3] for r in rows], "close": [r[4] for r in rows],
         "volume": [r[5] for r in rows]},
        schema={"time": pl.Datetime, "open": pl.Float64, "high": pl.Float64,
                "low": pl.Float64, "close": pl.Float64, "volume": pl.Float64},
    )
    strat = DoubleBottomStrategy()
    assert strat.generate_signals(df, symbol="XAUUSD") == []
