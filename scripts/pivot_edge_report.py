"""Build the Pivot Edge markdown report from pivot_transitions.parquet.

Analyses:
  - Per (symbol, from_level, direction): distribution of next_level.
    Highlights the strongest transition (highest probability destination)
    and classifies continuation vs reversal.
  - Per hour-of-day: how transition probabilities shift by session.
  - Edge ranking: (sym, hour, level, dir) combos where the top destination
    probability is high AND sample is large -> tradeable bias.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import polars as pl
from collections import defaultdict

OUTDIR = Path("reports/pivot")
df = pl.read_parquet(OUTDIR / "pivot_transitions.parquet")

# Level ordinal for continuation/reversal classification
ORD = {"S3_D":-3,"S2_D":-2,"S1_D":-1,"PP_D":0,"R1_D":1,"R2_D":2,"R3_D":3,
       "S3_W":-3,"S2_W":-2,"S1_W":-1,"PP_W":0,"R1_W":1,"R2_W":2,"R3_W":3}

MIN_N = 50   # minimum sample for a transition to be reported
MIN_P = 0.40 # minimum top-destination probability to flag as edge

md = []
md.append("# Pivot Point Edge Study — Daily + Weekly classic levels")
md.append(f"\n**Total crossing events:** {len(df):,}  ")
md.append(f"**Symbols:** {df['sym'].n_unique()}  ")
md.append(f"**Method:** M1 close crossings, next-level transition same UTC day\n")

# ---- 1. Per-symbol per-level transition (aggregated over hours) ----
md.append("## 1. Transición por (símbolo, nivel, dirección) — destino más probable\n")
md.append("| símbolo | nivel | dir | n | destino top | P(top) | continuación | reversión | EOD |")
md.append("|---|---|---|---|---|---|---|---|---|")

g = (df.group_by(["sym","from_level","direction","next_level"])
       .agg(pl.len().alias("n")))
totals = (df.group_by(["sym","from_level","direction"])
            .agg(pl.len().alias("total")))
gj = g.join(totals, on=["sym","from_level","direction"])
gj = gj.with_columns((pl.col("n")/pl.col("total")).alias("p"))

rows_for_edge = []
for (sym, lvl, dirn), sub in (gj.filter(pl.col("total")>=MIN_N)
                               .sort(["sym","from_level","direction","p"], descending=[False,False,False,True])
                               .group_by(["sym","from_level","direction"], maintain_order=True)):
    sub = sub.sort("p", descending=True)
    top = sub.row(0, named=True)
    total = top["total"]
    # continuation = destination further in break direction; reversal = opposite
    from_ord = ORD.get(lvl, 0)
    cont_p = rev_p = eod_p = 0.0
    for r in sub.iter_rows(named=True):
        nl = r["next_level"]
        if nl == "EOD":
            eod_p += r["p"]; continue
        to_ord = ORD.get(nl, 0)
        if dirn == "UP":
            if to_ord > from_ord: cont_p += r["p"]
            elif to_ord < from_ord: rev_p += r["p"]
        else:
            if to_ord < from_ord: cont_p += r["p"]
            elif to_ord > from_ord: rev_p += r["p"]
    md.append(f"| {sym} | {lvl} | {dirn} | {total} | {top['next_level']} | "
              f"{top['p']*100:.0f}% | {cont_p*100:.0f}% | {rev_p*100:.0f}% | {eod_p*100:.0f}% |")
    rows_for_edge.append({"sym":sym,"level":lvl,"dir":dirn,"n":total,
                          "top_dest":top["next_level"],"top_p":top["p"],
                          "cont_p":cont_p,"rev_p":rev_p,"eod_p":eod_p})

# ---- 2. Edge ranking: strong directional bias ----
md.append("\n## 2. EDGES — sesgo direccional fuerte (cont. o rev. ≥60%, n≥100)\n")
md.append("| símbolo | nivel | dir | n | continuación | reversión | sesgo |")
md.append("|---|---|---|---|---|---|---|")
edges = []
for r in rows_for_edge:
    if r["n"] < 100: continue
    if r["cont_p"] >= 0.60:
        edges.append((r, "CONTINUACIÓN", r["cont_p"]))
    elif r["rev_p"] >= 0.60:
        edges.append((r, "REVERSIÓN", r["rev_p"]))
edges.sort(key=lambda x: -x[2])
for r, bias, p in edges:
    md.append(f"| {r['sym']} | {r['level']} | {r['dir']} | {r['n']} | "
              f"{r['cont_p']*100:.0f}% | {r['rev_p']*100:.0f}% | **{bias} {p*100:.0f}%** |")
if not edges:
    md.append("| _ninguno supera el umbral 60%_ | | | | | | |")

# ---- 3. By hour: continuation rate per level (aggregated symbols) ----
md.append("\n## 3. Tasa de CONTINUACIÓN por hora UTC (todos los símbolos)\n")
md.append("Para cada hora, % de rupturas que continúan al siguiente nivel vs se devuelven.\n")
# compute continuation flag per event
df2 = df.with_columns([
    pl.col("from_level").replace_strict(ORD, default=0).alias("from_ord"),
    pl.col("next_level").replace_strict({**ORD,"EOD":99}, default=99).alias("to_ord"),
])
df2 = df2.with_columns(
    pl.when(pl.col("to_ord")==99).then(pl.lit("EOD"))
      .when((pl.col("direction")=="UP") & (pl.col("to_ord")>pl.col("from_ord"))).then(pl.lit("CONT"))
      .when((pl.col("direction")=="DOWN") & (pl.col("to_ord")<pl.col("from_ord"))).then(pl.lit("CONT"))
      .otherwise(pl.lit("REV")).alias("outcome")
)
byhour = (df2.group_by("hour")
            .agg([pl.len().alias("n"),
                  (pl.col("outcome")=="CONT").sum().alias("cont"),
                  (pl.col("outcome")=="REV").sum().alias("rev"),
                  (pl.col("outcome")=="EOD").sum().alias("eod")])
            .sort("hour"))
md.append("| hora UTC | n | continuación | reversión | EOD |")
md.append("|---|---|---|---|---|")
for r in byhour.iter_rows(named=True):
    n=r["n"]
    md.append(f"| {r['hour']:02d}:00 | {n} | {r['cont']/n*100:.0f}% | {r['rev']/n*100:.0f}% | {r['eod']/n*100:.0f}% |")

# ---- 4. Daily vs Weekly level strength ----
md.append("\n## 4. Daily vs Weekly — qué niveles tienen más sesgo\n")
df3 = df2.with_columns(pl.col("from_level").str.slice(-1).alias("period"))
byper = (df3.group_by(["period","from_level"])
           .agg([pl.len().alias("n"),
                 (pl.col("outcome")=="CONT").sum().alias("cont"),
                 (pl.col("outcome")=="REV").sum().alias("rev")])
           .sort(["period","from_level"]))
md.append("| nivel | n | continuación | reversión |")
md.append("|---|---|---|---|")
for r in byper.iter_rows(named=True):
    n=r["n"]
    md.append(f"| {r['from_level']} | {n} | {r['cont']/n*100:.0f}% | {r['rev']/n*100:.0f}% |")

(OUTDIR / "Pivot_Edge_Report.md").write_text("\n".join(md), encoding="utf-8")
print(f"WROTE {OUTDIR/'Pivot_Edge_Report.md'}")
print(f"edges found (>=60% bias, n>=100): {len(edges)}")
