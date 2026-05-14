"""Build live config para los 2 sistemas Traders:

  Swing (magic 1339): 5 estrategias D1-setup + M1 intraday breakout entry
  ORB   (magic 1340): 12 estrategias intradia opening range breakout

Reglas hardcoded segun la decision 2026-05-14:
  - Risk unificado 0.1% per trade en TODOS los sistemas.
  - Swing: 3 PDF-strict + 2 grid winners (best variant por sym/setup).
  - ORB: 12 grid uniform (top sum_R per sym) — gestion intradia.

Outputs:
  src/execution/bot_config_traders_swing.json
  src/execution/bot_config_traders_orb.json
"""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path


OUT_DIR = Path("src/execution")

UNIFIED_RISK = 0.001  # 0.1% per trade

# ── Tier 1: SWING (magic 1339) ───────────────────────────────────────────
# Cada entry: nomenclatura clara TS_<SYM>_<SETUP>_<VARIANTE>
# variant: PDF = PDF-strict (reglas literales del PDF), GRID = best grid uniform
SWING_STRATEGIES = [
    {
        "id": "TS_XAGUSD_QULLAHTF_PDF",
        "sym": "XAGUSD", "internal_sym": "XAGUSD",
        "trader": "Qulla", "setup_type": "HTF",
        "variant": "PDF",
        "signal_tf": "D1", "entry_tf": "M1",
        "direction_mode": "LONG",
        "exit_rules": {
            "initial_sl_type": "atr",
            "initial_sl_atr_mult": 1.0,
            "initial_sl_pct": None,
            "partials": [
                {"trigger": "days_held", "value": 3, "sell_frac": 0.30},
                {"trigger": "days_held", "value": 5, "sell_frac": 0.20},
            ],
            "trail_sma": 50,
            "time_stop_days": None,
            "max_hold_days": 40,
            "wait_bars": 2,
        },
        "valid_days": 5,
        # Backtest expected
        "expected_wr": 0.4233,
        "expected_pf": 2.299,
        "expected_pf_oos": 2.084,
        "expected_n_trades": 300,
        "expected_trades_per_year": 40.9,
        "expected_dd_r": 26.36,
        "expected_expectancy_r": 0.666,
        "expected_net_r": 199.79,
        "robustness_label": "FUERTE",
        "mc_ruin_pct": 0.11,
    },
    {
        "id": "TS_XAUUSD_MINERVINI_VCP_PDF",
        "sym": "XAUUSD", "internal_sym": "XAUUSD",
        "trader": "Minervini", "setup_type": "VCP",
        "variant": "PDF",
        "signal_tf": "D1", "entry_tf": "M1",
        "direction_mode": "LONG",
        "exit_rules": {
            "initial_sl_type": "pct",
            "initial_sl_atr_mult": None,
            "initial_sl_pct": 0.075,
            "partials": [
                {"trigger": "r_multiple", "value": 2.0, "sell_frac": 0.25},
                {"trigger": "r_multiple", "value": 4.0, "sell_frac": 0.25},
            ],
            "trail_sma": 10,
            "time_stop_days": None,
            "max_hold_days": 60,
            "wait_bars": 2,
        },
        "valid_days": 5,
        "expected_wr": 0.5884,
        "expected_pf": 2.236,
        "expected_pf_oos": 6.831,
        "expected_n_trades": 328,
        "expected_trades_per_year": 45.8,
        "expected_dd_r": 41.58,
        "expected_expectancy_r": 0.329,
        "expected_net_r": 107.87,
        "robustness_label": "ACEPTABLE",
        "mc_ruin_pct": 0.00,
    },
    {
        "id": "TS_XAUUSD_QULLAHTF_GRID",
        "sym": "XAUUSD", "internal_sym": "XAUUSD",
        "trader": "Qulla", "setup_type": "HTF",
        "variant": "GRID",
        "signal_tf": "D1", "entry_tf": "M1",
        "direction_mode": "LONG",
        "exit_rules": {
            "initial_sl_type": "atr",
            "initial_sl_atr_mult": 1.0,
            "initial_sl_pct": None,
            "partials": [
                {"trigger": "r_multiple", "value": 1.5, "sell_frac": 0.30},
                {"trigger": "r_multiple", "value": 3.0, "sell_frac": 0.30},
            ],
            "trail_sma": None,
            "time_stop_days": None,
            "max_hold_days": 15,
            "wait_bars": 2,
        },
        "valid_days": 3,
        "expected_wr": 0.4890,
        "expected_pf": 1.723,
        "expected_pf_oos": 2.644,
        "expected_n_trades": 227,
        "expected_trades_per_year": 33.6,
        "expected_dd_r": 32.21,
        "expected_expectancy_r": 0.402,
        "expected_net_r": 91.13,
        "robustness_label": "ACEPTABLE",
        "mc_ruin_pct": 0.02,
    },
    {
        "id": "TS_XAGUSD_MINERVINI_VCP_GRID",
        "sym": "XAGUSD", "internal_sym": "XAGUSD",
        "trader": "Minervini", "setup_type": "VCP",
        "variant": "GRID",
        "signal_tf": "D1", "entry_tf": "M1",
        "direction_mode": "LONG",
        "exit_rules": {
            "initial_sl_type": "atr",
            "initial_sl_atr_mult": 1.5,
            "initial_sl_pct": None,
            "partials": [
                {"trigger": "r_multiple", "value": 1.5, "sell_frac": 0.30},
                {"trigger": "r_multiple", "value": 3.0, "sell_frac": 0.30},
            ],
            "trail_sma": 50,
            "time_stop_days": None,
            "max_hold_days": 30,
            "wait_bars": 2,
        },
        "valid_days": 3,
        "expected_wr": 0.4136,
        "expected_pf": 1.467,
        "expected_pf_oos": 1.802,
        "expected_n_trades": 162,
        "expected_trades_per_year": 23.6,
        "expected_dd_r": 38.31,
        "expected_expectancy_r": 0.303,
        "expected_net_r": 49.17,
        "robustness_label": "ACEPTABLE",
        "mc_ruin_pct": 0.39,
    },
    {
        "id": "TS_BRENT_MINERVINI_VCP_GRID",
        "sym": "BRENT", "internal_sym": "BRENT",
        "trader": "Minervini", "setup_type": "VCP",
        "variant": "GRID",
        "signal_tf": "D1", "entry_tf": "M1",
        "direction_mode": "LONG",
        "exit_rules": {
            "initial_sl_type": "atr",
            "initial_sl_atr_mult": 1.0,
            "initial_sl_pct": None,
            "partials": [
                {"trigger": "r_multiple", "value": 1.0, "sell_frac": 0.30},
                {"trigger": "r_multiple", "value": 2.0, "sell_frac": 0.30},
            ],
            "trail_sma": 50,
            "time_stop_days": None,
            "max_hold_days": 30,
            "wait_bars": 2,
        },
        "valid_days": 3,
        "expected_wr": 0.4198,
        "expected_pf": 1.565,
        "expected_pf_oos": 1.964,
        "expected_n_trades": 81,
        "expected_trades_per_year": 15.7,
        "expected_dd_r": 13.10,
        "expected_expectancy_r": 0.374,
        "expected_net_r": 30.32,
        "robustness_label": "ACEPTABLE",
        "mc_ruin_pct": 0.00,
    },
]


# ── Tier 2: ORB (magic 1340) ─────────────────────────────────────────────
# Nomenclatura: TO_<SYM>_<OH>h_<RM>m
# Todas las ORB: SL = sl_atr × ATR_M1, partial 50% en partial_R, max_hold_hours
ORB_STRATEGIES = [
    # (sym, open_hour, range_min, sl_atr, max_hours, partial_R, n_trades, wr, pf, pf_oos, tpy, sum_r)
    ("WTI",        13, 15, 0.5, 4, 3.0, 1639, 0.5095, 2.793, 2.237, 196.6, 1868.55),
    ("GBPJPY",      7, 30, 0.5, 8, 2.0, 1454, 0.5578, 2.754, 2.643, 174.3, 1557.87),
    ("BRENT",      13, 30, 0.5, 4, 3.0, 1543, 0.5217, 2.715, 2.340, 185.2, 1634.57),
    ("XAUUSD",      7, 30, 0.5, 4, 3.0, 1442, 0.5125, 2.695, 2.957, 172.9, 1509.99),
    ("GBPUSD",      7, 15, 0.5, 8, 2.0, 1603, 0.5964, 2.670, 2.426, 192.2, 1476.89),
    ("EURUSD",     13, 15, 0.5, 8, 3.0, 1691, 0.5056, 2.406, 2.638, 202.8, 1680.28),
    ("NASDAQ100",  13, 30, 0.5, 8, 3.0, 1758, 0.5364, 2.330, 2.053, 210.8, 2102.83),
    ("GBPAUD",      7, 30, 0.5, 8, 2.0, 1452, 0.5716, 2.382, 2.668, 174.1, 1159.34),
    ("XAGUSD",     13, 30, 0.5, 4, 2.0, 1419, 0.5490, 2.282, 2.223, 170.2, 1018.79),
    ("USDJPY",      7, 15, 0.5, 8, 3.0, 1569, 0.5143, 2.277, 1.617, 188.3, 1469.10),
    ("AUDUSD",     13, 30, 0.5, 8, 3.0, 1574, 0.5032, 2.263, 2.581, 188.7, 1435.66),
    ("EURJPY",      7, 15, 0.5, 8, 2.0, 1633, 0.5566, 2.075, 2.090, 195.8, 1125.41),
]


def _build_orb_entry(t: tuple) -> dict:
    sym, oh, rm, sl, mh, pr, n, wr, pf, pf_oos, tpy, sumr = t
    return {
        "id": f"TO_{sym}_{oh:02d}h_{rm:02d}m",
        "sym": sym, "internal_sym": sym,
        "trader": "Qulla", "setup_type": "ORB",
        "variant": "GRID",
        "signal_tf": "M1", "entry_tf": "M1",
        "direction_mode": "LONG",
        "orb_params": {
            "open_hour_utc": oh,
            "open_minute_utc": 0,
            "range_minutes": rm,
            "breakout_window_minutes": 180,
        },
        "exit_rules": {
            "initial_sl_type": "atr",
            "initial_sl_atr_mult": sl,
            "initial_sl_pct": None,
            "partials": [
                {"trigger": "r_multiple", "value": pr, "sell_frac": 0.50},
            ],
            "trail_sma": None,
            "time_stop_days": None,
            "max_hold_hours": mh,
            "max_hold_days": mh / 24.0,
            "wait_bars": 2,
        },
        "expected_wr": wr,
        "expected_pf": pf,
        "expected_pf_oos": pf_oos,
        "expected_n_trades": n,
        "expected_trades_per_year": tpy,
        "expected_net_r": sumr,
        "robustness_label": "ALTA_FRECUENCIA_OK_BY_SIZING",
    }


def build():
    now = datetime.now(timezone.utc).isoformat()

    # === Swing config ===
    swing_cfg = {
        "_doc": (f"Traders Swing portfolio (magic 1339) — 5 estrategias D1 setup + "
                 f"M1 intraday breakout. PDF-strict (3) + grid winners (2). "
                 f"Risk unificado 0.1% per trade. Built {now}."),
        "_metrics_aggregate": {
            "n_strategies": len(SWING_STRATEGIES),
            "avg_pf": round(sum(s["expected_pf"] for s in SWING_STRATEGIES) / len(SWING_STRATEGIES), 3),
            "avg_pf_oos": round(sum(s["expected_pf_oos"] for s in SWING_STRATEGIES) / len(SWING_STRATEGIES), 3),
            "avg_wr": round(sum(s["expected_wr"] for s in SWING_STRATEGIES) / len(SWING_STRATEGIES), 4),
            "sum_trades_per_year": round(sum(s["expected_trades_per_year"] for s in SWING_STRATEGIES), 1),
            "sum_expected_net_r": round(sum(s["expected_net_r"] for s in SWING_STRATEGIES), 1),
        },
        "magic_number": 1339,
        "risk_per_trade": UNIFIED_RISK,
        "portfolio": SWING_STRATEGIES,
    }

    # === ORB config ===
    orb_entries = [_build_orb_entry(t) for t in ORB_STRATEGIES]
    orb_cfg = {
        "_doc": (f"Traders ORB portfolio (magic 1340) — 12 estrategias intraday opening "
                 f"range breakout. Grid uniform winners. SL tight 0.5xATR_M1, partial 50% "
                 f"en R, max_hold 4-8h. Risk unificado 0.1% per trade. Built {now}."),
        "_metrics_aggregate": {
            "n_strategies": len(orb_entries),
            "avg_pf": round(sum(e["expected_pf"] for e in orb_entries) / len(orb_entries), 3),
            "avg_pf_oos": round(sum(e["expected_pf_oos"] for e in orb_entries) / len(orb_entries), 3),
            "avg_wr": round(sum(e["expected_wr"] for e in orb_entries) / len(orb_entries), 4),
            "sum_trades_per_year": round(sum(e["expected_trades_per_year"] for e in orb_entries), 1),
            "sum_expected_net_r": round(sum(e["expected_net_r"] for e in orb_entries), 1),
        },
        "magic_number": 1340,
        "risk_per_trade": UNIFIED_RISK,
        "portfolio": orb_entries,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    swing_path = OUT_DIR / "bot_config_traders_swing.json"
    orb_path = OUT_DIR / "bot_config_traders_orb.json"
    with swing_path.open("w", encoding="utf-8") as f:
        json.dump(swing_cfg, f, indent=2, ensure_ascii=False)
    with orb_path.open("w", encoding="utf-8") as f:
        json.dump(orb_cfg, f, indent=2, ensure_ascii=False)

    print(f"=> {swing_path}  ({len(SWING_STRATEGIES)} strats, avg PF OOS "
          f"{swing_cfg['_metrics_aggregate']['avg_pf_oos']})")
    print(f"=> {orb_path}  ({len(orb_entries)} strats, avg PF OOS "
          f"{orb_cfg['_metrics_aggregate']['avg_pf_oos']})")
    print(f"Risk unificado: {UNIFIED_RISK} (0.1%)")
    print(f"Total estrategias nuevas: {len(SWING_STRATEGIES) + len(orb_entries)}")


if __name__ == "__main__":
    build()
