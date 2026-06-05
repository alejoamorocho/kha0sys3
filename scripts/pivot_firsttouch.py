"""Pivot first-touch study — the clean directional question.

Given price reaches level X (M1 close crosses it, first time in the
day/week), does it touch the NEXT level (X+1) BEFORE returning to the
PREVIOUS level (X-1)?

  - target_up   = adjacent level above (X+1)
  - target_down = adjacent level below (X-1)
  - Walk M1 within the level's validity (same day for Daily pivots,
    same week for Weekly). First high>=X+1 -> "UP first". First
    low<=X-1 -> "DOWN first". Levels are ~daily-range apart so intra-bar
    ambiguity is negligible (handled SL-... conservative if both in one bar).

This is metodologically clean: large, real targets; no tiny SL.
We report P(UP first) per level, and CRUCIALLY break it down BY YEAR to
verify the bias is stable across the whole history (not data-mined noise).

TREND vs FADE interpretation depends on the break direction recorded.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import numpy as np
import polars as pl
from collections import defaultdict

SYMBOLS = ["XAUUSD","XAGUSD","BRENT","WTI","GBPUSD","GBPJPY","EURUSD",
           "GBPAUD","USDJPY","AUDUSD","EURJPY","NASDAQ100","NATGAS","SP500"]
DATA = "data/enriched_math_tf"
OUTDIR = Path("reports/pivot"); OUTDIR.mkdir(parents=True, exist_ok=True)
LEVELS = ["S3","S2","S1","PP","R1","R2","R3"]
INTER = ["S2","S1","PP","R1","R2"]  # levels with neighbors on both sides

def classic_pivots(h,l,c):
    pp=(h+l+c)/3.0; rng=h-l
    return {"PP":pp,"R1":2*pp-l,"S1":2*pp-h,"R2":pp+rng,"S2":pp-rng,
            "R3":h+2*(pp-l),"S3":l-2*(pp-h)}

def period_pivots(m1, period):
    if period=="D":
        key=pl.col("time").dt.date(); g="d"
    else:
        key=pl.col("time").dt.strftime("%G-%V"); g="w"
    df=m1.with_columns(key.alias(g))
    agg=(df.group_by(g).agg([pl.col("high").max().alias("H"),pl.col("low").min().alias("L"),
          pl.col("close").last().alias("C")]).sort(g))
    agg=agg.with_columns([pl.col("H").shift(1).alias("pH"),pl.col("L").shift(1).alias("pL"),
                          pl.col("C").shift(1).alias("pC")])
    piv=classic_pivots(agg["pH"],agg["pL"],agg["pC"])
    cols={g:agg[g]}
    for nm in LEVELS: cols[f"{nm}_{period}"]=piv[nm]
    return df.join(pl.DataFrame(cols),on=g,how="left").drop(g), g

rows=[]
for sym in SYMBOLS:
    p=f"{DATA}/{sym}_M1.parquet"
    if not Path(p).exists(): continue
    print(f"{sym}...",flush=True)
    m1=pl.scan_parquet(p).select(["time","open","high","low","close"]).sort("time").collect()
    m1,_=period_pivots(m1,"D"); m1,_=period_pivots(m1,"W")
    closes=m1["close"].to_numpy().astype(float)
    highs=m1["high"].to_numpy().astype(float)
    lows=m1["low"].to_numpy().astype(float)
    years=m1["time"].dt.year().to_numpy()
    daykey=m1["time"].dt.strftime("%Y-%m-%d").to_numpy()
    weekkey=m1["time"].dt.strftime("%G-%V").to_numpy()
    n=len(closes)
    for period,pkey in (("D",daykey),("W",weekkey)):
        lev={nm:m1[f"{nm}_{period}"].to_numpy().astype(float) for nm in LEVELS}
        for li,lvl in enumerate(INTER):
            oi=LEVELS.index(lvl)
            up_name=LEVELS[oi+1]; dn_name=LEVELS[oi-1]
            L=lev[lvl]
            prevc=closes[:-1]; curc=closes[1:]; prevL=L[:-1]; curL=L[1:]
            same=pkey[:-1]==pkey[1:]; valid=same&~np.isnan(curL)
            up_cross=valid&(prevc<prevL)&(curc>=curL)
            dn_cross=valid&(prevc>prevL)&(curc<=curL)
            for bdir,mask in (("UP",up_cross),("DOWN",dn_cross)):
                idxs=np.nonzero(mask)[0]+1
                seen=set()
                for idx in idxs:
                    k=pkey[idx]
                    if (lvl,k) in seen: continue
                    seen.add((lvl,k))
                    up_t=lev[up_name][idx]; dn_t=lev[dn_name][idx]
                    if np.isnan(up_t) or np.isnan(dn_t): continue
                    # walk within period validity
                    res="NEITHER"
                    j=idx+1
                    while j<n and pkey[j]==k:
                        hi=highs[j]; lo=lows[j]
                        up_hit=hi>=up_t; dn_hit=lo<=dn_t
                        if up_hit and dn_hit:
                            res="BOTH"; break  # ambiguous same bar (rare)
                        if up_hit: res="UP"; break
                        if dn_hit: res="DOWN"; break
                        j+=1
                    rows.append({"sym":sym,"period":period,"level":lvl,
                        "bdir":bdir,"year":int(years[idx]),"result":res})

df=pl.DataFrame(rows)
df.write_parquet(OUTDIR/"pivot_firsttouch.parquet")
print(f"\n{len(df)} events",flush=True)
print("done")
