# Post-Fade Edge Analysis & Feature Relationships — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the ORB analysis pipeline to discover post-false-breakout patterns (shakeout reversals, continuations) and feature-conditional edges (RSI, OR position vs PD levels, ATR context), generating comprehensive per-asset reports.

**Architecture:** Organic extension of the existing 4-layer pipeline: `DataEnricher` gets RSI + positional features → `TrackerEngine` gets post-fade event tracking → `StatisticalEngine` gets new edge calculations + feature-conditional segmentation → `ReportGenerator` + `QuantTeam` get new report sections. No new files created.

**Tech Stack:** Python 3.12, Polars (vectorized, no row-level loops)

---

## File Structure

| File | Change | Responsibility |
|---|---|---|
| `src/application/calculators.py` | Modify | Add RSI(14) M15, RSI(14) daily, OR position vs PD, ATR change/percentile |
| `src/application/trackers.py` | Modify | Add post-fade event tracking (extensions + timing after SL hit) |
| `src/application/statistics.py` | Modify | Add post-fade edges, feature-conditional edges, timing stats |
| `src/application/quant_team.py` | Modify | Add SHAKEOUT-REVERSAL, RSI-CONDITIONAL, CONTEXT-BOOST archetypes |
| `src/engine/report_generator.py` | Modify | Add post-fade anatomy, feature table, timing sections; pass new features through pipeline |

---

### Task 1: Add RSI(14) M15 to DataEnricher

**Files:**
- Modify: `src/application/calculators.py`

- [ ] **Step 1: Add RSI calculation method to DataEnricher**

Add this static method to the `DataEnricher` class, after `enrich_with_opening_range`:

```python
@staticmethod
def enrich_with_rsi(df: pl.DataFrame, period: int = 14) -> pl.DataFrame:
    """
    Calculates RSI(14) over M15 close prices using Wilder's smoothing (EMA).
    No look-ahead bias: RSI at bar N uses only bars 0..N.
    """
    df = df.sort("time")
    delta = pl.col("close") - pl.col("close").shift(1)
    df = df.with_columns([
        pl.when(delta > 0).then(delta).otherwise(0.0).alias("_rsi_gain"),
        pl.when(delta < 0).then(delta.abs()).otherwise(0.0).alias("_rsi_loss"),
    ])
    # Wilder's smoothing = EMA with alpha = 1/period
    alpha = 1.0 / period
    df = df.with_columns([
        pl.col("_rsi_gain").ewm_mean(alpha=alpha, adjust=False, min_periods=period).alias("_avg_gain"),
        pl.col("_rsi_loss").ewm_mean(alpha=alpha, adjust=False, min_periods=period).alias("_avg_loss"),
    ])
    df = df.with_columns([
        pl.when(pl.col("_avg_loss") == 0)
        .then(100.0)
        .otherwise(100.0 - (100.0 / (1.0 + pl.col("_avg_gain") / pl.col("_avg_loss"))))
        .alias("rsi_14")
    ])
    # Clean up temp columns
    df = df.drop(["_rsi_gain", "_rsi_loss", "_avg_gain", "_avg_loss"])
    return df
```

- [ ] **Step 2: Verify RSI calculation runs without error**

Open a Python shell and run:
```bash
cd C:/Proyectos/kha0sys3 && python -c "
from src.infrastructure.data.polars_loader import CSVPolarsLoader
from src.application.calculators import DataEnricher
loader = CSVPolarsLoader('data')
df = loader.load_data('EURUSD', 'M15')
df = DataEnricher.enrich_with_rsi(df)
print(df.select(['time','close','rsi_14']).tail(10))
print(f'RSI range: {df[\"rsi_14\"].min():.1f} - {df[\"rsi_14\"].max():.1f}')
"
```
Expected: RSI values between 0-100, no nulls after first ~14 bars.

- [ ] **Step 3: Commit**

```bash
git add src/application/calculators.py
git commit -m "feat: add RSI(14) M15 calculation to DataEnricher"
```

---

### Task 2: Add RSI Daily + OR Position Features + ATR Context to DataEnricher

**Files:**
- Modify: `src/application/calculators.py`

- [ ] **Step 1: Add daily RSI to `enrich_with_daily_context`**

In the `enrich_with_daily_context` method, after the ATR(14) calculation (after line 57 where `atr_14` is created), add:

```python
# RSI(14) daily based on d_close
delta_close = pl.col("d_close") - pl.col("d_close").shift(1)
daily_df = daily_df.with_columns([
    pl.when(delta_close > 0).then(delta_close).otherwise(0.0).alias("_d_gain"),
    pl.when(delta_close < 0).then(delta_close.abs()).otherwise(0.0).alias("_d_loss"),
])
d_alpha = 1.0 / 14
daily_df = daily_df.with_columns([
    pl.col("_d_gain").ewm_mean(alpha=d_alpha, adjust=False, min_periods=14).alias("_d_avg_gain"),
    pl.col("_d_loss").ewm_mean(alpha=d_alpha, adjust=False, min_periods=14).alias("_d_avg_loss"),
])
daily_df = daily_df.with_columns([
    pl.when(pl.col("_d_avg_loss") == 0)
    .then(100.0)
    .otherwise(100.0 - (100.0 / (1.0 + pl.col("_d_avg_gain") / pl.col("_d_avg_loss"))))
    .shift(1)  # shift(1) to avoid look-ahead: use YESTERDAY's RSI
    .alias("rsi_daily_14")
])
daily_df = daily_df.drop(["_d_gain", "_d_loss", "_d_avg_gain", "_d_avg_loss"])

# ATR change vs previous day
daily_df = daily_df.with_columns([
    ((pl.col("atr_14") - pl.col("atr_14").shift(1)) / pl.col("atr_14").shift(1)).alias("atr_change")
])

# ATR percentile (rolling 50 days)
daily_df = daily_df.with_columns([
    pl.col("atr_14").rolling_quantile(quantile=0.5, window_size=50).alias("_atr_median_50")
])
daily_df = daily_df.with_columns([
    pl.col("atr_14").rolling_map(
        function=lambda s: (s[-1:].item() > s).sum() / len(s) * 100,
        window_size=50
    ).alias("atr_percentile")
])
daily_df = daily_df.drop(["_atr_median_50"])
```

Update the `select` in the join (around line 61) to include the new columns:

```python
enriched_m15 = df.join(
    daily_df.select(["trade_date", "pd_high", "pd_low", "pd_close", "pd_open", "pd_mid", 
                      "atr_14", "rsi_daily_14", "atr_change", "atr_percentile"]),
    on="trade_date",
    how="left"
)
```

- [ ] **Step 2: Add OR positional features to `enrich_with_opening_range`**

In `enrich_with_opening_range`, after the `or_atr_ratio` calculation (after line 117), add:

```python
# OR position relative to Previous Day levels
res_df = res_df.with_columns([
    # Categorical position
    pl.when(pl.col("or_open") > pl.col("pd_high"))
    .then(pl.lit("ABOVE_PD_HIGH"))
    .when(pl.col("or_open") < pl.col("pd_low"))
    .then(pl.lit("BELOW_PD_LOW"))
    .when(
        (pl.col("or_open") >= pl.col("pd_close")) & 
        (pl.col("or_open") <= pl.col("pd_high"))
    )
    .then(pl.lit("BETWEEN_CLOSE_AND_HIGH"))
    .when(
        (pl.col("or_open") >= pl.col("pd_low")) & 
        (pl.col("or_open") < pl.col("pd_close"))
    )
    .then(pl.lit("BETWEEN_LOW_AND_CLOSE"))
    .otherwise(pl.lit("INSIDE_PD_RANGE"))
    .alias("or_position_vs_pd"),
    
    # Normalized distances
    ((pl.col("or_open") - pl.col("pd_close")) / pl.col("atr_14")).alias("or_open_vs_pd_close"),
    ((pl.col("or_open") - pl.col("pd_mid")) / pl.col("atr_14")).alias("or_open_vs_pd_mid"),
    ((pl.col("or_high") - pl.col("pd_high")) / pl.col("atr_14")).alias("or_high_vs_pd_high"),
    ((pl.col("or_low") - pl.col("pd_low")) / pl.col("atr_14")).alias("or_low_vs_pd_low"),
])
```

- [ ] **Step 3: Capture `rsi_at_or_close` in `enrich_with_opening_range`**

This requires the RSI column to be present in the dataframe. In the `or_stats` calculation (around line 91), the OR candles group-by should also capture the last RSI:

Replace the existing `or_stats` aggregation block:

```python
or_candles = df.filter(
    (pl.col("mins_from_midnight") >= start_td) & 
    (pl.col("mins_from_midnight") < end_td)
)

# Build aggregation list - RSI column may not be present
agg_exprs = [
    pl.col("high").max().alias("or_high"),
    pl.col("low").min().alias("or_low"),
    pl.col("open").first().alias("or_open"),
]
if "rsi_14" in df.columns:
    agg_exprs.append(pl.col("rsi_14").last().alias("rsi_at_or_close"))

or_stats = or_candles.group_by("trade_date").agg(agg_exprs).sort("trade_date")
```

- [ ] **Step 4: Verify all new features compute correctly**

```bash
cd C:/Proyectos/kha0sys3 && python -c "
from src.infrastructure.data.polars_loader import CSVPolarsLoader
from src.application.calculators import DataEnricher
loader = CSVPolarsLoader('data')
df = loader.load_data('EURUSD', 'M15')
df = DataEnricher.enrich_with_rsi(df)
df = DataEnricher.enrich_with_daily_context(df, '00:00', '23:59')
df = DataEnricher.enrich_with_opening_range(df, '07:00', 15)
print('Columns:', sorted(df.columns))
print(df.select(['trade_date','rsi_at_or_close','rsi_daily_14','or_position_vs_pd','atr_change','atr_percentile','or_open_vs_pd_close']).drop_nulls().tail(5))
"
```
Expected: All new columns present with reasonable values.

- [ ] **Step 5: Commit**

```bash
git add src/application/calculators.py
git commit -m "feat: add RSI daily, ATR context, OR positional features to DataEnricher"
```

---

### Task 3: Add Post-Fade Event Tracking to TrackerEngine

**Files:**
- Modify: `src/application/trackers.py`

- [ ] **Step 1: Add post-fade tracking method**

Add this as a new static method in `TrackerEngine`, after `track_events`:

```python
@staticmethod
def track_post_fade_events(enriched_df: pl.DataFrame, stats_df: pl.DataFrame) -> pl.DataFrame:
    """
    For each day with a confirmed false breakout, tracks what happens AFTER the SL hit:
    - How far does price extend in the continuation direction (same as fade)?
    - How far does price reverse back (shakeout / re-breakout)?
    - How long until re-breakout?
    All measured from the SL hit time, within the active 8H session window.
    """
    post_or = enriched_df.filter(pl.col("is_post_or") == True)
    
    # --- FALSE BREAKOUT UP: broke OR high, then hit OR low (SL) ---
    false_up_days = stats_df.filter(
        pl.col("time_sl_up").is_not_null() &
        (pl.col("time_tp_up").is_null() | (pl.col("time_sl_up") < pl.col("time_tp_up")))
    ).select(["trade_date", "time_sl_up", "or_high", "or_low", "or_width"])
    
    post_fade_up_records = []
    for row in false_up_days.iter_rows(named=True):
        td = row["trade_date"]
        sl_time = row["time_sl_up"]
        or_high = row["or_high"]
        or_low = row["or_low"]
        or_w = row["or_width"]
        if or_w is None or or_w <= 0:
            continue
            
        # Candles AFTER the SL hit, still in active session
        post_sl = post_or.filter(
            (pl.col("trade_date") == td) &
            (pl.col("mins_from_midnight") > sl_time) &
            (pl.col("is_active_session") == True)
        )
        if post_sl.height == 0:
            continue
        
        # Max reversal UP (shakeout): how far above OR high after touching OR low
        max_high_after = post_sl.select(pl.col("high").max()).item()
        max_reversal_up = max(0, max_high_after - or_high) / or_w
        
        # Max continuation DOWN: how far below OR low after the fade
        min_low_after = post_sl.select(pl.col("low").min()).item()
        max_cont_down = max(0, or_low - min_low_after) / or_w
        
        # Time to re-breakout: first candle after SL where high > or_high
        re_break = post_sl.filter(pl.col("high") > or_high)
        time_to_rebreak = None
        if re_break.height > 0:
            time_to_rebreak = re_break.select(pl.col("mins_from_midnight").min()).item() - sl_time
        
        post_fade_up_records.append({
            "trade_date": td,
            "pf_up_max_reversal_up": max_reversal_up,
            "pf_up_max_cont_down": max_cont_down,
            "pf_up_time_to_rebreak": time_to_rebreak,
            "pf_up_rebreak_1x": max_reversal_up >= 1.0,
            "pf_up_rebreak_1_5x": max_reversal_up >= 1.5,
            "pf_up_rebreak_2x": max_reversal_up >= 2.0,
            "pf_up_cont_1x": max_cont_down >= 1.0,
            "pf_up_cont_1_5x": max_cont_down >= 1.5,
            "pf_up_cont_2x": max_cont_down >= 2.0,
        })
    
    # --- FALSE BREAKOUT DOWN: broke OR low, then hit OR high (SL) ---
    false_down_days = stats_df.filter(
        pl.col("time_sl_down").is_not_null() &
        (pl.col("time_tp_down").is_null() | (pl.col("time_sl_down") < pl.col("time_tp_down")))
    ).select(["trade_date", "time_sl_down", "or_high", "or_low", "or_width"])
    
    post_fade_down_records = []
    for row in false_down_days.iter_rows(named=True):
        td = row["trade_date"]
        sl_time = row["time_sl_down"]
        or_high = row["or_high"]
        or_low = row["or_low"]
        or_w = row["or_width"]
        if or_w is None or or_w <= 0:
            continue
            
        post_sl = post_or.filter(
            (pl.col("trade_date") == td) &
            (pl.col("mins_from_midnight") > sl_time) &
            (pl.col("is_active_session") == True)
        )
        if post_sl.height == 0:
            continue
        
        # Max reversal DOWN (shakeout): how far below OR low after touching OR high
        min_low_after = post_sl.select(pl.col("low").min()).item()
        max_reversal_down = max(0, or_low - min_low_after) / or_w
        
        # Max continuation UP: how far above OR high after the fade
        max_high_after = post_sl.select(pl.col("high").max()).item()
        max_cont_up = max(0, max_high_after - or_high) / or_w
        
        # Time to re-breakout: first candle after SL where low < or_low
        re_break = post_sl.filter(pl.col("low") < or_low)
        time_to_rebreak = None
        if re_break.height > 0:
            time_to_rebreak = re_break.select(pl.col("mins_from_midnight").min()).item() - sl_time
        
        post_fade_down_records.append({
            "trade_date": td,
            "pf_down_max_reversal_down": max_reversal_down,
            "pf_down_max_cont_up": max_cont_up,
            "pf_down_time_to_rebreak": time_to_rebreak,
            "pf_down_rebreak_1x": max_reversal_down >= 1.0,
            "pf_down_rebreak_1_5x": max_reversal_down >= 1.5,
            "pf_down_rebreak_2x": max_reversal_down >= 2.0,
            "pf_down_cont_1x": max_cont_up >= 1.0,
            "pf_down_cont_1_5x": max_cont_up >= 1.5,
            "pf_down_cont_2x": max_cont_up >= 2.0,
        })
    
    # Build DataFrames and join to stats_df
    if post_fade_up_records:
        pf_up_df = pl.DataFrame(post_fade_up_records)
        stats_df = stats_df.join(pf_up_df, on="trade_date", how="left")
    else:
        # Add null columns
        for col in ["pf_up_max_reversal_up", "pf_up_max_cont_down", "pf_up_time_to_rebreak",
                     "pf_up_rebreak_1x", "pf_up_rebreak_1_5x", "pf_up_rebreak_2x",
                     "pf_up_cont_1x", "pf_up_cont_1_5x", "pf_up_cont_2x"]:
            stats_df = stats_df.with_columns(pl.lit(None).alias(col))
    
    if post_fade_down_records:
        pf_down_df = pl.DataFrame(post_fade_down_records)
        stats_df = stats_df.join(pf_down_df, on="trade_date", how="left")
    else:
        for col in ["pf_down_max_reversal_down", "pf_down_max_cont_up", "pf_down_time_to_rebreak",
                     "pf_down_rebreak_1x", "pf_down_rebreak_1_5x", "pf_down_rebreak_2x",
                     "pf_down_cont_1x", "pf_down_cont_1_5x", "pf_down_cont_2x"]:
            stats_df = stats_df.with_columns(pl.lit(None).alias(col))
    
    return stats_df
```

- [ ] **Step 2: Verify post-fade tracking**

```bash
cd C:/Proyectos/kha0sys3 && python -c "
from src.infrastructure.data.polars_loader import CSVPolarsLoader
from src.application.calculators import DataEnricher
from src.application.trackers import TrackerEngine
loader = CSVPolarsLoader('data')
df = loader.load_data('EURUSD', 'M15')
df = DataEnricher.enrich_with_rsi(df)
df = DataEnricher.enrich_with_daily_context(df, '00:00', '23:59')
df = DataEnricher.enrich_with_opening_range(df, '07:00', 15)
stats = TrackerEngine.track_events(df, tp_multiplier=1.5)
stats = TrackerEngine.track_post_fade_events(df, stats)
# Show post-fade stats for false breakout UP days
pf = stats.filter(pl.col('pf_up_max_reversal_up').is_not_null())
print(f'False breakout UP days with post-fade data: {pf.height}')
print(pf.select(['trade_date','pf_up_max_reversal_up','pf_up_max_cont_down','pf_up_time_to_rebreak','pf_up_rebreak_1x']).head(10))
"
```
Expected: Non-zero count of post-fade days with reversal/continuation values.

- [ ] **Step 3: Commit**

```bash
git add src/application/trackers.py
git commit -m "feat: add post-fade event tracking to TrackerEngine (shakeout + continuation)"
```

---

### Task 4: Add Post-Fade Edges + Timing Stats to StatisticalEngine

**Files:**
- Modify: `src/application/statistics.py`

- [ ] **Step 1: Add post-fade edge calculations**

In `StatisticalEngine.calculate_edges()`, after the `false_breaks` dict (after line 104), add:

```python
# Post-Fade Analysis
post_fade_up = {}
pf_up_days = valid_df.filter(pl.col("pf_up_max_reversal_up").is_not_null())
if pf_up_days.height >= 5:
    post_fade_up = {
        "n_false_breakups": pf_up_days.height,
        "p_shakeout_rebreak_1x": pf_up_days.filter(pl.col("pf_up_rebreak_1x") == True).height / pf_up_days.height,
        "p_shakeout_rebreak_1_5x": pf_up_days.filter(pl.col("pf_up_rebreak_1_5x") == True).height / pf_up_days.height,
        "p_shakeout_rebreak_2x": pf_up_days.filter(pl.col("pf_up_rebreak_2x") == True).height / pf_up_days.height,
        "p_continuation_down_1x": pf_up_days.filter(pl.col("pf_up_cont_1x") == True).height / pf_up_days.height,
        "p_continuation_down_1_5x": pf_up_days.filter(pl.col("pf_up_cont_1_5x") == True).height / pf_up_days.height,
        "mean_reversal_up": pf_up_days.select(pl.col("pf_up_max_reversal_up").mean()).item(),
        "median_reversal_up": pf_up_days.select(pl.col("pf_up_max_reversal_up").median()).item(),
        "mean_cont_down": pf_up_days.select(pl.col("pf_up_max_cont_down").mean()).item(),
        "median_cont_down": pf_up_days.select(pl.col("pf_up_max_cont_down").median()).item(),
        "mean_time_to_rebreak": pf_up_days.filter(pl.col("pf_up_time_to_rebreak").is_not_null()).select(pl.col("pf_up_time_to_rebreak").mean()).item(),
        "median_time_to_rebreak": pf_up_days.filter(pl.col("pf_up_time_to_rebreak").is_not_null()).select(pl.col("pf_up_time_to_rebreak").median()).item(),
    }

post_fade_down = {}
pf_down_days = valid_df.filter(pl.col("pf_down_max_reversal_down").is_not_null())
if pf_down_days.height >= 5:
    post_fade_down = {
        "n_false_breakdowns": pf_down_days.height,
        "p_shakeout_rebreak_1x": pf_down_days.filter(pl.col("pf_down_rebreak_1x") == True).height / pf_down_days.height,
        "p_shakeout_rebreak_1_5x": pf_down_days.filter(pl.col("pf_down_rebreak_1_5x") == True).height / pf_down_days.height,
        "p_shakeout_rebreak_2x": pf_down_days.filter(pl.col("pf_down_rebreak_2x") == True).height / pf_down_days.height,
        "p_continuation_up_1x": pf_down_days.filter(pl.col("pf_down_cont_1x") == True).height / pf_down_days.height,
        "p_continuation_up_1_5x": pf_down_days.filter(pl.col("pf_down_cont_1_5x") == True).height / pf_down_days.height,
        "mean_reversal_down": pf_down_days.select(pl.col("pf_down_max_reversal_down").mean()).item(),
        "median_reversal_down": pf_down_days.select(pl.col("pf_down_max_reversal_down").median()).item(),
        "mean_cont_up": pf_down_days.select(pl.col("pf_down_max_cont_up").mean()).item(),
        "median_cont_up": pf_down_days.select(pl.col("pf_down_max_cont_up").median()).item(),
        "mean_time_to_rebreak": pf_down_days.filter(pl.col("pf_down_time_to_rebreak").is_not_null()).select(pl.col("pf_down_time_to_rebreak").mean()).item(),
        "median_time_to_rebreak": pf_down_days.filter(pl.col("pf_down_time_to_rebreak").is_not_null()).select(pl.col("pf_down_time_to_rebreak").median()).item(),
    }
```

- [ ] **Step 2: Add timing stats**

Still in `calculate_edges()`, after the post-fade block, add:

```python
# Timing to targets (in minutes from OR end)
timing = {}
# UP direction
up_with_tp = break_up_days.filter(pl.col("time_tp_up").is_not_null() & pl.col("time_entry_up").is_not_null())
if up_with_tp.height > 0:
    tp_times_up = up_with_tp.with_columns(
        (pl.col("time_tp_up") - pl.col("time_entry_up")).alias("mins_to_tp")
    )
    timing["up_mean_mins_to_tp"] = tp_times_up.select(pl.col("mins_to_tp").mean()).item()
    timing["up_median_mins_to_tp"] = tp_times_up.select(pl.col("mins_to_tp").median()).item()
    timing["up_p80_mins_to_tp"] = tp_times_up.select(pl.col("mins_to_tp").quantile(0.80)).item()

down_with_tp = break_down_days.filter(pl.col("time_tp_down").is_not_null() & pl.col("time_entry_down").is_not_null())
if down_with_tp.height > 0:
    tp_times_down = down_with_tp.with_columns(
        (pl.col("time_tp_down") - pl.col("time_entry_down")).alias("mins_to_tp")
    )
    timing["down_mean_mins_to_tp"] = tp_times_down.select(pl.col("mins_to_tp").mean()).item()
    timing["down_median_mins_to_tp"] = tp_times_down.select(pl.col("mins_to_tp").median()).item()
    timing["down_p80_mins_to_tp"] = tp_times_down.select(pl.col("mins_to_tp").quantile(0.80)).item()

# Time from breakout to SL for false breaks
up_with_sl = false_breakup_days.filter(pl.col("time_entry_up").is_not_null())
if up_with_sl.height > 0:
    sl_times_up = up_with_sl.with_columns(
        (pl.col("time_sl_up") - pl.col("time_entry_up")).alias("mins_to_sl")
    )
    timing["up_mean_mins_to_sl"] = sl_times_up.select(pl.col("mins_to_sl").mean()).item()

down_with_sl = false_breakdown_days.filter(pl.col("time_entry_down").is_not_null())
if down_with_sl.height > 0:
    sl_times_down = down_with_sl.with_columns(
        (pl.col("time_sl_down") - pl.col("time_entry_down")).alias("mins_to_sl")
    )
    timing["down_mean_mins_to_sl"] = sl_times_down.select(pl.col("mins_to_sl").mean()).item()
```

- [ ] **Step 3: Add feature-conditional edge segmentation**

Still in `calculate_edges()`, after the timing block, add:

```python
# Feature-Conditional Edge Segmentation
feature_segments = {}

def _safe_edges(sub_df, label):
    """Calculate core edges for a subset, return None if n < 20."""
    n = sub_df.height
    if n < 20:
        return None
    edges = _get_core_edges(sub_df, n)
    edges["label"] = label
    # Add post-fade shakeout rate if available
    pf_up = sub_df.filter(pl.col("pf_up_max_reversal_up").is_not_null()) if "pf_up_max_reversal_up" in sub_df.columns else pl.DataFrame()
    if hasattr(pf_up, 'height') and pf_up.height >= 5:
        edges["pf_shakeout_up"] = pf_up.filter(pl.col("pf_up_rebreak_1x") == True).height / pf_up.height
    pf_down = sub_df.filter(pl.col("pf_down_max_reversal_down").is_not_null()) if "pf_down_max_reversal_down" in sub_df.columns else pl.DataFrame()
    if hasattr(pf_down, 'height') and pf_down.height >= 5:
        edges["pf_shakeout_down"] = pf_down.filter(pl.col("pf_down_rebreak_1x") == True).height / pf_down.height
    return edges

# RSI segments (only if column exists)
if "rsi_at_or_close" in valid_df.columns:
    rsi_oversold = valid_df.filter(pl.col("rsi_at_or_close") < 30)
    rsi_overbought = valid_df.filter(pl.col("rsi_at_or_close") > 70)
    rsi_neutral = valid_df.filter(pl.col("rsi_at_or_close").is_between(30, 70))
    
    r = _safe_edges(rsi_oversold, "RSI < 30 (Oversold)")
    if r: feature_segments["rsi_oversold"] = r
    r = _safe_edges(rsi_overbought, "RSI > 70 (Overbought)")
    if r: feature_segments["rsi_overbought"] = r
    r = _safe_edges(rsi_neutral, "RSI 30-70 (Neutro)")
    if r: feature_segments["rsi_neutral"] = r

# OR Position segments
if "or_position_vs_pd" in valid_df.columns:
    for pos in ["ABOVE_PD_HIGH", "BELOW_PD_LOW", "BETWEEN_CLOSE_AND_HIGH", "BETWEEN_LOW_AND_CLOSE"]:
        sub = valid_df.filter(pl.col("or_position_vs_pd") == pos)
        r = _safe_edges(sub, f"OR {pos}")
        if r: feature_segments[f"or_pos_{pos.lower()}"] = r

# ATR change segments
if "atr_change" in valid_df.columns:
    atr_growing = valid_df.filter(pl.col("atr_change") > 0.1)
    atr_shrinking = valid_df.filter(pl.col("atr_change") < -0.1)
    r = _safe_edges(atr_growing, "ATR Creciente (>10%)")
    if r: feature_segments["atr_growing"] = r
    r = _safe_edges(atr_shrinking, "ATR Decreciente (<-10%)")
    if r: feature_segments["atr_shrinking"] = r

# ATR percentile segments
if "atr_percentile" in valid_df.columns:
    atr_q1 = valid_df.filter(pl.col("atr_percentile") < 25)
    atr_q4 = valid_df.filter(pl.col("atr_percentile") > 75)
    r = _safe_edges(atr_q1, "ATR Q1 (Baja Vol Historica)")
    if r: feature_segments["atr_q1"] = r
    r = _safe_edges(atr_q4, "ATR Q4 (Alta Vol Historica)")
    if r: feature_segments["atr_q4"] = r

# RSI Daily segments
if "rsi_daily_14" in valid_df.columns:
    rsi_d_low = valid_df.filter(pl.col("rsi_daily_14") < 35)
    rsi_d_high = valid_df.filter(pl.col("rsi_daily_14") > 65)
    r = _safe_edges(rsi_d_low, "RSI Diario < 35")
    if r: feature_segments["rsi_daily_low"] = r
    r = _safe_edges(rsi_d_high, "RSI Diario > 65")
    if r: feature_segments["rsi_daily_high"] = r
```

- [ ] **Step 4: Update the return dict**

Replace the existing return statement at the end of `calculate_edges()`:

```python
return {
    "total_evaluated_days": total_days,
    "directional": prob_dir,
    "gap_context": {
        "p_break_up_given_gap_up": p_up_given_gap_up,
        "p_break_down_given_gap_down": p_down_given_gap_down
    },
    "extensions": {
        "UP": extensions_up,
        "DOWN": extensions_down
    },
    "false_breaks": false_breaks,
    "post_fade": {
        "UP": post_fade_up,
        "DOWN": post_fade_down
    },
    "timing": timing,
    "pd_interactions": touch_stats,
    "day_of_week": dow_stats,
    "advanced_crossing": adv,
    "feature_segments": feature_segments
}
```

- [ ] **Step 5: Verify statistics compute**

```bash
cd C:/Proyectos/kha0sys3 && python -c "
from src.infrastructure.data.polars_loader import CSVPolarsLoader
from src.application.calculators import DataEnricher
from src.application.trackers import TrackerEngine
from src.application.statistics import StatisticalEngine
import polars as pl
loader = CSVPolarsLoader('data')
df = loader.load_data('EURUSD', 'M15')
df = DataEnricher.enrich_with_rsi(df)
df = DataEnricher.enrich_with_daily_context(df, '00:00', '23:59')
df_or = DataEnricher.enrich_with_opening_range(df, '07:00', 15)
stats = TrackerEngine.track_events(df_or, tp_multiplier=1.5)
daily_base = df_or.group_by('trade_date').agg([pl.col('or_open').first(), pl.col('pd_or_high').first(), pl.col('pd_or_low').first(), pl.col('rsi_at_or_close').first(), pl.col('rsi_daily_14').first(), pl.col('atr_change').first(), pl.col('atr_percentile').first(), pl.col('or_position_vs_pd').first()])
expanded = daily_base.join(stats, on='trade_date', how='left')
expanded = TrackerEngine.track_post_fade_events(df_or, expanded)
edges = StatisticalEngine.calculate_edges(expanded)
print('Post-fade UP:', edges.get('post_fade', {}).get('UP', {}))
print('Timing:', edges.get('timing', {}))
print('Feature segments:', list(edges.get('feature_segments', {}).keys()))
"
```
Expected: post_fade data with shakeout probabilities, timing values, and multiple feature segments.

- [ ] **Step 6: Commit**

```bash
git add src/application/statistics.py
git commit -m "feat: add post-fade edges, timing stats, feature-conditional segmentation to StatisticalEngine"
```

---

### Task 5: Update ReportGenerator Pipeline to Pass New Features

**Files:**
- Modify: `src/engine/report_generator.py`

- [ ] **Step 1: Update `_explore_grid` to call RSI enrichment**

In `_explore_grid`, after loading and enriching with daily context (line 31), add RSI enrichment:

```python
def _explore_grid(self, sym: str, cfg: dict):
    df_raw = self.loader.load_data(sym, "M15")
    df_raw = DataEnricher.enrich_with_rsi(df_raw)  # NEW: add RSI before daily context
    df_enriched = DataEnricher.enrich_with_daily_context(df_raw, cfg["pd_start"], cfg["pd_end"])
    
    # ... rest unchanged
```

- [ ] **Step 2: Update `_evaluate_combo` to pass new features and run post-fade tracking**

Replace the entire `_evaluate_combo` method:

```python
def _evaluate_combo(self, df_enriched: pl.DataFrame, t_start: str, d_min: int) -> dict:
    df_or = DataEnricher.enrich_with_opening_range(df_enriched, t_start, d_min)
    stats_df = TrackerEngine.track_events(df_or, tp_multiplier=1.5)
    
    # Collect new feature columns from OR-enriched data
    agg_cols = [
        pl.col("or_open").first(),
        pl.col("pd_or_high").first(),
        pl.col("pd_or_low").first(),
    ]
    # Conditionally add new columns if they exist
    for col_name in ["rsi_at_or_close", "rsi_daily_14", "atr_change", 
                      "atr_percentile", "or_position_vs_pd",
                      "or_open_vs_pd_close", "or_open_vs_pd_mid",
                      "or_high_vs_pd_high", "or_low_vs_pd_low"]:
        if col_name in df_or.columns:
            agg_cols.append(pl.col(col_name).first())
    
    daily_base = df_or.group_by("trade_date").agg(agg_cols)
    expanded_stats = daily_base.join(stats_df, on="trade_date", how="left")
    
    # Post-fade tracking
    expanded_stats = TrackerEngine.track_post_fade_events(df_or, expanded_stats)
    
    return StatisticalEngine.calculate_edges(expanded_stats)
```

- [ ] **Step 3: Commit**

```bash
git add src/engine/report_generator.py
git commit -m "feat: wire RSI enrichment and post-fade tracking into report pipeline"
```

---

### Task 6: Add New Report Sections to ReportGenerator

**Files:**
- Modify: `src/engine/report_generator.py`

- [ ] **Step 1: Add post-fade anatomy section to `_write_markdown`**

In `_write_markdown`, after the existing "Mapeo Hacia Niveles" section (after line 107), add:

```python
# Post-Fade Anatomy
pf_up = m.get("post_fade", {}).get("UP", {})
pf_down = m.get("post_fade", {}).get("DOWN", {})

if pf_up or pf_down:
    md += "### 🔄 Anatomia Post-False Breakout\n"
    
    if pf_up:
        md += f"**False Breakouts UP analizados:** `{pf_up.get('n_false_breakups', 0)}`\n\n"
        md += "| Metrica | Valor |\n| --- | --- |\n"
        md += f"| Shakeout & Re-breakout UP (>=1x OR) | `{pf_up.get('p_shakeout_rebreak_1x', 0):.2%}` |\n"
        md += f"| Shakeout & Re-breakout UP (>=1.5x OR) | `{pf_up.get('p_shakeout_rebreak_1_5x', 0):.2%}` |\n"
        md += f"| Shakeout & Re-breakout UP (>=2x OR) | `{pf_up.get('p_shakeout_rebreak_2x', 0):.2%}` |\n"
        md += f"| Continuacion Bajista (>=1x OR) | `{pf_up.get('p_continuation_down_1x', 0):.2%}` |\n"
        md += f"| Extension media reversal UP | `{pf_up.get('mean_reversal_up', 0):.2f}x OR` | Mediana: `{pf_up.get('median_reversal_up', 0):.2f}x` |\n"
        md += f"| Extension media continuacion DOWN | `{pf_up.get('mean_cont_down', 0):.2f}x OR` | Mediana: `{pf_up.get('median_cont_down', 0):.2f}x` |\n"
        t_rb = pf_up.get('mean_time_to_rebreak')
        t_rb_med = pf_up.get('median_time_to_rebreak')
        if t_rb is not None:
            md += f"| Tiempo medio al re-breakout | `{t_rb:.0f} min` | Mediana: `{t_rb_med:.0f} min` |\n"
        md += "\n"
    
    if pf_down:
        md += f"**False Breakouts DOWN analizados:** `{pf_down.get('n_false_breakdowns', 0)}`\n\n"
        md += "| Metrica | Valor |\n| --- | --- |\n"
        md += f"| Shakeout & Re-breakout DOWN (>=1x OR) | `{pf_down.get('p_shakeout_rebreak_1x', 0):.2%}` |\n"
        md += f"| Shakeout & Re-breakout DOWN (>=1.5x OR) | `{pf_down.get('p_shakeout_rebreak_1_5x', 0):.2%}` |\n"
        md += f"| Shakeout & Re-breakout DOWN (>=2x OR) | `{pf_down.get('p_shakeout_rebreak_2x', 0):.2%}` |\n"
        md += f"| Continuacion Alcista (>=1x OR) | `{pf_down.get('p_continuation_up_1x', 0):.2%}` |\n"
        md += f"| Extension media reversal DOWN | `{pf_down.get('mean_reversal_down', 0):.2f}x OR` | Mediana: `{pf_down.get('median_reversal_down', 0):.2f}x` |\n"
        md += f"| Extension media continuacion UP | `{pf_down.get('mean_cont_up', 0):.2f}x OR` | Mediana: `{pf_down.get('median_cont_up', 0):.2f}x` |\n"
        t_rb = pf_down.get('mean_time_to_rebreak')
        t_rb_med = pf_down.get('median_time_to_rebreak')
        if t_rb is not None:
            md += f"| Tiempo medio al re-breakout | `{t_rb:.0f} min` | Mediana: `{t_rb_med:.0f} min` |\n"
        md += "\n"
```

- [ ] **Step 2: Add feature-conditional edges table**

After the post-fade section, add:

```python
# Feature-Conditional Edges
feat_segs = m.get("feature_segments", {})
if feat_segs:
    md += "### 🔬 Edge por Contexto de Features\n"
    md += "| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |\n"
    md += "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
    
    for key, seg in feat_segs.items():
        label = seg.get("label", key)
        n = seg.get("n_days", 0)
        def _star(v): return f"`{v:.0%}` ⭐" if v >= 0.60 else f"`{v:.0%}`"
        
        p_up = _star(seg.get("p_break_up", 0))
        ext_up = _star(seg.get("up_ext_1.5", 0))
        f_up = _star(seg.get("f_breakup", 0))
        f_dw = _star(seg.get("f_breakdw", 0))
        shk_up = _star(seg.get("pf_shakeout_up", 0)) if "pf_shakeout_up" in seg else "N/A"
        magnet = _star(seg.get("touch_pd_close", 0))
        
        md += f"| {label} | {n} | {p_up} | {ext_up} | {f_up} | {f_dw} | {shk_up} | {magnet} |\n"
    md += "\n"
```

- [ ] **Step 3: Add timing section**

After the feature table, add:

```python
# Timing
timing = m.get("timing", {})
if timing:
    md += "### ⏱️ Velocidad de Ejecucion\n"
    md += "| Metrica | Media | Mediana | P80 |\n"
    md += "| --- | --- | --- | --- |\n"
    
    if "up_mean_mins_to_tp" in timing:
        md += f"| TP UP (desde entrada) | `{timing['up_mean_mins_to_tp']:.0f} min` | `{timing['up_median_mins_to_tp']:.0f} min` | `{timing['up_p80_mins_to_tp']:.0f} min` |\n"
    if "down_mean_mins_to_tp" in timing:
        md += f"| TP DOWN (desde entrada) | `{timing['down_mean_mins_to_tp']:.0f} min` | `{timing['down_median_mins_to_tp']:.0f} min` | `{timing['down_p80_mins_to_tp']:.0f} min` |\n"
    if "up_mean_mins_to_sl" in timing:
        md += f"| False Break UP → SL | `{timing['up_mean_mins_to_sl']:.0f} min` | - | - |\n"
    if "down_mean_mins_to_sl" in timing:
        md += f"| False Break DOWN → SL | `{timing['down_mean_mins_to_sl']:.0f} min` | - | - |\n"
    md += "\n"
```

- [ ] **Step 4: Commit**

```bash
git add src/engine/report_generator.py
git commit -m "feat: add post-fade, feature-conditional, and timing sections to reports"
```

---

### Task 7: Extend QuantTeam with New Edge Archetypes

**Files:**
- Modify: `src/application/quant_team.py`

- [ ] **Step 1: Add new archetypes to `debate_asset_portfolio`**

In the `for c in combinations` loop, after the existing MAGNET archetypes (after line 35), add:

```python
            # --- Arquetipo 4: Shakeout-Reversal (Post-False Breakout Re-entry) ---
            pf_up = metrics.get('post_fade', {}).get('UP', {})
            pf_down = metrics.get('post_fade', {}).get('DOWN', {})
            
            if pf_up and pf_up.get('p_shakeout_rebreak_1x', 0) >= 0.60:
                t_info = f" | Tiempo medio al re-breakout: {pf_up.get('mean_time_to_rebreak', 0):.0f} min" if pf_up.get('mean_time_to_rebreak') else ""
                edges_found.append(f"- **[EDGE SHAKEOUT-REVERSAL UP] {sess}**: Despues de un falso rompimiento alcista, el `{pf_up['p_shakeout_rebreak_1x']:.2%}` de las veces el precio retoma la direccion UP con extension >=1x OR. Media reversal: `{pf_up.get('mean_reversal_up', 0):.2f}x OR`{t_info}. Sugerencia Algo: Orden limite de COMPRA en OR_Low tras primer rompimiento UP. El mercado barre stops y luego arranca.")
            
            if pf_down and pf_down.get('p_shakeout_rebreak_1x', 0) >= 0.60:
                t_info = f" | Tiempo medio al re-breakout: {pf_down.get('mean_time_to_rebreak', 0):.0f} min" if pf_down.get('mean_time_to_rebreak') else ""
                edges_found.append(f"- **[EDGE SHAKEOUT-REVERSAL DOWN] {sess}**: Despues de un falso rompimiento bajista, el `{pf_down['p_shakeout_rebreak_1x']:.2%}` retoma direccion DOWN con extension >=1x OR. Media reversal: `{pf_down.get('mean_reversal_down', 0):.2f}x OR`{t_info}. Sugerencia Algo: Orden limite de VENTA en OR_High tras primer rompimiento DOWN.")
            
            # --- Arquetipo 5: Feature-Conditional Boosts ---
            feat_segs = metrics.get('feature_segments', {})
            # Get baseline false break rates for comparison
            base_f_up = metrics['false_breaks']['p_false_breakup']
            base_f_dw = metrics['false_breaks']['p_false_breakdown']
            base_ext_up = metrics['extensions']['UP']['up_gt_1.5_or']
            base_ext_dw = metrics['extensions']['DOWN']['down_gt_1.5_or']
            
            for seg_key, seg in feat_segs.items():
                label = seg.get('label', seg_key)
                n = seg.get('n_days', 0)
                if n < 20:
                    continue
                
                # Check if any metric beats baseline by >= 10pp AND exceeds 60%
                ext_up_seg = seg.get('up_ext_1.5', 0)
                if ext_up_seg >= 0.60 and (ext_up_seg - base_ext_up) >= 0.10:
                    edges_found.append(f"- **[EDGE CONTEXT-BOOST UP] {sess} | {label}**: Extension 1.5x UP sube a `{ext_up_seg:.2%}` (base: `{base_ext_up:.2%}`, +{(ext_up_seg - base_ext_up):.0%}pp). N={n}. Sugerencia: Filtrar entradas UP cuando se cumple esta condicion.")
                
                ext_dw_seg = seg.get('dw_ext_1.5', 0) if 'dw_ext_1.5' in seg else 0
                if ext_dw_seg >= 0.60 and (ext_dw_seg - base_ext_dw) >= 0.10:
                    edges_found.append(f"- **[EDGE CONTEXT-BOOST DOWN] {sess} | {label}**: Extension 1.5x DOWN sube a `{ext_dw_seg:.2%}` (base: `{base_ext_dw:.2%}`, +{(ext_dw_seg - base_ext_dw):.0%}pp). N={n}.")
                
                # RSI-conditional edges
                if 'rsi' in seg_key.lower():
                    shk = seg.get('pf_shakeout_up', 0)
                    if shk >= 0.60:
                        edges_found.append(f"- **[EDGE RSI-CONDITIONAL] {sess} | {label}**: Shakeout UP post-fade al `{shk:.2%}`. Cuando el RSI esta en esta zona, los false breakouts tienden a revertir con fuerza. N={n}.")
```

- [ ] **Step 2: Commit**

```bash
git add src/application/quant_team.py
git commit -m "feat: add SHAKEOUT-REVERSAL, CONTEXT-BOOST, RSI-CONDITIONAL archetypes to QuantTeam"
```

---

### Task 8: End-to-End Verification — Generate Reports

**Files:**
- None (verification only)

- [ ] **Step 1: Run the full report generator**

```bash
cd C:/Proyectos/kha0sys3 && python -c "
from src.engine.report_generator import ReportGenerator
rg = ReportGenerator(
    data_dir='c:/Proyectos/kha0sys3/data',
    config_path='c:/Proyectos/kha0sys3/src/infrastructure/config/asset_config.json',
    reports_dir='c:/Proyectos/kha0sys3/reports'
)
rg.generate_all()
print('Done!')
"
```
Expected: Reports generated for all 15 assets without errors.

- [ ] **Step 2: Spot-check a report**

Open `reports/EURUSD_Edge.md` and verify:
1. New "Anatomia Post-False Breakout" section exists with shakeout probabilities
2. "Edge por Contexto de Features" table has RSI, OR position, ATR segments
3. "Velocidad de Ejecucion" timing table present
4. QuantTeam debate includes new archetypes (SHAKEOUT-REVERSAL, CONTEXT-BOOST) where applicable

- [ ] **Step 3: Spot-check a second asset**

Open `reports/XAUUSD_Edge.md` — same verification.

- [ ] **Step 4: Final commit of generated reports**

```bash
git add reports/
git commit -m "feat: regenerate all edge reports with post-fade analysis and feature relationships"
```
