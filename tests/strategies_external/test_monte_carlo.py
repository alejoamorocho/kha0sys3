from datetime import datetime, timedelta

import pytest

from src.strategies_external.common.monte_carlo import monte_carlo_bootstrap
from src.strategies_external.common.trade import Trade


def _make(pnl_R: float, day: int) -> Trade:
    base = datetime(2024, 1, 1)
    return Trade(
        symbol="SP500", strategy="oops", exit_mode="doc", side="long",
        entry_ts=base + timedelta(days=day), entry=100.0, stop=99.0,
        tp1=None, tp2=None,
        exit_ts=base + timedelta(days=day, hours=1), exit=100.0 + pnl_R,
        exit_reason="tp1" if pnl_R > 0 else "stop",
        R=10.0, pnl_R=pnl_R, pnl_pct=pnl_R * 0.005, bars_in_trade=4,
    )


def test_monte_carlo_winning_system_low_ruin():
    """Sistema con expectancy positiva -> prob_ruin baja."""
    trades = [_make(2.0 if i % 3 != 0 else -1.0, i) for i in range(60)]
    res = monte_carlo_bootstrap(trades, n_simulations=2000, ruin_threshold_R=-15.0, seed=42)
    assert res["prob_ruin"] < 0.05
    assert res["dd_q50_R"] < res["dd_q95_R"]


def test_monte_carlo_losing_system_high_ruin():
    """Sistema perdedor -> prob_ruin alta."""
    trades = [_make(-1.0 if i % 3 != 0 else 0.5, i) for i in range(60)]
    res = monte_carlo_bootstrap(trades, n_simulations=2000, ruin_threshold_R=-15.0, seed=42)
    assert res["prob_ruin"] > 0.5


def test_monte_carlo_empty_trades():
    with pytest.raises(ValueError, match="empty trade list"):
        monte_carlo_bootstrap([], n_simulations=100, ruin_threshold_R=-15.0)
