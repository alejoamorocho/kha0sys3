"""Orquestador: 4 traders x 14 simbolos x LONG+INVERT.

Lee M1 cache de C:/Proyectos/kha0sys3/data/enriched_math_tf/<sym>_M1.parquet,
resamplea a D1 y H1, ejecuta detectores + backtest por trader, agrega y
emite parquet + reporte markdown comparable contra K3M1-75.

Usage:
    python scripts/run_traders_replication.py [--symbols SYM1 SYM2 ...] [--smoke]
"""
from __future__ import annotations
import argparse
import gc
import sys
import time as _time
from pathlib import Path

import numpy as np
import polars as pl

# Ensure repo root in path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.engine.traders_setups import (
    resample_to_daily, resample_to_hourly, add_indicators,
    detect_minervini_vcp, detect_zanger_flag, detect_zanger_cup_handle,
    detect_qulla_high_tight_flag, detect_qulla_episodic_pivot, detect_qulla_orb,
    detect_ryan_ants,
)
from src.engine.traders_backtest import backtest_signals, TRADER_RULES, _rules_for
from src.engine.indicator_validation import compute_metrics

M1_CACHE = Path("C:/Proyectos/kha0sys3/data/enriched_math_tf")
REPORTS = Path("reports")
REPORTS.mkdir(exist_ok=True)

UNIVERSE = [
    "AUDUSD", "BRENT", "EURJPY", "EURUSD", "GBPAUD",
    "GBPJPY", "GBPUSD", "NASDAQ100", "NATGAS", "SP500",
    "USDJPY", "WTI", "XAGUSD", "XAUUSD",
]

SETUP_REGISTRY = [
    # (trader, setup_name, signal_tf, detector_fn)
    ("Minervini", "VCP", "D1", detect_minervini_vcp),
    ("Zanger",    "FLAG", "D1", detect_zanger_flag),
    ("Zanger",    "CUP_HANDLE", "D1", detect_zanger_cup_handle),
    ("Qulla",     "HTF", "D1", detect_qulla_high_tight_flag),
    ("Qulla",     "EP", "D1", detect_qulla_episodic_pivot),
    ("Qulla",     "ORB", "H1", detect_qulla_orb),
    ("Ryan",      "ANTS", "D1", detect_ryan_ants),
]


def _tf_minutes(tf: str) -> int:
    return {"M1": 1, "H1": 60, "D1": 1440}[tf]


def run_symbol(sym: str, invert_modes: list[bool]) -> list[dict]:
    p = M1_CACHE / f"{sym}_M1.parquet"
    if not p.exists():
        print(f"  [SKIP] {sym}: no M1 cache")
        return []
    m1 = pl.read_parquet(p).select(["time", "open", "high", "low", "close", "volume"])
    m1 = m1.sort("time")
    m1_arr = m1.select(["open", "high", "low", "close"]).to_numpy()
    m1_times_us = m1["time"].cast(pl.Int64).to_numpy()

    daily = add_indicators(resample_to_daily(m1))
    hourly = add_indicators(resample_to_hourly(m1))

    out: list[dict] = []
    for trader, setup_name, tf, detector in SETUP_REGISTRY:
        if tf == "D1":
            sig_df = detector(daily)
        elif tf == "H1":
            sig_df = detector(hourly)
        else:
            sig_df = detector(daily)
        n_sig = len(sig_df)
        if n_sig == 0:
            continue
        rules = _rules_for(trader, setup_name)
        for invert in invert_modes:
            trades = backtest_signals(
                signals=sig_df,
                m1_arr=m1_arr,
                m1_times_us=m1_times_us,
                daily=daily,
                rules=rules,
                symbol=sym,
                signal_tf_min=_tf_minutes(tf),
                invert=invert,
            )
            if len(trades) < 5:
                continue
            tdf = pl.DataFrame(trades)
            m = compute_metrics(tdf)
            out.append({
                "symbol": sym,
                "trader": trader,
                "setup": setup_name,
                "signal_tf": tf,
                "direction_mode": "INVERT" if invert else "LONG",
                "n_signals": n_sig,
                "n_trades": m.n_trades,
                "wr": round(m.wr, 4),
                "pf": round(m.profit_factor, 3),
                "exp_r": round(m.expectancy_r, 4),
                "max_dd_r": round(m.max_dd_r, 2),
                "tpy": round(m.trades_per_year, 1),
                "sum_r": round(float(tdf["r_multiple"].sum()), 2),
            })
    del m1, m1_arr, m1_times_us, daily, hourly
    gc.collect()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", nargs="*", default=None)
    ap.add_argument("--smoke", action="store_true",
                    help="Solo XAUUSD + EURUSD + SP500 + NASDAQ100, LONG only")
    ap.add_argument("--long-only", action="store_true")
    ap.add_argument("--out", default="traders_replication")
    args = ap.parse_args()

    if args.smoke:
        symbols = ["XAUUSD", "EURUSD", "SP500", "NASDAQ100"]
    else:
        symbols = args.symbols if args.symbols else UNIVERSE

    invert_modes = [False] if args.long_only else [False, True]

    print(f"=== Traders Replication ===")
    print(f"Symbols: {len(symbols)} | Setups: {len(SETUP_REGISTRY)} | "
          f"Dirs: {len(invert_modes)} ({'LONG' if not invert_modes[-1] else 'LONG+INVERT'})")
    t0 = _time.time()
    all_rows: list[dict] = []
    for i, sym in enumerate(symbols, 1):
        print(f"\n[{i}/{len(symbols)}] {sym}  ({_time.time()-t0:.0f}s)")
        rows = run_symbol(sym, invert_modes)
        for r in rows:
            print(f"   {r['trader']:9s} {r['setup']:11s} {r['direction_mode']:6s} "
                  f"n={r['n_trades']:4d} wr={r['wr']:.2f} pf={r['pf']:.2f} "
                  f"exp_r={r['exp_r']:+.3f} dd={r['max_dd_r']:.1f}R tpy={r['tpy']:.0f}")
        all_rows.extend(rows)

    if not all_rows:
        print("\nNo trades generated.")
        return

    df = pl.DataFrame(all_rows)
    out_pq = REPORTS / f"{args.out}.parquet"
    df.write_parquet(out_pq)
    print(f"\n=> {out_pq}  ({len(df)} rows, elapsed {(_time.time()-t0)/60:.1f}m)")

    # Markdown report (manual writer; sin dependencia tabulate)
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

    md = REPORTS / f"{args.out}.md"
    with md.open("w", encoding="utf-8") as f:
        f.write("# Traders Replication — Resultados\n\n")
        f.write(f"Universo: {len(symbols)} | Setups: {len(SETUP_REGISTRY)} | "
                f"Modos: {'LONG' if args.long_only else 'LONG+INVERT'}\n\n")
        f.write("## Resumen por trader (agregado)\n\n")
        agg_trader = df.group_by(["trader", "direction_mode"]).agg([
            pl.col("n_trades").sum().alias("n_total"),
            pl.col("sum_r").sum().alias("sum_r"),
            (pl.col("pf") * pl.col("n_trades")).sum().alias("_pf_w"),
            (pl.col("wr") * pl.col("n_trades")).sum().alias("_wr_w"),
            pl.col("tpy").mean().alias("avg_tpy"),
        ]).with_columns([
            (pl.col("_pf_w") / pl.col("n_total")).round(3).alias("avg_pf"),
            (pl.col("_wr_w") / pl.col("n_total")).round(3).alias("avg_wr"),
        ]).select(["trader", "direction_mode", "n_total", "avg_wr", "avg_pf",
                   "sum_r", "avg_tpy"]).sort(["trader", "direction_mode"])
        f.write(_md_table(agg_trader) + "\n\n")

        f.write("## Top 25 combinaciones por sum_R\n\n")
        top = df.sort("sum_r", descending=True).head(25)
        f.write(_md_table(top) + "\n\n")

        f.write("## Detalle completo\n\n")
        f.write(_md_table(df.sort(["trader", "symbol", "setup", "direction_mode"])) + "\n")
    print(f"=> {md}")


if __name__ == "__main__":
    main()
