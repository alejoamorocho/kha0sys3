"""ORB Phase A: pattern + edge discovery.

Pipeline per (symbol, magic_time, or_duration, direction):
  1. Load M15 enriched parquet + M1 enriched parquet
  2. Apply DataEnricher.enrich_with_daily_context + enrich_with_opening_range
  3. Add state buckets via orb_patterns.add_state_columns
  4. For each valid day: build pattern_id, run detect_events_for_day on M1
  5. For each trigger: compute mfe_mae_walk -> R-units
  6. Aggregate by (pattern_id, direction): count, p25/p50/p75 MFE/MAE, edge_score
  7. Filter by Phase A gates

Output: reports/orb/orb_phase_a.parquet
"""
from __future__ import annotations

import bisect
import multiprocessing as mp
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import polars as pl

# Ensure project root is on sys.path so worker subprocesses can re-import
# this module on Windows (spawn start method).
_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)
_existing_pp = os.environ.get("PYTHONPATH", "")
if _PROJECT_ROOT not in _existing_pp.split(os.pathsep):
    os.environ["PYTHONPATH"] = (
        _PROJECT_ROOT + (os.pathsep + _existing_pp if _existing_pp else "")
    )

from src.application.calculators import DataEnricher
from src.application.orb_edge_metrics import mfe_mae_walk
from src.application.orb_patterns import add_state_columns, detect_events_for_day
from src.application.orb_utils import (
    DATA_DIR, MAGIC_TIMES, OR_DURATIONS, REPORTS_DIR, SYMBOLS_V1,
)


@dataclass(frozen=True)
class PhaseAConfig:
    # V1 exploratory gates: loosened from initial conservative values to
    # surface whatever edge exists in the 14-symbol universe. Tightened
    # in V2 once we see the distribution of edge scores.
    min_count_per_year: float = 30.0
    min_edge_score_r: float = 0.15
    min_p50_mfe_r: float = 0.5
    max_p50_mae_r: float = 2.0
    horizon_min: int = 240  # 4h forward window for MFE/MAE
    risk_atr_mult: float = 0.5


def _r_unit_columns(df: pl.DataFrame, risk_atr_mult: float) -> pl.DataFrame:
    r = pl.col("atr_at_setup") * risk_atr_mult
    return df.with_columns([
        (pl.col("mfe_long") / r).alias("mfe_long_r"),
        (pl.col("mae_long") / r).alias("mae_long_r"),
        (pl.col("mfe_short") / r).alias("mfe_short_r"),
        (pl.col("mae_short") / r).alias("mae_short_r"),
    ])


def aggregate_edge_per_pattern(
    triggers: pl.DataFrame,
    span_days: int,
    cfg: PhaseAConfig,
) -> pl.DataFrame:
    """Aggregate trigger rows into per-(pattern_id, direction) edge stats and filter."""
    if triggers.is_empty():
        return pl.DataFrame()

    span_years = max(span_days / 365.25, 1e-9)

    long_df = (
        triggers.filter(pl.col("direction") == "LONG")
        .group_by("pattern_id")
        .agg([
            pl.len().alias("count"),
            pl.col("mfe_long_r").quantile(0.25).alias("p25_mfe_r"),
            pl.col("mfe_long_r").quantile(0.50).alias("p50_mfe_r"),
            pl.col("mfe_long_r").quantile(0.75).alias("p75_mfe_r"),
            pl.col("mae_long_r").quantile(0.25).alias("p25_mae_r"),
            pl.col("mae_long_r").quantile(0.50).alias("p50_mae_r"),
            pl.col("mae_long_r").quantile(0.75).alias("p75_mae_r"),
            pl.col("mfe_long_r").mean().alias("e_mfe_r"),
            pl.col("mae_long_r").mean().alias("e_mae_r"),
        ])
        .with_columns(pl.lit("LONG").alias("direction"))
    )
    short_df = (
        triggers.filter(pl.col("direction") == "SHORT")
        .group_by("pattern_id")
        .agg([
            pl.len().alias("count"),
            pl.col("mfe_short_r").quantile(0.25).alias("p25_mfe_r"),
            pl.col("mfe_short_r").quantile(0.50).alias("p50_mfe_r"),
            pl.col("mfe_short_r").quantile(0.75).alias("p75_mfe_r"),
            pl.col("mae_short_r").quantile(0.25).alias("p25_mae_r"),
            pl.col("mae_short_r").quantile(0.50).alias("p50_mae_r"),
            pl.col("mae_short_r").quantile(0.75).alias("p75_mae_r"),
            pl.col("mfe_short_r").mean().alias("e_mfe_r"),
            pl.col("mae_short_r").mean().alias("e_mae_r"),
        ])
        .with_columns(pl.lit("SHORT").alias("direction"))
    )

    agg = pl.concat([long_df, short_df]).with_columns([
        (pl.col("count") / span_years).alias("count_per_year"),
        (pl.col("p50_mfe_r") - pl.col("p50_mae_r")).alias("edge_score"),
    ])

    return agg.filter(
        (pl.col("count_per_year") >= cfg.min_count_per_year)
        & (pl.col("edge_score") >= cfg.min_edge_score_r)
        & (pl.col("p50_mfe_r") >= cfg.min_p50_mfe_r)
        & (pl.col("p50_mae_r") <= cfg.max_p50_mae_r)
    )


def _build_pattern_id(event_type, or_position, or_atr_bucket, pd_or_bucket) -> str:
    parts = [event_type, or_position or "NULL", or_atr_bucket or "NULL", pd_or_bucket or "NULL"]
    return "_".join(parts)


def _load_enriched(symbol: str) -> tuple[pl.DataFrame, pl.DataFrame]:
    data = Path(DATA_DIR)
    m15 = pl.read_parquet(data / f"{symbol}_M15.parquet")
    m1 = pl.read_parquet(data / f"{symbol}_M1.parquet")
    return m15, m1


def _m1_to_arrays(m1: pl.DataFrame) -> dict:
    """Convert sorted M1 Polars DataFrame to numpy arrays once per symbol.

    Hoisted out of _scan_combo because converting millions of rows 16x
    (per magic_time × duration combo) was making Phase A effectively
    single-threaded. Now we do this exactly once per symbol.
    """
    m1_sorted = m1.sort("time")
    m1_times = m1_sorted["time"].to_list()
    return {
        "times_list": m1_times,
        "times": np.array(m1_times, dtype="object"),
        "highs": np.asarray(m1_sorted["high"].to_list(), dtype=float),
        "lows": np.asarray(m1_sorted["low"].to_list(), dtype=float),
        "closes": np.asarray(m1_sorted["close"].to_list(), dtype=float),
    }


def _scan_combo(
    symbol: str, magic_time: str, duration: int,
    m15: pl.DataFrame, m1_arr: dict, cfg: PhaseAConfig,
) -> tuple[pl.DataFrame, int]:
    """Return trigger DataFrame and span_days for this combo.

    `m1_arr` is the dict returned by `_m1_to_arrays(m1)` for this symbol.
    """
    pd_start, pd_end = "00:00", "23:59"
    enriched = DataEnricher.enrich_with_daily_context(m15, pd_start, pd_end)
    enriched_or = DataEnricher.enrich_with_opening_range(enriched, magic_time, duration)
    enriched_or = add_state_columns(enriched_or)

    per_day = (
        enriched_or.filter(pl.col("is_post_or"))
        .sort("time")
        .group_by("trade_date")
        .agg([
            pl.col("time").first().alias("or_close_ts"),
            pl.col("or_high").first(),
            pl.col("or_low").first(),
            pl.col("pd_mid").first(),
            pl.col("pd_close").first(),
            pl.col("pd_or_high").first(),
            pl.col("pd_or_low").first(),
            pl.col("or_position_vs_pd").first().alias("or_position"),
            pl.col("or_atr_bucket").first(),
            pl.col("pd_or_overlap_bucket").first().alias("pd_or_bucket"),
            pl.col("atr_14").first().alias("atr_at_setup"),
        ])
        .filter(pl.col("atr_at_setup").is_not_null() & (pl.col("atr_at_setup") > 0))
        .filter(pl.col("or_high").is_not_null() & pl.col("or_low").is_not_null())
        .sort("or_close_ts")
    )

    if per_day.is_empty():
        return pl.DataFrame(), 0

    m1_times = m1_arr["times_list"]
    m1_highs = m1_arr["highs"]
    m1_lows = m1_arr["lows"]
    m1_closes = m1_arr["closes"]
    m1_times_arr = m1_arr["times"]

    triggers: list[dict] = []
    for row in per_day.iter_rows(named=True):
        or_close_ts = row["or_close_ts"]
        start_idx = bisect.bisect_right(m1_times, or_close_ts)
        end_idx = start_idx
        while end_idx < len(m1_times) and m1_times[end_idx].date() == or_close_ts.date():
            end_idx += 1
        day_slice = {
            "times": m1_times_arr[start_idx:end_idx],
            "highs": m1_highs[start_idx:end_idx],
            "lows": m1_lows[start_idx:end_idx],
            "closes": m1_closes[start_idx:end_idx],
        }
        events = detect_events_for_day(
            or_close_ts=or_close_ts,
            or_high=row["or_high"], or_low=row["or_low"],
            pd_mid=row["pd_mid"], pd_close=row["pd_close"],
            pd_or_high=row["pd_or_high"], pd_or_low=row["pd_or_low"],
            atr_at_setup=row["atr_at_setup"], m1=day_slice,
        )
        for ev in events:
            pid = _build_pattern_id(
                ev["event_type"], row["or_position"],
                row["or_atr_bucket"], row["pd_or_bucket"],
            )
            mfe = mfe_mae_walk(
                trigger_ts=ev["trigger_ts"],
                entry=ev["trigger_close"],
                m1={
                    "times": m1_times_arr,
                    "highs": m1_highs,
                    "lows": m1_lows,
                    "closes": m1_closes,
                },
                horizon_min=cfg.horizon_min,
            )
            for direction in ("LONG", "SHORT"):
                triggers.append({
                    "symbol": symbol,
                    "magic_time": magic_time,
                    "or_duration_min": duration,
                    "pattern_id": pid,
                    "event_type": ev["event_type"],
                    "or_position": row["or_position"],
                    "or_atr_bucket": row["or_atr_bucket"],
                    "pd_or_bucket": row["pd_or_bucket"],
                    "direction": direction,
                    "trigger_ts": ev["trigger_ts"],
                    "trigger_close": ev["trigger_close"],
                    "atr_at_setup": ev["atr_at_setup"],
                    "mfe_long": mfe["mfe_long"],
                    "mae_long": mfe["mae_long"],
                    "mfe_short": mfe["mfe_short"],
                    "mae_short": mfe["mae_short"],
                })

    if not triggers:
        return pl.DataFrame(), 0
    trig_df = _r_unit_columns(pl.DataFrame(triggers), cfg.risk_atr_mult)
    span_days = (
        per_day["or_close_ts"].max() - per_day["or_close_ts"].min()
    ).days
    return trig_df, max(span_days, 1)


def _process_one_symbol(args):
    """Worker entry point: scan all (magic_time × duration) combos for one symbol.

    Must be top-level (picklable). Returns
    (symbol, agg_df, triggers_df, summary_str).
    """
    symbol, cfg, magic_times, or_durations = args
    # Limit each worker's internal threading so 6 workers x N threads doesn't
    # oversubscribe a 32-core machine.
    os.environ.setdefault("POLARS_MAX_THREADS", "4")
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")

    t0 = time.time()
    try:
        m15, m1 = _load_enriched(symbol)
    except FileNotFoundError:
        return symbol, pl.DataFrame(), pl.DataFrame(), "MISSING_DATA"

    m1_arr = _m1_to_arrays(m1)
    n_bars = len(m1_arr["times"])

    aggs: list[pl.DataFrame] = []
    trigs: list[pl.DataFrame] = []
    n_trig_raw = 0
    for magic_time in magic_times:
        for duration in or_durations:
            trig_df, span_days = _scan_combo(symbol, magic_time, duration, m15, m1_arr, cfg)
            if trig_df.is_empty():
                continue
            n_trig_raw += len(trig_df)
            agg = aggregate_edge_per_pattern(trig_df, span_days, cfg)
            if agg.is_empty():
                continue
            agg = agg.with_columns([
                pl.lit(symbol).alias("symbol"),
                pl.lit(magic_time).alias("magic_time"),
                pl.lit(duration).alias("or_duration_min"),
                pl.lit(span_days).alias("span_days"),
            ])
            aggs.append(agg)
            trigs.append(trig_df)

    agg_df = pl.concat(aggs, how="diagonal_relaxed") if aggs else pl.DataFrame()
    trig_df = pl.concat(trigs, how="diagonal_relaxed") if trigs else pl.DataFrame()
    secs = time.time() - t0
    summary = (
        f"{n_bars:,} bars | {n_trig_raw:,} raw triggers | "
        f"{len(agg_df)} pattern survivors | {secs:.0f}s"
    )
    return symbol, agg_df, trig_df, summary


def run_phase_a(out_path=None, cfg=None, workers: int | None = None) -> pl.DataFrame:
    """Run Phase A in parallel across symbols.

    Defaults to min(6, len(SYMBOLS_V1), cpu_count//4). On a 32-core / 32GB
    machine, 6 workers peak around 21GB RAM.
    """
    cfg = cfg or PhaseAConfig()
    out_path = Path(out_path) if out_path else Path(REPORTS_DIR) / "orb_phase_a.parquet"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    cpu = os.cpu_count() or 8
    if workers is None:
        workers = min(6, len(SYMBOLS_V1), max(1, cpu // 4))

    args_list = [(sym, cfg, MAGIC_TIMES, OR_DURATIONS) for sym in SYMBOLS_V1]

    t0 = time.time()
    print(f"[Phase A] {len(SYMBOLS_V1)} symbols across {workers} workers "
          f"(cpu={cpu}, polars_threads_per_worker=4)", flush=True)

    all_rows: list[pl.DataFrame] = []
    all_triggers: list[pl.DataFrame] = []
    completed = 0
    total = len(SYMBOLS_V1)

    ctx = mp.get_context("spawn")
    with ctx.Pool(processes=workers, maxtasksperchild=1) as pool:
        for symbol, agg_df, trig_df, summary in pool.imap_unordered(
            _process_one_symbol, args_list
        ):
            completed += 1
            elapsed_min = (time.time() - t0) / 60
            eta_min = (elapsed_min / completed) * (total - completed) if completed > 0 else 0
            pct = 100.0 * completed / total
            print(f"[Phase A] [{pct:5.1f}%] {completed}/{total} done | {symbol}: {summary} "
                  f"| total elapsed {elapsed_min:.1f}m, eta {eta_min:.1f}m", flush=True)
            if not agg_df.is_empty():
                all_rows.append(agg_df)
            if not trig_df.is_empty():
                all_triggers.append(trig_df)

    elapsed_total = (time.time() - t0) / 60
    print(f"[Phase A] [100.0%] done in {elapsed_total:.1f}m", flush=True)

    if not all_rows:
        out_df = pl.DataFrame()
    else:
        out_df = pl.concat(all_rows, how="diagonal_relaxed")
    out_df.write_parquet(out_path)

    trig_path = out_path.parent / "orb_phase_a_triggers.parquet"
    if all_triggers:
        pl.concat(all_triggers, how="diagonal_relaxed").write_parquet(trig_path)
    print(f"[Phase A] wrote {len(out_df)} rows to {out_path.name}, "
          f"{sum(len(t) for t in all_triggers):,} triggers to {trig_path.name}", flush=True)
    return out_df


if __name__ == "__main__":
    df = run_phase_a()
    print(f"Phase A: {len(df)} pattern survivors")
