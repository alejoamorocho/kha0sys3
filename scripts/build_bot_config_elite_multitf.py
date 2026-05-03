"""Build bot_config_math.json from elite WR>=65% portfolio across M15/H1/H4.

Each entry has a `tf` field (M15/H1/H4) so the engine knows which TF bars
to fetch per strategy.
"""
import json
from pathlib import Path
import polars as pl

ROOT = Path(__file__).resolve().parents[1]
CFG_PATH = ROOT / "src" / "execution" / "bot_config_math.json"
ELITE_PATH = ROOT / "reports" / "elite_wr65_portfolio.parquet"

VANTAGE_MAP = {
    "AUDUSD": "AUDUSD+", "EURJPY": "EURJPY+", "EURUSD": "EURUSD+",
    "GBPAUD": "GBPAUD+", "GBPJPY": "GBPJPY+", "GBPUSD": "GBPUSD+",
    "USDJPY": "USDJPY+", "XAGUSD": "XAGUSD",  "XAUUSD": "XAUUSD+",
}


def main():
    with open(CFG_PATH) as f:
        cur = json.load(f)
    risk_scaling = cur["risk_scaling"]

    df = pl.read_parquet(ELITE_PATH).sort(["tf", "wr"], descending=[False, True])

    portfolio = []
    for r in df.iter_rows(named=True):
        sym_int = r["symbol"]
        sym_v = VANTAGE_MAP.get(sym_int)
        if sym_v is None:
            continue
        portfolio.append({
            "sym": sym_v,
            "internal_sym": sym_int,
            "tf": r["tf"],
            "session": r["session"],
            "setup_type": r["setup_type"],
            "direction_mode": r["direction_mode"],
            "tp_atr_mult": round(float(r["tp"]), 2),
            "sl_atr_mult": round(float(r["sl"]), 2),
            "atr_period": 14,
            "regime": r["regime"],
            "rr": round(float(r["rr"]), 2),
            "expected_wr": round(float(r["wr"]), 4),
            "expected_pf": round(float(r["pf"]), 3),
            "expected_pf_oos": round(float(r["wf_pf_te"]), 3),
            "expected_expectancy_r": round(float(r["exp_r"]), 4),
            "expected_dd_r": round(float(r["max_dd"]), 2),
            "expected_tpy": round(float(r["tpy"]), 1),
            "mc_ruin_pct": round(float(r["mc_ruin"]), 4),
        })

    n = len(portfolio)
    by_tf = {}
    for p in portfolio:
        by_tf[p["tf"]] = by_tf.get(p["tf"], 0) + 1

    avg_wr = sum(p["expected_wr"] for p in portfolio) / n
    avg_pf = sum(p["expected_pf"] for p in portfolio) / n
    avg_pf_oos = sum(p["expected_pf_oos"] for p in portfolio) / n

    out = {
        "_doc": ("ELITE WR>=65% portfolio — multi-TF (M15/H1/H4) "
                 "from Optuna 3-regime + robustness. FUERTE only, MC ruin<=1%, "
                 "PF OOS>=1.5. Filtered for high-WR low-capital deployment."),
        "_metrics_aggregate": {
            "n_strategies": n,
            "by_tf": by_tf,
            "avg_wr": round(avg_wr, 4),
            "avg_pf": round(avg_pf, 3),
            "avg_pf_oos": round(avg_pf_oos, 3),
        },
        "risk_scaling": risk_scaling,
        "portfolio": portfolio,
    }

    backup = CFG_PATH.with_suffix(".json.bak_pre_elite")
    with open(backup, "w") as f:
        json.dump(cur, f, indent=2)
    with open(CFG_PATH, "w") as f:
        json.dump(out, f, indent=2)

    print(f"Wrote {CFG_PATH} with {n} strategies")
    print(f"By TF: {by_tf}")
    print(f"Backup: {backup}")
    print(f"Avg WR={avg_wr:.4f} PF={avg_pf:.2f} PF OOS={avg_pf_oos:.2f}")


if __name__ == "__main__":
    main()
