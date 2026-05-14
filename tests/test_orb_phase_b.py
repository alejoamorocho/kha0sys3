import polars as pl
import pytest

from src.engine.orb_management_grid import (
    aggregate_trades,
    PhaseBConfig,
    ENTRY_MODES,
    SL_GRID,
    TP_RR_GRID,
)


def test_entry_modes_are_five():
    assert ENTRY_MODES == [
        ("MARKET", 0.0),
        ("STOP_RETEST", 0.25),
        ("STOP_RETEST", 0.5),
        ("LIMIT_PULLBACK", -0.25),
        ("LIMIT_PULLBACK", -0.5),
    ]


def test_grid_constants():
    assert SL_GRID == [0.3, 0.5, 0.7, 1.0]
    assert TP_RR_GRID == [1.0, 1.5, 2.0, 3.0]


def test_aggregate_trades_computes_pf_and_wr():
    trades = pl.DataFrame({
        "realized_r": [1.5, -1.0, 2.0, -1.0, 1.0],
        "exit_reason": ["TP", "SL", "TP", "SL", "TP"],
    })
    out = aggregate_trades(trades, span_days=365)
    assert out["trades"] == 5
    assert out["win_rate"] == pytest.approx(0.6)
    assert out["pf"] == pytest.approx(4.5 / 2.0)
    assert out["expectancy_r"] == pytest.approx(0.5)
    assert out["trades_per_year"] == pytest.approx(5.0, rel=1e-3)


def test_phase_b_filter_drops_low_pf():
    cfg = PhaseBConfig()
    metrics = {
        "trades": 100, "trades_per_year": 100, "win_rate": 0.55,
        "pf": 1.1,
        "expectancy_r": 0.05, "max_dd_r": 5.0, "sharpe_annualized": 1.0,
        "rr": 1.0,
    }
    assert not cfg.passes(metrics)


def test_phase_b_filter_passes_strong():
    cfg = PhaseBConfig()
    metrics = {
        "trades": 100, "trades_per_year": 100, "win_rate": 0.6,
        "pf": 1.5, "expectancy_r": 0.2, "max_dd_r": 5.0,
        "sharpe_annualized": 1.5, "rr": 2.0,
    }
    assert cfg.passes(metrics)
