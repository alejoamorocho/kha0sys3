"""ORB Phase B: management grid search.

For each Phase A pattern survivor, iterate (entry_mode, sl_atr_mult, tp_rr)
and simulate every historical trigger via orb_management_walker.simulate_trade.
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path

import numpy as np
import polars as pl

from src.application.orb_management_walker import simulate_trade
from src.application.orb_utils import DATA_DIR, REPORTS_DIR
from src.engine.friction_real import friction_r as real_friction_r, load_median_atr


ENTRY_MODES = [
    ("MARKET", 0.0),
    ("STOP_RETEST", 0.25),
    ("STOP_RETEST", 0.5),
    ("LIMIT_PULLBACK", -0.25),
    ("LIMIT_PULLBACK", -0.5),
]
SL_GRID = [0.3, 0.5, 0.7, 1.0]
TP_RR_GRID = [1.0, 1.5, 2.0, 3.0]


@dataclass(frozen=True)
class PhaseBConfig:
    min_pf: float = 1.2
    min_wr: float = 0.5
    min_expectancy_r: float = 0.1
    min_trades_per_year: float = 30.0
    min_rr: float = 1.0
    slippage_r_floor: float = 0.2

    def passes(self, m: dict) -> bool:
        return (
            m["pf"] >= self.min_pf
            and m["win_rate"] > self.min_wr
            and m["expectancy_r"] >= self.min_expectancy_r
            and m["trades_per_year"] >= self.min_trades_per_year
            and m["rr"] >= self.min_rr
        )


def aggregate_trades(trades: pl.DataFrame, span_days: int) -> dict:
    if trades.is_empty():
        return {
            "trades": 0, "trades_per_year": 0.0, "win_rate": 0.0,
            "pf": 0.0, "expectancy_r": 0.0, "max_dd_r": 0.0,
            "sharpe_annualized": 0.0, "rr": 0.0,
        }
    r = trades["realized_r"].to_numpy()
    wins = r[r > 0].sum()
    losses = -r[r < 0].sum()
    pf = float(wins / losses) if losses > 0 else float("inf") if wins > 0 else 0.0
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
        "sharpe_annualized": sharpe,
        "rr": 0.0,
    }


def _entry_price(entry_mode: str, offset_mult: float, trigger_close: float,
                 atr: float, direction: str) -> float:
    if entry_mode == "MARKET":
        return trigger_close
    sign = 1.0 if direction == "LONG" else -1.0
    if entry_mode == "STOP_RETEST":
        return trigger_close + sign * abs(offset_mult) * atr
    if entry_mode == "LIMIT_PULLBACK":
        return trigger_close - sign * abs(offset_mult) * atr
    raise ValueError(f"Unknown entry_mode {entry_mode}")


def _check_fill(entry_price: float, direction: str, entry_mode: str,
                fill_window_min: int, trigger_ts, m1_window: dict):
    if entry_mode == "MARKET":
        return True, trigger_ts
    times = m1_window["times"]
    highs = m1_window["highs"]
    lows = m1_window["lows"]
    n = len(times)
    start = 0
    while start < n and times[start] <= trigger_ts:
        start += 1
    horizon = trigger_ts + timedelta(minutes=fill_window_min)
    for j in range(start, n):
        if times[j] > horizon:
            return False, None
        hi = highs[j]; lo = lows[j]
        if entry_mode == "STOP_RETEST":
            if direction == "LONG" and hi >= entry_price:
                return True, times[j]
            if direction == "SHORT" and lo <= entry_price:
                return True, times[j]
        if entry_mode == "LIMIT_PULLBACK":
            if direction == "LONG" and lo <= entry_price:
                return True, times[j]
            if direction == "SHORT" and hi >= entry_price:
                return True, times[j]
    return False, None


def _simulate_combo(
    triggers: pl.DataFrame,
    symbol: str, or_duration_min: int,
    entry_mode: str, offset_mult: float,
    sl_atr_mult: float, tp_atr_mult: float,
    m1: dict, friction_extra_r: float,
) -> pl.DataFrame:
    median_atr = load_median_atr(symbol)
    friction_pure = real_friction_r(symbol, sl_atr_mult, median_atr)
    friction_eff = friction_pure + friction_extra_r

    max_hold_min = 10 * or_duration_min
    fill_window_min = 5 * or_duration_min

    out_rows = []
    for row in triggers.iter_rows(named=True):
        direction = row["direction"]
        atr = row["atr_at_setup"]
        risk_per_r = 0.5 * atr
        trig_close = row["trigger_close"]
        ep = _entry_price(entry_mode, offset_mult, trig_close, atr, direction)
        sign = 1.0 if direction == "LONG" else -1.0
        tp = ep + sign * tp_atr_mult * atr
        sl = ep - sign * sl_atr_mult * atr
        filled, fill_ts = _check_fill(
            ep, direction, entry_mode, fill_window_min, row["trigger_ts"], m1,
        )
        if not filled:
            continue
        trade = simulate_trade(
            fill_ts=fill_ts, entry=ep, direction=direction,
            tp=tp, sl=sl, max_hold_min=max_hold_min, m1=m1,
            risk_per_r=risk_per_r, friction_r=friction_eff,
        )
        out_rows.append({
            "realized_r": trade["realized_r"],
            "exit_reason": trade["exit_reason"],
            "fill_ts": fill_ts,
            "exit_ts": trade["exit_ts"],
        })
    return pl.DataFrame(out_rows) if out_rows else pl.DataFrame()


def run_phase_b(
    phase_a_path=None, triggers_path=None, out_path=None, cfg=None,
) -> pl.DataFrame:
    cfg = cfg or PhaseBConfig()
    base = Path(REPORTS_DIR)
    phase_a_path = Path(phase_a_path or base / "orb_phase_a.parquet")
    triggers_path = Path(triggers_path or base / "orb_phase_a_triggers.parquet")
    out_path = Path(out_path or base / "orb_phase_b.parquet")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not phase_a_path.exists() or not triggers_path.exists():
        pl.DataFrame().write_parquet(out_path)
        trades_path = out_path.parent / (out_path.stem + "_trades.parquet")
        pl.DataFrame().write_parquet(trades_path)
        return pl.DataFrame()

    phase_a = pl.read_parquet(phase_a_path)
    triggers = pl.read_parquet(triggers_path)
    if phase_a.is_empty() or triggers.is_empty():
        pl.DataFrame().write_parquet(out_path)
        trades_path = out_path.parent / (out_path.stem + "_trades.parquet")
        pl.DataFrame().write_parquet(trades_path)
        return pl.DataFrame()

    survivors: list[dict] = []
    trade_rows: list[dict] = []
    total_slots = len(phase_a)
    t0 = time.time()
    m1_cache: dict[str, dict] = {}
    for slot_idx, slot in enumerate(phase_a.iter_rows(named=True), start=1):
        pct = 100.0 * (slot_idx - 1) / max(total_slots, 1)
        elapsed_min = (time.time() - t0) / 60
        if slot_idx == 1 or slot_idx % 10 == 0 or slot_idx == total_slots:
            eta_min = (elapsed_min / max(slot_idx - 1, 1)) * (total_slots - slot_idx + 1) if slot_idx > 1 else 0
            print(f"[Phase B] [{pct:5.1f}%] slot {slot_idx}/{total_slots} "
                  f"survivors_so_far={len(survivors)} "
                  f"(elapsed {elapsed_min:.1f}m, eta {eta_min:.1f}m)", flush=True)
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
            continue

        if symbol in m1_cache:
            m1 = m1_cache[symbol]
        else:
            m1_df = pl.read_parquet(Path(DATA_DIR) / f"{symbol}_M1.parquet").sort("time")
            m1 = {
                "times": np.array(m1_df["time"].to_list(), dtype="object"),
                "highs": np.asarray(m1_df["high"].to_list(), dtype=float),
                "lows": np.asarray(m1_df["low"].to_list(), dtype=float),
                "closes": np.asarray(m1_df["close"].to_list(), dtype=float),
            }
            m1_cache[symbol] = m1
        span_days = (
            trig_slot["trigger_ts"].max() - trig_slot["trigger_ts"].min()
        ).days
        span_days = max(span_days, 1)

        for entry_mode, offset_mult in ENTRY_MODES:
            for sl_mult in SL_GRID:
                for rr in TP_RR_GRID:
                    tp_mult = sl_mult * rr
                    trades = _simulate_combo(
                        trig_slot, symbol, duration,
                        entry_mode, offset_mult, sl_mult, tp_mult,
                        m1, cfg.slippage_r_floor,
                    )
                    metrics = aggregate_trades(trades, span_days)
                    metrics["rr"] = rr
                    if not cfg.passes(metrics):
                        continue
                    combo_id = (
                        f"{symbol}|{magic_time}|{duration}|{pattern_id}|{direction}|"
                        f"{entry_mode}|{offset_mult}|{sl_mult}|{tp_mult}"
                    )
                    survivors.append({
                        **slot, "entry_mode": entry_mode, "entry_offset_atr": offset_mult,
                        "sl_atr_mult": sl_mult, "tp_atr_mult": tp_mult,
                        "combo_id": combo_id,
                        **metrics,
                    })
                    for t in trades.iter_rows(named=True):
                        trade_rows.append({"combo_id": combo_id, **t})

    elapsed_min = (time.time() - t0) / 60
    print(f"[Phase B] [100.0%] done in {elapsed_min:.1f}m: "
          f"{len(survivors)} survivors, {len(trade_rows)} trades", flush=True)
    out_df = pl.DataFrame(survivors) if survivors else pl.DataFrame()
    out_df.write_parquet(out_path)
    trades_path = out_path.parent / (out_path.stem + "_trades.parquet")
    (pl.DataFrame(trade_rows) if trade_rows else pl.DataFrame()).write_parquet(trades_path)
    return out_df


if __name__ == "__main__":
    df = run_phase_b()
    print(f"Phase B: {len(df)} management survivors")
