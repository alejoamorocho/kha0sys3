"""ExitManagers: tres modos de calcular stop/tp1/tp2 para una señal raw.

- DocExitManager: reglas tal cual del documento por estrategia.
- ATRExitManager: multipliers de ATR (uniforme).
- IndicatorExitManager: anclas estructurales por estrategia.
"""

from abc import ABC, abstractmethod
from dataclasses import replace
from typing import ClassVar, Literal

from src.strategies_external.common.signal import Signal


_KNOWN_STRATEGIES = frozenset({"oops", "sma18", "double_bottom", "perdices_fib", "cot1"})


class ExitManager(ABC):
    name: ClassVar[Literal["doc", "atr", "indicator"]]

    @abstractmethod
    def attach_levels(self, signal_raw: Signal) -> Signal:
        """Devuelve una nueva Signal con stop/tp1/tp2 calculados."""


def _require_anchor(signal: Signal, key: str) -> float:
    if key not in signal.indicator_anchors:
        raise ValueError(
            f"strategy={signal.strategy} side={signal.side} requires anchor '{key}' "
            f"but only {sorted(signal.indicator_anchors)} are present"
        )
    return signal.indicator_anchors[key]


class DocExitManager(ExitManager):
    """Reglas de salida copiadas del documento fuente."""

    name = "doc"

    def __init__(self, strategy: str):
        if strategy not in _KNOWN_STRATEGIES:
            raise ValueError(f"unknown strategy: {strategy}")
        self.strategy = strategy

    def attach_levels(self, signal_raw: Signal) -> Signal:
        if self.strategy == "oops":
            return self._oops(signal_raw)
        # Otras estrategias: implementadas en Plan 2.
        raise ValueError(f"unknown strategy: {self.strategy}")

    def _oops(self, s: Signal) -> Signal:
        if s.side == "long":
            stop = _require_anchor(s, "today_low")
            R = s.entry_price - stop
            tp1 = s.entry_price + 2 * R
        else:
            stop = _require_anchor(s, "today_high")
            R = stop - s.entry_price
            tp1 = s.entry_price - 2 * R
        return replace(s, stop=stop, tp1=tp1, tp2=None)


class ATRExitManager(ExitManager):
    """Stops/TPs uniformes como múltiplos de ATR."""

    name = "atr"

    def __init__(self, sl_mult: float, tp1_mult: float, tp2_mult: float | None):
        if tp2_mult is not None and tp2_mult <= tp1_mult:
            raise ValueError("tp2_mult must be > tp1_mult")
        self.sl_mult = sl_mult
        self.tp1_mult = tp1_mult
        self.tp2_mult = tp2_mult

    def attach_levels(self, signal_raw: Signal) -> Signal:
        atr = _require_anchor(signal_raw, "atr14")
        if signal_raw.side == "long":
            stop = signal_raw.entry_price - self.sl_mult * atr
            tp1 = signal_raw.entry_price + self.tp1_mult * atr
            tp2 = signal_raw.entry_price + self.tp2_mult * atr if self.tp2_mult is not None else None
        else:
            stop = signal_raw.entry_price + self.sl_mult * atr
            tp1 = signal_raw.entry_price - self.tp1_mult * atr
            tp2 = signal_raw.entry_price - self.tp2_mult * atr if self.tp2_mult is not None else None
        return replace(signal_raw, stop=stop, tp1=tp1, tp2=tp2)


class IndicatorExitManager(ExitManager):
    """Stops/TPs anclados a indicadores estructurales por estrategia."""

    name = "indicator"

    def __init__(self, strategy: str):
        if strategy not in _KNOWN_STRATEGIES:
            raise ValueError(f"unknown strategy: {strategy}")
        self.strategy = strategy

    def attach_levels(self, signal_raw: Signal) -> Signal:
        if self.strategy == "oops":
            return self._oops(signal_raw)
        raise ValueError(f"unknown strategy: {self.strategy}")

    def _oops(self, s: Signal) -> Signal:
        prev_high = _require_anchor(s, "prev_high")
        prev_low = _require_anchor(s, "prev_low")
        prev_range = _require_anchor(s, "prev_range")
        if s.side == "long":
            stop = _require_anchor(s, "today_low")
            tp1 = prev_low + prev_range / 2.0
            tp2 = prev_high + prev_range
        else:
            stop = _require_anchor(s, "today_high")
            tp1 = prev_high - prev_range / 2.0
            tp2 = prev_low - prev_range
        return replace(s, stop=stop, tp1=tp1, tp2=tp2)
