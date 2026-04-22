"""Tests for Math FADE pipeline: detectors, direction guard, fill semantics, TP."""
from __future__ import annotations
from datetime import datetime, timedelta
import polars as pl
import pytest

from src.engine.run_math_fade import (
    detect_setups, run_backtest, BacktestConfig,
)


def _make_bars(closes, highs=None, lows=None, start="2024-01-02 09:00", extras=None):
    """Build a minimal M15 bars DataFrame with required columns."""
    n = len(closes)
    base = datetime.fromisoformat(start)
    times = [base + timedelta(minutes=15 * i) for i in range(n)]
    highs = highs if highs is not None else [c + 0.1 for c in closes]
    lows = lows if lows is not None else [c - 0.1 for c in closes]
    data = {
        "time": times,
        "open": list(closes),
        "high": list(highs),
        "low": list(lows),
        "close": list(closes),
        "atr_14": [1.0] * n,
        "kalman_innovation": [0.0] * n,
        "kalman_state": list(closes),
        "zscore_30": [0.0] * n,
        "ols_resid_z_30": [0.0] * n,
        "curvature_10": [0.0] * n,
        "meanrev_area_50": [0.0] * n,
        "garch_vol_z_50": [0.0] * n,
    }
    if extras:
        data.update(extras)
    return pl.DataFrame(data)


def test_zscore_extreme_fade_detects():
    """Bar T-1 has |z|>=2, bar T decays -> fire SHORT (z>0 -> fade short)."""
    n = 20
    z = [0.0] * n
    z[10] = 2.5  # extreme at T-1
    z[11] = 1.5  # decay at T
    bars = _make_bars([100.0] * n, extras={"zscore_30": z})
    setups = detect_setups(bars, "ZSCORE_EXTREME_FADE")
    assert len(setups) == 1
    row = setups.row(0, named=True)
    assert row["direction"] == "SHORT"
    assert row["time"] == bars["time"][11]


def test_ols_extreme_fade_detects_long():
    n = 20
    r = [0.0] * n
    r[5] = -2.5
    r[6] = -1.2
    bars = _make_bars([100.0] * n, extras={"ols_resid_z_30": r})
    setups = detect_setups(bars, "OLS_EXTREME_FADE")
    assert len(setups) == 1
    assert setups.row(0, named=True)["direction"] == "LONG"


def test_direction_guard_cancels_when_extreme_grows():
    """After extreme at T-1 (z=2.5) and decay at T (z=1.5), in wait window
    z climbs back to 3.0 -> guard cancels the LIMIT."""
    n = 30
    z = [0.0] * n
    z[10] = 2.5
    z[11] = 1.5  # fire bar
    z[12] = 3.0  # grows beyond original -> cancel
    closes = [100.0] * n
    bars = _make_bars(closes, extras={"zscore_30": z})
    setups = detect_setups(bars, "ZSCORE_EXTREME_FADE")
    cfg = BacktestConfig(tp_atr_mult=0.5, sl_atr_mult=2.5,
                         session_end_hour_utc=23, friction_r=0.0)
    trades = run_backtest(setups, bars, "ZSCORE_EXTREME_FADE", cfg, "TEST")
    assert len(trades) == 0


def test_limit_not_filled_if_no_retest():
    """Fade SHORT at close=100 requires bar high>=100 in wait window.
    If subsequent bars never retest, no fill."""
    n = 30
    z = [0.0] * n
    z[10] = 2.5
    z[11] = 1.5
    closes = [100.0] * n
    # After the fire bar, price drops and never retests
    highs = [c + 0.1 for c in closes]
    lows = [c - 0.1 for c in closes]
    for i in range(12, 17):
        closes[i] = 99.0
        highs[i] = 99.05
        lows[i] = 98.9
    bars = _make_bars(closes, highs=highs, lows=lows, extras={"zscore_30": z})
    setups = detect_setups(bars, "ZSCORE_EXTREME_FADE")
    cfg = BacktestConfig(tp_atr_mult=0.5, sl_atr_mult=2.5,
                         session_end_hour_utc=23, friction_r=0.0)
    trades = run_backtest(setups, bars, "ZSCORE_EXTREME_FADE", cfg, "TEST")
    assert len(trades) == 0


def test_fill_and_tp_hit_yields_positive_r():
    """SHORT fade at z=2.5 decay: fills on retest then TP hits (price drops)."""
    n = 40
    z = [0.0] * n
    z[10] = 2.5
    z[11] = 1.5
    closes = [100.0] * n
    highs = [c + 0.1 for c in closes]
    lows = [c - 0.1 for c in closes]
    # Bar 12: retest up to 100.2 -> LIMIT fills at 100 for SHORT
    highs[12] = 100.2
    lows[12] = 99.9
    closes[12] = 100.0
    # z stays within bounds (no guard trigger)
    # Bar 13: price drops to TP = 100 - 0.5*1.0 = 99.5. Low must reach 99.5.
    closes[13] = 99.4
    lows[13] = 99.3
    highs[13] = 99.9
    bars = _make_bars(closes, highs=highs, lows=lows, extras={"zscore_30": z})
    setups = detect_setups(bars, "ZSCORE_EXTREME_FADE")
    assert len(setups) == 1
    cfg = BacktestConfig(tp_atr_mult=0.5, sl_atr_mult=2.5,
                         session_end_hour_utc=23, friction_r=0.0)
    trades = run_backtest(setups, bars, "ZSCORE_EXTREME_FADE", cfg, "TEST")
    assert len(trades) == 1
    row = trades.row(0, named=True)
    assert row["exit_reason"] == "TP"
    # r = (100 - 99.5) / (2.5 * 1.0) = 0.2
    assert abs(row["r_multiple"] - 0.2) < 1e-9


def test_garch_z_fade_detects():
    n = 20
    gv = [0.0] * n
    z = [0.0] * n
    gv[10] = 2.5  # vol spike
    z[10] = 1.8   # price extreme (positive -> SHORT)
    bars = _make_bars([100.0] * n, extras={"zscore_30": z, "garch_vol_z_50": gv})
    setups = detect_setups(bars, "GARCH_Z_FADE")
    assert len(setups) >= 1
    # first fire at bar 10
    first = setups.row(0, named=True)
    assert first["direction"] == "SHORT"
