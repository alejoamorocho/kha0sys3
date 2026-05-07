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


def _signal_long_db_raw():
    return Signal(
        symbol="XAUUSD", strategy="double_bottom", side="long",
        setup_ts=datetime(2024, 1, 5),
        entry_type="stop", entry_price=2050.0,
        valid_until=datetime(2024, 2, 5),
        stop=0.0, tp1=None, tp2=None,
        indicator_anchors={"L1": 2000.0, "L2": 2010.0, "neckline": 2040.0,
                           "altura_patron": 30.0, "sma18": 2025.0,
                           "atr14": 15.0, "consol_low": 2042.0},
    )


def test_doc_exit_manager_double_bottom_long():
    s = DocExitManager(strategy="double_bottom").attach_levels(_signal_long_db_raw())
    # Doc DB: stop = consol_low; tp1 = neckline + altura_patron (fib100); tp2 = neckline + altura*1.618
    assert s.stop == pytest.approx(2042.0)
    assert s.tp1 == pytest.approx(2040.0 + 30.0)
    assert s.tp2 == pytest.approx(2040.0 + 30.0 * 1.618)


def test_indicator_exit_manager_double_bottom_long():
    s = IndicatorExitManager(strategy="double_bottom").attach_levels(_signal_long_db_raw())
    # Indicator DB: stop = L2 - 0.25*altura; tp1 = neckline + altura; tp2 = neckline + 1.618*altura
    assert s.stop == pytest.approx(2010.0 - 0.25 * 30.0)
    assert s.tp1 == pytest.approx(2040.0 + 30.0)
    assert s.tp2 == pytest.approx(2040.0 + 30.0 * 1.618)


def _signal_long_perdices_raw():
    return Signal(
        symbol="XAUUSD", strategy="perdices_fib", side="long",
        setup_ts=datetime(2024, 1, 5, 14),
        entry_type="market", entry_price=2030.0,
        valid_until=datetime(2024, 1, 5, 18),
        stop=0.0, tp1=None, tp2=None,
        indicator_anchors={"swing_high": 2050.0, "swing_low": 2000.0,
                           "fib_382": 2030.9, "fib_50": 2025.0,
                           "fib_127": 2063.6, "fib_1618": 2080.9,
                           "rsi": 38.0, "atr14": 5.0},
    )


def test_doc_exit_manager_perdices_long():
    s = DocExitManager(strategy="perdices_fib").attach_levels(_signal_long_perdices_raw())
    # Doc Perdices: stop = swing_low - 2pip ~= swing_low - 0.2 (oro), tp1 = swing_high
    assert s.stop == pytest.approx(1999.8, abs=0.01)
    assert s.tp1 == pytest.approx(2050.0)


def test_indicator_exit_manager_perdices_long():
    s = IndicatorExitManager(strategy="perdices_fib").attach_levels(_signal_long_perdices_raw())
    # Indicator Perdices: stop = swing_low - 2 pips, tp1 = swing_high, tp2 = fib_1618
    assert s.stop == pytest.approx(1999.8, abs=0.01)
    assert s.tp1 == pytest.approx(2050.0)
    assert s.tp2 == pytest.approx(2080.9)
