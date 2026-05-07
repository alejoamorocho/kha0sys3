# tests/strategies_external/test_exit_managers_extensions.py
from datetime import datetime

import pytest

from src.strategies_external.common.signal import Signal
from src.strategies_external.exit_managers import (
    DocExitManager, IndicatorExitManager,
)


def _signal_long_sma18_raw() -> Signal:
    return Signal(
        symbol="XAUUSD", strategy="sma18", side="long",
        setup_ts=datetime(2024, 1, 5),
        entry_type="stop", entry_price=2050.0,
        valid_until=datetime(2024, 1, 5, 23, 59),
        stop=0.0, tp1=None, tp2=None,
        indicator_anchors={"sma18": 2025.0, "atr14": 15.0,
                           "high_p1": 2048.0, "high_p2": 2045.0,
                           "low_p1": 2040.0, "low_p2": 2038.0},
    )


def test_doc_exit_manager_sma18_long():
    raw = _signal_long_sma18_raw()
    s = DocExitManager(strategy="sma18").attach_levels(raw)
    # Doc SMA-18: stop = sma18 (señal contraria); no fixed TP — the backtester
    # handles "exit on 2 closes against SMA" via timestop or signal_inverso later.
    # For now: stop=sma18, tp1=None, tp2=None.
    assert s.stop == pytest.approx(2025.0)
    assert s.tp1 is None
    assert s.tp2 is None


def test_indicator_exit_manager_sma18_long():
    raw = _signal_long_sma18_raw()
    s = IndicatorExitManager(strategy="sma18").attach_levels(raw)
    # Indicator SMA-18: stop = sma18 - 0.5*atr; tp1 = sma18 + 2*atr; tp2 = sma18 + 4*atr
    assert s.stop == pytest.approx(2025.0 - 0.5 * 15.0)
    assert s.tp1 == pytest.approx(2025.0 + 2.0 * 15.0)
    assert s.tp2 == pytest.approx(2025.0 + 4.0 * 15.0)
