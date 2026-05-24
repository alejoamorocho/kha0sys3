"""ATR-free AMO8 discovery — V2: full 15-symbol universe + bug fixes.

Fixes from v1:
  - Correct SHORT direction stats (separate aggregation per direction)
  - Relaxed filters to match original report (PF>=1.0, WR>=50%, exp>0, n>=30)
  - Universe expanded from 5 to 15 symbols (all with M1 data)
  - Adds report broken down per (sym, magic_time) for inspection
"""
from __future__ import annotations
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from datetime import timedelta
import bisect
import numpy as np
import polars as pl

from src.application.calculators import DataEnricher
from src.application.orb_patterns import detect_events_for_day

# Full 15-symbol universe (all that have M1 data in data/enriched_math_tf/)
SYMBOLS = [
    "XAUUSD", "XAGUSD", "BRENT", "WTI",
    "GBPUSD", "GBPJPY", "EURUSD", "GBPAUD",
    "USDJPY", "AUDUSD", "EURJPY", "EURAUD",
    "NASDAQ100", "NATGAS", "SP500",
]
MAGIC_TIMES = ["00:00", "07:00", "12:30", "22:00"]
OR_DURATIONS = [15, 30, 60, 120]
HORIZON_MIN = 240
SL_OR_GRID = [0.5, 1.0, 1.5]
RR_GRID = [1.0, 1.5, 2.0, 3.0]
FRICTION_R = 0.3  # 0.2 slippage + ~0.1 commission proxy

# Original report filters (relaxed)
MIN_TRADES = 30
MIN_TRADES_PER_YEAR = 30
MIN_PF = 1.0
MIN_WR = 0.50
MIN_EXPECTANCY = 0.0


def load_m1(sym: str):
    path = f"data/enriched_math_tf/{sym}_M1.parquet"
    if not Path(path).exists():
        return None
    print(f"  loading M1 for {sym}...", flush=True)
    m1 = pl.scan_parquet(path).select(["time","high","low","close"]).sort("time").collect()
    times_list = m1["time"].to_list()
    times_arr = np.array(times_list, dtype="object")
    highs = np.asarray(m1["high"].to_list(), dtype=float)
    lows = np.asarray(m1["low"].to_list(), dtype=float)
    closes = np.asarray(m1["close"].to_list(), dtype=float)
    print(f"     M1 loaded: {len(times_list)} bars", flush=True)
    return times_list, times_arr, highs, lows, closes


def simulate_or_fixed(trigger_ts, entry, direction, sl_or_frac, rr, or_width,
                      times_list, times_arr, highs, lows, max_hold_min):
    sign = 1.0 if direction == "LONG" else -1.0
    sl_dist = sl_or_frac * or_width
    if sl_dist <= 0:
        return None
    sl_price = entry - sign * sl_dist
    tp_price = entry + sign * rr * sl_dist
    start = bisect.bisect_right(times_list, trigger_ts)
    n = len(times_arr)
    if start >= n:
        return None
    horizon = trigger_ts + timedelta(minutes=max_hold_min)
    for j in range(start, n):
        if times_arr[j] > horizon:
            return 0.0
        hi = highs[j]; lo = lows[j]
        # SL-first conservative
        if direction == "LONG":
            if lo <= sl_price: return -1.0
            if hi >= tp_price: return float(rr)
        else:
            if hi >= sl_price: return -1.0
            if lo <= tp_price: return float(rr)
    return 0.0


def main():
    base = Path("reports/orb")
    base.mkdir(parents=True, exist_ok=True)
    all_triggers = []
    span_days_per_slot = {}
    m1_cache = {}

    for sym in SYMBOLS:
        m15_path = f"data/enriched_math_tf/{sym}_M15.parquet"
        if not Path(m15_path).exists():
            print(f"  SKIP {sym}: no M15 data", flush=True)
            continue
        m15 = pl.scan_parquet(m15_path).select(["time","open","high","low","close"]).sort("time").collect()
        m1_data = load_m1(sym)
        if m1_data is None:
            continue
        times_list, times_arr, highs, lows, closes = m1_data
        m1_cache[sym] = m1_data

        for mt in MAGIC_TIMES:
            for or_dur in OR_DURATIONS:
                print(f"  scanning {sym} mt={mt} dur={or_dur}m...", flush=True)
                enriched = DataEnricher.enrich_with_daily_context(m15, "00:00", "23:59")
                enriched_or = DataEnricher.enrich_with_opening_range(enriched, mt, or_dur)
                enriched_or = enriched_or.with_columns([
                    pl.when(pl.col("pd_or_high").is_null() | pl.col("pd_or_low").is_null()).then(pl.lit(None, dtype=pl.Utf8))
                      .when(pl.col("or_low") > pl.col("pd_or_high")).then(pl.lit("gap_up"))
                      .when(pl.col("or_high") < pl.col("pd_or_low")).then(pl.lit("gap_down"))
                      .otherwise(pl.lit("inside")).alias("pd_or_bucket"),
                    (pl.col("or_high") - pl.col("or_low")).alias("or_width_calc"),
                ])
                per_day = (enriched_or.filter(pl.col("is_post_or"))
                    .sort("time").group_by("trade_date")
                    .agg([
                        pl.col("time").first().alias("or_close_ts"),
                        pl.col("or_high").first(), pl.col("or_low").first(),
                        pl.col("pd_mid").first(), pl.col("pd_close").first(),
                        pl.col("pd_or_high").first(), pl.col("pd_or_low").first(),
                        pl.col("or_position_vs_pd").first().alias("or_position"),
                        pl.col("pd_or_bucket").first(),
                        pl.col("atr_14").first(),
                        pl.col("or_width_calc").first().alias("or_width"),
                    ]).filter(pl.col("or_high").is_not_null() & pl.col("or_low").is_not_null()
                              & pl.col("or_width").is_not_null() & (pl.col("or_width")>0))
                    .sort("trade_date"))
                # OR-width percentile bucket (NO ATR involvement)
                per_day = per_day.with_columns([
                    pl.col("or_width").rolling_quantile(0.30, window_size=90, min_samples=20).shift(1).alias("_q30"),
                    pl.col("or_width").rolling_quantile(0.70, window_size=90, min_samples=20).shift(1).alias("_q70"),
                ])
                per_day = per_day.with_columns([
                    pl.when(pl.col("_q30").is_null()).then(pl.lit(None, dtype=pl.Utf8))
                      .when(pl.col("or_width") <= pl.col("_q30")).then(pl.lit("compressed"))
                      .when(pl.col("or_width") >= pl.col("_q70")).then(pl.lit("expanded"))
                      .otherwise(pl.lit("normal")).alias("bkt_or"),
                ])
                first_d = per_day["or_close_ts"].min()
                last_d = per_day["or_close_ts"].max()
                if first_d and last_d:
                    span_days_per_slot[(sym, mt, or_dur)] = max((last_d - first_d).days, 1)

                slot_triggers = 0
                for row in per_day.iter_rows(named=True):
                    or_close_ts = row["or_close_ts"]
                    start_idx = bisect.bisect_right(times_list, or_close_ts)
                    end_idx = start_idx
                    while end_idx < len(times_list) and times_list[end_idx].date() == or_close_ts.date():
                        end_idx += 1
                    day_slice = {
                        "times": times_arr[start_idx:end_idx],
                        "highs": highs[start_idx:end_idx],
                        "lows": lows[start_idx:end_idx],
                        "closes": closes[start_idx:end_idx],
                    }
                    events = detect_events_for_day(
                        or_close_ts=or_close_ts,
                        or_high=row["or_high"], or_low=row["or_low"],
                        pd_mid=row["pd_mid"], pd_close=row["pd_close"],
                        pd_or_high=row["pd_or_high"], pd_or_low=row["pd_or_low"],
                        atr_at_setup=row["atr_14"] or 1.0,  # only used internally; not stored
                        m1=day_slice,
                    )
                    for ev in events:
                        all_triggers.append({
                            "sym": sym, "magic_time": mt, "or_dur": or_dur,
                            "event": ev["event_type"],
                            "or_position": row["or_position"] or "NONE",
                            "bkt_or": row["bkt_or"] or "NONE",
                            "pd_or_bucket": row["pd_or_bucket"] or "NONE",
                            "or_width": float(row["or_width"]),
                            "trigger_ts": ev["trigger_ts"],
                            "trigger_close": float(ev["trigger_close"]),
                        })
                        slot_triggers += 1
                print(f"     {slot_triggers} triggers", flush=True)

    df = pl.DataFrame(all_triggers)
    print(f"\n{len(df)} total triggers across {len(set(t['sym'] for t in all_triggers))} symbols", flush=True)
    df.write_parquet(base / "amo8_discovery_v2_triggers.parquet")

    # Now run management grid PER (sym, magic_time, or_dur, pattern_id, direction, sl, rr)
    print("\nRunning OR_FIXED management grid (per pattern × direction × sl × rr)...", flush=True)
    df = df.with_columns([
        pl.concat_str([
            pl.col("event"), pl.col("or_position"), pl.col("bkt_or"), pl.col("pd_or_bucket"),
        ], separator="_").alias("pattern_id"),
    ])

    # Pre-aggregate to count which (sym, mt, or_dur, pattern_id) slots have enough triggers
    pat_counts = df.group_by(["sym","magic_time","or_dur","pattern_id"]).agg(pl.len().alias("n"))
    pat_counts = pat_counts.filter(pl.col("n") >= MIN_TRADES)
    print(f"  Pattern slots with >= {MIN_TRADES} triggers: {len(pat_counts)}", flush=True)

    mgmt_rows = []
    progress = 0
    total_combos = len(pat_counts) * 2 * len(SL_OR_GRID) * len(RR_GRID)
    print(f"  Total mgmt combos to simulate: {total_combos:,}", flush=True)

    for pc in pat_counts.iter_rows(named=True):
        sym, mt, or_dur, pid = pc["sym"], pc["magic_time"], pc["or_dur"], pc["pattern_id"]
        triggers_for_pat = df.filter(
            (pl.col("sym")==sym) & (pl.col("magic_time")==mt)
            & (pl.col("or_dur")==or_dur) & (pl.col("pattern_id")==pid)
        )
        if sym not in m1_cache:
            continue
        times_list, times_arr, highs, lows, closes = m1_cache[sym]
        max_hold_min = 10 * or_dur
        span_days = span_days_per_slot.get((sym, mt, or_dur), 8*365)

        for direction in ["LONG", "SHORT"]:
            for sl in SL_OR_GRID:
                for rr in RR_GRID:
                    progress += 1
                    if progress % 500 == 0:
                        print(f"    [{progress}/{total_combos}] winners so far: {len(mgmt_rows)}", flush=True)
                    results = []
                    for t in triggers_for_pat.iter_rows(named=True):
                        r = simulate_or_fixed(
                            t["trigger_ts"], t["trigger_close"], direction,
                            sl, rr, t["or_width"],
                            times_list, times_arr, highs, lows, max_hold_min,
                        )
                        if r is not None:
                            results.append(r - FRICTION_R)
                    if len(results) < MIN_TRADES:
                        continue
                    arr = np.asarray(results)
                    wins = arr[arr > 0].sum()
                    losses = -arr[arr < 0].sum()
                    pf = float(wins / losses) if losses > 0 else (float("inf") if wins > 0 else 0.0)
                    wr = float((arr > 0).mean())
                    expectancy = float(arr.mean())
                    cum = np.cumsum(arr)
                    dd = float((np.maximum.accumulate(cum) - cum).max()) if len(cum) else 0.0
                    tpy = len(arr) / max(span_days / 365.25, 1e-9)
                    if (pf >= MIN_PF and wr >= MIN_WR and expectancy > MIN_EXPECTANCY
                            and tpy >= MIN_TRADES_PER_YEAR):
                        mgmt_rows.append({
                            "sym": sym, "magic_time": mt, "or_dur": or_dur,
                            "pattern_id": pid, "direction": direction,
                            "mode": "OR_FIXED", "sl_or_frac": sl, "rr": rr,
                            "trades": len(arr), "tpy": tpy,
                            "win_rate": wr, "pf": pf, "expectancy_r": expectancy,
                            "max_dd_r": dd, "sum_r": float(arr.sum()),
                        })

    mgmt_df = pl.DataFrame(mgmt_rows) if mgmt_rows else pl.DataFrame()
    print(f"\n{'='*60}", flush=True)
    print(f"WINNERS (PF>={MIN_PF}, WR>={MIN_WR}, exp>{MIN_EXPECTANCY}, tpy>={MIN_TRADES_PER_YEAR}): {len(mgmt_df)}", flush=True)
    print(f"{'='*60}", flush=True)

    if len(mgmt_df) == 0:
        print("No winners. Try relaxing filters or check data.")
        return

    mgmt_df.write_parquet(base / "amo8_discovery_v2_winners.parquet")

    # Per-symbol summary
    print("\nPer-symbol breakdown:")
    sym_summary = mgmt_df.group_by("sym").agg([
        pl.len().alias("n_winners"),
        pl.col("pf").max().alias("max_pf"),
        pl.col("pf").median().alias("med_pf"),
        pl.col("win_rate").max().alias("max_wr"),
        pl.col("tpy").sum().alias("sum_tpy"),
    ]).sort("n_winners", descending=True)
    print(sym_summary)

    print("\nPer-magic_time breakdown:")
    mt_summary = mgmt_df.group_by("magic_time").agg([
        pl.len().alias("n_winners"),
        pl.col("pf").max().alias("max_pf"),
    ]).sort("n_winners", descending=True)
    print(mt_summary)

    print("\nTop 25 winners by PF:")
    top = mgmt_df.sort("pf", descending=True).head(25)
    for r in top.iter_rows(named=True):
        print(f"  {r['sym']:<10} mt={r['magic_time']} dur={r['or_dur']:>3}m  {r['direction']:<5}  "
              f"sl_or={r['sl_or_frac']} rr={r['rr']}  PF={r['pf']:.2f} WR={r['win_rate']*100:.1f}% "
              f"tpy={r['tpy']:.0f} exp={r['expectancy_r']:.3f}R  pid={r['pattern_id']}")

    # Markdown report
    lines = [
        "# AMO8 Discovery V2 — 15 symbols × 4 magic_times × 4 OR_durations",
        f"\n**Filters:** PF>={MIN_PF}, WR>={MIN_WR}, exp>{MIN_EXPECTANCY}R, tpy>={MIN_TRADES_PER_YEAR}, friction={FRICTION_R}R",
        f"**Triggers:** {len(df)}",
        f"**Pattern slots with >={MIN_TRADES} triggers:** {len(pat_counts)}",
        f"**Mgmt combos simulated:** {total_combos:,}",
        f"**Winners:** {len(mgmt_df)}",
        "",
        "## Per-symbol",
        sym_summary.to_pandas().to_markdown(index=False),
        "",
        "## Per-magic_time",
        mt_summary.to_pandas().to_markdown(index=False),
        "",
        "## Top 50 winners by PF",
        mgmt_df.sort("pf", descending=True).head(50).to_pandas().to_markdown(index=False),
    ]
    (base / "AMO8_Discovery_V2.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport: reports/orb/AMO8_Discovery_V2.md")


if __name__ == "__main__":
    main()
