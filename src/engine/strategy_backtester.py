import polars as pl
import numpy as np
from typing import Dict, List, Optional
from src.domain.strategy_models import StrategyDef, StrategyResult
from src.engine.strategy_scanner import StrategyScanner


class StrategyBacktester:

    @classmethod
    def backtest(cls, strategy: StrategyDef, stats_df: pl.DataFrame,
                 context_filter: Optional[Dict] = None) -> StrategyResult:
        valid_df = stats_df.filter(
            pl.col("first_break_dir").is_not_null() &
            pl.col("or_atr_ratio").is_between(0.1, 0.8)
        ).sort("trade_date")

        if context_filter:
            valid_df = StrategyScanner.apply_context_filter(valid_df, context_filter)

        base_arch = strategy.archetype.replace("_UP", "").replace("_DOWN", "")
        direction = strategy.direction

        trade_log = cls._compute_trades(valid_df, base_arch, direction, strategy.tp_multiplier)

        if trade_log.height == 0:
            return StrategyResult(strategy=strategy)

        return cls._compute_metrics(strategy, trade_log)

    @classmethod
    def _compute_trades(cls, df: pl.DataFrame, archetype: str,
                        direction: str, tp_mult: float) -> pl.DataFrame:
        if archetype == "MOMENTUM":
            return cls._trades_momentum(df, direction, tp_mult)
        elif archetype == "FADE":
            return cls._trades_fade(df, direction)
        elif archetype == "SHAKEOUT":
            return cls._trades_shakeout(df, direction)
        return pl.DataFrame()

    @staticmethod
    def _trades_momentum(df: pl.DataFrame, direction: str, tp_mult: float) -> pl.DataFrame:
        if direction == "UP":
            trades = df.filter(pl.col("first_break_dir") == "UP")
            trades = trades.with_columns(
                pl.when(
                    pl.col("time_tp_up").is_not_null() &
                    (pl.col("time_sl_up").is_null() | (pl.col("time_tp_up") < pl.col("time_sl_up")))
                ).then(tp_mult)
                .when(
                    pl.col("time_sl_up").is_not_null() &
                    (pl.col("time_tp_up").is_null() | (pl.col("time_sl_up") <= pl.col("time_tp_up")))
                ).then(-1.0)
                .otherwise(0.0)
                .alias("r_multiple")
            )
        else:
            trades = df.filter(pl.col("first_break_dir") == "DOWN")
            trades = trades.with_columns(
                pl.when(
                    pl.col("time_tp_down").is_not_null() &
                    (pl.col("time_sl_down").is_null() | (pl.col("time_tp_down") < pl.col("time_sl_down")))
                ).then(tp_mult)
                .when(
                    pl.col("time_sl_down").is_not_null() &
                    (pl.col("time_tp_down").is_null() | (pl.col("time_sl_down") <= pl.col("time_tp_down")))
                ).then(-1.0)
                .otherwise(0.0)
                .alias("r_multiple")
            )
        return trades.filter(pl.col("r_multiple") != 0.0).select(["trade_date", "r_multiple"])

    @staticmethod
    def _trades_fade(df: pl.DataFrame, direction: str) -> pl.DataFrame:
        if direction == "UP":
            trades = df.filter(pl.col("first_break_dir") == "UP")
            trades = trades.with_columns(
                pl.when(
                    pl.col("time_sl_up").is_not_null() &
                    (pl.col("time_tp_up").is_null() | (pl.col("time_sl_up") < pl.col("time_tp_up")))
                ).then(1.0)
                .when(
                    pl.col("time_tp_up").is_not_null() &
                    (pl.col("time_sl_up").is_null() | (pl.col("time_tp_up") <= pl.col("time_sl_up")))
                ).then(-1.0)
                .otherwise(0.0)
                .alias("r_multiple")
            )
        else:
            trades = df.filter(pl.col("first_break_dir") == "DOWN")
            trades = trades.with_columns(
                pl.when(
                    pl.col("time_sl_down").is_not_null() &
                    (pl.col("time_tp_down").is_null() | (pl.col("time_sl_down") < pl.col("time_tp_down")))
                ).then(1.0)
                .when(
                    pl.col("time_tp_down").is_not_null() &
                    (pl.col("time_sl_down").is_null() | (pl.col("time_tp_down") <= pl.col("time_sl_down")))
                ).then(-1.0)
                .otherwise(0.0)
                .alias("r_multiple")
            )
        return trades.filter(pl.col("r_multiple") != 0.0).select(["trade_date", "r_multiple"])

    @staticmethod
    def _trades_shakeout(df: pl.DataFrame, direction: str) -> pl.DataFrame:
        if direction == "UP":
            if "pf_up_rebreak_1x" not in df.columns:
                return pl.DataFrame()
            trades = df.filter(
                (pl.col("first_break_dir") == "UP") &
                pl.col("time_sl_up").is_not_null() &
                (pl.col("time_tp_up").is_null() | (pl.col("time_sl_up") < pl.col("time_tp_up"))) &
                pl.col("pf_up_max_reversal_up").is_not_null()
            )
            trades = trades.with_columns(
                pl.when(pl.col("pf_up_rebreak_1x") == True)
                .then(1.0)
                .otherwise(-1.0)
                .alias("r_multiple")
            )
        else:
            if "pf_down_rebreak_1x" not in df.columns:
                return pl.DataFrame()
            trades = df.filter(
                (pl.col("first_break_dir") == "DOWN") &
                pl.col("time_sl_down").is_not_null() &
                (pl.col("time_tp_down").is_null() | (pl.col("time_sl_down") < pl.col("time_tp_down"))) &
                pl.col("pf_down_max_reversal_down").is_not_null()
            )
            trades = trades.with_columns(
                pl.when(pl.col("pf_down_rebreak_1x") == True)
                .then(1.0)
                .otherwise(-1.0)
                .alias("r_multiple")
            )
        return trades.filter(pl.col("r_multiple") != 0.0).select(["trade_date", "r_multiple"])

    @classmethod
    def _compute_metrics(cls, strategy: StrategyDef, trade_log: pl.DataFrame) -> StrategyResult:
        trades = trade_log.sort("trade_date")
        r_vals = trades["r_multiple"].to_list()
        dates = trades["trade_date"].to_list()

        total = len(r_vals)
        wins = sum(1 for r in r_vals if r > 0)
        losses = sum(1 for r in r_vals if r < 0)
        wr = wins / total if total > 0 else 0

        gross_profit = sum(r for r in r_vals if r > 0)
        gross_loss = abs(sum(r for r in r_vals if r < 0))
        pf = gross_profit / gross_loss if gross_loss > 0 else float("inf")

        net_r = sum(r_vals)
        avg_r = net_r / total if total > 0 else 0

        cumulative = np.cumsum(r_vals)
        peak = np.maximum.accumulate(cumulative)
        dd = cumulative - peak
        max_dd = float(np.min(dd)) if len(dd) > 0 else 0

        if len(r_vals) > 1:
            mean_r = np.mean(r_vals)
            std_r = np.std(r_vals, ddof=1)
            sharpe = (mean_r / std_r) * np.sqrt(252) if std_r > 0 else 0
        else:
            sharpe = 0

        if dates:
            first_date = min(dates)
            last_date = max(dates)
            if hasattr(first_date, 'days'):
                days_span = (last_date - first_date).days
            else:
                from datetime import date as dt_date
                if isinstance(first_date, dt_date):
                    days_span = (last_date - first_date).days
                else:
                    days_span = 1
            years = max(days_span / 365.25, 0.1)
            tpy = total / years
        else:
            tpy = 0

        # Yearly breakdown
        trades_with_year = trades.with_columns(
            pl.col("trade_date").cast(pl.Date).dt.year().alias("year")
        )
        yearly_stats = {}
        for year_row in trades_with_year.group_by("year").agg([
            pl.col("r_multiple").count().alias("n"),
            (pl.col("r_multiple") > 0).sum().alias("w"),
            pl.col("r_multiple").sum().alias("net"),
        ]).sort("year").iter_rows(named=True):
            yr = year_row["year"]
            n = year_row["n"]
            w = year_row["w"]
            yearly_stats[str(yr)] = {
                "trades": n,
                "wins": w,
                "wr": w / n if n > 0 else 0,
                "net_r": year_row["net"],
            }

        best_yr = max(yearly_stats, key=lambda y: yearly_stats[y]["net_r"]) if yearly_stats else ""
        worst_yr = min(yearly_stats, key=lambda y: yearly_stats[y]["net_r"]) if yearly_stats else ""

        passes = wr >= 0.65 and tpy >= 100 and pf > 1.0

        return StrategyResult(
            strategy=strategy,
            total_trades=total,
            trades_per_year=tpy,
            win_rate=wr,
            profit_factor=pf,
            net_r=net_r,
            max_drawdown=max_dd,
            sharpe=sharpe,
            avg_r_per_trade=avg_r,
            best_year=best_yr,
            worst_year=worst_yr,
            yearly_stats=yearly_stats,
            passes_filter=passes,
        )

    @classmethod
    def backtest_group(cls, strategies: List[StrategyDef],
                       stats_dfs: Dict[str, pl.DataFrame],
                       context_filters: List[Optional[Dict]]) -> StrategyResult:
        all_trades = []
        for strat, ctx in zip(strategies, context_filters):
            key = f"{strat.session_name}_{strat.duration}"
            stats_df = stats_dfs.get(key)
            if stats_df is None:
                continue
            valid_df = stats_df.filter(
                pl.col("first_break_dir").is_not_null() &
                pl.col("or_atr_ratio").is_between(0.1, 0.8)
            ).sort("trade_date")
            if ctx:
                valid_df = StrategyScanner.apply_context_filter(valid_df, ctx)
            base_arch = strat.archetype.replace("_UP", "").replace("_DOWN", "")
            log = cls._compute_trades(valid_df, base_arch, strat.direction, strat.tp_multiplier)
            if log.height > 0:
                all_trades.append(log)

        if not all_trades:
            group_strat = StrategyDef(
                symbol=strategies[0].symbol if strategies else "UNKNOWN",
                session_name="GROUP", time_start="", duration=0,
                archetype="GROUP", direction="ALL"
            )
            return StrategyResult(strategy=group_strat)

        combined = pl.concat(all_trades).sort("trade_date")
        group_strat = StrategyDef(
            symbol=strategies[0].symbol,
            session_name="GROUP", time_start="", duration=0,
            archetype="GROUP", direction="ALL",
            label=f"{strategies[0].symbol} GRUPO ({len(strategies)} estrategias)"
        )
        return cls._compute_metrics(group_strat, combined)
