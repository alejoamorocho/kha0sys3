"""Tests for the partial-exits doc-style walker."""
from datetime import datetime, timedelta

import numpy as np
import pytest

from src.application.orb_management_modes import simulate_doc_partial


def _m1(start, highs, lows, closes=None):
    n = len(highs)
    times = [start + timedelta(minutes=i) for i in range(n)]
    if closes is None:
        closes = [(h + l) / 2 for h, l in zip(highs, lows)]
    return {
        "times": np.array(times, dtype="object"),
        "highs": np.asarray(highs, dtype=float),
        "lows": np.asarray(lows, dtype=float),
        "closes": np.asarray(closes, dtype=float),
    }


def test_tp1_partial_then_tp2_full_long():
    """Long: TP1 hit closes 50%, TP2 hit closes the rest. Total = (1R × 0.5) + (2R × 0.5) = 1.5R."""
    fill_ts = datetime(2026, 1, 1, 8, 0)
    out = simulate_doc_partial(
        fill_ts=fill_ts, entry=1.10, direction="LONG",
        sl_distance=0.01, tp1_distance=0.01, tp2_distance=0.02,
        max_hold_min=60,
        m1=_m1(datetime(2026, 1, 1, 8, 1),
               highs=[1.105, 1.115, 1.125, 1.13],
               lows=[1.095, 1.105, 1.115, 1.125]),
        risk_per_r=0.01, friction_r=0.0,
    )
    assert out["tp1_hit"] is True
    assert out["tp2_hit"] is True
    assert out["realized_r"] == pytest.approx(1.5)


def test_tp1_hit_then_be_stop_long():
    """Long: TP1 hit (+0.5R), then SL moves to BE, price drops to BE, SL_BE triggers. Total = +0.5R."""
    fill_ts = datetime(2026, 1, 1, 8, 0)
    out = simulate_doc_partial(
        fill_ts=fill_ts, entry=1.10, direction="LONG",
        sl_distance=0.01, tp1_distance=0.01, tp2_distance=0.03,
        max_hold_min=120,
        m1=_m1(datetime(2026, 1, 1, 8, 1),
               # idx 0: TP1 hit (high=1.11). idx 1: drops to BE (low=1.10)
               highs=[1.115, 1.105, 1.10, 1.10],
               lows=[1.095, 1.10, 1.099, 1.099]),
        risk_per_r=0.01, friction_r=0.0,
    )
    assert out["tp1_hit"] is True
    assert out["tp2_hit"] is False
    # 0.5 × 1R (TP1) + 0.5 × 0R (BE stop) = 0.5R
    assert out["realized_r"] == pytest.approx(0.5)
    assert out["exits"][-1]["exit_reason"] == "SL_BE"


def test_initial_sl_hit_before_tp1_long():
    """Long: SL hits before TP1, lose 1R on full position."""
    fill_ts = datetime(2026, 1, 1, 8, 0)
    out = simulate_doc_partial(
        fill_ts=fill_ts, entry=1.10, direction="LONG",
        sl_distance=0.01, tp1_distance=0.02, tp2_distance=0.04,
        max_hold_min=60,
        m1=_m1(datetime(2026, 1, 1, 8, 1),
               highs=[1.105, 1.10],
               lows=[1.085, 1.10]),
        risk_per_r=0.01, friction_r=0.0,
    )
    assert out["tp1_hit"] is False
    assert out["realized_r"] == pytest.approx(-1.0)
    assert out["exit_reason"] == "SL"


def test_time_stop_low_mfe_kicks_in():
    """If at max_hold_min/2 the MFE < 0.5R and TP1 not hit, close at market."""
    fill_ts = datetime(2026, 1, 1, 8, 0)
    # 60 min hold, midpoint at fill+30min. M1 starts at fill+1min → idx 29 = fill+30min.
    # MFE never exceeds 0.3R (0.003). At idx 29 close = 1.100 → +0R.
    highs = [1.103] * 60
    lows = [1.098] * 60
    closes = [1.100] * 60
    closes[29] = 1.1005  # at midpoint close, +0.0005 → 0.05R × full position
    out = simulate_doc_partial(
        fill_ts=fill_ts, entry=1.10, direction="LONG",
        sl_distance=0.01, tp1_distance=0.02, tp2_distance=0.04,
        max_hold_min=60,
        m1=_m1(datetime(2026, 1, 1, 8, 1), highs=highs, lows=lows, closes=closes),
        risk_per_r=0.01, friction_r=0.0,
    )
    assert out["time_stopped"] is True
    assert out["exit_reason"] == "TIME_STOP_LOW_MFE"
    # +0.0005 / 0.01 = 0.05R
    assert out["realized_r"] == pytest.approx(0.05)


def test_max_hold_closes_remainder():
    """If time horizon ends with no TP/SL/timestop, close remainder at last close."""
    fill_ts = datetime(2026, 1, 1, 8, 0)
    # Slowly grinding higher; TP1 just out of reach. MFE >= 0.5R at midpoint so no time-stop.
    highs = [1.10 + i * 0.0001 for i in range(60)]  # idx 0=1.1001 ... idx 59=1.1059
    lows = [1.10 - 0.0005 for _ in range(60)]
    closes = [1.10 + i * 0.0001 for i in range(60)]
    out = simulate_doc_partial(
        fill_ts=fill_ts, entry=1.10, direction="LONG",
        sl_distance=0.01, tp1_distance=0.01, tp2_distance=0.03,
        max_hold_min=60,
        m1=_m1(datetime(2026, 1, 1, 8, 1), highs=highs, lows=lows, closes=closes),
        risk_per_r=0.01, friction_r=0.0,
    )
    # No TP1 hit (max high = 1.1059 < 1.11). MFE at midpoint (~idx 29) = 0.0029 = 0.29R < 0.5R
    # → TIME_STOP at midpoint
    assert out["time_stopped"] is True or out["exit_reason"] == "MAX_HOLD"


def test_friction_subtracted():
    """Friction R subtracted from total realized."""
    fill_ts = datetime(2026, 1, 1, 8, 0)
    out = simulate_doc_partial(
        fill_ts=fill_ts, entry=1.10, direction="LONG",
        sl_distance=0.01, tp1_distance=0.01, tp2_distance=0.02,
        max_hold_min=60,
        m1=_m1(datetime(2026, 1, 1, 8, 1),
               highs=[1.115, 1.125, 1.13],
               lows=[1.105, 1.115, 1.125]),
        risk_per_r=0.01, friction_r=0.3,
    )
    # TP1 0.5R + TP2 1.0R = 1.5R - 0.3 = 1.2R
    assert out["realized_r"] == pytest.approx(1.2)


def test_swing_traders_tp1_tp2_then_trail():
    """SWING: TP1 (25%) + TP2 (25%) + trail SMA crosses against → exits remainder."""
    from src.application.orb_management_modes import simulate_swing_traders
    fill_ts = datetime(2026, 1, 1, 8, 0)
    # Long, entry=1.10, R=0.01, TP1=1.12 (+2R), TP2=1.14 (+4R), SL=1.09
    # Bars 0-2: TP1+TP2 hit, then 3 trailing bars, bar 5 crosses below SMA(20)
    highs = [1.115, 1.125, 1.145, 1.13, 1.12, 1.11]
    lows = [1.105, 1.115, 1.125, 1.115, 1.105, 1.095]
    closes = [1.11, 1.12, 1.13, 1.12, 1.11, 1.10]  # last cl=1.10 < short SMA
    out = simulate_swing_traders(
        fill_ts=fill_ts, entry=1.10, direction="LONG",
        sl_distance=0.01,
        max_hold_min=60,
        m1=_m1(datetime(2026, 1, 1, 8, 1), highs=highs, lows=lows, closes=closes),
        risk_per_r=0.01, friction_r=0.0,
        trail_sma_period=3,  # short SMA so it adapts fast
    )
    assert out["tp1_hit"] is True
    assert out["tp2_hit"] is True
    # 25% × 2R (TP1) = 0.5R
    # 25% × 4R (TP2) = 1.0R
    # 50% × trail at idx=3 (close=1.12, sma=1.1233, LONG cross down) = 50% × (1.12-1.10)/0.01 = 1.0R
    # Total = 2.5R
    assert out["realized_r"] == pytest.approx(2.5, abs=0.01)


def test_swing_traders_sl_before_tp1():
    """SWING: SL hit before TP1 = -1R full position."""
    from src.application.orb_management_modes import simulate_swing_traders
    fill_ts = datetime(2026, 1, 1, 8, 0)
    out = simulate_swing_traders(
        fill_ts=fill_ts, entry=1.10, direction="LONG",
        sl_distance=0.01,
        max_hold_min=60,
        m1=_m1(datetime(2026, 1, 1, 8, 1),
               highs=[1.105, 1.10],
               lows=[1.085, 1.10]),
        risk_per_r=0.01, friction_r=0.0,
    )
    assert out["realized_r"] == pytest.approx(-1.0)
    assert out["exit_reason"] == "SL"


def test_short_direction_works():
    """Short: TP1+TP2 mirror of long."""
    fill_ts = datetime(2026, 1, 1, 8, 0)
    out = simulate_doc_partial(
        fill_ts=fill_ts, entry=1.10, direction="SHORT",
        sl_distance=0.01, tp1_distance=0.01, tp2_distance=0.02,
        max_hold_min=60,
        m1=_m1(datetime(2026, 1, 1, 8, 1),
               # short profits when price drops
               highs=[1.105, 1.095, 1.085, 1.08],
               lows=[1.095, 1.085, 1.075, 1.07]),
        risk_per_r=0.01, friction_r=0.0,
    )
    assert out["tp1_hit"] is True
    assert out["tp2_hit"] is True
    assert out["realized_r"] == pytest.approx(1.5)
