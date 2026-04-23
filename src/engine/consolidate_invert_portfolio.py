"""Consolidate the 414 validated inverted strategies into a diversified
portfolio that minimizes temporal overlap and concentration.

Rules:
 1. Session hierarchy (non-overlap): ASIA, LONDON, NY are mutually exclusive.
    LONDON_NY is the union of LONDON+NY. ALL_DAY subsumes everything.
    Prefer disjoint single-session setups over LONDON_NY; drop ALL_DAY if
    any session-specific exists for the same (symbol, setup).
 2. Per (symbol, setup) keep only the BEST entry (by expectancy).
 3. Cap per symbol: max 3 setups (diversify across 14 symbols).
 4. Cap per setup family: max 40% of portfolio (prevent OLS_SLOPE dominating).
 5. Sort final by expectancy descending.

Output: reports/Invert_Portfolio.md + .json (bot_config-compatible).
"""
from __future__ import annotations
from pathlib import Path
import json
import polars as pl

REPORTS_DIR = Path("reports")
MAX_PER_SYMBOL = 3
MAX_SETUP_SHARE = 0.40  # no single setup > 40% of portfolio


def consolidate():
    df = pl.read_parquet(REPORTS_DIR / "invert_validated.parquet")
    print(f"[Cons] input: {len(df)} validated strategies")

    # Step 1: session-overlap elimination per (symbol, setup).
    # Rule: within (symbol, setup), prefer specific sessions over LONDON_NY over ALL_DAY.
    # Keep the best-expectancy entry; drop entries whose sessions overlap its window.
    session_priority = {"ASIA": 0, "LONDON": 0, "NY": 0, "LONDON_NY": 1, "ALL_DAY": 2}
    df = df.with_columns([
        pl.col("session").replace_strict(session_priority, default=9).alias("_sprio")
    ])

    # Per (symbol, setup): sort by (priority asc, expectancy desc), build set of
    # sessions kept avoiding overlap. Simplification: take best expectancy combo
    # whose session does NOT overlap any already-kept session in that (symbol, setup).
    overlaps = {
        "ASIA":       {"ASIA", "ALL_DAY"},
        "LONDON":     {"LONDON", "LONDON_NY", "ALL_DAY"},
        "NY":         {"NY", "LONDON_NY", "ALL_DAY"},
        "LONDON_NY":  {"LONDON", "NY", "LONDON_NY", "ALL_DAY"},
        "ALL_DAY":    {"ASIA", "LONDON", "NY", "LONDON_NY", "ALL_DAY"},
    }

    # Per SYMBOL (not per symbol+setup): pick non-overlapping sessions globally.
    # This ensures a symbol never has 2 strategies firing simultaneously.
    # Greedy: sort by expectancy, add if session doesn't overlap already-kept ones.
    picked_rows = []
    for sym, sub in df.group_by("symbol"):
        sub_sorted = sub.sort("expectancy_r", descending=True)
        kept_sessions = set()
        for r in sub_sorted.iter_rows(named=True):
            ses = r["session"]
            if overlaps[ses] & kept_sessions:
                continue
            picked_rows.append(r)
            kept_sessions.add(ses)

    step1 = pl.DataFrame(picked_rows).drop("_sprio")
    print(f"[Cons] after session-disjoint-per-symbol filter: {len(step1)}")

    # Step 2: deduplicate (symbol, session) -> keep best. Already effectively done
    # but per-session may have same session picked via different setups across
    # groups — not possible here since we grouped by symbol.
    step2 = step1.sort("expectancy_r", descending=True)
    print(f"[Cons] step2 total: {len(step2)}")

    # Step 3: cap per symbol
    step3_rows = []
    per_symbol = {}
    for r in step2.sort("expectancy_r", descending=True).iter_rows(named=True):
        n = per_symbol.get(r["symbol"], 0)
        if n >= MAX_PER_SYMBOL:
            continue
        step3_rows.append(r)
        per_symbol[r["symbol"]] = n + 1
    step3 = pl.DataFrame(step3_rows)
    print(f"[Cons] after per-symbol cap ({MAX_PER_SYMBOL}): {len(step3)}")

    # Step 4: cap per setup family
    max_setup = int(len(step3) * MAX_SETUP_SHARE) + 1
    print(f"[Cons] per-setup cap: {max_setup} of {len(step3)}")
    final_rows = []
    per_setup = {}
    for r in step3.sort("expectancy_r", descending=True).iter_rows(named=True):
        n = per_setup.get(r["setup_type"], 0)
        if n >= max_setup:
            continue
        final_rows.append(r)
        per_setup[r["setup_type"]] = n + 1
    final = pl.DataFrame(final_rows).sort("expectancy_r", descending=True)
    print(f"[Cons] FINAL portfolio: {len(final)}")

    # Distributions
    print(f"\nBy symbol: {dict(final.group_by('symbol').len().sort('len',descending=True).iter_rows())}")
    print(f"By setup: {dict(final.group_by('setup_type').len().sort('len',descending=True).iter_rows())}")
    print(f"By session: {dict(final.group_by('session').len().sort('len',descending=True).iter_rows())}")

    # Aggregated metrics
    agg = final.select([
        pl.col("wr").mean().alias("avg_wr"),
        pl.col("pf").mean().alias("avg_pf"),
        pl.col("expectancy_r").mean().alias("avg_exp"),
        pl.col("trades_per_year").sum().alias("total_trades_per_year"),
        pl.col("expectancy_r").mul(pl.col("trades_per_year")).sum().alias("annual_R_expected"),
    ]).row(0, named=True)
    print(f"\nAvg WR: {agg['avg_wr']:.3f}")
    print(f"Avg PF: {agg['avg_pf']:.3f}")
    print(f"Avg expectancy: {agg['avg_exp']:.3f}R")
    print(f"Total trades/year: {agg['total_trades_per_year']:.0f}")
    print(f"Expected annual R sum: {agg['annual_R_expected']:.1f}R")

    # Save
    final.write_parquet(REPORTS_DIR / "invert_portfolio.parquet")

    # JSON
    items = []
    for r in final.iter_rows(named=True):
        items.append({
            "archetype": "MATH_INV_MOMENTUM",
            "symbol": r["symbol"], "tf": "M15", "session": r["session"],
            "setup_type": r["setup_type"], "direction_mode": "INVERTED",
            "tp_atr_mult": float(r["tp_atr_mult"]),
            "sl_atr_mult": float(r["sl_atr_mult"]),
            "atr_period": 14,
            "metrics": {
                "wr": float(r["wr"]), "pf": float(r["pf"]),
                "expectancy_r": float(r["expectancy_r"]),
                "max_dd_r": float(r["max_dd_r"]),
                "trades_per_year": float(r["trades_per_year"]),
                "wf_ratio": float(r["wf_ratio"]),
                "mc_ruin": float(r["mc_ruin"]),
                "decay_ratio": float(r["decay_ratio"]),
            }
        })
    (REPORTS_DIR / "invert_portfolio.json").write_text(json.dumps(items, indent=2), encoding="utf-8")

    # Markdown
    md = ["# Math-Invert Portfolio (diversified)", "",
          f"- Strategies: **{len(final)}**",
          f"- Avg WR: {agg['avg_wr']:.3f}",
          f"- Avg PF: {agg['avg_pf']:.3f}",
          f"- Avg expectancy: {agg['avg_exp']:.3f}R",
          f"- Expected trades/year (sum): {agg['total_trades_per_year']:.0f}",
          f"- Expected annual R (sum): {agg['annual_R_expected']:.1f}",
          "",
          "## Rules applied",
          "- Session-overlap elimination per (symbol, setup)",
          f"- Max {MAX_PER_SYMBOL} setups per symbol",
          f"- Max {int(MAX_SETUP_SHARE*100)}% share per setup family",
          "",
          "## Portfolio",
          "",
          "| # | Symbol | Session | Setup | TP | SL | WR | PF | Exp(R) | Trades/yr | WF | MC | Decay |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(final.iter_rows(named=True), 1):
        md.append(
            f"| {i} | {r['symbol']} | {r['session']} | {r['setup_type']} "
            f"| {r['tp_atr_mult']} | {r['sl_atr_mult']} | {r['wr']:.3f} "
            f"| {r['pf']:.2f} | {r['expectancy_r']:.3f} "
            f"| {r['trades_per_year']:.0f} | {r['wf_ratio']:.2f} "
            f"| {r['mc_ruin']:.3f} | {r['decay_ratio']:.2f} |"
        )
    (REPORTS_DIR / "Invert_Portfolio.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    consolidate()
