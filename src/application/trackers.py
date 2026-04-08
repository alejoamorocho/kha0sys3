"""Tracking vectorizado de eventos post-OR: breakouts, TP/SL hits, false breakouts."""

import polars as pl

class TrackerEngine:
    """
    Vectorized tracking of post-OR events across a dataset, avoiding look-ahead bias
    by finding the exact time (mins_from_midnight) that thresholds are crossed.
    """
    
    @staticmethod
    def track_events(enriched_df: pl.DataFrame, tp_multiplier: float = 1.5) -> pl.DataFrame:
        """
        Takes the enriched DataFrame and computes chronological hits for TP and SL.
        tp_multiplier determines how far the TP is relative to the OR width.
        """
        # We need or_width to define targets. It's already in the dataframe.
        df = enriched_df.filter(pl.col("is_post_or") == True)
        
        df = df.with_columns([
            (pl.col("or_high") + (pl.col("or_width") * tp_multiplier)).alias("target_up"),
            (pl.col("or_low") - (pl.col("or_width") * tp_multiplier)).alias("target_down"),
            pl.col("or_low").alias("sl_up"),  # Stop loss for LONG is OR Low
            pl.col("or_high").alias("sl_down") # Stop loss for SHORT is OR High
        ])
        
        # 1. Base daily stats
        stats_df = df.group_by("trade_date").agg([
            pl.col("or_width").first().alias("or_width"),
            pl.col("or_high").first().alias("or_high"),
            pl.col("or_low").first().alias("or_low"),
            pl.col("pd_close").first().alias("pd_close"),
            pl.col("or_atr_ratio").first().alias("or_atr_ratio"),
            pl.col("atr_14").first().alias("atr_14"),
            (pl.col("high").max() - pl.col("or_high").first()).alias("max_up"),
            (pl.col("or_low").first() - pl.col("low").min()).alias("max_down"),
            (pl.col("close") > pl.col("or_high").first()).sum().alias("breakout_up_count"),
            (pl.col("close") < pl.col("or_low").first()).sum().alias("breakout_down_count"),
            (pl.col("high") >= pl.col("pd_high").first()).sum().alias("touches_pd_high"),
            (pl.col("low") <= pl.col("pd_low").first()).sum().alias("touches_pd_low"),
            ((pl.col("high") >= pl.col("pd_close").first()) & (pl.col("low") <= pl.col("pd_close").first())).sum().alias("touches_pd_close"),
            ((pl.col("high") >= pl.col("pd_mid").first()) & (pl.col("low") <= pl.col("pd_mid").first())).sum().alias("touches_pd_mid"),
            ((pl.col("high") >= pl.col("pd_or_high").first()) & (pl.col("low") <= pl.col("pd_or_high").first())).sum().alias("touches_pd_or_high"),
            ((pl.col("high") >= pl.col("pd_or_low").first()) & (pl.col("low") <= pl.col("pd_or_low").first())).sum().alias("touches_pd_or_low"),
        ])
        
        # 2. Breakouts (Entries) - We trigger strictly when price breaks the level DURING the active 8H window
        first_break_up = df.filter(
            (pl.col("high") >= pl.col("or_high")) & (pl.col("is_active_session") == True)
        ).group_by("trade_date").agg([
            pl.col("mins_from_midnight").min().alias("time_entry_up")
        ])
        
        first_break_down = df.filter(
            (pl.col("low") <= pl.col("or_low")) & (pl.col("is_active_session") == True)
        ).group_by("trade_date").agg([
            pl.col("mins_from_midnight").min().alias("time_entry_down")
        ])
        
        # 3. TP / SL Hits
        tp_hit_up = df.filter(pl.col("high") >= pl.col("target_up")).group_by("trade_date").agg([
            pl.col("mins_from_midnight").min().alias("time_tp_up")
        ])
        
        sl_hit_up = df.filter(pl.col("low") <= pl.col("sl_up")).group_by("trade_date").agg([
            pl.col("mins_from_midnight").min().alias("time_sl_up")
        ])
        
        tp_hit_down = df.filter(pl.col("low") <= pl.col("target_down")).group_by("trade_date").agg([
            pl.col("mins_from_midnight").min().alias("time_tp_down")
        ])
        
        sl_hit_down = df.filter(pl.col("high") >= pl.col("sl_down")).group_by("trade_date").agg([
            pl.col("mins_from_midnight").min().alias("time_sl_down")
        ])
        
        # Join all chronological events back to stats_df
        stats_df = stats_df.join(first_break_up, on="trade_date", how="left")
        stats_df = stats_df.join(first_break_down, on="trade_date", how="left")
        stats_df = stats_df.join(tp_hit_up, on="trade_date", how="left")
        stats_df = stats_df.join(sl_hit_up, on="trade_date", how="left")
        stats_df = stats_df.join(tp_hit_down, on="trade_date", how="left")
        stats_df = stats_df.join(sl_hit_down, on="trade_date", how="left")
        
        # Determine strict first break direction
        stats_df = stats_df.with_columns([
            pl.when(pl.col("time_entry_up").is_not_null() & pl.col("time_entry_down").is_null())
            .then(pl.lit("UP"))
            .when(pl.col("time_entry_down").is_not_null() & pl.col("time_entry_up").is_null())
            .then(pl.lit("DOWN"))
            .when(pl.col("time_entry_up") < pl.col("time_entry_down"))
            .then(pl.lit("UP"))
            .when(pl.col("time_entry_down") < pl.col("time_entry_up"))
            .then(pl.lit("DOWN"))
            .otherwise(pl.lit("NONE"))
            .alias("first_break_dir")
        ])
        
        return stats_df

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
