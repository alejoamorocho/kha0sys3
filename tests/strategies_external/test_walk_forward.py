from datetime import datetime, timedelta

import pytest

from src.strategies_external.common.trade import Trade
from src.strategies_external.common.walk_forward import walk_forward_split


def _trade(day: int, pnl_R: float) -> Trade:
    base = datetime(2024, 1, 1)
    return Trade(
        symbol="SP500", strategy="oops", exit_mode="doc", side="long",
        entry_ts=base + timedelta(days=day), entry=100.0, stop=99.0,
        tp1=None, tp2=None,
        exit_ts=base + timedelta(days=day, hours=1), exit=100.0 + pnl_R,
        exit_reason="tp1" if pnl_R > 0 else "stop",
        R=10.0, pnl_R=pnl_R, pnl_pct=pnl_R * 0.005, bars_in_trade=4,
    )


def test_walk_forward_5_windows_70_30():
    trades = [_trade(i, (1.0 if i % 2 == 0 else -1.0)) for i in range(100)]
    windows = walk_forward_split(trades, n_windows=5, is_pct=0.7)
    assert len(windows) == 5
    for w in windows:
        is_, oos = w
        # cada ventana = 20 trades; IS=14, OOS=6
        assert len(is_) == 14
        assert len(oos) == 6
    # Las ventanas no se solapan
    all_is = [t.entry_ts for w in windows for t in w[0]]
    assert len(all_is) == len(set(all_is))


def test_walk_forward_too_few_trades():
    trades = [_trade(i, 1.0) for i in range(3)]
    with pytest.raises(ValueError, match="too few trades"):
        walk_forward_split(trades, n_windows=5, is_pct=0.7)
