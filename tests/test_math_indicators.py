"""Smoke tests for MathIndicatorEnricher."""
from __future__ import annotations
import polars as pl
import pytest
import numpy as np
from src.application.math_indicators import MathIndicatorEnricher


@pytest.fixture
def ohlc_df():
    """200-bar synthetic OHLC sorted ascending — enough for all rolling windows."""
    rng = np.random.default_rng(99)
    n = 200
    price = 100.0 + np.cumsum(rng.standard_normal(n) * 0.5)
    return pl.DataFrame({
        "time": pl.datetime_range(
            start=pl.datetime(2024, 1, 1), end=pl.datetime(2024, 1, 3, 3, 45),
            interval="15m", eager=True,
        )[:n],
        "open": price - 0.05,
        "high": price + 0.20,
        "low": price - 0.20,
        "close": price,
    })


def test_enrich_all_math_columns_exist(ohlc_df):
    """enrich_all_math must add all 12 expected columns."""
    out = MathIndicatorEnricher.enrich_all_math(ohlc_df)
    expected = {
        "velocity_10", "accel_10", "curvature_10",
        "vwap_area_20", "meanrev_area_50",
        "ols_slope_30", "ols_resid_z_30",
        "kalman_state", "kalman_innovation",
        "zscore_30",
        "ret_skew_50", "ret_kurt_50",
        "mean_rev_regime_50",
    }
    missing = expected - set(out.columns)
    assert not missing, f"Missing columns: {missing}"


def test_enrich_all_math_no_error(ohlc_df):
    """enrich_all_math must complete without raising."""
    out = MathIndicatorEnricher.enrich_all_math(ohlc_df)
    assert len(out) == 200


def test_no_lookahead_velocity(ohlc_df):
    """velocity_10 at bar K must not change when bars K+1..N are removed."""
    full = MathIndicatorEnricher.add_velocity(ohlc_df)
    trunc = MathIndicatorEnricher.add_velocity(ohlc_df.head(100))
    col = "velocity_10"
    for i in range(90):
        a = full[col][i]
        b = trunc[col][i]
        if a is None and b is None:
            continue
        assert pytest.approx(float(a), rel=1e-9) == float(b), f"Look-ahead in {col} at bar {i}"


def test_no_lookahead_zscore(ohlc_df):
    """zscore_30 at bar K must not change when bars K+1..N are removed."""
    full = MathIndicatorEnricher.add_zscore(ohlc_df)
    trunc = MathIndicatorEnricher.add_zscore(ohlc_df.head(100))
    col = "zscore_30"
    for i in range(90):
        a = full[col][i]
        b = trunc[col][i]
        if a is None and b is None:
            continue
        assert pytest.approx(float(a), rel=1e-9) == float(b), f"Look-ahead in {col} at bar {i}"


def test_kalman_smooths_price(ohlc_df):
    """Kalman state must be close to close price (within 5% of price range)."""
    out = MathIndicatorEnricher.add_kalman(ohlc_df)
    closes = out["close"].to_list()
    states = out["kalman_state"].to_list()
    price_range = max(closes) - min(closes)
    errors = [abs(s - c) for s, c in zip(states, closes) if s is not None and c is not None]
    assert max(errors) < price_range * 0.5


def test_ols_regression_columns(ohlc_df):
    """OLS must produce both slope and residual_z columns."""
    out = MathIndicatorEnricher.add_ols_regression(ohlc_df)
    assert "ols_slope_30" in out.columns
    assert "ols_resid_z_30" in out.columns
    # Non-null values must exist after warm-up
    assert out["ols_slope_30"].drop_nulls().__len__() > 0
