"""Full ATR-free AMO8 discovery: explore all (sym × magic_time × or_dur × event × state)
combinations and score with metrics that are independent of the deflated ATR.

Universe (matches the original spec but limited to deployed-symbol universe):
  - 5 symbols: XAUUSD, GBPUSD, NASDAQ100, NATGAS, SP500
  - 4 magic_times: 00:00, 07:00, 12:30, 22:00 (UTC)
  - 4 OR durations: 15m, 30m, 60m, 120m
  → 5 × 4 × 4 = 80 slots

For each slot, detect 8 event types over 8 years (2018-2026), aggregate per
pattern_id with TWO bucket schemes and TWO metric schemes:
  buckets: (a) original ATR-based 0.3/0.7, (b) rolling 90d OR_width percentile
  metric: (1) mfe/mae as OR_width fraction, (2) mfe/mae in absolute price units

Then for the survivors, simulate OR_FIXED management grid
(sl_or ∈ {0.5, 1.0, 1.5} × rr ∈ {1.0, 1.5, 2.0, 3.0}) → 12 combos per pattern.

Output:
  reports/orb/amo8_discovery_atr_free.parquet  (all combos with metrics)
  reports/orb/AMO8_Discovery_ATR_Free.md       (human-readable report)
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

SYMBOLS = ["XAUUSD", "GBPUSD", "NASDAQ100", "NATGAS", "SP500"]
MAGIC_TIMES = ["00:00", "07:00", "12:30", "22:00"]
OR_DURATIONS = [15, 30, 60, 120]
HORIZON_MIN = 240
SL_OR_GRID = [0.5, 1.0, 1.5]
RR_GRID = [1.0, 1.5, 2.0, 3.0]

# Filters
MIN_TRADES_PER_YEAR = 30
MIN_PF = 1.2
MIN_WR = 0.55
MIN_EXPECTANCY = 0.10

SYM_TO_M15 = {s: f"data/enriched_math_tf/{s}_M15.parquet" for s in SYMBOLS}
SYM_TO_M1 = {s: f"data/enriched_math_tf/{s}_M1.parquet" for s in SYMBOLS}


def load_m1(sym: str) -> tuple[list, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    print(f"  loading M1 for {sym}...", flush=True)
    m1 = pl.scan_parquet(SYM_TO_M1[sym]).select(["time","high","low","close"]).sort("time").collect()
    times_list = m1["time"].to_list()
    times_arr = np.array(times_list, dtype="object")
    highs = np.asarray(m1["high"].to_list(), dtype=float)
    lows = np.asarray(m1["low"].to_list(), dtype=float)
    closes = np.asarray(m1["close"].to_list(), dtype=float)
    print(f"     M1 loaded: {len(times_list)} bars", flush=True)
    return times_list, times_arr, highs, lows, closes


def mfe_mae(trigger_ts, entry, times_list, times_arr, highs, lows, horizon_min):
    start = bisect.bisect_right(times_list, trigger_ts)
    if start >= len(times_list):
        return None
    horizon = trigger_ts + timedelta(minutes=horizon_min)
    end = start
    n = len(times_arr)
    while end < n and times_arr[end] <= horizon:
        end += 1
    if end <= start:
        return None
    return {
        "mfe_long": float(highs[start:end].max() - entry),
        "mae_long": float(entry - lows[start:end].min()),
    }


def simulate_or_fixed(trigger_ts, entry, direction, sl_or_frac, rr, or_width,
                      times_list, times_arr, highs, lows, max_hold_min):
    """OR_FIXED single-target walker. Returns realized_r."""
    sign = 1.0 if direction == "LONG" else -1.0
    sl_dist = sl_or_frac * or_width
    tp_dist = rr * sl_dist
    if sl_dist <= 0:
        return None
    sl_price = entry - sign * sl_dist
    tp_price = entry + sign * tp_dist
    start = bisect.bisect_right(times_list, trigger_ts)
    if start >= len(times_list):
        return None
    horizon = trigger_ts + timedelta(minutes=max_hold_min)
    n = len(times_arr)
    for j in range(start, n):
        if times_arr[j] > horizon:
            return 0.0  # timeout at neutral
        hi = highs[j]; lo = lows[j]
        # SL-first conservative
        if direction == "LONG":
            if lo <= sl_price:
                return -1.0
            if hi >= tp_price:
                return float(rr)
        else:
            if hi >= sl_price:
                return -1.0
            if lo <= tp_price:
                return float(rr)
    return 0.0  # ran out of data


def main():
    base = Path("reports/orb")
    base.mkdir(parents=True, exist_ok=True)
    all_triggers = []
    span_days_per_slot = {}

    for sym in SYMBOLS:
        m15 = pl.scan_parquet(SYM_TO_M15[sym]).select(["time","open","high","low","close"]).sort("time").collect()
        times_list, times_arr, highs, lows, closes = load_m1(sym)

        for mt in MAGIC_TIMES:
            for or_dur in OR_DURATIONS:
                print(f"  scanning {sym} mt={mt} dur={or_dur}m...", flush=True)
                enriched = DataEnricher.enrich_with_daily_context(m15, "00:00", "23:59")
                enriched_or = DataEnricher.enrich_with_opening_range(enriched, mt, or_dur)
                enriched_or = enriched_or.with_columns([
                    pl.when(pl.col("or_atr_ratio").is_null()).then(pl.lit(None, dtype=pl.Utf8))
                      .when(pl.col("or_atr_ratio") <= 0.3).then(pl.lit("compressed"))
                      .when(pl.col("or_atr_ratio") >= 0.7).then(pl.lit("expanded"))
                      .otherwise(pl.lit("normal")).alias("bkt_atr"),
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
                        pl.col("bkt_atr").first(),
                        pl.col("pd_or_bucket").first(),
                        pl.col("atr_14").first(),
                        pl.col("or_width_calc").first().alias("or_width"),
                    ]).filter(pl.col("atr_14").is_not_null() & (pl.col("atr_14")>0)
                               & pl.col("or_high").is_not_null() & pl.col("or_low").is_not_null())
                    .sort("trade_date"))
                # OR-width percentile bucket
                per_day = per_day.with_columns([
                    pl.col("or_width").rolling_quantile(0.30, window_size=90, min_samples=20).shift(1).alias("_q30"),
                    pl.col("or_width").rolling_quantile(0.70, window_size=90, min_samples=20).shift(1).alias("_q70"),
                ])
                per_day = per_day.with_columns([
                    pl.when(pl.col("or_width").is_null()).then(pl.lit(None, dtype=pl.Utf8))
                      .when(pl.col("_q30").is_null()).then(pl.lit(None, dtype=pl.Utf8))
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
                        atr_at_setup=row["atr_14"], m1=day_slice,
                    )
                    for ev in events:
                        mm = mfe_mae(ev["trigger_ts"], ev["trigger_close"],
                                     times_list, times_arr, highs, lows, HORIZON_MIN)
                        if not mm:
                            continue
                        all_triggers.append({
                            "sym": sym, "magic_time": mt, "or_dur": or_dur,
                            "event": ev["event_type"],
                            "or_position": row["or_position"] or "NONE",
                            "bkt_atr": row["bkt_atr"] or "NONE",
                            "bkt_or": row["bkt_or"] or "NONE",
                            "pd_or_bucket": row["pd_or_bucket"] or "NONE",
                            "or_width": float(row["or_width"]),
                            "atr_14": float(row["atr_14"]),
                            "trigger_ts": ev["trigger_ts"],
                            "trigger_close": float(ev["trigger_close"]),
                            "mfe_long": mm["mfe_long"],
                            "mae_long": mm["mae_long"],
                        })
                        slot_triggers += 1
                print(f"     {slot_triggers} triggers", flush=True)

    df = pl.DataFrame(all_triggers)
    print(f"\n{len(df)} total triggers collected across {len(SYMBOLS)} symbols x {len(MAGIC_TIMES)} mt x {len(OR_DURATIONS)} dur\n", flush=True)
    df.write_parquet(base / "amo8_discovery_triggers.parquet")

    # Score patterns under V3 (OR-width pctl bucket + OR-width relative metric)
    print("Scoring patterns under ATR-free metric V3...", flush=True)
    rows = []
    for direction in ["LONG", "SHORT"]:
        # Use OR_FIXED simulation per pattern × per (sl, rr) combo
        scored = df.with_columns([
            pl.concat_str([
                pl.col("event"), pl.col("or_position"), pl.col("bkt_or"), pl.col("pd_or_bucket"),
            ], separator="_").alias("pattern_id"),
        ])
        # Group by slot + pattern, count per year
        by_pat = scored.group_by(["sym","magic_time","or_dur","pattern_id"]).agg([
            pl.len().alias("count"),
            pl.col("mfe_long").quantile(0.50).alias("p50_mfe_abs"),
            pl.col("mae_long").quantile(0.50).alias("p50_mae_abs"),
            (pl.col("mfe_long") / pl.col("or_width")).quantile(0.50).alias("p50_mfe_or"),
            (pl.col("mae_long") / pl.col("or_width")).quantile(0.50).alias("p50_mae_or"),
        ])
        for row in by_pat.iter_rows(named=True):
            sym = row["sym"]; mt = row["magic_time"]; or_dur = row["or_dur"]
            span_days = span_days_per_slot.get((sym, mt, or_dur), 8 * 365)
            count = row["count"]
            tpy = count / max(span_days / 365.25, 1e-9)
            # Direction adjustment for SHORT: flip mfe/mae
            if direction == "LONG":
                p50_mfe_or = row["p50_mfe_or"]; p50_mae_or = row["p50_mae_or"]
            else:
                p50_mfe_or = row["p50_mae_or"]; p50_mae_or = row["p50_mfe_or"]
            edge_or = p50_mfe_or - p50_mae_or
            rows.append({
                "sym": sym, "magic_time": mt, "or_dur": or_dur,
                "pattern_id": row["pattern_id"], "direction": direction,
                "count": count, "tpy": tpy,
                "p50_mfe_or": p50_mfe_or, "p50_mae_or": p50_mae_or,
                "edge_or": edge_or,
            })

    edge_df = pl.DataFrame(rows)
    # Filter: tpy >= 30 AND edge_or > 0.2 AND p50_mfe_or >= 0.5
    survivors = edge_df.filter(
        (pl.col("tpy") >= MIN_TRADES_PER_YEAR)
        & (pl.col("edge_or") >= 0.2)
        & (pl.col("p50_mfe_or") >= 0.5)
    ).sort("edge_or", descending=True)

    print(f"Edge survivors (before management grid): {len(survivors)}", flush=True)
    survivors.write_parquet(base / "amo8_discovery_edge_survivors.parquet")

    # Now simulate OR_FIXED management grid for each survivor
    print("Running OR_FIXED management grid...", flush=True)
    mgmt_rows = []
    by_sym = {}
    for sym in SYMBOLS:
        if sym not in by_sym:
            by_sym[sym] = load_m1(sym)

    for surv in survivors.iter_rows(named=True):
        sym = surv["sym"]; mt = surv["magic_time"]; or_dur = surv["or_dur"]
        pid = surv["pattern_id"]; direction = surv["direction"]
        triggers_for_pat = df.filter(
            (pl.col("sym")==sym) & (pl.col("magic_time")==mt) & (pl.col("or_dur")==or_dur)
        ).with_columns([
            pl.concat_str([
                pl.col("event"), pl.col("or_position"), pl.col("bkt_or"), pl.col("pd_or_bucket"),
            ], separator="_").alias("pattern_id"),
        ]).filter(pl.col("pattern_id") == pid)
        if len(triggers_for_pat) < 10:
            continue
        times_list, times_arr, highs, lows, closes = by_sym[sym]
        max_hold_min = 10 * or_dur
        span_days = span_days_per_slot.get((sym, mt, or_dur), 8*365)
        for sl in SL_OR_GRID:
            for rr in RR_GRID:
                results = []
                for t in triggers_for_pat.iter_rows(named=True):
                    r = simulate_or_fixed(
                        t["trigger_ts"], t["trigger_close"], direction,
                        sl, rr, t["or_width"], times_list, times_arr, highs, lows, max_hold_min,
                    )
                    if r is not None:
                        # Apply friction: 0.2R floor + commission proxy 0.1R
                        results.append(r - 0.3)
                if len(results) < 10:
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
                if (pf >= MIN_PF and wr >= MIN_WR and expectancy >= MIN_EXPECTANCY and tpy >= MIN_TRADES_PER_YEAR):
                    mgmt_rows.append({
                        "sym": sym, "magic_time": mt, "or_dur": or_dur,
                        "pattern_id": pid, "direction": direction,
                        "mode": "OR_FIXED", "sl_or_frac": sl, "rr": rr,
                        "trades": len(arr), "tpy": tpy,
                        "win_rate": wr, "pf": pf, "expectancy_r": expectancy,
                        "max_dd_r": dd, "sum_r": float(arr.sum()),
                    })

    mgmt_df = pl.DataFrame(mgmt_rows)
    print(f"\nManagement winners (PF>={MIN_PF}, WR>={MIN_WR}, exp>={MIN_EXPECTANCY}, tpy>={MIN_TRADES_PER_YEAR}): {len(mgmt_df)}", flush=True)
    mgmt_df.write_parquet(base / "amo8_discovery_atr_free.parquet")

    # Compact report
    if len(mgmt_df) > 0:
        top = mgmt_df.sort("pf", descending=True).head(30)
        lines = [
            "# AMO8 Discovery — ATR-Free (5 sym × 4 magic_time × 4 OR_dur)",
            "",
            f"**Triggers collected:** {len(df)}",
            f"**Edge survivors (pattern-level):** {len(survivors)}",
            f"**Management winners (PF>={MIN_PF}, WR>={MIN_WR}, tpy>={MIN_TRADES_PER_YEAR}):** {len(mgmt_df)}",
            "",
            "## Per (sym, magic_time, or_dur) — winner count",
            "",
            mgmt_df.group_by(["sym","magic_time","or_dur"]).agg([
                pl.len().alias("n_winners"),
                pl.col("pf").max().alias("max_pf"),
                pl.col("win_rate").max().alias("max_wr"),
            ]).sort("n_winners", descending=True).to_pandas().to_markdown(index=False),
            "",
            "## Top 30 winners by PF",
            "",
            top.to_pandas().to_markdown(index=False),
        ]
        (base / "AMO8_Discovery_ATR_Free.md").write_text("\n".join(lines), encoding="utf-8")
        print(f"Report written: {base / 'AMO8_Discovery_ATR_Free.md'}")
    else:
        print("No management winners — check filters / data.")


if __name__ == "__main__":
    main()
