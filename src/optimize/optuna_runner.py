import optuna
import polars as pl
from pathlib import Path
import json

from src.infrastructure.data.polars_loader import CSVPolarsLoader
from src.application.calculators import DataEnricher
from src.application.trackers import TrackerEngine

class OptunaOptimizer:
    def __init__(self, symbol: str, data_dir: str, config_path: str):
        self.symbol = symbol
        self.loader = CSVPolarsLoader(data_dir)
        self.df_raw = self.loader.load_data(symbol, "M15")
        with open(config_path, "r") as f:
            self.config = json.load(f)[symbol]

        # Pre-enrich dataset to save time
        self.df_enriched = DataEnricher.enrich_with_daily_context(
            self.df_raw, self.config["pd_start"], self.config["pd_end"]
        )
        self.df_or = DataEnricher.enrich_with_opening_range(
             self.df_enriched, self.config["time_start"], self.config["duration_minutes"]
        )
        
        self.daily_base = self.df_or.group_by("trade_date").agg([
            pl.col("or_width").first(),
            pl.col("or_high").first(),
            pl.col("or_low").first(),
            pl.col("atr_14").first()
        ])

    def objective(self, trial):
        or_width_min_ratio = trial.suggest_float("or_width_min_ratio", 0.05, 0.3)
        or_width_max_ratio = trial.suggest_float("or_width_max_ratio", 0.4, 1.2)
        target_mult = trial.suggest_float("target_multiplier", 1.0, 3.0)
        
        # Track events strictly chronologically
        stats = TrackerEngine.track_events(self.df_or, tp_multiplier=target_mult)
        results = self.daily_base.join(stats, on="trade_date", how="left")
        
        results = results.with_columns([
            (pl.col("or_width") / pl.col("atr_14")).alias("or_atr_ratio")
        ])
        
        valid_trade_days = pl.col("or_atr_ratio").is_between(or_width_min_ratio, or_width_max_ratio) & pl.col("first_break_dir").is_not_null()
        
        results = results.with_columns([
            pl.when(valid_trade_days & (pl.col("first_break_dir") == "UP"))
            .then(
                pl.when(pl.col("time_sl_up").is_null() & pl.col("time_tp_up").is_not_null())
                .then(target_mult)
                .when(pl.col("time_sl_up").is_not_null() & pl.col("time_tp_up").is_not_null())
                .then(
                    pl.when(pl.col("time_tp_up") < pl.col("time_sl_up"))
                    .then(target_mult)
                    .otherwise(-1.0)
                )
                .when(pl.col("time_sl_up").is_not_null())
                .then(-1.0)
                .otherwise(0.0)
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
        
        pnl = results.select(pl.col("r_multiple").sum()).item()
        return pnl if pnl is not None else 0

    def optimize(self, n_trials=50):
        study = optuna.create_study(direction="maximize")
        study.optimize(self.objective, n_trials=n_trials)
        print(f"Best trial for {self.symbol}: {study.best_value}")
        print(f"Best params: {study.best_params}")
        return study.best_params

if __name__ == "__main__":
    opt = OptunaOptimizer(
        "EURUSD",
        "c:/Proyectos/kha0sys3/data",
        "c:/Proyectos/kha0sys3/src/infrastructure/config/asset_config.json"
    )
    opt.optimize(n_trials=20)
