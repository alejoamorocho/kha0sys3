"""Replay AMO8 detection pipeline for current/last window. Run on VPS.

Mirrors _process_slot exactly to expose what AMO8 sees per slot:
 - OR detection (or_high, or_low, atr)
 - pd context (pd_mid, pd_or_overlap_bucket, etc.)
 - M1 slice size
 - events detected
 - pattern_id built and whether any strategy matches
"""
import sys, json, bisect
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import polars as pl
import MetaTrader5 as mt5

from src.execution.live_amo_trader import AmoTraderEngine as AmoLiveTrader
from src.application.orb_patterns import detect_events_for_day, add_state_columns
from src.application.data_enricher import DataEnricher

bot = AmoLiveTrader()
bot._refresh_broker_offset()
print(f"Broker offset: {bot._broker_offset_h:+d}h")

now = bot._now_broker()
real_utc = datetime.now(timezone.utc)
print(f"Real UTC now: {real_utc.strftime('%Y-%m-%d %H:%M')}")
print(f"Broker-as-UTC now: {now.strftime('%Y-%m-%d %H:%M')}")
print()

active = bot._active_slots(now)
print(f"Active slots NOW: {len(active)} / {len(bot.schedule)}")
print()

# If no active, replay against the most-recent window that DID close (today's window even if past 8h)
slots_to_check = active if active else bot.schedule
print(f"Replaying {len(slots_to_check)} slot(s)...")
print()

for (broker_sym, magic_time, or_dur), strategies in slots_to_check.items():
    print(f"=== {broker_sym} / mt={magic_time} / or_dur={or_dur}m  ({len(strategies)} strats) ===")
    or_close = bot._or_close_time(now, magic_time, or_dur)
    if or_close is None:
        # Force replay against today even though OR hasn't started -> use yesterday
        hh, mm = magic_time.split(":")
        or_close = (now - timedelta(days=1)).replace(hour=int(hh), minute=int(mm), second=0, microsecond=0) + timedelta(minutes=or_dur)
        print(f"  (window not started today; replaying yesterday OR close={or_close})")
    age_h = (now - or_close).total_seconds() / 3600
    print(f"  or_close (broker-as-UTC): {or_close}   age={age_h:.1f}h")

    m1 = bot._fetch_bars(broker_sym, "M1", bot.M1_LOOKBACK_BARS)
    m15 = bot._fetch_bars(broker_sym, "M15", bot.M15_LOOKBACK_BARS)
    if m1 is None or m1.is_empty() or m15 is None or m15.is_empty():
        print(f"  NO BARS m1={None if m1 is None else len(m1)} m15={None if m15 is None else len(m15)}")
        continue
    print(f"  bars: m1={len(m1)}  m15={len(m15)}  last_m1={m1['time'].max()}")

    try:
        e15 = DataEnricher.enrich_with_daily_context(m15, "00:00", "23:59")
        e_or = DataEnricher.enrich_with_opening_range(e15, magic_time, or_dur)
        e_or = add_state_columns(e_or)
    except Exception as e:
        print(f"  ENRICH ERROR: {e}")
        continue

    today = now.date()
    today_rows = e_or.filter(
        (pl.col("trade_date") == today) & (pl.col("is_post_or"))
    ).sort("time")
    if today_rows.is_empty():
        # Try yesterday
        yest = today - timedelta(days=1)
        today_rows = e_or.filter(
            (pl.col("trade_date") == yest) & (pl.col("is_post_or"))
        ).sort("time")
        if today_rows.is_empty():
            print(f"  NO post_or rows for today nor yesterday in enriched_or")
            print(f"  trade_date values present: {e_or['trade_date'].unique().sort().tail(5).to_list()}")
            continue
        else:
            print(f"  using YESTERDAY rows ({len(today_rows)})")

    row0 = today_rows.row(0, named=True)
    print(f"  row0 keys: or_high={row0.get('or_high')} or_low={row0.get('or_low')} "
          f"atr_14={row0.get('atr_14')} or_pos={row0.get('or_position_vs_pd')} "
          f"or_atr_b={row0.get('or_atr_bucket')} pd_or_b={row0.get('pd_or_overlap_bucket')}")

    for k in ("or_high", "or_low", "atr_14"):
        if row0.get(k) is None:
            print(f"  MISSING {k} -> skip")
            break
    else:
        or_high = float(row0["or_high"]); or_low = float(row0["or_low"])
        atr = float(row0["atr_14"])
        or_close_ts = row0["time"]

        m1_sorted = m1.sort("time")
        m1_times = m1_sorted["time"].to_list()
        start_idx = bisect.bisect_right(m1_times, or_close_ts)
        last_closed_ts = now.replace(second=0, microsecond=0) - timedelta(minutes=1)
        end_idx = bisect.bisect_right(m1_times, last_closed_ts)
        print(f"  M1 slice: start_idx={start_idx} end_idx={end_idx} (n={end_idx-start_idx})")
        if end_idx <= start_idx:
            print(f"  EMPTY SLICE -> skip")
        else:
            day_slice = {
                "times": np.array(m1_times[start_idx:end_idx], dtype="object"),
                "highs": np.asarray(m1_sorted["high"].to_list()[start_idx:end_idx], dtype=float),
                "lows": np.asarray(m1_sorted["low"].to_list()[start_idx:end_idx], dtype=float),
                "closes": np.asarray(m1_sorted["close"].to_list()[start_idx:end_idx], dtype=float),
            }
            events = detect_events_for_day(
                or_close_ts=or_close_ts, or_high=or_high, or_low=or_low,
                pd_mid=row0.get("pd_mid"), pd_close=row0.get("pd_close"),
                pd_or_high=row0.get("pd_or_high"), pd_or_low=row0.get("pd_or_low"),
                atr_at_setup=atr, m1=day_slice,
            )
            print(f"  EVENTS DETECTED: {len(events)}")
            or_position = row0.get("or_position_vs_pd") or "NULL"
            or_atr_bucket = row0.get("or_atr_bucket") or "NULL"
            pd_or_bucket = row0.get("pd_or_overlap_bucket") or "NULL"
            for ev in events:
                pid = f"{ev['event_type']}_{or_position}_{or_atr_bucket}_{pd_or_bucket}"
                matches = [s["id"] for s in strategies if s["pattern_id"] == pid]
                print(f"    event={ev['event_type']} -> pattern_id={pid}")
                print(f"      matching strategies: {len(matches)}  {matches[:3]}")
    print()

mt5.shutdown()
