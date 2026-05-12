"""Robustness validation for the 75 deduped K3+M1mgmt strategies.

For each strategy:
  - Regenerate trades using the SAME M1 mgmt backtest as Phase A
  - Monte Carlo 10k bootstrap (gate DD >= 30R = ruin)
  - Walk-forward 50/50 (IS vs OOS metrics + degradation)
  - Decay analysis (yearly WR slope)
  - Classification: FUERTE / ACEPTABLE / DEBIL / MUERTA

Outputs:
  reports/k3m1_dedup75_robustness.parquet
  reports/K3M1_Dedup75_Robustness.md
"""
from __future__ import annotations

import gc
import time
from collections import Counter
from pathlib import Path

import numpy as np
import polars as pl

from src.engine.k3_universe_m1_mgmt import (
    _backtest_m1m_mgmt, _align_guard_to_m1, _signal_tf_minutes,
    _flip, load_tf, realistic_friction,
)
from src.engine.run_math_momentum import (
    detect_setups as detect_mom, _guard_indicator_col,
    BacktestConfig as MomCfg,
)
from src.engine.run_indicator_discovery import _filter_by_session
from src.engine.indicator_validation import compute_metrics
from src.engine.friction_real import load_median_atr
from src.domain.constants import INDICATOR_SESSIONS

REPORTS = Path("reports")
MC_N = 10_000
RUIN_DD = 30.0
SEED = 42


def mc_ruin(r: np.ndarray, n: int = MC_N, ruin: float = RUIN_DD) -> dict:
    if len(r) < 30:
        return {"ruin_pct": 100.0, "p5_net": 0.0, "p50_net": 0.0, "p95_net": 0.0,
                "p95_dd": 999.0}
    rng = np.random.default_rng(SEED)
    nets = np.empty(n); dds = np.empty(n); ruins = 0
    for i in range(n):
        idx = rng.permutation(len(r))
        cum = np.cumsum(r[idx])
        peak = np.maximum.accumulate(cum)
        dd = (peak - cum).max()
        nets[i] = cum[-1]; dds[i] = dd
        if dd >= ruin:
            ruins += 1
    return {
        "ruin_pct": 100.0 * ruins / n,
        "p5_net": float(np.percentile(nets, 5)),
        "p50_net": float(np.percentile(nets, 50)),
        "p95_net": float(np.percentile(nets, 95)),
        "p95_dd": float(np.percentile(dds, 95)),
    }


def walk_forward(trades: pl.DataFrame) -> dict | None:
    if len(trades) < 40:
        return None
    s = trades.sort("time")
    mid = len(s) // 2
    tr = compute_metrics(s[:mid])
    te = compute_metrics(s[mid:])
    deg_wr = (tr.wr - te.wr) / max(tr.wr, 0.01) * 100
    deg_pf = (tr.profit_factor - te.profit_factor) / max(tr.profit_factor, 0.01) * 100
    return {
        "wr_tr": tr.wr, "wr_te": te.wr, "deg_wr_pct": deg_wr,
        "pf_tr": tr.profit_factor, "pf_te": te.profit_factor, "deg_pf_pct": deg_pf,
        "exp_tr": tr.expectancy_r, "exp_te": te.expectancy_r,
    }


def decay(trades: pl.DataFrame) -> dict | None:
    if len(trades) < 40:
        return None
    df = trades.sort("time").with_columns(pl.col("time").dt.year().alias("y"))
    g = df.group_by("y").agg([
        pl.len().alias("n"),
        (pl.col("r_multiple") > 0).cast(pl.Float64).mean().alias("wr"),
        pl.col("r_multiple").sum().alias("net_r"),
    ]).sort("y").filter(pl.col("n") >= 10)
    if len(g) < 2:
        return None
    yrs = g["y"].to_numpy().astype(float)
    wrs = g["wr"].to_numpy()
    slope = float(np.polyfit(yrs, wrs, 1)[0]) if yrs.std() > 0 else 0.0
    label = ("MEJORANDO" if slope > 0.005
             else ("ESTABLE" if slope > -0.01 else "DEGRADANDO"))
    return {"slope": slope, "label": label,
            "yearly_wrs": wrs.tolist(), "yearly_years": yrs.astype(int).tolist()}


def classify(mc: dict, wf: dict | None, dec: dict | None, net_r: float, pf: float) -> tuple:
    flags = []
    if mc["ruin_pct"] > 5.0: flags.append("ruin>5%")
    if mc["p5_net"] < 0: flags.append("MC P5<0")
    if wf and abs(wf["deg_wr_pct"]) > 15: flags.append("WF deg WR>15%")
    if wf and wf["pf_te"] < 1.0: flags.append("PF OOS<1")
    if wf and wf["pf_te"] < pf * 0.6: flags.append("WF PF drop >40%")
    if dec and dec["label"] == "DEGRADANDO": flags.append("decay-")
    if net_r < 0: flags.append("net-")
    if pf < 1.2: flags.append("PF<1.2")

    if not flags and mc["ruin_pct"] < 1.0 and (wf is None or abs(wf["deg_wr_pct"]) < 5):
        return "FUERTE", flags
    if (mc["ruin_pct"] < 5 and mc["p5_net"] >= 0
        and (wf is None or wf["pf_te"] >= 1.0)
        and net_r > 0 and pf >= 1.2):
        return "ACEPTABLE", flags
    if mc["ruin_pct"] > 20 or (wf and wf["pf_te"] < 0.8) or net_r < 0:
        return "MUERTA", flags
    return "DEBIL", flags


def main():
    dedup = pl.read_parquet(REPORTS / "k3m1_dedup_best_session.parquet")
    print(f"Robustness on {len(dedup)} deduped strategies")

    # Group by symbol for memory efficiency
    rows = []
    t0 = time.time()
    symbols = sorted(dedup["symbol"].unique().to_list())
    for sym_i, sym in enumerate(symbols, 1):
        print(f"\n[{sym_i}/{len(symbols)}] {sym}: loading M1 ({time.time()-t0:.0f}s)...")
        try:
            m1 = load_tf(sym, "M1")
            m1_arr = m1.select(["open","high","low","close"]).to_numpy()
            m1_times = m1["time"].cast(pl.Int64).to_numpy()
        except Exception as e:
            print(f"  SKIP {sym}: {e}")
            continue
        median_atr = load_median_atr(sym)
        signal_bars_cache = {}

        sym_strats = dedup.filter(pl.col("symbol") == sym)
        for j, s in enumerate(sym_strats.iter_rows(named=True), 1):
            tf = s["signal_tf"]; setup = s["setup_type"]
            sess = s["session"]; direction = s["direction_mode"]
            tp = float(s["tp"]); sl = float(s["sl"])
            try:
                if tf not in signal_bars_cache:
                    signal_bars_cache[tf] = load_tf(sym, tf)
                bars = signal_bars_cache[tf]
                guard_col = _guard_indicator_col(setup)
                if guard_col not in bars.columns:
                    continue
                if tf == "M1":
                    m1_guard = bars[guard_col].to_numpy()
                else:
                    m1_guard = _align_guard_to_m1(m1_times, bars, guard_col,
                                                  _signal_tf_minutes(tf))
                raw = detect_mom(bars, setup)
                if direction == "INVERT":
                    raw = _flip(raw)
                sigs = _filter_by_session(raw, sess)
                if len(sigs) < 30:
                    continue
                se_h = INDICATOR_SESSIONS[sess][1]
                fric_R = realistic_friction(sym, sl, median_atr)
                cfg = MomCfg(tp_atr_mult=tp, sl_atr_mult=sl,
                             session_end_hour_utc=se_h, friction_r=fric_R)
                trades = _backtest_m1m_mgmt(sigs, m1_arr, m1_times, m1_guard,
                                            cfg, setup, _signal_tf_minutes(tf))
                if len(trades) < 30:
                    continue
                r_arr = trades["r_multiple"].to_numpy()
                net_r = float(r_arr.sum())
                m = compute_metrics(trades)
                pf = m.profit_factor
                mc = mc_ruin(r_arr)
                wf = walk_forward(trades)
                dec = decay(trades)
                label, flags = classify(mc, wf, dec, net_r, pf)
                rows.append({
                    "symbol": sym, "signal_tf": tf, "session": sess,
                    "setup_type": setup, "direction_mode": direction,
                    "tp": tp, "sl": sl, "rr": tp/sl,
                    "n": m.n_trades, "wr": m.wr, "pf": pf,
                    "exp_r": m.expectancy_r, "max_dd_r": m.max_dd_r,
                    "tpy": m.trades_per_year, "net_r": net_r,
                    "friction_r": round(fric_R, 4),
                    "mc_ruin_pct": mc["ruin_pct"], "mc_p5_net": mc["p5_net"],
                    "mc_p50_net": mc["p50_net"], "mc_p95_dd": mc["p95_dd"],
                    "wf_wr_tr": wf["wr_tr"] if wf else None,
                    "wf_wr_te": wf["wr_te"] if wf else None,
                    "wf_deg_wr_pct": wf["deg_wr_pct"] if wf else None,
                    "wf_pf_tr": wf["pf_tr"] if wf else None,
                    "wf_pf_te": wf["pf_te"] if wf else None,
                    "wf_deg_pf_pct": wf["deg_pf_pct"] if wf else None,
                    "decay_slope": dec["slope"] if dec else None,
                    "decay_label": dec["label"] if dec else "N/A",
                    "label": label, "flags": ",".join(flags) or "-",
                })
                elapsed = (time.time() - t0) / 60
                wfp = f"{wf['pf_te']:.2f}" if wf else "-"
                dl = dec["label"] if dec else "-"
                print(f"  [{j:02d}/{len(sym_strats)}] {tf}/{setup}/{sess}/{direction} "
                      f"tp={tp}/sl={sl}: {label} | PF={pf:.2f} OOS={wfp} "
                      f"ruin={mc['ruin_pct']:.1f}% decay={dl} ({elapsed:.1f}m)")
            except Exception as e:
                print(f"  [{j:02d}] {tf}/{setup}/{sess}/{direction} FAIL: {e}")
        del m1, m1_arr, m1_times
        signal_bars_cache.clear()
        gc.collect()

    if not rows:
        print("No results"); return

    df = pl.DataFrame(rows)
    df.write_parquet(REPORTS / "k3m1_dedup75_robustness.parquet")
    cls = Counter(r["label"] for r in rows)
    print(f"\n=== CLASSIFICATION ({len(rows)} strats) ===")
    for k in ["FUERTE", "ACEPTABLE", "DEBIL", "MUERTA"]:
        print(f"  {k}: {cls.get(k, 0)}")
    keep = [r for r in rows if r["label"] in ("FUERTE", "ACEPTABLE")]
    print(f"\nKeepable (FUERTE+ACEPTABLE): {len(keep)}/{len(rows)}")
    if keep:
        avg_wr = float(np.mean([r["wr"] for r in keep]))
        avg_pf = float(np.mean([r["pf"] for r in keep]))
        avg_pf_oos = float(np.mean([r["wf_pf_te"] for r in keep if r["wf_pf_te"] is not None]))
        avg_ruin = float(np.mean([r["mc_ruin_pct"] for r in keep]))
        sum_net = float(np.sum([r["net_r"] for r in keep]))
        sum_tpy = float(np.sum([r["tpy"] for r in keep]))
        print(f"Avg WR     : {avg_wr*100:.1f}%")
        print(f"Avg PF IS  : {avg_pf:.2f}")
        print(f"Avg PF OOS : {avg_pf_oos:.2f}")
        print(f"Avg MC ruin: {avg_ruin:.2f}%")
        print(f"Sum NetR 8y: {sum_net:.0f}")
        print(f"Sum tpy    : {sum_tpy:.0f}")

    # By TF
    print("\n=== Classification BY TF ===")
    by_tf = df.group_by(["signal_tf", "label"]).agg(pl.len().alias("n")).sort(["signal_tf","label"])
    print(by_tf)

    # Decay distribution
    print("\n=== Decay distribution ===")
    print(df.group_by("decay_label").agg(pl.len().alias("n")).sort("n", descending=True))

    # Markdown
    md = ["# K3+M1mgmt 75-strategy Robustness (FINAL)",
          "",
          f"Strategies: {len(df)}. All M1 management with realistic Vantage friction.",
          f"Backtest: 2018-01 → 2026-05 (~8.3 years). MC=10k bootstrap, WF 50/50, decay yearly.",
          "",
          "## Classification distribution", "",
          "| Label | Count |", "|---|---|"]
    for k in ["FUERTE", "ACEPTABLE", "DEBIL", "MUERTA"]:
        md.append(f"| **{k}** | {cls.get(k, 0)} |")

    md += ["", "## Aggregate (FUERTE + ACEPTABLE)", ""]
    if keep:
        md += [
            f"- Avg WR: {avg_wr*100:.1f}%",
            f"- Avg PF (IS): {avg_pf:.2f}",
            f"- Avg PF (OOS): {avg_pf_oos:.2f}",
            f"- Avg MC ruin: {avg_ruin:.2f}%",
            f"- Sum Net R 8y: {sum_net:.0f}",
            f"- Sum trades/year: {sum_tpy:.0f}",
            "",
        ]

    md += ["## Per-strategy (sorted by label then by PF OOS)", "",
           "| TF | Symbol | Setup | Sess | Dir | TP/SL | n | WR | PF IS | PF OOS | DegWR% | Ruin% | Decay | Label | Flags |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    label_order = {"FUERTE": 0, "ACEPTABLE": 1, "DEBIL": 2, "MUERTA": 3}
    sorted_rows = sorted(rows, key=lambda r: (label_order[r["label"]],
                                              -(r["wf_pf_te"] or 0)))
    for r in sorted_rows:
        wfp = f"{r['wf_pf_te']:.2f}" if r["wf_pf_te"] is not None else "-"
        deg = f"{r['wf_deg_wr_pct']:+.1f}" if r["wf_deg_wr_pct"] is not None else "-"
        md.append(f"| {r['signal_tf']} | {r['symbol']} | {r['setup_type']} | "
                  f"{r['session']} | {r['direction_mode']} | "
                  f"{r['tp']:.1f}/{r['sl']:.1f} | {r['n']} | "
                  f"{r['wr']*100:.1f}% | {r['pf']:.2f} | {wfp} | {deg} | "
                  f"{r['mc_ruin_pct']:.1f} | {r['decay_label']} | "
                  f"**{r['label']}** | {r['flags']} |")
    (REPORTS / "K3M1_Dedup75_Robustness.md").write_text("\n".join(md), encoding="utf-8")
    print(f"\nReport: reports/K3M1_Dedup75_Robustness.md")


if __name__ == "__main__":
    main()
