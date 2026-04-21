"""Validation metrics for indicator-based strategies.

Pure functions that consume a trade-level Polars DataFrame with at minimum:
    time (datetime), r_multiple (float)
and return scalar or small struct results.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import polars as pl


@dataclass(frozen=True)
class MetricsResult:
    n_trades: int
    wr: float
    expectancy_r: float
    profit_factor: float
    max_dd_r: float
    trades_per_year: float


def compute_metrics(trades: pl.DataFrame) -> MetricsResult:
    if len(trades) == 0:
        return MetricsResult(0, 0.0, 0.0, 0.0, 0.0, 0.0)
    r = trades["r_multiple"].to_numpy()
    wins = r[r > 0]
    losses = r[r < 0]
    wr = float(len(wins) / len(r))
    expectancy = float(r.mean())
    pf = float(wins.sum() / -losses.sum()) if len(losses) > 0 and losses.sum() != 0 else float("inf")
    cum = np.cumsum(r)
    peak = np.maximum.accumulate(cum)
    dd = peak - cum
    max_dd = float(dd.max()) if len(dd) > 0 else 0.0
    span_days = (trades["time"].max() - trades["time"].min()).total_seconds() / 86400
    tpy = float(len(r) / (span_days / 365.25)) if span_days > 0 else 0.0
    return MetricsResult(len(r), wr, expectancy, pf, max_dd, tpy)


def walk_forward_wr(trades: pl.DataFrame, is_months: int, oos_months: int) -> float:
    """Rolling WF: compute mean(WR_oos / WR_is) across rolling windows.
    Returns 1.0 if no valid windows."""
    if len(trades) < 20:
        return 1.0
    trades = trades.sort("time")
    t0 = trades["time"].min()
    t_end = trades["time"].max()
    ratios = []
    cursor = t0
    from datetime import timedelta
    is_delta = timedelta(days=30 * is_months)
    oos_delta = timedelta(days=30 * oos_months)
    while cursor + is_delta + oos_delta <= t_end:
        is_slice = trades.filter(
            (pl.col("time") >= cursor) & (pl.col("time") < cursor + is_delta)
        )
        oos_slice = trades.filter(
            (pl.col("time") >= cursor + is_delta) &
            (pl.col("time") < cursor + is_delta + oos_delta)
        )
        if len(is_slice) >= 5 and len(oos_slice) >= 5:
            wr_is = (is_slice["r_multiple"] > 0).sum() / len(is_slice)
            wr_oos = (oos_slice["r_multiple"] > 0).sum() / len(oos_slice)
            if wr_is > 0:
                ratios.append(wr_oos / wr_is)
        cursor += oos_delta  # roll forward
    return float(np.mean(ratios)) if ratios else 1.0


def monte_carlo_ruin(trades: pl.DataFrame, risk_pct: float, initial_balance: float,
                     n_sims: int = 1000, n_steps: int = 500, seed: int = 42) -> float:
    """Bootstrap trades with replacement, compound balance. Ruin = balance <= 50% initial."""
    if len(trades) == 0:
        return 1.0
    r = trades["r_multiple"].to_numpy()
    rng = np.random.default_rng(seed)
    ruin_count = 0
    ruin_threshold = initial_balance * 0.5
    for _ in range(n_sims):
        balance = initial_balance
        sampled = rng.choice(r, size=n_steps, replace=True)
        for rm in sampled:
            balance *= (1.0 + risk_pct * rm)
            if balance <= ruin_threshold:
                ruin_count += 1
                break
    return ruin_count / n_sims


def decay_slope_ratio(trades: pl.DataFrame, last_months: int = 6) -> float:
    """Ratio of (mean R in last N months) / (global mean R).
    Values >= 1.0 mean improving, < 0.7 mean degrading."""
    if len(trades) < 20:
        return 1.0
    trades = trades.sort("time")
    t_end = trades["time"].max()
    from datetime import timedelta
    cutoff = t_end - timedelta(days=30 * last_months)
    recent = trades.filter(pl.col("time") >= cutoff)
    if len(recent) < 5:
        return 1.0
    global_mean = trades["r_multiple"].mean()
    recent_mean = recent["r_multiple"].mean()
    if global_mean <= 0:
        return 0.0
    return float(recent_mean / global_mean)
