from src.application.calculators import DataEnricher
from src.infrastructure.data.polars_loader import CSVPolarsLoader
import polars as pl

ld = CSVPolarsLoader('c:/Proyectos/kha0sys3/data')
df = ld.load_data('EURUSD', 'M15')
df_enriched = DataEnricher.enrich_with_daily_context(df, "00:00", "23:59")

start_td = 7 * 60
end_td = start_td + 30
df_mins = df_enriched.with_columns([
    (pl.col("time").dt.hour() * 60 + pl.col("time").dt.minute()).alias("mins_from_midnight")
])
or_candles = df_mins.filter(
    (pl.col("mins_from_midnight") >= start_td) & 
    (pl.col("mins_from_midnight") < end_td)
)
print("OR Candles:", or_candles.height)
or_stats = or_candles.group_by("trade_date").agg([
    pl.col("high").max().alias("or_high"),
    pl.col("low").min().alias("or_low"),
    pl.col("open").first().alias("or_open")
])
print("OR Stats Rows:", or_stats.height)

res_df = df_mins.join(or_stats, on="trade_date", how="left")
res_df = res_df.with_columns([
    (pl.col("or_high") - pl.col("or_low")).alias("or_width"),
    ((pl.col("or_high") + pl.col("or_low")) / 2).alias("or_mid")
])
print("Final Non-Null Width Rows:", res_df.filter(pl.col("or_width").is_not_null()).height)

