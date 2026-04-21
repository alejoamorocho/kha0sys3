"""Full-math discovery pipeline — entries + direction guards + exits ALL math.

Phase A : (symbol × session × math-signal × guard-subset) with hard-SL + TIME_STOP only.
Phase B : For top-100 Phase-A entries, search 1/2/3-exit combos from 10-style math pool.
Phase C : WF + MC + decay on Phase-B survivors.

ATR is allowed only as hard-SL scale.

Usage:
    python -m src.engine.run_full_math --phase {a,b,c,all}
"""
from __future__ import annotations

import argparse
import itertools
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import polars as pl

from src.domain.constants import (
    INDICATOR_UNIVERSE,
    INDICATOR_SESSIONS,
    FRICTION_FX,
    FRICTION_INDEX,
    INDEX_SYMBOLS,
    WF_IS_MONTHS,
    WF_OOS_MONTHS,
)
from src.application.signal_generator import SignalGenerator
from src.engine.indicator_validation import (
    compute_metrics,
    walk_forward_wr,
    monte_carlo_ruin,
    decay_slope_ratio,
)
from src.engine.run_math_discovery import _load_and_enrich_math
from src.engine.run_indicator_discovery import _filter_by_session

REPORTS_DIR = Path("reports")
TF = "M15"

# ── Math-only entry signals (17) ────────────────────────────────────────────
MATH_SIGNALS = (
    "ZSCORE_REV", "VELOCITY_REV", "ACCEL_SHOCK", "KALMAN_INNOV_REV", "OLS_RESIDUAL_REV",
    "CURVATURE_PEAK", "VWAP_AREA_EXTREME", "MEANREV_AREA_EXTREME", "REGRESSION_BREAKOUT",
    "SKEW_REGIME_REV",
    "FRAC_DIFF_REV", "SHANNON_DROP_TREND", "HURST_MEANREV", "HURST_TREND",
    "SPECTRAL_TREND", "KAMA_CROSS", "GARCH_SPIKE_FADE",
)

# Family mapping for REGIME_COHERENCE guard.
MATH_SIGNAL_FAMILY: dict[str, str] = {
    # Mean-reversion (need hurst_rs_100 < 0.5)
    "ZSCORE_REV": "meanrev",
    "FRAC_DIFF_REV": "meanrev",
    "HURST_MEANREV": "meanrev",
    "MEANREV_AREA_EXTREME": "meanrev",
    "VWAP_AREA_EXTREME": "meanrev",
    "OLS_RESIDUAL_REV": "meanrev",
    "GARCH_SPIKE_FADE": "meanrev",
    "SKEW_REGIME_REV": "meanrev",
    "KALMAN_INNOV_REV": "meanrev",
    # Momentum (need hurst_rs_100 >= 0.5)
    "HURST_TREND": "momentum",
    "SPECTRAL_TREND": "momentum",
    "KAMA_CROSS": "momentum",
    "SHANNON_DROP_TREND": "momentum",
    "REGRESSION_BREAKOUT": "momentum",
    # Structural (no regime filter)
    "VELOCITY_REV": "structural",
    "ACCEL_SHOCK": "structural",
    "CURVATURE_PEAK": "structural",
}

# ── Guards ──────────────────────────────────────────────────────────────────
GUARD_NAMES = ("VELOCITY_DECEL", "KALMAN_INNOV_PEAK", "CURVATURE_INFLECTION", "REGIME_COHERENCE")


def _guard_subsets() -> list[tuple[str, ...]]:
    """All subsets of size 0..3 from the 4 guards = 15 combos."""
    out: list[tuple[str, ...]] = []
    for k in range(0, 4):
        for combo in itertools.combinations(GUARD_NAMES, k):
            out.append(combo)
    return out


def _precompute_guard_columns(bars: pl.DataFrame) -> pl.DataFrame:
    """Compute per-bar boolean guard helper columns (time-indexed).

    For each guard we emit separate LONG/SHORT masks since they depend on direction.
    """
    # Kalman innov: |innov[t]| < |innov[t-1]| AND |innov[t-1]| is local max over last 5 bars.
    innov_abs = pl.col("kalman_innovation").abs()
    innov_abs_lag = innov_abs.shift(1)
    # local max of innov_abs at t-1: greater than previous 4 values [t-5..t-2]
    is_local_max_prev = (
        (innov_abs_lag > innov_abs.shift(2))
        & (innov_abs_lag > innov_abs.shift(3))
        & (innov_abs_lag > innov_abs.shift(4))
        & (innov_abs_lag > innov_abs.shift(5))
    )
    kalman_peak_ok = (innov_abs < innov_abs_lag) & is_local_max_prev

    # Curvature inflection
    curv_infl_long = (pl.col("curvature_10").shift(1) <= 0) & (pl.col("curvature_10") > 0)
    curv_infl_short = (pl.col("curvature_10").shift(1) >= 0) & (pl.col("curvature_10") < 0)

    # Velocity decel: LONG needs accel > 0 (decel of down move); SHORT needs accel < 0.
    accel_pos = pl.col("accel_10") > 0
    accel_neg = pl.col("accel_10") < 0

    # Regime
    hurst_meanrev = pl.col("hurst_rs_100") < 0.5
    hurst_momentum = pl.col("hurst_rs_100") >= 0.5

    return bars.with_columns([
        kalman_peak_ok.alias("_g_kalman_peak"),
        curv_infl_long.alias("_g_curv_long"),
        curv_infl_short.alias("_g_curv_short"),
        accel_pos.alias("_g_decel_long"),
        accel_neg.alias("_g_decel_short"),
        hurst_meanrev.alias("_g_hurst_mr"),
        hurst_momentum.alias("_g_hurst_mo"),
    ])


def _apply_guards_to_signals(
    signals: pl.DataFrame,
    bars_with_guards: pl.DataFrame,
    guards: tuple[str, ...],
    signal_type: str,
) -> pl.DataFrame:
    """Apply guard subset as AND filter. Signals joined to bars via time."""
    if len(signals) == 0:
        return signals
    if not guards:
        return signals

    family = MATH_SIGNAL_FAMILY.get(signal_type, "structural")
    helper_cols = ["time", "_g_kalman_peak", "_g_curv_long", "_g_curv_short",
                   "_g_decel_long", "_g_decel_short", "_g_hurst_mr", "_g_hurst_mo"]
    ctx = bars_with_guards.select(helper_cols)
    joined = signals.join(ctx, on="time", how="left")

    mask = pl.lit(True)
    for g in guards:
        if g == "VELOCITY_DECEL":
            m = pl.when(pl.col("direction") == "LONG").then(pl.col("_g_decel_long")) \
                  .otherwise(pl.col("_g_decel_short"))
            mask = mask & m.fill_null(False)
        elif g == "KALMAN_INNOV_PEAK":
            mask = mask & pl.col("_g_kalman_peak").fill_null(False)
        elif g == "CURVATURE_INFLECTION":
            m = pl.when(pl.col("direction") == "LONG").then(pl.col("_g_curv_long")) \
                  .otherwise(pl.col("_g_curv_short"))
            mask = mask & m.fill_null(False)
        elif g == "REGIME_COHERENCE":
            if family == "meanrev":
                mask = mask & pl.col("_g_hurst_mr").fill_null(False)
            elif family == "momentum":
                mask = mask & pl.col("_g_hurst_mo").fill_null(False)
            # structural: no filter
        else:
            raise ValueError(f"Unknown guard: {g}")

    return joined.filter(mask).select(signals.columns)


# ── Exits ───────────────────────────────────────────────────────────────────
EXIT_STYLES = (
    "VELOCITY_FLIP",
    "ACCEL_ZERO",
    "OLS_RESID_ZERO",
    "MEANREV_AREA_ZERO",
    "KALMAN_STATE_CROSS",
    "KAMA_CROSS_EXIT",
    "ZSCORE_NEUTRAL",
    "CURVATURE_FLIP",
    "HURST_REGIME_CHANGE",
    "SPECTRAL_DROP",
)


def _exit_triggered(style: str, prev_row: dict, curr_row: dict, direction: str) -> bool:
    """Check whether an exit condition fires on curr bar (given prev bar state).

    Convention: all crosses are symmetric (trigger regardless of direction),
    except VELOCITY_FLIP and CURVATURE_FLIP which need sign change. Style-based
    OR pool: first-to-fire wins in the backtester.
    """
    def g(row: dict, key: str):
        return row.get(key)

    p = prev_row
    c = curr_row

    def cross(key: str, level: float) -> bool:
        a, b = g(p, key), g(c, key)
        if a is None or b is None:
            return False
        return (a - level) * (b - level) < 0 or (b == level and a != level)

    if style == "VELOCITY_FLIP":
        a, b = g(p, "velocity_10"), g(c, "velocity_10")
        if a is None or b is None:
            return False
        return a * b < 0
    if style == "ACCEL_ZERO":
        return cross("accel_10", 0.0)
    if style == "OLS_RESID_ZERO":
        return cross("ols_resid_z_30", 0.0)
    if style == "MEANREV_AREA_ZERO":
        return cross("meanrev_area_50", 0.0)
    if style == "KALMAN_STATE_CROSS":
        # close crosses through kalman_state
        pa, pb = g(p, "close"), g(c, "close")
        ka, kb = g(p, "kalman_state"), g(c, "kalman_state")
        if None in (pa, pb, ka, kb):
            return False
        return (pa - ka) * (pb - kb) < 0
    if style == "KAMA_CROSS_EXIT":
        pa, pb = g(p, "close"), g(c, "close")
        ka, kb = g(p, "kama_10"), g(c, "kama_10")
        if None in (pa, pb, ka, kb):
            return False
        return (pa - ka) * (pb - kb) < 0
    if style == "ZSCORE_NEUTRAL":
        return cross("zscore_30", 0.0)
    if style == "CURVATURE_FLIP":
        a, b = g(p, "curvature_10"), g(c, "curvature_10")
        if a is None or b is None:
            return False
        return a * b < 0
    if style == "HURST_REGIME_CHANGE":
        return cross("hurst_rs_100", 0.5)
    if style == "SPECTRAL_DROP":
        a, b = g(p, "spectral_ratio_64"), g(c, "spectral_ratio_64")
        if a is None or b is None:
            return False
        return a >= 1.5 and b < 1.5
    raise ValueError(f"Unknown exit style: {style}")


# ── Backtester with math-only exits ─────────────────────────────────────────

_EXIT_COLS = (
    "velocity_10", "accel_10", "ols_resid_z_30", "meanrev_area_50",
    "kalman_state", "kama_10", "zscore_30", "curvature_10",
    "hurst_rs_100", "spectral_ratio_64", "close",
)


def _run_full_math_backtest(
    signals: pl.DataFrame,
    bars: pl.DataFrame,
    exits: tuple[str, ...],
    hard_sl_atr: float,
    session_end_hour: int,
    friction_r: float,
) -> pl.DataFrame:
    """Event-driven backtest: hard-SL (ATR) + math-only exit pool + session TIME_STOP.

    Risk per R = hard_sl_atr * ATR.
    """
    if len(signals) == 0:
        return _empty_trades()

    deduped = signals.with_columns([
        pl.col("time").dt.date().alias("_date")
    ]).sort("time").unique(
        subset=["symbol", "signal_type", "_date"], keep="first"
    ).drop("_date")

    bars_sorted = bars.sort("time")
    bar_times = bars_sorted["time"].to_list()
    bar_highs = bars_sorted["high"].to_list()
    bar_lows = bars_sorted["low"].to_list()
    bar_closes = bars_sorted["close"].to_list()

    # Pre-extract exit helper columns as list-of-dicts for speed.
    exit_cols_present = [c for c in _EXIT_COLS if c in bars_sorted.columns]
    exit_frame = bars_sorted.select(exit_cols_present).to_dicts()

    time_to_idx = {t: i for i, t in enumerate(bar_times)}

    results = []
    for sig in deduped.iter_rows(named=True):
        atr = sig.get("atr_14")
        if atr is None or atr <= 0:
            continue
        entry = sig["close"]
        direction = sig["direction"]
        if direction == "LONG":
            sl = entry - hard_sl_atr * atr
        else:
            sl = entry + hard_sl_atr * atr

        start_idx = time_to_idx.get(sig["time"])
        if start_idx is None:
            continue

        exit_reason = None
        exit_price = None
        exit_time = None
        signal_date = sig["time"].date()

        for i in range(start_idx + 1, len(bar_times)):
            bt = bar_times[i]
            # Time stop
            if bt.date() > signal_date or bt.hour >= session_end_hour:
                exit_reason = "TIME_STOP"
                exit_price = bar_closes[i - 1]
                exit_time = bar_times[i - 1]
                break
            hi = bar_highs[i]
            lo = bar_lows[i]
            # Hard SL first
            if direction == "LONG":
                if lo <= sl:
                    exit_reason, exit_price, exit_time = "SL", sl, bt
                    break
            else:
                if hi >= sl:
                    exit_reason, exit_price, exit_time = "SL", sl, bt
                    break
            # Math exits (OR, first wins)
            if exits:
                prev_row = exit_frame[i - 1]
                curr_row = exit_frame[i]
                fired = None
                for style in exits:
                    if _exit_triggered(style, prev_row, curr_row, direction):
                        fired = style
                        break
                if fired is not None:
                    exit_reason = fired
                    exit_price = bar_closes[i]
                    exit_time = bt
                    break
        else:
            exit_reason = "TIME_STOP"
            exit_price = bar_closes[-1]
            exit_time = bar_times[-1]

        risk_per_unit = hard_sl_atr * atr
        if direction == "LONG":
            pnl = exit_price - entry
        else:
            pnl = entry - exit_price
        r_gross = pnl / risk_per_unit if risk_per_unit > 0 else 0.0
        r_net = r_gross - friction_r

        results.append({
            "time": sig["time"],
            "symbol": sig["symbol"],
            "signal_type": sig["signal_type"],
            "direction": direction,
            "entry_price": entry,
            "sl_price": sl,
            "exit_time": exit_time,
            "exit_price": exit_price,
            "exit_reason": exit_reason,
            "r_multiple": r_net,
        })

    if not results:
        return _empty_trades()
    return pl.DataFrame(results)


def _empty_trades() -> pl.DataFrame:
    return pl.DataFrame(schema={
        "time": pl.Datetime, "symbol": pl.Utf8, "signal_type": pl.Utf8, "direction": pl.Utf8,
        "entry_price": pl.Float64, "sl_price": pl.Float64,
        "exit_time": pl.Datetime, "exit_price": pl.Float64, "exit_reason": pl.Utf8,
        "r_multiple": pl.Float64,
    })


# ── Gates ───────────────────────────────────────────────────────────────────

PA_MIN_TRADES_PER_YEAR = 30
PA_MIN_WR = 0.55
HARD_SL_ATR = 3.0

PB_MIN_TRADES_PER_YEAR = 30
PB_MIN_PF = 1.20
PB_MIN_EXPECTANCY = 0.05
PB_MAX_DD_R = 25.0

PC_MIN_WF_RATIO = 0.80
PC_MAX_MC_RUIN = 0.02
PC_MIN_DECAY = 0.60


def _friction_for(symbol: str) -> float:
    return FRICTION_INDEX if symbol in INDEX_SYMBOLS else FRICTION_FX


def _session_end_hour(session: str) -> int:
    return INDICATOR_SESSIONS[session][1]


# ── Phase A ─────────────────────────────────────────────────────────────────

def run_phase_a() -> pl.DataFrame:
    subsets = _guard_subsets()
    total = len(INDICATOR_UNIVERSE) * len(INDICATOR_SESSIONS) * len(MATH_SIGNALS) * len(subsets)
    print(f"[FM-A] {total} combos  ({len(INDICATOR_UNIVERSE)} sym x "
          f"{len(INDICATOR_SESSIONS)} sess x {len(MATH_SIGNALS)} sig x {len(subsets)} guard-sets)")

    rows = []
    i = 0
    for symbol in INDICATOR_UNIVERSE:
        try:
            bars = _load_and_enrich_math(symbol)
        except FileNotFoundError:
            print(f"[FM-A][SKIP] {symbol}: no data file")
            continue
        bars_g = _precompute_guard_columns(bars)
        friction = _friction_for(symbol)
        for signal_type in MATH_SIGNALS:
            try:
                raw_signals = SignalGenerator.generate(bars, signal_type, symbol)
            except Exception as exc:
                print(f"[FM-A][SKIP] {symbol} {signal_type}: {exc}")
                i += len(INDICATOR_SESSIONS) * len(subsets)
                continue
            for session in INDICATOR_SESSIONS:
                sess_sigs = _filter_by_session(raw_signals, session)
                for guards in subsets:
                    i += 1
                    if len(sess_sigs) < 20:
                        continue
                    sigs = _apply_guards_to_signals(sess_sigs, bars_g, guards, signal_type)
                    if len(sigs) < 20:
                        if i % 1000 == 0:
                            print(f"[FM-A] {i}/{total} — {symbol}/{session}/{signal_type}/{guards}")
                        continue
                    trades = _run_full_math_backtest(
                        sigs, bars, exits=(),  # Phase A: no math exits
                        hard_sl_atr=HARD_SL_ATR,
                        session_end_hour=_session_end_hour(session),
                        friction_r=friction,
                    )
                    if len(trades) == 0:
                        if i % 1000 == 0:
                            print(f"[FM-A] {i}/{total} — {symbol}/{session}/{signal_type}/{guards}")
                        continue
                    m = compute_metrics(trades)
                    rows.append({
                        "symbol": symbol, "session": session, "signal_type": signal_type,
                        "guards": list(guards),
                        "n_guards": len(guards),
                        "n_trades": m.n_trades, "wr": m.wr,
                        "pf": m.profit_factor, "expectancy_r": m.expectancy_r,
                        "max_dd_r": m.max_dd_r, "trades_per_year": m.trades_per_year,
                    })
                    if i % 1000 == 0:
                        print(f"[FM-A] {i}/{total} — kept={len(rows)} — last {symbol}/{session}/{signal_type}/{guards}")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    if not rows:
        print("[FM-A] No combos produced trades.")
        pl.DataFrame().write_parquet(REPORTS_DIR / "full_math_phase_a.parquet")
        (REPORTS_DIR / "full_math_phase_a.md").write_text(
            "# Full-Math Phase A\n\nNo combos produced trades.\n", encoding="utf-8"
        )
        return pl.DataFrame()

    results = pl.DataFrame(rows)
    survivors = results.filter(
        (pl.col("trades_per_year") >= PA_MIN_TRADES_PER_YEAR)
        & (pl.col("wr") >= PA_MIN_WR)
    ).sort(["wr", "expectancy_r"], descending=[True, True]).head(100)

    results.write_parquet(REPORTS_DIR / "full_math_phase_a.parquet")
    survivors.write_parquet(REPORTS_DIR / "full_math_phase_a_survivors.parquet")
    (REPORTS_DIR / "full_math_phase_a.md").write_text(
        _render_phase_a_md(results, survivors), encoding="utf-8"
    )
    print(f"[FM-A] {len(results)} evaluated, {len(survivors)} top-100 kept")
    return survivors


def _render_phase_a_md(results: pl.DataFrame, survivors: pl.DataFrame) -> str:
    lines = [
        "# Full-Math Discovery — Phase A",
        "",
        f"- Combos evaluated: **{len(results)}**",
        f"- Top-100 kept: **{len(survivors)}**",
        f"- Gates: trades/year >= {PA_MIN_TRADES_PER_YEAR}, WR >= {PA_MIN_WR}",
        f"- Hard SL: {HARD_SL_ATR} x ATR; exits: TIME_STOP only",
        "",
        "## Top 30 survivors",
        "",
        "| Symbol | Session | Signal | Guards | Trades | WR | PF | Exp (R) | MaxDD (R) |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for r in survivors.head(30).iter_rows(named=True):
        guards = ",".join(r["guards"]) if r["guards"] else "-"
        lines.append(
            f"| {r['symbol']} | {r['session']} | {r['signal_type']} | {guards} "
            f"| {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.2f} "
            f"| {r['expectancy_r']:.3f} | {r['max_dd_r']:.1f} |"
        )
    return "\n".join(lines) + "\n"


# ── Phase B ─────────────────────────────────────────────────────────────────

def _exit_combos() -> list[tuple[str, ...]]:
    out: list[tuple[str, ...]] = []
    for k in (1, 2, 3):
        for combo in itertools.combinations(EXIT_STYLES, k):
            out.append(combo)
    return out


def run_phase_b() -> pl.DataFrame:
    surv_path = REPORTS_DIR / "full_math_phase_a_survivors.parquet"
    if not surv_path.exists():
        raise FileNotFoundError(f"Run Phase-A first (missing {surv_path})")
    survivors = pl.read_parquet(surv_path)
    if len(survivors) == 0:
        print("[FM-B] No Phase-A survivors.")
        pl.DataFrame().write_parquet(REPORTS_DIR / "full_math_phase_b.parquet")
        (REPORTS_DIR / "full_math_phase_b.md").write_text(
            "# Full-Math Phase B\n\nNo Phase-A survivors.\n", encoding="utf-8"
        )
        return pl.DataFrame()

    combos = _exit_combos()
    total = len(survivors) * len(combos)
    print(f"[FM-B] {len(survivors)} entries x {len(combos)} exit-sets = {total}")
    rows = []
    i = 0

    # Cache per-symbol bars / guards
    bars_cache: dict[str, tuple[pl.DataFrame, pl.DataFrame]] = {}

    for surv in survivors.iter_rows(named=True):
        symbol, session, signal_type = surv["symbol"], surv["session"], surv["signal_type"]
        guards = tuple(surv["guards"])
        if symbol not in bars_cache:
            try:
                b = _load_and_enrich_math(symbol)
                bars_cache[symbol] = (b, _precompute_guard_columns(b))
            except FileNotFoundError:
                continue
        bars, bars_g = bars_cache[symbol]
        try:
            raw_signals = SignalGenerator.generate(bars, signal_type, symbol)
        except Exception:
            continue
        sess_sigs = _filter_by_session(raw_signals, session)
        sigs = _apply_guards_to_signals(sess_sigs, bars_g, guards, signal_type)
        if len(sigs) < 20:
            i += len(combos)
            continue
        friction = _friction_for(symbol)
        session_end = _session_end_hour(session)

        for exits in combos:
            i += 1
            trades = _run_full_math_backtest(
                sigs, bars, exits=exits,
                hard_sl_atr=HARD_SL_ATR,
                session_end_hour=session_end, friction_r=friction,
            )
            if len(trades) == 0:
                if i % 1000 == 0:
                    print(f"[FM-B] {i}/{total} kept={len(rows)}")
                continue
            m = compute_metrics(trades)
            if (m.trades_per_year < PB_MIN_TRADES_PER_YEAR
                    or m.profit_factor < PB_MIN_PF
                    or m.expectancy_r < PB_MIN_EXPECTANCY
                    or m.max_dd_r > PB_MAX_DD_R):
                if i % 1000 == 0:
                    print(f"[FM-B] {i}/{total} kept={len(rows)}")
                continue
            rows.append({
                "symbol": symbol, "session": session, "signal_type": signal_type,
                "guards": list(guards),
                "exits": list(exits),
                "n_exits": len(exits),
                "n_trades": m.n_trades, "wr": m.wr, "pf": m.profit_factor,
                "expectancy_r": m.expectancy_r, "max_dd_r": m.max_dd_r,
                "trades_per_year": m.trades_per_year,
            })
            if i % 1000 == 0:
                print(f"[FM-B] {i}/{total} kept={len(rows)}")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    if not rows:
        print("[FM-B] 0 strategies passed gates.")
        pl.DataFrame().write_parquet(REPORTS_DIR / "full_math_phase_b.parquet")
        (REPORTS_DIR / "full_math_phase_b.md").write_text(
            "# Full-Math Phase B\n\n0 strategies passed gates.\n", encoding="utf-8"
        )
        return pl.DataFrame()

    phase_b = pl.DataFrame(rows).sort("expectancy_r", descending=True)
    phase_b.write_parquet(REPORTS_DIR / "full_math_phase_b.parquet")
    (REPORTS_DIR / "full_math_phase_b.md").write_text(
        _render_phase_b_md(phase_b), encoding="utf-8"
    )
    print(f"[FM-B] {len(phase_b)} strategies passed")
    return phase_b


def _render_phase_b_md(phase_b: pl.DataFrame) -> str:
    lines = [
        "# Full-Math Discovery — Phase B",
        "",
        f"- Strategies passing gates: **{len(phase_b)}**",
        f"- Gates: trades/year >= {PB_MIN_TRADES_PER_YEAR}, PF >= {PB_MIN_PF}, "
        f"exp >= {PB_MIN_EXPECTANCY}R, MaxDD <= {PB_MAX_DD_R}R",
        "",
        "## Top 30 by expectancy",
        "",
        "| Symbol | Session | Signal | Guards | Exits | Trades | WR | PF | Exp (R) | MaxDD |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in phase_b.head(30).iter_rows(named=True):
        guards = ",".join(r["guards"]) if r["guards"] else "-"
        exits = ",".join(r["exits"])
        lines.append(
            f"| {r['symbol']} | {r['session']} | {r['signal_type']} | {guards} | {exits} "
            f"| {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.2f} "
            f"| {r['expectancy_r']:.3f} | {r['max_dd_r']:.1f} |"
        )
    return "\n".join(lines) + "\n"


# ── Phase C ─────────────────────────────────────────────────────────────────

def run_phase_c() -> pl.DataFrame:
    pb_path = REPORTS_DIR / "full_math_phase_b.parquet"
    if not pb_path.exists():
        raise FileNotFoundError(f"Run Phase-B first (missing {pb_path})")
    phase_b = pl.read_parquet(pb_path)
    if len(phase_b) == 0:
        print("[FM-C] No Phase-B survivors.")
        _write_empty_final()
        return pl.DataFrame()

    print(f"[FM-C] Validating {len(phase_b)} Phase-B survivors")
    rows = []
    kill_diag = {"wf": 0, "mc": 0, "decay": 0, "ntrades": 0}

    bars_cache: dict[str, tuple[pl.DataFrame, pl.DataFrame]] = {}

    for surv in phase_b.iter_rows(named=True):
        symbol = surv["symbol"]; session = surv["session"]
        signal_type = surv["signal_type"]
        guards = tuple(surv["guards"]); exits = tuple(surv["exits"])
        if symbol not in bars_cache:
            try:
                b = _load_and_enrich_math(symbol)
                bars_cache[symbol] = (b, _precompute_guard_columns(b))
            except FileNotFoundError:
                continue
        bars, bars_g = bars_cache[symbol]
        try:
            raw_signals = SignalGenerator.generate(bars, signal_type, symbol)
        except Exception:
            continue
        sess_sigs = _filter_by_session(raw_signals, session)
        sigs = _apply_guards_to_signals(sess_sigs, bars_g, guards, signal_type)
        if len(sigs) < 20:
            continue
        trades = _run_full_math_backtest(
            sigs, bars, exits=exits,
            hard_sl_atr=HARD_SL_ATR,
            session_end_hour=_session_end_hour(session),
            friction_r=_friction_for(symbol),
        )
        if len(trades) < 20:
            kill_diag["ntrades"] += 1
            continue

        wf = walk_forward_wr(trades, WF_IS_MONTHS, WF_OOS_MONTHS)
        mc = monte_carlo_ruin(trades, risk_pct=0.02, initial_balance=10_000)
        decay = decay_slope_ratio(trades, last_months=6)

        if wf < PC_MIN_WF_RATIO:
            kill_diag["wf"] += 1; continue
        if mc > PC_MAX_MC_RUIN:
            kill_diag["mc"] += 1; continue
        if decay < PC_MIN_DECAY:
            kill_diag["decay"] += 1; continue

        m = compute_metrics(trades)
        rows.append({
            "symbol": symbol, "session": session, "signal_type": signal_type,
            "guards": list(guards), "exits": list(exits),
            "n_trades": m.n_trades, "wr": m.wr, "pf": m.profit_factor,
            "expectancy_r": m.expectancy_r, "max_dd_r": m.max_dd_r,
            "trades_per_year": m.trades_per_year,
            "wf_ratio": wf, "mc_ruin": mc, "decay_ratio": decay,
        })

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    if not rows:
        print(f"[FM-C] 0 passed. Kill diag: {kill_diag}")
        _write_empty_final(kill_diag)
        return pl.DataFrame()

    final = pl.DataFrame(rows).sort("expectancy_r", descending=True)
    (REPORTS_DIR / "Full_Math_Final.md").write_text(
        _render_final_md(final, kill_diag), encoding="utf-8"
    )
    # JSON
    payload = []
    for r in final.iter_rows(named=True):
        payload.append({
            "symbol": r["symbol"], "session": r["session"],
            "signal_type": r["signal_type"],
            "guards": r["guards"], "exits": r["exits"],
            "hard_sl_atr": HARD_SL_ATR,
            "wr": r["wr"], "pf": r["pf"], "expectancy_r": r["expectancy_r"],
            "wf_ratio": r["wf_ratio"], "mc_ruin": r["mc_ruin"], "decay_ratio": r["decay_ratio"],
        })
    (REPORTS_DIR / "full_math_strategies.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )
    print(f"[FM-C] {len(final)} passed all gates. Kill diag: {kill_diag}")
    return final


def _render_final_md(final: pl.DataFrame, kill_diag: dict) -> str:
    lines = [
        "# Full-Math Discovery — Final",
        "",
        f"- Strategies passing ALL gates: **{len(final)}**",
        f"- Gates: WF >= {PC_MIN_WF_RATIO}, MC ruin <= {PC_MAX_MC_RUIN}, "
        f"decay >= {PC_MIN_DECAY}",
        f"- Kill diagnostic (from Phase-B set): {kill_diag}",
        "",
        "| Symbol | Session | Signal | Guards | Exits | Trades | WR | PF | Exp | WF | MC | Decay |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in final.iter_rows(named=True):
        guards = ",".join(r["guards"]) if r["guards"] else "-"
        exits = ",".join(r["exits"])
        lines.append(
            f"| {r['symbol']} | {r['session']} | {r['signal_type']} | {guards} | {exits} "
            f"| {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.2f} | {r['expectancy_r']:.3f} "
            f"| {r['wf_ratio']:.2f} | {r['mc_ruin']:.3f} | {r['decay_ratio']:.2f} |"
        )
    return "\n".join(lines) + "\n"


def _write_empty_final(kill_diag: dict | None = None) -> None:
    msg = "# Full-Math Final\n\nNo strategies passed all gates.\n"
    if kill_diag:
        msg += f"\nKill diagnostic: {kill_diag}\n"
    (REPORTS_DIR / "Full_Math_Final.md").write_text(msg, encoding="utf-8")
    (REPORTS_DIR / "full_math_strategies.json").write_text("[]", encoding="utf-8")


# ── CLI ─────────────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(description="Full-math discovery pipeline (entries+guards+exits)")
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
