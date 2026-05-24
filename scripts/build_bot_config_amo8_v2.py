"""Build bot_config_amo8.json V2 from the 116 high-confidence event-level winners.

Differences vs V1:
  - Event-level matching (not pattern_id sub-bucket)
  - 14 symbols (incl. WTI, BRENT, XAGUSD, all FX) vs 5 in V1
  - 4 magic_times (00:00, 07:00, 12:30, 22:00) vs 1 in V1
  - 4 OR durations (15/30/60/120) vs 3 in V1
  - Risk per trade reduced to 0.05% (116 configs × 0.05% = 5.8% max simultaneous)
  - All exits OR_FIXED (no ATR-based exits — known biased)

Input:  reports/orb/amo8_event_level_winners.parquet
Output: src/execution/bot_config_amo8.json
"""
from __future__ import annotations
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from datetime import datetime, timezone

import polars as pl
import yaml

MAGIC_NUMBER = 8338
RISK_PER_TRADE = 0.0005  # 0.05% per config — 116 configs => 5.8% max simultaneous
# Strong filter applied during analysis: PF>=2.0, WR>=65%, tpy>=50
PF_MIN = 2.0
WR_MIN = 0.65
TPY_MIN = 50.0


def _load_symbol_mapping() -> dict[str, str]:
    cfg = yaml.safe_load(Path("config/symbol_mapping.yaml").read_text())
    return cfg["mapping"]


def main():
    df = pl.read_parquet("reports/orb/amo8_event_level_winners.parquet")
    strong = df.filter(
        (pl.col("pf") >= PF_MIN)
        & (pl.col("win_rate") >= WR_MIN)
        & (pl.col("tpy") >= TPY_MIN)
    ).sort("pf", descending=True)
    print(f"Loaded {len(df)} event-level winners total")
    print(f"After strong filter (PF>={PF_MIN}, WR>={WR_MIN}, tpy>={TPY_MIN}): {len(strong)}")

    sym_map = _load_symbol_mapping()
    portfolio = []
    skipped = []
    for idx, row in enumerate(strong.iter_rows(named=True), start=1):
        internal_sym = row["sym"]
        broker_sym = sym_map.get(internal_sym)
        if broker_sym is None:
            skipped.append(internal_sym)
            continue
        sl_or = float(row["sl_or"])
        rr = float(row["rr"])
        or_dur = int(row["or_dur"])
        direction = row["direction"]
        event = row["event"]
        mt = row["magic_time"]
        dir_short = "L" if direction == "LONG" else "S"
        # Strategy ID encodes everything human-readable
        mt_safe = mt.replace(":", "")
        sid = (f"AMO8_{internal_sym}_{mt_safe}_{or_dur}m_"
               f"{event}_{dir_short}_OR{int(sl_or*10):02d}_RR{int(rr*10):02d}_"
               f"{idx:03d}")
        # Synthetic pattern_id for the order manager dedup logic.
        # The live engine matches on event_type + direction when match_mode="event_only".
        # Pattern_id needs to be UNIQUE per (sym, mt, or_dur, event, direction, sl, rr) so
        # different sl/rr combos on the same trigger can coexist and be tracked.
        synthetic_pid = (
            f"EVENT_ONLY:{event}_{mt_safe}_{or_dur}m_OR{int(sl_or*10):02d}_RR{int(rr*10):02d}"
        )
        portfolio.append({
            "id": sid,
            "internal_sym": internal_sym,
            "broker_sym": broker_sym,
            "or_duration_min": or_dur,
            "magic_time": mt,
            # NEW: event-level matching
            "match_mode": "event_only",
            "event_type": event,
            "direction": direction,
            # Legacy field preserved as synthetic ID for order-manager dedup
            "pattern_id": synthetic_pid,
            # Legacy slot fields (kept null since not used in event_only matching)
            "or_position": None,
            "or_atr_bucket": None,
            "pd_or_bucket": None,
            "exit_rules": {
                "mode": "OR_FIXED",
                "sl_or_frac": sl_or,
                "tp_or_frac": sl_or * rr,  # absolute fraction of OR_width
                "rr": rr,
                "max_hold_min": 10 * or_dur,
                "wait_fill_min": 5 * or_dur,
            },
            "expected_wr": float(row["win_rate"]),
            "expected_pf": float(row["pf"]),
            "expected_trades_per_year": float(row["tpy"]),
            "expected_n_trades": int(row["trades"]),
            "expected_expectancy_r": float(row["expectancy_r"]),
            "expected_sum_r": float(row["sum_r"]),
        })

    if skipped:
        print(f"Skipped (no broker mapping): {set(skipped)}")

    # Aggregate metrics
    sum_tpy = sum(s["expected_trades_per_year"] for s in portfolio)
    avg_pf = sum(s["expected_pf"] * s["expected_n_trades"] for s in portfolio) / max(
        sum(s["expected_n_trades"] for s in portfolio), 1
    )
    avg_wr = sum(s["expected_wr"] * s["expected_n_trades"] for s in portfolio) / max(
        sum(s["expected_n_trades"] for s in portfolio), 1
    )
    from collections import Counter
    syms_dist = Counter(s["internal_sym"] for s in portfolio)
    mt_dist = Counter(s["magic_time"] for s in portfolio)
    or_dist = Counter(s["or_duration_min"] for s in portfolio)
    event_dist = Counter(s["event_type"] for s in portfolio)

    cfg_out = {
        "_doc": (f"AMO8 V2 (event-level discovery). Built {datetime.now(timezone.utc).isoformat()}. "
                 f"Replaces V1 (84 sub-bucketed configs that never fired live due to ATR bias). "
                 f"V2 = 116 winners from event-level aggregation across 14 symbols × 4 magic_times × "
                 f"4 OR_dur. Filter: PF>={PF_MIN}, WR>={WR_MIN}, tpy>={TPY_MIN}. Risk reduced to "
                 f"{RISK_PER_TRADE*100:.3f}% per trade (max simultaneous = {RISK_PER_TRADE*len(portfolio)*100:.1f}%)."),
        "_metrics_aggregate": {
            "n_strategies": len(portfolio),
            "n_unique_pattern_slots": len(set(
                (s["internal_sym"], s["magic_time"], s["or_duration_min"],
                 s["event_type"], s["direction"]) for s in portfolio
            )),
            "sum_trades_per_year": round(sum_tpy, 1),
            "avg_wr_weighted": round(avg_wr, 4),
            "avg_pf_weighted": round(avg_pf, 4),
            "max_simultaneous_risk_pct": round(RISK_PER_TRADE * len(portfolio) * 100, 2),
            "symbols_distribution": dict(syms_dist),
            "magic_time_distribution": dict(mt_dist),
            "or_dur_distribution": dict(or_dist),
            "event_distribution": dict(event_dist),
        },
        "magic_number": MAGIC_NUMBER,
        "risk_per_trade": RISK_PER_TRADE,
        "risk_scaling": "balance",
        "portfolio": portfolio,
    }

    out_path = Path("src/execution/bot_config_amo8.json")
    out_path.write_text(json.dumps(cfg_out, indent=2), encoding="utf-8")
    print(f"\nWrote {out_path}")
    print(f"  configs: {len(portfolio)}")
    print(f"  unique slots: {cfg_out['_metrics_aggregate']['n_unique_pattern_slots']}")
    print(f"  sum tpy: {sum_tpy:.0f}")
    print(f"  weighted PF: {avg_pf:.3f}, WR: {avg_wr*100:.1f}%")
    print(f"  risk per trade: {RISK_PER_TRADE*100:.3f}%")
    print(f"  max simultaneous risk (if ALL fire): {RISK_PER_TRADE*len(portfolio)*100:.2f}%")
    print(f"  symbols: {dict(syms_dist)}")
    print(f"  magic_times: {dict(mt_dist)}")
    print(f"  OR_durations: {dict(or_dist)}")
    print(f"  events: {dict(event_dist)}")


if __name__ == "__main__":
    main()
