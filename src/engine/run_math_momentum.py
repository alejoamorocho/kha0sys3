"""Math-MOMENTUM discovery pipeline - M15 only.

Mirror of run_math_fade.py but for momentum/breakout edge. Instead of fading
math extremes, this pipeline takes STOP orders IN the direction of a building
trend detected by pure math indicators.

Per setup at bar T:
- Entry: STOP order at a confirmation price IN the momentum direction.
  - VELOCITY_ACCEL_GO uses bar T high/low +/- 1 tick (break-of-bar confirm).
  - All others use close[T] +/- 0.5*ATR.
- Wait window: next 5 bars (75 min). If not filled -> cancel.
- Direction guard: if the setup indicator WEAKENS during the wait -> cancel.
- On fill: TP at entry +/- tp_atr_mult*ATR, SL at entry -/+ sl_atr_mult*ATR.
  Default MOMENTUM R:R = TP 2.0*ATR / SL 1.0*ATR (opposite of FADE).
- Session time-stop.
- Dedup: 1 trade per (symbol, setup_type, date).

Phases:
    A = setup screen at default TP=2.0/SL=1.0 ATR
    B = R:R grid on Phase-A survivors (5 x 4 = 20 combos)
    C = WF + MC + decay robustness

Usage:
    python -m src.engine.run_math_momentum --phase {a,b,c,all}
"""
from __future__ import annotations
import argparse
import json
from dataclasses import dataclass
from pathlib import Path

import polars as pl

from src.domain.constants import (
    INDICATOR_UNIVERSE, INDICATOR_SESSIONS,
    FRICTION_FX, FRICTION_INDEX, INDEX_SYMBOLS,
    WF_IS_MONTHS, WF_OOS_MONTHS,
)
from src.engine.run_math_discovery import _load_and_enrich_math
from src.engine.run_indicator_discovery import _filter_by_session
from src.engine.indicator_validation import (
    compute_metrics, walk_forward_wr, monte_carlo_ruin, decay_slope_ratio,
)

REPORTS_DIR = Path("reports")
TF = "M15"

SETUP_TYPES = (
    "VELOCITY_ACCEL_GO",
    "KAMA_CROSS_MOM",
    "OLS_SLOPE_STRONG",
    "HURST_TREND_MOM",
    "KALMAN_INNOV_EXPAND",
    "SPECTRAL_TREND_MOM",
)

# ── Phase A gates (momentum: lower WR, higher payoff) ──────────────────
PA_DEFAULT_TP = 2.0
PA_DEFAULT_SL = 1.0
PA_MIN_TRADES_PER_YEAR = 15
PA_MIN_WR = 0.45
PA_MIN_PF = 1.15

# ── Phase B grid + gates ───────────────────────────────────────────────
PB_TP_GRID = (1.0, 1.5, 2.0, 2.5, 3.0)
PB_SL_GRID = (0.5, 0.75, 1.0, 1.5)
PB_MIN_TRADES_PER_YEAR = 15
PB_MIN_PF = 1.25
PB_MIN_EXPECTANCY = 0.05
PB_MAX_DD_R = 25.0

# ── Phase C gates ──────────────────────────────────────────────────────
PC_MIN_WF_RATIO = 0.80
PC_MAX_MC_RUIN = 0.02
PC_MIN_DECAY = 0.60

WAIT_BARS = 5  # 75 min on M15


def _friction_for(symbol: str) -> float:
    return FRICTION_INDEX if symbol in INDEX_SYMBOLS else FRICTION_FX


def _session_end_hour(session: str) -> int:
    return INDICATOR_SESSIONS[session][1]


# ── Setup detection ────────────────────────────────────────────────────

@dataclass(frozen=True)
class BacktestConfig:
    tp_atr_mult: float
    sl_atr_mult: float
    session_end_hour_utc: int
    friction_r: float


def detect_setups(bars: pl.DataFrame, setup_type: str) -> pl.DataFrame:
    """Return DataFrame with columns:
        time, close, high, low, direction (LONG/SHORT), atr_14,
        stop_price (confirmation breakout price),
        guard_value (initial signed magnitude of the setup's guard indicator).
    """
    if len(bars) == 0:
        return _empty_setups()

    df = bars

    if setup_type == "VELOCITY_ACCEL_GO":
        vel = pl.col("velocity_10")
        acc = pl.col("accel_10")
        vel_std = vel.rolling_std(window_size=50)
        # one tick = 1e-5 generic; we use a small fraction of ATR for a pip-like offset
        tick = pl.col("atr_14") * 0.01
        fire = (
            (vel.sign() == acc.sign())
            & (vel.abs() > 1.5 * vel_std)
            & (acc.abs() > 0)
            & vel.is_not_null() & acc.is_not_null() & vel_std.is_not_null()
        )
        direction = pl.when(vel > 0).then(pl.lit("LONG")).otherwise(pl.lit("SHORT"))
        # STOP price: high+tick for LONG, low-tick for SHORT
        stop_price = pl.when(vel > 0) \
            .then(pl.col("high") + tick) \
            .otherwise(pl.col("low") - tick)
        guard_value = vel  # guard tracks velocity sign/magnitude

    elif setup_type == "KAMA_CROSS_MOM":
        close = pl.col("close")
        kama = pl.col("kama_10")
        slope = pl.col("kama_slope_10")
        slope_std = slope.rolling_std(window_size=50)
        # Bullish cross: prev close <= prev kama, curr close > curr kama
        bull_cross = (close.shift(1) <= kama.shift(1)) & (close > kama)
        bear_cross = (close.shift(1) >= kama.shift(1)) & (close < kama)
        fire_long = bull_cross & (slope > 0) & (slope > slope_std)
        fire_short = bear_cross & (slope < 0) & (slope.abs() > slope_std)
        fire = (fire_long | fire_short) & slope.is_not_null() & slope_std.is_not_null()
        direction = pl.when(fire_long).then(pl.lit("LONG")).otherwise(pl.lit("SHORT"))
        stop_price = pl.when(fire_long) \
            .then(close + 0.5 * pl.col("atr_14")) \
            .otherwise(close - 0.5 * pl.col("atr_14"))
        guard_value = slope

    elif setup_type == "OLS_SLOPE_STRONG":
        slope = pl.col("ols_slope_30")
        slope_std = slope.rolling_std(window_size=50)
        strong = slope.abs() > 1.5 * slope_std
        rising = slope.abs() > slope.shift(1).abs()  # magnitude rising
        # Also require same sign (momentum, not reversal)
        same_sign = slope.sign() == slope.shift(1).sign()
        fire = strong & rising & same_sign & slope.is_not_null() & slope_std.is_not_null()
        direction = pl.when(slope > 0).then(pl.lit("LONG")).otherwise(pl.lit("SHORT"))
        stop_price = pl.when(slope > 0) \
            .then(pl.col("close") + 0.5 * pl.col("atr_14")) \
            .otherwise(pl.col("close") - 0.5 * pl.col("atr_14"))
        guard_value = slope

    elif setup_type == "HURST_TREND_MOM":
        h = pl.col("hurst_rs_100")
        vel = pl.col("velocity_10")
        vel_std = vel.rolling_std(window_size=50)
        persistent = h > 0.6
        confirmed = (vel.sign() == vel.shift(1).sign()) & (vel.abs() > vel_std)
        fire = persistent & confirmed & h.is_not_null() & vel.is_not_null() & vel_std.is_not_null()
        direction = pl.when(vel > 0).then(pl.lit("LONG")).otherwise(pl.lit("SHORT"))
        stop_price = pl.when(vel > 0) \
            .then(pl.col("close") + 0.5 * pl.col("atr_14")) \
            .otherwise(pl.col("close") - 0.5 * pl.col("atr_14"))
        guard_value = vel

    elif setup_type == "KALMAN_INNOV_EXPAND":
        innov = pl.col("kalman_innovation")
        innov_std = innov.rolling_std(window_size=50)
        same_sign = innov.sign() == innov.shift(1).sign()
        expanding = innov.abs() > innov.shift(1).abs()
        big = innov.abs() > 1.5 * innov_std
        fire = same_sign & expanding & big & innov.is_not_null() & innov_std.is_not_null()
        direction = pl.when(innov > 0).then(pl.lit("LONG")).otherwise(pl.lit("SHORT"))
        stop_price = pl.when(innov > 0) \
            .then(pl.col("close") + 0.5 * pl.col("atr_14")) \
            .otherwise(pl.col("close") - 0.5 * pl.col("atr_14"))
        guard_value = innov

    elif setup_type == "SPECTRAL_TREND_MOM":
        sr = pl.col("spectral_ratio_64")
        vel = pl.col("velocity_10")
        vel_std = vel.rolling_std(window_size=50)
        fire = (sr > 2.0) & (vel.abs() > vel_std) \
            & sr.is_not_null() & vel.is_not_null() & vel_std.is_not_null()
        direction = pl.when(vel > 0).then(pl.lit("LONG")).otherwise(pl.lit("SHORT"))
        stop_price = pl.when(vel > 0) \
            .then(pl.col("close") + 0.5 * pl.col("atr_14")) \
            .otherwise(pl.col("close") - 0.5 * pl.col("atr_14"))
        guard_value = vel

    else:
        raise ValueError(f"Unknown setup_type: {setup_type}")

    setups = df.with_columns([
        fire.alias("_fire"),
        direction.alias("direction"),
        stop_price.alias("stop_price"),
        guard_value.alias("guard_value"),
    ]).filter(
        pl.col("_fire") & pl.col("atr_14").is_not_null() & pl.col("stop_price").is_not_null()
    ).select([
        "time", "close", "high", "low", "direction", "atr_14", "stop_price", "guard_value",
    ])
    return setups


def _empty_setups() -> pl.DataFrame:
    return pl.DataFrame(schema={
        "time": pl.Datetime, "close": pl.Float64, "high": pl.Float64, "low": pl.Float64,
        "direction": pl.Utf8, "atr_14": pl.Float64,
        "stop_price": pl.Float64, "guard_value": pl.Float64,
    })


def _guard_indicator_col(setup_type: str) -> str:
    return {
        "VELOCITY_ACCEL_GO": "velocity_10",
        "KAMA_CROSS_MOM": "kama_slope_10",
        "OLS_SLOPE_STRONG": "ols_slope_30",
        "HURST_TREND_MOM": "velocity_10",
        "KALMAN_INNOV_EXPAND": "kalman_innovation",
        "SPECTRAL_TREND_MOM": "velocity_10",
    }[setup_type]


# ── Backtester ──────────────────────────────────────────────────────────

def run_backtest(setups: pl.DataFrame, bars: pl.DataFrame, setup_type: str,
                 cfg: BacktestConfig, symbol: str) -> pl.DataFrame:
    """Event-driven MOMENTUM backtest with STOP wait window + direction guard."""
    if len(setups) == 0:
        return _empty_trades()

    # Dedup: first per (date, setup_type)
    setups = setups.with_columns(pl.col("time").dt.date().alias("_date")) \
        .sort("time").unique(subset=["_date"], keep="first").drop("_date")

    bars_sorted = bars.sort("time")
    guard_col = _guard_indicator_col(setup_type)
    bar_times = bars_sorted["time"].to_list()
    bar_highs = bars_sorted["high"].to_list()
    bar_lows = bars_sorted["low"].to_list()
    bar_closes = bars_sorted["close"].to_list()
    guard_vals = bars_sorted[guard_col].to_list()
    time_to_idx = {t: i for i, t in enumerate(bar_times)}

    results = []
    for s in setups.iter_rows(named=True):
        atr = s["atr_14"]
        if atr is None or atr <= 0:
            continue
        direction = s["direction"]
        stop_price = s["stop_price"]
        g0 = s["guard_value"]
        if g0 is None or stop_price is None:
            continue
        start_idx = time_to_idx.get(s["time"])
        if start_idx is None:
            continue

        # Direction guard: initial sign + initial magnitude
        g0_sign = 1.0 if g0 > 0 else (-1.0 if g0 < 0 else 0.0)
        g0_abs = abs(g0)
        # threshold for "weakening": guard magnitude falls below 0.5 * initial
        weaken_thresh = 0.5 * g0_abs

        # Wait window for STOP fill
        fill_idx = None
        fill_price = None
        end_wait = min(start_idx + 1 + WAIT_BARS, len(bar_times))
        cancelled = False
        for i in range(start_idx + 1, end_wait):
            # Direction guard: cancel if guard flips sign or drops below half magnitude
            gv = guard_vals[i]
            if gv is not None and g0_sign != 0:
                gv_aligned = gv * g0_sign  # positive means still with us
                if gv_aligned < weaken_thresh:
                    cancelled = True
                    break
            hi = bar_highs[i]
            lo = bar_lows[i]
            # STOP fill: LONG STOP above stop_price requires hi>=stop_price;
            #           SHORT STOP below stop_price requires lo<=stop_price.
            if direction == "LONG":
                if hi >= stop_price:
                    fill_idx = i
                    fill_price = stop_price
                    break
            else:
                if lo <= stop_price:
                    fill_idx = i
                    fill_price = stop_price
                    break
        if cancelled or fill_idx is None:
            continue

        entry = fill_price
        if direction == "LONG":
            tp = entry + cfg.tp_atr_mult * atr
            sl = entry - cfg.sl_atr_mult * atr
        else:
            tp = entry - cfg.tp_atr_mult * atr
            sl = entry + cfg.sl_atr_mult * atr

        exit_reason = None
        exit_price = None
        exit_time = None
        signal_date = s["time"].date()
        # On the fill bar itself, check remaining range for immediate TP/SL.
        # Simplification: start scanning from fill bar + 1 (conservative; matches fade semantics).
        for j in range(fill_idx + 1, len(bar_times)):
            bt = bar_times[j]
            if bt.date() > signal_date or bt.hour >= cfg.session_end_hour_utc:
                exit_reason = "TIME_STOP"
                exit_price = bar_closes[j - 1]
                exit_time = bar_times[j - 1]
                break
            hi = bar_highs[j]
            lo = bar_lows[j]
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
            exit_reason = "TIME_STOP"
            exit_price = bar_closes[-1]
            exit_time = bar_times[-1]

        risk_per_unit = cfg.sl_atr_mult * atr
        if direction == "LONG":
            pnl = exit_price - entry
        else:
            pnl = entry - exit_price
        r_gross = pnl / risk_per_unit if risk_per_unit > 0 else 0.0
        r_net = r_gross - cfg.friction_r

        results.append({
            "time": s["time"], "symbol": symbol,
            "setup_type": setup_type, "direction": direction,
            "entry_price": entry, "tp_price": tp, "sl_price": sl,
            "exit_time": exit_time, "exit_price": exit_price,
            "exit_reason": exit_reason, "r_multiple": r_net,
        })
    if not results:
        return _empty_trades()
    return pl.DataFrame(results)


def _empty_trades() -> pl.DataFrame:
    return pl.DataFrame(schema={
        "time": pl.Datetime, "symbol": pl.Utf8, "setup_type": pl.Utf8, "direction": pl.Utf8,
        "entry_price": pl.Float64, "tp_price": pl.Float64, "sl_price": pl.Float64,
        "exit_time": pl.Datetime, "exit_price": pl.Float64, "exit_reason": pl.Utf8,
        "r_multiple": pl.Float64,
    })


# ── Phase A ──────────────────────────────────────────────────────────────

def run_phase_a() -> pl.DataFrame:
    total = len(INDICATOR_UNIVERSE) * len(INDICATOR_SESSIONS) * len(SETUP_TYPES)
    print(f"[MOM-PhaseA] {total} combos "
          f"({len(INDICATOR_UNIVERSE)} assets x {len(INDICATOR_SESSIONS)} sessions x {len(SETUP_TYPES)} setups)")

    rows = []
    i = 0
    for symbol in INDICATOR_UNIVERSE:
        try:
            bars = _load_and_enrich_math(symbol)
        except FileNotFoundError:
            print(f"[MOM-PhaseA][SKIP] {symbol}: no data")
            continue
        friction = _friction_for(symbol)
        for setup_type in SETUP_TYPES:
            try:
                all_setups = detect_setups(bars, setup_type)
            except Exception as exc:
                print(f"[MOM-PhaseA][SKIP] {symbol}/{setup_type}: {exc}")
                continue
            for session in INDICATOR_SESSIONS:
                i += 1
                sigs = _filter_by_session(all_setups, session)
                if len(sigs) < 10:
                    continue
                cfg = BacktestConfig(
                    tp_atr_mult=PA_DEFAULT_TP, sl_atr_mult=PA_DEFAULT_SL,
                    session_end_hour_utc=_session_end_hour(session),
                    friction_r=friction,
                )
                trades = run_backtest(sigs, bars, setup_type, cfg, symbol)
                if len(trades) == 0:
                    continue
                m = compute_metrics(trades)
                rows.append({
                    "symbol": symbol, "tf": TF, "session": session,
                    "setup_type": setup_type,
                    "n_trades": m.n_trades, "wr": m.wr, "pf": m.profit_factor,
                    "expectancy_r": m.expectancy_r, "max_dd_r": m.max_dd_r,
                    "trades_per_year": m.trades_per_year,
                })
                if i % 50 == 0:
                    print(f"[MOM-PhaseA] {i}/{total} - {symbol}/{session}/{setup_type}")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    if not rows:
        print("[MOM-PhaseA] No results.")
        pl.DataFrame().write_parquet(REPORTS_DIR / "math_momentum_phase_a.parquet")
        (REPORTS_DIR / "math_momentum_phase_a.md").write_text(
            "# Math MOMENTUM Phase A\n\nNo combos produced trades.\n", encoding="utf-8")
        return pl.DataFrame()

    results = pl.DataFrame(rows)
    survivors = results.filter(
        (pl.col("trades_per_year") >= PA_MIN_TRADES_PER_YEAR)
        & (pl.col("wr") >= PA_MIN_WR)
        & (pl.col("pf") >= PA_MIN_PF)
    ).sort("expectancy_r", descending=True)

    results.write_parquet(REPORTS_DIR / "math_momentum_phase_a.parquet")
    survivors.write_parquet(REPORTS_DIR / "math_momentum_phase_a_survivors.parquet")
    (REPORTS_DIR / "math_momentum_phase_a.md").write_text(
        _render_phase_a_md(results, survivors), encoding="utf-8")
    print(f"[MOM-PhaseA] {len(results)} evaluated, {len(survivors)} passed gates")
    return survivors


def _render_phase_a_md(results: pl.DataFrame, survivors: pl.DataFrame) -> str:
    lines = [
        "# Math MOMENTUM - Phase A Report", "",
        f"- Combos evaluated: **{len(results)}**",
        f"- Passed gates: **{len(survivors)}**",
        f"- Gates: trades/year >= {PA_MIN_TRADES_PER_YEAR}, WR >= {PA_MIN_WR}, PF >= {PA_MIN_PF}",
        f"- TP/SL: {PA_DEFAULT_TP}xATR / {PA_DEFAULT_SL}xATR (momentum ratio)",
        "",
        "## Top 30 survivors",
        "",
        "| Symbol | Session | Setup | Trades | WR | PF | Exp (R) | MaxDD (R) | Trades/yr |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for r in survivors.head(30).iter_rows(named=True):
        lines.append(
            f"| {r['symbol']} | {r['session']} | {r['setup_type']} "
            f"| {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.2f} "
            f"| {r['expectancy_r']:.3f} | {r['max_dd_r']:.1f} | {r['trades_per_year']:.1f} |"
        )
    return "\n".join(lines) + "\n"


# ── Phase B ──────────────────────────────────────────────────────────────

def run_phase_b() -> pl.DataFrame:
    surv_path = REPORTS_DIR / "math_momentum_phase_a_survivors.parquet"
    if not surv_path.exists():
        raise FileNotFoundError(f"Run Phase-A first (missing {surv_path})")
    survivors = pl.read_parquet(surv_path)
    if len(survivors) == 0:
        print("[MOM-PhaseB] No Phase-A survivors.")
        pl.DataFrame().write_parquet(REPORTS_DIR / "math_momentum_phase_b.parquet")
        (REPORTS_DIR / "math_momentum_phase_b.md").write_text(
            "# Math MOMENTUM Phase B\n\nNo Phase-A survivors.\n", encoding="utf-8")
        return pl.DataFrame()

    rr_combos = [(tp, sl) for tp in PB_TP_GRID for sl in PB_SL_GRID]
    total = len(survivors) * len(rr_combos)
    print(f"[MOM-PhaseB] {len(survivors)} x {len(rr_combos)} = {total}")

    rows = []
    for surv in survivors.iter_rows(named=True):
        symbol, session, setup_type = surv["symbol"], surv["session"], surv["setup_type"]
        try:
            bars = _load_and_enrich_math(symbol)
        except FileNotFoundError:
            continue
        all_setups = detect_setups(bars, setup_type)
        sigs = _filter_by_session(all_setups, session)
        if len(sigs) < 10:
            continue
        friction = _friction_for(symbol)
        session_end = _session_end_hour(session)
        for tp_mult, sl_mult in rr_combos:
            cfg = BacktestConfig(
                tp_atr_mult=tp_mult, sl_atr_mult=sl_mult,
                session_end_hour_utc=session_end, friction_r=friction,
            )
            trades = run_backtest(sigs, bars, setup_type, cfg, symbol)
            if len(trades) == 0:
                continue
            m = compute_metrics(trades)
            if (m.trades_per_year < PB_MIN_TRADES_PER_YEAR
                    or m.profit_factor < PB_MIN_PF
                    or m.expectancy_r < PB_MIN_EXPECTANCY
                    or m.max_dd_r > PB_MAX_DD_R):
                continue
            rows.append({
                "symbol": symbol, "tf": TF, "session": session,
                "setup_type": setup_type,
                "tp_atr_mult": tp_mult, "sl_atr_mult": sl_mult,
                "n_trades": m.n_trades, "wr": m.wr, "pf": m.profit_factor,
                "expectancy_r": m.expectancy_r, "max_dd_r": m.max_dd_r,
                "trades_per_year": m.trades_per_year,
            })

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    if not rows:
        print("[MOM-PhaseB] 0 survivors passed gates.")
        pl.DataFrame().write_parquet(REPORTS_DIR / "math_momentum_phase_b.parquet")
        (REPORTS_DIR / "math_momentum_phase_b.md").write_text(
            "# Math MOMENTUM Phase B\n\n0 survivors passed R:R gates.\n", encoding="utf-8")
        return pl.DataFrame()

    phase_b = pl.DataFrame(rows).sort("expectancy_r", descending=True)
    phase_b.write_parquet(REPORTS_DIR / "math_momentum_phase_b.parquet")
    (REPORTS_DIR / "math_momentum_phase_b.md").write_text(
        _render_phase_b_md(phase_b), encoding="utf-8")
    print(f"[MOM-PhaseB] {len(phase_b)} passed R:R gates")
    return phase_b


def _render_phase_b_md(phase_b: pl.DataFrame) -> str:
    lines = [
        "# Math MOMENTUM - Phase B Report", "",
        f"- Survivors: **{len(phase_b)}**",
        f"- Gates: trades/yr>={PB_MIN_TRADES_PER_YEAR}, PF>={PB_MIN_PF}, "
        f"exp>={PB_MIN_EXPECTANCY}R, MaxDD<={PB_MAX_DD_R}R",
        "",
        "| Symbol | Session | Setup | TP | SL | Trades | WR | PF | Exp(R) | MaxDD(R) | T/yr |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in phase_b.iter_rows(named=True):
        lines.append(
            f"| {r['symbol']} | {r['session']} | {r['setup_type']} "
            f"| {r['tp_atr_mult']} | {r['sl_atr_mult']} "
            f"| {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.2f} "
            f"| {r['expectancy_r']:.3f} | {r['max_dd_r']:.1f} | {r['trades_per_year']:.1f} |"
        )
    return "\n".join(lines) + "\n"


# ── Phase C ──────────────────────────────────────────────────────────────

def run_phase_c() -> pl.DataFrame:
    pb_path = REPORTS_DIR / "math_momentum_phase_b.parquet"
    if not pb_path.exists():
        raise FileNotFoundError(f"Run Phase-B first (missing {pb_path})")
    phase_b = pl.read_parquet(pb_path)
    if len(phase_b) == 0:
        print("[MOM-PhaseC] No Phase-B survivors.")
        _write_empty_final()
        return pl.DataFrame()

    print(f"[MOM-PhaseC] Validating {len(phase_b)} Phase-B survivors")
    final_rows = []

    for surv in phase_b.iter_rows(named=True):
        symbol = surv["symbol"]; session = surv["session"]; setup_type = surv["setup_type"]
        tp_mult = surv["tp_atr_mult"]; sl_mult = surv["sl_atr_mult"]
        try:
            bars = _load_and_enrich_math(symbol)
        except FileNotFoundError:
            continue
        all_setups = detect_setups(bars, setup_type)
        sigs = _filter_by_session(all_setups, session)
        if len(sigs) < 10:
            continue
        cfg = BacktestConfig(
            tp_atr_mult=tp_mult, sl_atr_mult=sl_mult,
            session_end_hour_utc=_session_end_hour(session),
            friction_r=_friction_for(symbol),
        )
        trades = run_backtest(sigs, bars, setup_type, cfg, symbol)
        if len(trades) < 20:
            continue
        wf = walk_forward_wr(trades, WF_IS_MONTHS, WF_OOS_MONTHS)
        mc = monte_carlo_ruin(trades, risk_pct=0.02, initial_balance=10_000)
        decay = decay_slope_ratio(trades, last_months=6)
        if wf < PC_MIN_WF_RATIO or mc > PC_MAX_MC_RUIN or decay < PC_MIN_DECAY:
            continue
        m = compute_metrics(trades)
        final_rows.append({
            "symbol": symbol, "tf": TF, "session": session,
            "setup_type": setup_type,
            "tp_atr_mult": tp_mult, "sl_atr_mult": sl_mult,
            "n_trades": m.n_trades, "wr": m.wr, "pf": m.profit_factor,
            "expectancy_r": m.expectancy_r, "max_dd_r": m.max_dd_r,
            "trades_per_year": m.trades_per_year,
            "wf_ratio": wf, "mc_ruin": mc, "decay_ratio": decay,
        })

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    if not final_rows:
        print("[MOM-PhaseC] 0 passed robustness gates.")
        _write_empty_final()
        return pl.DataFrame()

    final = pl.DataFrame(final_rows).sort("expectancy_r", descending=True)
    (REPORTS_DIR / "Math_Momentum_Final.md").write_text(_render_final_md(final), encoding="utf-8")
    _export_json(final, REPORTS_DIR / "math_momentum_strategies.json")
    print(f"[MOM-PhaseC] {len(final)} passed ALL gates")
    try:
        preview = final.select(["symbol", "session", "setup_type", "tp_atr_mult", "sl_atr_mult",
                                "wr", "pf", "expectancy_r"]).head(10)
        print(preview.write_csv(separator="|"))
    except Exception:
        pass
    return final


def _render_final_md(final: pl.DataFrame) -> str:
    lines = [
        "# Math MOMENTUM - Final Strategies", "",
        f"- Passed ALL gates (WF/MC/decay): **{len(final)}**",
        f"- Gates: WF>={PC_MIN_WF_RATIO}, MC<={PC_MAX_MC_RUIN}, decay>={PC_MIN_DECAY}",
        "",
        "| Symbol | Session | Setup | TP | SL | Trades | WR | PF | Exp(R) | T/yr | WF | MC | Decay |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in final.iter_rows(named=True):
        lines.append(
            f"| {r['symbol']} | {r['session']} | {r['setup_type']} "
            f"| {r['tp_atr_mult']} | {r['sl_atr_mult']} "
            f"| {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.2f} "
            f"| {r['expectancy_r']:.3f} | {r['trades_per_year']:.1f} "
            f"| {r['wf_ratio']:.2f} | {r['mc_ruin']:.3f} | {r['decay_ratio']:.2f} |"
        )
    return "\n".join(lines) + "\n"


def _export_json(final: pl.DataFrame, path: Path) -> None:
    records = []
    for r in final.iter_rows(named=True):
        records.append({
            "symbol": r["symbol"], "tf": r["tf"], "session": r["session"],
            "setup_type": r["setup_type"],
            "tp_atr_mult": float(r["tp_atr_mult"]),
            "sl_atr_mult": float(r["sl_atr_mult"]),
            "metrics": {
                "n_trades": int(r["n_trades"]),
                "wr": float(r["wr"]),
                "pf": float(r["pf"]),
                "expectancy_r": float(r["expectancy_r"]),
                "max_dd_r": float(r["max_dd_r"]),
                "trades_per_year": float(r["trades_per_year"]),
                "wf_ratio": float(r["wf_ratio"]),
                "mc_ruin": float(r["mc_ruin"]),
                "decay_ratio": float(r["decay_ratio"]),
            },
        })
    path.write_text(json.dumps(records, indent=2), encoding="utf-8")


def _write_empty_final() -> None:
    (REPORTS_DIR / "Math_Momentum_Final.md").write_text(
        "# Math MOMENTUM Final\n\nNo strategies passed all gates.\n", encoding="utf-8")
    (REPORTS_DIR / "math_momentum_strategies.json").write_text("[]", encoding="utf-8")


# ── Entry point ──────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(description="Math MOMENTUM discovery pipeline (M15)")
    ap.add_argument("--phase", choices=("a", "b", "c", "all"), default="all")
    args = ap.parse_args()

    if args.phase in ("a", "all"):
        run_phase_a()
    if args.phase in ("b", "all"):
        run_phase_b()
    if args.phase in ("c", "all"):
        run_phase_c()


if __name__ == "__main__":
    main()
