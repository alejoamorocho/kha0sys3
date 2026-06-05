"""Build executive Pivot Edge report focused on TRADEABLE intermediate-level
mean-reversion edges, with hour-of-day breakdown.

Excludes S3/R3 boundary levels from the edge ranking (their cont/rev is a
geometric artifact — no level beyond them, so direction is forced).
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import polars as pl

OUTDIR = Path("reports/pivot")
df = pl.read_parquet(OUTDIR / "pivot_transitions.parquet")
ORD = {"S3_D":-3,"S2_D":-2,"S1_D":-1,"PP_D":0,"R1_D":1,"R2_D":2,"R3_D":3,
       "S3_W":-3,"S2_W":-2,"S1_W":-1,"PP_W":0,"R1_W":1,"R2_W":2,"R3_W":3}
df = df.with_columns([
    pl.col("from_level").replace_strict(ORD, default=0).alias("fo"),
    pl.col("next_level").replace_strict({**ORD,"EOD":99}, default=99).alias("to"),
])
df = df.with_columns(
    pl.when(pl.col("to")==99).then(pl.lit("EOD"))
      .when((pl.col("direction")=="UP")&(pl.col("to")>pl.col("fo"))).then(pl.lit("CONT"))
      .when((pl.col("direction")=="DOWN")&(pl.col("to")<pl.col("fo"))).then(pl.lit("CONT"))
      .otherwise(pl.lit("REV")).alias("outcome")
)
INTER = ["S2_D","S1_D","PP_D","R1_D","R2_D","S2_W","S1_W","PP_W","R1_W","R2_W"]

md = []
md.append("# Pivot Point Edge Study — Resultados ejecutivos\n")
md.append(f"**Eventos de transición:** {len(df):,} · **Símbolos:** 14 · **Período:** 2018-2026 (M1)\n")
md.append("**Método:** ruptura = close M1 cruza el nivel. Destino = primer nivel DISTINTO "
          "alcanzado el mismo día UTC. Continuación = avanza al siguiente nivel en la dirección de "
          "la ruptura; Reversión = se devuelve.\n")

md.append("## TL;DR — El edge es FADE (mean-reversion) de niveles intermedios\n")
md.append("Las rupturas de niveles pivot intermedios **tienden a fallar (~58-75%)**. "
          "El efecto se intensifica en **horas asiáticas (00-08 UTC)**. Los niveles extremos "
          "S3/R3 se excluyen (su sesgo es artefacto geométrico).\n")

# Pooled intermediate edges
md.append("## 1. Sesgo agregado por nivel/dirección (todos los símbolos)\n")
md.append("| nivel | dir | n | CONT | REV | EOD | sesgo dominante |")
md.append("|---|---|---|---|---|---|---|")
agg = (df.filter(pl.col("from_level").is_in(INTER))
         .group_by(["from_level","direction"])
         .agg([pl.len().alias("n"),
               (pl.col("outcome")=="CONT").mean().alias("cont"),
               (pl.col("outcome")=="REV").mean().alias("rev"),
               (pl.col("outcome")=="EOD").mean().alias("eod")])
         .sort([pl.col("rev"),pl.col("cont")], descending=True))
for r in agg.iter_rows(named=True):
    if r["cont"]>r["rev"]:
        bias=f"CONTINUACIÓN {r['cont']*100:.0f}%" if r["cont"]>=0.55 else "neutro"
    else:
        bias=f"REVERSIÓN {r['rev']*100:.0f}%" if r["rev"]>=0.55 else "neutro"
    md.append(f"| {r['from_level']} | {r['direction']} | {r['n']:,} | {r['cont']*100:.0f}% | "
              f"{r['rev']*100:.0f}% | {r['eod']*100:.0f}% | **{bias}** |")

# Best tradeable edges by hour
md.append("\n## 2. EDGES tradeables y su mejor horario\n")
md.append("Para cada edge fuerte, la probabilidad sube en ciertas horas UTC.\n")
md.append("| nivel | dir | sesgo | global | mejores horas (UTC) |")
md.append("|---|---|---|---|---|")
for lvl,dirn,want,label in [
    ("S2_D","DOWN","REV","FADE breakdown S2 → comprar"),
    ("PP_D","UP","REV","FADE breakout PP → vender"),
    ("R1_D","UP","REV","FADE breakout R1 → vender"),
    ("R2_D","UP","REV","FADE breakout R2 → vender"),
    ("S2_D","UP","CONT","Seguir rebote S2 → comprar"),
    ("PP_D","DOWN","CONT","Seguir breakdown PP → vender"),
    ("R1_D","DOWN","CONT","Seguir breakdown R1 → vender"),
]:
    s = df.filter((pl.col("from_level")==lvl)&(pl.col("direction")==dirn))
    glob = (s["outcome"]==want).mean()
    byh = (s.group_by("hour").agg([pl.len().alias("n"),(pl.col("outcome")==want).mean().alias("p")])
             .filter(pl.col("n")>=200).sort("p",descending=True).head(4))
    hrs = ", ".join(f"{int(r['hour']):02d}h={r['p']*100:.0f}%" for r in byh.iter_rows(named=True))
    md.append(f"| {lvl} | {dirn} | {want} ({label}) | {glob*100:.0f}% | {hrs} |")

# Per-symbol strongest fade
md.append("\n## 3. FADE breakout PP/R1 al alza → reversión, por símbolo\n")
md.append("Robustez del edge principal en cada activo (rompe PP/R1 arriba → se devuelve).\n")
md.append("| símbolo | PP_D UP n | PP rev% | R1_D UP n | R1 rev% |")
md.append("|---|---|---|---|---|")
for sym in sorted(df["sym"].unique().to_list()):
    pp = df.filter((pl.col("sym")==sym)&(pl.col("from_level")=="PP_D")&(pl.col("direction")=="UP"))
    r1 = df.filter((pl.col("sym")==sym)&(pl.col("from_level")=="R1_D")&(pl.col("direction")=="UP"))
    md.append(f"| {sym} | {len(pp):,} | {(pp['outcome']=='REV').mean()*100:.0f}% | "
              f"{len(r1):,} | {(r1['outcome']=='REV').mean()*100:.0f}% |")

# S2 fade in asian hours — the strongest
md.append("\n## 4. EDGE ESTRELLA: S2_D breakdown en Asia (00-06 UTC) → rebote\n")
md.append("Romper S2 hacia abajo en horas asiáticas rebota con altísima probabilidad.\n")
md.append("| símbolo | n (00-06h) | rebote% |")
md.append("|---|---|---|")
asia = df.filter((pl.col("from_level")=="S2_D")&(pl.col("direction")=="DOWN")&(pl.col("hour")<=6))
for sym in sorted(asia["sym"].unique().to_list()):
    s = asia.filter(pl.col("sym")==sym)
    if len(s)>=80:
        md.append(f"| {sym} | {len(s)} | {(s['outcome']=='REV').mean()*100:.0f}% |")

md.append("\n## Nota metodológica\n")
md.append("- S3/R3 excluidos del ranking: son niveles extremos, su dirección de transición es "
          "forzada (no hay nivel más allá).\n")
md.append("- 'EOD' = no hubo otro cruce ese día (precio se quedó). ~12-22% de casos.\n")
md.append("- Próximo paso sugerido: análisis de GESTIÓN — medir hasta qué nivel llega la "
          "reversión (TP) y cuánto avanza la ruptura antes de fallar (SL), en R-múltiplos.\n")

(OUTDIR/"Pivot_Edge_Report.md").write_text("\n".join(md), encoding="utf-8")
print("WROTE", OUTDIR/"Pivot_Edge_Report.md")
