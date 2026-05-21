"""Replay the 84 deployed AMO8 configs against LOCAL backtest data.

Runs the exact same OR detection logic the live bot uses, but on
data/enriched_math_tf/*_M15.parquet — the same source the original
discovery used. Tests TWO hypotheses about magic_time mapping:

  H1: magic_time in config is broker-time. Match bars where time.hour == 0
  H2: magic_time is UTC and needs +3h shift to match Vantage broker. Match hour == 3

Compares trade-counts under each hypothesis. Backtest expected ~10/day.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
from collections import defaultdict, Counter
from datetime import datetime, timedelta

import polars as pl

from src.application.calculators import DataEnricher
from src.application.orb_patterns import add_state_columns

# Map internal_sym -> data file (from data/enriched_math_tf/)
SYM_TO_FILE = {
    "XAUUSD":   "data/enriched_math_tf/XAUUSD_M15.parquet",
    "GBPUSD":   "data/enriched_math_tf/GBPUSD_M15.parquet",
    "NASDAQ100":"data/enriched_math_tf/NASDAQ100_M15.parquet",
    "NATGAS":   "data/enriched_math_tf/NATGAS_M15.parquet",
    "SP500":    "data/enriched_math_tf/SP500_M15.parquet",
}

cfg = json.loads(Path("src/execution/bot_config_amo8.json").read_text(encoding="utf-8"))
ports = cfg["portfolio"]

# Group configs by (internal_sym, magic_time, or_dur)
slots = defaultdict(list)
for s in ports:
    slots[(s["internal_sym"], s["magic_time"], int(s["or_duration_min"]))].append(s)

print(f"{len(ports)} configs in {len(slots)} unique slots\n")

# Sanity: print what the unique magic_times are
print("Unique magic_time values in config:", sorted(set(s["magic_time"] for s in ports)))
print()

# For each slot, replay against local M15 data
# H1: use magic_time literally (treat config magic_time as the OR start hour)
# H2: use magic_time + 3h (assume config is UTC, data is broker-as-UTC)
HYPOTHESES = {"H1_literal_magic_time": 0, "H2_plus_3h_shift": 3}

results = defaultdict(lambda: defaultdict(lambda: {"days_observed": 0,
                                                    "by_bucket": Counter(),
                                                    "matchable_days": 0,
                                                    "configs_fired": 0,
                                                    "match_examples": []}))

for (internal_sym, magic_time, or_dur), configs in slots.items():
    path = SYM_TO_FILE.get(internal_sym)
    if not path or not Path(path).exists():
        print(f"SKIP {internal_sym}: no file {path}")
        continue
    df = pl.read_parquet(path).sort("time")
    last_ts = df["time"].max()
    print(f"{internal_sym}/{magic_time}/{or_dur}m: {len(df)} bars  ({df['time'].min()} -> {last_ts})  configs={len(configs)}")

    for hyp_name, shift_h in HYPOTHESES.items():
        # Shift the magic_time
        hh, mm = magic_time.split(":")
        shifted_h = (int(hh) + shift_h) % 24
        mt_shifted = f"{shifted_h:02d}:{mm}"
        try:
            enriched = DataEnricher.enrich_with_daily_context(df, "00:00", "23:59")
            enriched_or = DataEnricher.enrich_with_opening_range(enriched, mt_shifted, or_dur)
            enriched_or = add_state_columns(enriched_or)
        except Exception as e:
            print(f"  {hyp_name} enrich fail: {e}")
            continue
        post_or = enriched_or.filter(pl.col("is_post_or")).sort("time")
        if len(post_or) == 0:
            continue
        first = post_or.group_by("trade_date").agg([
            pl.col("or_atr_bucket").first(),
            pl.col("pd_or_overlap_bucket").first(),
            pl.col("or_position_vs_pd").first(),
            pl.col("atr_14").first(),
        ]).sort("trade_date")

        for row in first.iter_rows(named=True):
            if row["atr_14"] is None:
                continue
            atr_b = row["or_atr_bucket"] or "null"
            pd_b = row["pd_or_overlap_bucket"] or "null"
            pos = row["or_position_vs_pd"] or "null"
            r = results[hyp_name][(internal_sym, magic_time, or_dur)]
            r["days_observed"] += 1
            r["by_bucket"][atr_b] += 1
            matches = [c for c in configs
                       if c["or_position"] == pos
                       and c["or_atr_bucket"] == atr_b
                       and c["pd_or_bucket"] == pd_b]
            if matches:
                r["matchable_days"] += 1
                r["configs_fired"] += len(matches)
                if len(r["match_examples"]) < 3:
                    r["match_examples"].append((str(row["trade_date"]), pos, atr_b, pd_b, len(matches)))

print()
for hyp_name in HYPOTHESES:
    print("="*80)
    print(f"=== HYPOTHESIS: {hyp_name}  (magic_time shift = {HYPOTHESES[hyp_name]}h) ===")
    print("="*80)
    print(f"{'slot':<35} {'days':>6} {'expanded':>9} {'normal':>7} {'compr':>7} {'match_days':>11} {'fires':>7}")
    total_fires = 0
    total_days = 0
    total_matchable = 0
    total_expanded = 0
    for k in sorted(results[hyp_name].keys()):
        r = results[hyp_name][k]
        nb = r["by_bucket"]
        print(f"  {k[0]:<15} {k[1]:<6} {k[2]}m{'':<3} "
              f"{r['days_observed']:>6} {nb.get('expanded',0):>9} {nb.get('normal',0):>7} "
              f"{nb.get('compressed',0):>7} {r['matchable_days']:>11} {r['configs_fired']:>7}")
        total_fires += r["configs_fired"]
        total_days += r["days_observed"]
        total_matchable += r["matchable_days"]
        total_expanded += nb.get("expanded", 0)
    print()
    print(f"  TOTALS:  days_observed={total_days}  expanded_days={total_expanded}  matchable={total_matchable}  fires={total_fires}")
    if total_days > 0:
        years_approx = total_days / 260
        print(f"  Approx years of data: {years_approx:.2f}")
        print(f"  fires/year average: {total_fires/years_approx:.0f}   (backtest report said 2721/year)")
    print()
