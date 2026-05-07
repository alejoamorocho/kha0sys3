from datetime import datetime, timedelta

import pytest

from src.strategies_external.common.metrics import evaluate
from src.strategies_external.common.trade import Trade


def _make(pnl_R: float, ts: datetime, R: float = 10.0) -> Trade:
    return Trade(
        symbol="SP500", strategy="oops", exit_mode="doc", side="long",
        entry_ts=ts, entry=100.0, stop=99.0, tp1=None, tp2=None,
        exit_ts=ts + timedelta(hours=1), exit=100.0 + pnl_R,
        exit_reason="tp1" if pnl_R > 0 else "stop",
        R=R, pnl_R=pnl_R, pnl_pct=pnl_R * 0.005, bars_in_trade=4,
    )


def test_evaluate_empty_returns_zeros():
    m = evaluate([])
    assert m["n_trades"] == 0
    assert m["win_rate"] == 0.0
    assert m["profit_factor"] == 0.0
    assert m["expectancy_R"] == 0.0


def test_evaluate_simple_2_wins_1_loss():
    base = datetime(2024, 1, 1)
    trades = [
        _make(2.0, base),
        _make(2.0, base + timedelta(days=1)),
        _make(-1.0, base + timedelta(days=2)),
    ]
    m = evaluate(trades)
    assert m["n_trades"] == 3
    assert m["win_rate"] == pytest.approx(2 / 3)
    assert m["profit_factor"] == pytest.approx(4.0)  # 4 / 1
    assert m["expectancy_R"] == pytest.approx(1.0)   # (4-1)/3 = 1


def test_evaluate_max_dd_R():
    base = datetime(2024, 1, 1)
    trades = [
        _make(2.0, base),
        _make(-1.0, base + timedelta(days=1)),
        _make(-1.0, base + timedelta(days=2)),
        _make(-1.0, base + timedelta(days=3)),  # equity: 2, 1, 0, -1 -> DD = 3R
        _make(3.0, base + timedelta(days=4)),
    ]
    m = evaluate(trades)
    assert m["max_dd_R"] == pytest.approx(3.0)


def test_evaluate_sharpe_when_zero_std():
    base = datetime(2024, 1, 1)
    trades = [_make(1.0, base + timedelta(days=i)) for i in range(5)]
    m = evaluate(trades)
    # std = 0 -> sharpe convention: 0
    assert m["sharpe"] == 0.0
