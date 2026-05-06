"""Tests para data_loader del módulo strategies_external."""

import polars as pl
import pytest

from src.strategies_external.data_loader import aggregate_to_daily


def test_aggregate_to_daily_two_full_days(df_h1_two_days: pl.DataFrame):
    """48 barras H1 → 2 barras daily. OHLC se calcula correctamente."""
    daily = aggregate_to_daily(df_h1_two_days)

    assert daily.shape[0] == 2

    day1 = daily.row(0, named=True)
    # día 1 (i=0..23): open[0]=100.0, max high = 100+23*0.2+0.5=105.1, min low=99.5, close[23]=104.7
    assert day1["open"] == pytest.approx(100.0)
    assert day1["high"] == pytest.approx(105.1)
    assert day1["low"] == pytest.approx(99.5)
    assert day1["close"] == pytest.approx(104.7)

    day2 = daily.row(1, named=True)
    # día 2 (i=24..47): o(i)=105-(i-24)*0.2 → o(47)=100.4, h(47)=100.9, l(47)=99.9, c(47)=100.5
    # max h del día está en i=24 (105.5); min l del día está en i=47 (99.9); close = c(47) = 100.5
    assert day2["open"] == pytest.approx(105.0)
    assert day2["high"] == pytest.approx(105.5)
    assert day2["low"] == pytest.approx(99.9)
    assert day2["close"] == pytest.approx(100.5)


def test_aggregate_to_daily_volume_sum(df_h1_two_days: pl.DataFrame):
    """volume diario = sum de las 24 barras H1."""
    daily = aggregate_to_daily(df_h1_two_days)
    assert daily["volume"].to_list() == [24000.0, 24000.0]


def test_aggregate_to_daily_empty():
    """DataFrame vacío produce DataFrame vacío con schema correcto."""
    empty = pl.DataFrame(schema={
        "time": pl.Datetime, "open": pl.Float64, "high": pl.Float64,
        "low": pl.Float64, "close": pl.Float64, "volume": pl.Float64,
    })
    daily = aggregate_to_daily(empty)
    assert daily.shape[0] == 0
    assert daily.columns == ["time", "open", "high", "low", "close", "volume"]
