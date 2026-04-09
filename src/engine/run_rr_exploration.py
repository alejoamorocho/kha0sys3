"""
R:R Exploration — Encuentra el TP/SL óptimo por estrategia.
Prueba múltiples niveles de TP y SL sobre datos de velas post-OR,
determinando cronológicamente cuál se toca primero.

Restricciones:
  1. No disminuir la cantidad de trades vs baseline (TP=1x, SL=1x)
  2. Aumentar el PnL neto

Output: tabla por estrategia con el R:R óptimo y comparación vs baseline.
"""

import json
import os
import sys
import numpy as np
import polars as pl
from collections import defaultdict

from src.infrastructure.data.polars_loader import CSVPolarsLoader
from src.application.calculators import DataEnricher
from src.application.trackers import TrackerEngine
from src.engine.strategy_scanner import StrategyScanner
from src.domain.constants import (
    MT5_TO_INTERNAL, INDEX_SYMBOLS, FRICTION_FX, FRICTION_INDEX,
    ATR_RATIO_LOW, ATR_RATIO_HIGH, DEFAULT_TP_MULTIPLIER,
)
from src.execution.risk_manager import DynamicRiskAllocator


TP_MULTS = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0]
SL_MULTS = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]


def resolve_context_filter(context_label):
    if not context_label:
        return None
    for filt_def in StrategyScanner.CONTEXT_FILTERS.values():
        if filt_def["label"] == context_label:
            return filt_def
    for filt_def in StrategyScanner.COMBO_FILTERS.values():
        if filt_def["label"] == context_label:
            return filt_def
    return None


def track_multi_level_fade(post_or_df: pl.DataFrame, direction: str,
                           tp_mults: list, sl_mults: list) -> pl.DataFrame:
    """Track first hit times for multiple TP and SL levels per day.

    For FADE_UP (short from OR_HIGH):
      TP level = OR_HIGH - tp_mult * OR_WIDTH  (price drops, we profit)
      SL level = OR_HIGH + sl_mult * OR_WIDTH  (price rises, we lose)

    For FADE_DOWN (long from OR_LOW):
      TP level = OR_LOW + tp_mult * OR_WIDTH   (price rises, we profit)
      SL level = OR_LOW - sl_mult * OR_WIDTH   (price drops, we lose)

    Returns DataFrame with trade_date + time columns for each level.
    """
    df = post_or_df.filter(pl.col("is_active_session") == True)
    if df.height == 0:
        return pl.DataFrame()

    agg_exprs = []

    if direction == "UP":
        # FADE_UP: short from OR_HIGH
        for tp in tp_mults:
            # TP hit: LOW drops to OR_HIGH - tp * OR_WIDTH = OR_LOW + (1-tp)*OR_WIDTH
            # Simplified: LOW <= OR_HIGH - tp * OR_WIDTH
            col_name = f"time_tp_{tp:.2f}"
            tp_df = df.filter(
                pl.col("low") <= (pl.col("or_high") - pl.col("or_width") * tp)
            ).group_by("trade_date").agg(
                pl.col("mins_from_midnight").min().alias(col_name)
            )
            agg_exprs.append((col_name, tp_df))

        for sl in sl_mults:
            col_name = f"time_sl_{sl:.2f}"
            sl_df = df.filter(
                pl.col("high") >= (pl.col("or_high") + pl.col("or_width") * sl)
            ).group_by("trade_date").agg(
                pl.col("mins_from_midnight").min().alias(col_name)
            )
            agg_exprs.append((col_name, sl_df))

        # Also track first break direction
        break_up = df.filter(pl.col("high") >= pl.col("or_high")).group_by("trade_date").agg(
            pl.col("mins_from_midnight").min().alias("time_break_up")
        )
        break_down = df.filter(pl.col("low") <= pl.col("or_low")).group_by("trade_date").agg(
            pl.col("mins_from_midnight").min().alias("time_break_down")
        )

    else:
        # FADE_DOWN: long from OR_LOW
        for tp in tp_mults:
            col_name = f"time_tp_{tp:.2f}"
            tp_df = df.filter(
                pl.col("high") >= (pl.col("or_low") + pl.col("or_width") * tp)
            ).group_by("trade_date").agg(
                pl.col("mins_from_midnight").min().alias(col_name)
            )
            agg_exprs.append((col_name, tp_df))

        for sl in sl_mults:
            col_name = f"time_sl_{sl:.2f}"
            sl_df = df.filter(
                pl.col("low") <= (pl.col("or_low") - pl.col("or_width") * sl)
            ).group_by("trade_date").agg(
                pl.col("mins_from_midnight").min().alias(col_name)
            )
            agg_exprs.append((col_name, sl_df))

        break_up = df.filter(pl.col("high") >= pl.col("or_high")).group_by("trade_date").agg(
            pl.col("mins_from_midnight").min().alias("time_break_up")
        )
        break_down = df.filter(pl.col("low") <= pl.col("or_low")).group_by("trade_date").agg(
            pl.col("mins_from_midnight").min().alias("time_break_down")
        )

    # Build base with trade dates
    base = df.select("trade_date").unique()
    result = base.join(break_up, on="trade_date", how="left")
    result = result.join(break_down, on="trade_date", how="left")

    for col_name, level_df in agg_exprs:
        result = result.join(level_df, on="trade_date", how="left")

    # Add first_break_dir
    result = result.with_columns(
        pl.when(
            pl.col("time_break_up").is_not_null() & pl.col("time_break_down").is_null()
        ).then(pl.lit("UP"))
        .when(
            pl.col("time_break_down").is_not_null() & pl.col("time_break_up").is_null()
        ).then(pl.lit("DOWN"))
        .when(pl.col("time_break_up") < pl.col("time_break_down"))
        .then(pl.lit("UP"))
        .when(pl.col("time_break_down") < pl.col("time_break_up"))
        .then(pl.lit("DOWN"))
        .otherwise(pl.lit("NONE"))
        .alias("first_break_dir")
    )

    return result


def evaluate_rr(multi_df: pl.DataFrame, direction: str,
                tp_mult: float, sl_mult: float, friction: float) -> dict:
    """Evaluate a specific TP/SL combination on FADE trades."""
    tp_col = f"time_tp_{tp_mult:.2f}"
    sl_col = f"time_sl_{sl_mult:.2f}"

    if tp_col not in multi_df.columns or sl_col not in multi_df.columns:
        return {"trades": 0, "wins": 0, "wr": 0, "net_r": 0, "pnl_per_trade": 0}

    # Filter by direction
    if direction == "UP":
        trades = multi_df.filter(pl.col("first_break_dir") == "UP")
    else:
        trades = multi_df.filter(pl.col("first_break_dir") == "DOWN")

    # Compute PnL: TP hit first = win, SL hit first = loss
    trades = trades.with_columns(
        pl.when(
            pl.col(tp_col).is_not_null()
            & (pl.col(sl_col).is_null() | (pl.col(tp_col) < pl.col(sl_col)))
        ).then(tp_mult - friction)
        .when(
            pl.col(sl_col).is_not_null()
            & (pl.col(tp_col).is_null() | (pl.col(sl_col) <= pl.col(tp_col)))
        ).then(-sl_mult - friction)
        .otherwise(0.0)
        .alias("pnl_r")
    )

    resolved = trades.filter(pl.col("pnl_r") != 0.0)
    n = resolved.height
    if n == 0:
        return {"trades": 0, "wins": 0, "wr": 0, "net_r": 0, "pnl_per_trade": 0}

    wins = resolved.filter(pl.col("pnl_r") > 0).height
    net_r = resolved.select(pl.col("pnl_r").sum()).item()

    return {
        "trades": n,
        "wins": wins,
        "wr": wins / n,
        "net_r": net_r,
        "pnl_per_trade": net_r / n,
    }


def run_rr_exploration():
    ROOT = "c:/Proyectos/kha0sys3"
    loader = CSVPolarsLoader(os.path.join(ROOT, "data"))
    with open(os.path.join(ROOT, "src", "infrastructure", "config", "asset_config.json")) as f:
        asset_config = json.load(f)
    with open(os.path.join(ROOT, "src", "execution", "bot_config.json")) as f:
        bot_config = json.load(f)

    portfolio = bot_config["portfolio"]
    risk_cfg = bot_config["risk_scaling"]
    allocator = DynamicRiskAllocator(**risk_cfg)
    reports_dir = os.path.join(ROOT, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    print(f"=== R:R Exploration: {len(portfolio)} estrategias ===")
    print(f"  TP mults: {TP_MULTS}")
    print(f"  SL mults: {SL_MULTS}")

    # Group by combo
    combo_strategies = defaultdict(list)
    for strat in portfolio:
        sym = MT5_TO_INTERNAL.get(strat["sym"], strat["sym"])
        key = (sym, strat["magic_time"], strat["duration"])
        combo_strategies[key].append(strat)

    # Cache enriched post-OR data per combo
    combo_cache = {}
    for (sym, time_start, duration) in combo_strategies:
        cfg = asset_config.get(sym)
        if not cfg:
            continue
        try:
            df_raw = loader.load_data(sym, "M15")
            df_raw = DataEnricher.enrich_with_rsi(df_raw)
            df_enriched = DataEnricher.enrich_with_daily_context(df_raw, cfg["pd_start"], cfg["pd_end"])
            df_or = DataEnricher.enrich_with_opening_range(df_enriched, time_start, duration)

            # Keep post-OR candles with OR context
            post_or = df_or.filter(pl.col("is_post_or") == True)

            # ATR filter: need or_atr_ratio per day
            daily_atr = df_or.group_by("trade_date").agg(
                pl.col("or_atr_ratio").first()
            )
            valid_days = daily_atr.filter(
                pl.col("or_atr_ratio").is_between(ATR_RATIO_LOW, ATR_RATIO_HIGH)
            ).select("trade_date")

            post_or = post_or.join(valid_days, on="trade_date", how="inner")

            # Context columns for filtering
            agg_cols = []
            for c in ["rsi_at_or_close", "rsi_daily_14", "atr_change",
                       "atr_percentile", "or_position_vs_pd", "or_open_vs_pd_close",
                       "or_open", "pd_or_high", "pd_or_low"]:
                if c in df_or.columns:
                    agg_cols.append(pl.col(c).first().alias(c))
            if agg_cols:
                daily_ctx = df_or.group_by("trade_date").agg(agg_cols)
                # Add day_of_week
                daily_ctx = daily_ctx.with_columns(
                    pl.col("trade_date").cast(pl.Date).dt.weekday().alias("day_of_week")
                )
                # OR width percentiles
                if "or_width" in post_or.columns:
                    ow = post_or.group_by("trade_date").agg(pl.col("or_width").first())
                    q25 = ow.select(pl.col("or_width").quantile(0.25)).item()
                    q75 = ow.select(pl.col("or_width").quantile(0.75)).item()
                    if q25 is not None and q75 is not None:
                        daily_ctx = daily_ctx.join(ow, on="trade_date", how="left")
                        daily_ctx = daily_ctx.with_columns([
                            (pl.col("or_width") <= q25).alias("or_width_q1"),
                            (pl.col("or_width") >= q75).alias("or_width_q4"),
                        ])

                combo_cache[(sym, time_start, duration)] = (post_or, daily_ctx)
            else:
                combo_cache[(sym, time_start, duration)] = (post_or, None)

        except Exception as e:
            print(f"  ERROR loading {sym} {time_start} {duration}m: {e}")

    # Track multi-level events per combo (direction-specific)
    multi_cache = {}
    for (sym, time_start, duration), (post_or, daily_ctx) in combo_cache.items():
        for direction in ["UP", "DOWN"]:
            multi_df = track_multi_level_fade(post_or, direction, TP_MULTS, SL_MULTS)
            if daily_ctx is not None:
                # Join context for filtering
                ctx_cols = [c for c in daily_ctx.columns if c != "trade_date"]
                multi_df = multi_df.join(daily_ctx.select(["trade_date"] + ctx_cols), on="trade_date", how="left")
            multi_cache[(sym, time_start, duration, direction)] = multi_df

    # Evaluate each strategy
    results = []
    for strat in portfolio:
        sym = MT5_TO_INTERNAL.get(strat["sym"], strat["sym"])
        edge = strat["edge"]
        direction = edge.split("_")[-1]
        duration = strat["duration"]
        time_start = strat["magic_time"]
        ctx_label = strat.get("context")
        ctx_filter = resolve_context_filter(ctx_label)
        friction = FRICTION_INDEX if sym in INDEX_SYMBOLS else FRICTION_FX
        win_rate_cfg = strat["win_rate"]
        risk_pct = allocator.get_risk_percent(win_rate_cfg)
        label = f"{sym}|{strat['session']}|{edge}|{duration}m|{ctx_label or 'BASE'}"

        key = (sym, time_start, duration, direction)
        multi_df = multi_cache.get(key)
        if multi_df is None or multi_df.height == 0:
            continue

        # Apply context filter
        filtered = multi_df
        if ctx_filter:
            filtered = StrategyScanner.apply_context_filter(filtered, ctx_filter)

        if filtered.height == 0:
            continue

        # Baseline: TP=1.0, SL=1.0
        baseline = evaluate_rr(filtered, direction, 1.0, 1.0, friction)
        if baseline["trades"] == 0:
            continue

        # Test all combinations
        best = {
            "tp": 1.0, "sl": 1.0,
            **baseline,
            "improvement": 0.0,
        }

        grid_results = []
        for tp in TP_MULTS:
            for sl in SL_MULTS:
                res = evaluate_rr(filtered, direction, tp, sl, friction)
                rr_label = f"TP{tp:.1f}:SL{sl:.1f}"

                grid_results.append({
                    "tp": tp, "sl": sl, "rr_label": rr_label,
                    **res,
                })

                # Check constraints: trades >= baseline AND net_r > baseline
                if (res["trades"] >= baseline["trades"]
                        and res["net_r"] > baseline["net_r"]
                        and res["net_r"] > best["net_r"]):
                    best = {
                        "tp": tp, "sl": sl,
                        **res,
                        "improvement": res["net_r"] - baseline["net_r"],
                    }

        results.append({
            "label": label,
            "symbol": sym,
            "session": strat["session"],
            "direction": direction,
            "duration": duration,
            "risk_pct": risk_pct,
            "baseline": baseline,
            "best": best,
            "grid": grid_results,
        })

        if best["tp"] != 1.0 or best["sl"] != 1.0:
            print(f"  {label}: MEJOR TP={best['tp']:.1f} SL={best['sl']:.1f} "
                  f"| Net R: {baseline['net_r']:.1f} -> {best['net_r']:.1f} "
                  f"(+{best['improvement']:.1f}R) | WR: {baseline['wr']:.1%} -> {best['wr']:.1%} "
                  f"| Trades: {baseline['trades']} -> {best['trades']}")
        else:
            print(f"  {label}: baseline optimo (TP=1.0 SL=1.0) Net R={baseline['net_r']:.1f}")

    # =========================================================================
    # Portfolio simulation: baseline vs optimized
    # =========================================================================
    print(f"\n--- Portfolio comparison ---")
    initial_balance = 20000.0

    def simulate(results_list, use_best=False):
        all_trades = []
        for r in results_list:
            sym = r["symbol"]
            direction = r["direction"]
            filtered = multi_cache.get((sym, r["label"].split("|")[1],  # session extraction is fragile
                                         r["duration"], direction))
            # Re-derive filtered from the stored data
            # Actually let's just use the grid results to compute total portfolio
        # Simplified: sum up net_r * risk_pct for each strategy
        total_net_r = 0
        total_trades = 0
        for r in results_list:
            if use_best:
                total_net_r += r["best"]["net_r"] * r["risk_pct"]
                total_trades += r["best"]["trades"]
            else:
                total_net_r += r["baseline"]["net_r"] * r["risk_pct"]
                total_trades += r["baseline"]["trades"]
        return total_net_r * initial_balance, total_trades

    baseline_pnl, baseline_trades = simulate(results, use_best=False)
    optimized_pnl, optimized_trades = simulate(results, use_best=True)

    print(f"  Baseline (TP=1.0 SL=1.0):  PnL ~${baseline_pnl:,.0f} | {baseline_trades} trades")
    print(f"  Optimizado por estrategia:  PnL ~${optimized_pnl:,.0f} | {optimized_trades} trades")

    # =========================================================================
    # Generate Report
    # =========================================================================
    report_path = os.path.join(reports_dir, "RR_Exploration.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# R:R Exploration -- 108 Estrategias\n\n")
        f.write(f"> TP mults: {TP_MULTS}\n")
        f.write(f"> SL mults: {SL_MULTS}\n")
        f.write(f"> Restriccion: trades >= baseline AND net_r > baseline\n\n")

        # Summary of changes
        changed = [r for r in results if r["best"]["tp"] != 1.0 or r["best"]["sl"] != 1.0]
        unchanged = [r for r in results if r["best"]["tp"] == 1.0 and r["best"]["sl"] == 1.0]

        f.write(f"## Resumen\n")
        f.write(f"- **{len(changed)}** estrategias mejoran con R:R diferente\n")
        f.write(f"- **{len(unchanged)}** estrategias ya son optimas con TP=1.0 SL=1.0\n\n")

        # Changed strategies table
        if changed:
            f.write("## Estrategias con R:R Optimo Diferente\n\n")
            f.write("| Estrategia | Baseline Net R | Optimo TP:SL | Optimo Net R | Mejora R | Baseline WR | Optimo WR | Trades |\n")
            f.write("|:---|:---|:---|:---|:---|:---|:---|:---|\n")
            changed.sort(key=lambda x: x["best"]["improvement"], reverse=True)
            total_improvement = 0
            for r in changed:
                b = r["baseline"]
                o = r["best"]
                total_improvement += o["improvement"]
                f.write(f"| {r['label']} | `{b['net_r']:.1f}` | "
                        f"**TP={o['tp']:.1f} SL={o['sl']:.1f}** | `{o['net_r']:.1f}` | "
                        f"`+{o['improvement']:.1f}` | `{b['wr']:.1%}` | `{o['wr']:.1%}` | "
                        f"{b['trades']}->{o['trades']} |\n")
            f.write(f"\n**Total mejora: +{total_improvement:.1f}R**\n\n")

        # Unchanged strategies
        if unchanged:
            f.write("## Estrategias Optimas con Baseline (TP=1.0 SL=1.0)\n\n")
            f.write("| Estrategia | Net R | WR | Trades |\n")
            f.write("|:---|:---|:---|:---|\n")
            unchanged.sort(key=lambda x: x["baseline"]["net_r"], reverse=True)
            for r in unchanged:
                b = r["baseline"]
                f.write(f"| {r['label']} | `{b['net_r']:.1f}` | `{b['wr']:.1%}` | {b['trades']} |\n")
            f.write("\n")

        # Heatmap for top 10 changed strategies
        if changed:
            f.write("## Detalle Grid R:R (Top 10 estrategias con mayor mejora)\n\n")
            for r in changed[:10]:
                f.write(f"### {r['label']}\n")
                f.write(f"Baseline: TP=1.0 SL=1.0 | Net R={r['baseline']['net_r']:.1f} | WR={r['baseline']['wr']:.1%}\n\n")

                # Build grid
                f.write("| | " + " | ".join(f"SL={s:.1f}" for s in SL_MULTS) + " |\n")
                f.write("|:---|" + "|".join(":---" for _ in SL_MULTS) + "|\n")
                for tp in TP_MULTS:
                    row = f"| **TP={tp:.1f}** |"
                    for sl in SL_MULTS:
                        match = [g for g in r["grid"] if g["tp"] == tp and g["sl"] == sl]
                        if match:
                            g = match[0]
                            if g["trades"] == 0:
                                row += " - |"
                            elif g["trades"] >= r["baseline"]["trades"] and g["net_r"] > r["baseline"]["net_r"]:
                                row += f" **{g['net_r']:.1f}** ({g['wr']:.0%}) |"
                            else:
                                row += f" {g['net_r']:.1f} ({g['wr']:.0%}) |"
                        else:
                            row += " - |"
                    f.write(row + "\n")
                f.write("\n")

        # Distribution of optimal R:R
        if changed:
            f.write("## Distribucion de R:R Optimos\n\n")
            tp_dist = defaultdict(int)
            sl_dist = defaultdict(int)
            for r in changed:
                tp_dist[r["best"]["tp"]] += 1
                sl_dist[r["best"]["sl"]] += 1

            f.write("| TP Optimo | Cantidad | | SL Optimo | Cantidad |\n")
            f.write("|:---|:---|:---|:---|:---|\n")
            all_tps = sorted(tp_dist.keys())
            all_sls = sorted(sl_dist.keys())
            max_len = max(len(all_tps), len(all_sls))
            for i in range(max_len):
                tp_str = f"| **{all_tps[i]:.1f}** | {tp_dist[all_tps[i]]} |" if i < len(all_tps) else "| | |"
                sl_str = f" **{all_sls[i]:.1f}** | {sl_dist[all_sls[i]]} |" if i < len(all_sls) else " | |"
                f.write(f"{tp_str}{sl_str}\n")
            f.write("\n")

    print(f"\n{'='*70}")
    print(f"  R:R EXPLORATION COMPLETA")
    print(f"  {len(changed)} estrategias mejoran, {len(unchanged)} ya optimas")
    if changed:
        total_imp = sum(r["best"]["improvement"] for r in changed)
        print(f"  Total mejora: +{total_imp:.1f}R")
    print(f"  Reporte: {report_path}")
    print(f"{'='*70}")


if __name__ == "__main__":
    run_rr_exploration()
