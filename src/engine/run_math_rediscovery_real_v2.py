"""Math edge rediscovery with REALISTIC friction (v2).

Same skeleton as ``run_math_rediscovery_real.py`` but friction is bumped
by an additional +0.2R slippage to match observed live execution costs
(STOP fill slippage + spread widening + commission overshoot). Live
trades have been showing ~0.3R FX / ~0.4R index per round-turn. The
optimistic 0.1/0.2R generic model wildly underestimates that.

Friction model
--------------
``total_friction_R = friction_real.friction_r(sym, sl, median_atr) + 0.2``

Pipeline
--------
Phase A — full-grid screen on 3y+ M15 cache
    15 assets x 5 sessions x 12 setups (6 FADE + 6 MOMENTUM)
    R:R grid = TP(8) x SL(5) = 40 combos per (sym, ses, setup, dir)
    Direction tested both NORMAL and INVERT.
    Gates: trades/year >= 30, WR > 0.50, PF > 1.0, expectancy > 0.

Phase B — WF + MC + decay validation on Phase-A passers
    Gates: WF >= 0.80, MC <= 0.02, decay >= 0.60.

Phase C — diversified portfolio
    Best (sym, setup, direction) by expectancy_r kept once.
    Session-disjoint per (sym, setup).
    Cap 4 strategies per symbol.

Outputs
-------
    reports/math_realfriction_phase_a.parquet
    reports/math_realfriction_validated.parquet
    reports/math_realfriction_portfolio.parquet
    reports/Math_RealFriction_Final.md
    reports/math_realfriction_strategies.json

Time budget: 60 minutes. If exceeded, drops SL=2.5 and SL=2.0 from grid
on subsequent symbols.
"""
from __future__ import annotations

import argparse
import json
import time as _time
from pathlib import Path

import polars as pl

from src.domain.constants import (
    INDICATOR_UNIVERSE, INDICATOR_SESSIONS,
    WF_IS_MONTHS, WF_OOS_MONTHS,
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

# Wider TP grid: when friction is high, wider TPs amortize the slippage.
TP_GRID_FULL = (0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0)
SL_GRID_FULL = (0.75, 1.0, 1.5, 2.0, 2.5)
# Reduced grid (drop largest SL) used if budget runs hot.
SL_GRID_REDUCED = (0.75, 1.0, 1.5)

# Extra slippage R added to friction_r (STOP fill + spread widening).
EXTRA_SLIPPAGE_R = 0.2

# ── Phase A gates (per spec) ──────────────────────────────────
PA_MIN_TRADES_PER_YEAR = 30
PA_MIN_WR = 0.50
PA_MIN_PF = 1.0
PA_MIN_EXP = 0.0

# ── Phase B gates ────────────────────────────────────────────
PB_MIN_WF = 0.80
PB_MAX_MC = 0.02
PB_MIN_DECAY = 0.60

# ── Phase C portfolio caps ──────────────────────────────────
MAX_PER_SYMBOL = 4

# ── Session-overlap relation (used to enforce session-disjoint) ──
_OVERLAPS = {
    "ASIA":       {"ASIA", "ALL_DAY"},
    "LONDON":     {"LONDON", "LONDON_NY", "ALL_DAY"},
    "NY":         {"NY", "LONDON_NY", "ALL_DAY"},
    "LONDON_NY":  {"LONDON", "NY", "LONDON_NY", "ALL_DAY"},
    "ALL_DAY":    {"ASIA", "LONDON", "NY", "LONDON_NY", "ALL_DAY"},
}


# ───────────────────────── helpers ─────────────────────────

def _generic_friction(sym: str) -> float:
    return FRICTION_INDEX if sym in INDEX_SYMBOLS else FRICTION_FX


def _real_total_friction(sym: str, sl: float, med_atr: float) -> float:
    """friction_real.friction_r + 0.2R extra slippage."""
    return friction_r(sym, sl, med_atr) + EXTRA_SLIPPAGE_R


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

def run_phase_a(max_minutes: float = 50.0) -> pl.DataFrame:
    t0 = _time.time()
    medians = {s: load_median_atr(s) for s in INDICATOR_UNIVERSE}
    print(f"[PhaseA] median ATR per symbol: "
          f"{ {k: round(v, 5) for k, v in medians.items()} }", flush=True)

    rows: list[dict] = []
    sl_grid = SL_GRID_FULL
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
        # If budget is getting tight switch to reduced grid for the rest.
        if elapsed > 0.7 * max_minutes and sl_grid is SL_GRID_FULL:
            sl_grid = SL_GRID_REDUCED
            print(f"[PhaseA] BUDGET WARNING at {elapsed:.1f}m — reducing SL grid "
                  f"to {SL_GRID_REDUCED}", flush=True)
        if elapsed > max_minutes:
            print(f"[PhaseA] TIME BUDGET EXHAUSTED at {elapsed:.1f}m, stopping symbol scan",
                  flush=True)
            break

        print(f"[PhaseA] {si}/{total_sym} {sym} bars={len(bars)} elapsed={elapsed:.1f}m "
              f"sl_grid={len(sl_grid)} tp_grid={len(TP_GRID_FULL)}", flush=True)

        # Pre-detect every setup once per symbol.
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
                    for tp in TP_GRID_FULL:
                        for sl in sl_grid:
                            fric = _real_total_friction(sym, sl, med_atr)
                            cfg = cfg_cls(tp_atr_mult=tp, sl_atr_mult=sl,
                                          session_end_hour_utc=se_end,
                                          friction_r=fric)
                            for dmode, sig_df in (("NORMAL", sigs), ("INVERT", sigs_inv)):
                                trades = runner(sig_df, bars, setup, cfg, sym)
                                if len(trades) < 30:
                                    continue
                                m = compute_metrics(trades)
                                if (m.trades_per_year < PA_MIN_TRADES_PER_YEAR
                                        or m.wr <= PA_MIN_WR
                                        or m.profit_factor <= PA_MIN_PF
                                        or m.expectancy_r <= PA_MIN_EXP):
                                    continue
                                rows.append({
                                    "family": family, "direction_mode": dmode,
                                    "symbol": sym, "session": ses,
                                    "setup_type": setup,
                                    "tp_atr_mult": float(tp),
                                    "sl_atr_mult": float(sl),
                                    "friction_r_used": float(fric),
                                    "n_trades": int(m.n_trades),
                                    "wr": float(m.wr),
                                    "pf": float(m.profit_factor),
                                    "expectancy_r": float(m.expectancy_r),
                                    "max_dd_r": float(m.max_dd_r),
                                    "trades_per_year": float(m.trades_per_year),
                                    "net_r": float(m.expectancy_r * m.n_trades),
                                })
        elapsed = (_time.time() - t0) / 60.0
        print(f"[PhaseA] {sym}: cumulative rows={len(rows)} elapsed={elapsed:.1f}m",
              flush=True)

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    if not rows:
        print("[PhaseA] No strategies passed gates.")
        df = pl.DataFrame()
        df.write_parquet(REPORTS_DIR / "math_realfriction_phase_a.parquet")
        return df

    df = pl.DataFrame(rows).sort("expectancy_r", descending=True)
    df.write_parquet(REPORTS_DIR / "math_realfriction_phase_a.parquet")
    print(f"[PhaseA] {len(df)} strategies passed gates")
    return df


# ───────────────────────── Phase B ─────────────────────────

def run_phase_b(phase_a: pl.DataFrame) -> pl.DataFrame:
    if len(phase_a) == 0:
        print("[PhaseB] no input")
        return pl.DataFrame()
    print(f"[PhaseB] validating {len(phase_a)} candidates with WF+MC+decay",
          flush=True)

    medians = {s: load_median_atr(s) for s in INDICATOR_UNIVERSE}
    bars_cache: dict = {}
    sigs_cache: dict = {}
    out: list[dict] = []
    for i, c in enumerate(phase_a.iter_rows(named=True)):
        if i % 50 == 0:
            print(f"[PhaseB] {i}/{len(phase_a)} survivors_so_far={len(out)}",
                  flush=True)
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
        fric = _real_total_friction(sym, sl, medians[sym])
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
            "n_trades": int(m.n_trades), "wr": float(m.wr),
            "pf": float(m.profit_factor),
            "expectancy_r": float(m.expectancy_r),
            "max_dd_r": float(m.max_dd_r),
            "trades_per_year": float(m.trades_per_year),
            "net_r": float(m.expectancy_r * m.n_trades),
        })

    if not out:
        print("[PhaseB] 0 validated")
        pl.DataFrame().write_parquet(REPORTS_DIR / "math_realfriction_validated.parquet")
        return pl.DataFrame()
    df = pl.DataFrame(out).sort("expectancy_r", descending=True)
    df.write_parquet(REPORTS_DIR / "math_realfriction_validated.parquet")
    print(f"[PhaseB] {len(df)} validated")
    return df


# ───────────────────────── Phase C ─────────────────────────

def run_phase_c(valid: pl.DataFrame) -> pl.DataFrame:
    if len(valid) == 0:
        print("[PhaseC] empty input")
        return pl.DataFrame()

    # Step 1 — best by expectancy per (symbol, setup, direction_mode).
    step1 = (valid.sort("expectancy_r", descending=True)
             .unique(subset=["symbol", "setup_type", "direction_mode"], keep="first"))

    # Step 2 — session-disjoint per (symbol, setup).
    picks = []
    grouped = step1.sort("expectancy_r", descending=True)
    used: dict[tuple[str, str], set[str]] = {}
    for r in grouped.iter_rows(named=True):
        key = (r["symbol"], r["setup_type"])
        kept = used.setdefault(key, set())
        if _OVERLAPS[r["session"]] & kept:
            continue
        picks.append(r)
        kept.add(r["session"])
    if not picks:
        return pl.DataFrame()
    step2 = pl.DataFrame(picks)

    # Step 3 — cap per symbol (max 4).
    final_rows: list[dict] = []
    per_sym: dict[str, int] = {}
    for r in step2.sort("expectancy_r", descending=True).iter_rows(named=True):
        n = per_sym.get(r["symbol"], 0)
        if n >= MAX_PER_SYMBOL:
            continue
        final_rows.append(r); per_sym[r["symbol"]] = n + 1

    final = pl.DataFrame(final_rows).sort("expectancy_r", descending=True)
    final.write_parquet(REPORTS_DIR / "math_realfriction_portfolio.parquet")
    print(f"[PhaseC] final portfolio = {len(final)}")
    return final


# ───────────────────────── Reports ─────────────────────────

def _aggregate(df: pl.DataFrame) -> dict:
    if len(df) == 0:
        return {"n": 0}
    return {
        "n": int(len(df)),
        "avg_wr": float(df["wr"].mean()),
        "avg_pf": float(df["pf"].mean()),
        "avg_exp_r": float(df["expectancy_r"].mean()),
        "avg_dd_r": float(df["max_dd_r"].mean()),
        "avg_tpy": float(df["trades_per_year"].mean()),
    }


def _write_main_report(phase_a: pl.DataFrame, validated: pl.DataFrame,
                       portfolio: pl.DataFrame) -> None:
    agg_p = _aggregate(portfolio)
    lines = [
        "# Math Rediscovery — REALISTIC FRICTION (v2)",
        "",
        "Friction model: `friction_real.friction_r(sym, sl, median_atr) + 0.2`",
        "(broker spread + commission converted to R, plus +0.2R live slippage).",
        "",
        f"- Phase A passers (trades/yr>=30, WR>0.50, PF>1.0, exp>0): **{len(phase_a)}**",
        f"- Phase B validated (WF>=0.80, MC<=0.02, decay>=0.60): **{len(validated)}**",
        f"- Phase C portfolio (session-disjoint, max 4/sym): **{len(portfolio)}**",
        "",
        f"Grid: TP{TP_GRID_FULL} x SL{SL_GRID_FULL} (max combos), "
        f"families = FADE (6) + MOMENTUM (6), direction = NORMAL + INVERT,",
        "universe = 15 symbols x 5 sessions on 3y+ M15 cache.",
        "",
    ]
    if len(portfolio):
        lines += [
            "## Aggregate metrics — portfolio",
            "",
            f"- Strategies: **{agg_p['n']}**",
            f"- Avg WR: **{agg_p['avg_wr']:.4f}**",
            f"- Avg PF: **{agg_p['avg_pf']:.3f}**",
            f"- Avg expectancy: **{agg_p['avg_exp_r']:.4f}R**",
            f"- Avg max DD: **{agg_p['avg_dd_r']:.2f}R**",
            f"- Avg trades/year: **{agg_p['avg_tpy']:.1f}**",
            "",
        ]

    if len(validated):
        top = validated.sort("expectancy_r", descending=True).head(15)
        lines += [
            "## Top 15 validated by expectancy",
            "",
            "| # | Sym | Session | Setup | Dir | Fam | TP | SL | Fric_R | N | WR | PF | Exp(R) | DD(R) | T/yr | WF | MC | Decay |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
        ]
        for i, r in enumerate(top.iter_rows(named=True), 1):
            lines.append(
                f"| {i} | {r['symbol']} | {r['session']} | {r['setup_type']} "
                f"| {r['direction_mode']} | {r['family']} | {r['tp_atr_mult']} "
                f"| {r['sl_atr_mult']} | {r['friction_r_used']:.3f} "
                f"| {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.2f} "
                f"| {r['expectancy_r']:.3f} | {r['max_dd_r']:.2f} "
                f"| {r['trades_per_year']:.1f} | {r['wf_ratio']:.2f} "
                f"| {r['mc_ruin']:.3f} | {r['decay_ratio']:.2f} |"
            )

    if len(portfolio):
        lines += [
            "",
            "## Final consolidated portfolio",
            "",
            "| # | Sym | Session | Setup | Dir | Fam | TP | SL | Fric_R | N | WR | PF | Exp(R) | DD(R) | T/yr |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
        ]
        for i, r in enumerate(portfolio.iter_rows(named=True), 1):
            lines.append(
                f"| {i} | {r['symbol']} | {r['session']} | {r['setup_type']} "
                f"| {r['direction_mode']} | {r['family']} | {r['tp_atr_mult']} "
                f"| {r['sl_atr_mult']} | {r['friction_r_used']:.3f} "
                f"| {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.2f} "
                f"| {r['expectancy_r']:.3f} | {r['max_dd_r']:.2f} "
                f"| {r['trades_per_year']:.1f} |"
            )

        # Per-symbol distribution
        per_sym = (portfolio
                   .group_by("symbol")
                   .agg([
                       pl.len().alias("n"),
                       pl.col("expectancy_r").mean().alias("avg_exp"),
                       pl.col("pf").mean().alias("avg_pf"),
                       pl.col("wr").mean().alias("avg_wr"),
                   ])
                   .sort("n", descending=True))
        lines += ["", "## Per-symbol distribution", "",
                  "| Sym | N | avg WR | avg PF | avg Exp(R) |",
                  "|---|---|---|---|---|"]
        for r in per_sym.iter_rows(named=True):
            lines.append(f"| {r['symbol']} | {r['n']} | {r['avg_wr']:.3f} "
                         f"| {r['avg_pf']:.2f} | {r['avg_exp']:.3f} |")

    (REPORTS_DIR / "Math_RealFriction_Final.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8")


def _write_portfolio_json(portfolio: pl.DataFrame) -> None:
    items = []
    for r in portfolio.iter_rows(named=True):
        items.append({
            "family": r["family"],
            "direction_mode": r["direction_mode"],
            "internal_sym": r["symbol"],
            "tf": "M15",
            "session": r["session"],
            "setup_type": r["setup_type"],
            "tp_atr_mult": float(r["tp_atr_mult"]),
            "sl_atr_mult": float(r["sl_atr_mult"]),
            "atr_period": 14,
            "friction_r_used": float(r["friction_r_used"]),
            "metrics": {
                "wr": float(r["wr"]),
                "pf": float(r["pf"]),
                "expectancy_r": float(r["expectancy_r"]),
                "net_r": float(r["net_r"]),
                "max_dd_r": float(r["max_dd_r"]),
                "trades_per_year": float(r["trades_per_year"]),
                "wf_ratio": float(r.get("wf_ratio", 0.0)),
                "mc_ruin": float(r.get("mc_ruin", 0.0)),
                "decay_ratio": float(r.get("decay_ratio", 0.0)),
            },
        })
    (REPORTS_DIR / "math_realfriction_strategies.json").write_text(
        json.dumps({
            "_doc": "Math edges rediscovered with REALISTIC friction "
                    "(friction_real + 0.2R slippage). RESEARCH ONLY — "
                    "not deployed to bot_config_math.json.",
            "n_strategies": len(items),
            "portfolio": items,
        }, indent=2),
        encoding="utf-8",
    )


# ───────────────────────── main ─────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=("a", "b", "c", "all"), default="all")
    ap.add_argument("--max-minutes", type=float, default=50.0,
                    help="Phase-A time budget (symbols scanned until exceeded)")
    args = ap.parse_args()
    t0 = _time.time()

    if args.phase in ("a", "all"):
        pa = run_phase_a(max_minutes=args.max_minutes)
    else:
        pa = pl.read_parquet(REPORTS_DIR / "math_realfriction_phase_a.parquet")

    if args.phase in ("b", "all"):
        pb = run_phase_b(pa)
    else:
        path = REPORTS_DIR / "math_realfriction_validated.parquet"
        pb = pl.read_parquet(path) if path.exists() else pl.DataFrame()

    if args.phase in ("c", "all"):
        pc = run_phase_c(pb)
    else:
        path = REPORTS_DIR / "math_realfriction_portfolio.parquet"
        pc = pl.read_parquet(path) if path.exists() else pl.DataFrame()

    _write_main_report(pa, pb, pc)
    if len(pc):
        _write_portfolio_json(pc)

    elapsed = (_time.time() - t0) / 60.0
    print(f"\nDONE — elapsed {elapsed:.1f} min")
    print(f"  Phase A: {len(pa)} strategies passed gates")
    print(f"  Phase B: {len(pb)} validated (WF/MC/decay)")
    print(f"  Phase C: {len(pc)} final portfolio")


if __name__ == "__main__":
    main()
