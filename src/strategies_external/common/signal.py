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
