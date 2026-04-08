from dataclasses import dataclass, field
from typing import Optional, Dict

@dataclass
class StrategyDef:
    symbol: str
    session_name: str
    time_start: str
    duration: int
    archetype: str          # MOMENTUM_UP, MOMENTUM_DOWN, FADE_UP, FADE_DOWN, SHAKEOUT_UP, SHAKEOUT_DOWN
    direction: str          # UP or DOWN
    context_filter: Optional[Dict[str, str]] = None
    tp_multiplier: float = 1.5
    label: str = ""

    def __post_init__(self):
        if not self.label:
            ctx = ""
            if self.context_filter:
                ctx = " | " + ", ".join(f"{k}{v}" for k, v in self.context_filter.items())
            self.label = f"{self.symbol} {self.session_name} {self.duration}m {self.archetype}{ctx}"

    @property
    def strategy_id(self) -> str:
        parts = [self.symbol, self.session_name, str(self.duration), self.archetype]
        if self.context_filter:
            for k, v in sorted(self.context_filter.items()):
                parts.append(f"{k}{v}")
        return "_".join(parts).replace(" ", "")


@dataclass
class StrategyResult:
    strategy: StrategyDef
    total_trades: int = 0
    trades_per_year: float = 0.0
    win_rate: float = 0.0
    profit_factor: float = 0.0
    net_r: float = 0.0
    max_drawdown: float = 0.0
    sharpe: float = 0.0
    avg_r_per_trade: float = 0.0
    best_year: str = ""
    worst_year: str = ""
    yearly_stats: Dict = field(default_factory=dict)
    passes_filter: bool = False
