"""Compare hour-of-day volatility profile between backtest data and VPS live.

Goal: identify the timezone of data/enriched_math_tf/ by comparing its peak
volatility hour against known UTC session peaks (London open ~08, NY open ~13:30).

Then check whether AMO8's magic_time=00:00 matches a high-vol hour in the
backtest data — and if so, what REAL UTC hour that corresponds to in live MT5.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import polars as pl
import statistics

print("="*70)
print("HOUR-OF-DAY VOLATILITY PROFILE: backtest local M15 data")
print("="*70)
for sym in ["GBPUSD", "XAUUSD", "NASDAQ100", "SP500", "NATGAS"]:
    path = f"data/enriched_math_tf/{sym}_M15.parquet"
    if not Path(path).exists():
        continue
    df = pl.read_parquet(path)
    # M15 candle range as % of close
    df = df.with_columns([
        ((pl.col("high") - pl.col("low")) / pl.col("close") * 10000).alias("range_bps"),
        pl.col("time").dt.hour().alias("hr"),
    ])
    by_hr = df.group_by("hr").agg([
        pl.col("range_bps").mean().alias("avg_range_bps"),
        pl.col("range_bps").median().alias("med_range_bps"),
        pl.len().alias("n_bars"),
    ]).sort("hr")
    print(f"\n--- {sym} avg M15 range (bps) by hour-of-day in backtest data ---")
    # Find top 5 hours
    top = by_hr.sort("avg_range_bps", descending=True).head(5)
    print(f"  Top 5 vol hours: {[(int(r['hr']), round(r['avg_range_bps'],1)) for r in top.iter_rows(named=True)]}")
    # Show hour 00 specifically
    h0 = by_hr.filter(pl.col("hr")==0)
    if len(h0)>0:
        print(f"  hr=00: avg={h0['avg_range_bps'][0]:.1f} med={h0['med_range_bps'][0]:.1f} n_bars={h0['n_bars'][0]}")
    h8 = by_hr.filter(pl.col("hr")==8)
    if len(h8)>0:
        print(f"  hr=08: avg={h8['avg_range_bps'][0]:.1f} med={h8['med_range_bps'][0]:.1f} n_bars={h8['n_bars'][0]}")
    h13 = by_hr.filter(pl.col("hr")==13)
    if len(h13)>0:
        print(f"  hr=13: avg={h13['avg_range_bps'][0]:.1f} med={h13['med_range_bps'][0]:.1f} n_bars={h13['n_bars'][0]}")
