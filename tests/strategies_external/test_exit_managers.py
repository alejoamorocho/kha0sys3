from datetime import datetime

import pytest

from src.strategies_external.common.signal import Signal
from src.strategies_external.exit_managers import (
    ATRExitManager,
    DocExitManager,
    IndicatorExitManager,
)


def _signal_long_oops_raw() -> Signal:
    """Signal OOPS long sin stop/tp todavía (los pone el ExitManager)."""
    return Signal(
        symbol="SP500", strategy="oops", side="long",
        setup_ts=datetime(2024, 1, 5),
        entry_type="stop", entry_price=4500.0,
        valid_until=datetime(2024, 1, 5, 23, 59),
        stop=0.0, tp1=None, tp2=None,
        indicator_anchors={"prev_high": 4540.0, "prev_low": 4500.0,
                           "prev_range": 40.0, "today_open": 4480.0,
                           "atr14": 50.0, "today_low": 4470.0},
    )


def test_doc_exit_manager_oops_long():
    raw = _signal_long_oops_raw()
    mgr = DocExitManager(strategy="oops")
    s = mgr.attach_levels(raw)
    # Doc OOPS long: stop = today_low, tp = entry + 2R, eod fallback
    assert s.stop == pytest.approx(4470.0)
    R = 4500.0 - 4470.0
    assert s.tp1 == pytest.approx(4500.0 + 2 * R)
    assert s.timestop_bars is None  # eod handled by backtester via valid_until


def test_atr_exit_manager_oops_long():
    raw = _signal_long_oops_raw()
    mgr = ATRExitManager(sl_mult=1.5, tp1_mult=1.5, tp2_mult=3.0)
    s = mgr.attach_levels(raw)
    atr = 50.0
    assert s.stop == pytest.approx(4500.0 - 1.5 * atr)
    assert s.tp1 == pytest.approx(4500.0 + 1.5 * atr)
    assert s.tp2 == pytest.approx(4500.0 + 3.0 * atr)


def test_indicator_exit_manager_oops_long():
    raw = _signal_long_oops_raw()
    mgr = IndicatorExitManager(strategy="oops")
    s = mgr.attach_levels(raw)
    # Indicator OOPS long: stop = today_low (mismo doc), tp1 = mid prev_range, tp2 = prev_close + prev_range
    assert s.stop == pytest.approx(4470.0)
    # mid del rango previo respecto al precio de entrada: prev_low + prev_range/2 = 4520
    assert s.tp1 == pytest.approx(4520.0)
    # prev_high + prev_range = 4540 + 40 = 4580
    assert s.tp2 == pytest.approx(4580.0)


def _signal_short_oops_raw() -> Signal:
    """Signal OOPS short sin stop/tp todavía."""
    return Signal(
        symbol="SP500", strategy="oops", side="short",
        setup_ts=datetime(2024, 1, 5),
        entry_type="stop", entry_price=4540.0,
        valid_until=datetime(2024, 1, 5, 23, 59),
        stop=0.0, tp1=None, tp2=None,
        indicator_anchors={"prev_high": 4540.0, "prev_low": 4500.0,
                           "prev_range": 40.0, "today_open": 4560.0,
                           "atr14": 50.0, "today_high": 4570.0},
    )


def test_doc_exit_manager_oops_short():
    raw = _signal_short_oops_raw()
    mgr = DocExitManager(strategy="oops")
    s = mgr.attach_levels(raw)
    # Doc OOPS short: stop = today_high, tp1 = entry - 2R
    assert s.stop == pytest.approx(4570.0)
    R = 4570.0 - 4540.0
    assert s.tp1 == pytest.approx(4540.0 - 2 * R)


def test_indicator_exit_manager_oops_short():
    raw = _signal_short_oops_raw()
    mgr = IndicatorExitManager(strategy="oops")
    s = mgr.attach_levels(raw)
    # Indicator OOPS short: stop=today_high, tp1=prev_high - prev_range/2, tp2=prev_low - prev_range
    assert s.stop == pytest.approx(4570.0)
    assert s.tp1 == pytest.approx(4540.0 - 40.0 / 2.0)  # 4520
    assert s.tp2 == pytest.approx(4500.0 - 40.0)  # 4460


def test_atr_exit_manager_tp2_none_returns_none():
    """Si tp2_mult es None, tp2 sigue None (no produce 0.0 ni False-equivalente)."""
    raw = _signal_long_oops_raw()
    mgr = ATRExitManager(sl_mult=1.0, tp1_mult=1.0, tp2_mult=None)
    s = mgr.attach_levels(raw)
    assert s.tp2 is None


def test_exit_manager_unknown_strategy_raises():
    raw = _signal_long_oops_raw()
    with pytest.raises(ValueError, match="unknown strategy"):
        DocExitManager(strategy="not_a_strategy").attach_levels(raw)
