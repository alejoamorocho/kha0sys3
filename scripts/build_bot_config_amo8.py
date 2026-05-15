"""Generate bot_config_amo8.json from the 84 PF>=1.3 winners.

Output: src/execution/bot_config_amo8.json

AMO8 portfolio — magic 8338 — ORB pattern fade strategies (intraday).
- Symbols mapped internal -> broker via config/symbol_mapping.yaml
- magic_time stored as broker hour (matches K3M1 convention: broker-time-as-UTC)
- Each config = one strategy entry; same pattern + different management is OK,
  risk_per_trade is set low so 12-overlap on a single signal stays bounded
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import polars as pl
import yaml

from src.application.orb_utils import REPORTS_DIR

MAGIC_NUMBER = 8338
RISK_PER_TRADE = 0.001  # 0.1% per config; with up to 12 overlap on one signal = 1.2% max
PF_MIN = 1.3


def _load_symbol_mapping() -> dict[str, str]:
    cfg = yaml.safe_load(Path("config/symbol_mapping.yaml").read_text())
    return cfg["mapping"]


_EVENTS = [
    "FALSE_BREAK_UP", "FALSE_BREAK_DOWN",
    "BREAK_UP", "BREAK_DOWN",
    "MITIG_PD_MID", "MITIG_PD_CLOSE",
    "REENTRY_PD_OR_HIGH", "REENTRY_PD_OR_LOW",
]
_OR_POSITIONS = [
    "ABOVE_PD_HIGH", "BELOW_PD_LOW",
    "BETWEEN_CLOSE_AND_HIGH", "BETWEEN_LOW_AND_CLOSE",
    "INSIDE_PD_RANGE",
]
_OR_ATR_BUCKETS = ["compressed", "normal", "expanded"]
_PD_OR_BUCKETS = ["gap_up", "gap_down", "inside"]


def _parse_pattern_id(pattern_id: str) -> dict:
    """Parse '{EVENT}_{or_position}_{or_atr_bucket}_{pd_or_bucket}' into components."""
    # Find event (longest prefix match)
    event = None
    rest = pattern_id
    for ev in sorted(_EVENTS, key=len, reverse=True):
        if pattern_id.startswith(ev + "_"):
            event = ev
            rest = pattern_id[len(ev) + 1:]
            break
    if event is None:
        return {"event_type": "UNKNOWN", "or_position": None,
                "or_atr_bucket": None, "pd_or_bucket": None}
    # or_position (longest prefix match)
    or_pos = None
    for op in sorted(_OR_POSITIONS, key=len, reverse=True):
        if rest.startswith(op + "_"):
            or_pos = op
            rest = rest[len(op) + 1:]
            break
    # or_atr_bucket
    atr_b = None
    for ab in _OR_ATR_BUCKETS:
        if rest.startswith(ab + "_"):
            atr_b = ab
            rest = rest[len(ab) + 1:]
            break
    # pd_or_bucket (the remainder)
    pd_b = rest if rest in _PD_OR_BUCKETS else None
    return {"event_type": event, "or_position": or_pos,
            "or_atr_bucket": atr_b, "pd_or_bucket": pd_b}


def _build_strategy_id(row: dict, idx: int) -> str:
    sym = row["symbol"]
    dur = row["or_duration_min"]
    dir_ = row["direction"][0]  # L or S
    mode = row["mode"]
    # event_type lives in pattern_id like "FALSE_BREAK_DOWN_..."
    event = row["pattern_id"].split("_BETWEEN")[0].split("_INSIDE")[0]
    return f"AMO8_{sym}_{dur}m_{event}_{dir_}_{mode}_{idx:02d}"


def _exit_rules_for(row: dict) -> dict:
    """Translate the management mode params into a structured exit_rules dict
    compatible with how live_amo_trader will consume it.
    """
    mode = row["mode"]
    params = row["params"]
    common = {
        "max_hold_min": 10 * int(row["or_duration_min"]),
        "wait_fill_min": 5 * int(row["or_duration_min"]),
    }
    if mode == "ATR":
        # sl_atr=X,rr=Y
        parts = dict(p.split("=") for p in params.split(","))
        return {
            "mode": "ATR",
            "sl_atr_mult": float(parts["sl_atr"]),
            "tp_atr_mult": float(parts["sl_atr"]) * float(parts["rr"]),
            "rr": float(parts["rr"]),
            **common,
        }
    if mode == "OR_FIXED":
        # sl_or=X,rr=Y
        parts = dict(p.split("=") for p in params.split(","))
        return {
            "mode": "OR_FIXED",
            "sl_or_frac": float(parts["sl_or"]),
            "tp_or_frac": float(parts["sl_or"]) * float(parts["rr"]),
            "rr": float(parts["rr"]),
            **common,
        }
    if mode == "DOC":
        return {
            "mode": "DOC",
            "sl_or_frac": 1.0,
            "tp1_or_frac": 1.0,
            "tp2_or_frac": 2.0,
            "tp1_fraction": 0.5,
            "midpoint_mfe_min_r": 0.5,
            **common,
        }
    if mode == "SWING":
        return {
            "mode": "SWING",
            "sl_atr_mult": 1.0,
            "tp1_r": 2.0,
            "tp2_r": 4.0,
            "tp1_fraction": 0.25,
            "tp2_fraction": 0.25,
            "trail_sma_period": 20,
            **common,
        }
    raise ValueError(f"Unknown mode: {mode}")


def main():
    base = Path(REPORTS_DIR)
    df = pl.read_parquet(base / "orb_managements_positive.parquet")
    winners = df.filter(pl.col("pf") >= PF_MIN).sort("pf", descending=True)
    print(f"Loaded {len(df)} positive winners; {len(winners)} pass PF>={PF_MIN}")

    sym_map = _load_symbol_mapping()
    portfolio = []
    for idx, row in enumerate(winners.iter_rows(named=True), start=1):
        internal_sym = row["symbol"]
        broker_sym = sym_map.get(internal_sym)
        if broker_sym is None:
            print(f"[WARN] no broker mapping for {internal_sym}, skipping")
            continue
        parsed = _parse_pattern_id(row["pattern_id"])
        portfolio.append({
            "id": _build_strategy_id(row, idx),
            "internal_sym": internal_sym,
            "broker_sym": broker_sym,
            "or_duration_min": int(row["or_duration_min"]),
            "magic_time": row["magic_time"],  # broker-hour string "HH:MM"
            "pattern_id": row["pattern_id"],
            "event_type": parsed["event_type"],
            "or_position": parsed["or_position"],
            "or_atr_bucket": parsed["or_atr_bucket"],
            "pd_or_bucket": parsed["pd_or_bucket"],
            "direction": row["direction"],
            "exit_rules": _exit_rules_for(row),
            # Backtest expectations
            "expected_wr": round(float(row["win_rate"]), 4),
            "expected_pf": round(float(row["pf"]), 4),
            "expected_trades_per_year": round(float(row["trades_per_year"]), 2),
            "expected_n_trades": int(row["trades"]),
            "expected_expectancy_r": round(float(row["expectancy_r"]), 4),
            "expected_max_dd_r": round(float(row["max_dd_r"]), 2),
            "expected_sum_r": round(float(row["sum_r"]), 1),
        })

    # Aggregate metrics
    total_trades_per_year = sum(s["expected_trades_per_year"] for s in portfolio)
    avg_wr = sum(s["expected_wr"] * s["expected_n_trades"] for s in portfolio) / \
             max(sum(s["expected_n_trades"] for s in portfolio), 1)
    avg_pf = sum(s["expected_pf"] * s["expected_n_trades"] for s in portfolio) / \
             max(sum(s["expected_n_trades"] for s in portfolio), 1)

    config = {
        "_doc": (
            "AMO8 portfolio — magic 8338 — ORB false-break fade strategies. "
            f"Built {datetime.now(timezone.utc).isoformat()}. "
            f"Source: Phase A (14 syms, 3.5M raw triggers, loose gates) → "
            f"Phase B (4 management modes: ATR, OR_FIXED, DOC, SWING) → "
            f"Positive-edge filter (PF>=1.0, WR>=50%, exp_r>0, trades>=30) → "
            f"This file: PF>={PF_MIN} subset. "
            "IMPORTANT: 84 configs on only 7 unique pattern slots — same signal "
            "fires multiple orders with different management. Risk per trade is "
            "0.1% so worst-case ~1.2% per signal."
        ),
        "_metrics_aggregate": {
            "n_strategies": len(portfolio),
            "n_unique_pattern_slots": len(set((s["internal_sym"], s["magic_time"],
                                                s["or_duration_min"], s["pattern_id"],
                                                s["direction"]) for s in portfolio)),
            "sum_trades_per_year": round(total_trades_per_year, 1),
            "avg_wr_weighted": round(avg_wr, 4),
            "avg_pf_weighted": round(avg_pf, 3),
            "modes_distribution": {
                m: sum(1 for s in portfolio if s["exit_rules"]["mode"] == m)
                for m in ("ATR", "OR_FIXED", "DOC", "SWING")
            },
            "symbols_distribution": {
                sym: sum(1 for s in portfolio if s["internal_sym"] == sym)
                for sym in sorted(set(s["internal_sym"] for s in portfolio))
            },
        },
        "magic_number": MAGIC_NUMBER,
        "risk_per_trade": RISK_PER_TRADE,
        "risk_scaling": {
            "min_wr": 0.5,
            "max_wr": 1.0,
            "tiers": [
                {"max_balance": None, "min_risk": RISK_PER_TRADE, "max_risk": RISK_PER_TRADE}
            ],
        },
        "portfolio": portfolio,
    }

    out_path = Path("src/execution/bot_config_amo8.json")
    out_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {out_path}")
    print(f"  {len(portfolio)} configs across {config['_metrics_aggregate']['n_unique_pattern_slots']} unique pattern slots")
    print(f"  Symbols: {config['_metrics_aggregate']['symbols_distribution']}")
    print(f"  Modes:   {config['_metrics_aggregate']['modes_distribution']}")
    print(f"  Sum trades/year: {config['_metrics_aggregate']['sum_trades_per_year']}")
    print(f"  Avg PF weighted: {config['_metrics_aggregate']['avg_pf_weighted']}")


if __name__ == "__main__":
    main()
