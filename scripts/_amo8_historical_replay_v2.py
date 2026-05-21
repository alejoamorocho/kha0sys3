"""Replay AMO8 over VPS MT5 data — v2 uses corrected convention.

Bars from MT5 are converted to REAL UTC by subtracting the broker offset
(same as ORB/SWING/MATH live engines do). magic_time is treated literally
as real UTC. No shift applied — matches backtest source convention.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
from datetime import datetime, timezone, timedelta
from collections import defaultdict, Counter
import MetaTrader5 as mt5
import polars as pl

from src.application.calculators import DataEnricher
from src.application.orb_patterns import add_state_columns

LOOKBACK_DAYS = 60
CONFIG_PATH = "src/execution/bot_config_amo8.json"

cfg = json.loads(Path(CONFIG_PATH).read_text(encoding="utf-8"))
ports = cfg["portfolio"]

mt5.initialize()

# Detect broker offset from a fresh tick
import time as _t
now_real = int(_t.time())
offset_h = 3
for sym in ("EURUSD+","XAUUSD+","GBPUSD+","XAGUSD"):
    t = mt5.symbol_info_tick(sym)
    if t and int(t.time) > 0 and abs(int(t.time)-now_real) <= 300:
        offset_h = int(round((int(t.time)-now_real)/3600))
        break
print(f"Broker offset detected: {offset_h:+d}h")
offset_sec = offset_h * 3600

# Build slots: key by (broker_sym, magic_time_UTC, or_dur) — NO shift
schedule = defaultdict(list)
for s in ports:
    schedule[(s["broker_sym"], s["magic_time"], int(s["or_duration_min"]))].append(s)

print(f"Replaying {len(schedule)} slots over last {LOOKBACK_DAYS} trading days (real UTC convention)\n")

bars_needed = LOOKBACK_DAYS*24*4 + 2200
slot_stats = defaultdict(lambda: {
    "days": 0, "by_bucket": Counter(), "matchable": 0, "fires": 0, "examples": []
})
daily_fires = defaultdict(int)

for (broker_sym, mt_utc, or_dur), configs in schedule.items():
    rates = mt5.copy_rates_from_pos(broker_sym, mt5.TIMEFRAME_M15, 0, bars_needed)
    if rates is None or len(rates) < 100:
        continue
    # SUBTRACT offset to get real UTC (same as live now)
    df = pl.DataFrame({
        "time": [datetime.fromtimestamp(int(r["time"])-offset_sec, tz=None) for r in rates],
        "open": [float(r["open"]) for r in rates],
        "high": [float(r["high"]) for r in rates],
        "low":  [float(r["low"]) for r in rates],
        "close":[float(r["close"]) for r in rates],
    }).sort("time")
    print(f"  {broker_sym}|{mt_utc}|{or_dur}m: {len(df)} bars ({df['time'].min()} -> {df['time'].max()})")
    try:
        enriched = DataEnricher.enrich_with_daily_context(df, "00:00", "23:59")
        enriched_or = DataEnricher.enrich_with_opening_range(enriched, mt_utc, or_dur)
        enriched_or = add_state_columns(enriched_or)
    except Exception as e:
        print(f"   enrich FAIL: {e}")
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
    last_date = first["trade_date"].max()
    cutoff = last_date - timedelta(days=LOOKBACK_DAYS)
    first = first.filter(pl.col("trade_date") >= cutoff)

    for row in first.iter_rows(named=True):
        if row["atr_14"] is None:
            continue
        atr_b = row["or_atr_bucket"] or "null"
        pd_b = row["pd_or_overlap_bucket"] or "null"
        pos = row["or_position_vs_pd"] or "null"
        s = slot_stats[(broker_sym, mt_utc, or_dur)]
        s["days"] += 1
        s["by_bucket"][atr_b] += 1
        matches = [c for c in configs
                   if c["or_position"]==pos and c["or_atr_bucket"]==atr_b and c["pd_or_bucket"]==pd_b]
        if matches:
            s["matchable"] += 1
            s["fires"] += len(matches)
            daily_fires[row["trade_date"]] += len(matches)
            if len(s["examples"]) < 3:
                s["examples"].append((str(row["trade_date"]), pos, atr_b, pd_b, len(matches)))

print(f"\n{'='*80}")
print(f"=== AMO8 60-day VPS replay  (REAL UTC, no shift) ===")
print(f"{'='*80}")
print(f"{'slot':<32} {'days':>6} {'exp':>6} {'norm':>6} {'comp':>6} {'matchable':>10} {'fires':>7}")
total_fires = 0; total_matchable = 0; total_expanded = 0; total_days = 0
for k in sorted(slot_stats.keys()):
    s = slot_stats[k]
    nb = s["by_bucket"]
    print(f"  {k[0]:<10} {k[1]:<6} {k[2]}m{'':<3} "
          f"{s['days']:>6} {nb.get('expanded',0):>6} {nb.get('normal',0):>6} {nb.get('compressed',0):>6} "
          f"{s['matchable']:>10} {s['fires']:>7}")
    total_fires += s["fires"]; total_matchable += s["matchable"]
    total_expanded += nb.get("expanded",0); total_days += s["days"]
print()
print(f"  TOTALS: days_obs={total_days} expanded={total_expanded} ({total_expanded/max(total_days,1)*100:.1f}%) "
      f"matchable={total_matchable} fires={total_fires}")
days_with_any = sum(1 for c in daily_fires.values() if c>0)
print(f"  Unique calendar days with >=1 match: {days_with_any}")
print(f"  fires/trading-day avg: {total_fires/LOOKBACK_DAYS:.2f}  (backtest claimed 10.47/day)")
print()
print("Examples per slot:")
for k in sorted(slot_stats.keys()):
    if slot_stats[k]["examples"]:
        print(f"  {k[0]}|{k[1]}|{k[2]}m:")
        for ex in slot_stats[k]["examples"]:
            print(f"    {ex[0]}  pos={ex[1]:<22} atr_b={ex[2]:<10} pd_b={ex[3]:<10}  matches={ex[4]}")
mt5.shutdown()
