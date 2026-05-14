"""Analyze raw ORB Phase A triggers as hit-rate per favorable threshold.

Different framing than the gate-based aggregation in run_phase_a:
  - Edge = P(MFE_favorable >= threshold_R) per (pattern_id, direction)
  - Sweeps multiple thresholds (0.3R, 0.5R, 0.75R, 1.0R)
  - Shows hit-rate distributions and top context combinations

Run AFTER `python scripts/run_orb_pipeline.py --skip-phase D` finishes Phase A.
Reads: reports/orb/orb_phase_a_triggers.parquet
Writes: reports/orb/ORB_Edge_Analysis.md

Usage:
    py -3.12 scripts/analyze_orb_phase_a.py [--min-count 30]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import polars as pl

from src.application.orb_utils import REPORTS_DIR

THRESHOLDS_R = [0.3, 0.5, 0.75, 1.0]


def _load_triggers() -> pl.DataFrame:
    p = Path(REPORTS_DIR) / "orb_phase_a_triggers.parquet"
    if not p.exists():
        raise FileNotFoundError(f"Run Phase A first: {p}")
    df = pl.read_parquet(p)
    if df.is_empty():
        raise RuntimeError("triggers parquet is empty — Phase A produced no triggers")
    return df


def _add_hit_columns(triggers: pl.DataFrame) -> pl.DataFrame:
    """Add hit columns: R-based thresholds + OR-range-based thresholds."""
    exprs = []
    for t in THRESHOLDS_R:
        tag = str(t).replace(".", "")
        # R-based hit (price moved >= t R favorably)
        exprs.append(
            pl.when(pl.col("direction") == "LONG")
              .then(pl.col("mfe_long_r") >= t)
              .otherwise(pl.col("mfe_short_r") >= t)
              .alias(f"hit_{tag}r")
        )
        exprs.append(
            pl.when(pl.col("direction") == "LONG")
              .then(pl.col("mae_long_r") >= t)
              .otherwise(pl.col("mae_short_r") >= t)
              .alias(f"adverse_{tag}r")
        )
    # OR-range-based hits — present only if or_width column exists (new triggers)
    if "or_width" in triggers.columns:
        for frac in [0.5, 1.0, 1.5]:
            tag = str(frac).replace(".", "")
            thr = pl.col("or_width") * frac
            exprs.append(
                pl.when(pl.col("direction") == "LONG")
                  .then(pl.col("mfe_long") >= thr)
                  .otherwise(pl.col("mfe_short") >= thr)
                  .alias(f"hit_{tag}or")
            )
            exprs.append(
                pl.when(pl.col("direction") == "LONG")
                  .then(pl.col("mae_long") >= thr)
                  .otherwise(pl.col("mae_short") >= thr)
                  .alias(f"adverse_{tag}or")
            )
    return triggers.with_columns(exprs)


def _build_aggs(triggers: pl.DataFrame) -> list:
    aggs = [pl.len().alias("count")]
    for t in THRESHOLDS_R:
        tag = str(t).replace(".", "")
        aggs.append(pl.col(f"hit_{tag}r").mean().alias(f"hit_rate_{tag}r"))
        aggs.append(pl.col(f"adverse_{tag}r").mean().alias(f"adverse_rate_{tag}r"))
    if "hit_05or" in triggers.columns:
        for frac in [0.5, 1.0, 1.5]:
            tag = str(frac).replace(".", "")
            aggs.append(pl.col(f"hit_{tag}or").mean().alias(f"hit_rate_{tag}or"))
            aggs.append(pl.col(f"adverse_{tag}or").mean().alias(f"adverse_rate_{tag}or"))
    return aggs


def hit_rates_by_pattern(triggers: pl.DataFrame, min_count: int) -> pl.DataFrame:
    """Per (symbol, magic_time, or_duration_min, pattern_id, direction): hit rates."""
    base = ["symbol", "magic_time", "or_duration_min", "pattern_id",
            "event_type", "or_position", "or_atr_bucket", "pd_or_bucket", "direction"]
    sort_col = "hit_rate_05or" if "hit_05or" in triggers.columns else "hit_rate_05r"
    return (
        triggers.group_by(base)
        .agg(_build_aggs(triggers))
        .filter(pl.col("count") >= min_count)
        .sort(sort_col, descending=True)
    )


def hit_rates_by_context_combo(triggers: pl.DataFrame, min_count: int) -> pl.DataFrame:
    """Hit rates aggregated across all symbols, by context combo only."""
    base = ["event_type", "or_position", "or_atr_bucket", "pd_or_bucket", "direction"]
    sort_col = "hit_rate_05or" if "hit_05or" in triggers.columns else "hit_rate_05r"
    return (
        triggers.group_by(base)
        .agg(_build_aggs(triggers))
        .filter(pl.col("count") >= min_count)
        .sort(sort_col, descending=True)
    )


def edge_summary(triggers: pl.DataFrame) -> dict:
    """Headline distribution of MFE/MAE in R across all triggers (sanity check)."""
    rows = []
    for dir_ in ["LONG", "SHORT"]:
        sub = triggers.filter(pl.col("direction") == dir_)
        mfe_col = f"mfe_{dir_.lower()}_r"
        mae_col = f"mae_{dir_.lower()}_r"
        rows.append({
            "direction": dir_,
            "n_triggers": len(sub),
            "p50_mfe_r": float(sub[mfe_col].quantile(0.5) or 0),
            "p75_mfe_r": float(sub[mfe_col].quantile(0.75) or 0),
            "p90_mfe_r": float(sub[mfe_col].quantile(0.9) or 0),
            "p50_mae_r": float(sub[mae_col].quantile(0.5) or 0),
            "p75_mae_r": float(sub[mae_col].quantile(0.75) or 0),
            "p90_mae_r": float(sub[mae_col].quantile(0.9) or 0),
            "edge_p50": float((sub[mfe_col].quantile(0.5) or 0) - (sub[mae_col].quantile(0.5) or 0)),
        })
    return rows


def fmt_pct(x: float) -> str:
    if x is None:
        return "n/a"
    return f"{x*100:.1f}%"


def fmt_r(x: float) -> str:
    if x is None:
        return "n/a"
    return f"{x:.2f}R"


def write_report(
    triggers: pl.DataFrame,
    by_pattern: pl.DataFrame,
    by_combo: pl.DataFrame,
    summary: list,
    out_path: Path,
    min_count: int,
) -> None:
    lines: list[str] = []
    lines.append("# ORB Phase A — Hit-Rate Edge Analysis\n\n")
    lines.append(f"**Min count filter:** ≥{min_count} triggers per group\n\n")
    lines.append(f"**Total raw triggers:** {len(triggers):,}\n\n")
    lines.append(f"**Thresholds swept (R):** {THRESHOLDS_R}\n\n")

    lines.append("## 1. Sanity check — overall MFE/MAE distribution\n\n")
    lines.append("If MFE_p50 ≈ MAE_p50 → market is symmetric (no edge). "
                 "If MFE_p50 >> MAE_p50 → real asymmetric edge.\n\n")
    lines.append("| direction | n | p50 MFE | p75 MFE | p90 MFE | p50 MAE | p75 MAE | p90 MAE | edge p50 |\n")
    lines.append("|---|---|---|---|---|---|---|---|---|\n")
    for row in summary:
        lines.append(
            f"| {row['direction']} | {row['n_triggers']:,} | "
            f"{fmt_r(row['p50_mfe_r'])} | {fmt_r(row['p75_mfe_r'])} | {fmt_r(row['p90_mfe_r'])} | "
            f"{fmt_r(row['p50_mae_r'])} | {fmt_r(row['p75_mae_r'])} | {fmt_r(row['p90_mae_r'])} | "
            f"{fmt_r(row['edge_p50'])} |\n"
        )

    has_or_cols = "hit_rate_05or" in by_combo.columns
    sort_label = "P(MFE ≥ 0.5 × OR range)" if has_or_cols else "P(hit 0.5R)"
    lines.append(f"\n## 2. Top 30 context combos by {sort_label} — aggregated across all symbols\n\n")
    lines.append("Each row = `(event × or_position × or_atr_bucket × pd_or_bucket × direction)`. "
                 "Useful to see which contextual conditions matter most.\n\n")
    if has_or_cols:
        cols = ["event_type", "or_position", "or_atr_bucket", "pd_or_bucket", "direction",
                "count", "hit_rate_05or", "hit_rate_10or", "hit_rate_15or",
                "adverse_rate_05or", "adverse_rate_10or"]
    else:
        cols = ["event_type", "or_position", "or_atr_bucket", "pd_or_bucket", "direction",
                "count", "hit_rate_03r", "hit_rate_05r", "hit_rate_075r", "hit_rate_10r",
                "adverse_rate_05r"]
    lines.append("| " + " | ".join(cols) + " |\n")
    lines.append("| " + " | ".join("---" for _ in cols) + " |\n")
    for row in by_combo.head(30).iter_rows(named=True):
        cells = []
        for c in cols:
            v = row[c]
            if isinstance(v, float):
                if c.startswith("hit_rate") or c.startswith("adverse_rate"):
                    cells.append(fmt_pct(v))
                else:
                    cells.append(f"{v:.2f}")
            elif v is None:
                cells.append("NULL")
            else:
                cells.append(str(v))
        lines.append("| " + " | ".join(cells) + " |\n")

    lines.append(f"\n## 3. Top 50 individual patterns (symbol-specific) by {sort_label}\n\n")
    if has_or_cols:
        cols2 = ["symbol", "magic_time", "or_duration_min", "event_type",
                 "or_atr_bucket", "pd_or_bucket", "direction",
                 "count", "hit_rate_05or", "hit_rate_10or", "adverse_rate_05or"]
    else:
        cols2 = ["symbol", "magic_time", "or_duration_min", "event_type",
                 "or_atr_bucket", "pd_or_bucket", "direction",
                 "count", "hit_rate_05r", "hit_rate_10r", "adverse_rate_05r"]
    lines.append("| " + " | ".join(cols2) + " |\n")
    lines.append("| " + " | ".join("---" for _ in cols2) + " |\n")
    for row in by_pattern.head(50).iter_rows(named=True):
        cells = []
        for c in cols2:
            v = row[c]
            if isinstance(v, float):
                if c.startswith("hit_rate") or c.startswith("adverse_rate"):
                    cells.append(fmt_pct(v))
                else:
                    cells.append(f"{v:.2f}")
            elif v is None:
                cells.append("NULL")
            else:
                cells.append(str(v))
        lines.append("| " + " | ".join(cells) + " |\n")

    lines.append("\n## 4. Interpretación\n\n")
    lines.append("**Columnas en R** (1R = 0.5 × ATR del setup):\n")
    lines.append("- `hit_rate_05r` = P(MFE favorable ≥ 0.5R en 4h)\n")
    lines.append("- `adverse_rate_05r` = P(MAE adverso ≥ 0.5R en 4h)\n\n")
    lines.append("**Columnas en OR** (fracción del rango del Opening Range):\n")
    lines.append("- `hit_rate_05or` = P(MFE favorable ≥ 0.5 × OR_width en 4h) ← tu framing\n")
    lines.append("- `hit_rate_10or` = P(MFE favorable ≥ 1.0 × OR_width)\n")
    lines.append("- `adverse_rate_05or` = P(MAE adverso ≥ 0.5 × OR_width)\n\n")
    lines.append("**Cómo leer edge:**\n")
    lines.append("- **Hay edge si**: hit_rate >> adverse_rate (ej. hit 70% vs adverse 50%)\n")
    lines.append("- **Random walk si**: hit ≈ adverse (ambos ~60-70% por volatilidad natural)\n")
    lines.append("- **1:1 RR factible si**: hit_rate_05or > 50% Y hit_rate_10or > 33%\n")
    lines.append("- **Buen pattern para deploy**: hit_rate_05or > 65%, count ≥ 100, adverse_rate_10or < 50%\n\n")

    out_path.write_text("".join(lines), encoding="utf-8")
    print(f"[Analysis] wrote {out_path}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--min-count", type=int, default=30,
                   help="Min triggers per group (default 30)")
    args = p.parse_args()

    print(f"[Analysis] loading triggers parquet ...")
    triggers = _load_triggers()
    print(f"[Analysis] {len(triggers):,} raw triggers loaded")

    print(f"[Analysis] computing hit columns at thresholds {THRESHOLDS_R} ...")
    triggers = _add_hit_columns(triggers)

    print(f"[Analysis] aggregating per pattern (min count={args.min_count}) ...")
    by_pattern = hit_rates_by_pattern(triggers, args.min_count)
    print(f"[Analysis] {len(by_pattern)} patterns above count threshold")

    print(f"[Analysis] aggregating per context combo ...")
    by_combo = hit_rates_by_context_combo(triggers, args.min_count)
    print(f"[Analysis] {len(by_combo)} context combos above count threshold")

    print(f"[Analysis] computing overall summary ...")
    summary = edge_summary(triggers)
    for row in summary:
        print(f"  {row['direction']}: n={row['n_triggers']:,} "
              f"p50_mfe={row['p50_mfe_r']:.2f}R p50_mae={row['p50_mae_r']:.2f}R "
              f"edge={row['edge_p50']:.2f}R")

    base = Path(REPORTS_DIR)
    # also persist the aggregates as parquets for further drilldown
    by_pattern.write_parquet(base / "orb_hit_rates_by_pattern.parquet")
    by_combo.write_parquet(base / "orb_hit_rates_by_combo.parquet")

    write_report(triggers, by_pattern, by_combo, summary,
                 base / "ORB_Edge_Analysis.md", args.min_count)


if __name__ == "__main__":
    main()
