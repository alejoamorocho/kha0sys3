"""ORB Phase D: Optuna refinement for FUERTE/ACEPTABLE survivors.

Per-strategy TPE study tuning continuous (sl_atr_mult, rr, entry_offset_atr,
or_atr_ratio_min, or_atr_ratio_max). Objective: PF_OOS with penalties for
low TPY and high MC ruin. Constraint tp_atr_mult = sl * rr with rr >= 1.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import polars as pl

try:
    import optuna
    from optuna.samplers import TPESampler
    from optuna.pruners import MedianPruner
except ImportError as e:
    raise RuntimeError("optuna required for Phase D") from e

from src.application.orb_management_walker import simulate_trade
from src.application.orb_utils import DATA_DIR, REPORTS_DIR
from src.engine.friction_real import friction_r as real_friction_r, load_median_atr
from src.engine.k3m1_robustness import mc_ruin


@dataclass(frozen=True)
class OptunaConfig:
    trials: int = 200
    is_frac: float = 0.6
    tpy_floor: float = 30.0
    mc_ruin_cap: float = 0.05
    seed: int = 42


def _filter_triggers_by_state_thresholds(
    triggers: pl.DataFrame, or_atr_min: float, or_atr_max: float,
) -> pl.DataFrame:
    if triggers.is_empty():
        return triggers
    if "or_atr_ratio_at_trigger" in triggers.columns:
        return triggers.filter(
            (pl.col("or_atr_ratio_at_trigger") >= or_atr_min)
            & (pl.col("or_atr_ratio_at_trigger") <= or_atr_max)
        )
    return triggers


def _simulate_with_params(
    triggers: pl.DataFrame, m1: dict, symbol: str, or_duration_min: int,
    sl_atr_mult: float, tp_atr_mult: float, entry_offset_atr: float,
    friction_extra_r: float,
) -> pl.DataFrame:
    from src.engine.orb_management_grid import _entry_price, _check_fill
    if triggers.is_empty():
        return pl.DataFrame()
    median_atr = load_median_atr(symbol)
    friction_pure = real_friction_r(symbol, sl_atr_mult, median_atr)
    friction_eff = friction_pure + friction_extra_r
    max_hold_min = 10 * or_duration_min
    fill_window_min = 5 * or_duration_min

    if entry_offset_atr > 0:
        entry_mode = "STOP_RETEST"
    elif entry_offset_atr < 0:
        entry_mode = "LIMIT_PULLBACK"
    else:
        entry_mode = "MARKET"

    rows = []
    for row in triggers.iter_rows(named=True):
        direction = row["direction"]
        atr = row["atr_at_setup"]
        risk_per_r = 0.5 * atr
        trig_close = row["trigger_close"]
        ep = _entry_price(entry_mode, entry_offset_atr, trig_close, atr, direction)
        sign = 1.0 if direction == "LONG" else -1.0
        tp = ep + sign * tp_atr_mult * atr
        sl = ep - sign * sl_atr_mult * atr
        filled, fill_ts = _check_fill(ep, direction, entry_mode, fill_window_min,
                                      row["trigger_ts"], m1)
        if not filled:
            continue
        trade = simulate_trade(
            fill_ts=fill_ts, entry=ep, direction=direction,
            tp=tp, sl=sl, max_hold_min=max_hold_min, m1=m1,
            risk_per_r=risk_per_r, friction_r=friction_eff,
        )
        rows.append({"realized_r": trade["realized_r"]})
    return pl.DataFrame(rows) if rows else pl.DataFrame()


def build_objective(slot: dict, triggers: pl.DataFrame, m1: dict, span_days: int,
                    cfg: OptunaConfig):
    symbol = slot["symbol"]
    or_duration = slot["or_duration_min"]
    span_years = max(span_days / 365.25, 1e-9)

    def objective(trial):
        sl = trial.suggest_float("sl_atr_mult", 0.2, 1.2)
        rr = trial.suggest_float("rr", 1.0, 4.0)
        offset = trial.suggest_float("entry_offset_atr", -0.5, 0.5)
        or_min = trial.suggest_float("or_atr_ratio_min", 0.0, 0.4)
        or_max = trial.suggest_float("or_atr_ratio_max", 0.5, 1.5)
        if or_max <= or_min:
            return 0.0
        tp = sl * rr
        filtered = _filter_triggers_by_state_thresholds(triggers, or_min, or_max)
        trades = _simulate_with_params(
            filtered, m1, symbol, or_duration,
            sl, tp, offset, friction_extra_r=0.2,
        )
        if trades.is_empty():
            return 0.0
        r = trades["realized_r"].to_numpy()
        cut = int(len(r) * cfg.is_frac)
        oos = r[cut:]
        if len(oos) == 0:
            return 0.0
        wins = oos[oos > 0].sum(); losses = -oos[oos < 0].sum()
        pf_oos = float(wins / losses) if losses > 0 else (5.0 if wins > 0 else 0.0)
        tpy = len(r) / span_years
        penalty = 1.0
        if tpy < cfg.tpy_floor:
            penalty *= 0.5
        mc = mc_ruin(r)
        if mc["ruin_pct"] / 100.0 > cfg.mc_ruin_cap:
            penalty *= 0.3
        return pf_oos * penalty

    return objective


def run_phase_d(
    robustness_path=None, triggers_path=None, out_path=None, cfg=None,
) -> pl.DataFrame:
    cfg = cfg or OptunaConfig()
    base = Path(REPORTS_DIR)
    robustness_path = Path(robustness_path or base / "orb_robustness.parquet")
    triggers_path = Path(triggers_path or base / "orb_phase_a_triggers.parquet")
    out_path = Path(out_path or base / "orb_optuna_results.parquet")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not robustness_path.exists():
        pl.DataFrame().write_parquet(out_path)
        return pl.DataFrame()

    rob = pl.read_parquet(robustness_path)
    if rob.is_empty():
        pl.DataFrame().write_parquet(out_path)
        return pl.DataFrame()

    triggers = pl.read_parquet(triggers_path) if triggers_path.exists() else pl.DataFrame()

    survivors = rob.filter(pl.col("classification").is_in(["FUERTE", "ACEPTABLE"]))
    out_rows: list[dict] = []
    for slot in survivors.iter_rows(named=True):
        trig_slot = triggers.filter(
            (pl.col("symbol") == slot["symbol"])
            & (pl.col("magic_time") == slot["magic_time"])
            & (pl.col("or_duration_min") == slot["or_duration_min"])
            & (pl.col("pattern_id") == slot["pattern_id"])
            & (pl.col("direction") == slot["direction"])
        )
        if trig_slot.is_empty():
            continue
        m1_df = pl.read_parquet(Path(DATA_DIR) / f"{slot['symbol']}_M1.parquet").sort("time")
        m1 = {
            "times": np.array(m1_df["time"].to_list(), dtype="object"),
            "highs": np.asarray(m1_df["high"].to_list(), dtype=float),
            "lows": np.asarray(m1_df["low"].to_list(), dtype=float),
            "closes": np.asarray(m1_df["close"].to_list(), dtype=float),
        }
        span_days = (trig_slot["trigger_ts"].max() - trig_slot["trigger_ts"].min()).days
        study = optuna.create_study(
            direction="maximize",
            sampler=TPESampler(seed=cfg.seed),
            pruner=MedianPruner(n_warmup_steps=20),
        )
        study.optimize(
            build_objective(slot, trig_slot, m1, max(span_days, 1), cfg),
            n_trials=cfg.trials, show_progress_bar=False,
        )
        out_rows.append({
            **slot,
            "best_value": study.best_value,
            **{f"best_{k}": v for k, v in study.best_params.items()},
        })

    out = pl.DataFrame(out_rows) if out_rows else pl.DataFrame()
    out.write_parquet(out_path)
    return out


if __name__ == "__main__":
    df = run_phase_d()
    print(f"Phase D: {len(df)} Optuna-refined strategies")
