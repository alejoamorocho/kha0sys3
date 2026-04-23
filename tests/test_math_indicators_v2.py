"""Smoke tests for the v2 math indicators (6 new families)."""
from __future__ import annotations
import polars as pl
import pytest
import numpy as np
from src.application.math_indicators import MathIndicatorEnricher


@pytest.fixture
def ohlc_df():
    """300-bar synthetic OHLC — enough for Hurst R/S window=100."""
    rng = np.random.default_rng(7)
    n = 300
    price = 100.0 + np.cumsum(rng.standard_normal(n) * 0.5)
    return pl.DataFrame({
        "time": pl.datetime_range(
            start=pl.datetime(2024, 1, 1), end=pl.datetime(2024, 1, 4, 14, 45),
            interval="15m", eager=True,
        )[:n],
        "open": price - 0.05,
        "high": price + 0.20,
        "low": price - 0.20,
        "close": price,
    })


def test_frac_diff_z_column_and_values(ohlc_df):
    out = MathIndicatorEnricher.add_frac_diff_z(ohlc_df)
    assert "frac_diff_z_50" in out.columns
    assert out["frac_diff_z_50"].drop_nulls().len() > 50


def test_shannon_entropy_columns(ohlc_df):
    out = MathIndicatorEnricher.add_shannon_entropy(ohlc_df)
    assert "shannon_entropy_50" in out.columns
    assert "shannon_entropy_drop_50" in out.columns
    # entropy must be non-negative on defined bars
    ent = out["shannon_entropy_50"].drop_nulls().to_numpy()
    ent = ent[~np.isnan(ent)]
    assert len(ent) > 0
    assert (ent >= 0).all()


def test_hurst_rs_in_range(ohlc_df):
    out = MathIndicatorEnricher.add_hurst_rs(ohlc_df)
    assert "hurst_rs_100" in out.columns
    h = out["hurst_rs_100"].drop_nulls().to_numpy()
    h = h[~np.isnan(h)]
    assert len(h) > 0
    # H should roughly be in (0, 1.5) for normal series
    assert h.min() > -0.5 and h.max() < 2.0


def test_spectral_ratio_column(ohlc_df):
    out = MathIndicatorEnricher.add_spectral_power_ratio(ohlc_df)
    assert "spectral_ratio_64" in out.columns
    sr = out["spectral_ratio_64"].drop_nulls().to_numpy()
    sr = sr[~np.isnan(sr)]
    assert len(sr) > 0
    assert (sr >= 0).all()


def test_kama_columns(ohlc_df):
    out = MathIndicatorEnricher.add_kama_slope(ohlc_df)
    assert "kama_10" in out.columns
    assert "kama_slope_10" in out.columns
    kama = out["kama_10"].drop_nulls().to_numpy()
    kama = kama[~np.isnan(kama)]
    closes = out["close"].to_numpy()
    assert len(kama) > 0
    # KAMA bounded within price range
    assert kama.min() >= closes.min() - 1.0
    assert kama.max() <= closes.max() + 1.0


def test_garch_vol_z_column(ohlc_df):
    out = MathIndicatorEnricher.add_garch_vol_spike(ohlc_df)
    assert "garch_vol_z_50" in out.columns


def test_enrich_all_math_v2_complete(ohlc_df):
    out = MathIndicatorEnricher.enrich_all_math(ohlc_df)
    expected_v2 = {
        "frac_diff_z_50", "shannon_entropy_50", "shannon_entropy_drop_50",
        "hurst_rs_100", "spectral_ratio_64",
        "kama_10", "kama_slope_10", "garch_vol_z_50",
    }
    missing = expected_v2 - set(out.columns)
    assert not missing, f"Missing v2 columns: {missing}"
    # existing v1 columns must still be present
    assert "velocity_10" in out.columns
    assert "kalman_state" in out.columns
    assert len(out) == len(ohlc_df)


def _no_lookahead(full, trunc, col, upto):
    for i in range(upto):
        a, b = full[col][i], trunc[col][i]
        if a is None or b is None:
            continue
        fa, fb = float(a), float(b)
        if math_isnan(fa) and math_isnan(fb):
            continue
        if math_isnan(fa) or math_isnan(fb):
            continue
        assert pytest.approx(fa, rel=1e-6, abs=1e-9) == fb, f"Look-ahead in {col} at bar {i}"


def math_isnan(x):
    return x != x


def test_no_lookahead_frac_diff(ohlc_df):
    full = MathIndicatorEnricher.add_frac_diff_z(ohlc_df)
    trunc = MathIndicatorEnricher.add_frac_diff_z(ohlc_df.head(150))
    _no_lookahead(full, trunc, "frac_diff_z_50", 140)


def test_no_lookahead_kama(ohlc_df):
    full = MathIndicatorEnricher.add_kama_slope(ohlc_df)
    trunc = MathIndicatorEnricher.add_kama_slope(ohlc_df.head(150))
    _no_lookahead(full, trunc, "kama_10", 140)
