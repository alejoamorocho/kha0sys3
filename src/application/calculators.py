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
        
        # Join back mapped by trade_date
        enriched_m15 = df.join(
            daily_df.select(["trade_date", "pd_high", "pd_low", "pd_close", "pd_open", "pd_mid", "atr_14"]),
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
        or_stats = or_candles.group_by("trade_date").agg([
            pl.col("high").max().alias("or_high"),
            pl.col("low").min().alias("or_low"),
            pl.col("open").first().alias("or_open")
        ]).sort("trade_date")
        
        # Previous Day OR memory
        or_stats = or_stats.with_columns([
            pl.col("or_high").shift(1).alias("pd_or_high"),
            pl.col("or_low").shift(1).alias("pd_or_low")
        ])
        
        # Join back
        res_df = df.join(or_stats, on="trade_date", how="left")
        
        # Calculate OR Width
        res_df = res_df.with_columns([
            (pl.col("or_high") - pl.col("or_low")).alias("or_width"),
            ((pl.col("or_high") + pl.col("or_low")) / 2).alias("or_mid")
        ])
        
        # Flag post OR candles
        res_df = res_df.with_columns([
            (pl.col("mins_from_midnight") >= end_td).alias("is_post_or")
        ])
        
        return res_df
