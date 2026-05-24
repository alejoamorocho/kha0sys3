"""Aggregate edge at the EVENT level only (no bucket × position × gap subdivision).

This is a much more powerful statistical test: each (sym × mt × dur × event × dir)
combo gets thousands of triggers instead of dozens. If edge exists in any event
category for any symbol, it should surface here.

Reuses triggers parquet from v1 discovery (5 symbols only). For full 15-sym,
will need v2 to finish first or run separately.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from datetime import timedelta
import bisect
import numpy as np
import polars as pl

SL_OR_GRID = [0.5, 1.0, 1.5]
RR_GRID = [1.0, 1.5, 2.0, 3.0]
FRICTION_R = 0.3
MIN_TRADES = 100  # event-level needs more per combo for stat power
MIN_TPY = 30
MIN_PF = 1.0
MIN_WR = 0.50

# Try loading v2 triggers first (15 syms), fall back to v1 (5 syms)
trig_paths = [
    "reports/orb/amo8_discovery_v2_triggers.parquet",
    "reports/orb/amo8_discovery_triggers.parquet",
]
df = None
for p in trig_paths:
    if Path(p).exists():
        print(f"Loading triggers from {p}", flush=True)
        df = pl.read_parquet(p)
        break
if df is None:
    print("No triggers parquet found. Run discovery first.")
    sys.exit(1)

print(f"Loaded {len(df)} triggers", flush=True)
print(f"  symbols: {sorted(df['sym'].unique().to_list())}", flush=True)
print(f"  events: {sorted(df['event'].unique().to_list())}", flush=True)

# Load M1 caches lazily per symbol
m1_cache = {}
def get_m1(sym):
    if sym in m1_cache:
        return m1_cache[sym]
    path = f"data/enriched_math_tf/{sym}_M1.parquet"
    print(f"  loading M1 for {sym}...", flush=True)
    m1 = pl.scan_parquet(path).select(["time","high","low","close"]).sort("time").collect()
    times_list = m1["time"].to_list()
    times_arr = np.array(times_list, dtype="object")
    highs = np.asarray(m1["high"].to_list(), dtype=float)
    lows = np.asarray(m1["low"].to_list(), dtype=float)
    m1_cache[sym] = (times_list, times_arr, highs, lows)
    return m1_cache[sym]


def simulate(trigger_ts, entry, direction, sl_dist, rr, times_list, times_arr, highs, lows, max_hold_min):
    sign = 1.0 if direction == "LONG" else -1.0
    if sl_dist <= 0: return None
    sl_price = entry - sign * sl_dist
    tp_price = entry + sign * rr * sl_dist
    start = bisect.bisect_right(times_list, trigger_ts)
    n = len(times_arr)
    if start >= n: return None
    horizon = trigger_ts + timedelta(minutes=max_hold_min)
    for j in range(start, n):
        if times_arr[j] > horizon: return 0.0
        hi = highs[j]; lo = lows[j]
        if direction == "LONG":
            if lo <= sl_price: return -1.0
            if hi >= tp_price: return float(rr)
        else:
            if hi >= sl_price: return -1.0
            if lo <= tp_price: return float(rr)
    return 0.0


# Group at EVENT level (no bucket subdivision)
combos = df.group_by(["sym","magic_time","or_dur","event"]).agg(pl.len().alias("n")).filter(pl.col("n") >= MIN_TRADES)
print(f"\nEvent-level combos with >={MIN_TRADES} triggers: {len(combos)}", flush=True)

winners = []
for ci, c in enumerate(combos.iter_rows(named=True), 1):
    sym, mt, or_dur, ev = c["sym"], c["magic_time"], c["or_dur"], c["event"]
    sub = df.filter((pl.col("sym")==sym) & (pl.col("magic_time")==mt)
                    & (pl.col("or_dur")==or_dur) & (pl.col("event")==ev))
    if len(sub) < MIN_TRADES:
        continue
    times_list, times_arr, highs, lows = get_m1(sym)
    max_hold_min = 10 * or_dur
    # Span days
    first_ts = sub["trigger_ts"].min()
    last_ts = sub["trigger_ts"].max()
    span_days = max((last_ts - first_ts).days, 1)

    for direction in ["LONG","SHORT"]:
        for sl in SL_OR_GRID:
            for rr in RR_GRID:
                results = []
                for t in sub.iter_rows(named=True):
                    r = simulate(t["trigger_ts"], t["trigger_close"], direction,
                                 sl * t["or_width"], rr,
                                 times_list, times_arr, highs, lows, max_hold_min)
                    if r is not None:
                        results.append(r - FRICTION_R)
                if len(results) < MIN_TRADES:
                    continue
                arr = np.asarray(results)
                wins = arr[arr > 0].sum(); losses = -arr[arr < 0].sum()
                pf = float(wins/losses) if losses>0 else (float("inf") if wins>0 else 0.0)
                wr = float((arr>0).mean())
                expectancy = float(arr.mean())
                tpy = len(arr) / (span_days/365.25)
                if pf>=MIN_PF and wr>=MIN_WR and expectancy>0 and tpy>=MIN_TPY:
                    winners.append({
                        "sym":sym,"magic_time":mt,"or_dur":or_dur,"event":ev,"direction":direction,
                        "sl_or":sl,"rr":rr,"trades":len(arr),"tpy":tpy,
                        "win_rate":wr,"pf":pf,"expectancy_r":expectancy,
                        "sum_r":float(arr.sum()),
                    })
    if ci % 20 == 0:
        print(f"  [{ci}/{len(combos)}] winners so far: {len(winners)}", flush=True)

print(f"\n{'='*60}\nEVENT-LEVEL WINNERS: {len(winners)}\n{'='*60}\n", flush=True)
if winners:
    wdf = pl.DataFrame(winners)
    wdf.write_parquet("reports/orb/amo8_event_level_winners.parquet")
    print("Per-symbol breakdown:")
    print(wdf.group_by("sym").agg([pl.len().alias("n"), pl.col("pf").max().alias("max_pf")]).sort("n",descending=True))
    print("\nPer-event breakdown:")
    print(wdf.group_by("event").agg([pl.len().alias("n"), pl.col("pf").max().alias("max_pf")]).sort("n",descending=True))
    print("\nTop 30 by PF:")
    for r in wdf.sort("pf",descending=True).head(30).iter_rows(named=True):
        print(f"  {r['sym']:<10} mt={r['magic_time']} dur={r['or_dur']:>3}m  {r['event']:<20} {r['direction']:<5}  "
              f"sl={r['sl_or']} rr={r['rr']}  PF={r['pf']:.2f} WR={r['win_rate']*100:.1f}% "
              f"tpy={r['tpy']:.0f} n={r['trades']}")
else:
    print("NO EVENT-LEVEL WINNERS EITHER. Likely friction issue or simulation bug.")
    print("\nLet's check what edge LOOKS like raw — show top events by avg MFE/OR_width (no simulation):")
    # Compute raw MFE/OR — needs MFE columns. v1 triggers may have them, v2 doesn't.
    if "mfe_long" in df.columns:
        raw = df.with_columns([
            (pl.col("mfe_long") / pl.col("or_width")).alias("mfe_or"),
            (pl.col("mae_long") / pl.col("or_width")).alias("mae_or"),
        ]).group_by(["sym","magic_time","or_dur","event"]).agg([
            pl.len().alias("n"),
            pl.col("mfe_or").median().alias("med_mfe_or"),
            pl.col("mae_or").median().alias("med_mae_or"),
            (pl.col("mfe_or") - pl.col("mae_or")).median().alias("med_edge_or"),
        ]).filter(pl.col("n") >= MIN_TRADES).sort("med_edge_or", descending=True).head(20)
        print(raw)
    else:
        print("(v2 triggers don't have mfe columns — would need to rerun walker)")
