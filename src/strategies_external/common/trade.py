"""Trade: resultado de un Signal ejecutado por el backtester."""

from dataclasses import dataclass
from datetime import datetime
from typing import Literal


ExitReason = Literal["tp1", "tp2", "stop", "timestop", "signal_inverso", "eod"]


@dataclass(frozen=True)
class Trade:
    """Trade cerrado, después de friction y slippage."""

    symbol: str
    strategy: str
    exit_mode: Literal["doc", "atr", "indicator"]
    side: Literal["long", "short"]
    entry_ts: datetime
    entry: float
    stop: float
    tp1: float | None
    tp2: float | None
    exit_ts: datetime
    exit: float
    exit_reason: ExitReason
    R: float
    pnl_R: float
    pnl_pct: float
    bars_in_trade: int
