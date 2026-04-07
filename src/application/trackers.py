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
