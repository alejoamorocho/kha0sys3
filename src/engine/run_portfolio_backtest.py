"""
Portfolio Backtest — 121 estrategias, balance fijo $20k (sin interés compuesto).
Usa las mismas reglas del bot live: FADE edges, dedup 1 trade/día/símbolo,
riesgo dinámico 1-6% según win_rate, filtro ATR 0.1-0.8.
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
    ATR_RATIO_LOW, ATR_RATIO_HIGH,
)
from src.execution.risk_manager import DynamicRiskAllocator


def resolve_context_filter(context_label):
    """Map context label from bot_config back to filter definition."""
    if not context_label:
        return None
    for filt_def in StrategyScanner.CONTEXT_FILTERS.values():
        if filt_def["label"] == context_label:
            return filt_def
    for filt_def in StrategyScanner.COMBO_FILTERS.values():
        if filt_def["label"] == context_label:
            return filt_def
    return None


def run_portfolio_backtest(initial_balance=20000.0):
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
    print(f"Portfolio: {len(portfolio)} estrategias")
    print(f"Balance fijo: ${initial_balance:,.0f} (sin interés compuesto)")

    # Group strategies by (internal_symbol, magic_time, duration) to avoid recomputing stats
    combo_strategies = defaultdict(list)
    for strat in portfolio:
        sym_internal = MT5_TO_INTERNAL.get(strat["sym"], strat["sym"])
        key = (sym_internal, strat["magic_time"], strat["duration"])
        combo_strategies[key].append(strat)

    print(f"Combos únicos (symbol x time x duration): {len(combo_strategies)}")

    # Build stats once per combo, then evaluate each strategy
    all_trades = []
    strat_stats = {}
    allocator = DynamicRiskAllocator(**risk_cfg)

    for (sym, time_start, duration), strats in combo_strategies.items():
        cfg = asset_config.get(sym)
        if not cfg:
            print(f"  SKIP {sym}: no config found")
            continue

        try:
            df_raw = loader.load_data(sym, "M15")
            df_raw = DataEnricher.enrich_with_rsi(df_raw)
            df_enriched = DataEnricher.enrich_with_daily_context(df_raw, cfg["pd_start"], cfg["pd_end"])
            df_or = DataEnricher.enrich_with_opening_range(df_enriched, time_start, duration)
            stats_df = TrackerEngine.track_events(df_or, tp_multiplier=1.5)

            # Build expanded stats with context columns
            agg_cols = [pl.col("or_open").first(), pl.col("pd_or_high").first(), pl.col("pd_or_low").first()]
            for col_name in ["rsi_at_or_close", "rsi_daily_14", "atr_change",
                              "atr_percentile", "or_position_vs_pd", "or_open_vs_pd_close"]:
                if col_name in df_or.columns:
                    agg_cols.append(pl.col(col_name).first())

            daily_base = df_or.group_by("trade_date").agg(agg_cols)
            expanded = daily_base.join(stats_df, on="trade_date", how="left")
            expanded = TrackerEngine.track_post_fade_events(df_or, expanded)

            # day_of_week
            expanded = expanded.with_columns(
                pl.col("trade_date").cast(pl.Date).dt.weekday().alias("day_of_week")
            )
            # OR width percentiles
            if "or_width" in expanded.columns:
                q25 = expanded.select(pl.col("or_width").quantile(0.25)).item()
                q75 = expanded.select(pl.col("or_width").quantile(0.75)).item()
                if q25 is not None and q75 is not None:
                    expanded = expanded.with_columns([
                        (pl.col("or_width") <= q25).alias("or_width_q1"),
                        (pl.col("or_width") >= q75).alias("or_width_q4"),
                    ])

            # Filter valid days
            valid = expanded.filter(
                pl.col("first_break_dir").is_not_null()
                & pl.col("or_atr_ratio").is_between(ATR_RATIO_LOW, ATR_RATIO_HIGH)
            ).sort("trade_date")

        except Exception as e:
            print(f"  ERROR {sym} {time_start} {duration}m: {e}")
            continue

        friction = FRICTION_INDEX if sym in INDEX_SYMBOLS else FRICTION_FX

        for strat in strats:
            edge = strat["edge"]  # e.g. FADE_UP, FADE_DOWN
            direction = edge.split("_")[-1]  # UP or DOWN
            context_label = strat.get("context")
            context_filter = resolve_context_filter(context_label)
            win_rate_cfg = strat["win_rate"]
            risk_pct = allocator.get_risk_percent(win_rate_cfg)

            filtered = valid
            if context_filter:
                filtered = StrategyScanner.apply_context_filter(filtered, context_filter)

            # FADE logic: win when SL hits first (price reverts), lose when TP hits first
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

            trades = trades.filter(pl.col("pnl_r") != 0.0)

            if trades.height == 0:
                continue

            # Compute exec_mins for dedup priority (earlier session wins)
            h, m = map(int, time_start.split(':'))
            exec_mins = h * 60 + m + duration

            strat_label = f"{sym}|{strat['session']}|{edge}|{duration}m|{context_label or 'BASE'}"
            wins = trades.filter(pl.col("pnl_r") > 0).height
            total = trades.height
            actual_wr = wins / total if total > 0 else 0

            strat_stats[strat_label] = {
                "trades": total, "wins": wins, "losses": total - wins,
                "wr": actual_wr, "risk_pct": risk_pct,
                "net_r": trades.select(pl.col("pnl_r").sum()).item(),
            }

            for row in trades.select(["trade_date", "pnl_r"]).iter_rows(named=True):
                all_trades.append({
                    "date": str(row["trade_date"]),
                    "symbol": sym,
                    "edge": edge,
                    "session": strat["session"],
                    "duration": duration,
                    "context": context_label or "BASE",
                    "pnl_r": row["pnl_r"],
                    "risk_pct": risk_pct,
                    "exec_mins": exec_mins,
                    "strat_label": strat_label,
                })

    print(f"\nTotal trades brutos (antes de dedup): {len(all_trades)}")

    # Sort by date + exec_mins (earliest first)
    all_trades.sort(key=lambda x: (x["date"], x["exec_mins"]))

    # Dedup: 1 trade per day per symbol (earliest session wins)
    seen = set()
    deduped = []
    for t in all_trades:
        key = (t["date"], t["symbol"])
        if key not in seen:
            seen.add(key)
            deduped.append(t)

    print(f"Total trades deduplicados: {len(deduped)}")

    # --- Fixed balance simulation ---
    balance = initial_balance
    peak = initial_balance
    max_dd_pct = 0.0
    max_dd_usd = 0.0
    equity_curve = []
    yearly_pnl = defaultdict(lambda: {"trades": 0, "wins": 0, "pnl_usd": 0.0, "pnl_r": 0.0})

    for t in deduped:
        risk_amount = initial_balance * t["risk_pct"]  # FIXED on initial balance
        dollar_pnl = t["pnl_r"] * risk_amount
        balance += dollar_pnl

        peak = max(peak, balance)
        dd_usd = balance - peak
        dd_pct = dd_usd / peak if peak > 0 else 0
        max_dd_pct = min(max_dd_pct, dd_pct)
        max_dd_usd = min(max_dd_usd, dd_usd)

        year = t["date"][:4]
        yearly_pnl[year]["trades"] += 1
        yearly_pnl[year]["pnl_usd"] += dollar_pnl
        yearly_pnl[year]["pnl_r"] += t["pnl_r"]
        if t["pnl_r"] > 0:
            yearly_pnl[year]["wins"] += 1

        equity_curve.append({
            "date": t["date"],
            "balance": balance,
            "pnl_usd": dollar_pnl,
            "pnl_r": t["pnl_r"],
            "dd_pct": dd_pct,
            "symbol": t["symbol"],
        })

    total_trades = len(deduped)
    total_wins = sum(1 for t in deduped if t["pnl_r"] > 0)
    total_losses = total_trades - total_wins
    wr = total_wins / total_trades if total_trades > 0 else 0
    pnls_r = [t["pnl_r"] for t in deduped]
    gross_p = sum(p for p in pnls_r if p > 0)
    gross_l = abs(sum(p for p in pnls_r if p < 0))
    pf = gross_p / gross_l if gross_l > 0 else 99.9
    net_r = sum(pnls_r)
    total_pnl_usd = balance - initial_balance
    avg_risk_usd = np.mean([initial_balance * t["risk_pct"] for t in deduped])

    # Per-symbol stats
    sym_stats = defaultdict(lambda: {"trades": 0, "wins": 0, "pnl_r": 0.0, "pnl_usd": 0.0})
    for t in deduped:
        risk_amount = initial_balance * t["risk_pct"]
        sym_stats[t["symbol"]]["trades"] += 1
        sym_stats[t["symbol"]]["pnl_r"] += t["pnl_r"]
        sym_stats[t["symbol"]]["pnl_usd"] += t["pnl_r"] * risk_amount
        if t["pnl_r"] > 0:
            sym_stats[t["symbol"]]["wins"] += 1

    # Trading days
    unique_days = len(set(t["date"] for t in deduped))
    first_date = deduped[0]["date"] if deduped else "?"
    last_date = deduped[-1]["date"] if deduped else "?"

    # --- Generate Report ---
    report_path = os.path.join(reports_dir, "Portfolio_121_Fixed_20k_Backtest.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Portfolio Backtest: 121 Estrategias — $20,000 Balance Fijo\n\n")
        f.write(f"> Sin interés compuesto | Riesgo dinámico 1-6% sobre balance FIJO\n")
        f.write(f"> Período: {first_date} → {last_date}\n")
        f.write(f"> Deduplicación: 1 trade/día/símbolo (sesión más temprana gana)\n\n")

        f.write("## Resultado Principal\n")
        f.write("| | |\n|:---|:---|\n")
        f.write(f"| **Balance Inicial** | `${initial_balance:,.0f}` |\n")
        f.write(f"| **Balance Final** | `${balance:,.2f}` |\n")
        f.write(f"| **Ganancia Neta** | `${total_pnl_usd:,.2f}` ({total_pnl_usd/initial_balance:.1%}) |\n")
        f.write(f"| **Retorno Anualizado** | `${total_pnl_usd / max(1, len(yearly_pnl)):,.2f}/año` |\n")
        f.write(f"| **Pico Máximo** | `${peak:,.2f}` |\n")
        f.write(f"| **Max Drawdown %** | `{max_dd_pct:.1%}` |\n")
        f.write(f"| **Max Drawdown $** | `${abs(max_dd_usd):,.2f}` |\n\n")

        f.write("## Dashboard\n")
        f.write("| Métrica | Valor |\n|:---|:---|\n")
        f.write(f"| **Total Trades** | `{total_trades:,}` |\n")
        f.write(f"| **Wins / Losses** | `{total_wins:,} / {total_losses:,}` |\n")
        f.write(f"| **Win Rate** | `{wr:.1%}` |\n")
        f.write(f"| **Profit Factor** | `{pf:.2f}` |\n")
        f.write(f"| **Expectativa** | `{np.mean(pnls_r):.3f} R` |\n")
        f.write(f"| **Net R** | `{net_r:.1f} R` |\n")
        f.write(f"| **Riesgo Promedio/Trade** | `${avg_risk_usd:,.0f}` |\n")
        f.write(f"| **Días de Trading** | `{unique_days:,}` |\n")
        f.write(f"| **Trades/Día** | `{total_trades / max(1, unique_days):.1f}` |\n\n")

        # Yearly breakdown
        f.write("## Rendimiento por Año\n")
        f.write("| Año | Trades | Wins | WR | PnL ($) | PnL (R) | Retorno |\n")
        f.write("|:---|:---|:---|:---|:---|:---|:---|\n")
        for year in sorted(yearly_pnl.keys()):
            y = yearly_pnl[year]
            y_wr = y["wins"] / y["trades"] if y["trades"] > 0 else 0
            y_ret = y["pnl_usd"] / initial_balance
            f.write(f"| **{year}** | {y['trades']} | {y['wins']} | `{y_wr:.1%}` | "
                    f"`${y['pnl_usd']:,.0f}` | `{y['pnl_r']:.1f}` | `{y_ret:.1%}` |\n")
        f.write("\n")

        # Per-symbol
        f.write("## Rendimiento por Símbolo\n")
        f.write("| Símbolo | Trades | Wins | WR | PnL ($) | PnL (R) |\n")
        f.write("|:---|:---|:---|:---|:---|:---|\n")
        for sym in sorted(sym_stats.keys(), key=lambda s: sym_stats[s]["pnl_usd"], reverse=True):
            s = sym_stats[sym]
            s_wr = s["wins"] / s["trades"] if s["trades"] > 0 else 0
            f.write(f"| **{sym}** | {s['trades']} | {s['wins']} | `{s_wr:.1%}` | "
                    f"`${s['pnl_usd']:,.0f}` | `{s['pnl_r']:.1f}` |\n")
        f.write("\n")

        # Top/Bottom strategies
        sorted_strats = sorted(strat_stats.items(), key=lambda x: x[1]["net_r"], reverse=True)
        f.write("## Top 15 Estrategias (por Net R)\n")
        f.write("| Estrategia | Trades | WR | Net R | Risk% |\n")
        f.write("|:---|:---|:---|:---|:---|\n")
        for label, s in sorted_strats[:15]:
            f.write(f"| {label} | {s['trades']} | `{s['wr']:.1%}` | `{s['net_r']:.1f}` | `{s['risk_pct']:.1%}` |\n")
        f.write("\n")

        f.write("## Bottom 10 Estrategias (por Net R)\n")
        f.write("| Estrategia | Trades | WR | Net R | Risk% |\n")
        f.write("|:---|:---|:---|:---|:---|\n")
        for label, s in sorted_strats[-10:]:
            f.write(f"| {label} | {s['trades']} | `{s['wr']:.1%}` | `{s['net_r']:.1f}` | `{s['risk_pct']:.1%}` |\n")
        f.write("\n")

        # Equity curve (sampled)
        f.write("## Curva de Equity\n```text\n")
        if equity_curve:
            max_bal = max(e["balance"] for e in equity_curve)
            min_bal = min(e["balance"] for e in equity_curve)
            steps = 60
            chunk = max(1, len(equity_curve) // steps)
            for i in range(0, len(equity_curve), chunk):
                e = equity_curve[i]
                bar_len = int((e["balance"] - min_bal) / max(max_bal - min_bal, 1) * 60)
                bar = "#" * max(bar_len, 0)
                f.write(f"{e['date']} | ${e['balance']:>12,.2f} | {bar}\n")
            e = equity_curve[-1]
            bar_len = int((e["balance"] - min_bal) / max(max_bal - min_bal, 1) * 60)
            f.write(f"{e['date']} | ${e['balance']:>12,.2f} | {'#' * max(bar_len, 0)}\n")
        f.write("```\n\n")

        # Drawdown curve
        f.write("## Curva de Drawdown\n```text\n")
        if equity_curve:
            steps = 40
            chunk = max(1, len(equity_curve) // steps)
            for i in range(0, len(equity_curve), chunk):
                e = equity_curve[i]
                dd = e["dd_pct"]
                bar = "-" * int(abs(dd) * 200) if dd < 0 else ""
                f.write(f"{e['date']} | {dd:>7.1%} | {bar}\n")
        f.write("```\n\n")

        # Architecture
        f.write("---\n### Arquitectura\n")
        f.write(f"- **Balance fijo:** ${initial_balance:,.0f} (riesgo siempre sobre capital inicial)\n")
        f.write(f"- **Riesgo dinámico:** 1-6% según WR de cada estrategia\n")
        f.write(f"- **Fricción:** -{FRICTION_FX}R (forex), -{FRICTION_INDEX}R (índices/commodities)\n")
        f.write(f"- **Filtro ATR:** {ATR_RATIO_LOW}-{ATR_RATIO_HIGH}\n")
        f.write(f"- **Dedup:** 1 trade/día/símbolo\n")
        f.write(f"- **Edges:** Solo FADE (FADE_UP + FADE_DOWN)\n")
        f.write(f"- **TP 1.5R (tracker), FADE gana cuando SL toca primero = +1R neto**\n")

    print(f"\n{'='*60}")
    print(f"  BACKTEST COMPLETO")
    print(f"  Balance: ${initial_balance:,.0f} -> ${balance:,.2f}")
    print(f"  Ganancia: ${total_pnl_usd:,.2f} ({total_pnl_usd/initial_balance:.1%})")
    print(f"  Trades: {total_trades:,} | WR: {wr:.1%} | PF: {pf:.2f}")
    print(f"  Max DD: {max_dd_pct:.1%} (${abs(max_dd_usd):,.0f})")
    print(f"  Reporte: {report_path}")
    print(f"{'='*60}")

    return balance


if __name__ == "__main__":
    balance_arg = float(sys.argv[1]) if len(sys.argv) > 1 else 20000.0
    run_portfolio_backtest(balance_arg)
