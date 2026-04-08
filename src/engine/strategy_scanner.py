"""Scanner de estrategias ORB: evalua permutaciones de sesion x duracion x arquetipo x contexto."""

import polars as pl
from typing import List, Dict, Optional

from src.domain.constants import ATR_RATIO_LOW, ATR_RATIO_HIGH, MIN_STRATEGY_DAYS


class StrategyScanner:
    """
    Scans all permutations of (session x duration x archetype x direction x context_filter)
    for a given asset and evaluates win rate from enriched historical data.
    """

    # MOMENTUM/SHAKEOUT: dormant — no active strategies. Ready for reactivation via bot_config.json.
    ARCHETYPES = ["MOMENTUM", "FADE", "SHAKEOUT"]
    DIRECTIONS = ["UP", "DOWN"]

    # --- Single-feature context filters (21 total) ---
    CONTEXT_FILTERS = {
        # RSI M15
        "rsi_oversold": {"col": "rsi_at_or_close", "op": "<", "val": 30, "label": "RSI<30"},
        "rsi_overbought": {"col": "rsi_at_or_close", "op": ">", "val": 70, "label": "RSI>70"},
        "rsi_low_neutral": {"col": "rsi_at_or_close", "op": "between", "val": [30, 50], "label": "RSI_30-50"},
        "rsi_high_neutral": {"col": "rsi_at_or_close", "op": "between", "val": [50, 70], "label": "RSI_50-70"},
        # ATR volatility
        "atr_growing": {"col": "atr_change", "op": ">", "val": 0.1, "label": "ATR+10%"},
        "atr_shrinking": {"col": "atr_change", "op": "<", "val": -0.1, "label": "ATR-10%"},
        # OR position vs PD
        "above_pd_high": {"col": "or_position_vs_pd", "op": "==", "val": "ABOVE_PD_HIGH", "label": "AbovePD"},
        "below_pd_low": {"col": "or_position_vs_pd", "op": "==", "val": "BELOW_PD_LOW", "label": "BelowPD"},
        "between_close_high": {"col": "or_position_vs_pd", "op": "==", "val": "BETWEEN_CLOSE_AND_HIGH", "label": "BtwCloseHigh"},
        "between_low_close": {"col": "or_position_vs_pd", "op": "==", "val": "BETWEEN_LOW_AND_CLOSE", "label": "BtwLowClose"},
        # RSI Daily
        "rsi_daily_low": {"col": "rsi_daily_14", "op": "<", "val": 35, "label": "RSI_D<35"},
        "rsi_daily_high": {"col": "rsi_daily_14", "op": ">", "val": 65, "label": "RSI_D>65"},
        # Day of week
        "dow_monday": {"col": "day_of_week", "op": "==", "val": 1, "label": "Mon"},
        "dow_tuesday": {"col": "day_of_week", "op": "==", "val": 2, "label": "Tue"},
        "dow_wednesday": {"col": "day_of_week", "op": "==", "val": 3, "label": "Wed"},
        "dow_thursday": {"col": "day_of_week", "op": "==", "val": 4, "label": "Thu"},
        "dow_friday": {"col": "day_of_week", "op": "==", "val": 5, "label": "Fri"},
        # Gap size (or_open_vs_pd_close in ATR units)
        "gap_small": {"col": "or_open_vs_pd_close", "op": "abs<", "val": 0.5, "label": "GapSmall"},
        "gap_large": {"col": "or_open_vs_pd_close", "op": "abs>", "val": 1.5, "label": "GapLarge"},
        # OR width regime (precomputed booleans)
        "or_width_q1": {"col": "or_width_q1", "op": "==", "val": True, "label": "OR_Q1_Tight"},
        "or_width_q4": {"col": "or_width_q4", "op": "==", "val": True, "label": "OR_Q4_Wide"},
    }

    # --- Multi-feature AND combinations (6 total) ---
    COMBO_FILTERS = {
        "rsi_oversold_atr_growing": {
            "conditions": [
                {"col": "rsi_at_or_close", "op": "<", "val": 30},
                {"col": "atr_change", "op": ">", "val": 0.1},
            ],
            "label": "RSI<30+ATR+"
        },
        "rsi_overbought_atr_shrinking": {
            "conditions": [
                {"col": "rsi_at_or_close", "op": ">", "val": 70},
                {"col": "atr_change", "op": "<", "val": -0.1},
            ],
            "label": "RSI>70+ATR-"
        },
        "above_pd_rsi_d_high": {
            "conditions": [
                {"col": "or_position_vs_pd", "op": "==", "val": "ABOVE_PD_HIGH"},
                {"col": "rsi_daily_14", "op": ">", "val": 65},
            ],
            "label": "AbovePD+RSI_D>65"
        },
        "below_pd_rsi_d_low": {
            "conditions": [
                {"col": "or_position_vs_pd", "op": "==", "val": "BELOW_PD_LOW"},
                {"col": "rsi_daily_14", "op": "<", "val": 35},
            ],
            "label": "BelowPD+RSI_D<35"
        },
        "q4_wide_atr_growing": {
            "conditions": [
                {"col": "or_width_q4", "op": "==", "val": True},
                {"col": "atr_change", "op": ">", "val": 0.1},
            ],
            "label": "OR_Q4+ATR+"
        },
        "q1_tight_atr_shrinking": {
            "conditions": [
                {"col": "or_width_q1", "op": "==", "val": True},
                {"col": "atr_change", "op": "<", "val": -0.1},
            ],
            "label": "OR_Q1+ATR-"
        },
    }

    MIN_DAYS = MIN_STRATEGY_DAYS

    @staticmethod
    def apply_context_filter(df: pl.DataFrame, filt: Optional[Dict]) -> pl.DataFrame:
        """Aplica filtro contextual a un DataFrame. Soporta operadores: <, >, ==, between, abs<, abs>."""
        if not filt:
            return df
        # Multi-feature AND filter
        if "conditions" in filt:
            for sub in filt["conditions"]:
                df = StrategyScanner.apply_context_filter(df, sub)
            return df
        # Single filter
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
        elif op == "between":
            return df.filter(pl.col(col).is_between(val[0], val[1]))
        elif op == "abs<":
            return df.filter(pl.col(col).abs() < val)
        elif op == "abs>":
            return df.filter(pl.col(col).abs() > val)
        return df

    @classmethod
    def evaluate_archetype(cls, stats_df: pl.DataFrame, archetype: str,
                           direction: str, context_filter: Optional[Dict] = None) -> Dict:
        """Evalua win rate de un arquetipo (MOMENTUM/FADE/SHAKEOUT) con filtro opcional."""
        valid_df = stats_df.filter(
            pl.col("first_break_dir").is_not_null() &
            pl.col("or_atr_ratio").is_between(ATR_RATIO_LOW, ATR_RATIO_HIGH)
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
        """Evalua win rate de MOMENTUM: TP hit antes de SL."""
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
        """Evalua win rate de FADE: SL hit antes de TP (false breakout)."""
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
                (pl.col("time_sl_down").is_null() | (pl.col("time_tp_down") <= pl.col("time_sl_down")))
            ).height

        n = wins + losses
        if n == 0:
            return {"win_rate": 0, "n_trades": 0, "viable": False}
        return {"win_rate": wins / n, "n_trades": n, "wins": wins, "losses": losses,
                "r_per_win": 1.0, "r_per_loss": -1.0, "viable": True}

    @staticmethod
    def _eval_shakeout(df: pl.DataFrame, direction: str) -> Dict:
        """Evalua win rate de SHAKEOUT: re-breakout tras false break."""
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
        """Escanea todas las permutaciones de sesion x duracion x arquetipo x contexto para un activo."""
        all_strategies = []

        for meta in combo_meta:
            key = f"{meta['session_name']}_{meta['duration']}"
            stats_df = stats_by_combo.get(key)
            if stats_df is None:
                continue

            for arch in cls.ARCHETYPES:
                for direction in cls.DIRECTIONS:
                    # BASE (no filter)
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

                    # Single filters
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

                    # Multi-feature AND combos
                    for filt_key, filt_def in cls.COMBO_FILTERS.items():
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
