"""
Central constants for the kha0sys3 trading system.
Single source of truth for all magic numbers used across backtesting and live execution.
"""

# ── Risk allocation (DynamicRiskAllocator) ──────────────────────
RISK_MIN_PCT = 0.01       # 1% risk at lowest WR
RISK_MAX_PCT = 0.06       # 6% risk at highest WR
WR_MIN = 0.57             # WR threshold for min risk
WR_MAX = 0.91             # WR threshold for max risk
DEFAULT_WIN_RATE = 0.60   # Default WR when not specified

# ── ATR filter ──────────────────────────────────────────────────
ATR_RATIO_LOW = 0.1       # Minimum OR/ATR ratio for valid trade
ATR_RATIO_HIGH = 0.8      # Maximum OR/ATR ratio for valid trade

# ── Trade mechanics ─────────────────────────────────────────────
DEFAULT_TP_MULTIPLIER = 1.5   # TP distance in OR widths
SESSION_WINDOW_HOURS = 8      # Active session window after OR close

# ── Friction (slippage + spread) in R units ─────────────────────
FRICTION_FX = 0.1
FRICTION_INDEX = 0.2

# ── MT5 execution ──────────────────────────────────────────────
MAGIC_NUMBER = 1337
ORDER_EXPIRATION_HOURS = 8

# ── Symbol classification ──────────────────────────────────────
INDEX_SYMBOLS = frozenset({"SP500", "NASDAQ100", "VIX", "WTI", "BRENT", "NATGAS"})

MT5_TO_INTERNAL = {
    "EURUSD+": "EURUSD", "GBPUSD+": "GBPUSD", "USDJPY+": "USDJPY",
    "AUDUSD+": "AUDUSD", "GBPJPY+": "GBPJPY", "EURJPY+": "EURJPY",
    "GBPAUD+": "GBPAUD", "XAUUSD+": "XAUUSD", "XAGUSD": "XAGUSD",
    "USOUSD": "WTI", "UKOUSD": "BRENT", "NG-C": "NATGAS",
    "SP500": "SP500", "NAS100": "NASDAQ100", "VIX": "VIX",
}

# ── Strategy scanning ──────────────────────────────────────────
MIN_STRATEGY_DAYS = 20    # Minimum sample size for strategy evaluation
