import numpy as np
import pytest
from datetime import datetime, timedelta

from src.application.orb_edge_metrics import mfe_mae_walk


def _m1(start, highs, lows, closes):
    times = [start + timedelta(minutes=i) for i in range(len(highs))]
    return {
        "times": np.array(times, dtype="object"),
        "highs": np.asarray(highs, dtype=float),
        "lows": np.asarray(lows, dtype=float),
        "closes": np.asarray(closes, dtype=float),
    }


def test_mfe_mae_simple_long_excursion():
    trigger_ts = datetime(2026, 1, 1, 8, 0)
    entry = 1.10
    m1 = _m1(
        start=datetime(2026, 1, 1, 8, 1),
        highs=[1.11, 1.13, 1.12, 1.10],
        lows= [1.09, 1.10, 1.08, 1.07],
        closes=[1.10, 1.12, 1.10, 1.08],
    )
    out = mfe_mae_walk(trigger_ts=trigger_ts, entry=entry, m1=m1, horizon_min=480)
    assert out["mfe_long"] == pytest.approx(0.03)
    assert out["mae_long"] == pytest.approx(0.03)
    assert out["mfe_short"] == pytest.approx(0.03)
    assert out["mae_short"] == pytest.approx(0.03)


def test_mfe_mae_stops_at_horizon():
    trigger_ts = datetime(2026, 1, 1, 8, 0)
    entry = 1.10
    highs = [1.10 + 0.001 * i for i in range(500)]
    lows = [1.10 - 0.001 * i for i in range(500)]
    m1 = _m1(start=datetime(2026, 1, 1, 8, 1), highs=highs, lows=lows, closes=highs)
    out = mfe_mae_walk(trigger_ts=trigger_ts, entry=entry, m1=m1, horizon_min=5)
    assert abs(out["mfe_long"] - 0.004) < 1e-9


def test_mfe_mae_strictly_after_trigger():
    trigger_ts = datetime(2026, 1, 1, 8, 0)
    times = [
        datetime(2026, 1, 1, 7, 59),
        datetime(2026, 1, 1, 8, 0),
        datetime(2026, 1, 1, 8, 1),
    ]
    m1 = {
        "times": np.array(times, dtype="object"),
        "highs": np.array([1.20, 1.50, 1.11]),
        "lows":  np.array([1.05, 1.00, 1.09]),
        "closes": np.array([1.10, 1.10, 1.10]),
    }
    out = mfe_mae_walk(trigger_ts=trigger_ts, entry=1.10, m1=m1, horizon_min=480)
    assert out["mfe_long"] == pytest.approx(0.01)
    assert out["mae_long"] == pytest.approx(0.01)
