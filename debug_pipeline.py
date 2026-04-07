from src.engine.backtester import BacktestPipeline
from src.application.calculators import DataEnricher
import polars as pl

pb = BacktestPipeline('c:/Proyectos/kha0sys3/data', 'c:/Proyectos/kha0sys3/src/infrastructure/config/asset_config.json')
df = pb.loader.load_data('EURUSD', 'M15')
print("Loaded:", len(df))

sym_config = pb.config["EURUSD"]
df_enriched = DataEnricher.enrich_with_daily_context(df, sym_config["pd_start"], sym_config["pd_end"])
df_or = DataEnricher.enrich_with_opening_range(df_enriched, sym_config["time_start"], sym_config["duration_minutes"])

or_count = df_or.filter(pl.col("or_width").is_not_null()).height
print("Non-null OR widths:", or_count)

res = pb.run_asset('EURUSD')
