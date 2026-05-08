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
    # Plan 2.5: hard stop = sma18 - 3*atr14; exit_on_two_closes_against = sma18
    assert s.stop == pytest.approx(2025.0 - 3 * 15.0)   # 1980.0
    assert s.tp1 is None
    assert s.tp2 is None
    assert s.exit_on_two_closes_against == pytest.approx(2025.0)
    assert s.exit_close_count_required == 2


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
    # Plan 2.5: stop = swing_low - 0.2, tp1 = swing_high, no fixed timestop,
    # exit_after_bars_if_below_R = (240, 1.0) (conditional)
    assert s.stop == pytest.approx(1999.8, abs=0.01)
    assert s.tp1 == pytest.approx(2050.0)
    assert s.timestop_bars is None
    assert s.exit_after_bars_if_below_R == (240, 1.0)


def test_indicator_exit_manager_perdices_long():
    s = IndicatorExitManager(strategy="perdices_fib").attach_levels(_signal_long_perdices_raw())
    # Indicator Perdices: stop = swing_low - 2 pips, tp1 = swing_high, tp2 = fib_1618
    assert s.stop == pytest.approx(1999.8, abs=0.01)
    assert s.tp1 == pytest.approx(2050.0)
    assert s.tp2 == pytest.approx(2080.9)


def _signal_long_cot1_raw():
    return Signal(
        symbol="XAUUSD", strategy="cot1", side="long",
        setup_ts=datetime(2024, 1, 5),
        entry_type="stop", entry_price=2050.0,
        valid_until=datetime(2024, 1, 10),
        stop=0.0, tp1=None, tp2=None,
        timestop_bars=None,   # Plan 2.5: no timestop_bars
        indicator_anchors={"atr14": 15.0, "cot_index": 85.0,
                           "season_5d": 0.012,
                           "swing_high_5d": 2055.0, "swing_low_5d": 2030.0},
    )


def test_doc_exit_manager_cot1_long():
    s = DocExitManager(strategy="cot1").attach_levels(_signal_long_cot1_raw())
    # Plan 2.5: stop = swing_low_5d - 0.5*atr; tp1 = entry + 1.5R; tp2 = entry + 3R; no timestop
    assert s.stop == pytest.approx(2030.0 - 0.5 * 15.0)
    R = 2050.0 - (2030.0 - 0.5 * 15.0)
    assert s.tp1 == pytest.approx(2050.0 + 1.5 * R, abs=0.5)
    assert s.tp2 == pytest.approx(2050.0 + 3.0 * R, abs=0.5)
    assert s.timestop_bars is None


def test_indicator_exit_manager_cot1_long():
    s = IndicatorExitManager(strategy="cot1").attach_levels(_signal_long_cot1_raw())
    # Indicator COT1: stop = swing_low_5d - 0.5*atr; tp1/tp2 inherit doc style; no timestop
    assert s.stop == pytest.approx(2030.0 - 0.5 * 15.0)
    assert s.tp1 is not None
    assert s.tp2 is not None
    assert s.timestop_bars is None


# ── FADE exit manager tests ───────────────────────────────────────────────────


def _signal_fade_up_raw() -> Signal:
    """FADE_UP: short signal at OR_HIGH with or_width=10."""
    return Signal(
        symbol="EURUSD", strategy="fade", side="short",
        setup_ts=datetime(2024, 1, 2, 8, 0),
        entry_type="limit", entry_price=110.0,
        valid_until=datetime(2024, 1, 2, 14, 0),
        stop=0.0, tp1=None, tp2=None,
        indicator_anchors={
            "tp_mult": 0.5, "sl_mult": 2.5,
            "or_high": 110.0, "or_low": 100.0, "or_width": 10.0,
            "magic_time": 420.0, "duration": 60.0,
        },
    )


def _signal_fade_down_raw() -> Signal:
    """FADE_DOWN: long signal at OR_LOW with or_width=10."""
    return Signal(
        symbol="EURUSD", strategy="fade", side="long",
        setup_ts=datetime(2024, 1, 2, 8, 0),
        entry_type="limit", entry_price=100.0,
        valid_until=datetime(2024, 1, 2, 14, 0),
        stop=0.0, tp1=None, tp2=None,
        indicator_anchors={
            "tp_mult": 0.75, "sl_mult": 2.5,
            "or_high": 110.0, "or_low": 100.0, "or_width": 10.0,
            "magic_time": 420.0, "duration": 60.0,
        },
    )


def test_doc_exit_manager_fade_up_short():
    """DocExitManager FADE_UP: stop above entry, TP below entry."""
    s = DocExitManager(strategy="fade").attach_levels(_signal_fade_up_raw())
    # entry=110, or_width=10, sl_mult=2.5, tp_mult=0.5
    assert s.stop == pytest.approx(110.0 + 2.5 * 10.0)   # 135.0
    assert s.tp1 == pytest.approx(110.0 - 0.5 * 10.0)    # 105.0
    assert s.tp2 is None


def test_doc_exit_manager_fade_down_long():
    """DocExitManager FADE_DOWN: stop below entry, TP above entry."""
    s = DocExitManager(strategy="fade").attach_levels(_signal_fade_down_raw())
    # entry=100, or_width=10, sl_mult=2.5, tp_mult=0.75
    assert s.stop == pytest.approx(100.0 - 2.5 * 10.0)   # 75.0
    assert s.tp1 == pytest.approx(100.0 + 0.75 * 10.0)   # 107.5
    assert s.tp2 is None


def test_indicator_exit_manager_fade_up_short():
    """IndicatorExitManager FADE_UP: identical to doc for V1."""
    s = IndicatorExitManager(strategy="fade").attach_levels(_signal_fade_up_raw())
    assert s.stop == pytest.approx(110.0 + 2.5 * 10.0)
    assert s.tp1 == pytest.approx(110.0 - 0.5 * 10.0)
    assert s.tp2 is None


def test_indicator_exit_manager_fade_down_long():
    """IndicatorExitManager FADE_DOWN: identical to doc for V1."""
    s = IndicatorExitManager(strategy="fade").attach_levels(_signal_fade_down_raw())
    assert s.stop == pytest.approx(100.0 - 2.5 * 10.0)
    assert s.tp1 == pytest.approx(100.0 + 0.75 * 10.0)
    assert s.tp2 is None


def test_doc_exit_manager_fade_unknown_raises():
    """DocExitManager rejects unknown strategy."""
    with pytest.raises(ValueError, match="unknown strategy"):
        DocExitManager(strategy="unknown_xyz")
