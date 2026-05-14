"""Grid search + robustness para Qulla ORB LONG.

Pasos:
  1) Per simbolo, barrer (open_hour, range_hours, sl_atr, max_hold_hours,
     partial_R, breakout_window). LONG only — el INVERT ya se sabe que pierde.
  2) Filtrar por gates: n>=80, PF>=1.4, WR>=0.50, exp_r>=0.15, tpy>=40.
  3) Robustness: MC 10k bootstrap (ruin DD>=30R), WF 50/50, decay.
  4) Clasificar FUERTE / ACEPTABLE / DEBIL / MUERTA.
  5) Emitir parquet + markdown.

Outputs:
  reports/qulla_orb_grid.parquet
  reports/qulla_orb_survivors.parquet
  reports/qulla_orb_robustness.parquet
  reports/Qulla_ORB_Robustness.md
"""
from __future__ import annotations
import argparse
import gc
import sys
import time as _time
from dataclasses import replace
from pathlib import Path

import numpy as np
import polars as pl

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.engine.traders_setups import (
    resample_to_hourly, add_indicators, detect_qulla_orb_m1,
)
from src.engine.traders_backtest import (
    backtest_signals, backtest_orb_vectorized, TRADER_RULES, ExitRules,
)
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

# Per-symbol open hour HINTS basados en horarios de mercado UTC:
#  - FX 24h: London 07, NY 13
#  - Metales (overlap NY equity): 13
#  - WTI/BRENT/NATGAS (NYMEX RTH): 13
#  - SP500/NASDAQ100 (NYSE RTH summer 13, winter 14)
DEFAULT_OPEN_HOURS = {
    "EURUSD": [7, 13], "GBPUSD": [7, 13], "USDJPY": [7, 13],
    "AUDUSD": [7, 13], "GBPJPY": [7, 13], "EURJPY": [7, 13],
    "GBPAUD": [7, 13],
    "XAUUSD": [7, 13, 14], "XAGUSD": [7, 13, 14],
    "WTI":    [13, 14], "BRENT": [7, 13],
    "NATGAS": [13, 14],
    "SP500":  [13, 14], "NASDAQ100": [13, 14],
}

# Grid de exit / risk — range_minutes fiel al PDF Qulla (15/30/45/60)
GRID_RANGE_MIN  = [15, 30, 45, 60]
GRID_SL_ATR     = [0.5, 1.0]
GRID_MAX_HOURS  = [4, 8]
GRID_PARTIAL_R  = [2.0, 3.0]
GRID_BRK_WIN_MIN = [180]  # 3h post-rango (PDF: "primeros 20 min a 3 horas")

# Gates para survivors
SURV_MIN_N = 80
SURV_MIN_PF = 1.40
SURV_MIN_WR = 0.50
SURV_MIN_EXP = 0.15
SURV_MIN_TPY = 40


def _build_rules(sl_atr: float, max_hours: int, partial_R: float) -> ExitRules:
    return ExitRules(
        trader="Qulla",
        initial_sl_pct=None,
        initial_sl_atr_mult=sl_atr,
        partials=(("r_multiple", partial_R, 0.50),),
        trail_sma=None,
        time_stop_days=None,
        max_hold_days=max_hours / 24.0,
        wait_bars_after_signal=2,
    )


def run_grid(symbols: list[str]) -> list[dict]:
    rows: list[dict] = []
    t0 = _time.time()
    total_combos_per_sym = (
        len(GRID_RANGE_MIN) * len(GRID_SL_ATR) * len(GRID_MAX_HOURS)
        * len(GRID_PARTIAL_R) * len(GRID_BRK_WIN_MIN)
    )
    for i, sym in enumerate(symbols, 1):
        p = M1_CACHE / f"{sym}_M1.parquet"
        if not p.exists():
            print(f"  [SKIP] {sym}: no M1")
            continue
        m1 = pl.read_parquet(p).select(["time", "open", "high", "low", "close", "volume"]).sort("time")
        m1_arr = m1.select(["open", "high", "low", "close"]).to_numpy()
        m1_times_us = m1["time"].cast(pl.Int64).to_numpy()
        # Daily empty (no trailing SMA en intradia ORB)
        empty_daily = m1.head(0).select(["time", "open", "high", "low", "close", "volume"])

        open_hours = DEFAULT_OPEN_HOURS.get(sym, [13])
        combos_sym = total_combos_per_sym * len(open_hours)
        print(f"\n[{i}/{len(symbols)}] {sym}  open_hours={open_hours}  combos={combos_sym}  ({_time.time()-t0:.0f}s)")
        kept = 0
        for oh in open_hours:
            for rm in GRID_RANGE_MIN:
                for bw in GRID_BRK_WIN_MIN:
                    sigs = detect_qulla_orb_m1(
                        m1, open_hour_utc=oh, open_minute_utc=0,
                        range_minutes=rm, breakout_window_minutes=bw,
                    )
                    if len(sigs) < SURV_MIN_N:
                        continue
                    for sl in GRID_SL_ATR:
                        for mh in GRID_MAX_HOURS:
                            for pr in GRID_PARTIAL_R:
                                rules = _build_rules(sl, mh, pr)
                                trades = backtest_orb_vectorized(
                                    signals=sigs,
                                    m1_arr=m1_arr,
                                    m1_times_us=m1_times_us,
                                    rules=rules,
                                    symbol=sym,
                                    signal_tf_min=1,
                                )
                                if len(trades) < SURV_MIN_N:
                                    continue
                                tdf = pl.DataFrame(trades)
                                m = compute_metrics(tdf)
                                row = {
                                    "symbol": sym,
                                    "open_hour": oh,
                                    "range_min": rm,
                                    "brk_win_min": bw,
                                    "sl_atr": sl,
                                    "max_hours": mh,
                                    "partial_R": pr,
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
                                kept += 1
        print(f"   kept={kept}  cumulative={len(rows)}")
        del m1, m1_arr, m1_times_us
        gc.collect()
    return rows


def filter_survivors(rows: list[dict]) -> list[dict]:
    keep = []
    for r in rows:
        if (r["n_trades"] >= SURV_MIN_N and r["pf"] >= SURV_MIN_PF
                and r["wr"] >= SURV_MIN_WR and r["exp_r"] >= SURV_MIN_EXP
                and r["tpy"] >= SURV_MIN_TPY):
            keep.append(r)
    return keep


def dedup_best_per_symbol(rows: list[dict]) -> list[dict]:
    """Por simbolo, dejar la mejor combo (max sum_r)."""
    best = {}
    for r in rows:
        s = r["symbol"]
        if s not in best or r["sum_r"] > best[s]["sum_r"]:
            best[s] = r
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
        r["mc_p50_net"] = round(mc["p50_net"], 2)
        r["mc_p95_dd"] = round(mc["p95_dd"], 2)
        if wf:
            r["wf_pf_is"] = round(wf["pf_tr"], 3)
            r["wf_pf_oos"] = round(wf["pf_te"], 3)
            r["wf_deg_wr_pct"] = round(wf["deg_wr_pct"], 2)
        else:
            r["wf_pf_is"] = None; r["wf_pf_oos"] = None; r["wf_deg_wr_pct"] = None
        if dec:
            r["decay_slope"] = round(dec["slope"], 5)
            r["decay_label"] = dec["label"]
        else:
            r["decay_slope"] = None; r["decay_label"] = "N/A"
        r["robustness"] = cls
        r["flags"] = ", ".join(flags)
    return rows


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


def to_df(rows: list[dict]) -> pl.DataFrame:
    cleaned = [{k: v for k, v in r.items() if k != "_trades"} for r in rows]
    return pl.DataFrame(cleaned)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", nargs="*", default=None)
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()

    symbols = args.symbols if args.symbols else UNIVERSE
    if args.smoke:
        symbols = ["XAUUSD", "WTI", "NASDAQ100", "SP500"]
    print(f"=== Qulla ORB Grid (M1) + Robustness ===")
    print(f"Symbols: {len(symbols)} | range_min={GRID_RANGE_MIN} brk_win_min={GRID_BRK_WIN_MIN} "
          f"sl_atr={GRID_SL_ATR} max_h={GRID_MAX_HOURS} part_R={GRID_PARTIAL_R}")

    t0 = _time.time()
    rows = run_grid(symbols)
    print(f"\nGrid: {len(rows)} combos in {(_time.time()-t0)/60:.1f}m")

    full_df = to_df(rows)
    full_df.write_parquet(REPORTS / "qulla_orb_grid.parquet")

    surv = filter_survivors(rows)
    print(f"Survivors (n>={SURV_MIN_N}, PF>={SURV_MIN_PF}, WR>={SURV_MIN_WR}, "
          f"exp>={SURV_MIN_EXP}, tpy>={SURV_MIN_TPY}): {len(surv)}")

    if not surv:
        print("No survivors. Tightening gates may be needed.")
        return

    best = dedup_best_per_symbol(surv)
    print(f"Best per symbol: {len(best)}")

    print(f"\nRobustness (MC 10k + WF 50/50 + decay) on {len(best)} combos...")
    t1 = _time.time()
    best = add_robustness(best)
    print(f"  done in {(_time.time()-t1):.1f}s")

    best_df = to_df(best).sort("sum_r", descending=True)
    best_df.write_parquet(REPORTS / "qulla_orb_robustness.parquet")

    # Markdown
    md = REPORTS / "Qulla_ORB_Robustness.md"
    with md.open("w", encoding="utf-8") as f:
        f.write("# Qulla ORB — Grid + Robustness\n\n")
        f.write(f"Universo: {len(symbols)} | combos evaluados: {len(rows)} | "
                f"survivors: {len(surv)} | mejores por simbolo: {len(best)}\n\n")
        f.write("## Best per symbol con robustness\n\n")
        show_cols = ["symbol", "open_hour", "range_hours", "brk_win", "sl_atr",
                     "max_hours", "partial_R", "n_trades", "wr", "pf", "exp_r",
                     "max_dd_r", "tpy", "sum_r",
                     "wf_pf_is", "wf_pf_oos", "wf_deg_wr_pct",
                     "mc_ruin_pct", "mc_p5_net", "mc_p95_dd",
                     "decay_label", "robustness", "flags"]
        f.write(_md_table(best_df.select([c for c in show_cols if c in best_df.columns])) + "\n\n")
        f.write("## Top 30 survivors (todas las combinaciones que pasan gates)\n\n")
        surv_df = to_df(surv).sort("sum_r", descending=True).head(30)
        f.write(_md_table(surv_df) + "\n\n")
        # Resumen por clasificacion
        f.write("## Conteo por clasificacion (best per symbol)\n\n")
        cls = best_df.group_by("robustness").agg(pl.len().alias("n")).sort("n", descending=True)
        f.write(_md_table(cls) + "\n")
    print(f"\n=> {REPORTS/'qulla_orb_grid.parquet'}")
    print(f"=> {REPORTS/'qulla_orb_robustness.parquet'}")
    print(f"=> {md}")
    print(f"\nTotal: {(_time.time()-t0)/60:.1f}m")


if __name__ == "__main__":
    main()
