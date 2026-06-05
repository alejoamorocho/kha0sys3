"""Pivot TREND management — the robust core (TREND in London/NY), R:R >= 1.2.

For each (symbol, level S1/PP/R1/R2, break dir, session window London/NY),
trade TREND (follow the break). Grid of management:
  - SL_dist = sl_frac * spacing_to_next_level
  - TP_dist = RR * SL_dist, with RR in {1.2, 1.5, 2.0}
  - Walk M1 same UTC day, SL-first conservative.
  - Friction in R = round_turn_spread_price / SL_dist_price (REAL per symbol).

Keep combos that are net-positive in BOTH IS (2018-22) and OOS (2023-26).
Output: reports/pivot/Pivot_Gestion.md + parquet of survivors.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import numpy as np, polars as pl

SYMS=["XAUUSD","XAGUSD","BRENT","WTI","GBPUSD","GBPJPY","EURUSD","GBPAUD",
      "USDJPY","AUDUSD","EURJPY","NASDAQ100","NATGAS","SP500"]
DATA="data/enriched_math_tf"
LEVELS=["S3","S2","S1","PP","R1","R2","R3"]; INTER=["S1","PP","R1","R2"]
WINDOWS={"London":set(range(7,13)),"NY":set(range(13,20))}
SL_FRACS=[0.25,0.40,0.60]; RRS=[1.2,1.5,2.0]
# round-turn spread price per symbol (2 * spread_pt * tick_size)
SNAP={"EURUSD":(1,0.00001),"GBPUSD":(5,0.00001),"USDJPY":(4,0.001),"AUDUSD":(2,0.00001),
 "GBPJPY":(4,0.001),"EURJPY":(4,0.001),"GBPAUD":(6,0.00001),"XAUUSD":(12,0.01),
 "XAGUSD":(44,0.001),"WTI":(47,0.001),"BRENT":(47,0.001),"NATGAS":(200,0.001),
 "NASDAQ100":(100,0.1),"SP500":(50,0.1)}
def spread_price(sym):
    sp,ts=SNAP.get(sym,(10,0.0001)); return 2*sp*ts

def cp(h,l,c):
    pp=(h+l+c)/3; rng=h-l
    return {"PP":pp,"R1":2*pp-l,"S1":2*pp-h,"R2":pp+rng,"S2":pp-rng,"R3":h+2*(pp-l),"S3":l-2*(pp-h)}
def dpiv(m1):
    df=m1.with_columns(pl.col("time").dt.date().alias("d"))
    a=(df.group_by("d").agg([pl.col("high").max().alias("H"),pl.col("low").min().alias("L"),pl.col("close").last().alias("C")]).sort("d"))
    a=a.with_columns([pl.col("H").shift(1).alias("pH"),pl.col("L").shift(1).alias("pL"),pl.col("C").shift(1).alias("pC")])
    pv=cp(a["pH"],a["pL"],a["pC"]); cols={"d":a["d"]}
    for nm in LEVELS: cols[nm]=pv[nm]
    return df.join(pl.DataFrame(cols),on="d",how="left")

def walk(idx,highs,lows,dk,n,tp,sl,is_long):
    end=min(n,idx+1+600); d=dk[idx]
    for j in range(idx+1,end):
        if dk[j]!=d: break
        hi=highs[j]; lo=lows[j]
        if is_long: s=lo<=sl; t=hi>=tp
        else: s=hi>=sl; t=lo<=tp
        if s: return 0   # SL-first
        if t: return 1
    return -1  # timeout

rows=[]
for sym in SYMS:
    print(sym,flush=True)
    m1=pl.scan_parquet(f"{DATA}/{sym}_M1.parquet").select(["time","high","low","close"]).sort("time").collect()
    m1=dpiv(m1)
    closes=m1["close"].to_numpy().astype(float);highs=m1["high"].to_numpy().astype(float);lows=m1["low"].to_numpy().astype(float)
    dk=m1["time"].dt.strftime("%Y-%m-%d").to_numpy();hrs=m1["time"].dt.hour().to_numpy();yrs=m1["time"].dt.year().to_numpy();n=len(closes)
    lev={nm:m1[nm].to_numpy().astype(float) for nm in LEVELS}
    fr_price=spread_price(sym)
    for lvl in INTER:
        oi=LEVELS.index(lvl);L=lev[lvl]
        pc=closes[:-1];cc=closes[1:];pL=L[:-1];cL=L[1:];same=dk[:-1]==dk[1:];valid=same&~np.isnan(cL)
        for bdir in ("UP","DOWN"):
            mask=(valid&(pc<pL)&(cc>=cL)) if bdir=="UP" else (valid&(pc>pL)&(cc<=cL))
            idxs=np.nonzero(mask)[0]+1
            is_long=(bdir=="UP")  # TREND follows break
            nxt_oi=oi+1 if is_long else oi-1
            if nxt_oi<0 or nxt_oi>6: continue
            for wname,wh in WINDOWS.items():
                seen=set()
                for idx in idxs:
                    if int(hrs[idx]) not in wh: continue
                    k=dk[idx]
                    if (lvl,k) in seen: continue
                    seen.add((lvl,k))
                    entry=closes[idx];nxt=lev[LEVELS[nxt_oi]][idx]
                    if np.isnan(nxt): continue
                    spacing=abs(nxt-entry)
                    if spacing<=0: continue
                    yr=int(yrs[idx])
                    for slf in SL_FRACS:
                        sl_dist=slf*spacing
                        if sl_dist<=0: continue
                        fr_R=fr_price/sl_dist
                        for rr in RRS:
                            tp_dist=rr*sl_dist
                            if is_long: tp=entry+tp_dist; sl=entry-sl_dist
                            else: tp=entry-tp_dist; sl=entry+sl_dist
                            r=walk(idx,highs,lows,dk,n,tp,sl,is_long)
                            # net R
                            if r==1: net=rr-fr_R
                            elif r==0: net=-1-fr_R
                            else: net=-0.2-fr_R  # timeout
                            rows.append({"sym":sym,"level":lvl,"bdir":bdir,"win":wname,
                                "slf":slf,"rr":rr,"yr":yr,"net":net,"r":r})

df=pl.DataFrame(rows)
df.write_parquet("reports/pivot/pivot_gestion_raw.parquet")
print(f"{len(df)} sim rows",flush=True)

df=df.with_columns(pl.when(pl.col("yr")<=2022).then(pl.lit("IS")).otherwise(pl.lit("OOS")).alias("split"))
def stats(sub):
    n=len(sub)
    if n==0: return None
    return {"n":n,"exp":float(sub["net"].mean()),"wr":float((sub["r"]==1).mean())}

survivors=[]
for (sym,lvl,bd,w,slf,rr),sub in df.group_by(["sym","level","bdir","win","slf","rr"]):
    is_=stats(sub.filter(pl.col("split")=="IS")); oos=stats(sub.filter(pl.col("split")=="OOS"))
    if not is_ or not oos: continue
    if is_["n"]>=120 and oos["n"]>=60 and is_["exp"]>0 and oos["exp"]>0:
        survivors.append((sym,lvl,bd,w,slf,rr,is_,oos))
survivors.sort(key=lambda x:-min(x[6]["exp"],x[7]["exp"]))

md=["# Gestión de edges pivot TREND — R:R>=1.2, fricción real, IS/OOS\n",
    f"Combos simulados: {df.select(['sym','level','bdir','win','slf','rr']).n_unique():,} · "
    f"Supervivientes (exp>0 IS Y OOS, n_IS>=120, n_OOS>=60): {len(survivors)}\n",
    "SL=slf×spacing · TP=RR×SL · walk M1 SL-first · fricción spread real.\n",
    "| activo | nivel | dir | sesión | SL_frac | R:R | IS n/exp/wr | OOS n/exp/wr |",
    "|---|---|---|---|---|---|---|---|"]
for sym,lvl,bd,w,slf,rr,is_,oos in survivors:
    md.append(f"| {sym} | {lvl} | {bd} | {w} | {slf} | {rr} | "
              f"{is_['n']}/{is_['exp']:+.3f}/{is_['wr']*100:.0f}% | "
              f"{oos['n']}/{oos['exp']:+.3f}/{oos['wr']*100:.0f}% |")
from collections import Counter
if survivors:
    md.append("\n## Resumen supervivientes\n")
    md.append(f"- Activos: {len(set(s[0] for s in survivors))}/14: {sorted(set(s[0] for s in survivors))}")
    md.append(f"- R:R: {dict(Counter(s[5] for s in survivors))}")
    md.append(f"- Sesión: {dict(Counter(s[3] for s in survivors))}")
    md.append(f"- Nivel: {dict(Counter(s[1] for s in survivors))}")
Path("reports/pivot/Pivot_Gestion.md").write_text("\n".join(md),encoding="utf-8")
print(f"survivors: {len(survivors)}")
for s in survivors[:25]:
    print(f"  {s[0]:<10} {s[1]} {s[2]:<4} {s[3]:<7} SL={s[4]} RR={s[5]} | IS exp={s[6]['exp']:+.3f} OOS exp={s[7]['exp']:+.3f}")
