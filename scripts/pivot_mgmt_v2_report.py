"""Report for pivot management v2 with REAL per-symbol friction.

Friction in R per trade = round_turn_spread_price / sl_dist_price.
round_turn_spread_price = 2 * spread_pt * tick_size (cross spread on
entry+exit) — conservative. With tiny TP (5-10%), sl_dist is small so
friction_R can be large; this is the whole point of measuring it.

R:R 2:1 fixed. Win=+2-fric, Loss=-1-fric, Timeout=-0.2-fric.
Break-even gross WR at 2:1 = 33%. We report gross WR AND net expectancy.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import polars as pl

OUTDIR = Path("reports/pivot")
df = pl.read_parquet(OUTDIR/"pivot_mgmt_v2_raw.parquet")
RRWIN = 2.0

# round-turn spread in price per symbol (2 * spread_pt * tick_size)
SNAP = {
 "EURUSD":(1,0.00001),"GBPUSD":(5,0.00001),"USDJPY":(4,0.001),"AUDUSD":(2,0.00001),
 "GBPJPY":(4,0.001),"EURJPY":(4,0.001),"GBPAUD":(6,0.00001),"XAUUSD":(12,0.01),
 "XAGUSD":(44,0.001),"WTI":(47,0.001),"BRENT":(47,0.001),"NATGAS":(200,0.001),
 "NASDAQ100":(100,0.1),"SP500":(50,0.1),
}
def spread_price(sym):
    sp,ts = SNAP.get(sym,(10,0.0001))
    return 2*sp*ts  # round turn

# Add friction_R column
df = df.with_columns(
    pl.struct(["sym","sl_dist_price"]).map_elements(
        lambda r: (spread_price(r["sym"])/r["sl_dist_price"]) if r["sl_dist_price"]>0 else 9.9,
        return_dtype=pl.Float64).alias("fric_R")
)

def stats(sub):
    n=len(sub)
    if n==0: return None
    o=sub["outcome"].to_numpy(); fr=sub["fric_R"].to_numpy()
    w=(o=="WIN"); l=(o=="LOSS"); t=(o=="TIME")
    # net per trade
    import numpy as np
    net = np.where(w, RRWIN, np.where(l, -1.0, -0.2)) - fr
    return {"n":n,"wr":w.mean(),"exp":net.mean(),
            "fric":fr.mean(),"sl_atr":sub["sl_atr"].median(),
            "gross_pf": (w.sum()*RRWIN)/(l.sum()*1.0+t.sum()*0.2) if (l.sum()+t.sum())>0 else 99}

md=[]
md.append("# Pivot Management v2 — TP pequeños + fricción REAL por símbolo\n")
md.append(f"**Trades:** {len(df):,} · R:R 2:1 · fricción = spread round-turn real / SL_dist · SL-first\n")
md.append("Con TP pequeños (5-10%) el SL es minúsculo → la fricción real (spread) "
          "puede superar el riesgo. Por eso se mide exacta, no fija.\n")

md.append("## 1. Por TP% — WR bruto vs fricción (todos los setups/símbolos)\n")
md.append("| TP% | n | WR bruto | fric_R medio | SL(atr) | exp_R neto |")
md.append("|---|---|---|---|---|---|")
for tpf in [0.05,0.10,0.15,0.20,0.25,0.50]:
    s=stats(df.filter(pl.col("tpf")==tpf))
    flag=" ✅" if s["exp"]>0 else ""
    md.append(f"| {int(tpf*100)}% | {s['n']:,} | {s['wr']*100:.0f}% | {s['fric']:.2f}R | "
              f"{s['sl_atr']:.2f} | {s['exp']:+.3f}{flag} |")

md.append("\n## 2. Mejores setups por expectancy NETO (n>=300)\n")
md.append("| period | nivel | rup | tipo | TP% | n | WR bruto | fric_R | exp_R neto | PF bruto |")
md.append("|---|---|---|---|---|---|---|---|---|---|")
combos=[]
for (per,lvl,bd,tt,tpf),sub in df.group_by(["period","level","bdir","ttype","tpf"]):
    s=stats(sub)
    if s and s["n"]>=300: combos.append((per,lvl,bd,tt,tpf,s))
combos.sort(key=lambda x:-x[5]["exp"])
for per,lvl,bd,tt,tpf,s in combos[:30]:
    flag=" ✅" if s["exp"]>0 else ""
    md.append(f"| {per} | {lvl} | {bd} | {tt} | {int(tpf*100)}% | {s['n']:,} | "
              f"{s['wr']*100:.0f}% | {s['fric']:.2f} | {s['exp']:+.3f}{flag} | {s['gross_pf']:.2f} |")

# Gross WR ranking (ignore friction) to see if ANY directional bias exists
md.append("\n## 3. Ranking por WR BRUTO (ignora fricción) — ¿hay sesgo?\n")
md.append("Break-even bruto a 2:1 = 33%. Si WR bruto >> 33% hay sesgo direccional real.\n")
md.append("| period | nivel | rup | tipo | TP% | n | WR bruto |")
md.append("|---|---|---|---|---|---|---|")
combos.sort(key=lambda x:-x[5]["wr"])
for per,lvl,bd,tt,tpf,s in combos[:20]:
    mark="🟢" if s["wr"]>0.42 else ("🟡" if s["wr"]>0.36 else "🔴")
    md.append(f"| {mark} {per} | {lvl} | {bd} | {tt} | {int(tpf*100)}% | {s['n']:,} | {s['wr']*100:.0f}% |")

# Positive net setups + best hour
pos=[c for c in combos if c[5]["exp"]>0]
md.append(f"\n## 4. Setups con expectancy NETO positivo: {len(pos)}\n")
if pos:
    md.append("| setup | n | WR | fric_R | exp_R | mejor hora |")
    md.append("|---|---|---|---|---|---|")
    for per,lvl,bd,tt,tpf,s in sorted(pos,key=lambda x:-x[5]["exp"])[:20]:
        sub=df.filter((pl.col("period")==per)&(pl.col("level")==lvl)&(pl.col("bdir")==bd)
                      &(pl.col("ttype")==tt)&(pl.col("tpf")==tpf))
        best=None
        for h in range(24):
            hs=stats(sub.filter(pl.col("hour")==h))
            if hs and hs["n"]>=60 and (best is None or hs["exp"]>best[1]["exp"]): best=(h,hs)
        bh=f"{best[0]:02d}h ({best[1]['wr']*100:.0f}%WR)" if best else "-"
        md.append(f"| {per} {lvl} {bd} {tt} {int(tpf*100)}% | {s['n']:,} | {s['wr']*100:.0f}% | "
                  f"{s['fric']:.2f} | {s['exp']:+.3f} | {bh} |")
else:
    md.append("_Ninguno._ El WR bruto no supera lo suficiente el 33% para pagar la fricción.\n")

(OUTDIR/"Pivot_Management_v2_Report.md").write_text("\n".join(md),encoding="utf-8")
print("WROTE report. positive net setups:", len(pos))
# also print gross WR summary
print("\nGross WR by TP%:")
for tpf in [0.05,0.10,0.15,0.20,0.25,0.50]:
    s=stats(df.filter(pl.col("tpf")==tpf))
    print(f"  TP {int(tpf*100)}%: WR={s['wr']*100:.1f}%  fric={s['fric']:.2f}R  net_exp={s['exp']:+.3f}")
