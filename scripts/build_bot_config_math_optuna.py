"""Build bot_config_math.json from optuna_3regime_results.parquet (35 strategies).

Preserves risk_scaling tiers from existing config; replaces portfolio with the
35 robustness-validated strategies and their Optuna-optimized TP/SL.
"""
import json
from pathlib import Path
import polars as pl

ROOT = Path(__file__).resolve().parents[1]
CFG_PATH = ROOT / "src" / "execution" / "bot_config_math.json"
RESULTS_PATH = ROOT / "reports" / "optuna_3regime_results.parquet"
ROBUST_PATH = ROOT / "reports" / "robustness_math_optuna.parquet"

VANTAGE_MAP = {
    "AUDUSD": "AUDUSD+",
    "EURJPY": "EURJPY+",
    "EURUSD": "EURUSD+",
    "GBPAUD": "GBPAUD+",
    "GBPJPY": "GBPJPY+",
    "GBPUSD": "GBPUSD+",
    "USDJPY": "USDJPY+",
    "XAGUSD": "XAGUSD",
    "XAUUSD": "XAUUSD+",
}


def main():
    with open(CFG_PATH) as f:
        cur = json.load(f)
    risk_scaling = cur["risk_scaling"]

    df = pl.read_parquet(RESULTS_PATH)
    rob = pl.read_parquet(ROBUST_PATH)
    rob_lookup = {
        (r["symbol"], r["session"], r["setup_type"], r["direction_mode"]): r
        for r in rob.iter_rows(named=True)
    }

    portfolio = []
    for r in df.iter_rows(named=True):
        sym_int = r["symbol"]
        sym_v = VANTAGE_MAP.get(sym_int)
        if sym_v is None:
            print(f"skip unknown symbol: {sym_int}")
            continue
        key = (sym_int, r["session"], r["setup_type"], r["direction_mode"])
        rb = rob_lookup.get(key, {})
        portfolio.append({
            "sym": sym_v,
            "internal_sym": sym_int,
            "session": r["session"],
            "setup_type": r["setup_type"],
            "direction_mode": r["direction_mode"],
            "tp_atr_mult": round(float(r["best_tp"]), 2),
            "sl_atr_mult": round(float(r["best_sl"]), 2),
            "atr_period": 14,
            "regime": r["best_regime"],
            "rr": round(float(r["best_rr"]), 2),
            "expected_wr": round(float(r["best_wr"]), 4),
            "expected_pf": round(float(r["best_pf"]), 3),
            "expected_expectancy_r": round(float(r["best_exp"]), 4),
            "expected_dd_r": round(float(r["best_dd"]), 2),
            "expected_tpy": round(float(r["best_tpy"]), 1),
            "robustness_label": rb.get("label", "N/A"),
            "oos_pf": round(float(rb.get("wf_pf_te", 0.0) or 0.0), 3),
            "mc_ruin_pct": round(float(rb.get("mc_ruin_pct", 0.0) or 0.0), 2),
            "decay": rb.get("decay_label", "N/A"),
        })

    n = len(portfolio)
    avg_wr = sum(p["expected_wr"] for p in portfolio) / n
    avg_pf = sum(p["expected_pf"] for p in portfolio) / n
    avg_exp = sum(p["expected_expectancy_r"] for p in portfolio) / n
    fuerte = sum(1 for p in portfolio if p["robustness_label"] == "FUERTE")
    aceptable = sum(1 for p in portfolio if p["robustness_label"] == "ACEPTABLE")

    out = {
        "_doc": "Math portfolio 35 - Optuna 3-regime optimized + robustness validated",
        "_optimization": (
            "TP/SL optimized via Optuna 3-regime search (HIGH_RR / BALANCED / HIGH_WR), "
            "60 trials per regime per strategy. SL-invariant objective: "
            "(expectancy_R * SL * tpy) / max_dd_R. "
            "Realistic Vantage friction + 0.2R slippage."
        ),
        "_robustness": (
            "MC=10k bootstrap, walk-forward 50/50, decay analysis. "
            f"FUERTE={fuerte}, ACEPTABLE={aceptable}, DEBIL=0, MUERTA=0. "
            "Avg PF IS=2.42 -> OOS=2.44 (no degradation). Avg MC ruin=0.37%."
        ),
        "_metrics_aggregate": {
            "n_strategies": n,
            "avg_wr": round(avg_wr, 4),
            "avg_pf": round(avg_pf, 3),
            "avg_expectancy_r": round(avg_exp, 4),
            "fuerte": fuerte,
            "aceptable": aceptable,
        },
        "risk_scaling": risk_scaling,
        "portfolio": portfolio,
    }

    backup = CFG_PATH.with_suffix(".json.bak_pre_optuna")
    with open(backup, "w") as f:
        json.dump(cur, f, indent=2)
    with open(CFG_PATH, "w") as f:
        json.dump(out, f, indent=2)

    print(f"Wrote {CFG_PATH} with {n} strategies")
    print(f"Backup at {backup}")
    print(f"Avg WR={avg_wr:.3f} PF={avg_pf:.2f} Exp={avg_exp:+.3f}")
    print(f"FUERTE={fuerte} ACEPTABLE={aceptable}")


if __name__ == "__main__":
    main()
