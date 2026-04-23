import polars as pl
import pytest
from src.engine.indicator_validation import (
    compute_metrics, walk_forward_wr, monte_carlo_ruin, decay_slope_ratio,
    MetricsResult,
)


def _trade_df(r_list, start_day=1):
    import datetime as dt
    times = [dt.datetime(2024, 1, start_day) + dt.timedelta(days=i) for i in range(len(r_list))]
    return pl.DataFrame({"time": times, "r_multiple": r_list})


def test_compute_metrics_basic():
    trades = _trade_df([1, 1, 1, -1, 1])  # 4 wins, 1 loss
    m = compute_metrics(trades)
    assert m.n_trades == 5
    assert m.wr == pytest.approx(0.8)
    assert m.expectancy_r == pytest.approx(0.6)
    assert m.profit_factor == pytest.approx(4.0)


def test_walk_forward_computes_oos_ratio():
    # IS segment (first 60%): WR 80%, OOS (last 40%): WR 80%
    trades = _trade_df([1]*8 + [-1]*2 + [1]*4 + [-1]*1, start_day=1)
    ratio = walk_forward_wr(trades, is_months=1, oos_months=1)
    assert ratio >= 0.85


def test_monte_carlo_ruin_zero_for_winning_system():
    trades = _trade_df([1.0]*50 + [-1.0]*10)  # strongly positive
    ruin = monte_carlo_ruin(trades, risk_pct=0.01, initial_balance=10000,
                            n_sims=500, n_steps=100, seed=42)
    assert ruin < 0.01


def test_decay_slope_ratio_flags_degrading_system():
    # Increasing R through time — should NOT degrade
    import datetime as dt
    times = [dt.datetime(2024, 1, 1) + dt.timedelta(days=i) for i in range(100)]
    r = [0.5 + i * 0.01 for i in range(100)]
    trades = pl.DataFrame({"time": times, "r_multiple": r})
    ratio = decay_slope_ratio(trades, last_months=6)
    assert ratio >= 0.7
