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

# ── Indicator parameters (fixed; optimization out of scope) ────
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
BB_PERIOD = 20
BB_STD = 2.0
FRACTAL_WINDOW = 5  # 2 left + pivot + 2 right
ADX_PERIOD = 14
ADX_TREND_THRESHOLD = 25.0
ADX_TREND_SOFT = 20.0

# ── Indicator discovery: Phase-1 gates (loose) ─────────────────
PHASE1_MIN_TRADES_PER_YEAR = 100
PHASE1_MIN_WR = 0.60
PHASE1_MIN_PF = 1.2
PHASE1_MIN_EXPECTANCY_R = 0.0

# ── Indicator discovery: Phase-2 gates (strict) ────────────────
PHASE2_MIN_TRADES_PER_YEAR = 100
PHASE2_MIN_WR = 0.80
PHASE2_MIN_PF = 1.3
PHASE2_MIN_EXPECTANCY_R = 0.10
PHASE2_MAX_DD_R = 20.0
PHASE2_WF_OOS_RATIO = 0.85
PHASE2_MC_MAX_RUIN_PCT = 0.01
PHASE2_DECAY_MIN_RATIO = 0.70

# ── Indicator R:R ATR grid (Phase-2) ───────────────────────────
INDICATOR_TP_ATR_GRID = (1.0, 1.5, 2.0, 2.5, 3.0)
INDICATOR_SL_ATR_GRID = (0.75, 1.0, 1.5, 2.0)

# ── Session definitions (UTC hours) for indicator discovery ────
INDICATOR_SESSIONS = {
    "ASIA":        (0, 7),
    "LONDON":      (7, 12),
    "NY":          (12, 17),
    "LONDON_NY":   (7, 17),
    "ALL_DAY":     (0, 24),
}

# ── Walk-forward windows ──────────────────────────────────────
WF_IS_MONTHS = 6
WF_OOS_MONTHS = 2

# Universe of 15 assets (original set, includes XAGUSD + SP500)
INDICATOR_UNIVERSE = (
    "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "GBPJPY", "EURJPY", "GBPAUD",
    "XAUUSD", "XAGUSD", "WTI", "BRENT", "NATGAS",
    "SP500", "NASDAQ100", "VIX",
)
INDICATOR_TIMEFRAMES = ("M15", "H1")
