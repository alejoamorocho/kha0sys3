# tests/strategies_external/test_trade.py
from datetime import datetime

import pytest

from src.strategies_external.common.trade import Trade


def test_trade_minimal():
    t = Trade(
        symbol="SP500", strategy="oops", exit_mode="doc", side="long",
        entry_ts=datetime(2024, 1, 5, 9), entry=4500.0, stop=4490.0,
        tp1=4520.0, tp2=None,
        exit_ts=datetime(2024, 1, 5, 16), exit=4520.0,
        exit_reason="tp1", R=10.0, pnl_R=2.0, pnl_pct=0.01, bars_in_trade=420,
    )
    assert t.pnl_R == 2.0
    assert t.exit_reason == "tp1"


def test_trade_is_frozen():
    t = Trade(
        symbol="SP500", strategy="oops", exit_mode="doc", side="long",
        entry_ts=datetime(2024, 1, 5, 9), entry=4500.0, stop=4490.0,
        tp1=None, tp2=None,
        exit_ts=datetime(2024, 1, 5, 16), exit=4500.0,
        exit_reason="eod", R=10.0, pnl_R=0.0, pnl_pct=0.0, bars_in_trade=420,
    )
    with pytest.raises((AttributeError, TypeError)):
        t.pnl_R = 5.0
