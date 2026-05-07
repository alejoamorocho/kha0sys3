# tests/strategies_external/test_sma18_strategy.py
from datetime import datetime, timedelta

import polars as pl
import pytest

from src.strategies_external.strategies.sma18 import SMA18Strategy


def _daily(prices: list[tuple[float, float, float, float]]) -> pl.DataFrame:
    """Build daily OHLC from list of (open, high, low, close); volume=1000."""
    base = datetime(2024, 1, 1)
    rows = [(base + timedelta(days=i), o, h, l, c, 1000.0)
            for i, (o, h, l, c) in enumerate(prices)]
    return pl.DataFrame(
        {"time": [r[0] for r in rows],
         "open": [r[1] for r in rows], "high": [r[2] for r in rows],
         "low": [r[3] for r in rows], "close": [r[4] for r in rows],
         "volume": [r[5] for r in rows]},
        schema={"time": pl.Datetime, "open": pl.Float64, "high": pl.Float64,
                "low": pl.Float64, "close": pl.Float64, "volume": pl.Float64},
    )


def test_sma18_long_signal_after_two_clean_bars_above_sma():
    """Two consecutive bars with low > SMA, neither inside-day, then a higher high triggers."""
    # Construct 22 bars: first 18 ramping up to seed SMA, then 2 clean bars above SMA, then trigger bar
    prices = []
    for i in range(18):
        p = 100.0 + i * 0.5
        prices.append((p, p + 0.3, p - 0.3, p + 0.1))
    # bar 18: SMA ≈ 104.25; this bar (low > sma)
    prices.append((110.0, 111.0, 109.5, 110.5))  # low 109.5 > sma ~104.25
    # bar 19: also low > sma, not inside-day (high 112 > 111, low 109 < 109.5)
    prices.append((110.5, 112.0, 109.0, 111.5))
    # bar 20: trigger. high reaches max(high[-1], high[-2]) + 1tick = max(111, 112) = 112.01
    prices.append((111.0, 113.0, 110.0, 112.5))
    df = _daily(prices)
    strat = SMA18Strategy(sma_window=18)
    sigs = strat.generate_signals(df, symbol="XAUUSD")
    # The buy stop should be 112.01 (= max(111, 112) + 0.01).
    long_sigs = [s for s in sigs if s.side == "long"]
    assert len(long_sigs) >= 1
    s = long_sigs[-1]  # last triggered
    assert s.side == "long"
    assert s.entry_price == pytest.approx(112.01)
    assert s.entry_type == "stop"
    for k in ("sma18", "atr14"):
        assert k in s.indicator_anchors


def test_sma18_no_signal_when_inside_day():
    """If t-1 is inside-day relative to t-2, no signal even if both above SMA."""
    prices = []
    for i in range(18):
        p = 100.0 + i * 0.5
        prices.append((p, p + 0.3, p - 0.3, p + 0.1))
    # bar 18: not inside
    prices.append((110.0, 112.0, 109.0, 110.5))
    # bar 19: INSIDE-day vs bar 18 (high 111 < 112, low 109.5 > 109)
    prices.append((110.5, 111.0, 109.5, 110.0))
    # bar 20: would-be trigger
    prices.append((110.0, 113.0, 109.0, 111.0))
    df = _daily(prices)
    strat = SMA18Strategy(sma_window=18)
    sigs = strat.generate_signals(df, symbol="XAUUSD")
    # bar 19 inside-day → no long signal at bar 20 from this two-bar setup
    last_two_setups = [s for s in sigs if s.setup_ts == df["time"][20]]
    assert len(last_two_setups) == 0


def test_sma18_short_signal_after_two_clean_bars_below_sma():
    prices = []
    for i in range(18):
        p = 110.0 - i * 0.3  # downward to seed SMA
        prices.append((p, p + 0.3, p - 0.3, p - 0.1))
    # bar 18: high < SMA
    prices.append((104.0, 104.5, 103.0, 103.5))
    # bar 19: high < SMA, not inside-day
    prices.append((103.5, 105.0, 102.5, 103.0))
    # bar 20: trigger DOWN
    prices.append((103.0, 104.0, 101.5, 102.0))
    df = _daily(prices)
    strat = SMA18Strategy(sma_window=18)
    sigs = strat.generate_signals(df, symbol="XAUUSD")
    short_sigs = [s for s in sigs if s.side == "short"]
    assert len(short_sigs) >= 1
    # sell stop at min(low[-1], low[-2]) - 0.01 = min(102.5, 103.0) - 0.01 = 102.49
    s = short_sigs[-1]
    assert s.entry_price == pytest.approx(102.49)


def test_sma18_too_few_bars():
    df = _daily([(100.0, 101.0, 99.0, 100.5)] * 5)
    strat = SMA18Strategy(sma_window=18)
    assert strat.generate_signals(df, symbol="XAUUSD") == []
