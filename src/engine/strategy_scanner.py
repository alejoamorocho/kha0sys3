import polars as pl
from typing import List, Dict, Optional


class StrategyScanner:
    """
    Scans all permutations of (session x duration x archetype x direction x context_filter)
    for a given asset and evaluates win rate from enriched historical data.
    """

    ARCHETYPES = ["MOMENTUM", "FADE", "SHAKEOUT"]
    DIRECTIONS = ["UP", "DOWN"]

    CONTEXT_FILTERS = {
        "rsi_oversold": {"col": "rsi_at_or_close", "op": "<", "val": 30, "label": "RSI<30"},
        "rsi_overbought": {"col": "rsi_at_or_close", "op": ">", "val": 70, "label": "RSI>70"},
        "atr_growing": {"col": "atr_change", "op": ">", "val": 0.1, "label": "ATR+10%"},
        "atr_shrinking": {"col": "atr_change", "op": "<", "val": -0.1, "label": "ATR-10%"},
        "above_pd_high": {"col": "or_position_vs_pd", "op": "==", "val": "ABOVE_PD_HIGH", "label": "AbovePD"},
        "below_pd_low": {"col": "or_position_vs_pd", "op": "==", "val": "BELOW_PD_LOW", "label": "BelowPD"},
        "between_close_high": {"col": "or_position_vs_pd", "op": "==", "val": "BETWEEN_CLOSE_AND_HIGH", "label": "BtwCloseHigh"},
        "between_low_close": {"col": "or_position_vs_pd", "op": "==", "val": "BETWEEN_LOW_AND_CLOSE", "label": "BtwLowClose"},
        "rsi_daily_low": {"col": "rsi_daily_14", "op": "<", "val": 35, "label": "RSI_D<35"},
        "rsi_daily_high": {"col": "rsi_daily_14", "op": ">", "val": 65, "label": "RSI_D>65"},
    }

    MIN_DAYS = 20

    @staticmethod
    def apply_context_filter(df: pl.DataFrame, filt: Optional[Dict]) -> pl.DataFrame:
        if not filt:
            return df
        col = filt["col"]
        op = filt["op"]
        val = filt["val"]
        if col not in df.columns:
            return df.head(0)
        if op == "<":
            return df.filter(pl.col(col) < val)
        elif op == ">":
            return df.filter(pl.col(col) > val)
        elif op == "==":
            return df.filter(pl.col(col) == val)
        return df

    @classmethod
    def evaluate_archetype(cls, stats_df: pl.DataFrame, archetype: str,
                           direction: str, context_filter: Optional[Dict] = None) -> Dict:
        valid_df = stats_df.filter(
            pl.col("first_break_dir").is_not_null() &
            pl.col("or_atr_ratio").is_between(0.1, 0.8)
        )
        if context_filter:
            valid_df = cls.apply_context_filter(valid_df, context_filter)
        if valid_df.height < cls.MIN_DAYS:
            return {"win_rate": 0, "n_trades": 0, "viable": False}

        if archetype == "MOMENTUM":
            return cls._eval_momentum(valid_df, direction)
        elif archetype == "FADE":
            return cls._eval_fade(valid_df, direction)
        elif archetype == "SHAKEOUT":
            return cls._eval_shakeout(valid_df, direction)
        return {"win_rate": 0, "n_trades": 0, "viable": False}

    @staticmethod
    def _eval_momentum(df: pl.DataFrame, direction: str) -> Dict:
        if direction == "UP":
            trades = df.filter(pl.col("first_break_dir") == "UP")
            if trades.height == 0:
                return {"win_rate": 0, "n_trades": 0, "viable": False}
            wins = trades.filter(
                pl.col("time_tp_up").is_not_null() &
                (pl.col("time_sl_up").is_null() | (pl.col("time_tp_up") < pl.col("time_sl_up")))
            ).height
            losses = trades.filter(
                pl.col("time_sl_up").is_not_null() &
                (pl.col("time_tp_up").is_null() | (pl.col("time_sl_up") <= pl.col("time_tp_up")))
            ).height
        else:
            trades = df.filter(pl.col("first_break_dir") == "DOWN")
            if trades.height == 0:
                return {"win_rate": 0, "n_trades": 0, "viable": False}
            wins = trades.filter(
                pl.col("time_tp_down").is_not_null() &
                (pl.col("time_sl_down").is_null() | (pl.col("time_tp_down") < pl.col("time_sl_down")))
            ).height
            losses = trades.filter(
                pl.col("time_sl_down").is_not_null() &
                (pl.col("time_tp_down").is_null() | (pl.col("time_sl_down") <= pl.col("time_tp_down")))
            ).height

        n = wins + losses
        if n == 0:
            return {"win_rate": 0, "n_trades": 0, "viable": False}
        return {"win_rate": wins / n, "n_trades": n, "wins": wins, "losses": losses, "viable": True}

    @staticmethod
    def _eval_fade(df: pl.DataFrame, direction: str) -> Dict:
        if direction == "UP":
            trades = df.filter(pl.col("first_break_dir") == "UP")
            if trades.height == 0:
                return {"win_rate": 0, "n_trades": 0, "viable": False}
            wins = trades.filter(
                pl.col("time_sl_up").is_not_null() &
                (pl.col("time_tp_up").is_null() | (pl.col("time_sl_up") < pl.col("time_tp_up")))
            ).height
            losses = trades.filter(
                pl.col("time_tp_up").is_not_null() &
                (pl.col("time_sl_up").is_null() | (pl.col("time_tp_up") <= pl.col("time_sl_up")))
            ).height
        else:
            trades = df.filter(pl.col("first_break_dir") == "DOWN")
            if trades.height == 0:
                return {"win_rate": 0, "n_trades": 0, "viable": False}
            wins = trades.filter(
                pl.col("time_sl_down").is_not_null() &
                (pl.col("time_tp_down").is_null() | (pl.col("time_sl_down") < pl.col("time_tp_down")))
            ).height
            losses = trades.filter(
                pl.col("time_tp_down").is_not_null() &
                (pl.col("time_sl_down").is_null() | (pl.col("time_tp_down") <= pl.col("time_tp_down")))
            ).height

        n = wins + losses
        if n == 0:
            return {"win_rate": 0, "n_trades": 0, "viable": False}
        return {"win_rate": wins / n, "n_trades": n, "wins": wins, "losses": losses,
                "r_per_win": 1.0, "r_per_loss": -1.0, "viable": True}

    @staticmethod
    def _eval_shakeout(df: pl.DataFrame, direction: str) -> Dict:
        if direction == "UP":
            false_days = df.filter(
                (pl.col("first_break_dir") == "UP") &
                pl.col("time_sl_up").is_not_null() &
                (pl.col("time_tp_up").is_null() | (pl.col("time_sl_up") < pl.col("time_tp_up")))
            )
            if false_days.height == 0 or "pf_up_rebreak_1x" not in df.columns:
                return {"win_rate": 0, "n_trades": 0, "viable": False}
            pf_days = false_days.filter(pl.col("pf_up_max_reversal_up").is_not_null())
            if pf_days.height < 10:
                return {"win_rate": 0, "n_trades": 0, "viable": False}
            wins = pf_days.filter(pl.col("pf_up_rebreak_1x") == True).height
            losses = pf_days.height - wins
        else:
            false_days = df.filter(
                (pl.col("first_break_dir") == "DOWN") &
                pl.col("time_sl_down").is_not_null() &
                (pl.col("time_tp_down").is_null() | (pl.col("time_sl_down") < pl.col("time_tp_down")))
            )
            if false_days.height == 0 or "pf_down_rebreak_1x" not in df.columns:
                return {"win_rate": 0, "n_trades": 0, "viable": False}
            pf_days = false_days.filter(pl.col("pf_down_max_reversal_down").is_not_null())
            if pf_days.height < 10:
                return {"win_rate": 0, "n_trades": 0, "viable": False}
            wins = pf_days.filter(pl.col("pf_down_rebreak_1x") == True).height
            losses = pf_days.height - wins

        n = wins + losses
        return {"win_rate": wins / n if n > 0 else 0, "n_trades": n, "wins": wins, "losses": losses,
                "r_per_win": 1.0, "r_per_loss": -1.0, "viable": True}

    @classmethod
    def scan_asset(cls, symbol: str, stats_by_combo: Dict[str, pl.DataFrame],
                   combo_meta: List[Dict]) -> List[Dict]:
        all_strategies = []

        for meta in combo_meta:
            key = f"{meta['session_name']}_{meta['duration']}"
            stats_df = stats_by_combo.get(key)
            if stats_df is None:
                continue

            for arch in cls.ARCHETYPES:
                for direction in cls.DIRECTIONS:
                    result = cls.evaluate_archetype(stats_df, arch, direction)
                    if result.get("viable") and result["n_trades"] >= cls.MIN_DAYS:
                        all_strategies.append({
                            "symbol": symbol,
                            "session_name": meta["session_name"],
                            "time_start": meta["time_start"],
                            "duration": meta["duration"],
                            "archetype": f"{arch}_{direction}",
                            "direction": direction,
                            "context_filter": None,
                            "context_label": "BASE",
                            "win_rate": result["win_rate"],
                            "n_trades": result["n_trades"],
                            "wins": result.get("wins", 0),
                            "losses": result.get("losses", 0),
                        })

                    for filt_key, filt_def in cls.CONTEXT_FILTERS.items():
                        result = cls.evaluate_archetype(stats_df, arch, direction, filt_def)
                        if result.get("viable") and result["n_trades"] >= cls.MIN_DAYS:
                            all_strategies.append({
                                "symbol": symbol,
                                "session_name": meta["session_name"],
                                "time_start": meta["time_start"],
                                "duration": meta["duration"],
                                "archetype": f"{arch}_{direction}",
                                "direction": direction,
                                "context_filter": filt_def,
                                "context_label": filt_def["label"],
                                "win_rate": result["win_rate"],
                                "n_trades": result["n_trades"],
                                "wins": result.get("wins", 0),
                                "losses": result.get("losses", 0),
                            })

        all_strategies.sort(key=lambda x: x["win_rate"], reverse=True)
        return all_strategies
