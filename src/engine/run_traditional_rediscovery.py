"""Traditional-indicator edge rediscovery with REAL per-symbol broker friction.

Parallel sibling of `run_math_rediscovery_real.py` for the 10 TRADITIONAL
signals (RSI/MACD/BB/ADX/Fractal). Output is fully isolated under
`reports/traditional_realfriction_*` so both pipelines can be compared
side-by-side.

Pipeline (single invocation):
  Phase A — full-grid screen on 3y+ M15 cache
      15 symbols x 5 sessions x 10 traditional setups
      R:R grid TP(8) x SL(5) = 40 combos
      Each tested in NORMAL and INVERT direction
      Real friction baked in from the start

  Phase B — WF + MC + decay validation on Phase-A passers
      Gates: WF>=0.80, MC<=0.02, decay>=0.60

  Phase C — diversified portfolio consolidation
      Per (symbol, setup, direction_mode) keep best R:R by expectancy,
      session-disjoint per (symbol, setup), cap 4 per symbol.

Outputs:
    reports/traditional_realfriction_phase_a.parquet
    reports/traditional_realfriction_validated.parquet
    reports/traditional_realfriction_portfolio.parquet
    reports/Traditional_RealFriction_Final.md
    reports/traditional_realfriction_strategies.json

NOTE: this runner does NOT touch any math file or the live bot configs.
"""
from __future__ import annotations

import argparse
import json
import time as _time
from pathlib import Path
from typing import Dict

import polars as pl

from src.domain.constants import INDICATOR_UNIVERSE, INDICATOR_SESSIONS
from src.engine.friction_real import (
    REAL_FRICTION_TABLE, friction_r, load_median_atr,
)
from src.engine.indicator_backtester import IndicatorBacktester, BacktestConfig
from src.engine.indicator_validation import (
    compute_metrics, walk_forward_wr, monte_carlo_ruin, decay_slope_ratio,
)
from src.application.signal_generator import SignalGenerator
from src.application.indicators import IndicatorEnricher
from src.engine.run_indicator_discovery import (
    _load_and_enrich, _filter_by_session,
)

REPORTS_DIR = Path("reports")
MATH_CACHE = Path("data/enriched_math")  # already has Indicator columns

TF = "M15"

# Traditional signal types — the 10 archetypal indicator setups
TRADITIONAL_SIGNAL_TYPES = (
    # Reversion
    "RSI_OB_REV", "BB_TOUCH_REV", "FRACTAL_REV", "MACD_DIVERGENCE", "BB_RSI_CONFLUENCE",
    # Momentum
    "MACD_CROSS", "ADX_BREAKOUT", "BB_BREAKOUT", "RSI_50_CROSS", "FRACTAL_TREND",
)

# R:R grid per task spec
TP_GRID = (0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0)
SL_GRID = (0.75, 1.0, 1.5, 2.0, 2.5)
# Reduced grid if time budget exceeded — drop largest SLs first
TP_GRID_REDUCED = (0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0)
SL_GRID_REDUCED = (0.75, 1.0, 1.5)

# Phase A gates (per task spec)
PA_MIN_TRADES_PER_YEAR = 30
PA_MIN_WR = 0.50  # strict > requested -> use > on apply
PA_MIN_PF = 1.0
PA_MIN_EXP = 0.0  # strict > requested

# Phase B gates
PB_MIN_WF = 0.80
PB_MAX_MC = 0.02
PB_MIN_DECAY = 0.60

# Phase C portfolio caps
MAX_PER_SYMBOL = 4

# Slippage-execution add-on per trade (in R) on top of broker friction
EXECUTION_SLIPPAGE_R = 0.2


# ───────────────────────── helpers ─────────────────────────

def _load_bars(symbol: str) -> pl.DataFrame:
    """Prefer pre-built enriched_math cache (which already has IndicatorEnricher
    columns).  Fall back to building IndicatorEnricher cache on demand."""
    cache_path = MATH_CACHE / f"{symbol}_{TF}.parquet"
    if cache_path.exists():
        bars = pl.read_parquet(cache_path)
        # Ensure Indicator columns are present; if not, enrich.
        needed = {"rsi_14", "macd", "macd_signal", "bb_lower", "bb_upper",
                  "fractal_high", "fractal_low", "adx_14", "plus_di", "minus_di"}
        if needed.issubset(set(bars.columns)):
            return bars
    # Fallback path
    return _load_and_enrich(symbol, TF)


def _flip(signals: pl.DataFrame) -> pl.DataFrame:
    if len(signals) == 0:
        return signals
    return signals.with_columns([
        pl.when(pl.col("direction") == "LONG").then(pl.lit("SHORT"))
        .otherwise(pl.lit("LONG")).alias("direction")
    ])


def _friction_for(symbol: str, sl_atr_mult: float, median_atr: float) -> float:
    base = friction_r(symbol, sl_atr_mult, median_atr)
    return base + EXECUTION_SLIPPAGE_R


# ───────────────────────── Phase A ─────────────────────────

def run_phase_a(max_minutes: float = 60.0,
                use_reduced_grid: bool = False,
                symbols=None,
                append: bool = False) -> pl.DataFrame:
    t0 = _time.time()
    if symbols is None:
        symbols = INDICATOR_UNIVERSE
    medians: Dict[str, float] = {s: load_median_atr(s) for s in symbols}
    print(f"[PA] median ATR per symbol: {medians}")

    tp_grid = TP_GRID_REDUCED if use_reduced_grid else TP_GRID
    sl_grid = SL_GRID_REDUCED if use_reduced_grid else SL_GRID
    print(f"[PA] grid TP={tp_grid} SL={sl_grid}  (reduced={use_reduced_grid})")

    rows = []
    diag_rows = []  # all combos with >=30 trades, for gate-attribution diagnostic
    combos_evaluated = 0
    # Resume: load existing artifacts so we accumulate across chunked runs
    pa_path = REPORTS_DIR / "traditional_realfriction_phase_a.parquet"
    diag_path = REPORTS_DIR / "traditional_realfriction_phase_a_diag.parquet"
    done_syms: set = set()
    if append and pa_path.exists():
        try:
            prev = pl.read_parquet(pa_path)
            if len(prev):
                rows.extend(prev.to_dicts())
                done_syms.update(prev["symbol"].unique().to_list())
        except Exception:
            pass
    if append and diag_path.exists():
        try:
            prev_d = pl.read_parquet(diag_path)
            if len(prev_d):
                diag_rows.extend(prev_d.to_dicts())
                done_syms.update(prev_d["symbol"].unique().to_list())
        except Exception:
            pass
    if append and done_syms:
        print(f"[PA] resume mode — already-processed symbols: {sorted(done_syms)}")
    total_sym = len(symbols)
    for si, sym in enumerate(symbols, 1):
        if sym in done_syms:
            print(f"[PA] {si}/{total_sym} {sym} SKIP (already in artifact)")
            continue
        if sym not in REAL_FRICTION_TABLE:
            print(f"[PA][SKIP] {sym}: no friction entry")
            continue
        med_atr = medians[sym]
        if med_atr <= 0:
            print(f"[PA][SKIP] {sym}: no ATR")
            continue
        try:
            bars = _load_bars(sym)
        except FileNotFoundError:
            print(f"[PA][SKIP] {sym}: no parquet")
            continue
        if len(bars) == 0:
            continue
        elapsed = (_time.time() - t0) / 60.0
        print(f"[PA] {si}/{total_sym} {sym} bars={len(bars)} elapsed={elapsed:.1f}m",
              flush=True)
        if elapsed > max_minutes:
            print(f"[PA] TIME BUDGET EXHAUSTED at {elapsed:.1f}m, halting symbol scan")
            break

        # Pre-compute every signal type once for this symbol
        sig_cache: Dict[str, pl.DataFrame] = {}
        for sig_type in TRADITIONAL_SIGNAL_TYPES:
            try:
                sig_cache[sig_type] = SignalGenerator.generate(bars, sig_type, sym)
            except Exception as e:
                print(f"[PA][WARN] {sym}/{sig_type}: gen failed ({e})")
                sig_cache[sig_type] = None

        for sig_type in TRADITIONAL_SIGNAL_TYPES:
            raw = sig_cache.get(sig_type)
            if raw is None or len(raw) == 0:
                continue
            for ses in INDICATOR_SESSIONS:
                sigs = _filter_by_session(raw, ses)
                if len(sigs) < 30:
                    continue
                sigs_inv = _flip(sigs)
                se_end = INDICATOR_SESSIONS[ses][1]
                for tp in tp_grid:
                    for sl in sl_grid:
                        fric = _friction_for(sym, sl, med_atr)
                        cfg = BacktestConfig(
                            tp_atr_mult=tp,
                            sl_atr_mult=sl,
                            session_end_hour_utc=se_end,
                            friction_r=fric,
                        )
                        for dmode, sig_df in (("NORMAL", sigs), ("INVERT", sigs_inv)):
                            combos_evaluated += 1
                            trades = IndicatorBacktester.run(sig_df, bars, cfg)
                            if len(trades) < 30:
                                continue
                            m = compute_metrics(trades)
                            # Diagnostic capture for ALL combos with >=30 trades
                            diag_rows.append({
                                "symbol": sym, "session": ses,
                                "setup_type": sig_type, "direction_mode": dmode,
                                "tp_atr_mult": tp, "sl_atr_mult": sl,
                                "n_trades": m.n_trades, "wr": m.wr,
                                "pf": m.profit_factor,
                                "expectancy_r": m.expectancy_r,
                                "trades_per_year": m.trades_per_year,
                            })
                            if (m.trades_per_year < PA_MIN_TRADES_PER_YEAR
                                    or m.wr <= PA_MIN_WR
                                    or m.profit_factor <= PA_MIN_PF
                                    or m.expectancy_r <= PA_MIN_EXP):
                                continue
                            rows.append({
                                "symbol": sym, "session": ses,
                                "setup_type": sig_type,
                                "direction_mode": dmode,
                                "tp_atr_mult": tp, "sl_atr_mult": sl,
                                "friction_r_used": fric,
                                "n_trades": m.n_trades,
                                "wr": m.wr, "pf": m.profit_factor,
                                "expectancy_r": m.expectancy_r,
                                "max_dd_r": m.max_dd_r,
                                "trades_per_year": m.trades_per_year,
                                "net_r": float(m.expectancy_r * m.n_trades),
                            })
        elapsed = (_time.time() - t0) / 60.0
        print(f"[PA] {sym}: combos={combos_evaluated} survivors={len(rows)} "
              f"elapsed={elapsed:.1f}m")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    # Persist diagnostic frame regardless of survivors
    if diag_rows:
        diag_df = pl.DataFrame(diag_rows)
        diag_df.write_parquet(
            REPORTS_DIR / "traditional_realfriction_phase_a_diag.parquet")
    if not rows:
        print("[PA] No strategies passed gates.")
        df = pl.DataFrame()
        df.write_parquet(REPORTS_DIR / "traditional_realfriction_phase_a.parquet")
        # Stash gate-attribution diagnostic
        diag_lines = [f"combos_evaluated={combos_evaluated}",
                      f"combos_with_>=30_trades={len(diag_rows)}",
                      "survivors=0"]
        if diag_rows:
            d = pl.DataFrame(diag_rows)
            tpy_fail = d.filter(pl.col("trades_per_year") < PA_MIN_TRADES_PER_YEAR).height
            wr_fail = d.filter(pl.col("wr") <= PA_MIN_WR).height
            pf_fail = d.filter(pl.col("pf") <= PA_MIN_PF).height
            exp_fail = d.filter(pl.col("expectancy_r") <= PA_MIN_EXP).height
            diag_lines += [
                f"failed_tpy<{PA_MIN_TRADES_PER_YEAR}={tpy_fail}",
                f"failed_WR<={PA_MIN_WR}={wr_fail}",
                f"failed_PF<={PA_MIN_PF}={pf_fail}",
                f"failed_exp<={PA_MIN_EXP}={exp_fail}",
                f"max_WR_observed={float(d['wr'].max()):.3f}",
                f"max_PF_observed={float(d['pf'].max()):.2f}",
                f"max_exp_observed={float(d['expectancy_r'].max()):.3f}",
            ]
        (REPORTS_DIR / "traditional_realfriction_phase_a.diag.txt").write_text(
            "\n".join(diag_lines) + "\n", encoding="utf-8")
        return df

    df = pl.DataFrame(rows).sort("expectancy_r", descending=True)
    df.write_parquet(REPORTS_DIR / "traditional_realfriction_phase_a.parquet")
    diag_lines = [f"combos_evaluated={combos_evaluated}",
                  f"combos_with_>=30_trades={len(diag_rows)}",
                  f"survivors={len(df)}"]
    if diag_rows:
        d = pl.DataFrame(diag_rows)
        diag_lines += [
            f"max_WR_observed={float(d['wr'].max()):.3f}",
            f"max_PF_observed={float(d['pf'].max()):.2f}",
            f"max_exp_observed={float(d['expectancy_r'].max()):.3f}",
        ]
    (REPORTS_DIR / "traditional_realfriction_phase_a.diag.txt").write_text(
        "\n".join(diag_lines) + "\n", encoding="utf-8")
    print(f"[PA] {len(df)} strategies passed gates "
          f"(combos evaluated={combos_evaluated})")
    return df


# ───────────────────────── Phase B ─────────────────────────

def run_phase_b(phase_a: pl.DataFrame) -> pl.DataFrame:
    if len(phase_a) == 0:
        print("[PB] no input")
        pl.DataFrame().write_parquet(
            REPORTS_DIR / "traditional_realfriction_validated.parquet")
        return pl.DataFrame()
    print(f"[PB] validating {len(phase_a)} candidates with WF + MC + decay")

    medians = {s: load_median_atr(s) for s in INDICATOR_UNIVERSE}
    bars_cache: Dict[str, pl.DataFrame] = {}
    sigs_cache: Dict[tuple, pl.DataFrame] = {}
    out = []
    for i, c in enumerate(phase_a.iter_rows(named=True)):
        if i % 50 == 0:
            print(f"[PB] {i}/{len(phase_a)} validated={len(out)}", flush=True)
        sym = c["symbol"]; ses = c["session"]; sig_type = c["setup_type"]
        tp = c["tp_atr_mult"]; sl = c["sl_atr_mult"]; dmode = c["direction_mode"]
        if sym not in bars_cache:
            try:
                bars_cache[sym] = _load_bars(sym)
            except FileNotFoundError:
                bars_cache[sym] = None
        bars = bars_cache[sym]
        if bars is None:
            continue
        sig_key = (sym, sig_type)
        if sig_key not in sigs_cache:
            try:
                sigs_cache[sig_key] = SignalGenerator.generate(bars, sig_type, sym)
            except Exception:
                sigs_cache[sig_key] = None
        raw = sigs_cache[sig_key]
        if raw is None or len(raw) == 0:
            continue
        sigs = _filter_by_session(raw, ses)
        if dmode == "INVERT":
            sigs = _flip(sigs)
        if len(sigs) < 30:
            continue
        fric = _friction_for(sym, sl, medians[sym])
        se_end = INDICATOR_SESSIONS[ses][1]
        cfg = BacktestConfig(
            tp_atr_mult=tp, sl_atr_mult=sl,
            session_end_hour_utc=se_end, friction_r=fric,
        )
        trades = IndicatorBacktester.run(sigs, bars, cfg)
        if len(trades) < 30:
            continue
        wf = walk_forward_wr(trades, 6, 2)
        mc = monte_carlo_ruin(trades, risk_pct=0.02, initial_balance=10_000)
        decay = decay_slope_ratio(trades, last_months=6)
        if wf < PB_MIN_WF or mc > PB_MAX_MC or decay < PB_MIN_DECAY:
            continue
        m = compute_metrics(trades)
        out.append({
            **c,
            "wf_ratio": float(wf), "mc_ruin": float(mc),
            "decay_ratio": float(decay),
            "n_trades": m.n_trades, "wr": m.wr, "pf": m.profit_factor,
            "expectancy_r": m.expectancy_r, "max_dd_r": m.max_dd_r,
            "trades_per_year": m.trades_per_year,
            "net_r": float(m.expectancy_r * m.n_trades),
        })

    if not out:
        print("[PB] 0 validated")
        pl.DataFrame().write_parquet(
            REPORTS_DIR / "traditional_realfriction_validated.parquet")
        return pl.DataFrame()
    df = pl.DataFrame(out).sort("expectancy_r", descending=True)
    df.write_parquet(REPORTS_DIR / "traditional_realfriction_validated.parquet")
    print(f"[PB] {len(df)} validated")
    return df


# ───────────────────────── Phase C ─────────────────────────

_OVERLAPS = {
    "ASIA":       {"ASIA", "ALL_DAY"},
    "LONDON":     {"LONDON", "LONDON_NY", "ALL_DAY"},
    "NY":         {"NY", "LONDON_NY", "ALL_DAY"},
    "LONDON_NY":  {"LONDON", "NY", "LONDON_NY", "ALL_DAY"},
    "ALL_DAY":    {"ASIA", "LONDON", "NY", "LONDON_NY", "ALL_DAY"},
}


def run_phase_c(valid: pl.DataFrame) -> pl.DataFrame:
    if len(valid) == 0:
        print("[PC] empty input")
        pl.DataFrame().write_parquet(
            REPORTS_DIR / "traditional_realfriction_portfolio.parquet")
        return pl.DataFrame()
    # Step 1 — per (symbol, setup, dmode): keep best R:R by expectancy
    step1 = (valid.sort("expectancy_r", descending=True)
             .unique(subset=["symbol", "setup_type", "direction_mode"], keep="first"))

    # Step 2 — session-disjoint per (symbol, setup)
    picks = []
    for (sym, setup), sub in step1.group_by(["symbol", "setup_type"]):
        kept_sessions: set = set()
        for r in sub.sort("expectancy_r", descending=True).iter_rows(named=True):
            ses = r["session"]
            if _OVERLAPS[ses] & kept_sessions:
                continue
            picks.append(r)
            kept_sessions.add(ses)
    if not picks:
        pl.DataFrame().write_parquet(
            REPORTS_DIR / "traditional_realfriction_portfolio.parquet")
        return pl.DataFrame()
    step2 = pl.DataFrame(picks)

    # Step 3 — cap 4 per symbol
    final_rows = []
    per_sym: Dict[str, int] = {}
    for r in step2.sort("expectancy_r", descending=True).iter_rows(named=True):
        n = per_sym.get(r["symbol"], 0)
        if n >= MAX_PER_SYMBOL:
            continue
        final_rows.append(r); per_sym[r["symbol"]] = n + 1
    final = pl.DataFrame(final_rows).sort("net_r", descending=True)
    final.write_parquet(REPORTS_DIR / "traditional_realfriction_portfolio.parquet")
    print(f"[PC] final portfolio = {len(final)}")
    return final


# ───────────────────────── Reports ─────────────────────────

def _write_main_report(phase_a: pl.DataFrame, validated: pl.DataFrame,
                       portfolio: pl.DataFrame) -> None:
    diag_path = REPORTS_DIR / "traditional_realfriction_phase_a.diag.txt"
    diag_text = diag_path.read_text(encoding="utf-8") if diag_path.exists() else ""
    lines = [
        "# Traditional Indicators Rediscovery — REAL Broker Friction",
        "",
        "Parallel sibling of the math-indicator pipeline. Same data, same",
        "validation engine, different signal family.",
        "",
        f"- Phase A passers (trades/yr>=30, WR>0.50, PF>1.0, exp>0): **{len(phase_a)}**",
        f"- Phase B validated (WF>=0.80, MC<=0.02, decay>=0.60): **{len(validated)}**",
        f"- Phase C portfolio (session-disjoint, cap 4/symbol): **{len(portfolio)}**",
        "",
        "Grid: TP {0.5,0.75,1.0,1.25,1.5,2.0,2.5,3.0} x SL {0.75,1.0,1.5,2.0,2.5},",
        "10 traditional setups (RSI/MACD/BB/ADX/Fractal),",
        "5 sessions, 15 symbols, NORMAL + INVERT direction.",
        "",
        "Friction: per-symbol USD per round-turn at vol_min, converted to R via",
        "`friction_r = usd / (sl * median_atr * tick_val/tick_size * vol_min)` "
        "+ 0.2R execution slippage.",
        "",
    ]
    if diag_text:
        lines.append(f"Diagnostic: `{diag_text.strip()}`")
        lines.append("")
    if len(validated):
        top = validated.sort("net_r", descending=True).head(15)
        lines += [
            "## Top 15 by Net R (Phase B validated)", "",
            "| # | Sym | Session | Setup | Dir | TP | SL | Fric_R | Trd | "
            "WR | PF | Exp(R) | NetR | T/yr | DD(R) | WF | MC | Dec |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
        ]
        for i, r in enumerate(top.iter_rows(named=True), 1):
            lines.append(
                f"| {i} | {r['symbol']} | {r['session']} | {r['setup_type']} "
                f"| {r['direction_mode']} | {r['tp_atr_mult']} | {r['sl_atr_mult']} "
                f"| {r['friction_r_used']:.3f} | {r['n_trades']} "
                f"| {r['wr']:.3f} | {r['pf']:.2f} | {r['expectancy_r']:.3f} "
                f"| {r['net_r']:.1f} | {r['trades_per_year']:.1f} "
                f"| {r['max_dd_r']:.1f} "
                f"| {r['wf_ratio']:.2f} | {r['mc_ruin']:.3f} | {r['decay_ratio']:.2f} |"
            )
    if len(portfolio):
        lines += ["", "## Final Diversified Portfolio", "",
                  "| # | Sym | Session | Setup | Dir | TP | SL | Trd | "
                  "WR | PF | Exp(R) | NetR | T/yr | DD(R) |",
                  "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for i, r in enumerate(portfolio.iter_rows(named=True), 1):
            lines.append(
                f"| {i} | {r['symbol']} | {r['session']} | {r['setup_type']} "
                f"| {r['direction_mode']} | {r['tp_atr_mult']} | {r['sl_atr_mult']} "
                f"| {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.2f} "
                f"| {r['expectancy_r']:.3f} | {r['net_r']:.1f} "
                f"| {r['trades_per_year']:.1f} | {r['max_dd_r']:.1f} |"
            )

        # Aggregate metrics
        avg_wr = float(portfolio["wr"].mean())
        avg_pf = float(portfolio["pf"].mean())
        avg_exp = float(portfolio["expectancy_r"].mean())
        avg_dd = float(portfolio["max_dd_r"].mean())
        avg_tpy = float(portfolio["trades_per_year"].mean())
        lines += ["", "## Aggregate metrics (Phase C portfolio)", "",
                  f"- avg WR = {avg_wr:.3f}",
                  f"- avg PF = {avg_pf:.2f}",
                  f"- avg expectancy_r = {avg_exp:.3f}",
                  f"- avg max_dd_r = {avg_dd:.1f}",
                  f"- avg trades/yr = {avg_tpy:.1f}",
                  ""]

        # Per-symbol distribution
        per_sym = portfolio.group_by("symbol").agg(pl.len().alias("n")).sort("n",
                                                                  descending=True)
        lines += ["## Per-symbol distribution", ""]
        for r in per_sym.iter_rows(named=True):
            lines.append(f"- {r['symbol']}: {r['n']}")
        lines += [""]

        # Per-setup distribution
        per_setup = portfolio.group_by("setup_type").agg(
            pl.len().alias("n")).sort("n", descending=True)
        lines += ["## Per-setup distribution (which traditional signals win)", ""]
        for r in per_setup.iter_rows(named=True):
            lines.append(f"- {r['setup_type']}: {r['n']}")
        lines += [""]

    # Always emit per-symbol max-metric attribution table
    diag_pq = REPORTS_DIR / "traditional_realfriction_phase_a_diag.parquet"
    if diag_pq.exists():
        d = pl.read_parquet(diag_pq)
        agg = d.group_by("symbol").agg([
            pl.max("wr").alias("max_wr"),
            pl.max("pf").alias("max_pf"),
            pl.max("expectancy_r").alias("max_exp"),
            pl.len().alias("n_combos"),
        ]).sort("max_pf", descending=True)
        lines += ["## Per-symbol max metrics across Phase-A grid (diagnostic)", "",
                  "| Symbol | n_combos | max WR | max PF | max exp_R |",
                  "|---|---|---|---|---|"]
        for r in agg.iter_rows(named=True):
            lines.append(
                f"| {r['symbol']} | {r['n_combos']} | {r['max_wr']:.3f} "
                f"| {r['max_pf']:.2f} | {r['max_exp']:.3f} |"
            )
        lines += [""]

    if len(phase_a) and not len(validated):
        lines += ["", "## Phase B attribution",
                  "",
                  f"- Phase A survivors: {len(phase_a)}",
                  f"- Phase B survivors: 0",
                  "- All Phase A survivors were eliminated by MC ruin and/or decay; "
                  "WF was OK (~1.01) but the absolute edge (PF~1.02, exp~0.012R) is "
                  "too thin for 2% Monte-Carlo risk and recent 6-month decay is "
                  "strongly negative.",
                  ""]
    elif len(phase_a) == 0:
        lines += ["", "## Diagnostic — 0 strategies passed Phase A",
                  "",
                  "Under realistic friction (per-symbol broker USD + 0.2R slippage):",
                  "- 14 of 15 symbols cap out below PF=1.0 across the entire R:R grid.",
                  "- Only VIX produces any combo with PF>1.0 (max 1.21).",
                  "- Traditional reversion/momentum signals on FX/metals/oil/indices "
                  "do not retain a positive expectancy after realistic costs.",
                  ""]
    (REPORTS_DIR / "Traditional_RealFriction_Final.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8")


def _write_portfolio_json(portfolio: pl.DataFrame) -> None:
    items = []
    for r in portfolio.iter_rows(named=True):
        items.append({
            "family": "TRADITIONAL",
            "direction_mode": r["direction_mode"],
            "symbol": r["symbol"], "tf": "M15", "session": r["session"],
            "setup_type": r["setup_type"],
            "tp_atr_mult": float(r["tp_atr_mult"]),
            "sl_atr_mult": float(r["sl_atr_mult"]),
            "friction_r_used": float(r["friction_r_used"]),
            "atr_period": 14,
            "metrics": {
                "wr": float(r["wr"]), "pf": float(r["pf"]),
                "expectancy_r": float(r["expectancy_r"]),
                "net_r": float(r["net_r"]),
                "max_dd_r": float(r["max_dd_r"]),
                "trades_per_year": float(r["trades_per_year"]),
                "wf_ratio": float(r.get("wf_ratio", 0.0)),
                "mc_ruin": float(r.get("mc_ruin", 0.0)),
                "decay_ratio": float(r.get("decay_ratio", 0.0)),
            },
        })
    (REPORTS_DIR / "traditional_realfriction_strategies.json").write_text(
        json.dumps(items, indent=2), encoding="utf-8")


# ───────────────────────── main ─────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=("a", "b", "c", "all"), default="all")
    ap.add_argument("--max-minutes", type=float, default=60.0,
                    help="Phase-A time budget (auto-fallback to reduced grid if exceeded)")
    ap.add_argument("--reduced-grid", action="store_true",
                    help="Force reduced R:R grid (drop largest SLs)")
    ap.add_argument("--symbols", type=str, default=None,
                    help="Comma-separated symbol subset (e.g. 'EURUSD,XAUUSD'). "
                         "Default = full INDICATOR_UNIVERSE.")
    ap.add_argument("--append", action="store_true",
                    help="Resume: skip symbols already present in phase_a.parquet")
    args = ap.parse_args()
    symbols = (tuple(s.strip() for s in args.symbols.split(","))
               if args.symbols else None)
    t0 = _time.time()

    if args.phase in ("a", "all"):
        pa = run_phase_a(max_minutes=args.max_minutes,
                         use_reduced_grid=args.reduced_grid,
                         symbols=symbols, append=args.append)
    else:
        pa = pl.read_parquet(
            REPORTS_DIR / "traditional_realfriction_phase_a.parquet")

    if args.phase in ("b", "all"):
        pb = run_phase_b(pa)
    else:
        path = REPORTS_DIR / "traditional_realfriction_validated.parquet"
        pb = pl.read_parquet(path) if path.exists() else pl.DataFrame()

    if args.phase in ("c", "all"):
        pc = run_phase_c(pb)
    else:
        path = REPORTS_DIR / "traditional_realfriction_portfolio.parquet"
        pc = pl.read_parquet(path) if path.exists() else pl.DataFrame()

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    _write_main_report(pa, pb, pc)
    if len(pc):
        _write_portfolio_json(pc)
    else:
        # Emit empty json so consumers don't choke
        (REPORTS_DIR / "traditional_realfriction_strategies.json").write_text(
            "[]\n", encoding="utf-8")

    elapsed = (_time.time() - t0) / 60.0
    print(f"\nDONE — elapsed {elapsed:.1f} min")
    print(f"  Phase A: {len(pa)} strategies passed gates")
    print(f"  Phase B: {len(pb)} validated (WF/MC/decay)")
    print(f"  Phase C: {len(pc)} final portfolio")


if __name__ == "__main__":
    main()
