import numpy as np
import polars as pl
import pytest

from src.engine.orb_optuna_refine import build_objective, OptunaConfig


class _FakeTrial:
    def __init__(self, params):
        self.params = params

    def suggest_float(self, name, low, high, **kw):
        return self.params[name]


def test_objective_returns_pf_with_rr_constraint(monkeypatch):
    """If params produce trades where wins > losses, objective > 1."""
    # Need >= 30 trades to avoid 100% ruin_pct penalty in mc_ruin
    fake_trades = pl.DataFrame({"realized_r": [1.0] * 40 + [-0.5] * 10})

    def fake_simulate(*args, **kw):
        return fake_trades

    monkeypatch.setattr(
        "src.engine.orb_optuna_refine._simulate_with_params",
        fake_simulate,
    )

    slot = {
        "symbol": "EURUSD", "magic_time": "07:00", "or_duration_min": 60,
        "pattern_id": "X", "direction": "LONG", "combo_id": "c1",
    }
    triggers = pl.DataFrame()
    m1 = {"times": np.array([]), "highs": np.array([]), "lows": np.array([]), "closes": np.array([])}
    obj = build_objective(slot, triggers, m1, span_days=365, cfg=OptunaConfig())
    trial = _FakeTrial({
        "sl_atr_mult": 0.5, "rr": 2.0, "entry_offset_atr": 0.0,
        "or_atr_ratio_min": 0.0, "or_atr_ratio_max": 1.5,
    })
    score = obj(trial)
    assert score > 1.0
