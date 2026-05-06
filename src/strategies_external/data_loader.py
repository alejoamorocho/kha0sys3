"""Extensiones del cargador de datos para strategies_external.

Reusa CSVPolarsLoader de src/infrastructure/data/polars_loader.py.
Añade resampling y selección de tracking timeframe.
"""

from pathlib import Path

import polars as pl

from src.infrastructure.data.polars_loader import CSVPolarsLoader


_OHLC_COLS = ["time", "open", "high", "low", "close", "volume"]


def load_csv(symbol: str, tf: str, data_dir: str = "data") -> pl.DataFrame:
    """Carga el CSV histórico para (symbol, tf) reusando CSVPolarsLoader.

    Devuelve DataFrame con columnas canónicas en orden _OHLC_COLS.
    """
    loader = CSVPolarsLoader(data_dir)
    df = loader.load_data(symbol, tf)
    return df.select(_OHLC_COLS)


def _load_fine_tf(symbol: str, subdir: str, data_dir: str) -> pl.DataFrame | None:
    """Helper: lee data_dir/<subdir>/<symbol>.csv si existe, sino None."""
    path = Path(data_dir) / subdir / f"{symbol}.csv"
    if not path.is_file():
        return None
    df = pl.read_csv(path, has_header=True)
    df = df.rename({c: c.strip().lower() for c in df.columns})
    df = df.with_columns(
        pl.col("time")
        .str.slice(0, 19)
        .str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S", strict=False)
    )
    return df.sort("time").select(_OHLC_COLS)


def load_m1(symbol: str, data_dir: str = "data") -> pl.DataFrame | None:
    """Lee data/M1/<symbol>.csv si existe; None si no."""
    return _load_fine_tf(symbol, "M1", data_dir)


def load_m5(symbol: str, data_dir: str = "data") -> pl.DataFrame | None:
    """Lee data/M5/<symbol>.csv si existe; None si no."""
    return _load_fine_tf(symbol, "M5", data_dir)


def aggregate_to_daily(df: pl.DataFrame) -> pl.DataFrame:
    """Resamplea OHLCV a daily.

    Reglas: open=first, high=max, low=min, close=last, volume=sum.
    Asume `time` ya es polars Datetime; el DataFrame se ordena por tiempo
    defensivamente antes de agrupar.
    Devuelve un DataFrame con las mismas columnas; `time` queda al inicio del día.
    """
    if df.is_empty():
        return df.select(_OHLC_COLS)

    return (
        df.sort("time")
        .group_by_dynamic("time", every="1d", closed="left", label="left")
        .agg(
            pl.col("open").first(),
            pl.col("high").max(),
            pl.col("low").min(),
            pl.col("close").last(),
            pl.col("volume").sum(),
        )
        .select(_OHLC_COLS)
    )
