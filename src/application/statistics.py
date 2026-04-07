import polars as pl
from typing import Dict, Any

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
            pl.col("or_atr_ratio").is_between(0.1, 0.8)
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
        df_open_above = df.filter(pl.col("or_open") > pl.col("pd_close"))
        p_up_given_gap_up = df_open_above.filter(pl.col("first_break_dir") == "UP").height / max(1, df_open_above.height)
        
        df_open_below = df.filter(pl.col("or_open") < pl.col("pd_close"))
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
        
        # Previous Day Touches
        touches_up = break_up_days.filter(pl.col("touches_pd_high") > 0).height / max(1, break_up_days.height)
        touches_down = break_down_days.filter(pl.col("touches_pd_low") > 0).height / max(1, break_down_days.height)
        
        # New interactions regardless of direction (or conditional if needed)
        t_pd_close = df.filter(pl.col("touches_pd_close") > 0).height / total_days
        t_pd_mid = df.filter(pl.col("touches_pd_mid") > 0).height / total_days
        t_pd_or_high = df.filter(pl.col("touches_pd_or_high") > 0).height / total_days
        t_pd_or_low = df.filter(pl.col("touches_pd_or_low") > 0).height / total_days
        
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
            dow_df = df.filter(pl.col("day_of_week") == d_num)
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
            "pd_interactions": touch_stats,
            "day_of_week": dow_stats,
            "advanced_crossing": adv
        }
