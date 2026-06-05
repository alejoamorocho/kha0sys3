"""Exhaustive pivot edge catalog — EVERY combination, IS/OOS validated.

Sweeps: symbol × level(S1,PP,R1,R2) × break_dir(UP,DOWN) × trade(TREND,FADE)
        × time-granularity:
          - 4 session windows (Asia/London/NY/Late) — large samples, robust
          - 24 exact hours — small samples, overfit-prone (flagged)

For each: in-sample exp (2018-2022) and out-of-sample exp (2023-2026).
A combo is "robust" if exp>0.05 in BOTH IS and OOS with min samples.
Each row flagged by sample reliability so the user can judge.

Outputs:
  reports/pivot/Pivot_Full_Catalog.md
  reports/pivot/pivot_full_catalog.parquet
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import polars as pl, numpy as np

df = pl.read_parquet("reports/pivot/pivot_byhour.parquet").filter(pl.col("level")!="S2")
FR=0.1
df=df.with_columns(pl.when(pl.col("year")<=2022).then(pl.lit("IS")).otherwise(pl.lit("OOS")).alias("split"))
WINDOWS={"Asia":set(range(0,7)),"London":set(range(7,13)),"NY":set(range(13,20)),"Late":set(range(20,24))}

def exp_of(sub, trade):
    n=len(sub)
    if n==0: return None
    u=int((sub["res"]=="U").sum()); d=int((sub["res"]=="D").sum()); res=u+d
    if res==0: return None
    bd_up=sub["bdir"]=="UP"
    trend_win=((sub["res"]=="U")&bd_up)|((sub["res"]=="D")&~bd_up)
    wr_tr=int(trend_win.sum())/res; rr_tr=float(sub["rr_tr"].mean()); rr_fd=1/rr_tr if rr_tr>0 else 0
    rate=res/n
    wr,rr=(wr_tr,rr_tr) if trade=="TREND" else (1-wr_tr,rr_fd)
    pw=rate*wr; ploss=rate*(1-wr)
    return {"n":n,"wr":wr,"rr":rr,"exp":pw*rr-ploss-(pw+ploss)*FR}

SYMS=sorted(df["sym"].unique().to_list())
rows=[]
# add window col
def win_of(h):
    for w,r in WINDOWS.items():
        if h in r: return w
    return "?"
df=df.with_columns(pl.col("hour").map_elements(win_of,return_dtype=pl.Utf8).alias("win"))

for sym in SYMS:
    s=df.filter(pl.col("sym")==sym)
    for lvl in ["S1","PP","R1","R2"]:
        for bd in ["UP","DOWN"]:
            base=s.filter((pl.col("level")==lvl)&(pl.col("bdir")==bd))
            for tr in ["TREND","FADE"]:
                # session windows
                for w in WINDOWS:
                    cell=base.filter(pl.col("win")==w)
                    is_=exp_of(cell.filter(pl.col("split")=="IS"),tr)
                    oos=exp_of(cell.filter(pl.col("split")=="OOS"),tr)
                    if not is_ or not oos: continue
                    rows.append({"sym":sym,"level":lvl,"bdir":bd,"trade":tr,"gran":"WINDOW","slot":w,
                        "is_n":is_["n"],"is_exp":round(is_["exp"],3),"is_wr":round(is_["wr"],3),
                        "oos_n":oos["n"],"oos_exp":round(oos["exp"],3),"oos_wr":round(oos["wr"],3),
                        "rr":round(is_["rr"],2)})
                # exact hours
                for h in range(24):
                    cell=base.filter(pl.col("hour")==h)
                    is_=exp_of(cell.filter(pl.col("split")=="IS"),tr)
                    oos=exp_of(cell.filter(pl.col("split")=="OOS"),tr)
                    if not is_ or not oos: continue
                    rows.append({"sym":sym,"level":lvl,"bdir":bd,"trade":tr,"gran":"HOUR","slot":f"{h:02d}h",
                        "is_n":is_["n"],"is_exp":round(is_["exp"],3),"is_wr":round(is_["wr"],3),
                        "oos_n":oos["n"],"oos_exp":round(oos["exp"],3),"oos_wr":round(oos["wr"],3),
                        "rr":round(is_["rr"],2)})

cat=pl.DataFrame(rows)
cat=cat.with_columns([
    pl.min_horizontal("is_exp","oos_exp").alias("min_exp"),
    pl.min_horizontal("is_n","oos_n").alias("min_n"),
])
# robust = both positive
robust=cat.filter((pl.col("is_exp")>0.05)&(pl.col("oos_exp")>0.05))
# reliability flag
robust=robust.with_columns(
    pl.when((pl.col("gran")=="WINDOW")&(pl.col("min_n")>=150)).then(pl.lit("ALTA"))
      .when(pl.col("min_n")>=120).then(pl.lit("MEDIA"))
      .otherwise(pl.lit("BAJA(overfit?)")).alias("conf")
).sort("min_exp",descending=True)

cat.write_parquet("reports/pivot/pivot_full_catalog.parquet")

md=["# Catálogo COMPLETO de edges pivot — todas las combinaciones IS/OOS validadas\n",
    f"Combinaciones evaluadas: {len(cat):,} · Robustas (IS+OOS exp>0.05): {len(robust):,}\n",
    "Granularidad: WINDOW (sesión, muestra grande) + HOUR (hora exacta, muestra chica).\n",
    "Confianza: ALTA=window n>=150 · MEDIA=n>=120 · BAJA=muestra chica (probable overfit).\n"]

for conf in ["ALTA","MEDIA","BAJA(overfit?)"]:
    sub=robust.filter(pl.col("conf")==conf)
    md.append(f"\n## Confianza {conf}: {len(sub)} combos\n")
    md.append("| activo | nivel | dir | tipo | gran | slot | IS n/exp/wr | OOS n/exp/wr | R:R |")
    md.append("|---|---|---|---|---|---|---|---|---|")
    for r in sub.iter_rows(named=True):
        md.append(f"| {r['sym']} | {r['level']} | {r['bdir']} | {r['trade']} | {r['gran']} | {r['slot']} | "
                  f"{r['is_n']}/{r['is_exp']:+.3f}/{r['is_wr']*100:.0f}% | "
                  f"{r['oos_n']}/{r['oos_exp']:+.3f}/{r['oos_wr']*100:.0f}% | {r['rr']:.2f} |")

# stats: trend vs fade, session distribution among ALTA
alta=robust.filter(pl.col("conf")=="ALTA")
md.append("\n## Estadística de los robustos de ALTA confianza\n")
if len(alta)>0:
    from collections import Counter
    md.append(f"- TREND vs FADE: {dict(Counter(alta['trade'].to_list()))}")
    md.append(f"- Por sesión: {dict(Counter(alta['slot'].to_list()))}")
    md.append(f"- Por nivel: {dict(Counter(alta['level'].to_list()))}")
    md.append(f"- Activos con ≥1 robusto ALTA: {alta['sym'].n_unique()}/14")

Path("reports/pivot/Pivot_Full_Catalog.md").write_text("\n".join(md),encoding="utf-8")
print(f"evaluated={len(cat)} robust={len(robust)}")
print(f"  ALTA={len(robust.filter(pl.col('conf')=='ALTA'))} MEDIA={len(robust.filter(pl.col('conf')=='MEDIA'))} BAJA={len(robust.filter(pl.col('conf')=='BAJA(overfit?)'))}")
print("WROTE Pivot_Full_Catalog.md + parquet")
