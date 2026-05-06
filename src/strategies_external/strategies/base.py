"""Strategy ABC: contrato común de las estrategias."""

from abc import ABC, abstractmethod

import polars as pl

from src.strategies_external.common.signal import Signal


class Strategy(ABC):
    """Una estrategia produce señales raw (sin stop/tp; eso lo pone el ExitManager)."""

    name: str

    @abstractmethod
    def generate_signals(self, df: pl.DataFrame, symbol: str) -> list[Signal]:
        """df: barras del TF de señal (típicamente daily). symbol: ticker."""
