"""Test 3 management modes on the patterns that survived Phase A gates.

Inputs:
  reports/orb/orb_phase_a.parquet         (37 survivors)
  reports/orb/orb_phase_a_triggers.parquet  (~3.5M raw triggers)
  data/enriched_math_tf/<SYM>_M1.parquet  (per symbol, cached)

Modes:
  1. ATR — SL = sl_atr × ATR, TP = sl × rr ; grid (4 sl × 4 rr = 16)
  2. OR-FIXED — SL = sl_or × OR_width, TP = sl × rr ; grid (3 sl × 4 rr = 12)
  3. DOC — partial exits + BE + time-stop (no grid, single config)

Output:
  reports/orb/orb_managements_compare.parquet
  reports/orb/ORB_Managements_Compare.md
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

from src.application.orb_management_modes import (
    _trade_atr_or_fixed,
    simulate_doc_partial,
)
from src.application.orb_utils import DATA_DIR, REPORTS_DIR
from src.engine.friction_real import friction_r as real_friction_r, load_median_atr


ATR_SL_GRID = [0.3, 0.5, 0.7, 1.0]
ATR_RR_GRID = [1.0, 1.5, 2.0, 3.0]

OR_SL_GRID = [0.5, 1.0, 1.5]  # fraction of or_width
OR_RR_GRID = [1.0, 1.5, 2.0, 3.0]

SLIPPAGE_R_FLOOR = 0.2


def _aggregate_trades(realized_r: list[float], span_days: int, rr: float | None) -> dict:
    if not realized_r:
        return {
            "trades": 0, "trades_per_year": 0.0, "win_rate": 0.0,
            "pf": 0.0, "expectancy_r": 0.0, "max_dd_r": 0.0,
            "sharpe": 0.0, "rr": rr if rr is not None else 0.0,
            "sum_r": 0.0,
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
        "rr": rr if rr is not None else 0.0,
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


def _simulate_mode_atr(triggers: pl.DataFrame, symbol: str, or_duration: int,
                       m1: dict, sl_atr: float, rr: float) -> list[float]:
    median_atr = load_median_atr(symbol)
    friction_eff = real_friction_r(symbol, sl_atr, median_atr) + SLIPPAGE_R_FLOOR
    max_hold_min = 10 * or_duration

    out = []
    for row in triggers.iter_rows(named=True):
        atr = row["atr_at_setup"]
        risk_per_r = 0.5 * atr
        entry = row["trigger_close"]
        sign = 1.0 if row["direction"] == "LONG" else -1.0
        sl_dist = sl_atr * atr
        tp_dist = sl_dist * rr
        tp = entry + sign * tp_dist
        sl = entry - sign * sl_dist
        trade = _trade_atr_or_fixed(
            fill_ts=row["trigger_ts"], entry=entry, direction=row["direction"],
            sl=sl, tp=tp, max_hold_min=max_hold_min, m1=m1,
            risk_per_r=risk_per_r, friction_r=friction_eff,
        )
        if trade["exit_reason"] != "NO_BARS":
            out.append(trade["realized_r"])
    return out


def _simulate_mode_or(triggers: pl.DataFrame, symbol: str, or_duration: int,
                      m1: dict, sl_or_frac: float, rr: float) -> list[float]:
    # Friction uses sl_atr equivalent for the friction formula. We use the OR-equivalent
    # ATR multiple by computing avg OR-width / ATR ratio for this trigger set.
    median_atr = load_median_atr(symbol)
    # Use a representative sl_atr_mult = sl_or_frac × median or_atr_ratio (0.5 typical).
    # This is a simplification: friction_r expects atr-mult-based SL units.
    avg_or_atr_ratio = float(triggers["or_atr_ratio_at_trigger"].mean() or 0.5)
    equiv_sl_atr = sl_or_frac * avg_or_atr_ratio
    friction_eff = real_friction_r(symbol, equiv_sl_atr, median_atr) + SLIPPAGE_R_FLOOR
    max_hold_min = 10 * or_duration

    out = []
    for row in triggers.iter_rows(named=True):
        atr = row["atr_at_setup"]
        or_w = row["or_width"]
        risk_per_r = 0.5 * atr
        entry = row["trigger_close"]
        sign = 1.0 if row["direction"] == "LONG" else -1.0
        sl_dist = sl_or_frac * or_w
        tp_dist = sl_dist * rr
        tp = entry + sign * tp_dist
        sl = entry - sign * sl_dist
        trade = _trade_atr_or_fixed(
            fill_ts=row["trigger_ts"], entry=entry, direction=row["direction"],
            sl=sl, tp=tp, max_hold_min=max_hold_min, m1=m1,
            risk_per_r=risk_per_r, friction_r=friction_eff,
        )
        if trade["exit_reason"] != "NO_BARS":
            out.append(trade["realized_r"])
    return out


def _simulate_mode_doc(triggers: pl.DataFrame, symbol: str, or_duration: int,
                       m1: dict) -> list[float]:
    """Doc-style: SL = 1.0×OR, TP1 = 1.0×OR (50%), TP2 = 2.0×OR (50%), BE after TP1,
    mid-time check at max_hold/2."""
    median_atr = load_median_atr(symbol)
    avg_or_atr_ratio = float(triggers["or_atr_ratio_at_trigger"].mean() or 0.5)
    equiv_sl_atr = 1.0 * avg_or_atr_ratio
    friction_eff = real_friction_r(symbol, equiv_sl_atr, median_atr) + SLIPPAGE_R_FLOOR
    max_hold_min = 10 * or_duration

    out = []
    for row in triggers.iter_rows(named=True):
        atr = row["atr_at_setup"]
        or_w = row["or_width"]
        risk_per_r = 0.5 * atr
        result = simulate_doc_partial(
            fill_ts=row["trigger_ts"], entry=row["trigger_close"],
            direction=row["direction"],
            sl_distance=1.0 * or_w,
            tp1_distance=1.0 * or_w,
            tp2_distance=2.0 * or_w,
            max_hold_min=max_hold_min, m1=m1,
            risk_per_r=risk_per_r, friction_r=friction_eff,
            tp1_fraction=0.5, midpoint_mfe_min_r=0.5,
        )
        if result["exit_reason"] != "NO_BARS":
            out.append(result["realized_r"])
    return out


def run():
    base = Path(REPORTS_DIR)
    print("[managements] loading survivors + triggers ...", flush=True)
    survivors = pl.read_parquet(base / "orb_phase_a.parquet")
    triggers = pl.read_parquet(base / "orb_phase_a_triggers.parquet")
    print(f"[managements] {len(survivors)} survivors, {len(triggers):,} triggers", flush=True)

    rows: list[dict] = []
    m1_cache: dict[str, dict] = {}
    t_total = time.time()
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
            print(f"[managements] [{idx}/{len(survivors)}] {symbol} {pattern_id} {direction}: 0 triggers, skip")
            continue

        if symbol not in m1_cache:
            print(f"[managements]   loading M1 for {symbol} ...", flush=True)
            m1_cache[symbol] = _load_m1(symbol)
        m1 = m1_cache[symbol]

        span_days = (trig_slot["trigger_ts"].max() - trig_slot["trigger_ts"].min()).days
        span_days = max(span_days, 1)
        slot_t0 = time.time()

        # Mode 1: ATR grid
        for sl_atr in ATR_SL_GRID:
            for rr in ATR_RR_GRID:
                rs = _simulate_mode_atr(trig_slot, symbol, duration, m1, sl_atr, rr)
                metrics = _aggregate_trades(rs, span_days, rr)
                rows.append({
                    **{k: slot[k] for k in ["symbol", "magic_time", "or_duration_min",
                                              "pattern_id", "direction"]},
                    "mode": "ATR",
                    "params": f"sl_atr={sl_atr},rr={rr}",
                    "sl_atr": sl_atr, "sl_or_frac": None, "rr_used": rr,
                    **metrics,
                })

        # Mode 2: OR-fixed grid
        for sl_or in OR_SL_GRID:
            for rr in OR_RR_GRID:
                rs = _simulate_mode_or(trig_slot, symbol, duration, m1, sl_or, rr)
                metrics = _aggregate_trades(rs, span_days, rr)
                rows.append({
                    **{k: slot[k] for k in ["symbol", "magic_time", "or_duration_min",
                                              "pattern_id", "direction"]},
                    "mode": "OR_FIXED",
                    "params": f"sl_or={sl_or},rr={rr}",
                    "sl_atr": None, "sl_or_frac": sl_or, "rr_used": rr,
                    **metrics,
                })

        # Mode 3: DOC (single config)
        rs = _simulate_mode_doc(trig_slot, symbol, duration, m1)
        metrics = _aggregate_trades(rs, span_days, None)
        rows.append({
            **{k: slot[k] for k in ["symbol", "magic_time", "or_duration_min",
                                      "pattern_id", "direction"]},
            "mode": "DOC",
            "params": "sl=1.0OR,tp1=1.0OR(50%),tp2=2.0OR(50%),BE,timestop@1/2,mfe<0.5R",
            "sl_atr": None, "sl_or_frac": 1.0, "rr_used": 2.0,
            **metrics,
        })

        slot_secs = time.time() - slot_t0
        elapsed_total = (time.time() - t_total) / 60
        eta = (elapsed_total / idx) * (len(survivors) - idx)
        print(f"[managements] [{idx}/{len(survivors)}] {symbol} {pattern_id} {direction}: "
              f"{len(trig_slot):,} triggers, {slot_secs:.0f}s "
              f"(elapsed {elapsed_total:.1f}m, eta {eta:.1f}m)", flush=True)

    out = pl.DataFrame(rows)
    out_path = base / "orb_managements_compare.parquet"
    out.write_parquet(out_path)
    print(f"[managements] wrote {len(out)} rows to {out_path.name}")

    # Build report
    md_path = base / "ORB_Managements_Compare.md"
    _write_report(out, md_path)
    print(f"[managements] wrote {md_path.name}")


def _fmt(v, kind=""):
    if v is None:
        return "—"
    if isinstance(v, float):
        if kind == "pct":
            return f"{v*100:.1f}%"
        if kind == "r":
            return f"{v:+.2f}R"
        return f"{v:.2f}"
    return str(v)


def _write_report(df: pl.DataFrame, out_path: Path) -> None:
    lines: list[str] = []
    lines.append("# ORB Managements Comparison (37 Phase A survivors)\n\n")
    lines.append(f"**Total rows:** {len(df)}\n\n")
    lines.append("Modes: **ATR** (sl=sl_atr×ATR, tp=sl×rr), "
                 "**OR_FIXED** (sl=sl_or×or_width, tp=sl×rr), "
                 "**DOC** (sl=1.0×OR, tp1=1.0×OR @ 50% + BE, tp2=2.0×OR @ 50%, time-stop)\n\n")

    # 1. Best management per pattern
    lines.append("## 1. Best management per pattern (by PF, min 30 trades)\n\n")
    filtered = df.filter(pl.col("trades") >= 30)
    if filtered.is_empty():
        lines.append("_No mode reached ≥30 trades for any pattern._\n\n")
    else:
        slot_cols = ["symbol", "magic_time", "or_duration_min", "pattern_id", "direction"]
        ranked = filtered.with_columns(
            pl.col("pf").rank(method="dense", descending=True).over(slot_cols).alias("_rk")
        )
        best = ranked.filter(pl.col("_rk") == 1).drop("_rk")
        cols = ["symbol", "magic_time", "or_duration_min", "event_type" if "event_type" in best.columns else "pattern_id",
                "direction", "mode", "params", "trades", "trades_per_year",
                "win_rate", "pf", "expectancy_r", "sum_r", "max_dd_r"]
        cols = [c for c in cols if c in best.columns]
        lines.append("| " + " | ".join(cols) + " |\n")
        lines.append("| " + " | ".join("---" for _ in cols) + " |\n")
        for row in best.sort("pf", descending=True).iter_rows(named=True):
            cells = []
            for c in cols:
                v = row[c]
                if c == "win_rate":
                    cells.append(_fmt(v, "pct"))
                elif c in ("expectancy_r", "sum_r", "max_dd_r"):
                    cells.append(_fmt(v, "r"))
                else:
                    cells.append(_fmt(v))
            lines.append("| " + " | ".join(cells) + " |\n")

    # 2. Headline: mean PF / WR / expectancy per mode (across all patterns ≥30 trades)
    lines.append("\n## 2. Headline by mode (across all patterns with ≥30 trades)\n\n")
    if not filtered.is_empty():
        mode_summary = (
            filtered.group_by("mode").agg([
                pl.len().alias("n_configs"),
                pl.col("pf").median().alias("pf_median"),
                pl.col("win_rate").median().alias("wr_median"),
                pl.col("expectancy_r").median().alias("exp_median"),
                pl.col("sum_r").median().alias("sum_r_median"),
                pl.col("pf").max().alias("pf_max"),
            ])
            .sort("pf_median", descending=True)
        )
        lines.append("| mode | n configs | PF median | WR median | exp_r median | sum_R median | PF max |\n")
        lines.append("|---|---|---|---|---|---|---|\n")
        for row in mode_summary.iter_rows(named=True):
            lines.append(f"| {row['mode']} | {row['n_configs']} | "
                         f"{_fmt(row['pf_median'])} | {_fmt(row['wr_median'], 'pct')} | "
                         f"{_fmt(row['exp_median'], 'r')} | {_fmt(row['sum_r_median'], 'r')} | "
                         f"{_fmt(row['pf_max'])} |\n")

    # 3. Top 30 (mode, params) by PF across all symbols
    lines.append("\n## 3. Top 30 (mode + params) configurations across all symbols (≥30 trades)\n\n")
    if not filtered.is_empty():
        top = filtered.sort("pf", descending=True).head(30)
        cols = ["symbol", "magic_time", "or_duration_min", "pattern_id", "direction",
                "mode", "params", "trades", "win_rate", "pf", "expectancy_r", "sum_r"]
        cols = [c for c in cols if c in top.columns]
        lines.append("| " + " | ".join(cols) + " |\n")
        lines.append("| " + " | ".join("---" for _ in cols) + " |\n")
        for row in top.iter_rows(named=True):
            cells = []
            for c in cols:
                v = row[c]
                if c == "win_rate":
                    cells.append(_fmt(v, "pct"))
                elif c in ("expectancy_r", "sum_r"):
                    cells.append(_fmt(v, "r"))
                else:
                    cells.append(_fmt(v))
            lines.append("| " + " | ".join(cells) + " |\n")

    lines.append("\n## 4. Interpretación\n\n")
    lines.append("- **trades**: nº de operaciones simuladas (más es mejor para significancia)\n")
    lines.append("- **PF (profit factor)**: suma de ganancias / suma de pérdidas. >1.5 buen; >2.0 muy bueno\n")
    lines.append("- **WR**: % de trades con realized_r > 0\n")
    lines.append("- **expectancy_r**: R promedio por trade. Edge real está aquí\n")
    lines.append("- **sum_R**: R acumulado neto (incluye fricción)\n")
    lines.append("- **DOC** tiene RR efectivo 1.5 (porque promedia TP1=1R con TP2=2R al 50% cada uno), "
                 "pero con BE shift después de TP1 el riesgo neto efectivo baja\n\n")

    out_path.write_text("".join(lines), encoding="utf-8")


if __name__ == "__main__":
    run()
