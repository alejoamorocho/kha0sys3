"""Replay AMO8 OR detection over the last N days of MT5 M15 data.

For each (symbol, magic_time_broker, or_duration) slot, count how many days
had OR_bucket=expanded (the only bucket the 84 configs match against).
Run on VPS where MT5 is live.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
from datetime import datetime, timezone, timedelta
from collections import defaultdict, Counter

import MetaTrader5 as mt5
import polars as pl
import numpy as np

from src.application.calculators import DataEnricher
from src.application.orb_patterns import add_state_columns

# ---- config ----
LOOKBACK_DAYS = 60
BROKER_OFFSET_H = 3  # Vantage EEST
CONFIG_PATH = "src/execution/bot_config_amo8.json"

cfg = json.loads(Path(CONFIG_PATH).read_text(encoding="utf-8"))
ports = cfg["portfolio"]

# Build schedule: (broker_sym, magic_time_broker, or_duration) -> list of configs
schedule = defaultdict(list)
for s in ports:
    hh, mm = s["magic_time"].split(":")
    mt_broker = f"{(int(hh)+BROKER_OFFSET_H)%24:02d}:{mm}"
    schedule[(s["broker_sym"], mt_broker, int(s["or_duration_min"]))].append(s)

print(f"Replaying {len(schedule)} slots over last {LOOKBACK_DAYS} trading days")
print(f"Broker offset assumed: +{BROKER_OFFSET_H}h\n")

mt5.initialize()

now = datetime.now(timezone.utc)
# Fetch ~80 calendar days to ensure we have 60 trading days + warm-up for atr_14
bars_needed = LOOKBACK_DAYS * 24 * 4 + 2200  # margin

# Per-slot stats
slot_stats = defaultdict(lambda: {
    "days_with_or": 0,        # had any OR bars
    "days_with_atr": 0,        # atr_14 computed
    "by_bucket": Counter(),    # {'expanded': N, 'normal': N, 'compressed': N}
    "by_pd": Counter(),        # {'gap_up': N, 'gap_down': N, 'inside': N}
    "matchable_days": 0,       # day where some deployed config would match
    "match_examples": [],
})

# Per-day grand totals: any slot that would have fired
daily_match_count = defaultdict(int)
daily_slots_processed = defaultdict(int)

for (broker_sym, mt_broker, or_dur), configs in schedule.items():
    print(f"  fetching {broker_sym} M15 ({bars_needed} bars)...", end=" ", flush=True)
    rates = mt5.copy_rates_from_pos(broker_sym, mt5.TIMEFRAME_M15, 0, bars_needed)
    if rates is None or len(rates) < 100:
        print(f"NO DATA ({0 if rates is None else len(rates)})")
        continue
    df = pl.DataFrame({
        "time": [datetime.fromtimestamp(int(r["time"]), tz=None) for r in rates],
        "open": [float(r["open"]) for r in rates],
        "high": [float(r["high"]) for r in rates],
        "low":  [float(r["low"]) for r in rates],
        "close":[float(r["close"]) for r in rates],
    }).sort("time")
    print(f"got {len(df)}")

    try:
        enriched = DataEnricher.enrich_with_daily_context(df, "00:00", "23:59")
        enriched_or = DataEnricher.enrich_with_opening_range(enriched, mt_broker, or_dur)
        enriched_or = add_state_columns(enriched_or)
    except Exception as e:
        print(f"  ENRICH FAIL {broker_sym}: {e}")
        continue

    # First post-OR row per trade_date
    post_or = enriched_or.filter(pl.col("is_post_or")).sort("time")
    # Take only the FIRST row per trade_date (the OR-close moment)
    if "trade_date" not in post_or.columns or len(post_or) == 0:
        continue
    first = post_or.group_by("trade_date").agg([
        pl.col("time").min().alias("or_close_ts"),
        pl.col("or_high").first(),
        pl.col("or_low").first(),
        pl.col("atr_14").first(),
        pl.col("or_atr_bucket").first(),
        pl.col("pd_or_overlap_bucket").first(),
        pl.col("or_position_vs_pd").first(),
    ]).sort("trade_date")

    # Restrict to last LOOKBACK_DAYS trading days
    last_date = first["trade_date"].max()
    cutoff = last_date - timedelta(days=LOOKBACK_DAYS)
    first = first.filter(pl.col("trade_date") >= cutoff)

    for row in first.iter_rows(named=True):
        td = row["trade_date"]
        slot_stats[(broker_sym, mt_broker, or_dur)]["days_with_or"] += 1
        daily_slots_processed[td] += 1
        if row["atr_14"] is None:
            continue
        slot_stats[(broker_sym, mt_broker, or_dur)]["days_with_atr"] += 1
        atr_b = row["or_atr_bucket"] or "null"
        pd_b = row["pd_or_overlap_bucket"] or "null"
        pos = row["or_position_vs_pd"] or "null"
        slot_stats[(broker_sym, mt_broker, or_dur)]["by_bucket"][atr_b] += 1
        slot_stats[(broker_sym, mt_broker, or_dur)]["by_pd"][pd_b] += 1
        # Would any deployed config match?
        matches = [c for c in configs
                   if c["or_position"] == pos
                   and c["or_atr_bucket"] == atr_b
                   and c["pd_or_bucket"] == pd_b]
        if matches:
            slot_stats[(broker_sym, mt_broker, or_dur)]["matchable_days"] += 1
            daily_match_count[td] += len(matches)
            if len(slot_stats[(broker_sym, mt_broker, or_dur)]["match_examples"]) < 3:
                slot_stats[(broker_sym, mt_broker, or_dur)]["match_examples"].append(
                    (str(td), pos, atr_b, pd_b, len(matches))
                )

# ---------- Reports ----------
print(f"\n{'='*80}\n=== PER-SLOT SUMMARY (last {LOOKBACK_DAYS} trading days) ===\n{'='*80}")
print(f"{'slot':<32} {'days_OR':>8} {'days_ATR':>9} {'expanded':>9} {'normal':>7} {'compr':>7} {'matchable':>10}")
total_matchable = 0
total_configs_fired = sum(daily_match_count.values())
for k in sorted(slot_stats.keys()):
    s = slot_stats[k]
    label = f"{k[0]}|{k[1]}|{k[2]}m"
    nb = s["by_bucket"]
    print(f"  {label:<30} {s['days_with_or']:>8} {s['days_with_atr']:>9} "
          f"{nb.get('expanded',0):>9} {nb.get('normal',0):>7} {nb.get('compressed',0):>7} "
          f"{s['matchable_days']:>10}")
    total_matchable += s["matchable_days"]

print()
print(f"=== AGGREGATE ===")
print(f"  total slot-days observed:        {sum(s['days_with_atr'] for s in slot_stats.values())}")
print(f"  total slot-days with match:      {total_matchable}")
print(f"  unique calendar days with ≥1 match: {sum(1 for c in daily_match_count.values() if c>0)} / {len(daily_slots_processed)}")
print(f"  total config-fires in window:    {total_configs_fired}  ({total_configs_fired/LOOKBACK_DAYS:.2f}/day avg)")
print(f"  backtest expected total tpy:     {cfg['_metrics_aggregate']['sum_trades_per_year']}  ({cfg['_metrics_aggregate']['sum_trades_per_year']/260:.2f}/trading-day)")

print()
print(f"=== DAYS WHERE AMO8 WOULD HAVE FIRED (top 15) ===")
top_days = sorted(daily_match_count.items(), key=lambda x: -x[1])[:15]
for td, n in top_days:
    print(f"  {td}: {n} config-fires across slots")

print()
print(f"=== EXAMPLES PER SLOT (first match for matched slots) ===")
for k in sorted(slot_stats.keys()):
    if slot_stats[k]["match_examples"]:
        print(f"  {k[0]}|{k[1]}|{k[2]}m:")
        for ex in slot_stats[k]["match_examples"]:
            print(f"     {ex[0]} pos={ex[1]} atr_b={ex[2]} pd_b={ex[3]} -> {ex[4]} configs match")

mt5.shutdown()
