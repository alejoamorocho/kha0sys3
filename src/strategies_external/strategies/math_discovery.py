"""MATH discovery helpers for multi-TF (M15/H1/H4) with M1 intra-bar tracking.

T1: TF-parametric enrichment  (_load_and_enrich_math_tf)
T2: M1-tracking backtester    (run_setup_backtest_m1)

Direction guard is intentionally omitted in V1 (known simplification).
Setup detection already filters signals; guard mainly affects edge-case fills.
"""
from __future__ import annotations

from pathlib import Path
from dataclasses import dataclass

import polars as pl

from src.application.math_indicators import MathIndicatorEnricher
from src.engine.run_indicator_discovery import _load_and_enrich, _filter_by_session  # noqa: F401 (re-export)

# ── Constants ──────────────────────────────────────────────────────────────────

_TF_MINUTES = {"M15": 15, "H1": 60, "H4": 240}
CACHE_DIR = Path("data/enriched_math_tf")

MOMENTUM_SETUP_TYPES = (
    "VELOCITY_ACCEL_GO",
    "KAMA_CROSS_MOM",
    "OLS_SLOPE_STRONG",
    "HURST_TREND_MOM",
    "KALMAN_INNOV_EXPAND",
    "SPECTRAL_TREND_MOM",
)

FADE_SETUP_TYPES = (
    "KALMAN_PEAK_FADE",
    "ZSCORE_EXTREME_FADE",
    "OLS_EXTREME_FADE",
    "CURVATURE_PEAK_FADE",
    "GARCH_Z_FADE",
    "AREA_EXTREME_FADE",
)

WAIT_BARS = 5  # signal-TF bars to wait for fill


# ── T1: TF-parametric enrichment ──────────────────────────────────────────────

def _load_and_enrich_math_tf(symbol: str, tf: str) -> pl.DataFrame:
    """Load + enrich for any TF (M15/H1/H4). Caches to data/enriched_math_tf/."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE_DIR / f"{symbol}_{tf}.parquet"
    if cache_path.exists():
        return pl.read_parquet(cache_path)
    bars = _load_and_enrich(symbol, tf)          # base enrichment (IndicatorEnricher + ATR)
    bars = MathIndicatorEnricher.enrich_all_math(bars)
    bars.write_parquet(cache_path)
    return bars


# ── T2: M1-tracking backtester ────────────────────────────────────────────────

@dataclass(frozen=True)
class _BacktestCfg:
    tp_atr_mult: float
    sl_atr_mult: float
    session_end_hour_utc: int
    friction_r: float
    is_fade: bool
    wait_m1_bars: int     # derived from signal TF minutes * WAIT_BARS


def _empty_trades() -> pl.DataFrame:
    return pl.DataFrame(schema={
        "time": pl.Datetime, "symbol": pl.Utf8, "setup_type": pl.Utf8,
        "direction": pl.Utf8,
        "entry_price": pl.Float64, "tp_price": pl.Float64, "sl_price": pl.Float64,
        "exit_time": pl.Datetime, "exit_price": pl.Float64, "exit_reason": pl.Utf8,
        "r_multiple": pl.Float64,
    })


def precompute_m1_arrays(m1_df: pl.DataFrame) -> dict:
    """Pre-compute M1 numeric arrays once per symbol so they can be reused
    across many setup_type/session combos without re-converting polars→python list.

    Returns dict with keys: times (list[datetime]), highs/lows/closes (list[float]).
    """
    m1_sorted = m1_df.sort("time")
    return {
        "times": m1_sorted["time"].to_list(),
        "highs": m1_sorted["high"].to_list(),
        "lows": m1_sorted["low"].to_list(),
        "closes": m1_sorted["close"].to_list(),
    }


def run_setup_backtest_m1(
    setups: pl.DataFrame,
    bars_signal_tf: pl.DataFrame,   # M15/H1/H4 bars (for dedup ATR key lookup if needed)
    m1_df: pl.DataFrame,            # M1 tracking bars (or None if m1_arrays passed)
    setup_type: str,
    is_fade: bool,
    tp_atr_mult: float,
    sl_atr_mult: float,
    session_end_hour_utc: int,
    friction_r: float,
    symbol: str,
    signal_tf: str = "M15",
    m1_arrays: dict | None = None,
    invert_direction: bool = False,
) -> pl.DataFrame:
    """Simulate MOMENTUM or FADE fill + TP/SL tracking on M1 bars.

    Mechanics:
    - MOMENTUM: STOP order at stop_price (from detect_setups). Fill when
      M1 high >= stop_price (LONG) or M1 low <= stop_price (SHORT).
    - FADE: LIMIT order at close (from detect_setups). Fill when
      M1 low <= close (LONG) or M1 high >= close (SHORT).
    - Wait window: 5 signal_tf bars in M1 time = 5 * tf_minutes M1 bars.
    - TP/SL scan from fill bar+1 on M1.
    - Session time-stop when M1 bar hour >= session_end_hour_utc or next day.
    - Dedup: 1 trade per (setup_type, date).

    Known simplification: direction guard skipped (V1). Setup detection
    pre-filters; guard only affects edge-case fills.
    """
    if len(setups) == 0:
        return _empty_trades()

    tf_minutes = _TF_MINUTES.get(signal_tf, 15)
    wait_m1_bars = WAIT_BARS * tf_minutes

    # Plan 4 fix: bot live MATH uses direction_mode=INVERT (contrarian).
    # When invert_direction=True, flip LONG↔SHORT and recompute stop_price
    # for momentum (close ± 0.5*ATR mirror).
    if invert_direction:
        setups = setups.with_columns(
            pl.when(pl.col("direction") == "LONG").then(pl.lit("SHORT"))
              .otherwise(pl.lit("LONG")).alias("direction")
        )
        if "stop_price" in setups.columns and "atr_14" in setups.columns and "close" in setups.columns:
            setups = setups.with_columns(
                pl.when(pl.col("direction") == "LONG")
                  .then(pl.col("close") + 0.5 * pl.col("atr_14"))
                  .otherwise(pl.col("close") - 0.5 * pl.col("atr_14"))
                  .alias("stop_price")
            )

    # Dedup: 1 per (setup_type, date)
    setups = (
        setups.with_columns(pl.col("time").dt.date().alias("_date"))
        .sort("time")
        .unique(subset=["_date"], keep="first")
        .drop("_date")
    )

    # M1 arrays — reuse precomputed if provided (avoids re-converting per combo).
    if m1_arrays is not None:
        m1_times = m1_arrays["times"]
        m1_highs = m1_arrays["highs"]
        m1_lows = m1_arrays["lows"]
        m1_closes = m1_arrays["closes"]
    else:
        if m1_df is None or len(m1_df) == 0:
            return _empty_trades()
        m1_sorted = m1_df.sort("time")
        m1_times = m1_sorted["time"].to_list()
        m1_highs = m1_sorted["high"].to_list()
        m1_lows = m1_sorted["low"].to_list()
        m1_closes = m1_sorted["close"].to_list()

    if len(m1_times) == 0:
        return _empty_trades()

    # Build a searchable index: we use bisect to find starting position
    import bisect
    m1_time_list = m1_times  # already a list

    results = []

    # Determine the column name for order price depending on setup type
    # FADE setups use 'close' as limit_price; MOMENTUM uses 'stop_price'
    has_stop_price = "stop_price" in setups.columns
    has_close = "close" in setups.columns

    for s in setups.iter_rows(named=True):
        atr = s.get("atr_14")
        if atr is None or atr <= 0:
            continue
        direction = s.get("direction")
        if direction is None:
            continue

        # Order price
        if is_fade:
            order_price = s.get("close")
        else:
            order_price = s.get("stop_price") if has_stop_price else s.get("close")
        if order_price is None:
            continue

        setup_time = s["time"]

        # Find first M1 bar AFTER setup_time
        start_idx = bisect.bisect_right(m1_time_list, setup_time)
        if start_idx >= len(m1_times):
            continue

        # Wait window: up to start_idx + wait_m1_bars M1 bars
        end_wait = min(start_idx + wait_m1_bars, len(m1_times))

        fill_idx = None
        fill_price = None
        for i in range(start_idx, end_wait):
            hi = m1_highs[i]
            lo = m1_lows[i]
            if hi is None or lo is None:
                continue
            if is_fade:
                # LIMIT fill: LONG LIMIT -> lo touches limit; SHORT LIMIT -> hi touches limit
                if direction == "LONG":
                    if lo <= order_price:
                        fill_idx = i
                        fill_price = order_price
                        break
                else:
                    if hi >= order_price:
                        fill_idx = i
                        fill_price = order_price
                        break
            else:
                # STOP fill: LONG STOP -> hi crosses stop; SHORT STOP -> lo crosses stop
                if direction == "LONG":
                    if hi >= order_price:
                        fill_idx = i
                        fill_price = order_price
                        break
                else:
                    if lo <= order_price:
                        fill_idx = i
                        fill_price = order_price
                        break

        if fill_idx is None:
            continue

        entry = fill_price
        if direction == "LONG":
            tp = entry + tp_atr_mult * atr
            sl = entry - sl_atr_mult * atr
        else:
            tp = entry - tp_atr_mult * atr
            sl = entry + sl_atr_mult * atr

        exit_reason = None
        exit_price = None
        exit_time = None
        signal_date = setup_time.date()

        for j in range(fill_idx + 1, len(m1_times)):
            bt = m1_times[j]
            if bt.date() > signal_date or bt.hour >= session_end_hour_utc:
                exit_reason = "TIME_STOP"
                prev = j - 1
                exit_price = m1_closes[prev] if prev >= 0 else entry
                exit_time = m1_times[prev] if prev >= 0 else bt
                break
            hi = m1_highs[j]
            lo = m1_lows[j]
            if hi is None or lo is None:
                continue
            if direction == "LONG":
                if hi >= tp:
                    exit_reason, exit_price, exit_time = "TP", tp, bt
                    break
                if lo <= sl:
                    exit_reason, exit_price, exit_time = "SL", sl, bt
                    break
            else:
                if lo <= tp:
                    exit_reason, exit_price, exit_time = "TP", tp, bt
                    break
                if hi >= sl:
                    exit_reason, exit_price, exit_time = "SL", sl, bt
                    break
        else:
            # Reached end of M1 data without exit
            exit_reason = "TIME_STOP"
            exit_price = m1_closes[-1]
            exit_time = m1_times[-1]

        if exit_price is None:
            continue

        risk_per_unit = sl_atr_mult * atr
        if direction == "LONG":
            pnl = exit_price - entry
        else:
            pnl = entry - exit_price
        r_gross = pnl / risk_per_unit if risk_per_unit > 0 else 0.0
        r_net = r_gross - friction_r

        results.append({
            "time": setup_time,
            "symbol": symbol,
            "setup_type": setup_type,
            "direction": direction,
            "entry_price": entry,
            "tp_price": tp,
            "sl_price": sl,
            "exit_time": exit_time,
            "exit_price": exit_price,
            "exit_reason": exit_reason,
            "r_multiple": r_net,
        })

    if not results:
        return _empty_trades()
    return pl.DataFrame(results)
