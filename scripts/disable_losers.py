"""Remove confirmed losers + ALL OLS_SLOPE_STRONG from bot_config_math.json.

Rationale:
  - 6 strategies with n>=2 trades, 0% WR → confirmed losers
  - All 4 OLS_SLOPE_STRONG strategies tested showed 0% WR (P=0.0018 under H0=65%)
    The pattern is consistent across (sym, tf, sess) so we remove ALL 10 OLS.
  - Result: 75 - 12 = 63 strategies.
"""
import json
from pathlib import Path

CFG = Path("src/execution/bot_config_math.json")
BACKUP = Path("src/execution/bot_config_math.json.bak_pre_loser_purge")

# Confirmed losers (>=2 trades, 0% WR, Net negative)
CONFIRMED_LOSERS = {
    "GBPAUD_M1_OLS_ALL_DAY_INV",       # 3 trades, -$1,691 (OLS — covered by OLS purge)
    "AUDUSD_M1_SPEC_ALL_DAY_INV",      # 2 trades, -$1,210
    "GBPAUD_M1_HURS_ASIA_INV",          # 2 trades, -$1,167
    "GBPJPY_M1_OLS_LONDON_NY_INV",     # 2 trades, -$1,121 (OLS)
    "GBPUSD_M15_OLS_LONDON_NY_INV",    # 2 trades, -$880  (OLS)
    "EURUSD_M15_OLS_LONDON_INV",       # 2 trades, -$868  (OLS)
}

# Setup-level purge: OLS_SLOPE_STRONG performs 0/6 in live (statistically
# inconsistent with backtest WR=60-69%; P < 0.2% under H0).
PURGE_SETUPS = {"OLS_SLOPE_STRONG"}


def main():
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    portfolio = cfg["portfolio"]
    print(f"Current portfolio: {len(portfolio)} strategies")

    keep, drop = [], []
    drop_reasons = {}
    for p in portfolio:
        sid = p.get("id", "?")
        if sid in CONFIRMED_LOSERS:
            drop.append(p); drop_reasons[sid] = "CONFIRMED_LOSER"
        elif p["setup_type"] in PURGE_SETUPS:
            drop.append(p); drop_reasons[sid] = f"OLS_PURGE (setup={p['setup_type']})"
        else:
            keep.append(p)

    print(f"Dropping: {len(drop)}")
    for p in drop:
        print(f"  - {p['id']}  [{drop_reasons[p['id']]}]")
    print(f"Keeping: {len(keep)}")
    print()
    # New aggregate
    from collections import Counter
    rob = Counter(p.get("robustness_label", "?") for p in keep)
    tf = Counter(p["tf"] for p in keep)
    sym = Counter(p["internal_sym"] for p in keep)
    setup = Counter(p["setup_type"] for p in keep)
    sess = Counter(p["session"] for p in keep)
    avg_wr = sum(p["expected_wr"] for p in keep) / len(keep)
    avg_pf = sum(p["expected_pf"] for p in keep) / len(keep)
    avg_pf_oos = sum(p["expected_pf_oos"] for p in keep) / len(keep)
    sum_tpy = sum(p["expected_trades_per_year"] for p in keep)
    avg_ruin = sum(p["mc_ruin_pct"] for p in keep) / len(keep)
    print(f"By TF: {dict(tf)}")
    print(f"By setup: {dict(setup)}")
    print(f"Avg WR={avg_wr:.4f}  Avg PF={avg_pf:.2f}  Avg PF OOS={avg_pf_oos:.2f}")

    out = dict(cfg)
    out["_doc"] = (out["_doc"] + " | LOSER-PURGE 2026-05-13: removed 6 confirmed "
                   "losers (n>=2 0% WR) + all 10 OLS_SLOPE_STRONG (consistent "
                   "0/6 live failures). 75 -> 63 strategies.")
    out["_metrics_aggregate"] = {
        "n_strategies": len(keep),
        "by_robustness": dict(rob),
        "by_tf": dict(tf),
        "by_symbol": dict(sym),
        "by_setup": dict(setup),
        "by_session": dict(sess),
        "avg_wr": round(avg_wr, 4),
        "avg_pf": round(avg_pf, 3),
        "avg_pf_oos": round(avg_pf_oos, 3),
        "avg_mc_ruin_pct": round(avg_ruin, 3),
        "sum_trades_per_year": round(sum_tpy, 1),
    }
    out["portfolio"] = keep

    BACKUP.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    CFG.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nBackup: {BACKUP}")
    print(f"Wrote: {CFG} ({len(keep)} strategies)")


if __name__ == "__main__":
    main()
