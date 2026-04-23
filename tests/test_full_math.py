"""Tests for full-math discovery pipeline."""
from __future__ import annotations

import numpy as np
import polars as pl
import pytest

from src.engine.run_full_math import (
    MATH_SIGNALS,
    MATH_SIGNAL_FAMILY,
    GUARD_NAMES,
    EXIT_STYLES,
    _guard_subsets,
    _precompute_guard_columns,
    _apply_guards_to_signals,
    _run_full_math_backtest,
)


def test_family_mapping_covers_all_signals():
    missing = [s for s in MATH_SIGNALS if s not in MATH_SIGNAL_FAMILY]
    assert not missing, f"Signals missing family: {missing}"
    valid = {"meanrev", "momentum", "structural"}
    for s, fam in MATH_SIGNAL_FAMILY.items():
        assert fam in valid, f"Bad family for {s}: {fam}"


def test_guard_subsets_count():
    subs = _guard_subsets()
    # C(4,0)+C(4,1)+C(4,2)+C(4,3) = 1+4+6+4 = 15
    assert len(subs) == 15
    assert () in subs
    assert all(len(s) <= 3 for s in subs)


def _synthetic_bars(n: int = 300, seed: int = 0) -> pl.DataFrame:
    rng = np.random.default_rng(seed)
    price = 100.0 + np.cumsum(rng.standard_normal(n) * 0.1)
    times = pl.datetime_range(
        start=pl.datetime(2024, 1, 1, 0, 0),
        interval="15m",
        end=pl.datetime(2024, 1, 1, 0, 0) + pl.duration(minutes=15 * (n - 1)),
        eager=True,
    )
    return pl.DataFrame({
        "time": times,
        "open": price,
        "high": price + 0.3,
        "low": price - 0.3,
        "close": price,
        "atr_14": [0.5] * n,
        # Math cols needed by guards / exits
        "accel_10": rng.standard_normal(n) * 0.1,
        "kalman_innovation": rng.standard_normal(n) * 0.1,
        "curvature_10": rng.standard_normal(n) * 0.01,
        "hurst_rs_100": np.clip(0.5 + rng.standard_normal(n) * 0.1, 0.1, 0.9),
        "velocity_10": rng.standard_normal(n) * 0.05,
        "ols_resid_z_30": rng.standard_normal(n),
        "meanrev_area_50": rng.standard_normal(n),
        "kalman_state": price + rng.standard_normal(n) * 0.05,
        "kama_10": price + rng.standard_normal(n) * 0.05,
        "zscore_30": rng.standard_normal(n),
        "spectral_ratio_64": 1.5 + rng.standard_normal(n) * 0.5,
    })


def test_guard_filtering_reduces_count():
    bars = _synthetic_bars()
    bars_g = _precompute_guard_columns(bars)
    # Fake signals: one per bar
    signals = bars.select(["time", "close", "high", "low", "atr_14"]).with_columns([
        pl.lit("TEST").alias("symbol"),
        pl.lit("LONG").alias("direction"),
        pl.lit("ZSCORE_REV").alias("signal_type"),
    ])
    sub = _apply_guards_to_signals(signals, bars_g, ("VELOCITY_DECEL",), "ZSCORE_REV")
    assert len(sub) < len(signals)
    sub2 = _apply_guards_to_signals(signals, bars_g,
                                    ("VELOCITY_DECEL", "KALMAN_INNOV_PEAK",
                                     "CURVATURE_INFLECTION", "REGIME_COHERENCE"),
                                    "ZSCORE_REV")
    assert len(sub2) <= len(sub)
    # No-guard should be identity
    same = _apply_guards_to_signals(signals, bars_g, (), "ZSCORE_REV")
    assert len(same) == len(signals)


def test_hard_sl_triggers():
    """Craft a scenario where price plummets after a LONG — hard SL must fire."""
    n = 60
    # Price drops sharply after bar 10
    price = np.concatenate([
        np.full(11, 100.0),
        np.linspace(100.0, 90.0, n - 11),
    ])
    times = pl.datetime_range(
        start=pl.datetime(2024, 1, 1, 0, 0),
        interval="15m",
        end=pl.datetime(2024, 1, 1, 0, 0) + pl.duration(minutes=15 * (n - 1)),
        eager=True,
    )
    bars = pl.DataFrame({
        "time": times,
        "open": price, "high": price + 0.1, "low": price - 0.1, "close": price,
        "atr_14": [1.0] * n,
        # minimal math cols (unused since exits=())
        "velocity_10": [0.0] * n, "accel_10": [0.0] * n, "curvature_10": [0.0] * n,
        "kalman_innovation": [0.0] * n, "kalman_state": price,
        "kama_10": price, "ols_resid_z_30": [0.0] * n,
        "meanrev_area_50": [0.0] * n, "zscore_30": [0.0] * n,
        "hurst_rs_100": [0.5] * n, "spectral_ratio_64": [1.5] * n,
    })
    sig_row = bars.row(10, named=True)
    signals = pl.DataFrame({
        "time": [sig_row["time"]], "symbol": ["X"], "direction": ["LONG"],
        "signal_type": ["TEST"],
        "close": [sig_row["close"]], "high": [sig_row["high"]],
        "low": [sig_row["low"]], "atr_14": [sig_row["atr_14"]],
    })
    trades = _run_full_math_backtest(
        signals, bars, exits=(),
        hard_sl_atr=3.0, session_end_hour=24, friction_r=0.0,
    )
    assert len(trades) == 1
    assert trades["exit_reason"][0] == "SL"
    # r_multiple must be close to -1
    assert trades["r_multiple"][0] < -0.9


def test_velocity_flip_exit_fires():
    """LONG entry; velocity flips from positive to negative -> VELOCITY_FLIP closes at close."""
    n = 40
    price = np.full(n, 100.0)
    # Engineer velocity: positive before bar 15, negative after.
    vel = np.concatenate([np.full(15, 0.1), np.full(n - 15, -0.1)])
    times = pl.datetime_range(
        start=pl.datetime(2024, 1, 1, 0, 0),
        interval="15m",
        end=pl.datetime(2024, 1, 1, 0, 0) + pl.duration(minutes=15 * (n - 1)),
        eager=True,
    )
    bars = pl.DataFrame({
        "time": times,
        "open": price, "high": price + 0.01, "low": price - 0.01, "close": price,
        "atr_14": [1.0] * n,
        "velocity_10": vel, "accel_10": [0.0] * n, "curvature_10": [0.0] * n,
        "kalman_innovation": [0.0] * n, "kalman_state": price,
        "kama_10": price, "ols_resid_z_30": [0.0] * n,
        "meanrev_area_50": [0.0] * n, "zscore_30": [0.0] * n,
        "hurst_rs_100": [0.5] * n, "spectral_ratio_64": [1.5] * n,
    })
    sig_row = bars.row(10, named=True)
    signals = pl.DataFrame({
        "time": [sig_row["time"]], "symbol": ["X"], "direction": ["LONG"],
        "signal_type": ["TEST"],
        "close": [sig_row["close"]], "high": [sig_row["high"]],
        "low": [sig_row["low"]], "atr_14": [sig_row["atr_14"]],
    })
    trades = _run_full_math_backtest(
        signals, bars, exits=("VELOCITY_FLIP",),
        hard_sl_atr=3.0, session_end_hour=24, friction_r=0.0,
    )
    assert len(trades) == 1
    assert trades["exit_reason"][0] == "VELOCITY_FLIP"


def test_zscore_neutral_exit_fires():
    """LONG entry while z=-1; z rises and crosses 0 -> ZSCORE_NEUTRAL closes."""
    n = 40
    price = np.full(n, 100.0)
    z = np.concatenate([np.full(15, -1.0), np.full(n - 15, 1.0)])
    times = pl.datetime_range(
        start=pl.datetime(2024, 1, 1, 0, 0),
        interval="15m",
        end=pl.datetime(2024, 1, 1, 0, 0) + pl.duration(minutes=15 * (n - 1)),
        eager=True,
    )
    bars = pl.DataFrame({
        "time": times,
        "open": price, "high": price + 0.01, "low": price - 0.01, "close": price,
        "atr_14": [1.0] * n,
        "velocity_10": [0.0] * n, "accel_10": [0.0] * n, "curvature_10": [0.0] * n,
        "kalman_innovation": [0.0] * n, "kalman_state": price,
        "kama_10": price, "ols_resid_z_30": [0.0] * n,
        "meanrev_area_50": [0.0] * n, "zscore_30": z,
        "hurst_rs_100": [0.5] * n, "spectral_ratio_64": [1.5] * n,
    })
    sig_row = bars.row(10, named=True)
    signals = pl.DataFrame({
        "time": [sig_row["time"]], "symbol": ["X"], "direction": ["LONG"],
        "signal_type": ["TEST"],
        "close": [sig_row["close"]], "high": [sig_row["high"]],
        "low": [sig_row["low"]], "atr_14": [sig_row["atr_14"]],
    })
    trades = _run_full_math_backtest(
        signals, bars, exits=("ZSCORE_NEUTRAL",),
        hard_sl_atr=3.0, session_end_hour=24, friction_r=0.0,
    )
    assert len(trades) == 1
    assert trades["exit_reason"][0] == "ZSCORE_NEUTRAL"


def test_exit_styles_count():
    assert len(EXIT_STYLES) == 10
    assert len(set(EXIT_STYLES)) == 10


def test_guard_names_count():
    assert len(GUARD_NAMES) == 4
