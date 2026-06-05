"""Report for pivot management v2 (R:R 2:1, fractional TP, fade+trend).

Break-even WR at 2:1 with friction 0.3R:
  win = +2 - 0.3 = 1.7 ; loss = -1 - 0.3 = -1.3 ; timeout = -0.2
  expectancy = wr*1.7 - loss_rate*1.3 - timeout_rate*0.2
We compute exact expectancy from the WIN/LOSS/TIME counts.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import polars as pl

OUTDIR = Path("reports/pivot")
df = pl.read_parquet(OUTDIR/"pivot_mgmt_v2_raw.parquet")
RRWIN = 2.0; FR = 0.3

def stats(sub):
    n=len(sub)
    if n==0: return None
    w=(sub["outcome"]=="WIN").sum()
    l=(sub["outcome"]=="LOSS").sum()
    t=(sub["outcome"]=="TIME").sum()
    wr=w/n
    exp=(w*(RRWIN-FR) + l*(-1-FR) + t*(-0.2))/n
    gw=w*RRWIN; gl=l*1.0 + t*0.2
    pf=gw/gl if gl>0 else 99
    return {"n":n,"wr":wr,"exp":exp,"pf":min(pf,99),
            "w":w,"l":l,"t":t,"sl_atr":sub["sl_atr"].median()}

md=[]
md.append("# Pivot Management v2 — R:R 2:1, TP fraccional, FADE + TREND\n")
md.append(f"**Trades simulados:** {len(df):,} · R:R fijo 2:1 · fricción {FR}R · SL-first · walk M1\n")
md.append("Break-even WR a 2:1 (con fricción) ≈ **40%**. Buscamos setups con WR>42% y exp>0.\n")

# Aggregate per (period, level, bdir, ttype, tpf) — pooled symbols
md.append("## 1. Por setup (todos los símbolos) — ordenado por expectancy\n")
md.append("| period | nivel | ruptura | tipo | TP% | n | WR | exp_R | PF | SL(atr) |")
md.append("|---|---|---|---|---|---|---|---|---|---|")
combos=[]
for (per,lvl,bd,tt,tpf),sub in df.group_by(["period","level","bdir","ttype","tpf"]):
    s=stats(sub)
    if s and s["n"]>=300:
        combos.append((per,lvl,bd,tt,tpf,s))
combos.sort(key=lambda x:-x[5]["exp"])
for per,lvl,bd,tt,tpf,s in combos[:40]:
    flag=" ✅" if s["exp"]>0 else ""
    md.append(f"| {per} | {lvl} | {bd} | {tt} | {int(tpf*100)}% | {s['n']:,} | "
              f"{s['wr']*100:.0f}% | {s['exp']:+.3f}{flag} | {s['pf']:.2f} | {s['sl_atr']:.2f} |")

# Positive-expectancy setups, broken down by hour
md.append("\n## 2. Setups POSITIVOS + su mejor horario\n")
pos=[c for c in combos if c[5]["exp"]>0]
if pos:
    md.append("| setup | global exp | mejor hora UTC | n | WR | exp_R |")
    md.append("|---|---|---|---|---|---|")
    for per,lvl,bd,tt,tpf,s in pos[:20]:
        sub=df.filter((pl.col("period")==per)&(pl.col("level")==lvl)&(pl.col("bdir")==bd)
                      &(pl.col("ttype")==tt)&(pl.col("tpf")==tpf))
        best=None
        for h in range(24):
            hs=stats(sub.filter(pl.col("hour")==h))
            if hs and hs["n"]>=60 and (best is None or hs["exp"]>best[1]["exp"]):
                best=(h,hs)
        if best:
            md.append(f"| {per} {lvl} {bd} {tt} {int(tpf*100)}% | {s['exp']:+.3f} | "
                      f"{best[0]:02d}h | {best[1]['n']} | {best[1]['wr']*100:.0f}% | {best[1]['exp']:+.3f} |")
else:
    md.append("_Ningún setup con expectancy positivo a nivel agregado._\n")

# Best per symbol for any positive setup
md.append("\n## 3. Mejores (símbolo × setup) con exp>0, n>=100\n")
md.append("| símbolo | period | nivel | ruptura | tipo | TP% | n | WR | exp_R |")
md.append("|---|---|---|---|---|---|---|---|---|")
persym=[]
for (sym,per,lvl,bd,tt,tpf),sub in df.group_by(["sym","period","level","bdir","ttype","tpf"]):
    s=stats(sub)
    if s and s["n"]>=100 and s["exp"]>0:
        persym.append((sym,per,lvl,bd,tt,tpf,s))
persym.sort(key=lambda x:-x[6]["exp"])
for sym,per,lvl,bd,tt,tpf,s in persym[:30]:
    md.append(f"| {sym} | {per} | {lvl} | {bd} | {tt} | {int(tpf*100)}% | {s['n']} | "
              f"{s['wr']*100:.0f}% | {s['exp']:+.3f} |")
if not persym:
    md.append("| _ninguno_ | | | | | | | | |")

md.append(f"\n## Resumen\n")
md.append(f"- Setups agregados con exp>0: **{len(pos)}** de {len(combos)} evaluados\n")
md.append(f"- Combos (símbolo×setup) positivos n>=100: **{len(persym)}**\n")
md.append("- Break-even WR a R:R 2:1 (fricción 0.3R) ≈ 40%.\n")

(OUTDIR/"Pivot_Management_v2_Report.md").write_text("\n".join(md),encoding="utf-8")
print("WROTE",OUTDIR/"Pivot_Management_v2_Report.md")
print(f"positive aggregate setups: {len(pos)} | positive sym-combos: {len(persym)}")
