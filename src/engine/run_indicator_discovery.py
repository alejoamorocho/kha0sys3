"""Helpers used by the K3M1-75 discovery / robustness pipelines.

The legacy multi-phase Phase 1/2/3 CLI was removed in the K3M1-75 cleanup.
What remains:
  - `_filter_by_session(signals, session)`: slice a signal DF to the bars
    whose hour falls inside the configured session window. Used by both the
    live bot and the discovery scripts.
  - `_load_and_enrich(symbol, tf)`: load raw CSV bars, add ATR(14) and base
    technical indicators, cache to `data/enriched/<symbol>_<tf>.parquet`.
    Used by the K3 discovery rebuild path.
"""
from __future__ import annotations
from pathlib import Path

import polars as pl

from src.domain.constants import INDICATOR_SESSIONS
from src.application.indicators import IndicatorEnricher
from src.infrastructure.data.polars_loader import CSVPolarsLoader

DATA_DIR = "c:/Proyectos/kha0sys3/data"
ENRICHED_CACHE = Path("data/enriched")


def _filter_by_session(signals: pl.DataFrame, session: str) -> pl.DataFrame:
    start_h, end_h = INDICATOR_SESSIONS[session]
    return signals.filter(
        (pl.col("time").dt.hour() >= start_h) & (pl.col("time").dt.hour() < end_h)
    )


def _load_and_enrich(symbol: str, tf: str) -> pl.DataFrame:
    """Load raw CSV bars for (symbol, tf), add ATR(14) + base IndicatorEnricher
    features, cache to `data/enriched/`. Used by k3 discovery rebuild only."""
    cache_path = ENRICHED_CACHE / f"{symbol}_{tf}.parquet"
    if cache_path.exists():
        return pl.read_parquet(cache_path)
    ENRICHED_CACHE.mkdir(parents=True, exist_ok=True)
    loader = CSVPolarsLoader(DATA_DIR)
    bars = loader.load_data(symbol, tf)
    if "atr_14" not in bars.columns:
        bars = bars.with_columns(
            pl.max_horizontal(
                pl.col("high") - pl.col("low"),
                (pl.col("high") - pl.col("close").shift(1)).abs(),
                (pl.col("low") - pl.col("close").shift(1)).abs(),
            ).alias("_tr")
        ).with_columns(
            pl.col("_tr").ewm_mean(alpha=1 / 14, adjust=False,
                                    min_samples=14).alias("atr_14")
        ).drop("_tr")
    enriched = IndicatorEnricher.enrich_all(bars)
    enriched.write_parquet(cache_path)
    return enriched
