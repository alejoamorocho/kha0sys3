"""Motor estadistico: probabilidades condicionales y edges sobre eventos ORB."""

import polars as pl
from typing import Dict, Any

from src.domain.constants import ATR_RATIO_LOW, ATR_RATIO_HIGH

class StatisticalEngine:
    """
    Computes Probability metrics and deep statistical edges over the vectorized events.
    """
    
    @staticmethod
    def calculate_edges(results_df: pl.DataFrame) -> Dict[str, Any]:
        """
        Takes the results_df (which is trade_date bounded and includes PD, OR stats, and tracking hit events)
        and computes conditional probabilities.
        """
        # Ensure we have day of week (1 = Monday, 7 = Sunday)
        df = results_df.with_columns(
            pl.col("trade_date").cast(pl.Date).dt.weekday().alias("day_of_week"),
            (pl.col("max_up") / pl.col("or_width")).alias("up_extension_or"),
            (pl.col("max_down") / pl.col("or_width")).alias("down_extension_or"),
            (pl.col("max_up") / pl.col("atr_14")).alias("up_extension_atr"),
            (pl.col("max_down") / pl.col("atr_14")).alias("down_extension_atr")
        )
        
        # We only work with days that had a valid OR mapped and pass the volatility filter
        valid_df = df.filter(
            pl.col("first_break_dir").is_not_null() &
            pl.col("or_atr_ratio").is_between(ATR_RATIO_LOW, ATR_RATIO_HIGH)
        )
        total_days = valid_df.height
        if total_days == 0:
            return {"error": "No valid days found"}
            
        def _get_core_edges(sub_df: pl.DataFrame, total_sub: int) -> dict:
            if total_sub == 0: return {}
            b_up = sub_df.filter(pl.col("first_break_dir") == "UP")
            b_dw = sub_df.filter(pl.col("first_break_dir") == "DOWN")
            
            p_up = b_up.height / max(1, total_sub)
            p_dw = b_dw.height / max(1, total_sub)
            
            fup = b_up.filter(pl.col("time_sl_up").is_not_null() & (pl.col("time_tp_up").is_null() | (pl.col("time_sl_up") < pl.col("time_tp_up")))).height / max(1, b_up.height)
            fdw = b_dw.filter(pl.col("time_sl_down").is_not_null() & (pl.col("time_tp_down").is_null() | (pl.col("time_sl_down") < pl.col("time_tp_down")))).height / max(1, b_dw.height)
            
            return {
                "n_days": total_sub,
                "p_break_up": p_up,
                "p_break_down": p_dw,
                "up_ext_1.5": b_up.filter(pl.col("up_extension_or") >= 1.5).height / max(1, b_up.height),
                "dw_ext_1.5": b_dw.filter(pl.col("down_extension_or") >= 1.5).height / max(1, b_dw.height),
                "f_breakup": fup,
                "f_breakdw": fdw,
                "touch_pd_close": sub_df.filter(pl.col("touches_pd_close") > 0).height / max(1, total_sub),
                "touch_pd_mid": sub_df.filter(pl.col("touches_pd_mid") > 0).height / max(1, total_sub)
            }
            
        # Basic directional probability
        break_up_days = valid_df.filter(pl.col("first_break_dir") == "UP")
        break_down_days = valid_df.filter(pl.col("first_break_dir") == "DOWN")
        
        prob_dir = {
            "p_break_up": break_up_days.height / total_days,
            "p_break_down": break_down_days.height / total_days
        }
        
        # Positional Open Edge
        df_open_above = valid_df.filter(pl.col("or_open") > pl.col("pd_close"))
        p_up_given_gap_up = df_open_above.filter(pl.col("first_break_dir") == "UP").height / max(1, df_open_above.height)

        df_open_below = valid_df.filter(pl.col("or_open") < pl.col("pd_close"))
        p_down_given_gap_down = df_open_below.filter(pl.col("first_break_dir") == "DOWN").height / max(1, df_open_below.height)
        
        # Extensions given valid breakout
        def ext_prob(sub_df, col, threshold):
            return sub_df.filter(pl.col(col) >= threshold).height / max(1, sub_df.height)
            
        extensions_up = {
            "up_gt_1_or": ext_prob(break_up_days, "up_extension_or", 1.0),
            "up_gt_1.5_or": ext_prob(break_up_days, "up_extension_or", 1.5),
            "up_gt_2_or": ext_prob(break_up_days, "up_extension_or", 2.0),
            "up_gt_1_atr": ext_prob(break_up_days, "up_extension_atr", 1.0),
        }
        
        extensions_down = {
            "down_gt_1_or": ext_prob(break_down_days, "down_extension_or", 1.0),
            "down_gt_1.5_or": ext_prob(break_down_days, "down_extension_or", 1.5),
            "down_gt_2_or": ext_prob(break_down_days, "down_extension_or", 2.0),
            "down_gt_1_atr": ext_prob(break_down_days, "down_extension_atr", 1.0),
        }
        
        # False Breakouts
        # We consider a false break up if it broke up, didn't hit 1.5 R, but hit SL
        false_breakup_days = break_up_days.filter(
            pl.col("time_sl_up").is_not_null() & 
            (pl.col("time_tp_up").is_null() | (pl.col("time_sl_up") < pl.col("time_tp_up")))
        )
        false_breakdown_days = break_down_days.filter(
            pl.col("time_sl_down").is_not_null() & 
            (pl.col("time_tp_down").is_null() | (pl.col("time_sl_down") < pl.col("time_tp_down")))
        )
        
        false_breaks = {
             "p_false_breakup": false_breakup_days.height / max(1, break_up_days.height),
             "p_false_breakdown": false_breakdown_days.height / max(1, break_down_days.height)
        }

        # Post-Fade Analysis
        post_fade_up = {}
        if "pf_up_max_reversal_up" in valid_df.columns:
            pf_up_days = valid_df.filter(pl.col("pf_up_max_reversal_up").is_not_null())
            if pf_up_days.height >= 5:
                post_fade_up = {
                    "n_false_breakups": pf_up_days.height,
                    "p_shakeout_rebreak_1x": pf_up_days.filter(pl.col("pf_up_rebreak_1x") == True).height / pf_up_days.height,
                    "p_shakeout_rebreak_1_5x": pf_up_days.filter(pl.col("pf_up_rebreak_1_5x") == True).height / pf_up_days.height,
                    "p_shakeout_rebreak_2x": pf_up_days.filter(pl.col("pf_up_rebreak_2x") == True).height / pf_up_days.height,
                    "p_continuation_down_1x": pf_up_days.filter(pl.col("pf_up_cont_1x") == True).height / pf_up_days.height,
                    "p_continuation_down_1_5x": pf_up_days.filter(pl.col("pf_up_cont_1_5x") == True).height / pf_up_days.height,
                    "mean_reversal_up": pf_up_days.select(pl.col("pf_up_max_reversal_up").mean()).item(),
                    "median_reversal_up": pf_up_days.select(pl.col("pf_up_max_reversal_up").median()).item(),
                    "mean_cont_down": pf_up_days.select(pl.col("pf_up_max_cont_down").mean()).item(),
                    "median_cont_down": pf_up_days.select(pl.col("pf_up_max_cont_down").median()).item(),
                    "mean_time_to_rebreak": pf_up_days.filter(pl.col("pf_up_time_to_rebreak").is_not_null()).select(pl.col("pf_up_time_to_rebreak").mean()).item(),
                    "median_time_to_rebreak": pf_up_days.filter(pl.col("pf_up_time_to_rebreak").is_not_null()).select(pl.col("pf_up_time_to_rebreak").median()).item(),
                }

        post_fade_down = {}
        if "pf_down_max_reversal_down" in valid_df.columns:
            pf_down_days = valid_df.filter(pl.col("pf_down_max_reversal_down").is_not_null())
            if pf_down_days.height >= 5:
                post_fade_down = {
                    "n_false_breakdowns": pf_down_days.height,
                    "p_shakeout_rebreak_1x": pf_down_days.filter(pl.col("pf_down_rebreak_1x") == True).height / pf_down_days.height,
                    "p_shakeout_rebreak_1_5x": pf_down_days.filter(pl.col("pf_down_rebreak_1_5x") == True).height / pf_down_days.height,
                    "p_shakeout_rebreak_2x": pf_down_days.filter(pl.col("pf_down_rebreak_2x") == True).height / pf_down_days.height,
                    "p_continuation_up_1x": pf_down_days.filter(pl.col("pf_down_cont_1x") == True).height / pf_down_days.height,
                    "p_continuation_up_1_5x": pf_down_days.filter(pl.col("pf_down_cont_1_5x") == True).height / pf_down_days.height,
                    "mean_reversal_down": pf_down_days.select(pl.col("pf_down_max_reversal_down").mean()).item(),
                    "median_reversal_down": pf_down_days.select(pl.col("pf_down_max_reversal_down").median()).item(),
                    "mean_cont_up": pf_down_days.select(pl.col("pf_down_max_cont_up").mean()).item(),
                    "median_cont_up": pf_down_days.select(pl.col("pf_down_max_cont_up").median()).item(),
                    "mean_time_to_rebreak": pf_down_days.filter(pl.col("pf_down_time_to_rebreak").is_not_null()).select(pl.col("pf_down_time_to_rebreak").mean()).item(),
                    "median_time_to_rebreak": pf_down_days.filter(pl.col("pf_down_time_to_rebreak").is_not_null()).select(pl.col("pf_down_time_to_rebreak").median()).item(),
                }

        # Timing to targets (in minutes from entry)
        timing = {}
        up_with_tp = break_up_days.filter(pl.col("time_tp_up").is_not_null() & pl.col("time_entry_up").is_not_null())
        if up_with_tp.height > 0:
            tp_times_up = up_with_tp.with_columns(
                (pl.col("time_tp_up") - pl.col("time_entry_up")).alias("mins_to_tp")
            )
            timing["up_mean_mins_to_tp"] = tp_times_up.select(pl.col("mins_to_tp").mean()).item()
            timing["up_median_mins_to_tp"] = tp_times_up.select(pl.col("mins_to_tp").median()).item()
            timing["up_p80_mins_to_tp"] = tp_times_up.select(pl.col("mins_to_tp").quantile(0.80)).item()

        down_with_tp = break_down_days.filter(pl.col("time_tp_down").is_not_null() & pl.col("time_entry_down").is_not_null())
        if down_with_tp.height > 0:
            tp_times_down = down_with_tp.with_columns(
                (pl.col("time_tp_down") - pl.col("time_entry_down")).alias("mins_to_tp")
            )
            timing["down_mean_mins_to_tp"] = tp_times_down.select(pl.col("mins_to_tp").mean()).item()
            timing["down_median_mins_to_tp"] = tp_times_down.select(pl.col("mins_to_tp").median()).item()
            timing["down_p80_mins_to_tp"] = tp_times_down.select(pl.col("mins_to_tp").quantile(0.80)).item()

        # Time from breakout to SL for false breaks
        up_with_sl = false_breakup_days.filter(pl.col("time_entry_up").is_not_null())
        if up_with_sl.height > 0:
            sl_times_up = up_with_sl.with_columns(
                (pl.col("time_sl_up") - pl.col("time_entry_up")).alias("mins_to_sl")
            )
            timing["up_mean_mins_to_sl"] = sl_times_up.select(pl.col("mins_to_sl").mean()).item()

        down_with_sl = false_breakdown_days.filter(pl.col("time_entry_down").is_not_null())
        if down_with_sl.height > 0:
            sl_times_down = down_with_sl.with_columns(
                (pl.col("time_sl_down") - pl.col("time_entry_down")).alias("mins_to_sl")
            )
            timing["down_mean_mins_to_sl"] = sl_times_down.select(pl.col("mins_to_sl").mean()).item()

        # Feature-Conditional Edge Segmentation
        feature_segments = {}

        def _safe_edges(sub_df, label):
            """Calculate core edges for a subset, return None if n < 20."""
            n = sub_df.height
            if n < 20:
                return None
            edges = _get_core_edges(sub_df, n)
            edges["label"] = label
            # Add post-fade shakeout rate if available
            if "pf_up_max_reversal_up" in sub_df.columns:
                pf_up = sub_df.filter(pl.col("pf_up_max_reversal_up").is_not_null())
                if pf_up.height >= 5:
                    edges["pf_shakeout_up"] = pf_up.filter(pl.col("pf_up_rebreak_1x") == True).height / pf_up.height
            if "pf_down_max_reversal_down" in sub_df.columns:
                pf_down = sub_df.filter(pl.col("pf_down_max_reversal_down").is_not_null())
                if pf_down.height >= 5:
                    edges["pf_shakeout_down"] = pf_down.filter(pl.col("pf_down_rebreak_1x") == True).height / pf_down.height
            return edges

        # RSI segments (only if column exists)
        if "rsi_at_or_close" in valid_df.columns:
            rsi_oversold = valid_df.filter(pl.col("rsi_at_or_close") < 30)
            rsi_overbought = valid_df.filter(pl.col("rsi_at_or_close") > 70)
            rsi_neutral = valid_df.filter(pl.col("rsi_at_or_close").is_between(30, 70))

            r = _safe_edges(rsi_oversold, "RSI < 30 (Oversold)")
            if r: feature_segments["rsi_oversold"] = r
            r = _safe_edges(rsi_overbought, "RSI > 70 (Overbought)")
            if r: feature_segments["rsi_overbought"] = r
            r = _safe_edges(rsi_neutral, "RSI 30-70 (Neutro)")
            if r: feature_segments["rsi_neutral"] = r

        # OR Position segments
        if "or_position_vs_pd" in valid_df.columns:
            for pos in ["ABOVE_PD_HIGH", "BELOW_PD_LOW", "BETWEEN_CLOSE_AND_HIGH", "BETWEEN_LOW_AND_CLOSE"]:
                sub = valid_df.filter(pl.col("or_position_vs_pd") == pos)
                r = _safe_edges(sub, f"OR {pos}")
                if r: feature_segments[f"or_pos_{pos.lower()}"] = r

        # ATR change segments
        if "atr_change" in valid_df.columns:
            atr_growing = valid_df.filter(pl.col("atr_change") > 0.1)
            atr_shrinking = valid_df.filter(pl.col("atr_change") < -0.1)
            r = _safe_edges(atr_growing, "ATR Creciente (>10%)")
            if r: feature_segments["atr_growing"] = r
            r = _safe_edges(atr_shrinking, "ATR Decreciente (<-10%)")
            if r: feature_segments["atr_shrinking"] = r

        # ATR percentile segments
        if "atr_percentile" in valid_df.columns:
            atr_q1 = valid_df.filter(pl.col("atr_percentile") < 25)
            atr_q4 = valid_df.filter(pl.col("atr_percentile") > 75)
            r = _safe_edges(atr_q1, "ATR Q1 (Baja Vol Historica)")
            if r: feature_segments["atr_q1"] = r
            r = _safe_edges(atr_q4, "ATR Q4 (Alta Vol Historica)")
            if r: feature_segments["atr_q4"] = r

        # RSI Daily segments
        if "rsi_daily_14" in valid_df.columns:
            rsi_d_low = valid_df.filter(pl.col("rsi_daily_14") < 35)
            rsi_d_high = valid_df.filter(pl.col("rsi_daily_14") > 65)
            r = _safe_edges(rsi_d_low, "RSI Diario < 35")
            if r: feature_segments["rsi_daily_low"] = r
            r = _safe_edges(rsi_d_high, "RSI Diario > 65")
            if r: feature_segments["rsi_daily_high"] = r

        # Previous Day Touches
        touches_up = break_up_days.filter(pl.col("touches_pd_high") > 0).height / max(1, break_up_days.height)
        touches_down = break_down_days.filter(pl.col("touches_pd_low") > 0).height / max(1, break_down_days.height)
        
        # New interactions regardless of direction (or conditional if needed)
        t_pd_close = valid_df.filter(pl.col("touches_pd_close") > 0).height / total_days
        t_pd_mid = valid_df.filter(pl.col("touches_pd_mid") > 0).height / total_days
        t_pd_or_high = valid_df.filter(pl.col("touches_pd_or_high") > 0).height / total_days
        t_pd_or_low = valid_df.filter(pl.col("touches_pd_or_low") > 0).height / total_days
        
        touch_stats = {
            "p_touch_pd_high_if_breakup": touches_up,
            "p_touch_pd_low_if_breakdown": touches_down,
            "p_touch_pd_close": t_pd_close,
            "p_touch_pd_mid": t_pd_mid,
            "p_touch_pd_or_high": t_pd_or_high,
            "p_touch_pd_or_low": t_pd_or_low
        }
        
        # Day of week statistics (Win Rate simplified > 1.5R without hitting SL)
        # 1=Mon, 2=Tue, 3=Wed, 4=Thu, 5=Fri
        day_names = {1:"Lunes", 2:"Martes", 3:"Miercoles", 4:"Jueves", 5:"Viernes"}
        dow_stats = {}
        for d_num, d_name in day_names.items():
            dow_df = valid_df.filter(pl.col("day_of_week") == d_num)
            if dow_df.height > 0:
                # We reuse the r_multiple logic dynamically
                target_mult = 1.5
                valid = dow_df.filter(pl.col("first_break_dir").is_not_null())
                # approximate simple wins
                wins_up = valid.filter(
                    (pl.col("first_break_dir") == "UP") & 
                    pl.col("time_tp_up").is_not_null() &
                    (pl.col("time_sl_up").is_null() | (pl.col("time_tp_up") < pl.col("time_sl_up")))
                ).height
                wins_down = valid.filter(
                    (pl.col("first_break_dir") == "DOWN") & 
                    pl.col("time_tp_down").is_not_null() &
                    (pl.col("time_sl_down").is_null() | (pl.col("time_tp_down") < pl.col("time_sl_down")))
                ).height
                win_rate = (wins_up + wins_down) / max(1, valid.height)
                dow_stats[d_name] = {"total": valid.height, "win_rate": win_rate}
        
        # Advanced Feature Crossing (Subsets)
        # 1. Percentiles of volatily OR Width
        q25 = valid_df.select(pl.col("or_width").quantile(0.25)).item()
        q75 = valid_df.select(pl.col("or_width").quantile(0.75)).item()
        
        df_q1 = valid_df.filter(pl.col("or_width") <= q25)
        df_q4 = valid_df.filter(pl.col("or_width") >= q75)
        
        # 2. Inside Yesterday OR vs Outside
        df_inside = valid_df.filter(
            (pl.col("or_open") <= pl.col("pd_or_high")) & 
            (pl.col("or_open") >= pl.col("pd_or_low"))
        )
        df_outside = valid_df.filter(
            (pl.col("or_open") > pl.col("pd_or_high")) | 
            (pl.col("or_open") < pl.col("pd_or_low"))
        )
        
        adv = {
             "q1_tight_width": _get_core_edges(df_q1, df_q1.height),
             "q4_loose_width": _get_core_edges(df_q4, df_q4.height),
             "inside_pd_or": _get_core_edges(df_inside, df_inside.height),
             "gap_outside_pd_or": _get_core_edges(df_outside, df_outside.height)
        }
        
        return {
            "total_evaluated_days": total_days,
            "directional": prob_dir,
            "gap_context": {
                "p_break_up_given_gap_up": p_up_given_gap_up,
                "p_break_down_given_gap_down": p_down_given_gap_down
            },
            "extensions": {
                "UP": extensions_up,
                "DOWN": extensions_down
            },
            "false_breaks": false_breaks,
            "post_fade": {
                "UP": post_fade_up,
                "DOWN": post_fade_down
            },
            "timing": timing,
            "pd_interactions": touch_stats,
            "day_of_week": dow_stats,
            "advanced_crossing": adv,
            "feature_segments": feature_segments
        }
