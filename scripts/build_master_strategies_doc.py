"""Generate Master_Strategies.md — comprehensive multi-TF FUERTE portfolio doc.

Includes:
  - Full per-strategy tables for M15/H1/H4 (FUERTE only)
  - Per-TF aggregates: WR, PF IS/OOS, DD, ruin, tpy, net R
  - Combined portfolio aggregates
  - Risk allocation projection on $10k with aggressive risk-per-trade
  - Growth projection to $1M

Risk model: each FUERTE strategy gets per-trade risk based on its WR using
the existing risk_scaling tier 1 (balance <= $2k = 1-15%; for $10k applies
tier 2 = 1-8%). For "test/aggressive" mode we override with tier 1 (1-15%)
to find the upper bound of growth speed.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import math
import polars as pl

REPORTS = Path("reports")

# Load 3 TF robustness parquets and harmonize
m15 = pl.read_parquet(REPORTS / "robustness_math_optuna.parquet").with_columns([
    pl.lit("M15").alias("tf"), pl.col("mc_ruin_pct").alias("mc_ruin"),
])
h1 = pl.read_parquet(REPORTS / "math_h1_robustness.parquet").with_columns(
    pl.lit("H1").alias("tf"))
h4 = pl.read_parquet(REPORTS / "math_h4_robustness.parquet").with_columns(
    pl.lit("H4").alias("tf"))

COLS = ['tf','symbol','session','setup_type','direction_mode','regime',
        'tp','sl','rr','n','wr','pf','wf_pf_te','exp_r','net_r','max_dd','tpy',
        'mc_ruin','label']
m15 = m15.select(COLS); h1 = h1.select(COLS); h4 = h4.select(COLS)
allp = pl.concat([m15, h1, h4])

# FUERTE only (most strict robustness)
fuerte = allp.filter(pl.col("label") == "FUERTE")

# Risk model: aggressive tier (1-15%) keyed on WR
# linear interpolation between WR=0.55 -> 1% and WR=0.80 -> 15%
def aggressive_risk_pct(wr: float) -> float:
    if wr <= 0.55:
        return 0.01
    if wr >= 0.80:
        return 0.15
    return 0.01 + (wr - 0.55) / (0.80 - 0.55) * (0.15 - 0.01)


def fmt_table_md(df: pl.DataFrame, cols: list[str], headers: list[str]) -> str:
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in df.iter_rows(named=True):
        line = []
        for c in cols:
            v = r[c]
            if isinstance(v, float):
                if c in ("wr", "mc_ruin"):
                    line.append(f"{v*100:.1f}%" if c == "wr" else f"{v:.2f}%")
                elif c in ("pf", "wf_pf_te", "rr"):
                    line.append(f"{v:.2f}")
                elif c in ("exp_r",):
                    line.append(f"{v:+.3f}")
                elif c in ("max_dd", "tpy", "net_r"):
                    line.append(f"{v:.1f}")
                elif c in ("tp", "sl"):
                    line.append(f"{v:.2f}")
                else:
                    line.append(f"{v:.2f}")
            elif isinstance(v, int):
                line.append(f"{v:,}")
            else:
                line.append(str(v) if v is not None else "-")
        out.append("| " + " | ".join(line) + " |")
    return "\n".join(out)


def aggregate(df: pl.DataFrame) -> dict:
    if len(df) == 0:
        return {}
    return {
        "n": len(df),
        "avg_wr": float(df["wr"].mean()),
        "min_wr": float(df["wr"].min()),
        "max_wr": float(df["wr"].max()),
        "avg_pf": float(df["pf"].mean()),
        "avg_pf_oos": float(df["wf_pf_te"].mean()),
        "avg_exp": float(df["exp_r"].mean()),
        "avg_dd": float(df["max_dd"].mean()),
        "avg_tpy": float(df["tpy"].mean()),
        "sum_tpy": float(df["tpy"].sum()),
        "avg_ruin": float(df["mc_ruin"].mean()),
        "max_dd_overall": float(df["max_dd"].max()),
        "sum_n": int(df["n"].sum()),
        "sum_net_r": float(df["net_r"].sum()),
    }


def growth_projection(avg_exp_R: float, sum_tpy: float, avg_risk_pct: float,
                      start: float, target: float, realism_factor: float = 1.0):
    """Linear annual return with realism factor.

    Linear annual = sum_tpy × avg_exp_R × avg_risk_pct  (theoretical)
    Realistic = linear × realism_factor (accounts for slippage, correlation,
    DD compounding, broker liquidity at higher volumes).

    Returns (annual_return, years_to_target).
    """
    linear_annual = sum_tpy * avg_exp_R * avg_risk_pct * realism_factor
    if linear_annual <= 0:
        return linear_annual, float("inf")
    years = math.log(target / start) / math.log(1.0 + linear_annual)
    return linear_annual, years


def main():
    by_tf = {tf: fuerte.filter(pl.col("tf") == tf).sort("wr", descending=True)
             for tf in ["M15", "H1", "H4"]}

    # Per-TF aggregates
    aggs = {tf: aggregate(df) for tf, df in by_tf.items()}
    aggs["TOTAL"] = aggregate(fuerte)

    # Risk allocations per strategy
    fuerte_with_risk = fuerte.with_columns(
        pl.col("wr").map_elements(aggressive_risk_pct, return_dtype=pl.Float64).alias("risk_pct")
    ).with_columns(
        # On a $10k balance, USD risk per trade
        (pl.col("risk_pct") * 10000).alias("usd_risk_per_trade"),
        # Expected R per trade × risk_pct = portfolio % growth per trade (Kelly-style)
        (pl.col("exp_r") * pl.col("risk_pct")).alias("pct_growth_per_trade"),
    )

    # Growth projection per TF — 4 risk levels × 3 realism factors
    RISK_LEVELS = [
        ("Conservador 1%",   0.01),
        ("Moderado 3%",      0.03),
        ("Agresivo 5%",      0.05),
        ("WR-tier (1-15%)",  None),  # uses per-strategy WR scaling
    ]
    REALISM = [
        ("Teórico (perfect)",    1.00),
        ("Realista 50%",         0.50),
        ("Conservador 30%",      0.30),
    ]
    projections = {}
    for tf in ["M15", "H1", "H4", "TOTAL"]:
        sub = fuerte_with_risk if tf == "TOTAL" else fuerte_with_risk.filter(
            pl.col("tf") == tf)
        if len(sub) == 0:
            continue
        avg_exp = float(sub["exp_r"].mean())
        sum_tpy = float(sub["tpy"].sum())
        avg_risk_tier = float(sub["risk_pct"].mean())
        scen_results = []
        for risk_name, fixed_risk in RISK_LEVELS:
            risk = fixed_risk if fixed_risk is not None else avg_risk_tier
            for real_name, factor in REALISM:
                ann, yrs = growth_projection(avg_exp, sum_tpy, risk, 10_000, 1_000_000, factor)
                scen_results.append({
                    "risk_name": risk_name, "risk": risk,
                    "real_name": real_name, "factor": factor,
                    "annual": ann, "years": yrs
                })
        projections[tf] = {
            "n": len(sub),
            "sum_tpy": sum_tpy,
            "avg_exp": avg_exp,
            "avg_risk_tier": avg_risk_tier,
            "scenarios": scen_results,
        }

    # Build markdown
    lines = []
    lines += ["# Portfolio Master — Math Multi-TF FUERTE",
              "",
              f"Generated: {datetime.utcnow().isoformat()}Z  ·  Backtest period: 2018-01-01 → 2026-03-24 (8.22y)",
              "",
              "## Filtros aplicados",
              "",
              "- Robustness class = **FUERTE** (la más estricta: WF deg < 5%, ruin < 1%, PF OOS > IS×0.95)",
              "- Friction realista Vantage por símbolo + 0.2R slippage",
              "- Walk-forward 50/50 IS vs OOS",
              "- Monte Carlo 10k bootstrap, gate DD ≥ 30R",
              "- Optuna 3-regime TP/SL per estrategia (HIGH_RR / BALANCED / HIGH_WR)",
              "",
              "## Resumen ejecutivo",
              "", ]

    # Aggregate table
    head = ["TF", "n", "Avg WR", "Avg PF IS", "Avg PF OOS", "Avg Exp R", "Avg DD R",
            "Avg ruin", "Sum trades/yr", "Sum n trades", "Avg trades/yr/strat",
            "Sum Net R (8.2y)"]
    lines += ["| " + " | ".join(head) + " |",
              "|" + "|".join(["---"] * len(head)) + "|"]
    for tf in ["M15", "H1", "H4", "TOTAL"]:
        a = aggs.get(tf, {})
        if not a: continue
        lines.append(
            f"| **{tf}** | {a['n']} | {a['avg_wr']*100:.1f}% | {a['avg_pf']:.2f} | "
            f"{a['avg_pf_oos']:.2f} | {a['avg_exp']:+.3f} | {a['avg_dd']:.1f} | "
            f"{a['avg_ruin']:.2f}% | {a['sum_tpy']:.0f} | {a['sum_n']:,} | "
            f"{a['avg_tpy']:.1f} | {a['sum_net_r']:.0f} |"
        )

    # Growth projection table
    lines += ["", "## Proyección de crecimiento $10k → $1M",
              "",
              "**Modelo lineal con factor de realismo**:",
              "",
              "- **Linear annual return** = `sum_trades_per_year × avg_exp_R × risk_pct × realism_factor`",
              "- Realism factor 1.0 = teórico (sin slippage extra, sin correlación entre strats)",
              "- Realism factor 0.5 = realista (escalado por correlación + slippage al subir lots)",
              "- Realism factor 0.3 = conservador (asume live-vs-backtest gap del 70%)",
              "",
              "Para cada TF se muestran 4 niveles de riesgo × 3 factores de realismo = 12 combinaciones.",
              ""]
    for tf, p in projections.items():
        lines += [f"### {tf} — {p['n']} estrategias FUERTE | {p['sum_tpy']:.0f} trades/año | "
                  f"avg exp R={p['avg_exp']:+.3f}",
                  "",
                  "| Riesgo/trade | Realismo | Annual return | Years a $1M | $10k → 1y |",
                  "|---|---|---|---|---|"]
        for sc in p["scenarios"]:
            yrs = f"{sc['years']:.2f}" if math.isfinite(sc['years']) else "∞"
            end_1y = 10_000 * (1 + sc['annual'])
            ann_str = f"{sc['annual']*100:,.0f}%" if sc['annual'] < 100 else f"{sc['annual']*100:,.2e}%"
            end_str = f"${end_1y:,.0f}" if end_1y < 1e9 else f"${end_1y:.2e}"
            lines.append(
                f"| {sc['risk_name']} ({sc['risk']*100:.1f}%) | {sc['real_name']} ({sc['factor']:.1f}) | "
                f"{ann_str} | {yrs} | {end_str} |"
            )
        lines.append("")

    lines += ["", "**ADVERTENCIAS sobre proyecciones**",
              "",
              "1. **Trades NO son perfectamente independientes**: cuando varias estrategias "
              "operan el mismo símbolo, los DD se correlacionan. El cap del 30% simultáneo "
              "ya descuenta esto pero es heurístico.",
              "2. **Expectancy degrada con el balance**: la fricción USD aumenta proporcionalmente "
              "con el lote, lo que reduce los R efectivos. A volumen alto, también puedes salir "
              "del rango de mejor ejecución del broker.",
              "3. **Black swans no están modelados**: gaps, flash crashes, suspensiones de mercado "
              "pueden crear DD muy superiores al MC ruin del backtest.",
              "4. **Margin requirements escalan**: con $1M+ balance, el broker puede requerir "
              "lots más grandes que tu liquidez disponible, forzándote a fraccionar.",
              "5. **Realista vs teórico**: aplica un factor 0.3-0.5 a las proyecciones de arriba "
              "para una estimación menos optimista. P. ej. si el modelo dice 5 años, planea para 10-15.",
              "",
              "## Distribución por símbolo (todas las TF, FUERTE)",
              "", ]
    by_sym = fuerte.group_by("symbol").agg([
        pl.len().alias("n"),
        pl.col("tpy").sum().alias("sum_tpy"),
        pl.col("wr").mean().alias("avg_wr"),
        pl.col("pf").mean().alias("avg_pf"),
        pl.col("net_r").sum().alias("sum_net_r"),
    ]).sort("sum_net_r", descending=True)
    lines += ["| Symbol | Strats | trades/yr | Avg WR | Avg PF | Sum Net R |",
              "|---|---|---|---|---|---|"]
    for r in by_sym.iter_rows(named=True):
        lines.append(f"| {r['symbol']} | {r['n']} | {r['sum_tpy']:.0f} | "
                     f"{r['avg_wr']*100:.1f}% | {r['avg_pf']:.2f} | {r['sum_net_r']:.0f} |")

    # Per-TF detailed table
    cols = ['symbol','session','setup_type','direction_mode','regime',
            'tp','sl','rr','n','wr','pf','wf_pf_te','exp_r','max_dd','tpy','mc_ruin']
    headers = ['Symbol','Sess','Setup','Dir','Regime','TP','SL','RR','n','WR','PF IS',
               'PF OOS','Exp R','DD R','tpy','Ruin%']

    for tf in ["M15", "H1", "H4"]:
        df = by_tf[tf]
        lines += ["", f"## {tf} — {len(df)} estrategias FUERTE", ""]
        if len(df) == 0:
            lines.append("_Sin estrategias FUERTE en este TF_")
            continue
        # Add per-strategy risk columns
        df_x = df.with_columns(
            pl.col("wr").map_elements(aggressive_risk_pct, return_dtype=pl.Float64).alias("risk_pct"),
        ).with_columns(
            (pl.col("risk_pct") * 10000).alias("usd_risk_10k"),
        )
        # show with risk columns appended
        cols2 = cols + ["risk_pct", "usd_risk_10k"]
        headers2 = headers + ["Risk %", "USD risk @$10k"]
        out_lines = ["| " + " | ".join(headers2) + " |",
                     "|" + "|".join(["---"] * len(headers2)) + "|"]
        for r in df_x.iter_rows(named=True):
            line = []
            for c in cols2:
                v = r[c]
                if c == "wr":
                    line.append(f"{v*100:.1f}%")
                elif c == "mc_ruin":
                    line.append(f"{v:.2f}%")
                elif c == "risk_pct":
                    line.append(f"{v*100:.1f}%")
                elif c == "usd_risk_10k":
                    line.append(f"${v:.0f}")
                elif c in ("pf", "wf_pf_te", "rr", "tp", "sl"):
                    line.append(f"{v:.2f}")
                elif c == "exp_r":
                    line.append(f"{v:+.3f}")
                elif c in ("max_dd", "tpy"):
                    line.append(f"{v:.1f}")
                elif isinstance(v, int):
                    line.append(f"{v:,}")
                else:
                    line.append(str(v) if v is not None else "-")
            out_lines.append("| " + " | ".join(line) + " |")
        lines += out_lines

    # Sum risk projection on $10k
    lines += ["", "## Riesgo total simultáneo (worst-case overlap @ $10k)",
              "",
              "Si TODAS las estrategias FUERTE dispararan trades simultáneamente "
              "y cada una perdiera 1R, el drawdown agregado sería:",
              ""]
    for tf in ["M15", "H1", "H4", "TOTAL"]:
        sub = fuerte_with_risk if tf == "TOTAL" else fuerte_with_risk.filter(pl.col("tf") == tf)
        if len(sub) == 0: continue
        sum_risk_usd = float(sub["usd_risk_per_trade"].sum())
        sum_risk_pct = sum_risk_usd / 10000 * 100
        lines.append(f"- **{tf}**: {len(sub)} strats — riesgo simultáneo total = "
                     f"${sum_risk_usd:.0f} ({sum_risk_pct:.1f}% del balance $10k)")

    lines += ["",
              "En la práctica, los trades NO disparan todos al mismo tiempo (deduplicación por día, "
              "session windows distintas, TFs separados). El riesgo simultáneo realista es ~10-20% "
              "del worst-case por overlap natural.",
              "",
              "## Recomendación de deploy",
              "",
              "1. **Bot LIVE actual** ya tiene 34 estrategias elite WR≥65% activas.",
              f"2. Si quieres todas las {aggs['TOTAL']['n']} FUERTE, hay que ampliar el filtro de "
              "`bot_config_math.json` (reemplazar el current 34 con el dataset FUERTE completo).",
              "3. **Risk model**: el actual usa BalanceTieredRiskAllocator con tier 1 (≤$2k = 1-15%). "
              "Si tu balance es $10k, automáticamente cae en tier 2 (1-8%). Para modo agresivo "
              "(test rápido a $1M) hay que sobrescribir con tier 1 explícitamente.",
              "4. **Crítico**: monitorear primer mes en VIVO. Las proyecciones asumen que la "
              "fricción real-time iguala la del backtest. Si los R efectivos son menores, ajustar "
              "el risk_pct a la baja.",
              ""]

    out_path = REPORTS / "Master_Strategies_Portfolio.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out_path} ({len(lines)} lines)")
    # Also save the FUERTE dataframe
    fuerte_with_risk.write_parquet(REPORTS / "fuerte_master_portfolio.parquet")
    print(f"Wrote {REPORTS}/fuerte_master_portfolio.parquet ({len(fuerte)} rows)")

    # Echo aggregate summary
    print()
    print("=== AGGREGATE BY TF ===")
    for tf in ["M15", "H1", "H4", "TOTAL"]:
        a = aggs.get(tf, {})
        if not a: continue
        print(f"{tf:6s}: n={a['n']:3d}  WR={a['avg_wr']*100:.1f}%  PF={a['avg_pf']:.2f}  "
              f"PFoos={a['avg_pf_oos']:.2f}  DD={a['avg_dd']:.1f}R  tpy={a['sum_tpy']:.0f}  "
              f"netR={a['sum_net_r']:.0f}")
    print()
    print("=== GROWTH PROJECTION (10k -> 1M, key scenarios) ===")
    for tf in ["TOTAL"]:
        p = projections.get(tf)
        if not p: continue
        print(f"{tf} (n={p['n']} strats, {p['sum_tpy']:.0f} trades/yr, exp R={p['avg_exp']:+.3f}):")
        for sc in p["scenarios"][:9]:  # Show subset
            y = f"{sc['years']:5.2f}y" if math.isfinite(sc['years']) else "  INF"
            ann = sc['annual']*100
            ann_str = f"{ann:>10,.0f}%" if ann < 1e6 else f"{ann:>10.2e}%"
            print(f"  risk={sc['risk']*100:5.1f}% real={sc['factor']:.1f}: ann={ann_str} -> {y}")


if __name__ == "__main__":
    main()
