"""Pivot management v2 — PROFESSIONAL spec (per user 2026-06-05).

Key corrections vs v1:
  - TP is a FRACTION of the spacing to the next level (e.g. 50% between S2
    and S1), NOT the full next level.
  - Fixed R:R = 2:1 (SL distance = TP distance / 2). Each loss must be paid
    by 2 wins -> break-even WR ~ 33% (38% with friction).
  - Test BOTH directions per level break: FADE (trade opposite the break)
    and TREND (follow the break).
  - Full M1 walk: entry at the M1 close that crosses the level; then walk
    M1 minute-by-minute, SL-first conservative, until TP / SL / EOD.
  - Friction 0.3R. Report median SL distance in ATR so we know it's viable.

Setups: each intermediate level (S2,S1,PP,R1,R2 for Daily + Weekly),
each break direction (UP/DOWN), each trade type (FADE/TREND),
TP fraction grid {0.25, 0.5, 0.75} of spacing -> SL = TP/2 (R:R 2:1).
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import numpy as np
import polars as pl

SYMBOLS = ["XAUUSD","XAGUSD","BRENT","WTI","GBPUSD","GBPJPY","EURUSD",
           "GBPAUD","USDJPY","AUDUSD","EURJPY","NASDAQ100","NATGAS","SP500"]
DATA = "data/enriched_math_tf"
OUTDIR = Path("reports/pivot"); OUTDIR.mkdir(parents=True, exist_ok=True)
TP_FRACS = [0.25, 0.5, 0.75]
RR = 2.0                 # fixed 2:1 -> SL = TP/RR
FRICTION_R = 0.3
MAX_HOLD_BARS = 600      # cap intraday walk (~10h)

LEVELS_ORDER = ["S3","S2","S1","PP","R1","R2","R3"]  # low->high
INTER = ["S2","S1","PP","R1","R2"]

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
    for nm in LEVELS_ORDER:
        cols[f"{nm}_{period}"]=piv[nm]
    return df.join(pl.DataFrame(cols),on=g,how="left").drop(g)

def walk(entry_idx, highs, lows, daykey, n, tp_price, sl_price, is_long):
    """Walk M1 from entry_idx+1, SL-first. Return 'WIN','LOSS','TIME'."""
    end=min(n, entry_idx+1+MAX_HOLD_BARS)
    dk=daykey[entry_idx]
    for j in range(entry_idx+1, end):
        if daykey[j]!=dk: break
        hi=highs[j]; lo=lows[j]
        if is_long:
            sl=lo<=sl_price; tp=hi>=tp_price
        else:
            sl=hi>=sl_price; tp=lo<=tp_price
        if sl and tp: return "LOSS"   # SL-first conservative
        if sl: return "LOSS"
        if tp: return "WIN"
    return "TIME"

rows=[]
for sym in SYMBOLS:
    p=f"{DATA}/{sym}_M1.parquet"
    if not Path(p).exists(): continue
    print(f"{sym}...",flush=True)
    m1=pl.scan_parquet(p).select(["time","open","high","low","close","atr_14"]).sort("time").collect()
    m1=period_pivots(m1,"D"); m1=period_pivots(m1,"W")
    closes=m1["close"].to_numpy().astype(float)
    highs=m1["high"].to_numpy().astype(float)
    lows=m1["low"].to_numpy().astype(float)
    hours=m1["time"].dt.hour().to_numpy()
    atr=m1["atr_14"].to_numpy().astype(float)
    daykey=m1["time"].dt.strftime("%Y-%m-%d").to_numpy()
    n=len(closes)
    for period in ("D","W"):
        levarr={nm:m1[f"{nm}_{period}"].to_numpy().astype(float) for nm in LEVELS_ORDER}
        for lvl in INTER:
            oi=LEVELS_ORDER.index(lvl)
            L=levarr[lvl]
            prevc=closes[:-1]; curc=closes[1:]; prevL=L[:-1]; curL=L[1:]
            same=daykey[:-1]==daykey[1:]; valid=same & ~np.isnan(curL)
            up_cross=valid&(prevc<prevL)&(curc>=curL)
            dn_cross=valid&(prevc>prevL)&(curc<=curL)
            for bdir,mask in (("UP",up_cross),("DOWN",dn_cross)):
                idxs=np.nonzero(mask)[0]+1
                seen=set()
                for idx in idxs:
                    dk=daykey[idx]
                    if (lvl,dk) in seen: continue
                    seen.add((lvl,dk))
                    entry=closes[idx]; a=atr[idx]
                    if np.isnan(a) or a<=0: continue
                    h=int(hours[idx])
                    # Two trade types
                    for ttype in ("FADE","TREND"):
                        if ttype=="FADE":
                            is_long = (bdir=="DOWN")  # break down -> long
                        else:
                            is_long = (bdir=="UP")    # follow up -> long
                        # next level in the trade direction
                        nxt_oi = oi+1 if is_long else oi-1
                        if nxt_oi<0 or nxt_oi>6: continue
                        nxt_price=levarr[LEVELS_ORDER[nxt_oi]][idx]
                        if np.isnan(nxt_price): continue
                        spacing=abs(nxt_price-entry)
                        if spacing<=0: continue
                        for tpf in TP_FRACS:
                            tp_dist=tpf*spacing
                            sl_dist=tp_dist/RR
                            if is_long:
                                tp_price=entry+tp_dist; sl_price=entry-sl_dist
                            else:
                                tp_price=entry-tp_dist; sl_price=entry+sl_dist
                            out=walk(idx,highs,lows,daykey,n,tp_price,sl_price,is_long)
                            rows.append({"sym":sym,"period":period,"level":lvl,
                                "bdir":bdir,"ttype":ttype,"tpf":tpf,"hour":h,
                                "outcome":out,"sl_atr":sl_dist/a})

df=pl.DataFrame(rows)
df.write_parquet(OUTDIR/"pivot_mgmt_v2_raw.parquet")
print(f"\n{len(df)} trades simulated",flush=True)
print("done")
