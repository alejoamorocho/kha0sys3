"""Robustness validation for Optuna 3-regime math strategies.

For each of the 35 strategies with optimized TP/SL from optuna_3regime_results.parquet:
  - Regenerate trade ledger using best_tp/best_sl + realistic friction
  - Monte Carlo ruin (10k bootstrap of trade order)
  - Walk-Forward (50/50 train/test)
  - Decay analysis (yearly window WR/PF trend)
  - Classification: FUERTE / ACEPTABLE / DEBIL / MUERTA

Output:
  reports/robustness_math_optuna.parquet
  reports/Robustness_Math_Optuna.md
"""
from __future__ import annotations
import time
from pathlib import Path
import numpy as np
import polars as pl

from src.domain.constants import INDICATOR_SESSIONS
from src.engine.indicator_validation import compute_metrics
from src.engine.run_math_discovery import _load_and_enrich_math
from src.engine.run_indicator_discovery import _filter_by_session
from src.engine.run_math_momentum import (
    detect_setups as detect_mom, run_backtest as run_mom_bt, BacktestConfig as MomCfg,
)
from src.engine.run_math_fade import (
    detect_setups as detect_fade, run_backtest as run_fade_bt, BacktestConfig as FadeCfg,
)
from src.engine.friction_real import friction_r, load_median_atr

REPORTS_DIR = Path("reports")
FADE_SETUPS = {"KALMAN_PEAK_FADE", "ZSCORE_EXTREME_FADE", "OLS_EXTREME_FADE",
               "CURVATURE_PEAK_FADE", "GARCH_Z_FADE", "AREA_EXTREME_FADE"}

MC_N = 10_000
SEED = 42


def _flip(df: pl.DataFrame) -> pl.DataFrame:
    if len(df) == 0:
        return df
    return df.with_columns([
        pl.when(pl.col("direction") == "LONG").then(pl.lit("SHORT"))
          .otherwise(pl.lit("LONG")).alias("direction")
    ])


def _backtest(strat, bars, sigs, tp, sl, median_atr):
    sym = strat["symbol"]; ses = strat["session"]; setup = strat["setup_type"]
    fric_R = friction_r(sym, sl, median_atr) + 0.2
    se_h = INDICATOR_SESSIONS[ses][1]
    if setup in FADE_SETUPS:
        cfg = FadeCfg(tp_atr_mult=tp, sl_atr_mult=sl, session_end_hour_utc=se_h, friction_r=fric_R)
        return run_fade_bt(sigs, bars, setup, cfg, sym)
    cfg = MomCfg(tp_atr_mult=tp, sl_atr_mult=sl, session_end_hour_utc=se_h, friction_r=fric_R)
    return run_mom_bt(sigs, bars, setup, cfg, sym)


def monte_carlo_ruin(r_series: np.ndarray, n_runs: int = MC_N, ruin_dd: float = 30.0):
    """Bootstrap shuffle trade order, count runs that hit -ruin_dd cumulative R."""
    rng = np.random.default_rng(SEED)
    n = len(r_series)
    if n < 30:
        return {"ruin_pct": 100.0, "p5_net": 0.0, "p50_net": 0.0, "p95_net": 0.0,
                "p5_dd": 999.0, "p50_dd": 999.0}
    nets = np.empty(n_runs); dds = np.empty(n_runs); ruins = 0
    for i in range(n_runs):
        idx = rng.permutation(n)
        cum = np.cumsum(r_series[idx])
        peak = np.maximum.accumulate(cum)
        dd = (peak - cum).max()
        nets[i] = cum[-1]; dds[i] = dd
        if dd >= ruin_dd:
            ruins += 1
    return {
        "ruin_pct": 100.0 * ruins / n_runs,
        "p5_net": float(np.percentile(nets, 5)),
        "p50_net": float(np.percentile(nets, 50)),
        "p95_net": float(np.percentile(nets, 95)),
        "p5_dd": float(np.percentile(dds, 95)),  # worst-case DD percentile
        "p50_dd": float(np.percentile(dds, 50)),
    }


def walk_forward(trades: pl.DataFrame):
    """50/50 split: train metrics vs test metrics, degradation = (train - test) / train."""
    if len(trades) < 40:
        return None
    sorted_t = trades.sort("time")
    n = len(sorted_t); mid = n // 2
    train = sorted_t[:mid]; test = sorted_t[mid:]
    m_tr = compute_metrics(train); m_te = compute_metrics(test)
    deg_wr = (m_tr.wr - m_te.wr) / max(m_tr.wr, 0.01) * 100
    deg_pf = (m_tr.profit_factor - m_te.profit_factor) / max(m_tr.profit_factor, 0.01) * 100
    return {
        "wr_train": m_tr.wr, "wr_test": m_te.wr, "deg_wr": deg_wr,
        "pf_train": m_tr.profit_factor, "pf_test": m_te.profit_factor, "deg_pf": deg_pf,
        "exp_train": m_tr.expectancy_r, "exp_test": m_te.expectancy_r,
    }


def decay_analysis(trades: pl.DataFrame):
    """Split into yearly windows; compute WR per year and slope."""
    if len(trades) < 40:
        return None
    df = trades.sort("time").with_columns(pl.col("time").dt.year().alias("y"))
    by_y = df.group_by("y").agg([
        pl.len().alias("n"),
        (pl.col("r_multiple") > 0).cast(pl.Float64).mean().alias("wr"),
        pl.col("r_multiple").sum().alias("net_r"),
    ]).sort("y").filter(pl.col("n") >= 10)
    if len(by_y) < 2:
        return None
    years = by_y["y"].to_numpy().astype(float)
    wrs = by_y["wr"].to_numpy()
    if len(years) >= 2 and years.std() > 0:
        slope = float(np.polyfit(years, wrs, 1)[0])
    else:
        slope = 0.0
    label = "MEJORANDO" if slope > 0.005 else ("ESTABLE" if slope > -0.01 else "DEGRADANDO")
    return {
        "yearly_wrs": wrs.tolist(),
        "yearly_years": years.astype(int).tolist(),
        "slope": slope,
        "label": label,
    }


def classify(mc, wf, dec, net_r):
    flags = []
    if mc["ruin_pct"] > 5.0: flags.append("ruin>5%")
    if mc["p5_net"] < 0: flags.append("MC P5<0")
    if wf and wf["deg_wr"] > 15: flags.append("WF deg WR>15%")
    if wf and wf["pf_test"] < 1.0: flags.append("PF OOS<1")
    if dec and dec["label"] == "DEGRADANDO": flags.append("decay-")
    if net_r < 0: flags.append("net-")

    if not flags and mc["ruin_pct"] < 1.0 and (wf is None or wf["deg_wr"] < 5):
        return "FUERTE", flags
    if mc["ruin_pct"] < 5 and mc["p5_net"] >= 0 and (wf is None or wf["pf_test"] >= 1.0):
        return "ACEPTABLE", flags
    if mc["ruin_pct"] > 20 or (wf and wf["pf_test"] < 0.8):
        return "MUERTA", flags
    return "DEBIL", flags


def main():
    portfolio = pl.read_parquet(REPORTS_DIR / "optuna_3regime_results.parquet")
    print(f"Robustness on {len(portfolio)} optuna-optimized math strategies\n")

    bar_cache = {}; sig_cache = {}
    rows = []
    t0 = time.time()

    for i, strat in enumerate(portfolio.iter_rows(named=True), 1):
        sym = strat["symbol"]; setup = strat["setup_type"]
        direction = strat["direction_mode"]; ses = strat["session"]
        tp = float(strat["best_tp"]); sl = float(strat["best_sl"])
        try:
            if sym not in bar_cache:
                bar_cache[sym] = _load_and_enrich_math(sym)
            bars = bar_cache[sym]
            ck = (sym, setup, direction)
            if ck not in sig_cache:
                raw = detect_fade(bars, setup) if setup in FADE_SETUPS else detect_mom(bars, setup)
                sig_cache[ck] = raw
            sigs = _filter_by_session(sig_cache[ck], ses)
            if direction == "INVERT":
                sigs = _flip(sigs)
            median_atr = load_median_atr(sym)
            trades = _backtest(strat, bars, sigs, tp, sl, median_atr)
            if len(trades) < 30:
                print(f"  [{i:02d}/{len(portfolio)}] {sym}/{ses}/{setup}: skip (n<30)")
                continue
            r_series = trades["r_multiple"].to_numpy()
            net_r = float(r_series.sum())
            m = compute_metrics(trades)

            mc = monte_carlo_ruin(r_series)
            wf = walk_forward(trades)
            dec = decay_analysis(trades)
            label, flags = classify(mc, wf, dec, net_r)

            row = {
                "symbol": sym, "session": ses, "setup_type": setup, "direction_mode": direction,
                "regime": strat["best_regime"], "tp": tp, "sl": sl, "rr": tp/sl,
                "n": m.n_trades, "wr": m.wr, "pf": m.profit_factor, "exp_r": m.expectancy_r,
                "net_r": net_r, "max_dd": m.max_dd_r, "tpy": m.trades_per_year,
                "mc_ruin_pct": mc["ruin_pct"], "mc_p5": mc["p5_net"], "mc_p50": mc["p50_net"],
                "mc_p95": mc["p95_net"], "mc_p95_dd": mc["p5_dd"],
                "wf_wr_tr": wf["wr_train"] if wf else None,
                "wf_wr_te": wf["wr_test"] if wf else None,
                "wf_pf_tr": wf["pf_train"] if wf else None,
                "wf_pf_te": wf["pf_test"] if wf else None,
                "wf_deg_wr": wf["deg_wr"] if wf else None,
                "wf_deg_pf": wf["deg_pf"] if wf else None,
                "decay_slope": dec["slope"] if dec else None,
                "decay_label": dec["label"] if dec else "N/A",
                "label": label, "flags": ",".join(flags) if flags else "-",
            }
            rows.append(row)
            elapsed = (time.time() - t0) / 60
            print(f"  [{i:02d}/{len(portfolio)}] {sym}/{ses}/{setup}/{direction}: "
                  f"{label} | PF={m.profit_factor:.2f} OOS={wf['pf_test']:.2f} "
                  f"ruin={mc['ruin_pct']:.1f}% decay={dec['label'] if dec else '-'} ({elapsed:.1f}m)")
        except Exception as e:
            print(f"  [{i:02d}/{len(portfolio)}] {sym} err: {e}")

    if not rows:
        print("No results")
        return

    df = pl.DataFrame(rows)
    df.write_parquet(REPORTS_DIR / "robustness_math_optuna.parquet")

    from collections import Counter
    cls_counter = Counter(r["label"] for r in rows)
    print("\n=== CLASSIFICATION ===")
    for k in ["FUERTE", "ACEPTABLE", "DEBIL", "MUERTA"]:
        print(f"  {k}: {cls_counter.get(k, 0)}")

    keepable = [r for r in rows if r["label"] in ("FUERTE", "ACEPTABLE")]
    print(f"\nKeepable: {len(keepable)}/{len(rows)}")
    if keepable:
        avg_wr = np.mean([r["wr"] for r in keepable])
        avg_pf = np.mean([r["pf"] for r in keepable])
        avg_pf_oos = np.mean([r["wf_pf_te"] for r in keepable if r["wf_pf_te"] is not None])
        avg_ruin = np.mean([r["mc_ruin_pct"] for r in keepable])
        sum_net = np.sum([r["net_r"] for r in keepable])
        print(f"Avg WR     : {avg_wr:.3f}")
        print(f"Avg PF (IS): {avg_pf:.2f}")
        print(f"Avg PF OOS : {avg_pf_oos:.2f}")
        print(f"Avg MC ruin: {avg_ruin:.2f}%")
        print(f"Sum net R  : {sum_net:.1f}")

    md = ["# Robustness — Optuna 3-Regime Math Portfolio", "",
          f"Tested on {len(rows)} strategies with optimized TP/SL.",
          f"Realistic Vantage friction + 0.2R slippage. MC=10k.", "",
          "## Classification distribution", ""]
    for k in ["FUERTE", "ACEPTABLE", "DEBIL", "MUERTA"]:
        md.append(f"- **{k}**: {cls_counter.get(k, 0)}")
    md += ["", "## Per-strategy results", "",
           "| Symbol | Sess | Setup | Dir | TP/SL | RR | n | WR | PF | PF OOS | DegWR% | Ruin% | P5 | Decay | Label | Flags |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda x: (
        {"FUERTE": 0, "ACEPTABLE": 1, "DEBIL": 2, "MUERTA": 3}[x["label"]],
        -x["pf"],
    )):
        wfp = f"{r['wf_pf_te']:.2f}" if r["wf_pf_te"] is not None else "-"
        wfd = f"{r['wf_deg_wr']:+.1f}" if r["wf_deg_wr"] is not None else "-"
        md.append(
            f"| {r['symbol']} | {r['session']} | {r['setup_type']} | {r['direction_mode']} "
            f"| {r['tp']:.2f}/{r['sl']:.2f} | {r['rr']:.2f} | {r['n']} "
            f"| {r['wr']:.3f} | {r['pf']:.2f} | {wfp} | {wfd} "
            f"| {r['mc_ruin_pct']:.1f} | {r['mc_p5']:+.1f} | {r['decay_label']} "
            f"| **{r['label']}** | {r['flags']} |"
        )
    (REPORTS_DIR / "Robustness_Math_Optuna.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"\nReport: reports/Robustness_Math_Optuna.md")


if __name__ == "__main__":
    main()
