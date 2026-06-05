"""Pivot edge BY HOUR — the key cut.

Aggregate-over-the-whole-day washes out the edge. Session opens (London 07h,
NY 12:30-13:30, Asia 00h) behave very differently. For each (level, break dir,
trade type) we compute expectancy PER UTC HOUR using the real geometric R:R,
then flag hours where exp>0 AND verify the bias is stable across years
(anti-overfit).

Saves a per-event parquet (with hour) and a markdown of the positive
hour-setups with yearly consistency.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import numpy as np, polars as pl
from collections import defaultdict

SYMBOLS=["XAUUSD","XAGUSD","BRENT","WTI","GBPUSD","GBPJPY","EURUSD","GBPAUD",
         "USDJPY","AUDUSD","EURJPY","NASDAQ100","NATGAS","SP500"]
LEVELS=["S3","S2","S1","PP","R1","R2","R3"]; INTER=["S2","S1","PP","R1","R2"]
FR=0.1
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

rows=[]
for sym in SYMBOLS:
    print(sym,flush=True)
    m1=pl.scan_parquet(f"data/enriched_math_tf/{sym}_M1.parquet").select(["time","high","low","close"]).sort("time").collect()
    m1=dpiv(m1)
    closes=m1["close"].to_numpy().astype(float);highs=m1["high"].to_numpy().astype(float);lows=m1["low"].to_numpy().astype(float)
    dk=m1["time"].dt.strftime("%Y-%m-%d").to_numpy(); hrs=m1["time"].dt.hour().to_numpy(); yrs=m1["time"].dt.year().to_numpy(); n=len(closes)
    lev={nm:m1[nm].to_numpy().astype(float) for nm in LEVELS}
    for lvl in INTER:
        oi=LEVELS.index(lvl); up=lev[LEVELS[oi+1]]; dn=lev[LEVELS[oi-1]]; L=lev[lvl]
        pc=closes[:-1];cc=closes[1:];pL=L[:-1];cL=L[1:];same=dk[:-1]==dk[1:];valid=same&~np.isnan(cL)
        for bdir in ("UP","DOWN"):
            mask=(valid&(pc<pL)&(cc>=cL)) if bdir=="UP" else (valid&(pc>pL)&(cc<=cL))
            idxs=np.nonzero(mask)[0]+1; seen=set()
            for idx in idxs:
                k=dk[idx]
                if (lvl,k) in seen: continue
                seen.add((lvl,k))
                ut=up[idx];dt=dn[idx];e=closes[idx]
                if np.isnan(ut) or np.isnan(dt): continue
                d_up=abs(ut-e);d_dn=abs(e-dt)
                if d_up<=0 or d_dn<=0: continue
                j=idx+1;res="N"
                while j<n and dk[j]==k:
                    if highs[j]>=ut: res="U";break
                    if lows[j]<=dt: res="D";break
                    j+=1
                rr_tr=(d_up/d_dn) if bdir=="UP" else (d_dn/d_up)
                rows.append({"sym":sym,"level":lvl,"bdir":bdir,"hour":int(hrs[idx]),
                             "year":int(yrs[idx]),"res":res,"rr_tr":float(rr_tr)})

df=pl.DataFrame(rows)
df.write_parquet("reports/pivot/pivot_byhour.parquet")
print(f"{len(df)} events",flush=True)

# Exclude S2 (geometric artifact). Evaluate per (level,bdir,trade,hour)
df=df.filter(pl.col("level")!="S2")
def exp_of(sub, trade):
    n=len(sub)
    if n<200: return None
    u=(sub["res"]=="U").sum(); d=(sub["res"]=="D").sum(); res=u+d
    if res==0: return None
    rr_tr=float(sub["rr_tr"].mean()); rr_fd=1/rr_tr if rr_tr>0 else 0
    rate=res/n
    bd=sub["bdir"][0]
    wr_tr=(u/res) if bd=="UP" else (d/res); wr_fd=1-wr_tr
    if trade=="TREND":
        wr,rr=wr_tr,rr_tr
    else:
        wr,rr=wr_fd,rr_fd
    pw=rate*wr; ploss=rate*(1-wr)
    exp=pw*rr - ploss - (pw+ploss)*FR
    return {"n":n,"wr":wr,"rr":rr,"exp":exp}

md=["# Pivot Edge POR HORARIO (R:R real, S2 excluido por artefacto)\n",
    "exp con no-resuelto=scratch, fricción 0.1R. Sesiones clave: 07h London, "
    "12-13h NY, 00h Asia.\n"]

positives=[]
for lvl in ["S1","PP","R1","R2"]:
    for bdir in ("UP","DOWN"):
        for trade in ("TREND","FADE"):
            for h in range(24):
                sub=df.filter((pl.col("level")==lvl)&(pl.col("bdir")==bdir)&(pl.col("hour")==h))
                e=exp_of(sub,trade)
                if e and e["exp"]>0.05 and e["n"]>=300:
                    positives.append((lvl,bdir,trade,h,e))
positives.sort(key=lambda x:-x[4]["exp"])
md.append(f"## Setups (nivel×dir×tipo×HORA) con exp>0.05R, n>=300: {len(positives)}\n")
md.append("| nivel | ruptura | tipo | hora UTC | n | WR_res | R:R | exp_R |")
md.append("|---|---|---|---|---|---|---|---|")
for lvl,bd,tr,h,e in positives:
    md.append(f"| {lvl} | {bd} | {tr} | {h:02d}h | {e['n']:,} | {e['wr']*100:.0f}% | {e['rr']:.2f} | {e['exp']:+.3f} |")

# Yearly consistency for top positives
md.append("\n## Consistencia AÑO-A-AÑO (top 10 positivos)\n")
for lvl,bd,tr,h,e in positives[:10]:
    sub=df.filter((pl.col("level")==lvl)&(pl.col("bdir")==bd)&(pl.col("hour")==h))
    line=f"- **{lvl} {bd} {tr} {h:02d}h** (exp {e['exp']:+.3f}): "
    parts=[]
    for y in range(2018,2027):
        ys=sub.filter(pl.col("year")==y)
        ey=exp_of(ys,tr)
        if ey: parts.append(f"{y%100:02d}:{ey['exp']:+.2f}")
    md.append(line+" ".join(parts))

Path("reports/pivot/Pivot_ByHour.md").write_text("\n".join(md),encoding="utf-8")
print(f"positives: {len(positives)}")
for lvl,bd,tr,h,e in positives[:15]:
    print(f"  {lvl} {bd} {tr} {h:02d}h: n={e['n']} WR={e['wr']*100:.0f}% RR={e['rr']:.2f} exp={e['exp']:+.3f}")
