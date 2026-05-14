"""
Central constants for the kha0sys3 trading system.
Single source of truth for all magic numbers used across backtesting and live execution.
"""

# ── Risk allocation (DynamicRiskAllocator) ──────────────────────
# Balance-tiered risk: aggressive while small, conservative as account grows.
# Each tier: (max_balance, min_risk_pct, max_risk_pct)
#   - Below $2k:  2.5% – 15%  (growth phase)
#   - $2k – $8k:  1.67% – 10% (consolidation)
#   - Above $8k:  1% – 6%     (preservation)
RISK_TIERS = [
    (2_000,  0.025,  0.15),
    (8_000,  0.0167, 0.10),
    (None,   0.01,   0.06),
]
RISK_MIN_PCT = 0.025      # Current tier default (< $2k)
RISK_MAX_PCT = 0.15       # Current tier default (< $2k)
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

# ── Math parallel runner (isolated from FADE) ──────────────────
# Distinct magic so fetch_positions(magic=1338) never sees FADE orders
# and the FADE runner never sees MATH orders.
MAGIC_NUMBER_MATH = 1338
MATH_BARS_LOOKBACK = 500       # M15 bars needed for math indicator enrichment
MATH_WAIT_BARS = 5             # STOP expiration window (5 * 15min = 75 min)
MATH_STOP_ATR_OFFSET = 0.5     # STOP placement distance in ATR units
MATH_GUARD_WEAKEN_THRESHOLD = 0.5  # guard triggers if |guard| < 0.5 * |g0|

# Unified portfolio risk (2026-05-14): SAME 0.1% por trade en TODOS los
# sistemas (K3M1-75 + Traders Swing + Traders ORB) para que la prueba de
# supervivencia sea homogenea. Sustituye el risk scaling antiguo del math-bot.
UNIFIED_RISK_PCT = 0.001       # 0.1% por trade, todos los magics

# Math-bot risk scaling (LEGACY — sustituido por UNIFIED_RISK_PCT, mantenido
# por compatibilidad con codigo antiguo que importa estas constantes).
MATH_RISK_MIN_PCT = 0.001
MATH_RISK_MAX_PCT = 0.001
MATH_WR_MIN = 0.57
MATH_WR_MAX = 1.00

# ── Traders (replica PDFs: Minervini/Zanger/Qulla/Ryan) ──────────
# Sistemas paralelos aislados de K3M1-75. Magic distinto por filosofia.
MAGIC_NUMBER_TRADERS_SWING = 1339   # Swing trend-following stocks-style (5 strats)
MAGIC_NUMBER_TRADERS_ORB   = 1340   # Qulla ORB intradia (12 strats)

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
# Relaxed 2026-04-20: original WR>=0.60 was unreachable with 2:1 R:R default.
# Max observed WR across 1500 combos was 0.44. New gates keep combos with
# positive expectancy at the default R:R, so Phase-2 can re-optimize R:R.
PHASE1_MIN_TRADES_PER_YEAR = 100
PHASE1_MIN_WR = 0.35
PHASE1_MIN_PF = 1.00
PHASE1_MIN_EXPECTANCY_R = 0.0

# ── Indicator discovery: Phase-2 gates (strict) ────────────────
# WR gate relaxed from 0.80 to 0.65 (realistic for indicator-based edge).
PHASE2_MIN_TRADES_PER_YEAR = 100
PHASE2_MIN_WR = 0.65
PHASE2_MIN_PF = 1.3
PHASE2_MIN_EXPECTANCY_R = 0.10
PHASE2_MAX_DD_R = 20.0
PHASE2_WF_OOS_RATIO = 0.85
PHASE2_MC_MAX_RUIN_PCT = 0.01
PHASE2_DECAY_MIN_RATIO = 0.70

# ── Indicator R:R ATR grid (Phase-2) ───────────────────────────
# Expanded to include tight TPs (0.3-0.75 ATR). Tight TP + wide SL lifts WR
# into the 65-85% band required by Phase-2 gate.
INDICATOR_TP_ATR_GRID = (0.3, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0)
INDICATOR_SL_ATR_GRID = (0.75, 1.0, 1.5, 2.0, 2.5)

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
