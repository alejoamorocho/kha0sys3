"""Pivot Point edge discovery — classic Daily + Weekly levels.

For each symbol (M1, 2018-2026):
  1. Compute classic pivot levels from PRIOR day / PRIOR week OHLC:
       PP=(H+L+C)/3
       R1=2PP-L  S1=2PP-H
       R2=PP+(H-L)  S2=PP-(H-L)
       R3=H+2(PP-L)  S3=L-2(PP-H)
  2. Detect M1-close crossings of each level (close crosses the level,
     no ATR buffer). Up-cross / down-cross, only within the same period
     (so a level jump at day/week boundary is NOT a crossing).
  3. Sequence crossing events chronologically. For each event, the
     "destination" is the NEXT level crossed the same UTC day (or EOD).
  4. Aggregate transition distributions by (symbol, hour, from_level,
     direction) -> P(next_level). Classify continuation (next level
     further in break direction) vs reversal (price returns).

Outputs:
  reports/pivot/pivot_transitions.parquet   (raw event+transition rows)
  reports/pivot/Pivot_Edge_Report.md        (human-readable edges)
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import numpy as np
import polars as pl
from collections import defaultdict, Counter

SYMBOLS = ["XAUUSD","XAGUSD","BRENT","WTI","GBPUSD","GBPJPY","EURUSD",
           "GBPAUD","USDJPY","AUDUSD","EURJPY","NASDAQ100","NATGAS","SP500"]
DATA = "data/enriched_math_tf"
OUTDIR = Path("reports/pivot"); OUTDIR.mkdir(parents=True, exist_ok=True)

# Level order low->high for direction logic
D_LEVELS = ["S3_D","S2_D","S1_D","PP_D","R1_D","R2_D","R3_D"]
W_LEVELS = ["S3_W","S2_W","S1_W","PP_W","R1_W","R2_W","R3_W"]
ALL_LEVELS = D_LEVELS + W_LEVELS


def classic_pivots(h, l, c):
    pp = (h + l + c) / 3.0
    rng = h - l
    return {
        "PP": pp,
        "R1": 2*pp - l, "S1": 2*pp - h,
        "R2": pp + rng, "S2": pp - rng,
        "R3": h + 2*(pp - l), "S3": l - 2*(pp - h),
    }


def compute_period_pivots(m1: pl.DataFrame, period: str) -> pl.DataFrame:
    """Return per-bar DataFrame with the 7 pivot levels valid that day/week,
    derived from the PRIOR period's OHLC."""
    if period == "D":
        key = pl.col("time").dt.date()
        gcol = "d"
    else:  # weekly: ISO year-week
        key = pl.col("time").dt.strftime("%G-%V")
        gcol = "w"
    df = m1.with_columns(key.alias(gcol))
    agg = (df.group_by(gcol)
             .agg([pl.col("high").max().alias("H"),
                   pl.col("low").min().alias("L"),
                   pl.col("close").last().alias("C"),
                   pl.col(gcol).first().alias("_g")])
             .sort(gcol))
    # shift to use PRIOR period
    agg = agg.with_columns([pl.col("H").shift(1).alias("pH"),
                            pl.col("L").shift(1).alias("pL"),
                            pl.col("C").shift(1).alias("pC")])
    piv = classic_pivots(agg["pH"], agg["pL"], agg["pC"])
    suffix = "_" + period
    cols = {gcol: agg[gcol]}
    for name, series in piv.items():
        cols[name + suffix] = series
    pivdf = pl.DataFrame(cols)
    return df.join(pivdf, on=gcol, how="left").drop(gcol)


def detect_crossings(times, closes, levels_dict, period_key):
    """Yield crossing events. A crossing of level L at bar t requires
    sign change of (close - L) between t-1 and t, within same period."""
    n = len(closes)
    events = []  # (idx, level_name, direction)
    for lvl_name, lvl_arr in levels_dict.items():
        prev_close = closes[:-1]
        cur_close = closes[1:]
        prev_lvl = lvl_arr[:-1]
        cur_lvl = lvl_arr[1:]
        same_period = period_key[:-1] == period_key[1:]
        valid = same_period & ~np.isnan(cur_lvl) & ~np.isnan(prev_lvl)
        up = valid & (prev_close < prev_lvl) & (cur_close >= cur_lvl)
        dn = valid & (prev_close > prev_lvl) & (cur_close <= cur_lvl)
        for idx in np.nonzero(up)[0]:
            events.append((idx+1, lvl_name, "UP"))
        for idx in np.nonzero(dn)[0]:
            events.append((idx+1, lvl_name, "DOWN"))
    events.sort(key=lambda e: e[0])
    return events


all_rows = []
for sym in SYMBOLS:
    p = f"{DATA}/{sym}_M1.parquet"
    if not Path(p).exists():
        print(f"skip {sym}", flush=True); continue
    print(f"processing {sym}...", flush=True)
    m1 = pl.scan_parquet(p).select(["time","open","high","low","close"]).sort("time").collect()
    m1 = compute_period_pivots(m1, "D")
    m1 = compute_period_pivots(m1, "W")

    times = m1["time"].to_numpy()
    closes = m1["close"].to_numpy().astype(float)
    dates = m1["time"].dt.date().to_numpy()
    hours = m1["time"].dt.hour().to_numpy()
    # period keys for same-period guard (day for D levels, week for W)
    day_key = m1["time"].dt.strftime("%Y-%m-%d").to_numpy()
    week_key = m1["time"].dt.strftime("%G-%V").to_numpy()

    lvlD = {nm: m1[nm].to_numpy().astype(float) for nm in ALL_LEVELS if nm.endswith("_D")}
    lvlW = {nm: m1[nm].to_numpy().astype(float) for nm in ALL_LEVELS if nm.endswith("_W")}

    evD = detect_crossings(times, closes, lvlD, day_key)
    evW = detect_crossings(times, closes, lvlW, week_key)
    events = sorted(evD + evW, key=lambda e: e[0])

    # Build transitions: next crossing event the SAME UTC day
    for i, (idx, lvl, dirn) in enumerate(events):
        d = dates[idx]; h = int(hours[idx])
        nxt = "EOD"
        for j in range(i+1, len(events)):
            jidx, jlvl, jdir = events[j]
            if dates[jidx] != d:
                break
            nxt = jlvl
            break
        all_rows.append({"sym": sym, "hour": h, "from_level": lvl,
                         "direction": dirn, "next_level": nxt})

df = pl.DataFrame(all_rows)
df.write_parquet(OUTDIR / "pivot_transitions.parquet")
print(f"\nTotal crossing events: {len(df)}", flush=True)
print("done — run pivot_edge_report.py to build the markdown", flush=True)
