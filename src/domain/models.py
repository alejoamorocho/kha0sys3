from dataclasses import dataclass
from typing import Optional, List, Dict
from datetime import time, datetime

@dataclass
class AssetConfig:
    symbol: str
    session_name: str
    time_start: time
    duration_minutes: int
    time_end: time
    pd_start: time
    pd_end: time
    atr_multiplier: float = 1.0
    premarket_start: Optional[time] = None

@dataclass
class TradeSignal:
    symbol: str
    direction: str  # "LONG" or "SHORT"
    entry_price: float
    stop_loss: float
    tp1: float
    tp2: float
    tp3: float
    position_size_pct: float
    confidence_multiplier: float
    timestamp: datetime
    
@dataclass
class DailyMetrics:
    symbol: str
    date: str
    or_high: float
    or_low: float
    or_width: float
    or_open: float
    pd_high: float
    pd_low: float
    pd_close: float
    atr_d1: float
    max_up: float
    max_down: float
    breakout_up_count: int
    breakout_down_count: int
    touches_pd_high: int
    touches_pd_low: int
