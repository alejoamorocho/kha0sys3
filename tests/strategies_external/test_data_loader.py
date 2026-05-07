"""Tests para data_loader del módulo strategies_external."""

import polars as pl
import pytest

from src.strategies_external.data_loader import aggregate_to_daily
from src.strategies_external.data_loader import load_csv, load_m1, load_m5
from src.strategies_external.data_loader import best_tracking_tf


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


def test_load_csv_returns_polars_with_canonical_schema(tmp_path):
    """load_csv lee un CSV con el formato del proyecto y normaliza schema."""
    csv_file = tmp_path / "EURUSD_H1_20180101_20180101.csv"
    csv_file.write_text(
        "time,open,high,low,close,volume\n"
        "2018-01-01 00:00:00+00:00,1.20,1.21,1.19,1.205,1000.0\n"
        "2018-01-01 01:00:00+00:00,1.205,1.215,1.20,1.21,1500.0\n"
    )
    df = load_csv("EURUSD", "H1", data_dir=str(tmp_path))
    assert df.columns == ["time", "open", "high", "low", "close", "volume"]
    assert df["time"].dtype == pl.Datetime
    assert df.shape[0] == 2


def test_load_csv_missing_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_csv("NOPE", "H1", data_dir=str(tmp_path))


def test_load_m1_returns_none_when_missing(tmp_path):
    """load_m1 devuelve None si no existe data/M1/<symbol>.csv."""
    assert load_m1("EURUSD", data_dir=str(tmp_path)) is None


def test_load_m5_returns_none_when_missing(tmp_path):
    assert load_m5("EURUSD", data_dir=str(tmp_path)) is None


def test_load_m1_loads_when_present(tmp_path):
    m1_dir = tmp_path / "M1"
    m1_dir.mkdir()
    (m1_dir / "EURUSD.csv").write_text(
        "time,open,high,low,close,volume\n"
        "2024-01-01 00:00:00+00:00,1.10,1.11,1.09,1.105,500.0\n"
    )
    df = load_m1("EURUSD", data_dir=str(tmp_path))
    assert df is not None
    assert df.shape[0] == 1
    assert df["time"].dtype == pl.Datetime


def test_best_tracking_tf_prefers_m1(tmp_path):
    """Si existe M1, devuelve ('M1', df)."""
    (tmp_path / "M1").mkdir()
    (tmp_path / "M5").mkdir()
    (tmp_path / "M1" / "EURUSD.csv").write_text(
        "time,open,high,low,close,volume\n"
        "2024-01-01 00:00:00+00:00,1.10,1.11,1.09,1.105,500.0\n"
    )
    (tmp_path / "M5" / "EURUSD.csv").write_text(
        "time,open,high,low,close,volume\n"
        "2024-01-01 00:00:00+00:00,1.10,1.11,1.09,1.105,500.0\n"
    )
    tf, df = best_tracking_tf("EURUSD", data_dir=str(tmp_path))
    assert tf == "M1"
    assert df.shape[0] == 1


def test_best_tracking_tf_falls_back_to_m5(tmp_path):
    (tmp_path / "M5").mkdir()
    (tmp_path / "M5" / "EURUSD.csv").write_text(
        "time,open,high,low,close,volume\n"
        "2024-01-01 00:00:00+00:00,1.10,1.11,1.09,1.105,500.0\n"
    )
    # Crear M15 también
    (tmp_path / "EURUSD_M15_20240101_20240101.csv").write_text(
        "time,open,high,low,close,volume\n"
        "2024-01-01 00:00:00+00:00,1.10,1.11,1.09,1.105,500.0\n"
    )
    tf, _ = best_tracking_tf("EURUSD", data_dir=str(tmp_path))
    assert tf == "M5"


def test_best_tracking_tf_falls_back_to_m15(tmp_path):
    (tmp_path / "EURUSD_M15_20240101_20240101.csv").write_text(
        "time,open,high,low,close,volume\n"
        "2024-01-01 00:00:00+00:00,1.10,1.11,1.09,1.105,500.0\n"
    )
    tf, _ = best_tracking_tf("EURUSD", data_dir=str(tmp_path))
    assert tf == "M15"


def test_best_tracking_tf_raises_when_nothing(tmp_path):
    with pytest.raises(FileNotFoundError):
        best_tracking_tf("EURUSD", data_dir=str(tmp_path))
