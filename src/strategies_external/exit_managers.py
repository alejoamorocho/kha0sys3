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
        if self.strategy == "sma18":
            return self._sma18(signal_raw)
        if self.strategy == "double_bottom":
            return self._double_bottom(signal_raw)
        if self.strategy == "perdices_fib":
            return self._perdices_fib(signal_raw)
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

    def _sma18(self, s: Signal) -> Signal:
        # Stop = SMA-18 (señal contraria definida como cruce de SMA).
        # No fixed TP — let the trade run.
        sma = _require_anchor(s, "sma18")
        return replace(s, stop=sma, tp1=None, tp2=None)

    def _double_bottom(self, s: Signal) -> Signal:
        consol_low = _require_anchor(s, "consol_low")
        neckline = _require_anchor(s, "neckline")
        altura = _require_anchor(s, "altura_patron")
        if s.side == "long":
            stop = consol_low
            tp1 = neckline + altura
            tp2 = neckline + altura * 1.618
        else:
            consol_high = _require_anchor(s, "consol_high")
            stop = consol_high
            tp1 = neckline - altura
            tp2 = neckline - altura * 1.618
        return replace(s, stop=stop, tp1=tp1, tp2=tp2)

    def _perdices_fib(self, s: Signal) -> Signal:
        if s.side == "long":
            stop = _require_anchor(s, "swing_low") - 0.2
            tp1 = _require_anchor(s, "swing_high")
        else:
            stop = _require_anchor(s, "swing_high") + 0.2
            tp1 = _require_anchor(s, "swing_low")
        return replace(s, stop=stop, tp1=tp1, tp2=None, timestop_bars=240)  # 240 M1 bars = 4h


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
        if self.strategy == "sma18":
            return self._sma18(signal_raw)
        if self.strategy == "double_bottom":
            return self._double_bottom(signal_raw)
        if self.strategy == "perdices_fib":
            return self._perdices_fib(signal_raw)
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

    def _sma18(self, s: Signal) -> Signal:
        sma = _require_anchor(s, "sma18")
        atr = _require_anchor(s, "atr14")
        if s.side == "long":
            stop = sma - 0.5 * atr
            tp1 = sma + 2.0 * atr
            tp2 = sma + 4.0 * atr
        else:
            stop = sma + 0.5 * atr
            tp1 = sma - 2.0 * atr
            tp2 = sma - 4.0 * atr
        return replace(s, stop=stop, tp1=tp1, tp2=tp2)

    def _double_bottom(self, s: Signal) -> Signal:
        L2 = _require_anchor(s, "L2")
        neckline = _require_anchor(s, "neckline")
        altura = _require_anchor(s, "altura_patron")
        if s.side == "long":
            stop = L2 - 0.25 * altura
            tp1 = neckline + altura
            tp2 = neckline + altura * 1.618
        else:
            stop = L2 + 0.25 * altura
            tp1 = neckline - altura
            tp2 = neckline - altura * 1.618
        return replace(s, stop=stop, tp1=tp1, tp2=tp2)

    def _perdices_fib(self, s: Signal) -> Signal:
        if s.side == "long":
            stop = _require_anchor(s, "swing_low") - 0.2
            tp1 = _require_anchor(s, "swing_high")
            tp2 = _require_anchor(s, "fib_1618")
        else:
            stop = _require_anchor(s, "swing_high") + 0.2
            tp1 = _require_anchor(s, "swing_low")
            tp2 = _require_anchor(s, "fib_1618")
        return replace(s, stop=stop, tp1=tp1, tp2=tp2, timestop_bars=240)
