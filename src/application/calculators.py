import polars as pl
from datetime import datetime, time

class DataEnricher:
    """
    Application layer service to enrich raw M15 data with Daily Context (ATR, Prev Day)
    and Opening Range context using Polars vectorized operations.
    """
    
    @staticmethod
    def enrich_with_daily_context(m15_df: pl.DataFrame, pd_start_str: str, pd_end_str: str) -> pl.DataFrame:
        """
        Calculates Daily stats (High, Low, Close) based on the session's daily definition 
        (pd_start to pd_end) and ATR(14), then joins back to M15.
        """
        # Create a trading date column. For strict midnight-midnight it's just the date.
        # If pd_start is non-standard, we might need a custom grouping.
        # Simplicity for now: standard date.
        
        df = m15_df.with_columns([
            pl.col("time").dt.date().alias("trade_date")
        ])
        
        # Calculate daily aggregates
        daily_df = df.group_by("trade_date").agg([
            pl.col("high").max().alias("d_high"),
            pl.col("low").min().alias("d_low"),
            pl.col("close").last().alias("d_close"),
            pl.col("open").first().alias("d_open")
        ]).sort("trade_date")
        
        # Shift back 1 day to get 'Previous Day' metrics
        daily_df = daily_df.with_columns([
            pl.col("d_high").shift(1).alias("pd_high"),
            pl.col("d_low").shift(1).alias("pd_low"),
            pl.col("d_close").shift(1).alias("pd_close"),
            pl.col("d_open").shift(1).alias("pd_open")
        ])
        
        # Calculate pd_mid
        daily_df = daily_df.with_columns([
            ((pl.col("pd_high") + pl.col("pd_low")) / 2.0).alias("pd_mid")
        ])
        
        # Calculate True Range for the day
        daily_df = daily_df.with_columns([
            pl.max_horizontal(
                pl.col("d_high") - pl.col("d_low"),
                (pl.col("d_high") - pl.col("pd_close")).abs(),
                (pl.col("d_low") - pl.col("pd_close")).abs()
            ).alias("tr")
        ])
        
        # Calculate ATR(14)
        daily_df = daily_df.with_columns([
            pl.col("tr").rolling_mean(window_size=14).shift(1).alias("atr_14")
        ])

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

        # ATR percentile (global rank, simpler approach for Polars compatibility)
        daily_df = daily_df.with_columns([
            (pl.col("atr_14").rank() / pl.col("atr_14").count() * 100).alias("atr_percentile")
        ])

        # Join back mapped by trade_date
        enriched_m15 = df.join(
            daily_df.select(["trade_date", "pd_high", "pd_low", "pd_close", "pd_open", "pd_mid",
                              "atr_14", "rsi_daily_14", "atr_change", "atr_percentile"]),
            on="trade_date",
            how="left"
        )
        return enriched_m15

    @staticmethod
    def enrich_with_opening_range(df: pl.DataFrame, or_start: str, duration_mins: int) -> pl.DataFrame:
        """
        Calculates the Opening Range (High, Low) for each day based on the or_start time 
        and duration, and broadcasts it to the entire day.
        """
        # Parse time str
        hh, mm = map(int, or_start.split(":"))
        start_td = hh * 60 + mm
        end_td = start_td + duration_mins
        expiration_td = start_td + (8 * 60) # 8 hours exactly from magic_time
        
        # Map time of day to total minutes. Need to cast hour to Int32 to avoid Int8 overflow when multiplying by 60.
        df = df.with_columns([
            (pl.col("time").dt.hour().cast(pl.Int32) * 60 + pl.col("time").dt.minute()).alias("mins_from_midnight")
        ])
        
        # Filter for OR candles
        or_candles = df.filter(
            (pl.col("mins_from_midnight") >= start_td) & 
            (pl.col("mins_from_midnight") < end_td)
        )
        
        # Calculate OR High and Low per day
        # Build aggregation list - RSI column may not be present
        agg_exprs = [
            pl.col("high").max().alias("or_high"),
            pl.col("low").min().alias("or_low"),
            pl.col("open").first().alias("or_open"),
        ]
        if "rsi_14" in df.columns:
            agg_exprs.append(pl.col("rsi_14").last().alias("rsi_at_or_close"))

        or_stats = or_candles.group_by("trade_date").agg(agg_exprs).sort("trade_date")
        
        # Previous Day OR memory
        or_stats = or_stats.with_columns([
            pl.col("or_high").shift(1).alias("pd_or_high"),
            pl.col("or_low").shift(1).alias("pd_or_low")
        ])
        
        # Join back
        res_df = df.join(or_stats, on="trade_date", how="left")
        
        # Calculate OR Width and ATR Ratio
        res_df = res_df.with_columns([
            (pl.col("or_high") - pl.col("or_low")).alias("or_width"),
            ((pl.col("or_high") + pl.col("or_low")) / 2).alias("or_mid")
        ])
        
        res_df = res_df.with_columns([
            pl.when(pl.col("atr_14").is_not_null() & (pl.col("atr_14") > 0))
            .then(pl.col("or_width") / pl.col("atr_14"))
            .otherwise(pl.lit(None))
            .alias("or_atr_ratio")
        ])

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

        # Flag post OR candles & 8H Active Session Window
        res_df = res_df.with_columns([
            (pl.col("mins_from_midnight") >= end_td).alias("is_post_or"),
            ((pl.col("mins_from_midnight") >= end_td) & (pl.col("mins_from_midnight") <= expiration_td)).alias("is_active_session")
        ])
        
        return res_df

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
