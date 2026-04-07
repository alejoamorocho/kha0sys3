import polars as pl
from pathlib import Path
import json

from src.infrastructure.data.polars_loader import CSVPolarsLoader
from src.application.calculators import DataEnricher
from src.application.trackers import TrackerEngine

class BacktestPipeline:
    def __init__(self, data_dir: str, config_path: str):
        self.data_dir = data_dir
        self.loader = CSVPolarsLoader(data_dir)
        with open(config_path, "r") as f:
            self.config = json.load(f)

    def run_asset(self, symbol: str, tp_multiplier: float = None) -> pl.DataFrame:
        """Ejecuta backtest para un activo.

        Args:
            symbol: Nombre interno del activo.
            tp_multiplier: Multiplicador de TP sobre OR width.
                Si None, usa el valor de la config del símbolo (tp_opt) o 1.5 por default.
        """
        sym_config = self.config.get(symbol)
        if not sym_config:
            raise ValueError(f"Config for {symbol} not found.")

        df = self.loader.load_data(symbol, "M15")

        df_enriched = DataEnricher.enrich_with_daily_context(
            df, sym_config["pd_start"], sym_config["pd_end"]
        )

        df_or = DataEnricher.enrich_with_opening_range(
             df_enriched, sym_config["time_start"], sym_config["duration_minutes"]
        )

        # TP multiplier: usar el pasado como argumento, o el de config, o 1.5
        target_mult = tp_multiplier or sym_config.get("tp_opt", 1.5)
        stats = TrackerEngine.track_events(df_or, tp_multiplier=target_mult)
        
        daily_base = df_or.group_by("trade_date").agg([
            pl.col("or_width").first(),
            pl.col("or_high").first(),
            pl.col("or_low").first(),
            pl.col("atr_14").first()
        ])
        
        results = daily_base.join(stats, on="trade_date", how="left")
        
        results = results.with_columns([
            (pl.col("or_width") / pl.col("atr_14")).alias("or_atr_ratio")
        ])
        
        valid_trade_days = pl.col("or_atr_ratio").is_between(0.1, 0.8) & pl.col("first_break_dir").is_not_null()
        
        # STRICT Execution logic ensuring TP happens BEFORE SL, and SL happens AFTER Entry
        # Intra-bar priority: if time_tp == time_sl, we assume LOSS (pessimistic, preventing bias)
        results = results.with_columns([
            pl.when(valid_trade_days & (pl.col("first_break_dir") == "UP"))
            .then(
                pl.when(pl.col("time_sl_up").is_null() & pl.col("time_tp_up").is_not_null())
                .then(target_mult)  # Hit TP, didn't hit SL at all
                .when(pl.col("time_sl_up").is_not_null() & pl.col("time_tp_up").is_not_null())
                .then(
                    pl.when(pl.col("time_tp_up") < pl.col("time_sl_up"))
                    .then(target_mult) # TP hit strictly before SL
                    .otherwise(-1.0) # SL hit before or at the exact same minute as TP
                )
                .when(pl.col("time_sl_up").is_not_null())
                .then(-1.0) # Hit SL, didn't hit TP
                .otherwise(0.0) # Closed day without hitting TP or SL
            )
            .when(valid_trade_days & (pl.col("first_break_dir") == "DOWN"))
            .then(
                pl.when(pl.col("time_sl_down").is_null() & pl.col("time_tp_down").is_not_null())
                .then(target_mult)
                .when(pl.col("time_sl_down").is_not_null() & pl.col("time_tp_down").is_not_null())
                .then(
                    pl.when(pl.col("time_tp_down") < pl.col("time_sl_down"))
                    .then(target_mult)
                    .otherwise(-1.0)
                )
                .when(pl.col("time_sl_down").is_not_null())
                .then(-1.0)
                .otherwise(0.0)
            )
            .otherwise(0.0)
            .alias("r_multiple")
        ])
        
        win_rate = results.filter(pl.col("r_multiple") > 0).height / max(1, results.filter(pl.col("r_multiple") != 0).height)
        total_pnl = results.select(pl.col("r_multiple").sum()).item()
        total_trades = results.filter(pl.col("r_multiple") != 0).height
        
        print(f"{symbol} -> T: {total_trades:>4} | WR: {win_rate:>6.2%} | Net R: {total_pnl:>7.2f}")
        return results

if __name__ == "__main__":
    pb = BacktestPipeline(
        data_dir=str(Path("c:/Proyectos/kha0sys3/data")),
        config_path=str(Path("c:/Proyectos/kha0sys3/src/infrastructure/config/asset_config.json"))
    )
    res = pb.run_asset("EURUSD")
