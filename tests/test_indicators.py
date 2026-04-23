"""Unit tests for indicator calculations. Reference values computed vs TA-Lib."""
import polars as pl
import pytest
from src.application.indicators import IndicatorEnricher


@pytest.fixture
def ohlc_df():
    """30 deterministic bars for stable indicator math."""
    closes = [
        44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84, 46.08,
        45.89, 46.03, 45.61, 46.28, 46.28, 46.00, 46.03, 46.41, 46.22, 45.64,
        46.21, 46.25, 45.71, 46.45, 45.78, 45.35, 44.03, 44.18, 44.22, 44.57,
    ]
    highs = [c + 0.20 for c in closes]
    lows = [c - 0.20 for c in closes]
    opens = [c - 0.05 for c in closes]
    return pl.DataFrame({
        "time": pl.datetime_range(
            start=pl.datetime(2024, 1, 1), end=pl.datetime(2024, 1, 1, 7, 15),
            interval="15m", eager=True,
        )[:30],
        "open": opens, "high": highs, "low": lows, "close": closes,
    })


def test_rsi_14_matches_reference(ohlc_df):
    """RSI(14) on Wilder's smoothing at bar 14 ≈ 70.53."""
    out = IndicatorEnricher.add_rsi(ohlc_df, period=14)
    rsi_14 = out["rsi_14"].to_list()[14]
    assert rsi_14 == pytest.approx(70.53, abs=0.5)


def test_macd_columns_present(ohlc_df):
    out = IndicatorEnricher.add_macd(ohlc_df, fast=12, slow=26, signal=9)
    assert {"macd", "macd_signal", "macd_hist"}.issubset(out.columns)
    # At the last bar, MACD and signal should both be defined
    last = out.row(-1, named=True)
    assert last["macd"] is not None
    assert last["macd_signal"] is not None


def test_bollinger_bands_contain_price_at_mean(ohlc_df):
    out = IndicatorEnricher.add_bollinger(ohlc_df, period=20, std_mult=2.0)
    row = out.row(25, named=True)
    assert row["bb_lower"] <= row["bb_middle"] <= row["bb_upper"]
    assert 0.0 <= row["bb_pct"] <= 1.5  # price usually within or slightly beyond


def test_fractal_marks_local_extrema(ohlc_df):
    out = IndicatorEnricher.add_fractals(ohlc_df, window=5)
    # At least one fractal_high and one fractal_low should exist in 30 bars
    assert out["fractal_high"].sum() >= 1
    assert out["fractal_low"].sum() >= 1
    # Fractals cannot exist in first 2 or last 2 bars (confirmation lag)
    assert out["fractal_high"].to_list()[0] is False
    assert out["fractal_high"].to_list()[-1] is False


def test_adx_in_valid_range(ohlc_df):
    out = IndicatorEnricher.add_adx(ohlc_df, period=14)
    adx = out["adx_14"].drop_nulls().to_list()
    assert len(adx) > 0
    assert all(0 <= v <= 100 for v in adx)


def test_no_lookahead_in_any_indicator(ohlc_df):
    """Given bars [0..N], indicator values at bar K must not change when bars K+1..N are removed."""
    full = IndicatorEnricher.enrich_all(ohlc_df)
    trunc = IndicatorEnricher.enrich_all(ohlc_df.head(20))
    for col in ["rsi_14", "macd", "bb_upper", "adx_14"]:
        for i in range(19):  # compare bars 0..18 (last bar has fractal confirmation lag)
            a = full[col].to_list()[i]
            b = trunc[col].to_list()[i]
            if a is None and b is None:
                continue
            assert a == pytest.approx(b, rel=1e-9), f"look-ahead in {col} at bar {i}"
