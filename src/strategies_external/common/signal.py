"""Signal: estructura de salida de cada estrategia."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal


@dataclass(frozen=True)
class Signal:
    """Una orden potencial generada por una estrategia.

    El backtester resuelve su fill y exit; los ExitManagers pueden modificar
    stop/tp1/tp2 a partir de los indicator_anchors antes de pasar al backtester.
    """

    symbol: str
    strategy: str
    side: Literal["long", "short"]
    setup_ts: datetime
    entry_type: Literal["market", "stop", "limit"]
    entry_price: float
    valid_until: datetime
    stop: float
    tp1: float | None
    tp2: float | None
    tp1_size_pct: float = 0.5
    timestop_bars: int | None = None
    indicator_anchors: dict[str, float] = field(default_factory=dict)
    # NEW (Plan 2.5):
    # Para SMA-18: el backtester cierra el trade si hay N cierres consecutivos
    # del df_signal (típicamente daily) que cruzan este nivel en contra del side.
    exit_on_two_closes_against: float | None = None
    exit_close_count_required: int = 2
    # Para Perdices Fib: tras N barras tracking_tf, si el pnl_R < threshold, cerrar.
    # Tupla (bars, R_threshold). None desactiva.
    exit_after_bars_if_below_R: tuple[int, float] | None = None
