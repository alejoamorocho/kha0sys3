"""Grid + robustness para los 6 setups swing FX-calibrated:
  Minervini_VCP, Zanger_FLAG, Zanger_CUP, Qulla_HTF, Qulla_EP, Ryan_ANTS.

Pipeline por simbolo:
  M1 cache  ->  D1 con indicadores  ->  setup_table (D1 detector)
            ->  intraday_breakouts (primer cierre M1 > pivot)
            ->  backtest_signals (varios ExitRules grid)
            ->  filter survivors + best per (sym, setup)
            ->  MC bootstrap + WF 50/50 + decay

Grid (compacto para tractabilidad):
  sl_atr           {1.0, 1.5}        (SL en multiplos de ATR D1)
  partial_R        {2.0, 3.0}
  trail_sma        {None, 50}        (PDF: trailing por SMA50 = "ultimo recurso")
  max_hold_days    {15, 30}          (swing: 2 a 6 semanas)
  time_stop_days   {None, 3}         (Zanger: cierra si revierte en 2-3d)

Outputs:
  reports/traders_swing_grid.parquet
  reports/traders_swing_robustness.parquet
  reports/Traders_Swing_Robustness.md
"""
from __future__ import annotations
import argparse
import gc
import sys
import time as _time
from pathlib import Path

import numpy as np
import polars as pl

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.engine.traders_setups import resample_to_daily, add_indicators
from src.engine.traders_swing import SWING_DETECTORS, find_intraday_breakouts
from src.engine.traders_backtest import backtest_signals, ExitRules
from src.engine.indicator_validation import compute_metrics
from src.engine.k3m1_robustness import mc_ruin, walk_forward, decay, classify

M1_CACHE = Path("C:/Proyectos/kha0sys3/data/enriched_math_tf")
REPORTS = Path("reports")
REPORTS.mkdir(exist_ok=True)

UNIVERSE = [
    "AUDUSD", "BRENT", "EURJPY", "EURUSD", "GBPAUD",
    "GBPJPY", "GBPUSD", "NASDAQ100", "NATGAS", "SP500",
    "USDJPY", "WTI", "XAGUSD", "XAUUSD",
]

# Trader -> (default partials, time_stop, max_hold) hint del PDF
TRADER_PROFILE = {
    "Minervini_VCP": {"sl_pct": None, "partials_default": "r_multi",
                      "trail_default": 50, "max_hold": 60},
    "Zanger_FLAG":   {"sl_pct": 0.05, "partials_default": "pct",
                      "trail_default": 20, "max_hold": 30,
                      "time_stop": 3},
    "Zanger_CUP":    {"sl_pct": 0.05, "partials_default": "pct",
                      "trail_default": 20, "max_hold": 40,
                      "time_stop": 5},
    "Qulla_HTF":     {"sl_pct": None, "partials_default": "days",
                      "trail_default": 50, "max_hold": 40},
    "Qulla_EP":      {"sl_pct": None, "partials_default": "days",
                      "trail_default": 50, "max_hold": 30},
    "Ryan_ANTS":     {"sl_pct": 0.04, "partials_default": "pct",
                      "trail_default": 50, "max_hold": 60},
}

# Grid compacto
GRID_SL_ATR = [1.0, 1.5]
GRID_PARTIAL_R = [2.0, 3.0]
GRID_TRAIL = [None, 50]
GRID_MAX_HOLD = [15, 30]
GRID_VALID_DAYS = [3, 5]  # validez del setup post-D1

# Gates survivors
SURV_MIN_N = 30
SURV_MIN_PF = 1.30
SURV_MIN_WR = 0.40
SURV_MIN_EXP = 0.10
SURV_MIN_TPY = 5


def _build_rules(trader_setup: str, sl_atr: float, partial_R: float,
                  trail: int | None, max_hold: int) -> ExitRules:
    prof = TRADER_PROFILE[trader_setup]
    partials = ((partial_R / 2.0, 0.30), (partial_R, 0.30))  # parciales escalonados
    partials_tuples = tuple(("r_multiple", float(p), float(f)) for p, f in partials)
    return ExitRules(
        trader=trader_setup.split("_")[0],
        initial_sl_pct=prof.get("sl_pct"),
        initial_sl_atr_mult=sl_atr if prof.get("sl_pct") is None else None,
        partials=partials_tuples,
        trail_sma=trail,
        time_stop_days=prof.get("time_stop"),
        max_hold_days=float(max_hold),
        wait_bars_after_signal=2,
    )


def run_grid(symbols: list[str]) -> list[dict]:
    rows = []
    t0 = _time.time()
    for i, sym in enumerate(symbols, 1):
        p = M1_CACHE / f"{sym}_M1.parquet"
        if not p.exists():
            print(f"  [SKIP] {sym}: no M1 cache")
            continue
        m1 = pl.read_parquet(p).select(["time", "open", "high", "low", "close", "volume"]).sort("time")
        m1_arr = m1.select(["open", "high", "low", "close"]).to_numpy()
        m1_times_us = m1["time"].cast(pl.Int64).to_numpy()
        m1_close = m1_arr[:, 3]
        daily = add_indicators(resample_to_daily(m1))
        print(f"\n[{i}/{len(symbols)}] {sym}  D1 bars: {len(daily)}  ({_time.time()-t0:.0f}s)")

        for trader_setup, detector in SWING_DETECTORS.items():
            for valid_d in GRID_VALID_DAYS:
                setup_t = detector(daily, valid_days=valid_d)
                n_setups = len(setup_t)
                if n_setups == 0:
                    continue
                # Scan intraday breakouts
                sigs = find_intraday_breakouts(
                    setup_t, m1_arr, m1_times_us, m1_close,
                    trader=trader_setup.split("_")[0],
                    setup_name=trader_setup.split("_", 1)[1],
                )
                if len(sigs) < SURV_MIN_N:
                    continue
                for sl_atr in GRID_SL_ATR:
                    for pr in GRID_PARTIAL_R:
                        for trail in GRID_TRAIL:
                            for mh in GRID_MAX_HOLD:
                                rules = _build_rules(trader_setup, sl_atr, pr, trail, mh)
                                trades = backtest_signals(
                                    signals=sigs, m1_arr=m1_arr,
                                    m1_times_us=m1_times_us,
                                    daily=daily, rules=rules,
                                    symbol=sym, signal_tf_min=1, invert=False,
                                )
                                if len(trades) < SURV_MIN_N:
                                    continue
                                tdf = pl.DataFrame(trades)
                                m = compute_metrics(tdf)
                                row = {
                                    "symbol": sym,
                                    "trader_setup": trader_setup,
                                    "valid_days": valid_d,
                                    "sl_atr": sl_atr,
                                    "partial_R": pr,
                                    "trail": trail if trail else 0,
                                    "max_hold": mh,
                                    "n_setups": n_setups,
                                    "n_signals": len(sigs),
                                    "n_trades": m.n_trades,
                                    "wr": round(m.wr, 4),
                                    "pf": round(m.profit_factor, 3),
                                    "exp_r": round(m.expectancy_r, 4),
                                    "max_dd_r": round(m.max_dd_r, 2),
                                    "tpy": round(m.trades_per_year, 1),
                                    "sum_r": round(float(tdf["r_multiple"].sum()), 2),
                                    "_trades": tdf,
                                }
                                rows.append(row)
        print(f"   cumulative combos: {len(rows)}")
        del m1, m1_arr, m1_times_us, m1_close, daily
        gc.collect()
    return rows


def filter_survivors(rows: list[dict]) -> list[dict]:
    return [r for r in rows
            if r["n_trades"] >= SURV_MIN_N and r["pf"] >= SURV_MIN_PF
            and r["wr"] >= SURV_MIN_WR and r["exp_r"] >= SURV_MIN_EXP
            and r["tpy"] >= SURV_MIN_TPY]


def dedup_best(rows: list[dict]) -> list[dict]:
    """Best por (symbol, trader_setup)."""
    best = {}
    for r in rows:
        k = (r["symbol"], r["trader_setup"])
        if k not in best or r["sum_r"] > best[k]["sum_r"]:
            best[k] = r
    return list(best.values())


def add_robustness(rows: list[dict]) -> list[dict]:
    for r in rows:
        tdf = r["_trades"]
        tr = tdf["r_multiple"].to_numpy()
        mc = mc_ruin(tr)
        wf = walk_forward(tdf)
        dec = decay(tdf)
        cls, flags = classify(mc, wf, dec, net_r=float(tr.sum()), pf=r["pf"])
        r["mc_ruin_pct"] = round(mc["ruin_pct"], 3)
        r["mc_p5_net"] = round(mc["p5_net"], 2)
        r["mc_p95_dd"] = round(mc["p95_dd"], 2)
        if wf:
            r["wf_pf_is"] = round(wf["pf_tr"], 3)
            r["wf_pf_oos"] = round(wf["pf_te"], 3)
            r["wf_deg_wr_pct"] = round(wf["deg_wr_pct"], 2)
        else:
            r["wf_pf_is"] = None; r["wf_pf_oos"] = None; r["wf_deg_wr_pct"] = None
        r["decay_label"] = dec["label"] if dec else "N/A"
        r["robustness"] = cls
        r["flags"] = ", ".join(flags)
    return rows


def to_df(rows: list[dict]) -> pl.DataFrame:
    cleaned = [{k: v for k, v in r.items() if k != "_trades"} for r in rows]
    return pl.DataFrame(cleaned)


def _md_table(df_in: pl.DataFrame) -> str:
    cols = df_in.columns
    lines = ["| " + " | ".join(cols) + " |",
             "|" + "|".join("---" for _ in cols) + "|"]
    for row in df_in.iter_rows(named=True):
        cells = []
        for c in cols:
            v = row[c]
            if isinstance(v, float):
                cells.append(f"{v:.3f}")
            elif v is None:
                cells.append("")
            else:
                cells.append(str(v))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", nargs="*", default=None)
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()

    symbols = args.symbols if args.symbols else UNIVERSE
    if args.smoke:
        symbols = ["XAUUSD", "WTI", "NASDAQ100", "EURUSD"]

    print(f"=== Traders Swing Grid (FX-calibrated, intraday M1 breakout) ===")
    print(f"Symbols: {len(symbols)} | Setups: {len(SWING_DETECTORS)} | "
          f"sl_atr={GRID_SL_ATR} part_R={GRID_PARTIAL_R} trail={GRID_TRAIL} "
          f"max_hold={GRID_MAX_HOLD} valid_d={GRID_VALID_DAYS}")

    t0 = _time.time()
    rows = run_grid(symbols)
    print(f"\nGrid: {len(rows)} combos in {(_time.time()-t0)/60:.1f}m")

    full_df = to_df(rows)
    full_df.write_parquet(REPORTS / "traders_swing_grid.parquet")

    surv = filter_survivors(rows)
    print(f"Survivors (n>={SURV_MIN_N}, PF>={SURV_MIN_PF}, WR>={SURV_MIN_WR}, "
          f"exp>={SURV_MIN_EXP}, tpy>={SURV_MIN_TPY}): {len(surv)}")
    if not surv:
        print("No survivors.")
        return

    best = dedup_best(surv)
    print(f"Best per (symbol, trader_setup): {len(best)}")

    print(f"\nRobustness on {len(best)}...")
    best = add_robustness(best)
    best_df = to_df(best).sort("sum_r", descending=True)
    best_df.write_parquet(REPORTS / "traders_swing_robustness.parquet")

    md = REPORTS / "Traders_Swing_Robustness.md"
    with md.open("w", encoding="utf-8") as f:
        f.write("# Traders Swing — Grid + Robustness (FX-calibrated, intraday M1 breakout)\n\n")
        f.write(f"Universo: {len(symbols)} | Setups: {len(SWING_DETECTORS)} | "
                f"combos: {len(rows)} | survivors: {len(surv)} | best: {len(best)}\n\n")
        f.write("## Best per (symbol, setup) con robustness\n\n")
        show_cols = ["symbol", "trader_setup", "valid_days", "sl_atr",
                     "partial_R", "trail", "max_hold", "n_trades", "wr",
                     "pf", "exp_r", "max_dd_r", "tpy", "sum_r",
                     "wf_pf_is", "wf_pf_oos", "wf_deg_wr_pct",
                     "mc_ruin_pct", "mc_p95_dd", "decay_label",
                     "robustness", "flags"]
        f.write(_md_table(best_df.select([c for c in show_cols if c in best_df.columns])) + "\n\n")

        f.write("## Resumen por setup (mejor por simbolo, agregado)\n\n")
        ag = best_df.group_by("trader_setup").agg([
            pl.col("symbol").n_unique().alias("syms_ok"),
            pl.col("n_trades").sum().alias("n_total"),
            pl.col("sum_r").sum().alias("sum_r_total"),
            (pl.col("pf") * pl.col("n_trades")).sum().alias("_pfw"),
            pl.col("tpy").mean().alias("avg_tpy"),
        ]).with_columns(
            (pl.col("_pfw") / pl.col("n_total")).round(3).alias("avg_pf")
        ).select(["trader_setup", "syms_ok", "n_total", "avg_pf",
                  "sum_r_total", "avg_tpy"]).sort("sum_r_total", descending=True)
        f.write(_md_table(ag) + "\n\n")

        f.write("## Top 30 survivors (todas las combinaciones)\n\n")
        top = to_df(surv).sort("sum_r", descending=True).head(30)
        f.write(_md_table(top) + "\n")
    print(f"\n=> {REPORTS/'traders_swing_grid.parquet'}")
    print(f"=> {REPORTS/'traders_swing_robustness.parquet'}")
    print(f"=> {md}")
    print(f"\nTotal: {(_time.time()-t0)/60:.1f}m")


if __name__ == "__main__":
    main()
