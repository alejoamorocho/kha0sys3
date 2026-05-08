"""Construye bot_config_math.json con las 97 estrategias K3 overlap-free.

Cada entry tiene:
  - id:             nombre claro y único (sym_tf_setup_session_inv)
  - sym:            broker name (con sufijo + para FX Vantage)
  - internal_sym:   nombre interno
  - tf:             M1 / M15 / H1
  - session:        ASIA / LONDON / NY / LONDON_NY / ALL_DAY
  - setup_type:     uno de los 6 setups MATH
  - direction_mode: INVERT (inv=T) o NORMAL (inv=F)
  - tp_atr_mult, sl_atr_mult, atr_period
  - expected_*:     wr, pf, n_trades, trades_per_year, dd_r, calmar
  - rr:             tp_atr_mult / sl_atr_mult

Risk: tier único 0.5%/0.5% (fijo independiente de WR).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
import yaml
import polars as pl

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent
PARQUET = REPO / "reports/external/math_discovery_m1_phase_k3_dedup_overlap.parquet"
MAPPING_FILE = REPO / "config/symbol_mapping.yaml"
OUT = REPO / "src/execution/bot_config_math.json"
BACKUP = REPO / "src/execution/bot_config_math.json.bak_pre_k3_97"


def load_symbol_mapping() -> dict[str, str]:
    with open(MAPPING_FILE) as f:
        cfg = yaml.safe_load(f)
    return cfg["mapping"]


def make_id(r: dict) -> str:
    """sym_tf_setup_session_dir e.g. EURUSD_H1_KAMA_NY_INV"""
    setup_short = {
        "KAMA_CROSS_MOM": "KAMA",
        "SPECTRAL_TREND_MOM": "SPEC",
        "VELOCITY_ACCEL_GO": "VEL",
        "KALMAN_INNOV_EXPAND": "KAL",
        "HURST_TREND_MOM": "HURS",
        "OLS_SLOPE_STRONG": "OLS",
    }[r["setup_type"]]
    inv = "INV" if r["invert"] else "NORM"
    return f"{r['symbol']}_{r['tf']}_{setup_short}_{r['session']}_{inv}"


def main():
    mapping = load_symbol_mapping()
    df = pl.read_parquet(PARQUET).sort("calmar", descending=True)

    portfolio = []
    for r in df.iter_rows(named=True):
        internal = r["symbol"]
        broker = mapping.get(internal)
        if broker is None:
            print(f"[WARN] no broker mapping for {internal} — skipping")
            continue
        tp = float(r["tp_mult"])
        sl = float(r["sl_mult"])
        portfolio.append({
            "id": make_id(r),
            "sym": broker,
            "internal_sym": internal,
            "tf": r["tf"],
            "session": r["session"],
            "setup_type": r["setup_type"],
            "direction_mode": "INVERT" if r["invert"] else "NORMAL",
            "tp_atr_mult": tp,
            "sl_atr_mult": sl,
            "atr_period": 14,
            "rr": round(tp / sl, 3) if sl > 0 else 0.0,
            "expected_wr": round(float(r["wr"]), 4),
            "expected_pf": round(float(r["pf"]), 3),
            "expected_n_trades": int(r["n_trades"]),
            "expected_trades_per_year": round(float(r["trades_per_year"]), 1),
            "expected_dd_r": round(float(r["max_dd_r"]), 1),
            "expected_calmar": round(float(r["calmar"]), 4),
            "expected_expectancy_r": round(float(r["expectancy_r"]), 3),
        })

    # Aggregate stats for header
    from collections import Counter
    by_tf = Counter(s["tf"] for s in portfolio)
    by_setup = Counter(s["setup_type"] for s in portfolio)
    by_sym = Counter(s["internal_sym"] for s in portfolio)
    by_sess = Counter(s["session"] for s in portfolio)
    avg_wr = sum(s["expected_wr"] for s in portfolio) / max(len(portfolio), 1)
    avg_pf = sum(s["expected_pf"] for s in portfolio) / max(len(portfolio), 1)
    sum_tpy = sum(s["expected_trades_per_year"] for s in portfolio)

    cfg = {
        "_doc": (
            "K3 portfolio — 97 strategies overlap-free. M1 (77) + M15 (13) + H1 (7). "
            "6 setups (KAMA_CROSS_MOM, SPECTRAL_TREND_MOM, VELOCITY_ACCEL_GO, "
            "KALMAN_INNOV_EXPAND, HURST_TREND_MOM, OLS_SLOPE_STRONG). 14 symbols. "
            "Friction Vantage realista 0.05R FX / 0.10R no-FX. "
            "Gate WR>=0.6, PF>=1.3, n>=30 + sessions disjuntas dentro de (sym,setup,tf)."
        ),
        "_metrics_aggregate": {
            "n_strategies": len(portfolio),
            "by_tf": dict(by_tf),
            "by_setup": dict(by_setup),
            "by_session": dict(by_sess),
            "by_symbol": dict(by_sym.most_common()),
            "avg_wr": round(avg_wr, 4),
            "avg_pf": round(avg_pf, 3),
            "sum_trades_per_year": round(sum_tpy, 1),
        },
        "risk_scaling": {
            "min_wr": 0.50,
            "max_wr": 1.00,
            "_doc": "Tier único 0.5% fijo. WR no escala (min == max).",
            "tiers": [
                {"max_balance": None, "min_risk": 0.005, "max_risk": 0.005}
            ]
        },
        "portfolio": portfolio,
    }

    if OUT.exists():
        if not BACKUP.exists():
            BACKUP.write_text(OUT.read_text(encoding="utf-8"), encoding="utf-8")
            print(f"Backup -> {BACKUP}")
        else:
            print(f"Backup ya existe: {BACKUP}")

    OUT.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    print(f"\nWrote {OUT}")
    print(f"  Strategies: {len(portfolio)}")
    print(f"  By TF:      {dict(by_tf)}")
    print(f"  By setup:   {dict(by_setup)}")
    print(f"  By session: {dict(by_sess)}")
    print(f"  Avg WR:     {avg_wr:.3f}")
    print(f"  Avg PF:     {avg_pf:.3f}")
    print(f"  Sum tpy:    {sum_tpy:.0f} trades/year")
    print(f"  Risk:       0.5% fijo")

    # Sanity: print the first 3 IDs for visual validation
    print(f"\nFirst 5 IDs:")
    for s in portfolio[:5]:
        print(f"  {s['id']:<40s} -> {s['sym']:<10s} tp={s['tp_atr_mult']} sl={s['sl_atr_mult']}")


if __name__ == "__main__":
    main()
