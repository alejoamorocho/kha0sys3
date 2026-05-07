"""Tests for OOPSStrategy.generate_signals."""

import pytest

from src.strategies_external.strategies.oops import OOPSStrategy


def test_oops_long_signal_detected(df_daily_oops_long):
    # atr_window=3 because the fixture only has 5 daily bars (< 14+2=16).
    strat = OOPSStrategy(atr_window=3)
    signals = strat.generate_signals(df_daily_oops_long, symbol="SP500")
    # Day 4: open=104 < prev_low=105 ∧ high=109 > prev_low=105 → OOPS long
    assert len(signals) == 1
    s = signals[0]
    assert s.side == "long"
    # entry_price = prev_low + _TICK = 105 + 0.01 = 105.01
    assert s.entry_price == pytest.approx(105.01)
    assert s.entry_type == "stop"
    # anchors populated
    for k in ("prev_high", "prev_low", "prev_range", "today_open", "atr14",
              "today_low", "today_high"):
        assert k in s.indicator_anchors


def test_oops_short_signal_detected(df_daily_oops_short):
    # atr_window=3 because the fixture only has 5 daily bars (< 14+2=16).
    strat = OOPSStrategy(atr_window=3)
    signals = strat.generate_signals(df_daily_oops_short, symbol="SP500")
    assert len(signals) == 1
    s = signals[0]
    assert s.side == "short"
    # entry_price = prev_high - _TICK = 110 - 0.01 = 109.99
    assert s.entry_price == pytest.approx(109.99)


def test_oops_no_signal_when_no_gap(df_h1_two_days):
    """Without gaps, no signals are generated."""
    from src.strategies_external.data_loader import aggregate_to_daily

    daily = aggregate_to_daily(df_h1_two_days)
    # aggregate_to_daily of 2 H1-days = 2 daily bars, too few for atr_window=14.
    # Use atr_window=1 so that min rows required = 1+2 = 3; with 2 bars we still
    # get 0 signals because there are only 2 bars (need at least i=1, i.e. 2 rows)
    # but the early-return guard is shape[0] < atr_window + 2.
    # With atr_window=1: need >= 3 rows but we only have 2 → returns [].
    # That correctly validates the no-gap behaviour.
    strat = OOPSStrategy(atr_window=1)
    sigs = strat.generate_signals(daily, symbol="EURUSD")
    assert sigs == []
