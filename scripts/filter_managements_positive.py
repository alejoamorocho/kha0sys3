"""Filter ORB management comparison to only configs with positive edge.

Reads:  reports/orb/orb_managements_compare.parquet
Writes: reports/orb/ORB_Managements_Positive.md

Filter: PF >= 1.0 AND win_rate >= 0.5 AND expectancy_r > 0 AND trades >= 30
"""
from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import polars as pl

from src.application.orb_utils import REPORTS_DIR


def _fmt(v, kind=""):
    if v is None:
        return "—"
    if isinstance(v, float):
        if kind == "pct":
            return f"{v*100:.1f}%"
        if kind == "r":
            return f"{v:+.2f}R"
        return f"{v:.2f}"
    return str(v)


def main():
    base = Path(REPORTS_DIR)
    src = base / "orb_managements_compare.parquet"
    df = pl.read_parquet(src)
    print(f"Total rows: {len(df)}")

    filtered = df.filter(
        (pl.col("pf") >= 1.0)
        & (pl.col("win_rate") >= 0.5)
        & (pl.col("expectancy_r") > 0.0)
        & (pl.col("trades") >= 30)
    ).sort(["pf", "expectancy_r"], descending=[True, True])
    print(f"Configs passing filter (PF>=1.0 & WR>=50% & exp_r>0 & trades>=30): {len(filtered)}")

    out_md = base / "ORB_Managements_Positive.md"
    lines = []
    lines.append("# ORB Managements — Configs con Edge Positivo\n\n")
    lines.append(f"**Filtro:** PF ≥ 1.0 AND WR ≥ 50% AND expectancy_r > 0 AND trades ≥ 30\n\n")
    lines.append(f"**Total configs que pasan:** {len(filtered)} de {len(df)} ({100*len(filtered)/len(df):.1f}%)\n\n")

    # 1. Resumen por modo
    lines.append("## 1. Distribución por modo (solo configs ganadoras)\n\n")
    if not filtered.is_empty():
        by_mode = (
            filtered.group_by("mode").agg([
                pl.len().alias("n_winners"),
                pl.col("pf").median().alias("pf_median"),
                pl.col("pf").max().alias("pf_max"),
                pl.col("win_rate").median().alias("wr_median"),
                pl.col("expectancy_r").median().alias("exp_median"),
                pl.col("sum_r").sum().alias("sum_r_total"),
            ])
            .sort("n_winners", descending=True)
        )
        lines.append("| modo | n configs ganadoras | PF mediano | PF max | WR mediano | exp_r mediano | sum_R total |\n")
        lines.append("|---|---|---|---|---|---|---|\n")
        for row in by_mode.iter_rows(named=True):
            lines.append(f"| {row['mode']} | {row['n_winners']} | "
                         f"{_fmt(row['pf_median'])} | {_fmt(row['pf_max'])} | "
                         f"{_fmt(row['wr_median'], 'pct')} | {_fmt(row['exp_median'], 'r')} | "
                         f"{_fmt(row['sum_r_total'], 'r')} |\n")

    # 2. Por símbolo
    lines.append("\n## 2. Distribución por símbolo (solo configs ganadoras)\n\n")
    if not filtered.is_empty():
        by_sym = (
            filtered.group_by("symbol").agg([
                pl.len().alias("n_winners"),
                pl.col("pf").median().alias("pf_median"),
                pl.col("pf").max().alias("pf_max"),
                pl.col("win_rate").median().alias("wr_median"),
                pl.col("expectancy_r").median().alias("exp_median"),
                pl.col("sum_r").sum().alias("sum_r_total"),
            ])
            .sort("sum_r_total", descending=True)
        )
        lines.append("| símbolo | n configs ganadoras | PF mediano | PF max | WR mediano | exp_r mediano | sum_R total |\n")
        lines.append("|---|---|---|---|---|---|---|\n")
        for row in by_sym.iter_rows(named=True):
            lines.append(f"| {row['symbol']} | {row['n_winners']} | "
                         f"{_fmt(row['pf_median'])} | {_fmt(row['pf_max'])} | "
                         f"{_fmt(row['wr_median'], 'pct')} | {_fmt(row['exp_median'], 'r')} | "
                         f"{_fmt(row['sum_r_total'], 'r')} |\n")

    # 3. Lista completa de configs ganadoras
    lines.append("\n## 3. TODAS las configs ganadoras (ordenadas por PF desc)\n\n")
    cols = ["symbol", "or_duration_min", "pattern_id", "direction",
            "mode", "params", "trades", "trades_per_year",
            "win_rate", "pf", "expectancy_r", "sum_r", "max_dd_r"]
    avail = [c for c in cols if c in filtered.columns]
    lines.append("| " + " | ".join(avail) + " |\n")
    lines.append("| " + " | ".join("---" for _ in avail) + " |\n")
    for row in filtered.iter_rows(named=True):
        cells = []
        for c in avail:
            v = row[c]
            if c == "win_rate":
                cells.append(_fmt(v, "pct"))
            elif c in ("expectancy_r", "sum_r", "max_dd_r"):
                cells.append(_fmt(v, "r"))
            elif c == "pattern_id":
                # shorten pattern_id for readability
                cells.append(str(v)[:60])
            else:
                cells.append(_fmt(v))
        lines.append("| " + " | ".join(cells) + " |\n")

    lines.append("\n## 4. Lectura\n\n")
    lines.append("- **n_winners** = configs (de las 29 totales por patrón) que pasaron el filtro\n")
    lines.append("- **sum_R total** = suma acumulada de R-units a través de TODAS las configs ganadoras del modo/símbolo\n")
    lines.append("- Si un modo tiene muchos winners pero PF mediano bajo, es **consistente**\n")
    lines.append("- Si un modo tiene pocos winners pero PF max alto, tiene **outliers buenos** pero poca robustez\n")

    out_md.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {out_md}")

    # Also persist the filtered parquet for further drilldown
    out_parquet = base / "orb_managements_positive.parquet"
    filtered.write_parquet(out_parquet)
    print(f"Wrote {out_parquet}")


if __name__ == "__main__":
    main()
