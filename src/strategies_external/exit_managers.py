"""ExitManagers: tres modos de calcular stop/tp1/tp2 para una señal raw.

- DocExitManager: reglas tal cual del documento por estrategia.
- ATRExitManager: multipliers de ATR (uniforme).
- IndicatorExitManager: anclas estructurales por estrategia.
"""

from abc import ABC, abstractmethod
from dataclasses import replace
from typing import ClassVar, Literal

from src.strategies_external.common.signal import Signal


_KNOWN_STRATEGIES = frozenset({"oops", "sma18", "double_bottom", "perdices_fib", "cot1", "fade"})


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
        if self.strategy == "cot1":
            return self._cot1(signal_raw)
        if self.strategy == "fade":
            return self._fade(signal_raw)
        raise ValueError(f"unknown strategy: {self.strategy}")

    def _oops(self, s: Signal) -> Signal:
        # Doc target = EOD: el backtester cierra al close de la última barra antes
        # de valid_until cuando no hay tp/stop hit. tp1=None, tp2=None.
        if s.side == "long":
            stop = _require_anchor(s, "today_low")
        else:
            stop = _require_anchor(s, "today_high")
        return replace(s, stop=stop, tp1=None, tp2=None)

    def _sma18(self, s: Signal) -> Signal:
        sma = _require_anchor(s, "sma18")
        atr = _require_anchor(s, "atr14")
        # Stop "hard" como protección extrema: SMA - 3*ATR (long) en caso de gap brutal
        if s.side == "long":
            hard_stop = sma - 3 * atr
        else:
            hard_stop = sma + 3 * atr
        # Backtester cierra cuando 2 cierres daily consecutivos cruzan la SMA en contra.
        return replace(
            s,
            stop=hard_stop,
            tp1=None, tp2=None,
            exit_on_two_closes_against=sma,
            exit_close_count_required=2,
        )

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
        # Doc: "cerrar si tras 4h la posición no avanza 1R a favor" — condicional, no fijo.
        return replace(
            s, stop=stop, tp1=tp1, tp2=None,
            timestop_bars=None,
            exit_after_bars_if_below_R=(240, 1.0),
        )

    def _cot1(self, s: Signal) -> Signal:
        atr = _require_anchor(s, "atr14")
        if s.side == "long":
            stop = _require_anchor(s, "swing_low_5d") - 0.5 * atr
            R = s.entry_price - stop
            tp1 = s.entry_price + 1.5 * R
            tp2 = s.entry_price + 3.0 * R
        else:
            stop = _require_anchor(s, "swing_high_5d") + 0.5 * atr
            R = stop - s.entry_price
            tp1 = s.entry_price - 1.5 * R
            tp2 = s.entry_price - 3.0 * R
        # NO timestop_bars: el doc dice "5 días hábiles" que ya está en valid_until.
        return replace(s, stop=stop, tp1=tp1, tp2=tp2, timestop_bars=None)

    def _fade(self, s: Signal) -> Signal:
        tp_mult = _require_anchor(s, "tp_mult")
        sl_mult = _require_anchor(s, "sl_mult")
        or_width = _require_anchor(s, "or_width")
        if s.side == "short":
            # FADE_UP: entry at or_high, TP toward or_low, SL above or_high
            stop = s.entry_price + sl_mult * or_width
            tp1 = s.entry_price - tp_mult * or_width
        else:
            # FADE_DOWN: entry at or_low, TP toward or_high, SL below or_low
            stop = s.entry_price - sl_mult * or_width
            tp1 = s.entry_price + tp_mult * or_width
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
        if self.strategy == "sma18":
            return self._sma18(signal_raw)
        if self.strategy == "double_bottom":
            return self._double_bottom(signal_raw)
        if self.strategy == "perdices_fib":
            return self._perdices_fib(signal_raw)
        if self.strategy == "cot1":
            return self._cot1(signal_raw)
        if self.strategy == "fade":
            return self._fade(signal_raw)
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
        return replace(s, stop=stop, tp1=tp1, tp2=tp2, timestop_bars=None,
                       exit_after_bars_if_below_R=(240, 1.0))

    def _cot1(self, s: Signal) -> Signal:
        # Same anchors as doc; if a clearer "indicator" anchoring emerges later, refine.
        atr = _require_anchor(s, "atr14")
        if s.side == "long":
            stop = _require_anchor(s, "swing_low_5d") - 0.5 * atr
            R = s.entry_price - stop
            tp1 = s.entry_price + 1.5 * R
            tp2 = s.entry_price + 3.0 * R
        else:
            stop = _require_anchor(s, "swing_high_5d") + 0.5 * atr
            R = stop - s.entry_price
            tp1 = s.entry_price - 1.5 * R
            tp2 = s.entry_price - 3.0 * R
        # NO timestop_bars (same as DocExitManager._cot1)
        return replace(s, stop=stop, tp1=tp1, tp2=tp2, timestop_bars=None)

    def _fade(self, s: Signal) -> Signal:
        # Delegate to DocExitManager logic: OR-width based TP/SL.
        # No structural anchor improvements needed for V1.
        tp_mult = _require_anchor(s, "tp_mult")
        sl_mult = _require_anchor(s, "sl_mult")
        or_width = _require_anchor(s, "or_width")
        if s.side == "short":
            stop = s.entry_price + sl_mult * or_width
            tp1 = s.entry_price - tp_mult * or_width
        else:
            stop = s.entry_price - sl_mult * or_width
            tp1 = s.entry_price + tp_mult * or_width
        return replace(s, stop=stop, tp1=tp1, tp2=None)
