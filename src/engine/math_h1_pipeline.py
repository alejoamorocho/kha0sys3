"""Math portfolio pipeline on H1 (vs the live M15 portfolio).

Same 5 setups (OLS_SLOPE_STRONG, HURST_TREND_MOM, KALMAN_INNOV_EXPAND,
SPECTRAL_TREND_MOM, GARCH_Z_FADE), same 9 symbols, same 5 sessions, same
realistic Vantage friction + 0.2R slippage — but on H1 bars instead of M15.

Goal: see if the math edge survives at higher timeframe (typically less
noise, fewer trades, larger per-trade R).

Pipeline:
  Phase A: discovery grid (TP × SL × NORMAL/INVERT)
  Phase B: filter (trades/yr ≥ 15, WR > 0.50, PF > 1.0) — lower TPY gate because H1
  Phase C: 3-regime Optuna per survivor
  Phase D: robustness (MC=10k + WF + decay)

Outputs:
  reports/Math_H1_Phase_A.md / .parquet
  reports/Math_H1_Phase_B.md / .parquet
  reports/Math_H1_Optuna.md / .parquet
  reports/Math_H1_Robustness.md / .parquet
"""
from __future__ import annotations

import time
from collections import Counter
from pathlib import Path

import numpy as np
import optuna
import polars as pl

from src.application.math_indicators import MathIndicatorEnricher
from src.domain.constants import INDICATOR_SESSIONS
from src.engine.indicator_validation import compute_metrics
from src.engine.run_indicator_discovery import _load_and_enrich, _filter_by_session
from src.engine.run_math_fade import (
    BacktestConfig as FadeCfg,
    detect_setups as detect_fade,
    run_backtest as run_fade_bt,
)
from src.engine.run_math_momentum import (
    BacktestConfig as MomCfg,
    detect_setups as detect_mom,
    run_backtest as run_mom_bt,
)
from src.engine.friction_real import friction_r, load_median_atr

REPORTS_DIR = Path("reports")
H1_CACHE = Path("data/enriched_math_h1")
TF = "H1"

SYMBOLS = ["AUDUSD", "EURJPY", "EURUSD", "GBPAUD", "GBPJPY",
           "GBPUSD", "USDJPY", "XAGUSD", "XAUUSD"]
SETUPS_MOM = ["OLS_SLOPE_STRONG", "HURST_TREND_MOM", "KALMAN_INNOV_EXPAND",
              "SPECTRAL_TREND_MOM"]
SETUPS_FADE = ["GARCH_Z_FADE"]
ALL_SETUPS = SETUPS_MOM + SETUPS_FADE
FADE_SET = set(SETUPS_FADE)
SESSIONS = list(INDICATOR_SESSIONS.keys())
DIRECTIONS = ["NORMAL", "INVERT"]

# Phase A grid (kept tight to be tractable on H1)
TP_GRID_A = [0.5, 0.75, 1.0, 1.5, 2.0]
SL_GRID_A = [0.5, 0.75, 1.0, 1.5, 2.0]

# Phase B filter (H1 → fewer trades, lower TPY gate)
PB_MIN_TPY = 15
PB_MIN_WR = 0.50
PB_MIN_PF = 1.0
PB_MIN_EXP = 0.05

# Optuna
N_TRIALS_PER_REGIME = 60
SEED = 42
REGIMES = {
    "HIGH_RR":  {"tp_lo": 1.0, "tp_hi": 4.0, "sl_lo": 0.3, "sl_hi": 1.5},
    "BALANCED": {"tp_lo": 0.5, "tp_hi": 2.0, "sl_lo": 0.5, "sl_hi": 2.0},
    "HIGH_WR":  {"tp_lo": 0.3, "tp_hi": 1.5, "sl_lo": 1.0, "sl_hi": 4.0},
}

# Robustness
MC_N = 10_000
RUIN_DD = 30.0

optuna.logging.set_verbosity(optuna.logging.WARNING)


def _flip(df: pl.DataFrame) -> pl.DataFrame:
    if len(df) == 0:
        return df
    return df.with_columns([
        pl.when(pl.col("direction") == "LONG").then(pl.lit("SHORT"))
          .otherwise(pl.lit("LONG")).alias("direction")
    ])


def _load_h1_math(symbol: str) -> pl.DataFrame:
    cache = H1_CACHE / f"{symbol}_{TF}.parquet"
    if cache.exists():
        return pl.read_parquet(cache)
    H1_CACHE.mkdir(parents=True, exist_ok=True)
    bars = _load_and_enrich(symbol, TF)
    bars = MathIndicatorEnricher.enrich_all_math(bars)
    bars.write_parquet(cache)
    return bars


def _backtest(setup: str, sym: str, ses: str, sigs, bars,
              tp: float, sl: float, median_atr: float):
    fric_R = friction_r(sym, sl, median_atr) + 0.2
    se_h = INDICATOR_SESSIONS[ses][1]
    if setup in FADE_SET:
        cfg = FadeCfg(tp_atr_mult=tp, sl_atr_mult=sl,
                      session_end_hour_utc=se_h, friction_r=fric_R)
        return run_fade_bt(sigs, bars, setup, cfg, sym)
    cfg = MomCfg(tp_atr_mult=tp, sl_atr_mult=sl,
                 session_end_hour_utc=se_h, friction_r=fric_R)
    return run_mom_bt(sigs, bars, setup, cfg, sym)


# ─── Phase A ──────────────────────────────────────────────────────────

def phase_a():
    print(f"=== Phase A (H1) ===")
    print(f"Symbols: {len(SYMBOLS)} | Setups: {len(ALL_SETUPS)} | "
          f"Sessions: {len(SESSIONS)} | TP: {len(TP_GRID_A)} | "
          f"SL: {len(SL_GRID_A)} | Dirs: {len(DIRECTIONS)}")
    rows = []
    bar_cache = {}
    sig_cache = {}
    t0 = time.time()
    total = (len(SYMBOLS) * len(ALL_SETUPS) * len(SESSIONS) *
             len(DIRECTIONS) * len(TP_GRID_A) * len(SL_GRID_A))
    print(f"Total combos: {total}")

    cnt = 0
    for sym in SYMBOLS:
        try:
            if sym not in bar_cache:
                bar_cache[sym] = _load_h1_math(sym)
            bars = bar_cache[sym]
            median_atr = load_median_atr(sym)
        except Exception as e:
            print(f"  [SKIP] {sym}: {e}")
            continue
        for setup in ALL_SETUPS:
            for direction in DIRECTIONS:
                ck = (sym, setup, direction)
                if ck not in sig_cache:
                    try:
                        raw = (detect_fade(bars, setup) if setup in FADE_SET
                               else detect_mom(bars, setup))
                    except Exception as e:
                        print(f"  [SKIP detect] {sym}/{setup}: {e}")
                        sig_cache[ck] = None
                        continue
                    if direction == "INVERT":
                        raw = _flip(raw)
                    sig_cache[ck] = raw
                raw = sig_cache[ck]
                if raw is None:
                    continue
                for ses in SESSIONS:
                    sigs = _filter_by_session(raw, ses)
                    if len(sigs) < 20:
                        cnt += len(TP_GRID_A) * len(SL_GRID_A)
                        continue
                    for tp in TP_GRID_A:
                        for sl in SL_GRID_A:
                            cnt += 1
                            try:
                                trades = _backtest(setup, sym, ses, sigs, bars,
                                                   tp, sl, median_atr)
                            except Exception:
                                continue
                            if len(trades) < 30:
                                continue
                            m = compute_metrics(trades)
                            rows.append({
                                "symbol": sym, "setup_type": setup,
                                "session": ses, "direction_mode": direction,
                                "tp": tp, "sl": sl, "rr": tp / sl,
                                "n": m.n_trades, "wr": m.wr,
                                "pf": m.profit_factor,
                                "exp_r": m.expectancy_r,
                                "max_dd_r": m.max_dd_r,
                                "tpy": m.trades_per_year,
                            })
        elapsed = (time.time() - t0) / 60
        print(f"  {sym}: {cnt}/{total} combos done | {len(rows)} kept | {elapsed:.1f}m")

    if not rows:
        print("Phase A: no rows")
        return pl.DataFrame()
    df = pl.DataFrame(rows)
    df.write_parquet(REPORTS_DIR / "math_h1_phase_a.parquet")
    print(f"Phase A: {len(df)} surviving combos")
    return df


# ─── Phase B ──────────────────────────────────────────────────────────

def phase_b(phase_a_df: pl.DataFrame) -> pl.DataFrame:
    print(f"\n=== Phase B filter ===")
    df = phase_a_df.filter(
        (pl.col("tpy") >= PB_MIN_TPY) &
        (pl.col("wr") >= PB_MIN_WR) &
        (pl.col("pf") >= PB_MIN_PF) &
        (pl.col("exp_r") >= PB_MIN_EXP)
    )
    # Per (symbol, session, setup, direction_mode), keep best by (pf * exp_r)
    df = df.with_columns(
        (pl.col("pf") * pl.col("exp_r")).alias("score")
    ).sort("score", descending=True).group_by(
        ["symbol", "session", "setup_type", "direction_mode"]
    ).agg(pl.all().first()).drop("score")
    df.write_parquet(REPORTS_DIR / "math_h1_phase_b.parquet")
    print(f"Phase B: {len(df)} unique (sym, sess, setup, dir) survivors")
    return df


# ─── Phase C: 3-regime Optuna ────────────────────────────────────────

def optimize_strat(strat, bars, sigs, median_atr, regime_name, bounds, n_trials):
    sym = strat["symbol"]; ses = strat["session"]; setup = strat["setup_type"]

    def objective(trial):
        tp = round(trial.suggest_float("tp", bounds["tp_lo"], bounds["tp_hi"], step=0.1), 2)
        sl = round(trial.suggest_float("sl", bounds["sl_lo"], bounds["sl_hi"], step=0.1), 2)
        try:
            trades = _backtest(setup, sym, ses, sigs, bars, tp, sl, median_atr)
        except Exception:
            return -1.0
        if len(trades) < 20:
            return -1.0
        m = compute_metrics(trades)
        if m.trades_per_year < PB_MIN_TPY or m.wr < 0.50 or m.profit_factor < 1.0:
            return -1.0
        atr_per_trade = float(m.expectancy_r) * sl
        annual_atr = atr_per_trade * float(m.trades_per_year)
        dd_pen = max(float(m.max_dd_r), 1.0)
        return annual_atr / dd_pen

    study = optuna.create_study(direction="maximize",
                                sampler=optuna.samplers.TPESampler(seed=SEED))
    study.optimize(objective, n_trials=n_trials, show_progress_bar=False)
    if study.best_value <= 0:
        return None
    tp = study.best_params["tp"]; sl = study.best_params["sl"]
    trades = _backtest(setup, sym, ses, sigs, bars, tp, sl, median_atr)
    m = compute_metrics(trades)
    return {
        "regime": regime_name,
        "tp": float(tp), "sl": float(sl),
        "rr": round(tp/sl, 2),
        "n": m.n_trades, "wr": m.wr, "pf": m.profit_factor,
        "exp_r": m.expectancy_r, "dd_r": m.max_dd_r,
        "tpy": m.trades_per_year,
        "objective_score": float(study.best_value),
    }


def phase_c_optuna(phase_b_df: pl.DataFrame) -> pl.DataFrame:
    print(f"\n=== Phase C: 3-regime Optuna on {len(phase_b_df)} survivors ===")
    bar_cache = {}; sig_cache = {}
    best_rows = []
    t0 = time.time()
    for i, strat in enumerate(phase_b_df.iter_rows(named=True), 1):
        sym = strat["symbol"]; setup = strat["setup_type"]
        direction = strat["direction_mode"]; ses = strat["session"]
        try:
            if sym not in bar_cache:
                bar_cache[sym] = _load_h1_math(sym)
            bars = bar_cache[sym]
            ck = (sym, setup, direction)
            if ck not in sig_cache:
                raw = (detect_fade(bars, setup) if setup in FADE_SET
                       else detect_mom(bars, setup))
                if direction == "INVERT":
                    raw = _flip(raw)
                sig_cache[ck] = raw
            sigs = _filter_by_session(sig_cache[ck], ses)
            if len(sigs) < 30:
                continue
            median_atr = load_median_atr(sym)

            results = []
            for rn, b in REGIMES.items():
                r = optimize_strat(strat, bars, sigs, median_atr, rn, b, N_TRIALS_PER_REGIME)
                if r is not None:
                    r.update({"symbol": sym, "session": ses,
                              "setup_type": setup, "direction_mode": direction})
                    results.append(r)
            if not results:
                continue
            best = max(results, key=lambda x: x["objective_score"])
            best_rows.append(best)
            elapsed = (time.time() - t0) / 60
            print(f"  [{i:02d}/{len(phase_b_df)}] {sym}/{ses}/{setup}/{direction}: "
                  f"best={best['regime']} TP={best['tp']}/SL={best['sl']} "
                  f"PF={best['pf']:.2f} exp={best['exp_r']:+.3f} ({elapsed:.1f}m)")
        except Exception as e:
            print(f"  [{i:02d}/{len(phase_b_df)}] {sym} err: {e}")

    if not best_rows:
        print("Optuna: no winners")
        return pl.DataFrame()
    df = pl.DataFrame(best_rows)
    df.write_parquet(REPORTS_DIR / "math_h1_optuna.parquet")
    print(f"\nRegime distribution: {Counter(r['regime'] for r in best_rows)}")
    return df


# ─── Phase D: robustness ────────────────────────────────────────────

def mc_ruin(r_series, n=MC_N, ruin_dd=RUIN_DD):
    if len(r_series) < 30:
        return {"ruin_pct": 100.0, "p5_net": 0.0, "p50_net": 0.0, "p95_net": 0.0}
    rng = np.random.default_rng(SEED)
    nets = np.empty(n); ruins = 0
    for i in range(n):
        idx = rng.permutation(len(r_series))
        cum = np.cumsum(r_series[idx])
        peak = np.maximum.accumulate(cum)
        if (peak - cum).max() >= ruin_dd:
            ruins += 1
        nets[i] = cum[-1]
    return {"ruin_pct": 100.0 * ruins / n,
            "p5_net": float(np.percentile(nets, 5)),
            "p50_net": float(np.percentile(nets, 50)),
            "p95_net": float(np.percentile(nets, 95))}


def walk_forward(trades):
    if len(trades) < 40:
        return None
    s = trades.sort("time")
    n = len(s); mid = n // 2
    tr = compute_metrics(s[:mid]); te = compute_metrics(s[mid:])
    return {"wr_tr": tr.wr, "wr_te": te.wr,
            "pf_tr": tr.profit_factor, "pf_te": te.profit_factor,
            "deg_wr": (tr.wr - te.wr) / max(tr.wr, 0.01) * 100}


def decay(trades):
    if len(trades) < 40:
        return None
    df = trades.sort("time").with_columns(pl.col("time").dt.year().alias("y"))
    g = df.group_by("y").agg([
        pl.len().alias("n"),
        (pl.col("r_multiple") > 0).cast(pl.Float64).mean().alias("wr"),
    ]).sort("y").filter(pl.col("n") >= 5)
    if len(g) < 2:
        return None
    yrs = g["y"].to_numpy().astype(float); wrs = g["wr"].to_numpy()
    slope = float(np.polyfit(yrs, wrs, 1)[0]) if yrs.std() > 0 else 0.0
    label = "MEJORANDO" if slope > 0.005 else ("ESTABLE" if slope > -0.01 else "DEGRADANDO")
    return {"slope": slope, "label": label}


def classify(mc, wf, dec, net_r):
    flags = []
    if mc["ruin_pct"] > 5: flags.append("ruin>5%")
    if mc["p5_net"] < 0: flags.append("MC P5<0")
    if wf and abs(wf["deg_wr"]) > 15: flags.append("WF deg>15%")
    if wf and wf["pf_te"] < 1.0: flags.append("PF OOS<1")
    if dec and dec["label"] == "DEGRADANDO": flags.append("decay-")
    if net_r < 0: flags.append("net-")
    if not flags and mc["ruin_pct"] < 1 and (wf is None or abs(wf["deg_wr"]) < 5):
        return "FUERTE", flags
    if mc["ruin_pct"] < 5 and mc["p5_net"] >= 0 and (wf is None or wf["pf_te"] >= 1.0):
        return "ACEPTABLE", flags
    if mc["ruin_pct"] > 20 or (wf and wf["pf_te"] < 0.8):
        return "MUERTA", flags
    return "DEBIL", flags


def phase_d_robustness(opt_df: pl.DataFrame) -> pl.DataFrame:
    print(f"\n=== Phase D: robustness on {len(opt_df)} optuna survivors ===")
    bar_cache = {}; sig_cache = {}
    rows = []
    for i, strat in enumerate(opt_df.iter_rows(named=True), 1):
        sym = strat["symbol"]; setup = strat["setup_type"]
        direction = strat["direction_mode"]; ses = strat["session"]
        tp = float(strat["tp"]); sl = float(strat["sl"])
        try:
            if sym not in bar_cache:
                bar_cache[sym] = _load_h1_math(sym)
            bars = bar_cache[sym]
            ck = (sym, setup, direction)
            if ck not in sig_cache:
                raw = (detect_fade(bars, setup) if setup in FADE_SET
                       else detect_mom(bars, setup))
                if direction == "INVERT":
                    raw = _flip(raw)
                sig_cache[ck] = raw
            sigs = _filter_by_session(sig_cache[ck], ses)
            median_atr = load_median_atr(sym)
            trades = _backtest(setup, sym, ses, sigs, bars, tp, sl, median_atr)
            if len(trades) < 30:
                continue
            r_arr = trades["r_multiple"].to_numpy()
            net_r = float(r_arr.sum())
            m = compute_metrics(trades)
            mc = mc_ruin(r_arr); wf = walk_forward(trades); dec = decay(trades)
            label, flags = classify(mc, wf, dec, net_r)
            rows.append({
                "symbol": sym, "session": ses, "setup_type": setup,
                "direction_mode": direction, "regime": strat["regime"],
                "tp": tp, "sl": sl, "rr": tp/sl,
                "n": m.n_trades, "wr": m.wr, "pf": m.profit_factor,
                "exp_r": m.expectancy_r, "net_r": net_r,
                "max_dd": m.max_dd_r, "tpy": m.trades_per_year,
                "mc_ruin": mc["ruin_pct"], "mc_p5": mc["p5_net"],
                "wf_pf_tr": wf["pf_tr"] if wf else None,
                "wf_pf_te": wf["pf_te"] if wf else None,
                "wf_deg_wr": wf["deg_wr"] if wf else None,
                "decay": dec["label"] if dec else "N/A",
                "label": label, "flags": ",".join(flags) or "-",
            })
            print(f"  [{i:02d}/{len(opt_df)}] {sym}/{ses}/{setup}/{direction}: "
                  f"{label} | PF={m.profit_factor:.2f} OOS={(wf['pf_te'] if wf else 0):.2f} "
                  f"ruin={mc['ruin_pct']:.1f}%")
        except Exception as e:
            print(f"  [{i:02d}] {sym} err: {e}")

    if not rows:
        return pl.DataFrame()
    df = pl.DataFrame(rows)
    df.write_parquet(REPORTS_DIR / "math_h1_robustness.parquet")
    cls = Counter(r["label"] for r in rows)
    print(f"\n=== Classification ===")
    for k in ["FUERTE", "ACEPTABLE", "DEBIL", "MUERTA"]:
        print(f"  {k}: {cls.get(k, 0)}")
    keep = [r for r in rows if r["label"] in ("FUERTE", "ACEPTABLE")]
    print(f"\nKeepable: {len(keep)}/{len(rows)}")
    if keep:
        avg_pf = float(np.mean([r["pf"] for r in keep]))
        avg_pf_oos = float(np.mean([r["wf_pf_te"] for r in keep if r["wf_pf_te"]]))
        avg_ruin = float(np.mean([r["mc_ruin"] for r in keep]))
        sum_net = float(np.sum([r["net_r"] for r in keep]))
        print(f"Avg PF IS    : {avg_pf:.2f}")
        print(f"Avg PF OOS   : {avg_pf_oos:.2f}")
        print(f"Avg MC ruin  : {avg_ruin:.2f}%")
        print(f"Sum NetR     : {sum_net:.1f}")

    md_lines = ["# Math H1 Pipeline — Robustness", "",
                f"Tested {len(rows)} H1 strategies (vs M15 portfolio of 35).",
                "Same setups, symbols, sessions, friction. Higher TF.", "",
                "## Classification distribution", ""]
    for k in ["FUERTE", "ACEPTABLE", "DEBIL", "MUERTA"]:
        md_lines.append(f"- **{k}**: {cls.get(k, 0)}")
    md_lines += ["", "## Per-strategy", "",
                 "| Symbol | Sess | Setup | Dir | Regime | TP/SL | RR | n | WR | PF | PF OOS | DegWR% | Ruin% | Decay | Label |",
                 "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda x: ({"FUERTE":0,"ACEPTABLE":1,"DEBIL":2,"MUERTA":3}[x["label"]], -x["pf"])):
        wfp = f"{r['wf_pf_te']:.2f}" if r["wf_pf_te"] is not None else "-"
        wfd = f"{r['wf_deg_wr']:+.1f}" if r["wf_deg_wr"] is not None else "-"
        md_lines.append(
            f"| {r['symbol']} | {r['session']} | {r['setup_type']} | {r['direction_mode']} "
            f"| {r['regime']} | {r['tp']:.2f}/{r['sl']:.2f} | {r['rr']:.2f} | {r['n']} "
            f"| {r['wr']:.3f} | {r['pf']:.2f} | {wfp} | {wfd} | {r['mc_ruin']:.1f} "
            f"| {r['decay']} | **{r['label']}** |"
        )
    (REPORTS_DIR / "Math_H1_Robustness.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    return df


def main():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    pa = phase_a()
    if len(pa) == 0:
        return
    pb = phase_b(pa)
    if len(pb) == 0:
        print("Phase B: no survivors")
        return
    opt = phase_c_optuna(pb)
    if len(opt) == 0:
        print("Optuna: no winners")
        return
    phase_d_robustness(opt)
    print("\nDone. Reports:")
    print("  reports/math_h1_phase_a.parquet")
    print("  reports/math_h1_phase_b.parquet")
    print("  reports/math_h1_optuna.parquet")
    print("  reports/Math_H1_Robustness.md / .parquet")


if __name__ == "__main__":
    main()
