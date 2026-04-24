"""Full math-edge rediscovery with REAL per-symbol broker friction.

Replaces the generic 0.1R/0.2R friction with a per-symbol USD figure (spread
slippage + commission at vol_min) derived from Vantage VPS symbol_info, then
converts to R-units via the sl_atr_mult and each symbol's median ATR.

Pipeline (single invocation):
  Phase A — full-grid screen on 3y+ CSV M15
      15 assets x 5 sessions x 12 setups (6 FADE + 6 MOMENTUM)
      R:R grid = TP(7) x SL(5) = 35 combos (each RR tested both on
      original direction AND inverted direction)
      Real-friction applied from the start.

  Phase B — WF + MC + decay validation on Phase-A passers
      Gates: trades/year>=60, WR>=0.55, PF>=1.25, expectancy>=0.05R,
             WF>=0.80, MC<=0.02, decay>=0.60.

  Phase C — diversified portfolio consolidation
      Per-(symbol,setup) best R:R, session-disjoint per symbol,
      cap 3/symbol and 40%/setup-family. Sort by net R.

Outputs:
    reports/Math_Rediscovery_Real.md
    reports/math_rediscovery_real.json
    reports/math_rediscovery_real.parquet          (Phase A full scan)
    reports/math_rediscovery_real_validated.parquet (Phase B survivors)
    reports/math_rediscovery_real_portfolio.parquet (Phase C final)
    reports/Math_Rediscovery_Comparison.md
    reports/Universe_Pruning.md
"""
from __future__ import annotations

import argparse
import json
import time as _time
from dataclasses import dataclass
from pathlib import Path

import polars as pl

from src.domain.constants import (
    INDICATOR_UNIVERSE, INDICATOR_SESSIONS, WF_IS_MONTHS, WF_OOS_MONTHS,
    FRICTION_FX, FRICTION_INDEX, INDEX_SYMBOLS,
)
from src.engine.friction_real import (
    REAL_FRICTION_TABLE, friction_r, load_median_atr,
)
from src.engine.indicator_validation import (
    compute_metrics, walk_forward_wr, monte_carlo_ruin, decay_slope_ratio,
)
from src.engine.run_math_discovery import _load_and_enrich_math
from src.engine.run_indicator_discovery import _filter_by_session
from src.engine.run_math_fade import (
    detect_setups as detect_fade,
    run_backtest as run_fade_bt,
    BacktestConfig as FadeCfg,
)
from src.engine.run_math_momentum import (
    detect_setups as detect_mom,
    run_backtest as run_mom_bt,
    BacktestConfig as MomCfg,
)

REPORTS_DIR = Path("reports")

FADE_SETUPS = ("KALMAN_PEAK_FADE", "ZSCORE_EXTREME_FADE", "OLS_EXTREME_FADE",
               "CURVATURE_PEAK_FADE", "GARCH_Z_FADE", "AREA_EXTREME_FADE")
MOM_SETUPS = ("VELOCITY_ACCEL_GO", "KAMA_CROSS_MOM", "OLS_SLOPE_STRONG",
              "HURST_TREND_MOM", "KALMAN_INNOV_EXPAND", "SPECTRAL_TREND_MOM")

# RR grid — task spec
TP_GRID = (0.3, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0)
SL_GRID = (0.75, 1.0, 1.5, 2.0, 2.5)

# Gates — Phase A (retain for Phase B)
PA_MIN_TRADES_PER_YEAR = 60
PA_MIN_WR = 0.55
PA_MIN_PF = 1.25
PA_MIN_EXP = 0.05

# Gates — Phase B (robustness)
PB_MIN_WF = 0.80
PB_MAX_MC = 0.02
PB_MIN_DECAY = 0.60

# Portfolio caps (Phase C)
MAX_PER_SYMBOL = 3
MAX_SETUP_SHARE = 0.40


# ───────────────────────── helpers ─────────────────────────

def _generic_friction(sym: str) -> float:
    return FRICTION_INDEX if sym in INDEX_SYMBOLS else FRICTION_FX


def _flip(signals: pl.DataFrame) -> pl.DataFrame:
    if len(signals) == 0:
        return signals
    return signals.with_columns([
        pl.when(pl.col("direction") == "LONG").then(pl.lit("SHORT"))
        .otherwise(pl.lit("LONG")).alias("direction")
    ])


def _safe_detect_fade(bars, setup):
    try:
        return detect_fade(bars, setup)
    except Exception:
        return None


def _safe_detect_mom(bars, setup):
    try:
        return detect_mom(bars, setup)
    except Exception:
        return None


# ───────────────────────── Phase A ─────────────────────────

def run_phase_a(max_minutes: float = 40.0) -> pl.DataFrame:
    t0 = _time.time()
    medians = {s: load_median_atr(s) for s in INDICATOR_UNIVERSE}
    print(f"[PhaseA] median ATR per symbol: {medians}")

    rows = []
    total_sym = len(INDICATOR_UNIVERSE)
    for si, sym in enumerate(INDICATOR_UNIVERSE, 1):
        if sym not in REAL_FRICTION_TABLE:
            print(f"[PhaseA][SKIP] {sym}: no friction entry")
            continue
        med_atr = medians[sym]
        if med_atr <= 0:
            print(f"[PhaseA][SKIP] {sym}: no ATR")
            continue
        try:
            bars = _load_and_enrich_math(sym)
        except FileNotFoundError:
            print(f"[PhaseA][SKIP] {sym}: no parquet")
            continue
        if len(bars) == 0:
            continue
        elapsed = (_time.time() - t0) / 60.0
        print(f"[PhaseA] {si}/{total_sym} {sym} bars={len(bars)} elapsed={elapsed:.1f}m",
              flush=True)
        if elapsed > max_minutes:
            print(f"[PhaseA] TIME BUDGET EXHAUSTED at {elapsed:.1f}m, stopping symbol scan")
            break

        # Pre-detect every setup for this symbol once.
        fade_sigs = {s: _safe_detect_fade(bars, s) for s in FADE_SETUPS}
        mom_sigs = {s: _safe_detect_mom(bars, s) for s in MOM_SETUPS}

        for family, setups, cfg_cls, runner, sigs_map in (
            ("FADE", FADE_SETUPS, FadeCfg, run_fade_bt, fade_sigs),
            ("MOM",  MOM_SETUPS,  MomCfg,  run_mom_bt,  mom_sigs),
        ):
            for setup in setups:
                raw = sigs_map.get(setup)
                if raw is None or len(raw) == 0:
                    continue
                for ses in INDICATOR_SESSIONS:
                    sigs = _filter_by_session(raw, ses)
                    if len(sigs) < 30:
                        continue
                    sigs_inv = _flip(sigs)
                    se_end = INDICATOR_SESSIONS[ses][1]
                    for tp in TP_GRID:
                        for sl in SL_GRID:
                            fric = friction_r(sym, sl, med_atr)
                            cfg = cfg_cls(tp_atr_mult=tp, sl_atr_mult=sl,
                                          session_end_hour_utc=se_end,
                                          friction_r=fric)
                            for dmode, sig_df in (("NORMAL", sigs), ("INVERT", sigs_inv)):
                                trades = runner(sig_df, bars, setup, cfg, sym)
                                if len(trades) < 30:
                                    continue
                                m = compute_metrics(trades)
                                if (m.trades_per_year < PA_MIN_TRADES_PER_YEAR
                                        or m.wr < PA_MIN_WR
                                        or m.profit_factor < PA_MIN_PF
                                        or m.expectancy_r < PA_MIN_EXP):
                                    continue
                                rows.append({
                                    "family": family, "direction_mode": dmode,
                                    "symbol": sym, "session": ses,
                                    "setup_type": setup,
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
        print(f"[PhaseA] {sym}: cumulative rows={len(rows)} elapsed={elapsed:.1f}m")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    if not rows:
        print("[PhaseA] No strategies passed gates.")
        df = pl.DataFrame()
        df.write_parquet(REPORTS_DIR / "math_rediscovery_real.parquet")
        return df

    df = pl.DataFrame(rows).sort("expectancy_r", descending=True)
    df.write_parquet(REPORTS_DIR / "math_rediscovery_real.parquet")
    print(f"[PhaseA] {len(df)} strategies passed gates")
    return df


# ───────────────────────── Phase B ─────────────────────────

def run_phase_b(phase_a: pl.DataFrame) -> pl.DataFrame:
    if len(phase_a) == 0:
        print("[PhaseB] no input")
        return pl.DataFrame()
    print(f"[PhaseB] validating {len(phase_a)} candidates with WF+MC+decay")

    medians = {s: load_median_atr(s) for s in INDICATOR_UNIVERSE}
    bars_cache: dict = {}
    sigs_cache: dict = {}
    out = []
    for i, c in enumerate(phase_a.iter_rows(named=True)):
        if i % 25 == 0:
            print(f"[PhaseB] {i}/{len(phase_a)}", flush=True)
        sym = c["symbol"]; ses = c["session"]; setup = c["setup_type"]
        tp = c["tp_atr_mult"]; sl = c["sl_atr_mult"]
        family = c["family"]; dmode = c["direction_mode"]
        if sym not in bars_cache:
            try:
                bars_cache[sym] = _load_and_enrich_math(sym)
            except FileNotFoundError:
                bars_cache[sym] = None
        bars = bars_cache[sym]
        if bars is None:
            continue
        sig_key = (sym, setup, family)
        if sig_key not in sigs_cache:
            if family == "FADE":
                sigs_cache[sig_key] = _safe_detect_fade(bars, setup)
            else:
                sigs_cache[sig_key] = _safe_detect_mom(bars, setup)
        raw = sigs_cache[sig_key]
        if raw is None or len(raw) == 0:
            continue
        sigs = _filter_by_session(raw, ses)
        if dmode == "INVERT":
            sigs = _flip(sigs)
        if len(sigs) < 30:
            continue
        fric = friction_r(sym, sl, medians[sym])
        se_end = INDICATOR_SESSIONS[ses][1]
        if family == "FADE":
            cfg = FadeCfg(tp_atr_mult=tp, sl_atr_mult=sl,
                          session_end_hour_utc=se_end, friction_r=fric)
            trades = run_fade_bt(sigs, bars, setup, cfg, sym)
        else:
            cfg = MomCfg(tp_atr_mult=tp, sl_atr_mult=sl,
                         session_end_hour_utc=se_end, friction_r=fric)
            trades = run_mom_bt(sigs, bars, setup, cfg, sym)
        if len(trades) < 30:
            continue
        wf = walk_forward_wr(trades, WF_IS_MONTHS, WF_OOS_MONTHS)
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
        print("[PhaseB] 0 validated")
        pl.DataFrame().write_parquet(REPORTS_DIR / "math_rediscovery_real_validated.parquet")
        return pl.DataFrame()
    df = pl.DataFrame(out).sort("expectancy_r", descending=True)
    df.write_parquet(REPORTS_DIR / "math_rediscovery_real_validated.parquet")
    print(f"[PhaseB] {len(df)} validated")
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
        print("[PhaseC] empty input")
        return pl.DataFrame()
    # Step 1 — per (symbol, setup): keep best by expectancy
    step1 = (valid.sort("expectancy_r", descending=True)
             .unique(subset=["symbol", "setup_type", "direction_mode"], keep="first"))
    # Step 2 — session-disjoint per symbol
    picks = []
    for sym, sub in step1.group_by("symbol"):
        kept_sessions = set()
        for r in sub.sort("expectancy_r", descending=True).iter_rows(named=True):
            ses = r["session"]
            if _OVERLAPS[ses] & kept_sessions:
                continue
            picks.append(r)
            kept_sessions.add(ses)
    if not picks:
        return pl.DataFrame()
    step2 = pl.DataFrame(picks)
    # Step 3 — cap per symbol
    step3 = []
    per_sym = {}
    for r in step2.sort("expectancy_r", descending=True).iter_rows(named=True):
        n = per_sym.get(r["symbol"], 0)
        if n >= MAX_PER_SYMBOL:
            continue
        step3.append(r); per_sym[r["symbol"]] = n + 1
    step3_df = pl.DataFrame(step3)
    # Step 4 — cap per setup family
    max_setup = int(len(step3_df) * MAX_SETUP_SHARE) + 1
    final_rows = []
    per_setup = {}
    for r in step3_df.sort("expectancy_r", descending=True).iter_rows(named=True):
        n = per_setup.get(r["setup_type"], 0)
        if n >= max_setup:
            continue
        final_rows.append(r); per_setup[r["setup_type"]] = n + 1
    final = pl.DataFrame(final_rows).sort("net_r", descending=True)
    final.write_parquet(REPORTS_DIR / "math_rediscovery_real_portfolio.parquet")
    print(f"[PhaseC] final portfolio = {len(final)}")
    return final


# ───────────────────────── Reports ─────────────────────────

def _write_main_report(phase_a: pl.DataFrame, validated: pl.DataFrame,
                       portfolio: pl.DataFrame) -> None:
    lines = ["# Math Rediscovery — REAL Broker Friction", "",
             f"- Phase A passers (PF>=1.25, WR>=0.55, trades/yr>=60, exp>=0.05R): **{len(phase_a)}**",
             f"- Phase B validated (WF>=0.80, MC<=0.02, decay>=0.60): **{len(validated)}**",
             f"- Phase C portfolio (session-disjoint, caps): **{len(portfolio)}**",
             "",
             "Grid: TP(0.3..2.0 x7) x SL(0.75..2.5 x5) = 35 combos,",
             "families = FADE (6 setups) + MOMENTUM (6 setups),",
             "direction = NORMAL + INVERT (tested in parallel),",
             "universe = 15 symbols x 5 sessions on 3y+ M15 cache.",
             "",
             "Friction: per-symbol USD per round-turn at vol_min, converted to R via",
             "`friction_r = usd / (sl * median_atr * tick_val/tick_size * vol_min)`.",
             ""]
    if len(validated):
        top = validated.sort("net_r", descending=True).head(15)
        lines += ["## Top 15 by Net R (Phase B validated)", "",
                  "| # | Sym | Session | Setup | Dir | Fam | TP | SL | Fric_R | Trd | WR | PF | Exp(R) | NetR | T/yr | WF | MC | Dec |",
                  "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for i, r in enumerate(top.iter_rows(named=True), 1):
            lines.append(
                f"| {i} | {r['symbol']} | {r['session']} | {r['setup_type']} "
                f"| {r['direction_mode']} | {r['family']} | {r['tp_atr_mult']} "
                f"| {r['sl_atr_mult']} | {r['friction_r_used']:.3f} "
                f"| {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.2f} "
                f"| {r['expectancy_r']:.3f} | {r['net_r']:.1f} "
                f"| {r['trades_per_year']:.1f} | {r['wf_ratio']:.2f} "
                f"| {r['mc_ruin']:.3f} | {r['decay_ratio']:.2f} |"
            )
    if len(portfolio):
        lines += ["", "## Final Diversified Portfolio", "",
                  "| # | Sym | Session | Setup | Dir | Fam | TP | SL | WR | PF | Exp(R) | NetR | T/yr |",
                  "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for i, r in enumerate(portfolio.iter_rows(named=True), 1):
            lines.append(
                f"| {i} | {r['symbol']} | {r['session']} | {r['setup_type']} "
                f"| {r['direction_mode']} | {r['family']} | {r['tp_atr_mult']} "
                f"| {r['sl_atr_mult']} | {r['wr']:.3f} | {r['pf']:.2f} "
                f"| {r['expectancy_r']:.3f} | {r['net_r']:.1f} "
                f"| {r['trades_per_year']:.1f} |"
            )
    (REPORTS_DIR / "Math_Rediscovery_Real.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8")


def _write_portfolio_json(portfolio: pl.DataFrame) -> None:
    items = []
    for r in portfolio.iter_rows(named=True):
        items.append({
            "family": r["family"], "direction_mode": r["direction_mode"],
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
    (REPORTS_DIR / "math_rediscovery_real.json").write_text(
        json.dumps(items, indent=2), encoding="utf-8")


# ── Comparison: current 6-setup bot under old vs real friction ──────────

CURRENT_BOT_SETUPS = [
    # (internal_sym, session, setup_type, direction_mode, tp, sl, family)
    ("XAUUSD", "LONDON", "OLS_SLOPE_STRONG", "INVERT", 0.75, 1.5, "MOM"),
    ("XAUUSD", "ASIA",   "HURST_TREND_MOM",  "INVERT", 0.5,  1.5, "MOM"),
    ("GBPAUD", "NY",     "OLS_SLOPE_STRONG", "INVERT", 0.75, 1.5, "MOM"),
    ("NASDAQ100", "LONDON", "HURST_TREND_MOM", "INVERT", 0.75, 1.5, "MOM"),
    ("GBPAUD", "ASIA",   "OLS_SLOPE_STRONG", "INVERT", 0.75, 1.5, "MOM"),
    ("EURJPY", "ASIA",   "OLS_SLOPE_STRONG", "INVERT", 0.75, 1.5, "MOM"),
]


def _backtest_one(sym, ses, setup, dmode, tp, sl, family, friction_r_val):
    try:
        bars = _load_and_enrich_math(sym)
    except FileNotFoundError:
        return None
    if family == "FADE":
        raw = _safe_detect_fade(bars, setup)
        runner = run_fade_bt; CfgCls = FadeCfg
    else:
        raw = _safe_detect_mom(bars, setup)
        runner = run_mom_bt;  CfgCls = MomCfg
    if raw is None or len(raw) == 0:
        return None
    sigs = _filter_by_session(raw, ses)
    if dmode == "INVERT":
        sigs = _flip(sigs)
    if len(sigs) < 20:
        return None
    cfg = CfgCls(tp_atr_mult=tp, sl_atr_mult=sl,
                 session_end_hour_utc=INDICATOR_SESSIONS[ses][1],
                 friction_r=friction_r_val)
    trades = runner(sigs, bars, setup, cfg, sym)
    if len(trades) < 20:
        return None
    return compute_metrics(trades)


def _write_comparison_report() -> None:
    rows = []
    for sym, ses, setup, dmode, tp, sl, family in CURRENT_BOT_SETUPS:
        old_fric = _generic_friction(sym)
        real_fric = friction_r(sym, sl, load_median_atr(sym))
        old_m = _backtest_one(sym, ses, setup, dmode, tp, sl, family, old_fric)
        new_m = _backtest_one(sym, ses, setup, dmode, tp, sl, family, real_fric)
        passes_new = (new_m is not None
                      and new_m.trades_per_year >= PA_MIN_TRADES_PER_YEAR
                      and new_m.wr >= PA_MIN_WR
                      and new_m.profit_factor >= PA_MIN_PF
                      and new_m.expectancy_r >= PA_MIN_EXP)
        rows.append((sym, ses, setup, old_fric, real_fric, old_m, new_m, passes_new))
    lines = ["# Current 6-Setup Bot — Old vs Real Friction", "",
             "Metrics of the live math portfolio recomputed with per-symbol real friction.",
             "",
             "| Sym | Session | Setup | OldFric_R | RealFric_R | WR old | WR new | PF old | PF new | Exp old | Exp new | NewGate |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for (sym, ses, setup, old_f, new_f, om, nm, ok) in rows:
        wo = f"{om.wr:.3f}" if om else "-"
        wn = f"{nm.wr:.3f}" if nm else "-"
        po = f"{om.profit_factor:.2f}" if om else "-"
        pn = f"{nm.profit_factor:.2f}" if nm else "-"
        eo = f"{om.expectancy_r:.3f}" if om else "-"
        en = f"{nm.expectancy_r:.3f}" if nm else "-"
        lines.append(
            f"| {sym} | {ses} | {setup} | {old_f:.3f} | {new_f:.3f} "
            f"| {wo} | {wn} | {po} | {pn} | {eo} | {en} "
            f"| {'PASS' if ok else 'FAIL'} |"
        )
    lines += ["", f"Gate: trades/year>={PA_MIN_TRADES_PER_YEAR}, WR>={PA_MIN_WR}, "
              f"PF>={PA_MIN_PF}, expectancy>={PA_MIN_EXP}R."]
    (REPORTS_DIR / "Math_Rediscovery_Comparison.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8")


def _write_pruning_report(phase_a: pl.DataFrame, validated: pl.DataFrame,
                          portfolio: pl.DataFrame) -> None:
    """Symbols that survive vs don't, and new wins."""
    all_syms = set(INDICATOR_UNIVERSE)
    with_survivors = set(validated["symbol"].unique().to_list()) if len(validated) else set()
    dead = sorted(all_syms - with_survivors)
    alive = sorted(with_survivors)

    current_combos = {(s[0], s[1], s[2]) for s in CURRENT_BOT_SETUPS}
    new_combos = []
    if len(portfolio):
        for r in portfolio.iter_rows(named=True):
            k = (r["symbol"], r["session"], r["setup_type"])
            if k not in current_combos:
                new_combos.append(r)

    lines = ["# Universe Pruning Recommendation", "",
             "## Symbols with ZERO surviving strategies under real friction",
             ""]
    if dead:
        for s in dead:
            lines.append(f"- **{s}** (drop from math discovery universe)")
    else:
        lines.append("- _(none — every symbol has at least one survivor)_")
    lines += ["", "## Symbols with surviving strategies (keep)", ""]
    for s in alive:
        n = int(validated.filter(pl.col("symbol") == s).height)
        lines.append(f"- **{s}** — {n} validated combos")
    lines += ["", "## New (symbol, session, setup) combinations in portfolio but NOT in current 6-setup bot",
              ""]
    if new_combos:
        for r in new_combos:
            lines.append(f"- {r['symbol']} / {r['session']} / {r['setup_type']} "
                         f"/ {r['direction_mode']} "
                         f"TP={r['tp_atr_mult']} SL={r['sl_atr_mult']} "
                         f"(exp={r['expectancy_r']:.3f}R, WR={r['wr']:.3f}, "
                         f"PF={r['pf']:.2f}, trades/yr={r['trades_per_year']:.0f})")
    else:
        lines.append("- _(none; real-friction portfolio is a subset of current)_")
    (REPORTS_DIR / "Universe_Pruning.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8")


# ───────────────────────── main ─────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=("a", "b", "c", "all"), default="all")
    ap.add_argument("--max-minutes", type=float, default=40.0,
                    help="Phase-A time budget (symbols scanned until exceeded)")
    args = ap.parse_args()
    t0 = _time.time()

    if args.phase in ("a", "all"):
        pa = run_phase_a(max_minutes=args.max_minutes)
    else:
        pa = pl.read_parquet(REPORTS_DIR / "math_rediscovery_real.parquet")

    if args.phase in ("b", "all"):
        pb = run_phase_b(pa)
    else:
        path = REPORTS_DIR / "math_rediscovery_real_validated.parquet"
        pb = pl.read_parquet(path) if path.exists() else pl.DataFrame()

    if args.phase in ("c", "all"):
        pc = run_phase_c(pb)
    else:
        path = REPORTS_DIR / "math_rediscovery_real_portfolio.parquet"
        pc = pl.read_parquet(path) if path.exists() else pl.DataFrame()

    _write_main_report(pa, pb, pc)
    _write_portfolio_json(pc) if len(pc) else None
    _write_comparison_report()
    _write_pruning_report(pa, pb, pc)

    elapsed = (_time.time() - t0) / 60.0
    print(f"\nDONE — elapsed {elapsed:.1f} min")
    print(f"  Phase A: {len(pa)} strategies passed gates")
    print(f"  Phase B: {len(pb)} validated (WF/MC/decay)")
    print(f"  Phase C: {len(pc)} final portfolio")


if __name__ == "__main__":
    main()
