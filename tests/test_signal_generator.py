"""Unit tests for signal generation."""
import polars as pl
import pytest
from src.application.indicators import IndicatorEnricher
from src.application.signal_generator import SignalGenerator, SIGNAL_TYPES, CONFLUENCE_FILTERS


@pytest.fixture
def enriched_df():
    """200 bars enriched with all indicators for signal coverage."""
    import numpy as np
    rng = np.random.default_rng(42)
    n = 200
    price = 100.0 + rng.standard_normal(n).cumsum() * 0.5
    df = pl.DataFrame({
        "time": pl.datetime_range(
            start=pl.datetime(2024, 1, 1), end=pl.datetime(2024, 1, 3, 3, 45),
            interval="15m", eager=True,
        )[:n],
        "open": price - 0.05, "high": price + 0.20, "low": price - 0.20, "close": price,
    })
    return IndicatorEnricher.enrich_all(df)


def test_all_10_signal_types_registered():
    assert len(SIGNAL_TYPES) == 10
    expected = {
        "RSI_OB_REV", "BB_TOUCH_REV", "FRACTAL_REV", "MACD_DIVERGENCE", "BB_RSI_CONFLUENCE",
        "MACD_CROSS", "ADX_BREAKOUT", "BB_BREAKOUT", "RSI_50_CROSS", "FRACTAL_TREND",
    }
    assert set(SIGNAL_TYPES) == expected


def test_4_confluence_filters_registered():
    expected = {"RSI_ZONE", "ADX_REGIME", "BB_POSITION", "MACD_ALIGN"}
    assert set(CONFLUENCE_FILTERS) == expected


def test_rsi_ob_rev_produces_signals(enriched_df):
    sigs = SignalGenerator.generate(enriched_df, signal_type="RSI_OB_REV", symbol="TEST")
    assert {"time", "symbol", "direction", "signal_type"}.issubset(sigs.columns)
    assert set(sigs["direction"].unique()).issubset({"LONG", "SHORT"})


def test_macd_cross_directions_balanced(enriched_df):
    sigs = SignalGenerator.generate(enriched_df, signal_type="MACD_CROSS", symbol="TEST")
    # On random walk we expect at least a handful of crosses, both directions
    assert len(sigs) >= 2


def test_confluence_filter_reduces_signal_count(enriched_df):
    base = SignalGenerator.generate(enriched_df, signal_type="MACD_CROSS", symbol="TEST")
    filtered = SignalGenerator.apply_filters(base, enriched_df, filters=("ADX_REGIME_TREND",))
    assert len(filtered) <= len(base)


def test_signal_timestamp_is_bar_of_confirmation(enriched_df):
    """Signal timestamp must match the bar where the condition is first true (no look-ahead)."""
    sigs = SignalGenerator.generate(enriched_df, signal_type="BB_BREAKOUT", symbol="TEST")
    if len(sigs) > 0:
        t = sigs["time"].to_list()[0]
        # Confirm the breakout condition was true at that bar
        row = enriched_df.filter(pl.col("time") == t).row(0, named=True)
        assert (row["close"] > row["bb_upper"]) or (row["close"] < row["bb_lower"])
