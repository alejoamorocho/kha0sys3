"""Pivot fade management study — realised R:R for the edge setups.

For each confirmed edge setup, walk M1 forward the same UTC day:
  - 1R = distance from entry to the INVALIDATION level (next pivot in the
    breakout direction). SL = 1R against the trade.
  - TP grid in R-multiples. RR>=1 honoured.
  - SL-first conservative on ties. Friction 0.3R.

Setups (FADE = trade opposite breakout; CONT = follow):
  PP_D UP->SHORT, R1_D UP->SHORT, R2_D UP->SHORT, S2_D DOWN->LONG (fades)
  PP_D DOWN->SHORT, R1_D DOWN->SHORT (continuations)
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
RR_GRID = [0.5, 1.0, 1.5, 2.0, 3.0]
FRICTION_R = 0.3

D_LEVELS = ["S3_D","S2_D","S1_D","PP_D","R1_D","R2_D","R3_D"]
LVL_ORD = {n:i for i,n in enumerate(D_LEVELS)}

SETUPS = [
    ("PP_D","UP","SHORT","FADE"),
    ("R1_D","UP","SHORT","FADE"),
    ("R2_D","UP","SHORT","FADE"),
    ("S2_D","DOWN","LONG","FADE"),
    ("PP_D","DOWN","SHORT","CONT"),
    ("R1_D","DOWN","SHORT","CONT"),
]

def classic_pivots(h,l,c):
    pp=(h+l+c)/3.0; rng=h-l
    return {"PP":pp,"R1":2*pp-l,"S1":2*pp-h,"R2":pp+rng,"S2":pp-rng,
            "R3":h+2*(pp-l),"S3":l-2*(pp-h)}

def daily_pivots(m1):
    df=m1.with_columns(pl.col("time").dt.date().alias("d"))
    agg=(df.group_by("d").agg([pl.col("high").max().alias("H"),pl.col("low").min().alias("L"),
          pl.col("close").last().alias("C")]).sort("d"))
    agg=agg.with_columns([pl.col("H").shift(1).alias("pH"),pl.col("L").shift(1).alias("pL"),
                          pl.col("C").shift(1).alias("pC")])
    piv=classic_pivots(agg["pH"],agg["pL"],agg["pC"])
    cols={"d":agg["d"]}
    for nm in D_LEVELS:
        cols[nm]=piv[nm[:-2]]
    return df.join(pl.DataFrame(cols),on="d",how="left")

rows=[]
for sym in SYMBOLS:
    p=f"{DATA}/{sym}_M1.parquet"
    if not Path(p).exists(): continue
    print(f"{sym}...",flush=True)
    m1=pl.scan_parquet(p).select(["time","open","high","low","close"]).sort("time").collect()
    m1=daily_pivots(m1)
    closes=m1["close"].to_numpy().astype(float)
    highs=m1["high"].to_numpy().astype(float)
    lows=m1["low"].to_numpy().astype(float)
    hours=m1["time"].dt.hour().to_numpy()
    levarr={nm:m1[nm].to_numpy().astype(float) for nm in D_LEVELS}
    daykey=m1["time"].dt.strftime("%Y-%m-%d").to_numpy()
    n=len(closes)
    for lvl,bdir,tdir,kind in SETUPS:
        L=levarr[lvl]; oi=LVL_ORD[lvl]
        prevc=closes[:-1]; curc=closes[1:]
        prevL=L[:-1]; curL=L[1:]
        same=daykey[:-1]==daykey[1:]
        valid=same & ~np.isnan(curL)
        if bdir=="UP":
            cross=valid&(prevc<prevL)&(curc>=curL)
        else:
            cross=valid&(prevc>prevL)&(curc<=curL)
        idxs=np.nonzero(cross)[0]+1
        seen=set()
        for idx in idxs:
            dk=daykey[idx]
            if (lvl,dk) in seen: continue
            seen.add((lvl,dk))
            entry=closes[idx]
            inv_oi = oi+1 if bdir=="UP" else oi-1
            if inv_oi<0 or inv_oi>6: continue
            inv_price=levarr[D_LEVELS[inv_oi]][idx]
            if np.isnan(inv_price): continue
            R=abs(inv_price-entry)
            if R<=0: continue
            j=idx+1
            mfe=0.0; mae=0.0
            while j<n and daykey[j]==dk:
                hi=highs[j]; lo=lows[j]
                if tdir=="LONG":
                    fav=(hi-entry); adv=(entry-lo)
                else:
                    fav=(entry-lo); adv=(hi-entry)
                if fav>mfe: mfe=fav
                if adv>mae: mae=adv
                j+=1
            rows.append({"sym":sym,"setup":f"{lvl}_{bdir}_{tdir}","kind":kind,
                         "hour":int(hours[idx]),"R":float(R),
                         "mfe_R":float(mfe/R),"mae_R":float(mae/R)})

df=pl.DataFrame(rows)
df.write_parquet(OUTDIR/"pivot_mgmt_raw.parquet")
print(f"\n{len(df)} simulated setups",flush=True)

def eval_setup(sub):
    mfe=sub["mfe_R"].to_numpy(); mae=sub["mae_R"].to_numpy(); n=len(mfe)
    res={}
    for rr in RR_GRID:
        sl_hit=mae>=1.0
        tp_hit=mfe>=rr
        win=tp_hit & ~sl_hit
        exp=0.0
        for k in range(n):
            if win[k]: exp+=rr-FRICTION_R
            elif sl_hit[k]: exp+=-1-FRICTION_R
            else: exp+=-0.2
        exp/=n if n else 1
        gw=win.sum()*rr
        gl=sl_hit.sum()*1.0+((~tp_hit)&(~sl_hit)).sum()*0.2
        pf=gw/gl if gl>0 else float('inf')
        res[rr]={"n":n,"wr":win.mean(),"exp":exp,"pf":pf}
    return res

md=[]
md.append("# Pivot Fade — Análisis de Gestión (R:R)\n")
md.append(f"**Setups simulados:** {len(df):,} · SL=1R (siguiente nivel pivot) · fricción {FRICTION_R}R · SL-first\n")
md.append("WR = alcanza TP (rr·R favorable) antes del SL (1R adverso). Expectancy neta de fricción. R:R≥1 respetado.\n")

md.append("## Por setup (todos los símbolos/horas)\n")
for setup in df["setup"].unique().to_list():
    sub=df.filter(pl.col("setup")==setup)
    if len(sub)<200: continue
    r=eval_setup(sub)
    md.append(f"\n### {setup}  (n={len(sub):,})\n")
    md.append("| R:R | WR | expectancy_R | PF |")
    md.append("|---|---|---|---|")
    for rr in RR_GRID:
        e=r[rr]; flag=" ✅" if e["exp"]>0 and rr>=1.0 else ""
        md.append(f"| 1:{rr} | {e['wr']*100:.0f}% | {e['exp']:+.3f}{flag} | {min(e['pf'],99):.2f} |")

md.append("\n## Mejor horario por setup (R:R 1:1)\n")
md.append("| setup | mejor hora UTC | n | WR | exp_R |")
md.append("|---|---|---|---|---|")
for setup in df["setup"].unique().to_list():
    best=None
    for h in range(24):
        sub=df.filter((pl.col("setup")==setup)&(pl.col("hour")==h))
        if len(sub)<80: continue
        e=eval_setup(sub)[1.0]
        if best is None or e["exp"]>best[1]["exp"]: best=(h,e)
    if best and best[1]["exp"]>0:
        md.append(f"| {setup} | {best[0]:02d}h | {best[1]['n']} | {best[1]['wr']*100:.0f}% | {best[1]['exp']:+.3f} |")

md.append("\n## EDGE ESTRELLA S2_D_DOWN_LONG · por símbolo (R:R 1:1)\n")
md.append("| símbolo | n | WR | exp_R | PF |")
md.append("|---|---|---|---|---|")
star=df.filter(pl.col("setup")=="S2_D_DOWN_LONG")
for sym in sorted(star["sym"].unique().to_list()):
    sub=star.filter(pl.col("sym")==sym)
    if len(sub)<50: continue
    e=eval_setup(sub)[1.0]
    md.append(f"| {sym} | {e['n']} | {e['wr']*100:.0f}% | {e['exp']:+.3f} | {min(e['pf'],99):.2f} |")

md.append("\n## Notas\n")
md.append("- 1R = distancia entry→siguiente nivel pivot en dirección de ruptura (SL ahí).\n")
md.append("- SL-first en empates. 'neither' (ni TP ni SL ese día) = -0.2R timeout.\n")
md.append("- Fricción 0.3R/trade. R:R≥1 = tu mínimo.\n")
(OUTDIR/"Pivot_Management_Report.md").write_text("\n".join(md),encoding="utf-8")
print("WROTE",OUTDIR/"Pivot_Management_Report.md")
