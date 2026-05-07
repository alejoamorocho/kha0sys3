# tests/strategies_external/test_signal.py
from datetime import datetime

import pytest

from src.strategies_external.common.signal import Signal


def test_signal_minimal_long():
    s = Signal(
        symbol="SP500",
        strategy="oops",
        side="long",
        setup_ts=datetime(2024, 1, 5),
        entry_type="stop",
        entry_price=4500.0,
        valid_until=datetime(2024, 1, 5, 23, 59),
        stop=4490.0,
        tp1=4520.0,
        tp2=None,
    )
    assert s.side == "long"
    assert s.tp1_size_pct == 0.5  # default
    assert s.indicator_anchors == {}


def test_signal_with_anchors():
    s = Signal(
        symbol="XAUUSD",
        strategy="sma18",
        side="long",
        setup_ts=datetime(2024, 1, 5),
        entry_type="stop",
        entry_price=2050.0,
        valid_until=datetime(2024, 1, 5, 23, 59),
        stop=2030.0,
        tp1=None,
        tp2=None,
        timestop_bars=20,
        indicator_anchors={"sma18": 2025.0, "atr14": 15.0},
    )
    assert s.indicator_anchors["sma18"] == 2025.0
    assert s.timestop_bars == 20


def test_signal_is_frozen():
    s = Signal(
        symbol="SP500", strategy="oops", side="long",
        setup_ts=datetime(2024, 1, 5), entry_type="stop", entry_price=4500.0,
        valid_until=datetime(2024, 1, 5, 23, 59), stop=4490.0, tp1=None, tp2=None,
    )
    with pytest.raises((AttributeError, TypeError)):
        s.entry_price = 5000.0  # frozen
