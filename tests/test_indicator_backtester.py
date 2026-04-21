import polars as pl
import pytest
from src.engine.indicator_backtester import IndicatorBacktester, BacktestConfig


@pytest.fixture
def bars_with_atr():
    """Synthetic 100-bar series with ATR=0.50 and clean trend to trigger TP."""
    import numpy as np
    n = 100
    rng = np.random.default_rng(0)
    price = 100.0 + np.arange(n) * 0.10 + rng.standard_normal(n) * 0.05
    return pl.DataFrame({
        "time": pl.datetime_range(
            start=pl.datetime(2024, 1, 1, 7, 0),
            end=pl.datetime(2024, 1, 2, 7, 45),
            interval="15m", eager=True,
        )[:n],
        "open": price, "high": price + 0.25, "low": price - 0.25, "close": price,
        "atr_14": [0.50] * n,
    })


@pytest.fixture
def trivial_long_signal(bars_with_atr):
    """One LONG signal at bar 10."""
    row = bars_with_atr.row(10, named=True)
    return pl.DataFrame({
        "time": [row["time"]],
        "symbol": ["TEST"],
        "direction": ["LONG"],
        "signal_type": ["UNIT_TEST"],
        "close": [row["close"]],
        "high": [row["high"]],
        "low": [row["low"]],
        "atr_14": [row["atr_14"]],
    })


def test_long_trade_hits_tp(bars_with_atr, trivial_long_signal):
    cfg = BacktestConfig(tp_atr_mult=2.0, sl_atr_mult=1.0, session_end_hour_utc=17,
                         friction_r=0.0)
    trades = IndicatorBacktester.run(trivial_long_signal, bars_with_atr, cfg)
    assert len(trades) == 1
    t = trades.row(0, named=True)
    assert t["exit_reason"] in ("TP", "SL", "TIME_STOP")
    # Rising series w/ ATR=0.5, TP=1.0 above entry → should hit TP
    assert t["exit_reason"] == "TP"
    assert t["r_multiple"] == pytest.approx(2.0, abs=0.01)


def test_dedup_one_trade_per_day_per_symbol_signal(bars_with_atr):
    # Two signals on the same day same symbol same type → only first survives
    row_a = bars_with_atr.row(5, named=True)
    row_b = bars_with_atr.row(10, named=True)
    signals = pl.DataFrame({
        "time": [row_a["time"], row_b["time"]],
        "symbol": ["TEST", "TEST"],
        "direction": ["LONG", "LONG"],
        "signal_type": ["DUP", "DUP"],
        "close": [row_a["close"], row_b["close"]],
        "high": [row_a["high"], row_b["high"]],
        "low": [row_a["low"], row_b["low"]],
        "atr_14": [0.50, 0.50],
    })
    cfg = BacktestConfig(tp_atr_mult=2.0, sl_atr_mult=1.0, session_end_hour_utc=17,
                         friction_r=0.0)
    trades = IndicatorBacktester.run(signals, bars_with_atr, cfg)
    assert len(trades) == 1
    assert trades["time"].to_list()[0] == row_a["time"]


def test_session_time_stop_closes_trade(bars_with_atr, trivial_long_signal):
    cfg = BacktestConfig(tp_atr_mult=100.0, sl_atr_mult=100.0, session_end_hour_utc=17,
                         friction_r=0.0)
    trades = IndicatorBacktester.run(trivial_long_signal, bars_with_atr, cfg)
    assert trades.row(0, named=True)["exit_reason"] == "TIME_STOP"


def test_friction_is_subtracted(bars_with_atr, trivial_long_signal):
    cfg = BacktestConfig(tp_atr_mult=2.0, sl_atr_mult=1.0, session_end_hour_utc=17,
                         friction_r=0.10)
    trades = IndicatorBacktester.run(trivial_long_signal, bars_with_atr, cfg)
    # Gross = +2R, net = 2.0 - 0.1 = 1.9
    assert trades.row(0, named=True)["r_multiple"] == pytest.approx(1.90, abs=0.01)
