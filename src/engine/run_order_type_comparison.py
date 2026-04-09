"""
Order Type Comparison Backtest — LIMIT vs STOP vs MIXED
Usa las mismas 108 estrategias del bot_config.json y compara:
  A) Todas FADE (LIMIT) — lógica actual del bot
  B) Todas MOMENTUM (STOP) — breakout-following en lugar de fade
  C) MIXTO — FADE para pares con WR >= umbral fade, MOMENTUM para el resto
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


def compute_trades_fade(filtered, direction, friction):
    """FADE: gana cuando SL toca primero (precio revierte). LIMIT order logic."""
    if direction == "UP":
        trades = filtered.filter(pl.col("first_break_dir") == "UP")
        trades = trades.with_columns(
            pl.when(
                pl.col("time_sl_up").is_not_null()
                & (pl.col("time_tp_up").is_null() | (pl.col("time_sl_up") < pl.col("time_tp_up")))
            ).then(1.0 - friction)
            .when(
                pl.col("time_tp_up").is_not_null()
                & (pl.col("time_sl_up").is_null() | (pl.col("time_tp_up") <= pl.col("time_sl_up")))
            ).then(-1.0 - friction)
            .otherwise(0.0)
            .alias("pnl_r")
        )
    else:
        trades = filtered.filter(pl.col("first_break_dir") == "DOWN")
        trades = trades.with_columns(
            pl.when(
                pl.col("time_sl_down").is_not_null()
                & (pl.col("time_tp_down").is_null() | (pl.col("time_sl_down") < pl.col("time_tp_down")))
            ).then(1.0 - friction)
            .when(
                pl.col("time_tp_down").is_not_null()
                & (pl.col("time_sl_down").is_null() | (pl.col("time_tp_down") <= pl.col("time_sl_down")))
            ).then(-1.0 - friction)
            .otherwise(0.0)
            .alias("pnl_r")
        )
    return trades.filter(pl.col("pnl_r") != 0.0)


def compute_trades_momentum(filtered, direction, friction, tp_mult=1.5):
    """MOMENTUM: gana cuando TP toca primero (precio continúa). STOP order logic."""
    if direction == "UP":
        trades = filtered.filter(pl.col("first_break_dir") == "UP")
        trades = trades.with_columns(
            pl.when(
                pl.col("time_tp_up").is_not_null()
                & (pl.col("time_sl_up").is_null() | (pl.col("time_tp_up") < pl.col("time_sl_up")))
            ).then(pl.lit(tp_mult) - friction)
            .when(
                pl.col("time_sl_up").is_not_null()
                & (pl.col("time_tp_up").is_null() | (pl.col("time_sl_up") <= pl.col("time_tp_up")))
            ).then(-1.0 - friction)
            .otherwise(0.0)
            .alias("pnl_r")
        )
    else:
        trades = filtered.filter(pl.col("first_break_dir") == "DOWN")
        trades = trades.with_columns(
            pl.when(
                pl.col("time_tp_down").is_not_null()
                & (pl.col("time_sl_down").is_null() | (pl.col("time_tp_down") < pl.col("time_sl_down")))
            ).then(pl.lit(tp_mult) - friction)
            .when(
                pl.col("time_sl_down").is_not_null()
                & (pl.col("time_tp_down").is_null() | (pl.col("time_tp_down") <= pl.col("time_sl_down")))
            ).then(-1.0 - friction)
            .otherwise(0.0)
            .alias("pnl_r")
        )
    return trades.filter(pl.col("pnl_r") != 0.0)


def simulate_portfolio(trades_list, initial_balance, risk_cfg):
    """Simula portfolio con balance fijo y dedup 1/día/símbolo."""
    all_trades = []
    for t in trades_list:
        all_trades.extend(t)

    all_trades.sort(key=lambda x: (x["date"], x["exec_mins"]))

    # Dedup: 1 trade per day per symbol
    seen = set()
    deduped = []
    for t in all_trades:
        key = (t["date"], t["symbol"])
        if key not in seen:
            seen.add(key)
            deduped.append(t)

    if not deduped:
        return {"balance": initial_balance, "trades": 0, "wins": 0, "wr": 0,
                "pf": 0, "net_r": 0, "pnl_usd": 0, "max_dd_pct": 0, "yearly": {}}

    balance = initial_balance
    peak = initial_balance
    max_dd_pct = 0.0
    yearly = defaultdict(lambda: {"trades": 0, "wins": 0, "pnl_usd": 0.0, "pnl_r": 0.0})

    for t in deduped:
        risk_amount = initial_balance * t["risk_pct"]
        dollar_pnl = t["pnl_r"] * risk_amount
        balance += dollar_pnl

        peak = max(peak, balance)
        dd_pct = (balance - peak) / peak if peak > 0 else 0
        max_dd_pct = min(max_dd_pct, dd_pct)

        year = t["date"][:4]
        yearly[year]["trades"] += 1
        yearly[year]["pnl_usd"] += dollar_pnl
        yearly[year]["pnl_r"] += t["pnl_r"]
        if t["pnl_r"] > 0:
            yearly[year]["wins"] += 1

    total = len(deduped)
    wins = sum(1 for t in deduped if t["pnl_r"] > 0)
    pnls = [t["pnl_r"] for t in deduped]
    gross_p = sum(p for p in pnls if p > 0)
    gross_l = abs(sum(p for p in pnls if p < 0))

    return {
        "balance": balance,
        "trades": total,
        "wins": wins,
        "wr": wins / total if total > 0 else 0,
        "pf": gross_p / gross_l if gross_l > 0 else 99.9,
        "net_r": sum(pnls),
        "pnl_usd": balance - initial_balance,
        "max_dd_pct": max_dd_pct,
        "yearly": dict(yearly),
        "deduped": deduped,
    }


def run_comparison(initial_balance=20000.0):
    ROOT = "c:/Proyectos/kha0sys3"
    data_dir = os.path.join(ROOT, "data")
    config_path = os.path.join(ROOT, "src", "infrastructure", "config", "asset_config.json")
    bot_config_path = os.path.join(ROOT, "src", "execution", "bot_config.json")
    reports_dir = os.path.join(ROOT, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    loader = CSVPolarsLoader(data_dir)
    with open(config_path, "r") as f:
        asset_config = json.load(f)
    with open(bot_config_path, "r") as f:
        bot_config = json.load(f)

    portfolio = bot_config["portfolio"]
    risk_cfg = bot_config["risk_scaling"]
    allocator = DynamicRiskAllocator(**risk_cfg)
    print(f"Portfolio: {len(portfolio)} estrategias")

    # Group by (symbol, magic_time, duration)
    combo_strategies = defaultdict(list)
    for strat in portfolio:
        sym_internal = MT5_TO_INTERNAL.get(strat["sym"], strat["sym"])
        key = (sym_internal, strat["magic_time"], strat["duration"])
        combo_strategies[key].append(strat)

    # Collect trades for each scenario
    trades_fade = []      # A: todas LIMIT/FADE
    trades_momentum = []  # B: todas STOP/MOMENTUM
    trades_mixed = []     # C: mixto inteligente

    # Per-strategy comparison for mixed selection
    strat_comparison = []

    for (sym, time_start, duration), strats in combo_strategies.items():
        cfg = asset_config.get(sym)
        if not cfg:
            continue

        try:
            df_raw = loader.load_data(sym, "M15")
            df_raw = DataEnricher.enrich_with_rsi(df_raw)
            df_enriched = DataEnricher.enrich_with_daily_context(df_raw, cfg["pd_start"], cfg["pd_end"])
            df_or = DataEnricher.enrich_with_opening_range(df_enriched, time_start, duration)
            stats_df = TrackerEngine.track_events(df_or, tp_multiplier=DEFAULT_TP_MULTIPLIER)

            agg_cols = [pl.col("or_open").first(), pl.col("pd_or_high").first(), pl.col("pd_or_low").first()]
            for col_name in ["rsi_at_or_close", "rsi_daily_14", "atr_change",
                              "atr_percentile", "or_position_vs_pd", "or_open_vs_pd_close"]:
                if col_name in df_or.columns:
                    agg_cols.append(pl.col(col_name).first())

            daily_base = df_or.group_by("trade_date").agg(agg_cols)
            expanded = daily_base.join(stats_df, on="trade_date", how="left")
            expanded = TrackerEngine.track_post_fade_events(df_or, expanded)
            expanded = expanded.with_columns(
                pl.col("trade_date").cast(pl.Date).dt.weekday().alias("day_of_week")
            )
            if "or_width" in expanded.columns:
                q25 = expanded.select(pl.col("or_width").quantile(0.25)).item()
                q75 = expanded.select(pl.col("or_width").quantile(0.75)).item()
                if q25 is not None and q75 is not None:
                    expanded = expanded.with_columns([
                        (pl.col("or_width") <= q25).alias("or_width_q1"),
                        (pl.col("or_width") >= q75).alias("or_width_q4"),
                    ])

            valid = expanded.filter(
                pl.col("first_break_dir").is_not_null()
                & pl.col("or_atr_ratio").is_between(ATR_RATIO_LOW, ATR_RATIO_HIGH)
            ).sort("trade_date")

        except Exception as e:
            print(f"  ERROR {sym} {time_start} {duration}m: {e}")
            continue

        friction = FRICTION_INDEX if sym in INDEX_SYMBOLS else FRICTION_FX

        for strat in strats:
            edge = strat["edge"]
            direction = edge.split("_")[-1]
            context_label = strat.get("context")
            context_filter = resolve_context_filter(context_label)
            win_rate_cfg = strat["win_rate"]
            risk_pct = allocator.get_risk_percent(win_rate_cfg)

            filtered = valid
            if context_filter:
                filtered = StrategyScanner.apply_context_filter(filtered, context_filter)

            h, m_ = map(int, time_start.split(':'))
            exec_mins = h * 60 + m_ + duration
            strat_label = f"{sym}|{strat['session']}|{edge}|{duration}m|{context_label or 'BASE'}"

            # A: FADE (LIMIT)
            fade_trades = compute_trades_fade(filtered, direction, friction)
            fade_rows = []
            for row in fade_trades.select(["trade_date", "pnl_r"]).iter_rows(named=True):
                fade_rows.append({
                    "date": str(row["trade_date"]),
                    "symbol": sym,
                    "edge": edge,
                    "session": strat["session"],
                    "duration": duration,
                    "pnl_r": row["pnl_r"],
                    "risk_pct": risk_pct,
                    "exec_mins": exec_mins,
                    "strat_label": strat_label,
                })
            trades_fade.append(fade_rows)

            # B: MOMENTUM (STOP)
            mom_trades = compute_trades_momentum(filtered, direction, friction, DEFAULT_TP_MULTIPLIER)
            mom_rows = []
            for row in mom_trades.select(["trade_date", "pnl_r"]).iter_rows(named=True):
                mom_rows.append({
                    "date": str(row["trade_date"]),
                    "symbol": sym,
                    "edge": f"MOMENTUM_{direction}",
                    "session": strat["session"],
                    "duration": duration,
                    "pnl_r": row["pnl_r"],
                    "risk_pct": risk_pct,
                    "exec_mins": exec_mins,
                    "strat_label": strat_label.replace("FADE", "MOM"),
                })
            trades_momentum.append(mom_rows)

            # Compute per-strategy metrics for mixed selection
            fade_pnls = [r["pnl_r"] for r in fade_rows]
            mom_pnls = [r["pnl_r"] for r in mom_rows]
            fade_wr = sum(1 for p in fade_pnls if p > 0) / len(fade_pnls) if fade_pnls else 0
            mom_wr = sum(1 for p in mom_pnls if p > 0) / len(mom_pnls) if mom_pnls else 0
            fade_net = sum(fade_pnls)
            mom_net = sum(mom_pnls)

            strat_comparison.append({
                "label": strat_label,
                "symbol": sym,
                "direction": direction,
                "session": strat["session"],
                "fade_trades": len(fade_pnls),
                "fade_wr": fade_wr,
                "fade_net_r": fade_net,
                "mom_trades": len(mom_pnls),
                "mom_wr": mom_wr,
                "mom_net_r": mom_net,
                "best": "FADE" if fade_net >= mom_net else "MOMENTUM",
            })

            # C: MIXED — pick best per strategy
            if fade_net >= mom_net:
                trades_mixed.append(fade_rows)
            else:
                trades_mixed.append(mom_rows)

    # Run simulations
    print("\n" + "=" * 70)
    print("SIMULANDO 3 ESCENARIOS...")
    print("=" * 70)

    res_a = simulate_portfolio(trades_fade, initial_balance, risk_cfg)
    res_b = simulate_portfolio(trades_momentum, initial_balance, risk_cfg)
    res_c = simulate_portfolio(trades_mixed, initial_balance, risk_cfg)

    # Generate report
    report_path = os.path.join(reports_dir, "Order_Type_Comparison.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Comparación: LIMIT (FADE) vs STOP (MOMENTUM) vs MIXTO\n\n")
        f.write(f"> Balance inicial: ${initial_balance:,.0f} | Riesgo dinámico 1-6%\n")
        f.write(f"> Dedup: 1 trade/día/símbolo | TP: {DEFAULT_TP_MULTIPLIER}R\n\n")

        f.write("## Resultado Principal\n\n")
        f.write("| Métrica | A: FADE (LIMIT) | B: MOMENTUM (STOP) | C: MIXTO |\n")
        f.write("|:---|:---|:---|:---|\n")
        for label, key in [
            ("Balance Final", "balance"),
            ("Ganancia $", "pnl_usd"),
            ("Total Trades", "trades"),
            ("Wins", "wins"),
            ("Win Rate", "wr"),
            ("Profit Factor", "pf"),
            ("Net R", "net_r"),
            ("Max Drawdown", "max_dd_pct"),
        ]:
            va = res_a[key]
            vb = res_b[key]
            vc = res_c[key]
            if key == "balance":
                f.write(f"| **{label}** | `${va:,.2f}` | `${vb:,.2f}` | `${vc:,.2f}` |\n")
            elif key == "pnl_usd":
                f.write(f"| **{label}** | `${va:,.2f}` | `${vb:,.2f}` | `${vc:,.2f}` |\n")
            elif key in ("trades", "wins"):
                f.write(f"| **{label}** | `{va:,}` | `{vb:,}` | `{vc:,}` |\n")
            elif key == "wr":
                f.write(f"| **{label}** | `{va:.1%}` | `{vb:.1%}` | `{vc:.1%}` |\n")
            elif key == "pf":
                f.write(f"| **{label}** | `{va:.2f}` | `{vb:.2f}` | `{vc:.2f}` |\n")
            elif key == "net_r":
                f.write(f"| **{label}** | `{va:.1f}R` | `{vb:.1f}R` | `{vc:.1f}R` |\n")
            elif key == "max_dd_pct":
                f.write(f"| **{label}** | `{va:.1%}` | `{vb:.1%}` | `{vc:.1%}` |\n")
        f.write("\n")

        # Yearly comparison
        all_years = sorted(set(
            list(res_a.get("yearly", {}).keys()) +
            list(res_b.get("yearly", {}).keys()) +
            list(res_c.get("yearly", {}).keys())
        ))
        if all_years:
            f.write("## Rendimiento Anual Comparado\n\n")
            f.write("| Año | FADE WR | FADE PnL$ | MOM WR | MOM PnL$ | MIX WR | MIX PnL$ |\n")
            f.write("|:---|:---|:---|:---|:---|:---|:---|\n")
            for yr in all_years:
                ya = res_a["yearly"].get(yr, {"trades": 0, "wins": 0, "pnl_usd": 0})
                yb = res_b["yearly"].get(yr, {"trades": 0, "wins": 0, "pnl_usd": 0})
                yc = res_c["yearly"].get(yr, {"trades": 0, "wins": 0, "pnl_usd": 0})
                wr_a = ya["wins"] / ya["trades"] if ya["trades"] > 0 else 0
                wr_b = yb["wins"] / yb["trades"] if yb["trades"] > 0 else 0
                wr_c = yc["wins"] / yc["trades"] if yc["trades"] > 0 else 0
                f.write(f"| **{yr}** | `{wr_a:.1%}` | `${ya['pnl_usd']:,.0f}` | "
                        f"`{wr_b:.1%}` | `${yb['pnl_usd']:,.0f}` | "
                        f"`{wr_c:.1%}` | `${yc['pnl_usd']:,.0f}` |\n")
            f.write("\n")

        # Per-strategy comparison
        f.write("## Comparación por Estrategia: FADE vs MOMENTUM\n\n")
        f.write("| Estrategia | FADE Trades | FADE WR | FADE Net R | MOM Trades | MOM WR | MOM Net R | Mejor |\n")
        f.write("|:---|:---|:---|:---|:---|:---|:---|:---|\n")
        strat_comparison.sort(key=lambda x: x["fade_net_r"] - x["mom_net_r"], reverse=True)
        for s in strat_comparison:
            better = "**FADE**" if s["best"] == "FADE" else "**MOM**"
            f.write(
                f"| {s['label']} | {s['fade_trades']} | `{s['fade_wr']:.1%}` | `{s['fade_net_r']:.1f}` | "
                f"{s['mom_trades']} | `{s['mom_wr']:.1%}` | `{s['mom_net_r']:.1f}` | {better} |\n"
            )
        f.write("\n")

        # Summary counts
        n_fade_wins = sum(1 for s in strat_comparison if s["best"] == "FADE")
        n_mom_wins = sum(1 for s in strat_comparison if s["best"] == "MOMENTUM")
        f.write(f"### Resumen: {n_fade_wins} estrategias mejor como FADE, {n_mom_wins} mejor como MOMENTUM\n\n")

        # Architecture notes
        f.write("---\n### Notas\n")
        f.write("- **FADE (LIMIT):** Entrada contra el breakout. Sell Limit en OR_HIGH, Buy Limit en OR_LOW.\n")
        f.write("  Gana cuando el precio revierte al otro lado del OR (SL del breakout original).\n")
        f.write("- **MOMENTUM (STOP):** Entrada a favor del breakout. Buy Stop en OR_HIGH, Sell Stop en OR_LOW.\n")
        f.write(f"  Gana cuando el precio continúa {DEFAULT_TP_MULTIPLIER}x OR width más allá del breakout.\n")
        f.write("- **MIXTO:** Selecciona el mejor tipo de orden por estrategia individual (backtest Net R).\n")
        f.write("  Nota: selección con beneficio de hindsight — en live habría que validar con walk-forward.\n")

    print(f"\nReporte: {report_path}")

    # Console summary
    print(f"\n{'='*70}")
    print(f"  A) FADE (LIMIT):     ${res_a['pnl_usd']:>10,.2f}  |  WR {res_a['wr']:.1%}  |  PF {res_a['pf']:.2f}  |  DD {res_a['max_dd_pct']:.1%}  |  {res_a['trades']} trades")
    print(f"  B) MOMENTUM (STOP):  ${res_b['pnl_usd']:>10,.2f}  |  WR {res_b['wr']:.1%}  |  PF {res_b['pf']:.2f}  |  DD {res_b['max_dd_pct']:.1%}  |  {res_b['trades']} trades")
    print(f"  C) MIXTO:            ${res_c['pnl_usd']:>10,.2f}  |  WR {res_c['wr']:.1%}  |  PF {res_c['pf']:.2f}  |  DD {res_c['max_dd_pct']:.1%}  |  {res_c['trades']} trades")
    print(f"  Mejor por estrategia: {n_fade_wins} FADE vs {n_mom_wins} MOMENTUM")
    print(f"{'='*70}")


if __name__ == "__main__":
    bal = float(sys.argv[1]) if len(sys.argv) > 1 else 20000.0
    run_comparison(bal)
