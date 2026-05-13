"""Classify live-tradeable strategies into WINNERS / NEUTRALS / LOSERS.

Matches K3M1-75 config entries against the broker deal stream (with truncated
session tag prefix matching), then assigns each strategy to a bucket based on
WR (with n>=2 trades minimum).

Output: reports/Live_Strategy_Classification.md
"""
from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import polars as pl

REPORTS = Path("reports")
TRADES = REPORTS / "live_strategy_trades.parquet"
CFG = Path("src/execution/bot_config_math.json")

SETUP_TAG = {
    "KAMA_CROSS_MOM": "KAMA",
    "SPECTRAL_TREND_MOM": "SPECTRAL",
    "VELOCITY_ACCEL_GO": "VELOCITY",
    "KALMAN_INNOV_EXPAND": "KALMAN",
    "HURST_TREND_MOM": "HURST",
    "OLS_SLOPE_STRONG": "OLS",
}
SESSION_TAG = {
    "ASIA": "ASIA", "LONDON": "LDN", "NY": "NY",
    "LONDON_NY": "LDNNY", "ALL_DAY": "ALLDAY",
}


def main():
    trades = pl.read_parquet(TRADES)
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    portfolio = cfg["portfolio"]

    # Build prefix-match lookup: (symbol, tf, setup_tag) → list of strategies
    # We'll match the truncated session_tag by prefix
    by_prefix = defaultdict(list)
    for p in portfolio:
        st = SETUP_TAG.get(p["setup_type"])
        ss = SESSION_TAG.get(p["session"])
        if not st or not ss:
            continue
        key = (p["sym"], p["tf"], st)
        by_prefix[key].append({**p, "_setup_tag": st, "_session_tag": ss})

    # Attribute each trade to a config entry (or "legacy" if no match)
    def attribute(t):
        sym, tf, stag, sstag = t["symbol"], t["tf"], t["setup_tag"], t["session_tag"]
        candidates = by_prefix.get((sym, tf, stag), [])
        # Match by session_tag prefix (deal comment may be truncated)
        for c in candidates:
            if c["_session_tag"].startswith(sstag) or sstag.startswith(c["_session_tag"]):
                return c
        return None

    rows = []
    for t in trades.iter_rows(named=True):
        cfg_entry = attribute(t)
        rows.append({
            **t,
            "matched_id": (cfg_entry or {}).get("id", "LEGACY"),
            "matched_session": (cfg_entry or {}).get("session", "-"),
            "matched_setup": (cfg_entry or {}).get("setup_type", "-"),
            "robustness": (cfg_entry or {}).get("robustness_label", "?"),
            "expected_wr": (cfg_entry or {}).get("expected_wr", None),
            "expected_pf_oos": (cfg_entry or {}).get("expected_pf_oos", None),
            "in_config": cfg_entry is not None,
        })
    matched = pl.DataFrame(rows)

    # Aggregate per strategy_id (only current config entries)
    in_cfg = matched.filter(pl.col("in_config"))
    if len(in_cfg) == 0:
        print("No matched trades to current config")
        return

    agg = in_cfg.group_by([
        "matched_id", "symbol", "tf", "matched_setup", "matched_session", "robustness",
        "expected_wr", "expected_pf_oos",
    ]).agg([
        pl.len().alias("n_trades"),
        (pl.col("net_usd") > 0).cast(pl.Int64).sum().alias("wins"),
        pl.col("net_usd").sum().alias("net_usd"),
        pl.col("net_usd").filter(pl.col("net_usd") > 0).sum().alias("gross_profit"),
        pl.col("net_usd").filter(pl.col("net_usd") < 0).sum().abs().alias("gross_loss"),
        pl.col("net_usd").mean().alias("avg_net_usd"),
    ]).with_columns([
        (pl.col("wins").cast(pl.Float64) / pl.col("n_trades")).alias("wr_live"),
        (pl.col("gross_profit") / pl.col("gross_loss")).alias("pf_live"),
    ]).sort("n_trades", descending=True)

    # Add bucket label
    def bucket(row):
        n = row["n_trades"]
        wr = row["wr_live"]
        net = row["net_usd"]
        if n < 2:
            return "TOO_FEW"
        if wr >= 0.60 and net > 0:
            return "WINNER"
        if 0.40 <= wr <= 0.60:
            return "NEUTRAL"
        if wr < 0.40 or net < 0:
            return "LOSER"
        return "OBSERVE"

    agg = agg.with_columns(
        pl.struct(["n_trades", "wr_live", "net_usd"])
          .map_elements(bucket, return_dtype=pl.Utf8)
          .alias("bucket")
    )

    # Per-bucket aggregate
    print("=" * 80)
    print("LIVE STRATEGY CLASSIFICATION — K3M1-75 only (matched to current config)")
    print("=" * 80)
    print(f"Total K3M1-75 strategies with trades: {len(agg)}")
    print(f"  — of 75 configured ({75 - len(agg)} have NOT fired yet)")
    print()
    from collections import Counter
    bc = Counter(r["bucket"] for r in agg.iter_rows(named=True))
    for b in ["WINNER", "NEUTRAL", "LOSER", "TOO_FEW"]:
        print(f"  {b}: {bc.get(b, 0)}")
    print()

    # WINNERS
    win = agg.filter(pl.col("bucket") == "WINNER").sort("net_usd", descending=True)
    print(f"\n=== WINNERS ({len(win)}) — KEEP ===")
    with pl.Config(tbl_rows=20, tbl_cols=12, tbl_width_chars=200):
        print(win.select(["matched_id", "tf", "matched_setup", "matched_session",
                          "n_trades", "wins", "wr_live", "pf_live",
                          "net_usd", "expected_wr", "expected_pf_oos"]))

    # NEUTRALS
    neu = agg.filter(pl.col("bucket") == "NEUTRAL").sort("net_usd", descending=True)
    print(f"\n=== NEUTRALS ({len(neu)}) — OBSERVE ===")
    with pl.Config(tbl_rows=20, tbl_cols=12, tbl_width_chars=200):
        print(neu.select(["matched_id", "tf", "matched_setup", "matched_session",
                          "n_trades", "wins", "wr_live", "pf_live",
                          "net_usd", "expected_wr", "expected_pf_oos"]))

    # LOSERS
    los = agg.filter(pl.col("bucket") == "LOSER").sort("net_usd")
    print(f"\n=== LOSERS ({len(los)}) — DISABLE ===")
    with pl.Config(tbl_rows=30, tbl_cols=12, tbl_width_chars=200):
        print(los.select(["matched_id", "tf", "matched_setup", "matched_session",
                          "n_trades", "wins", "wr_live",
                          "net_usd", "expected_wr", "expected_pf_oos"]))

    # TOO_FEW (single trade — not enough data)
    tf_rows = agg.filter(pl.col("bucket") == "TOO_FEW").sort("net_usd")
    print(f"\n=== TOO_FEW ({len(tf_rows)}) — keep ON for more data ===")
    with pl.Config(tbl_rows=30, tbl_cols=10, tbl_width_chars=160):
        print(tf_rows.select(["matched_id", "tf", "matched_setup", "matched_session",
                              "n_trades", "wr_live", "net_usd"]))

    # By TF
    print("\n=== BY TF (matched K3M1-75 only) ===")
    by_tf = agg.group_by("tf").agg([
        pl.len().alias("n_strats"),
        pl.col("n_trades").sum().alias("n_trades"),
        pl.col("wins").sum().alias("wins"),
        pl.col("net_usd").sum().alias("net_usd"),
    ]).with_columns(
        (pl.col("wins") / pl.col("n_trades")).alias("wr")
    ).sort("n_trades", descending=True)
    print(by_tf)

    # Write parquet + markdown
    agg.write_parquet(REPORTS / "live_strategy_classification.parquet")

    md = ["# Live Strategy Classification — K3M1-75 (5 days, May 9-13 2026)",
          "",
          f"Account demo $100,000 → $68,253 (-31.7% in 5 days)",
          f"Total trades: 94 (66 K3-97 era + 28 K3M1-75 era)",
          f"Bot stopped May 13 to prevent further bleed.",
          "",
          "## Classification rules",
          "- **WINNER** : n ≥ 2 trades AND wr_live ≥ 60% AND net > 0",
          "- **NEUTRAL**: n ≥ 2 AND 40% ≤ wr_live ≤ 60%",
          "- **LOSER**  : n ≥ 2 AND (wr_live < 40% OR net < 0)",
          "- **TOO_FEW**: n = 1 (cannot conclude — keep ON)",
          "",
          "## Summary",
          ""]
    for b in ["WINNER", "NEUTRAL", "LOSER", "TOO_FEW"]:
        md.append(f"- **{b}**: {bc.get(b, 0)}")
    md += [f"- **Cold (never fired)**: {75 - len(agg)}/75",
           "",
           "## WINNERS — KEEP ON",
           "",
           "| ID | TF | Setup | Sess | n | WR | PF live | Net USD | WR expected | PF OOS exp |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for r in win.iter_rows(named=True):
        ev_pf = r["expected_pf_oos"] or 0
        md.append(f"| {r['matched_id']} | {r['tf']} | {r['matched_setup']} | "
                  f"{r['matched_session']} | {r['n_trades']} | "
                  f"{(r['wr_live'] or 0)*100:.0f}% | "
                  f"{r['pf_live']:.2f} | ${r['net_usd']:+.0f} | "
                  f"{(r['expected_wr'] or 0)*100:.0f}% | {ev_pf:.2f} |")

    md += ["", "## NEUTRALS — OBSERVE",
           "",
           "| ID | TF | Setup | Sess | n | WR | PF live | Net USD | WR expected | PF OOS exp |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for r in neu.iter_rows(named=True):
        ev_pf = r["expected_pf_oos"] or 0
        md.append(f"| {r['matched_id']} | {r['tf']} | {r['matched_setup']} | "
                  f"{r['matched_session']} | {r['n_trades']} | "
                  f"{(r['wr_live'] or 0)*100:.0f}% | "
                  f"{(r['pf_live'] or 0):.2f} | ${r['net_usd']:+.0f} | "
                  f"{(r['expected_wr'] or 0)*100:.0f}% | {ev_pf:.2f} |")

    md += ["", "## LOSERS — DISABLE",
           "",
           "| ID | TF | Setup | Sess | n | WR | Net USD | WR expected | PF OOS exp |",
           "|---|---|---|---|---|---|---|---|---|"]
    for r in los.iter_rows(named=True):
        ev_pf = r["expected_pf_oos"] or 0
        md.append(f"| {r['matched_id']} | {r['tf']} | {r['matched_setup']} | "
                  f"{r['matched_session']} | {r['n_trades']} | "
                  f"{(r['wr_live'] or 0)*100:.0f}% | ${r['net_usd']:+.0f} | "
                  f"{(r['expected_wr'] or 0)*100:.0f}% | {ev_pf:.2f} |")

    md += ["", "## TOO_FEW (1 trade — keep ON for more data)",
           "",
           "| ID | TF | Setup | Sess | n | WR | Net USD |",
           "|---|---|---|---|---|---|---|"]
    for r in tf_rows.iter_rows(named=True):
        md.append(f"| {r['matched_id']} | {r['tf']} | {r['matched_setup']} | "
                  f"{r['matched_session']} | {r['n_trades']} | "
                  f"{(r['wr_live'] or 0)*100:.0f}% | ${r['net_usd']:+.0f} |")

    md += ["", "## By TF",
           "",
           "| TF | strats | trades | wins | WR | Net USD |",
           "|---|---|---|---|---|---|"]
    for r in by_tf.iter_rows(named=True):
        md.append(f"| **{r['tf']}** | {r['n_strats']} | {r['n_trades']} | "
                  f"{r['wins']} | {(r['wr'] or 0)*100:.0f}% | ${r['net_usd']:+.0f} |")

    md += ["", "## Strategies that have NOT fired yet (cold)",
           "", f"{75 - len(agg)} strategies remain untested. Don't disable — "
           "let them run when bot resumes to gather data."]

    (REPORTS / "Live_Strategy_Classification.md").write_text("\n".join(md), encoding="utf-8")
    print(f"\nReport: reports/Live_Strategy_Classification.md")
    print(f"Parquet: reports/live_strategy_classification.parquet")


if __name__ == "__main__":
    main()
