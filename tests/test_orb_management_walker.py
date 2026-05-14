from datetime import datetime, timedelta

import numpy as np
import pytest

from src.application.orb_management_walker import simulate_trade


def _m1(start, highs, lows):
    n = len(highs)
    times = [start + timedelta(minutes=i) for i in range(n)]
    closes = [(h + l) / 2 for h, l in zip(highs, lows)]
    return {
        "times": np.array(times, dtype="object"),
        "highs": np.asarray(highs, dtype=float),
        "lows": np.asarray(lows, dtype=float),
        "closes": np.asarray(closes, dtype=float),
    }


def test_long_tp_hit_returns_positive_r():
    fill_ts = datetime(2026, 1, 1, 8, 0)
    out = simulate_trade(
        fill_ts=fill_ts, entry=1.10, direction="LONG",
        tp=1.12, sl=1.09, max_hold_min=60,
        m1=_m1(datetime(2026, 1, 1, 8, 1),
               highs=[1.105, 1.115, 1.125, 1.11],
               lows= [1.095, 1.100, 1.115, 1.105]),
        risk_per_r=0.01,
        friction_r=0.3,
    )
    assert out["exit_reason"] == "TP"
    assert out["realized_r"] == pytest.approx(1.7)


def test_long_sl_first_when_tp_and_sl_both_in_bar():
    fill_ts = datetime(2026, 1, 1, 8, 0)
    out = simulate_trade(
        fill_ts=fill_ts, entry=1.10, direction="LONG",
        tp=1.11, sl=1.09, max_hold_min=60,
        m1=_m1(datetime(2026, 1, 1, 8, 1),
               highs=[1.115, 1.10],
               lows= [1.085, 1.095]),
        risk_per_r=0.01, friction_r=0.3,
    )
    assert out["exit_reason"] == "SL"
    assert out["realized_r"] == pytest.approx(-1.3)


def test_max_hold_timeout_exits_at_last_close():
    fill_ts = datetime(2026, 1, 1, 8, 0)
    out = simulate_trade(
        fill_ts=fill_ts, entry=1.10, direction="LONG",
        tp=1.20, sl=1.00, max_hold_min=3,
        m1=_m1(datetime(2026, 1, 1, 8, 1),
               highs=[1.11, 1.12, 1.11],
               lows= [1.09, 1.10, 1.10]),
        risk_per_r=0.01, friction_r=0.3,
    )
    assert out["exit_reason"] == "MAX_HOLD"
    assert out["realized_r"] == pytest.approx(0.2)


def test_short_tp_hit():
    fill_ts = datetime(2026, 1, 1, 8, 0)
    out = simulate_trade(
        fill_ts=fill_ts, entry=1.10, direction="SHORT",
        tp=1.08, sl=1.11, max_hold_min=60,
        m1=_m1(datetime(2026, 1, 1, 8, 1),
               highs=[1.105, 1.105, 1.100],
               lows= [1.095, 1.085, 1.080]),
        risk_per_r=0.01, friction_r=0.3,
    )
    assert out["exit_reason"] == "TP"
    assert out["realized_r"] == pytest.approx(1.7)


def test_no_bars_after_fill_returns_zero_with_no_bars_reason():
    fill_ts = datetime(2026, 1, 1, 8, 0)
    out = simulate_trade(
        fill_ts=fill_ts, entry=1.10, direction="LONG",
        tp=1.12, sl=1.09, max_hold_min=60,
        m1=_m1(datetime(2026, 1, 1, 7, 0), highs=[1.10], lows=[1.10]),
        risk_per_r=0.01, friction_r=0.3,
    )
    assert out["exit_reason"] == "NO_BARS"
    assert out["realized_r"] == 0.0
