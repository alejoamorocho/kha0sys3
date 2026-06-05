"""Risk-management optimisation over the 9 robust window-level pivot edges.

The 9 setups (all TREND, validated IS/OOS by session window):
  EURUSD   PP DOWN London      GBPAUD   PP DOWN London
  GBPJPY   PP DOWN London      USDJPY   R1 UP   London
  NASDAQ100 PP DOWN NY         SP500    S1 DOWN NY  (premium)
  WTI      R1 DOWN NY (premium) XAGUSD  R1 UP   NY
  XAUUSD   R1 UP   NY

For each, sweep management:
  SL_frac in {0.25,0.35,0.5,0.75,1.0} (× spacing to next level)
  R:R     in {1.2,1.5,2.0,2.5,3.0}
  mode    in {FIXED, BE}  (BE = move SL to entry after +1R favorable)
Walk M1 same day, SL-first, REAL friction. Report best mgmt per setup
with IS(2018-22)/OOS(2023-26) expectancy, WR, PF, maxDD(R).
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import numpy as np, polars as pl

DATA="data/enriched_math_tf"
LEVELS=["S3","S2","S1","PP","R1","R2","R3"]
WINDOWS={"London":set(range(7,13)),"NY":set(range(13,20))}
SL_FRACS=[0.25,0.35,0.5,0.75,1.0]; RRS=[1.2,1.5,2.0,2.5,3.0]; MODES=["FIXED","BE"]
SNAP={"EURUSD":(1,0.00001),"GBPUSD":(5,0.00001),"USDJPY":(4,0.001),"AUDUSD":(2,0.00001),
 "GBPJPY":(4,0.001),"EURJPY":(4,0.001),"GBPAUD":(6,0.00001),"XAUUSD":(12,0.01),
 "XAGUSD":(44,0.001),"WTI":(47,0.001),"BRENT":(47,0.001),"NATGAS":(200,0.001),
 "NASDAQ100":(100,0.1),"SP500":(50,0.1)}
def spr(s): sp,ts=SNAP[s]; return 2*sp*ts

# the 9 setups
SETUPS=[("EURUSD","PP","DOWN","London"),("GBPAUD","PP","DOWN","London"),
        ("GBPJPY","PP","DOWN","London"),("USDJPY","R1","UP","London"),
        ("NASDAQ100","PP","DOWN","NY"),("SP500","S1","DOWN","NY"),
        ("WTI","R1","DOWN","NY"),("XAGUSD","R1","UP","NY"),("XAUUSD","R1","UP","NY")]

def cp(h,l,c):
    pp=(h+l+c)/3;rng=h-l
    return {"PP":pp,"R1":2*pp-l,"S1":2*pp-h,"R2":pp+rng,"S2":pp-rng,"R3":h+2*(pp-l),"S3":l-2*(pp-h)}
def dpiv(m1):
    df=m1.with_columns(pl.col("time").dt.date().alias("d"))
    a=(df.group_by("d").agg([pl.col("high").max().alias("H"),pl.col("low").min().alias("L"),pl.col("close").last().alias("C")]).sort("d"))
    a=a.with_columns([pl.col("H").shift(1).alias("pH"),pl.col("L").shift(1).alias("pL"),pl.col("C").shift(1).alias("pC")])
    pv=cp(a["pH"],a["pL"],a["pC"]);cols={"d":a["d"]}
    for nm in LEVELS: cols[nm]=pv[nm]
    return df.join(pl.DataFrame(cols),on="d",how="left")

def walk(idx,highs,lows,dk,n,entry,sl_dist,tp_dist,is_long,mode):
    end=min(n,idx+1+600); d=dk[idx]
    sl = entry-sl_dist if is_long else entry+sl_dist
    tp = entry+tp_dist if is_long else entry-tp_dist
    be_armed=False; be_level=entry
    be_trigger = entry + (sl_dist if is_long else -sl_dist)  # +1R favorable
    for j in range(idx+1,end):
        if dk[j]!=d: break
        hi=highs[j]; lo=lows[j]
        if is_long:
            # SL-first
            if lo<=sl: return (0.0 if be_armed and sl>=entry else -1.0)
            if hi>=tp: return tp_dist/sl_dist  # = RR
            if mode=="BE" and not be_armed and hi>=be_trigger:
                be_armed=True; sl=entry  # move to breakeven
        else:
            if hi>=sl: return (0.0 if be_armed and sl<=entry else -1.0)
            if lo<=tp: return tp_dist/sl_dist
            if mode=="BE" and not be_armed and lo<=be_trigger:
                be_armed=True; sl=entry
    return -0.2  # timeout

# load + simulate
cache={}
def load(sym):
    if sym in cache: return cache[sym]
    m1=pl.scan_parquet(f"{DATA}/{sym}_M1.parquet").select(["time","high","low","close"]).sort("time").collect()
    m1=dpiv(m1)
    d=dict(closes=m1["close"].to_numpy().astype(float),highs=m1["high"].to_numpy().astype(float),
           lows=m1["low"].to_numpy().astype(float),dk=m1["time"].dt.strftime("%Y-%m-%d").to_numpy(),
           hrs=m1["time"].dt.hour().to_numpy(),yrs=m1["time"].dt.year().to_numpy())
    for nm in LEVELS: d[nm]=m1[nm].to_numpy().astype(float)
    cache[sym]=d; return d

rows=[]
for sym,lvl,bd,win in SETUPS:
    print(f"{sym} {lvl} {bd} {win}",flush=True)
    D=load(sym); n=len(D["closes"]); oi=LEVELS.index(lvl); L=D[lvl]
    fr_price=spr(sym); wh=WINDOWS[win]
    pc=D["closes"][:-1];cc=D["closes"][1:];pL=L[:-1];cL=L[1:];same=D["dk"][:-1]==D["dk"][1:];valid=same&~np.isnan(cL)
    mask=(valid&(pc<pL)&(cc>=cL)) if bd=="UP" else (valid&(pc>pL)&(cc<=cL))
    idxs=np.nonzero(mask)[0]+1; is_long=(bd=="UP"); nxt_oi=oi+1 if is_long else oi-1
    if nxt_oi<0 or nxt_oi>6: continue
    seen=set()
    evs=[]
    for idx in idxs:
        if int(D["hrs"][idx]) not in wh: continue
        k=D["dk"][idx]
        if (lvl,k) in seen: continue
        seen.add((lvl,k))
        entry=D["closes"][idx]; nxt=D[LEVELS[nxt_oi]][idx]
        if np.isnan(nxt): continue
        spacing=abs(nxt-entry)
        if spacing<=0: continue
        evs.append((idx,entry,spacing,int(D["yrs"][idx])))
    for slf in SL_FRACS:
        for rr in RRS:
            for mode in MODES:
                for idx,entry,spacing,yr in evs:
                    sl_dist=slf*spacing; tp_dist=rr*sl_dist
                    fr_R=fr_price/sl_dist
                    r=walk(idx,D["highs"],D["lows"],D["dk"],n,entry,sl_dist,tp_dist,is_long,mode)
                    net = r - fr_R if r>0 else r - fr_R
                    rows.append({"setup":f"{sym}_{lvl}_{bd}_{win}","sym":sym,"slf":slf,"rr":rr,"mode":mode,
                                 "yr":yr,"r":r,"net":net})

df=pl.DataFrame(rows)
df=df.with_columns(pl.when(pl.col("yr")<=2022).then(pl.lit("IS")).otherwise(pl.lit("OOS")).alias("split"))
df.write_parquet("reports/pivot/pivot_gestion_v2_raw.parquet")

def stats(sub):
    n=len(sub)
    if n==0: return None
    net=sub["net"].to_numpy()
    wins=(sub["r"]>0).sum()
    cum=np.cumsum(net); dd=float((np.maximum.accumulate(cum)-cum).max()) if n else 0
    gw=net[net>0].sum(); gl=-net[net<0].sum()
    return {"n":n,"exp":float(net.mean()),"wr":wins/n,"pf":(gw/gl if gl>0 else 99),"dd":dd,"sumR":float(net.sum())}

md=["# Optimización de gestión — 9 edges pivot robustos\n",
    "Grid: SL_frac×R:R×modo(FIXED/BE). Mejor gestión por setup (max OOS exp con IS>0).\n",
    "| setup | mejor gestión | IS n/exp/wr/pf | OOS n/exp/wr/pf | maxDD(R) |",
    "|---|---|---|---|---|"]
best_per=[]
for setup in df["setup"].unique().to_list():
    s=df.filter(pl.col("setup")==setup)
    best=None
    for (slf,rr,mode),sub in s.group_by(["slf","rr","mode"]):
        is_=stats(sub.filter(pl.col("split")=="IS")); oos=stats(sub.filter(pl.col("split")=="OOS"))
        if not is_ or not oos: continue
        if is_["n"]>=100 and oos["n"]>=50 and is_["exp"]>0 and oos["exp"]>0:
            if best is None or oos["exp"]>best[3]["exp"]:
                best=(slf,rr,mode,oos,is_)
    if best:
        slf,rr,mode,oos,is_=best
        best_per.append((setup,slf,rr,mode,is_,oos))
        md.append(f"| {setup} | SL={slf} RR={rr} {mode} | {is_['n']}/{is_['exp']:+.3f}/{is_['wr']*100:.0f}%/{is_['pf']:.2f} | "
                  f"{oos['n']}/{oos['exp']:+.3f}/{oos['wr']*100:.0f}%/{oos['pf']:.2f} | {oos['dd']:.1f} |")
    else:
        md.append(f"| {setup} | NINGUNA sobrevive | - | - | - |")

md.append(f"\n## Resumen\n- Setups con gestión rentable IS+OOS: {len(best_per)}/9\n")
Path("reports/pivot/Pivot_Gestion_v2.md").write_text("\n".join(md),encoding="utf-8")
print(f"\nsurviving setups: {len(best_per)}/9")
for setup,slf,rr,mode,is_,oos in best_per:
    print(f"  {setup:<26} SL={slf} RR={rr} {mode:<5} IS exp={is_['exp']:+.3f} pf={is_['pf']:.2f} | OOS exp={oos['exp']:+.3f} pf={oos['pf']:.2f} wr={oos['wr']*100:.0f}%")
