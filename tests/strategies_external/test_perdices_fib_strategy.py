# tests/strategies_external/test_perdices_fib_strategy.py
from datetime import datetime, timedelta

import polars as pl
import pytest

from src.strategies_external.strategies.perdices_fib import PerdicesFibStrategy


@pytest.fixture
def perdices_long_df():
    """H1 OHLC: clear uptrend on 4H, then 1H pullback to fib zone with RSI<40 turning up."""
    base = datetime(2024, 1, 1)
    rows = []
    # 200 bars H1 (8 days):
    # bars 0-100: monotonic uptrend 1900 -> 1950
    # bars 100-150: pullback 1950 -> 1925 (50% retrace)
    # bars 150-200: rally back to 1960
    for i in range(200):
        if i <= 100:
            v = 1900.0 + i * 0.5
        elif i <= 150:
            v = 1950.0 - (i - 100) * 0.5
        else:
            v = 1925.0 + (i - 150) * 0.7
        rows.append((base + timedelta(hours=i), v, v + 1.0, v - 1.0, v, 1000.0))
    return pl.DataFrame(
        {"time": [r[0] for r in rows],
         "open": [r[1] for r in rows], "high": [r[2] for r in rows],
         "low": [r[3] for r in rows], "close": [r[4] for r in rows],
         "volume": [r[5] for r in rows]},
        schema={"time": pl.Datetime, "open": pl.Float64, "high": pl.Float64,
                "low": pl.Float64, "close": pl.Float64, "volume": pl.Float64},
    )


def test_perdices_fib_detects_long(perdices_long_df):
    strat = PerdicesFibStrategy()
    sigs = strat.generate_signals(perdices_long_df, symbol="XAUUSD")
    long_sigs = [s for s in sigs if s.side == "long"]
    assert len(long_sigs) >= 1
    s = long_sigs[0]
    for k in ("swing_high", "swing_low", "fib_382", "fib_50", "rsi", "atr14"):
        assert k in s.indicator_anchors


def test_perdices_fib_no_signal_in_downtrend():
    """Monotonic downtrend -> trend_up filter fails -> no longs."""
    base = datetime(2024, 1, 1)
    rows = [(base + timedelta(hours=i), 1950.0 - i * 0.3,
             1950.0 - i * 0.3 + 1, 1950.0 - i * 0.3 - 1,
             1950.0 - i * 0.3, 1000.0) for i in range(200)]
    df = pl.DataFrame(
        {"time": [r[0] for r in rows],
         "open": [r[1] for r in rows], "high": [r[2] for r in rows],
         "low": [r[3] for r in rows], "close": [r[4] for r in rows],
         "volume": [r[5] for r in rows]},
        schema={"time": pl.Datetime, "open": pl.Float64, "high": pl.Float64,
                "low": pl.Float64, "close": pl.Float64, "volume": pl.Float64},
    )
    strat = PerdicesFibStrategy()
    sigs = strat.generate_signals(df, symbol="XAUUSD")
    long_sigs = [s for s in sigs if s.side == "long"]
    assert long_sigs == []
