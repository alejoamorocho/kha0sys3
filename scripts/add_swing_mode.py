"""Add only Mode 4 (SWING) to the existing managements compare parquet.

Reads:  reports/orb/orb_managements_compare.parquet (has modes ATR, OR_FIXED, DOC)
        reports/orb/orb_phase_a_triggers.parquet
        reports/orb/orb_phase_a.parquet
        data/enriched_math_tf/<SYM>_M1.parquet
Writes: reports/orb/orb_managements_compare.parquet (overwritten, with SWING rows appended)
        reports/orb/ORB_Managements_Compare.md (regenerated)
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import numpy as np
import polars as pl

from src.application.orb_management_modes import simulate_swing_traders
from src.application.orb_utils import DATA_DIR, REPORTS_DIR
from src.engine.friction_real import friction_r as real_friction_r, load_median_atr


SLIPPAGE_R_FLOOR = 0.2


def _aggregate_trades(realized_r: list[float], span_days: int) -> dict:
    if not realized_r:
        return {
            "trades": 0, "trades_per_year": 0.0, "win_rate": 0.0,
            "pf": 0.0, "expectancy_r": 0.0, "max_dd_r": 0.0,
            "sharpe": 0.0, "rr": 0.0, "sum_r": 0.0,
        }
    r = np.asarray(realized_r, dtype=float)
    wins = r[r > 0].sum()
    losses = -r[r < 0].sum()
    pf = float(wins / losses) if losses > 0 else (float("inf") if wins > 0 else 0.0)
    wr = float((r > 0).mean())
    expectancy = float(r.mean())
    cum = np.cumsum(r)
    dd = float((np.maximum.accumulate(cum) - cum).max()) if len(cum) else 0.0
    span_years = max(span_days / 365.25, 1e-9)
    sharpe = float(r.mean() / r.std() * np.sqrt(252)) if r.std() > 0 else 0.0
    return {
        "trades": int(len(r)),
        "trades_per_year": float(len(r) / span_years),
        "win_rate": wr,
        "pf": pf,
        "expectancy_r": expectancy,
        "max_dd_r": dd,
        "sharpe": sharpe,
        "rr": 3.0,  # SWING avg RR ~3 (TP1=2R + TP2=4R weighted)
        "sum_r": float(r.sum()),
    }


def _load_m1(symbol: str) -> dict:
    m1_df = pl.read_parquet(Path(DATA_DIR) / f"{symbol}_M1.parquet").sort("time")
    return {
        "times": np.array(m1_df["time"].to_list(), dtype="object"),
        "highs": np.asarray(m1_df["high"].to_list(), dtype=float),
        "lows": np.asarray(m1_df["low"].to_list(), dtype=float),
        "closes": np.asarray(m1_df["close"].to_list(), dtype=float),
    }


def _simulate_swing(triggers: pl.DataFrame, symbol: str, or_duration: int, m1: dict) -> list[float]:
    median_atr = load_median_atr(symbol)
    friction_eff = real_friction_r(symbol, 1.0, median_atr) + SLIPPAGE_R_FLOOR
    max_hold_min = 10 * or_duration

    out = []
    for row in triggers.iter_rows(named=True):
        atr = row["atr_at_setup"]
        risk_per_r = 0.5 * atr
        result = simulate_swing_traders(
            fill_ts=row["trigger_ts"], entry=row["trigger_close"],
            direction=row["direction"],
            sl_distance=1.0 * atr,
            max_hold_min=max_hold_min, m1=m1,
            risk_per_r=risk_per_r, friction_r=friction_eff,
            tp1_r=2.0, tp2_r=4.0, tp1_fraction=0.25, tp2_fraction=0.25,
            trail_sma_period=20,
        )
        if result["exit_reason"] != "NO_BARS":
            out.append(result["realized_r"])
    return out


def main():
    base = Path(REPORTS_DIR)
    print("[swing] loading existing compare parquet + survivors + triggers ...", flush=True)
    existing = pl.read_parquet(base / "orb_managements_compare.parquet")
    survivors = pl.read_parquet(base / "orb_phase_a.parquet")
    triggers = pl.read_parquet(base / "orb_phase_a_triggers.parquet")
    print(f"[swing] existing: {len(existing)} rows, survivors: {len(survivors)}, triggers: {len(triggers):,}", flush=True)

    # Drop any pre-existing SWING rows so we can re-run cleanly
    existing = existing.filter(pl.col("mode") != "SWING")

    new_rows: list[dict] = []
    m1_cache: dict[str, dict] = {}
    t_total = time.time()
    total = len(survivors)
    for idx, slot in enumerate(survivors.iter_rows(named=True), start=1):
        symbol = slot["symbol"]
        magic_time = slot["magic_time"]
        duration = slot["or_duration_min"]
        pattern_id = slot["pattern_id"]
        direction = slot["direction"]

        trig_slot = triggers.filter(
            (pl.col("symbol") == symbol)
            & (pl.col("magic_time") == magic_time)
            & (pl.col("or_duration_min") == duration)
            & (pl.col("pattern_id") == pattern_id)
            & (pl.col("direction") == direction)
        )
        if trig_slot.is_empty():
            print(f"[swing] [{idx}/{total}] {symbol} {pattern_id} {direction}: 0 triggers, skip", flush=True)
            continue

        if symbol not in m1_cache:
            print(f"[swing]   loading M1 for {symbol} ...", flush=True)
            m1_cache[symbol] = _load_m1(symbol)
        m1 = m1_cache[symbol]

        span_days = (trig_slot["trigger_ts"].max() - trig_slot["trigger_ts"].min()).days
        span_days = max(span_days, 1)

        slot_t0 = time.time()
        rs = _simulate_swing(trig_slot, symbol, duration, m1)
        metrics = _aggregate_trades(rs, span_days)
        new_rows.append({
            **{k: slot[k] for k in ["symbol", "magic_time", "or_duration_min",
                                      "pattern_id", "direction"]},
            "mode": "SWING",
            "params": "sl=1.0ATR,tp1=2R(25%),tp2=4R(25%),BE,trail_sma20(50%)",
            "sl_atr": 1.0, "sl_or_frac": None, "rr_used": 3.0,
            **metrics,
        })
        slot_secs = time.time() - slot_t0
        elapsed_total = (time.time() - t_total) / 60
        eta = (elapsed_total / idx) * (total - idx)
        print(f"[swing] [{idx}/{total}] {symbol} {pattern_id} {direction}: "
              f"{len(trig_slot):,} triggers, {slot_secs:.0f}s "
              f"(elapsed {elapsed_total:.1f}m, eta {eta:.1f}m) "
              f"PF={metrics['pf']:.2f} WR={metrics['win_rate']*100:.1f}% "
              f"exp={metrics['expectancy_r']:+.2f}R", flush=True)

    new_df = pl.DataFrame(new_rows) if new_rows else pl.DataFrame()
    combined = pl.concat([existing, new_df], how="diagonal_relaxed") if not new_df.is_empty() else existing
    combined.write_parquet(base / "orb_managements_compare.parquet")
    print(f"[swing] wrote {len(combined)} rows ({len(new_rows)} new SWING) to compare parquet", flush=True)


if __name__ == "__main__":
    main()
