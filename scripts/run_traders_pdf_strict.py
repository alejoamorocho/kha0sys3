"""Replica PDF-STRICT de los 4 traders (Minervini / Zanger / Qulla / Ryan).

A diferencia del grid uniforme, aqui aplicamos las reglas EXACTAS del PDF
por cada trader_setup. Una sola configuracion por trader_setup, sin grid:
solo seteamos `valid_days` del setup (3 o 5) y dejamos que el walker
ejecute el resto.

Reglas EXACTAS por trader_setup (PDF-strict):

  Minervini_VCP
    SL inicial      : 7.5% fijo bajo entry
    Partial 1       : 25% al alcanzar +2R
    Partial 2       : 25% al alcanzar +4R
    Trailing        : SMA10 D1 (corto plazo, "media clave")
    Max hold        : 60 dias
    Filtro mercado  : (no implementado en backtest — solo Stage 2 individual)

  Zanger_FLAG / Zanger_CUP_HANDLE
    SL inicial      : 8% fijo (regla sacrosanta)
    Partial 1       : 50% al alcanzar +15% from entry
    Trailing        : SMA20 D1
    Time-stop       : 2 dias (proxy intradia "20min-3h")
    Max hold        : 30/40 dias

  Qulla_HTF / Qulla_EP
    SL inicial      : 1×ATR_D1 bajo entry
    Partial 1       : 30% al dia 3 desde entry
    Partial 2       : 20% al dia 5 desde entry
    Moonbag (50%)   : trailing SMA50 D1
    Max hold        : 40 dias

  Qulla_ORB (intradia)
    SL inicial      : Range Low (base_low del signal)
    Partial 1       : 30% al dia 3 (en intradia: el "dia 3" se interpreta como
                      after 3 sessions = 3 days en M1 walking)
    Partial 2       : 20% al dia 5
    Moonbag (50%)   : trailing SMA50 D1
    Max hold        : 10 dias (intradia trigger, pero gestion swing)

  Ryan_ANTS
    SL inicial      : 7% fijo
    Partial 1       : 15% al +22% from entry (median 20-25%)
    Partial 2       : 15% al +40% from entry
    Trailing        : SMA50 D1 (exit si D1 close < SMA50)
    Max hold        : 80 dias

Outputs:
  reports/traders_pdf_strict.parquet
  reports/Traders_PDF_Strict.md
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

from src.engine.traders_setups import (
    resample_to_daily, resample_to_hourly, add_indicators,
    detect_qulla_orb_m1,
)
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

DEFAULT_OPEN_HOURS = {
    "EURUSD": 7, "GBPUSD": 7, "USDJPY": 7, "AUDUSD": 7, "GBPJPY": 7,
    "EURJPY": 7, "GBPAUD": 7,
    "XAUUSD": 7, "XAGUSD": 13,
    "WTI": 13, "BRENT": 7, "NATGAS": 13,
    "SP500": 13, "NASDAQ100": 13,
}


# ── Reglas PDF-strict por trader_setup ───────────────────────────────────

PDF_RULES: dict[str, ExitRules] = {
    "Minervini_VCP": ExitRules(
        trader="Minervini",
        initial_sl_pct=0.075,
        initial_sl_atr_mult=None,
        partials=(("r_multiple", 2.0, 0.25), ("r_multiple", 4.0, 0.25)),
        trail_sma=10,
        time_stop_days=None,
        max_hold_days=60.0,
        wait_bars_after_signal=2,
    ),
    "Zanger_FLAG": ExitRules(
        trader="Zanger",
        initial_sl_pct=0.08,
        initial_sl_atr_mult=None,
        partials=(("pct_from_entry", 0.15, 0.50),),
        trail_sma=20,
        time_stop_days=2,
        max_hold_days=30.0,
        wait_bars_after_signal=2,
    ),
    "Zanger_CUP": ExitRules(
        trader="Zanger",
        initial_sl_pct=0.08,
        initial_sl_atr_mult=None,
        partials=(("pct_from_entry", 0.15, 0.50),),
        trail_sma=20,
        time_stop_days=3,
        max_hold_days=40.0,
        wait_bars_after_signal=2,
    ),
    "Qulla_HTF": ExitRules(
        trader="Qulla",
        initial_sl_pct=None,
        initial_sl_atr_mult=1.0,
        partials=(("days_held", 3, 0.30), ("days_held", 5, 0.20)),
        trail_sma=50,
        time_stop_days=None,
        max_hold_days=40.0,
        wait_bars_after_signal=2,
    ),
    "Qulla_EP": ExitRules(
        trader="Qulla",
        initial_sl_pct=None,
        initial_sl_atr_mult=1.0,
        partials=(("days_held", 3, 0.30), ("days_held", 5, 0.20)),
        trail_sma=50,
        time_stop_days=None,
        max_hold_days=40.0,
        wait_bars_after_signal=2,
    ),
    "Ryan_ANTS": ExitRules(
        trader="Ryan",
        initial_sl_pct=0.07,
        initial_sl_atr_mult=None,
        partials=(("pct_from_entry", 0.22, 0.15), ("pct_from_entry", 0.40, 0.15)),
        trail_sma=50,
        time_stop_days=None,
        max_hold_days=80.0,
        wait_bars_after_signal=2,
        trail_uses_d1_close=True,
    ),
    "Qulla_ORB": ExitRules(
        trader="Qulla",
        initial_sl_pct=None,
        initial_sl_atr_mult=None,
        partials=(("days_held", 3, 0.30), ("days_held", 5, 0.20)),
        trail_sma=50,
        time_stop_days=None,
        max_hold_days=10.0,
        wait_bars_after_signal=2,
        use_base_low_as_sl=True,
    ),
}

# Para los swing usamos valid_days fijo del PDF: setup tiene que romperse pronto
SWING_VALID_DAYS = 5  # PDF: rompimientos tardios se descartan, pero damos 1 semana


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


def run_pdf_strict(symbols: list[str]) -> list[dict]:
    """Una corrida por (sym, trader_setup) con reglas PDF exactas."""
    rows = []
    t0 = _time.time()
    for i, sym in enumerate(symbols, 1):
        p = M1_CACHE / f"{sym}_M1.parquet"
        if not p.exists():
            print(f"  [SKIP] {sym}")
            continue
        m1 = pl.read_parquet(p).select(["time", "open", "high", "low", "close", "volume"]).sort("time")
        m1_arr = m1.select(["open", "high", "low", "close"]).to_numpy()
        m1_times_us = m1["time"].cast(pl.Int64).to_numpy()
        m1_close = m1_arr[:, 3]
        daily = add_indicators(resample_to_daily(m1))
        print(f"\n[{i}/{len(symbols)}] {sym}  D1 bars: {len(daily)}  ({_time.time()-t0:.0f}s)")

        # === Swing setups (Minervini, Zanger, Qulla HTF/EP, Ryan) ===
        for trader_setup, detector in SWING_DETECTORS.items():
            if trader_setup not in PDF_RULES:
                continue
            rules = PDF_RULES[trader_setup]
            setup_t = detector(daily, valid_days=SWING_VALID_DAYS)
            n_setups = len(setup_t)
            if n_setups == 0:
                continue
            sigs = find_intraday_breakouts(
                setup_t, m1_arr, m1_times_us, m1_close,
                trader=trader_setup.split("_")[0],
                setup_name=trader_setup.split("_", 1)[1],
            )
            if len(sigs) < 10:
                continue
            trades = backtest_signals(
                signals=sigs, m1_arr=m1_arr, m1_times_us=m1_times_us,
                daily=daily, rules=rules, symbol=sym, signal_tf_min=1,
                invert=False,
            )
            if len(trades) < 10:
                continue
            tdf = pl.DataFrame(trades)
            m = compute_metrics(tdf)
            rows.append({
                "symbol": sym, "trader_setup": trader_setup,
                "n_setups": n_setups, "n_signals": len(sigs),
                "n_trades": m.n_trades,
                "wr": round(m.wr, 4), "pf": round(m.profit_factor, 3),
                "exp_r": round(m.expectancy_r, 4),
                "max_dd_r": round(m.max_dd_r, 2),
                "tpy": round(m.trades_per_year, 1),
                "sum_r": round(float(tdf["r_multiple"].sum()), 2),
                "_trades": tdf,
            })
            print(f"   {trader_setup:18s}: n={m.n_trades:4d} wr={m.wr:.2f} "
                  f"pf={m.profit_factor:.2f} exp_r={m.expectancy_r:+.3f} "
                  f"dd={m.max_dd_r:.1f}R tpy={m.trades_per_year:.0f}")

        # === Qulla ORB (intraday entry + swing gestion) ===
        oh = DEFAULT_OPEN_HOURS.get(sym, 13)
        sigs = detect_qulla_orb_m1(
            m1, open_hour_utc=oh, open_minute_utc=0,
            range_minutes=30, breakout_window_minutes=180,
        )
        if len(sigs) >= 10:
            rules = PDF_RULES["Qulla_ORB"]
            trades = backtest_signals(
                signals=sigs, m1_arr=m1_arr, m1_times_us=m1_times_us,
                daily=daily, rules=rules, symbol=sym, signal_tf_min=1,
                invert=False,
            )
            if len(trades) >= 10:
                tdf = pl.DataFrame(trades)
                m = compute_metrics(tdf)
                rows.append({
                    "symbol": sym, "trader_setup": "Qulla_ORB",
                    "n_setups": 0, "n_signals": len(sigs),
                    "n_trades": m.n_trades,
                    "wr": round(m.wr, 4), "pf": round(m.profit_factor, 3),
                    "exp_r": round(m.expectancy_r, 4),
                    "max_dd_r": round(m.max_dd_r, 2),
                    "tpy": round(m.trades_per_year, 1),
                    "sum_r": round(float(tdf["r_multiple"].sum()), 2),
                    "_trades": tdf,
                })
                print(f"   {'Qulla_ORB':18s}: n={m.n_trades:4d} wr={m.wr:.2f} "
                      f"pf={m.profit_factor:.2f} exp_r={m.expectancy_r:+.3f} "
                      f"dd={m.max_dd_r:.1f}R tpy={m.trades_per_year:.0f}")

        del m1, m1_arr, m1_times_us, m1_close, daily
        gc.collect()
    return rows


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", nargs="*", default=None)
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()

    symbols = args.symbols if args.symbols else UNIVERSE
    if args.smoke:
        symbols = ["XAUUSD", "WTI", "NASDAQ100", "EURUSD"]

    print(f"=== Traders PDF-Strict ===")
    print(f"Symbols: {len(symbols)} | trader_setups: {len(PDF_RULES)}")
    t0 = _time.time()
    rows = run_pdf_strict(symbols)
    if not rows:
        print("No survivors.")
        return
    print(f"\nResults: {len(rows)} combos in {(_time.time()-t0)/60:.1f}m")

    rows = add_robustness(rows)
    df = to_df(rows).sort("sum_r", descending=True)
    df.write_parquet(REPORTS / "traders_pdf_strict.parquet")

    md = REPORTS / "Traders_PDF_Strict.md"
    with md.open("w", encoding="utf-8") as f:
        f.write("# Traders PDF-Strict — Reglas EXACTAS de los PDFs\n\n")
        f.write(f"Universo: {len(symbols)} | trader_setups: {len(PDF_RULES)} | "
                f"resultados: {len(rows)}\n\n")
        f.write("## Reglas aplicadas\n\n")
        f.write("| trader_setup | SL inicial | Partials | Trail | Time-stop | Max hold |\n")
        f.write("|---|---|---|---|---|---|\n")
        f.write("| Minervini_VCP | 7.5% fijo | 25%@2R + 25%@4R | SMA10 D1 | – | 60 d |\n")
        f.write("| Zanger_FLAG | 8% fijo | 50%@+15% | SMA20 D1 | 2 d | 30 d |\n")
        f.write("| Zanger_CUP | 8% fijo | 50%@+15% | SMA20 D1 | 3 d | 40 d |\n")
        f.write("| Qulla_HTF | 1×ATR_D1 | 30%@d3 + 20%@d5 | SMA50 D1 | – | 40 d |\n")
        f.write("| Qulla_EP | 1×ATR_D1 | 30%@d3 + 20%@d5 | SMA50 D1 | – | 40 d |\n")
        f.write("| Qulla_ORB | **Range Low** | 30%@d3 + 20%@d5 | SMA50 D1 | – | 10 d |\n")
        f.write("| Ryan_ANTS | 7% fijo | 15%@+22% + 15%@+40% | SMA50 D1 (exit si close<SMA50) | – | 80 d |\n\n")

        f.write("## Resultados por (symbol, trader_setup)\n\n")
        show_cols = ["symbol", "trader_setup", "n_trades", "wr", "pf", "exp_r",
                     "max_dd_r", "tpy", "sum_r",
                     "wf_pf_is", "wf_pf_oos", "wf_deg_wr_pct",
                     "mc_ruin_pct", "mc_p95_dd", "decay_label",
                     "robustness", "flags"]
        f.write(_md_table(df.select([c for c in show_cols if c in df.columns])) + "\n\n")

        f.write("## Agregado por trader_setup\n\n")
        ag = df.group_by("trader_setup").agg([
            pl.col("symbol").n_unique().alias("syms_ok"),
            pl.col("n_trades").sum().alias("n_total"),
            pl.col("sum_r").sum().alias("sum_r_total"),
            (pl.col("pf") * pl.col("n_trades")).sum().alias("_pfw"),
            (pl.col("wr") * pl.col("n_trades")).sum().alias("_wrw"),
            pl.col("tpy").mean().alias("avg_tpy"),
        ]).with_columns([
            (pl.col("_pfw") / pl.col("n_total")).round(3).alias("avg_pf"),
            (pl.col("_wrw") / pl.col("n_total")).round(3).alias("avg_wr"),
        ]).select(["trader_setup", "syms_ok", "n_total", "avg_wr", "avg_pf",
                   "sum_r_total", "avg_tpy"]).sort("sum_r_total", descending=True)
        f.write(_md_table(ag) + "\n")
    print(f"=> {REPORTS/'traders_pdf_strict.parquet'}")
    print(f"=> {md}")
    print(f"\nTotal: {(_time.time()-t0)/60:.1f}m")


if __name__ == "__main__":
    main()
