"""Build bot_config_math.json with the 75 K3+M1mgmt deduped strategies.

Source: reports/k3m1_dedup75_robustness.parquet (FUERTE + ACEPTABLE only).
All strategies validated with:
  - M1 management (TP/SL walked minute-by-minute)
  - Realistic Vantage friction (per-symbol)
  - MC 10k bootstrap (ruin < 5%)
  - Walk-forward 50/50 (PF OOS >= 1.0)
  - Decay yearly slope

Risk: tier único 0.5%/0.5% (fijo, mismo que K3-97).
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
import yaml
import polars as pl

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent
PARQUET = REPO / "reports/k3m1_dedup75_robustness.parquet"
MAPPING_FILE = REPO / "config/symbol_mapping.yaml"
OUT = REPO / "src/execution/bot_config_math.json"
BACKUP = REPO / "src/execution/bot_config_math.json.bak_pre_k3m1_75"


def load_symbol_mapping() -> dict[str, str]:
    with open(MAPPING_FILE) as f:
        cfg = yaml.safe_load(f)
    return cfg["mapping"]


def make_id(r: dict) -> str:
    """sym_tf_setup_session_dir e.g. XAGUSD_H1_OLS_ASIA_INV"""
    setup_short = {
        "KAMA_CROSS_MOM": "KAMA",
        "SPECTRAL_TREND_MOM": "SPEC",
        "VELOCITY_ACCEL_GO": "VEL",
        "KALMAN_INNOV_EXPAND": "KAL",
        "HURST_TREND_MOM": "HURS",
        "OLS_SLOPE_STRONG": "OLS",
    }[r["setup_type"]]
    dir_short = "INV" if r["direction_mode"] == "INVERT" else "NORM"
    return f"{r['symbol']}_{r['signal_tf']}_{setup_short}_{r['session']}_{dir_short}"


def main():
    mapping = load_symbol_mapping()
    df = pl.read_parquet(PARQUET)
    # Sort by robustness label (FUERTE first) then PF OOS
    label_order = {"FUERTE": 0, "ACEPTABLE": 1, "DEBIL": 2, "MUERTA": 3}
    df = df.with_columns(
        pl.col("label").replace_strict(label_order, default=99).alias("_lbl")
    ).sort(["_lbl", "wf_pf_te"], descending=[False, True]).drop("_lbl")

    portfolio = []
    skipped = 0
    for r in df.iter_rows(named=True):
        internal = r["symbol"]
        broker = mapping.get(internal)
        if broker is None:
            print(f"[WARN] no broker mapping for {internal} — skipping")
            skipped += 1
            continue
        tp = float(r["tp"])
        sl = float(r["sl"])
        portfolio.append({
            "id": make_id(r),
            "sym": broker,
            "internal_sym": internal,
            "tf": r["signal_tf"],
            "session": r["session"],
            "setup_type": r["setup_type"],
            "direction_mode": r["direction_mode"],
            "tp_atr_mult": tp,
            "sl_atr_mult": sl,
            "atr_period": 14,
            "rr": round(tp / sl, 3) if sl > 0 else 0.0,
            # Backtest expectations
            "expected_wr": round(float(r["wr"]), 4),
            "expected_pf": round(float(r["pf"]), 3),
            "expected_pf_oos": round(float(r["wf_pf_te"] or 0), 3),
            "expected_n_trades": int(r["n"]),
            "expected_trades_per_year": round(float(r["tpy"]), 1),
            "expected_dd_r": round(float(r["max_dd_r"]), 2),
            "expected_expectancy_r": round(float(r["exp_r"]), 4),
            "expected_net_r": round(float(r["net_r"]), 1),
            # Robustness validation
            "robustness_label": r["label"],
            "mc_ruin_pct": round(float(r["mc_ruin_pct"]), 3),
            "wf_deg_wr_pct": round(float(r["wf_deg_wr_pct"] or 0), 2),
            "decay_label": r["decay_label"],
            "friction_r": round(float(r["friction_r"]), 4),
        })

    n = len(portfolio)
    cls_counter = Counter(p["robustness_label"] for p in portfolio)
    tf_counter = Counter(p["tf"] for p in portfolio)
    sym_counter = Counter(p["internal_sym"] for p in portfolio)
    setup_counter = Counter(p["setup_type"] for p in portfolio)
    sess_counter = Counter(p["session"] for p in portfolio)

    avg_wr = sum(p["expected_wr"] for p in portfolio) / n
    avg_pf = sum(p["expected_pf"] for p in portfolio) / n
    avg_pf_oos = sum(p["expected_pf_oos"] for p in portfolio) / n
    sum_tpy = sum(p["expected_trades_per_year"] for p in portfolio)
    avg_ruin = sum(p["mc_ruin_pct"] for p in portfolio) / n

    out = {
        "_doc": ("K3+M1mgmt 75 portfolio — discovery on 4 signal TFs (M1/M15/H1/H4) "
                 "with M1 management (TP/SL walked minute-by-minute). "
                 "Realistic Vantage friction (per-symbol). All FUERTE + ACEPTABLE "
                 "after MC 10k bootstrap + walk-forward 50/50 + decay analysis. "
                 "DEDUPED: best session per (symbol, tf, setup, direction)."),
        "_metrics_aggregate": {
            "n_strategies": n,
            "by_robustness": dict(cls_counter),
            "by_tf": dict(tf_counter),
            "by_symbol": dict(sym_counter),
            "by_setup": dict(setup_counter),
            "by_session": dict(sess_counter),
            "avg_wr": round(avg_wr, 4),
            "avg_pf": round(avg_pf, 3),
            "avg_pf_oos": round(avg_pf_oos, 3),
            "avg_mc_ruin_pct": round(avg_ruin, 3),
            "sum_trades_per_year": round(sum_tpy, 1),
        },
        "risk_scaling": {
            "min_wr": 0.50,
            "max_wr": 1.00,
            "tiers": [
                {"max_balance": None, "min_risk": 0.005, "max_risk": 0.005},
            ],
        },
        "portfolio": portfolio,
    }

    if OUT.exists():
        cur = json.loads(OUT.read_text(encoding="utf-8"))
        BACKUP.write_text(json.dumps(cur, indent=2), encoding="utf-8")
        print(f"Backup: {BACKUP}")

    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Wrote {OUT} with {n} strategies (skipped {skipped})")
    print()
    print(f"By robustness: {dict(cls_counter)}")
    print(f"By TF: {dict(tf_counter)}")
    print(f"By setup: {dict(setup_counter)}")
    print(f"Avg WR={avg_wr:.4f} PF={avg_pf:.2f} PF OOS={avg_pf_oos:.2f}")
    print(f"Avg MC ruin: {avg_ruin:.3f}%  Sum tpy: {sum_tpy:.0f}")


if __name__ == "__main__":
    main()
