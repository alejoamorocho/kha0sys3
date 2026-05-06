"""Extensiones del cargador de datos para strategies_external.

Reusa CSVPolarsLoader de src/infrastructure/data/polars_loader.py.
Añade resampling y selección de tracking timeframe.
"""

from pathlib import Path

import polars as pl

from src.infrastructure.data.polars_loader import CSVPolarsLoader


_OHLC_COLS = ["time", "open", "high", "low", "close", "volume"]


def aggregate_to_daily(df: pl.DataFrame) -> pl.DataFrame:
    """Resamplea OHLCV a daily.

    Reglas: open=first, high=max, low=min, close=last, volume=sum.
    Asume `time` ya es polars Datetime y el DataFrame está ordenado.
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
