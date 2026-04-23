"""Tests for Math MOMENTUM pipeline: detectors, direction guard, STOP fill, TP/SL."""
from __future__ import annotations
from datetime import datetime, timedelta

import polars as pl

from src.engine.run_math_momentum import (
    detect_setups, run_backtest, BacktestConfig,
)


def _make_bars(closes, highs=None, lows=None, start="2024-01-02 09:00", extras=None):
    """Build a minimal M15 bars DataFrame with required math columns."""
    n = len(closes)
    base = datetime.fromisoformat(start)
    times = [base + timedelta(minutes=15 * i) for i in range(n)]
    highs = list(highs) if highs is not None else [c + 0.1 for c in closes]
    lows = list(lows) if lows is not None else [c - 0.1 for c in closes]
    data = {
        "time": times,
        "open": list(closes),
        "high": highs,
        "low": lows,
        "close": list(closes),
        "atr_14": [1.0] * n,
        "velocity_10": [0.0] * n,
        "accel_10": [0.0] * n,
        "kama_10": list(closes),
        "kama_slope_10": [0.0] * n,
        "ols_slope_30": [0.0] * n,
        "hurst_rs_100": [0.5] * n,
        "kalman_innovation": [0.0] * n,
        "spectral_ratio_64": [1.0] * n,
    }
    if extras:
        data.update(extras)
    return pl.DataFrame(data)


def test_velocity_accel_go_detects_long():
    """A trending regime where velocity and acceleration align produces LONG setup."""
    n = 80
    # Velocity and accel grow in the last bars (trend up)
    vel = [0.0] * n
    acc = [0.0] * n
    # supply enough variance in earlier bars so rolling_std is meaningful
    for i in range(10, 60):
        vel[i] = 0.1 * ((i % 3) - 1)  # noise around 0
        acc[i] = 0.05 * ((i % 2) - 0.5)
    vel[70] = 1.0   # big positive velocity
    acc[70] = 0.3   # positive accel
    bars = _make_bars([100.0] * n, extras={"velocity_10": vel, "accel_10": acc})
    setups = detect_setups(bars, "VELOCITY_ACCEL_GO")
    assert len(setups) >= 1
    assert any(r["direction"] == "LONG" for r in setups.iter_rows(named=True))


def test_ols_slope_strong_detects():
    """Strong rising positive slope produces LONG setup."""
    n = 80
    s = [0.0] * n
    # noisy slope early
    for i in range(10, 60):
        s[i] = 0.01 * ((i % 3) - 1)
    # two large consecutive same-sign slopes with magnitude rising
    s[68] = 0.5
    s[69] = 0.8   # T: bigger magnitude, same sign
    bars = _make_bars([100.0] * n, extras={"ols_slope_30": s})
    setups = detect_setups(bars, "OLS_SLOPE_STRONG")
    assert len(setups) >= 1
    r = setups.row(0, named=True)
    assert r["direction"] == "LONG"


def test_direction_guard_cancels_when_indicator_weakens():
    """Setup fires but in the wait window the guard indicator drops below half
    of its initial magnitude -> STOP cancelled, no trade."""
    n = 80
    s = [0.0] * n
    for i in range(10, 60):
        s[i] = 0.01 * ((i % 3) - 1)
    s[68] = 0.5
    s[69] = 0.8  # fire at i=69 with guard_value=0.8
    # In wait window bars (70..74), slope collapses to a very small positive value
    s[70] = 0.1   # 0.1 < 0.5*0.8=0.4 -> weaken -> cancel
    s[71] = 0.1
    closes = [100.0] * n
    highs = [c + 0.1 for c in closes]
    lows = [c - 0.1 for c in closes]
    # Make bar 70 high exceed the stop price so normally it would fill without guard.
    # stop_price = close[69] + 0.5*1.0 = 100.5 for LONG.
    highs[70] = 101.0
    bars = _make_bars(closes, highs=highs, lows=lows, extras={"ols_slope_30": s})
    setups = detect_setups(bars, "OLS_SLOPE_STRONG")
    assert len(setups) >= 1
    cfg = BacktestConfig(tp_atr_mult=2.0, sl_atr_mult=1.0,
                         session_end_hour_utc=23, friction_r=0.0)
    trades = run_backtest(setups, bars, "OLS_SLOPE_STRONG", cfg, "TEST")
    assert len(trades) == 0


def test_stop_not_filled_if_price_never_breaks():
    """LONG STOP at 100.5 requires high>=100.5 in wait window. If price stays
    below, no fill."""
    n = 80
    s = [0.0] * n
    for i in range(10, 60):
        s[i] = 0.01 * ((i % 3) - 1)
    s[68] = 0.5
    s[69] = 0.8
    # guard stays strong (so no cancel) but price never breaks up
    for i in range(70, 75):
        s[i] = 0.8
    closes = [100.0] * n
    highs = [c + 0.1 for c in closes]  # max 100.1, well below 100.5
    lows = [c - 0.1 for c in closes]
    bars = _make_bars(closes, highs=highs, lows=lows, extras={"ols_slope_30": s})
    setups = detect_setups(bars, "OLS_SLOPE_STRONG")
    assert len(setups) >= 1
    cfg = BacktestConfig(tp_atr_mult=2.0, sl_atr_mult=1.0,
                         session_end_hour_utc=23, friction_r=0.0)
    trades = run_backtest(setups, bars, "OLS_SLOPE_STRONG", cfg, "TEST")
    assert len(trades) == 0


def test_fill_and_tp_hit_yields_correct_r_multiple():
    """STOP fills on breakout, then TP hit. r_multiple should be +tp/sl ratio."""
    n = 80
    s = [0.0] * n
    for i in range(10, 60):
        s[i] = 0.01 * ((i % 3) - 1)
    s[68] = 0.5
    s[69] = 0.8
    for i in range(70, 75):
        s[i] = 0.8  # guard stays strong
    closes = [100.0] * n
    highs = [c + 0.1 for c in closes]
    lows = [c - 0.1 for c in closes]
    # stop_price = close[69] + 0.5*atr = 100 + 0.5 = 100.5
    # bar 70: price breaks up to 100.6 -> fill at 100.5
    highs[70] = 100.6
    closes[70] = 100.55
    # bar 71: hits TP at entry + 2.0*1.0 = 102.5
    highs[71] = 102.7
    closes[71] = 102.6
    bars = _make_bars(closes, highs=highs, lows=lows, extras={"ols_slope_30": s})
    setups = detect_setups(bars, "OLS_SLOPE_STRONG")
    assert len(setups) >= 1
    cfg = BacktestConfig(tp_atr_mult=2.0, sl_atr_mult=1.0,
                         session_end_hour_utc=23, friction_r=0.0)
    trades = run_backtest(setups, bars, "OLS_SLOPE_STRONG", cfg, "TEST")
    assert len(trades) == 1
    row = trades.row(0, named=True)
    assert row["exit_reason"] == "TP"
    # r = (102.5 - 100.5) / (1.0 * 1.0) = 2.0
    assert abs(row["r_multiple"] - 2.0) < 1e-9


def test_fill_and_sl_hit_yields_negative_r():
    """STOP fills on breakout, then SL hit downward."""
    n = 80
    s = [0.0] * n
    for i in range(10, 60):
        s[i] = 0.01 * ((i % 3) - 1)
    s[68] = 0.5
    s[69] = 0.8
    for i in range(70, 75):
        s[i] = 0.8
    closes = [100.0] * n
    highs = [c + 0.1 for c in closes]
    lows = [c - 0.1 for c in closes]
    # bar 70 fills at 100.5 (STOP)
    highs[70] = 100.6
    closes[70] = 100.55
    # bar 71: drops to SL = 100.5 - 1.0*1.0 = 99.5
    lows[71] = 99.4
    closes[71] = 99.5
    highs[71] = 100.55
    bars = _make_bars(closes, highs=highs, lows=lows, extras={"ols_slope_30": s})
    setups = detect_setups(bars, "OLS_SLOPE_STRONG")
    assert len(setups) >= 1
    cfg = BacktestConfig(tp_atr_mult=2.0, sl_atr_mult=1.0,
                         session_end_hour_utc=23, friction_r=0.0)
    trades = run_backtest(setups, bars, "OLS_SLOPE_STRONG", cfg, "TEST")
    assert len(trades) == 1
    row = trades.row(0, named=True)
    assert row["exit_reason"] == "SL"
    assert abs(row["r_multiple"] - (-1.0)) < 1e-9
