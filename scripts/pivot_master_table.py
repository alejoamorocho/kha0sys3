"""Master table: EVERY (symbol, level, entry-dir) with TREND and FADE
WR + geometric R:R + expectancy. NEITHER treated as scratch (0) to be
generous. This shows ALL cases transparently so the user can judge.

For a level X broken in direction D:
  TREND target = next level in D, stop = previous level (opposite)
  FADE  target = previous level (opposite), stop = next level in D
WR over RESOLVED events; expectancy over ALL (NEITHER=0 scratch).
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import numpy as np, polars as pl

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

# accumulate per (level, bdir): list of (toward_next, rr_trend, neither)
agg=dict()  # key=(level,bdir) -> dict(sym-> [n, next_first, prev_first, neither, rr_trend_sum])
for sym in SYMBOLS:
    print(sym,flush=True)
    m1=pl.scan_parquet(f"data/enriched_math_tf/{sym}_M1.parquet").select(["time","high","low","close"]).sort("time").collect()
    m1=dpiv(m1)
    closes=m1["close"].to_numpy().astype(float);highs=m1["high"].to_numpy().astype(float);lows=m1["low"].to_numpy().astype(float)
    dk=m1["time"].dt.strftime("%Y-%m-%d").to_numpy(); n=len(closes)
    lev={nm:m1[nm].to_numpy().astype(float) for nm in LEVELS}
    for lvl in INTER:
        oi=LEVELS.index(lvl); up=lev[LEVELS[oi+1]]; dn=lev[LEVELS[oi-1]]; L=lev[lvl]
        pc=closes[:-1];cc=closes[1:];pL=L[:-1];cL=L[1:];same=dk[:-1]==dk[1:];valid=same&~np.isnan(cL)
        for bdir in ("UP","DOWN"):
            mask=(valid&(pc<pL)&(cc>=cL)) if bdir=="UP" else (valid&(pc>pL)&(cc<=cL))
            idxs=np.nonzero(mask)[0]+1; seen=set()
            key=(lvl,bdir)
            d=agg.setdefault(key,{}).setdefault(sym,[0,0,0,0,0.0])
            for idx in idxs:
                k=dk[idx]
                if (lvl,k) in seen: continue
                seen.add((lvl,k))
                ut=up[idx]; dt=dn[idx]; e=closes[idx]
                if np.isnan(ut) or np.isnan(dt): continue
                d_up=abs(ut-e); d_dn=abs(e-dt)
                if d_up<=0 or d_dn<=0: continue
                # walk first touch up vs dn
                j=idx+1;res="N"
                while j<n and dk[j]==k:
                    if highs[j]>=ut: res="U";break
                    if lows[j]<=dt: res="D";break
                    j+=1
                d[0]+=1
                if res=="U": d[1]+=1
                elif res=="D": d[2]+=1
                else: d[3]+=1
                # rr_trend: target in break dir / stop opposite
                rr_tr = (d_up/d_dn) if bdir=="UP" else (d_dn/d_up)
                d[4]+=rr_tr

md=["# Pivot Master Table — TODOS los casos (trend + fade, R:R real)\n",
    "WR sobre eventos resueltos. R:R = distancia(target)/distancia(stop). "
    "exp con NEITHER=scratch(0), fricción 0.1R. Break-even: WR_resuelto × (1+R:R)/... "
    "(exp>0 = rentable).\n",
    "**TREND** = continúa al siguiente nivel. **FADE** = vuelve al anterior.\n"]

def expectancy(wr_res, rr, resolved_rate, win_is_trend, p_trend_res):
    # over ALL events: P(win)=resolved_rate*wr_res ; P(loss)=resolved_rate*(1-wr_res); NEITHER=0
    pw=resolved_rate*wr_res; pl_=resolved_rate*(1-wr_res)
    return pw*rr - pl_*1.0 - (pw+pl_)*FR

print("\nbuilding table...",flush=True)
for lvl in INTER:
    for bdir in ("UP","DOWN"):
        key=(lvl,bdir)
        if key not in agg: continue
        # pooled across symbols
        N=NU=ND=NN=0; RRsum=0.0
        persym=[]
        for sym,d in agg[key].items():
            n,u,dn_,nn,rrs=d
            if n<150: continue
            N+=n;NU+=u;ND+=dn_;NN+=nn;RRsum+=rrs
            res=u+dn_
            rr_tr=rrs/n if n else 0
            wr_trend = (u/res) if res and bdir=="UP" else ((dn_/res) if res else 0)
            persym.append((sym,n,nn/n,wr_trend,rr_tr))
        if N==0: continue
        res=NU+ND; resolved_rate=res/N
        rr_trend=RRsum/N
        rr_fade=1/rr_trend if rr_trend>0 else 0
        # trend WR (resolved): toward break dir
        wr_trend_res = (NU/res) if bdir=="UP" else (ND/res)
        wr_fade_res = 1-wr_trend_res
        exp_tr=expectancy(wr_trend_res,rr_trend,resolved_rate,True,wr_trend_res)
        exp_fd=expectancy(wr_fade_res,rr_fade,resolved_rate,False,wr_trend_res)
        md.append(f"\n## {lvl} roto hacia {bdir}  (n={N:,}, no-resuelto={NN/N*100:.0f}%)\n")
        md.append(f"- **TREND** (→{'arriba' if bdir=='UP' else 'abajo'}): WR_resuelto={wr_trend_res*100:.0f}% · R:R={rr_trend:.2f} · **exp={exp_tr:+.3f}R** {'✅' if exp_tr>0 else ''}")
        md.append(f"- **FADE** (→vuelve): WR_resuelto={wr_fade_res*100:.0f}% · R:R={rr_fade:.2f} · **exp={exp_fd:+.3f}R** {'✅' if exp_fd>0 else ''}")

# Summary: any positive?
pos=[]
for lvl in INTER:
    for bdir in ("UP","DOWN"):
        key=(lvl,bdir)
        if key not in agg: continue
        N=NU=ND=NN=0;RRsum=0.0
        for sym,d in agg[key].items():
            n,u,dn_,nn,rrs=d
            if n<150: continue
            N+=n;NU+=u;ND+=dn_;NN+=nn;RRsum+=rrs
        if N==0: continue
        res=NU+ND;rr_trend=RRsum/N;rr_fade=1/rr_trend
        wr_tr=(NU/res) if bdir=="UP" else (ND/res); wr_fd=1-wr_tr
        rate=res/N
        et=expectancy(wr_tr,rr_trend,rate,True,wr_tr); ef=expectancy(wr_fd,rr_fade,rate,False,wr_tr)
        if et>0: pos.append((lvl,bdir,"TREND",et))
        if ef>0: pos.append((lvl,bdir,"FADE",ef))
md.insert(3, f"\n## RESUMEN: setups con expectancy POSITIVO = {len(pos)}\n" +
         ("".join(f"\n- {l} {b} {t}: exp {e:+.3f}R" for l,b,t,e in pos) if pos else "\n_NINGUNO._") + "\n")

Path("reports/pivot/Pivot_Master_Table.md").write_text("\n".join(md),encoding="utf-8")
print(f"WROTE master table. positive setups: {len(pos)}")
