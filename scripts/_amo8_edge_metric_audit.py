"""Re-score the AMO8 deployed patterns under 3 different edge metrics to test
whether the edge is REAL (geometric) or an ARTIFACT of the deflated ATR.

Variants:
  V1: ATR-bucketed + R-units scoring (mfe / (atr*0.5))        ← original
  V2: ATR-bucketed + OR-width-relative scoring (mfe / or_width) ← ATR-free exit metric
  V3: OR-width-pctl bucketed + OR-width-relative scoring         ← fully ATR-free

For each variant we apply Phase A filters:
  count_per_year >= 30  AND  edge_score >= 0.15
  AND p50_mfe >= 0.5  AND p50_mae <= 2.0
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

cfg = json.loads(Path("src/execution/bot_config_amo8.json").read_text())
ports = cfg["portfolio"]
deployed_slots = sorted({(s["internal_sym"], s["magic_time"], int(s["or_duration_min"])) for s in ports})
deployed_patterns = sorted({(s["internal_sym"], s["or_duration_min"], s["pattern_id"], s["direction"]) for s in ports})
print(f"Deployed slots: {len(deployed_slots)}")
print(f"Unique (sym, dur, pattern_id, dir) combos in config: {len(deployed_patterns)}")
print()

SYM_TO_FILE = {
    "XAUUSD":"data/enriched_math_tf/XAUUSD_M15.parquet",
    "GBPUSD":"data/enriched_math_tf/GBPUSD_M15.parquet",
    "NASDAQ100":"data/enriched_math_tf/NASDAQ100_M15.parquet",
    "NATGAS":"data/enriched_math_tf/NATGAS_M15.parquet",
    "SP500":"data/enriched_math_tf/SP500_M15.parquet",
}
SYM_TO_M1 = {k: v.replace("_M15.parquet","_M1.parquet") for k,v in SYM_TO_FILE.items()}

HORIZON_MIN = 240

def mfe_mae_walk(trigger_ts, entry, m1_times_arr, m1_highs, m1_lows, horizon_min):
    n = len(m1_times_arr)
    times_list = list(m1_times_arr)
    start = bisect.bisect_right(times_list, trigger_ts)
    if start >= n:
        return None
    horizon = trigger_ts + timedelta(minutes=horizon_min)
    end = start
    while end < n and m1_times_arr[end] <= horizon:
        end += 1
    if end <= start:
        return None
    window_h = m1_highs[start:end]
    window_l = m1_lows[start:end]
    return {
        "mfe_long": float(window_h.max() - entry),
        "mae_long": float(entry - window_l.min()),
    }

triggers_all = []
for (sym, mt, or_dur) in deployed_slots:
    print(f"  scanning {sym} {mt}/{or_dur}m...", flush=True)
    # Read only the columns we need to keep memory + I/O low
    m15 = pl.scan_parquet(SYM_TO_FILE[sym]).select(["time","open","high","low","close"]).sort("time").collect()
    m1 = pl.scan_parquet(SYM_TO_M1[sym]).select(["time","high","low","close"]).sort("time").collect()
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
    # OR-width percentile bucket (scheme 2)
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

    m1_sorted = m1.sort("time")
    m1_times = m1_sorted["time"].to_list()
    m1_times_arr = np.array(m1_times, dtype="object")
    m1_highs = np.asarray(m1_sorted["high"].to_list(), dtype=float)
    m1_lows = np.asarray(m1_sorted["low"].to_list(), dtype=float)
    m1_closes = np.asarray(m1_sorted["close"].to_list(), dtype=float)

    span_first = None
    span_last = None
    for row in per_day.iter_rows(named=True):
        or_close_ts = row["or_close_ts"]
        if span_first is None or or_close_ts < span_first: span_first = or_close_ts
        if span_last is None or or_close_ts > span_last: span_last = or_close_ts
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
            atr_at_setup=row["atr_14"], m1=day_slice,
        )
        for ev in events:
            mfe = mfe_mae_walk(ev["trigger_ts"], ev["trigger_close"], m1_times_arr, m1_highs, m1_lows, HORIZON_MIN)
            if not mfe:
                continue
            triggers_all.append({
                "sym": sym, "or_dur": or_dur, "magic_time": mt,
                "event": ev["event_type"], "or_position": row["or_position"] or "NONE",
                "bkt_atr": row["bkt_atr"] or "NONE",
                "bkt_or": row["bkt_or"] or "NONE",
                "pd_or_bucket": row["pd_or_bucket"] or "NONE",
                "atr_14": float(row["atr_14"]), "or_width": float(row["or_width"]),
                "mfe_long": mfe["mfe_long"], "mae_long": mfe["mae_long"],
                "mfe_short": mfe["mae_long"], "mae_short": mfe["mfe_long"],
            })
    if span_first and span_last:
        print(f"     span: {span_first.date()} -> {span_last.date()}")

df = pl.DataFrame(triggers_all)
print(f"\n{len(df)} total triggers across {len(deployed_slots)} slots")

# Per-symbol span_days for tpy
span_days_by_sym = {}
for (sym, mt, or_dur) in deployed_slots:
    sub = df.filter((pl.col("sym")==sym) & (pl.col("or_dur")==or_dur))
    if len(sub) > 0:
        span_days_by_sym[(sym, or_dur)] = 8 * 365  # 8-year backtest approx

print()

def aggregate_pattern(df_long_or_short, direction_label, scale_col, bkt_col, mfe_col, mae_col):
    d = df_long_or_short.with_columns([
        (pl.col(mfe_col) / pl.col(scale_col)).alias("mfe_m"),
        (pl.col(mae_col) / pl.col(scale_col)).alias("mae_m"),
        pl.concat_str([pl.col("event"), pl.col("or_position"), pl.col(bkt_col), pl.col("pd_or_bucket")], separator="_").alias("pattern_id"),
    ]).filter(pl.col("scale_l").is_not_null() & (pl.col("scale_l") > 0))
    if "scale_l" in d.columns:
        d = d.filter(pl.col("scale_l") > 0)
    by_pat = d.group_by(["sym","or_dur","pattern_id"]).agg([
        pl.len().alias("count"),
        pl.col("mfe_m").quantile(0.50).alias("p50_mfe"),
        pl.col("mae_m").quantile(0.50).alias("p50_mae"),
    ]).with_columns([
        pl.lit(direction_label).alias("direction"),
        (pl.col("p50_mfe") - pl.col("p50_mae")).alias("edge_score"),
        (pl.col("count") / 8.0).alias("count_per_year"),  # 8 years approx
    ])
    return by_pat

variants = [
    ("V1: ATR-bucket + R-units (mfe/(atr*0.5))", "bkt_atr", "atr_half"),
    ("V2: ATR-bucket + OR-width scoring",        "bkt_atr", "or_width"),
    ("V3: OR-pctl bucket + OR-width scoring",    "bkt_or",  "or_width"),
]

deployed_set = set(deployed_patterns)

print(f"{'Variant':<45}  {'#total':>8}  {'#pass':>8}  {'#dep_match':>11}  {'%dep_kept':>10}")
print("-" * 95)
for vname, bkt_col, scale_kind in variants:
    if scale_kind == "atr_half":
        df_scaled = df.with_columns([(pl.col("atr_14") * 0.5).alias("scale_l")])
    else:
        df_scaled = df.with_columns([pl.col("or_width").alias("scale_l")])

    long_agg = aggregate_pattern(df_scaled, "LONG", "scale_l", bkt_col, "mfe_long", "mae_long")
    short_agg = aggregate_pattern(df_scaled, "SHORT", "scale_l", bkt_col, "mfe_short", "mae_short")
    agg = pl.concat([long_agg, short_agg])
    passing = agg.filter(
        (pl.col("count_per_year") >= 30)
        & (pl.col("edge_score") >= 0.15)
        & (pl.col("p50_mfe") >= 0.5)
        & (pl.col("p50_mae") <= 2.0)
    )
    n_match = sum(1 for r in passing.iter_rows(named=True)
                  if (r["sym"], r["or_dur"], r["pattern_id"], r["direction"]) in deployed_set)
    pct_kept = n_match / max(len(deployed_set), 1) * 100
    print(f"  {vname:<43}  {len(agg):>8}  {len(passing):>8}  {n_match:>11}  {pct_kept:>9.0f}%")

print()
print("Interpretation guide:")
print("  V1 ~84 deployed_match → confirms our metric replicates original Phase A.")
print("  V2 deployed_match vs V1 → reveals how many configs are due to R-unit inflation by deflated ATR.")
print("  V3 deployed_match vs V2 → reveals additional shift from re-bucketing.")
print()
print("If V3 deployed_match << V1, the edge was largely an artifact of ATR.")
print("If V3 deployed_match ~ V1, the edge is real and only the bucketing/metric needs fixing.")
