"""
Portfolio Backtest con R:R optimizado por estrategia.
Usa tp_mult y sl_mult de bot_config.json para cada estrategia.
Balance fijo $20k, riesgo dinamico 1-6%, dedup 1 trade/dia/simbolo.
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
from src.engine.statistical_validator import StatisticalValidator
from src.domain.constants import (
    MT5_TO_INTERNAL, INDEX_SYMBOLS, FRICTION_FX, FRICTION_INDEX,
    ATR_RATIO_LOW, ATR_RATIO_HIGH,
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


def run_portfolio_backtest_rr(initial_balance=20000.0):
    ROOT = "c:/Proyectos/kha0sys3"
    data_dir = os.path.join(ROOT, "data")
    config_path = os.path.join(ROOT, "src", "infrastructure", "config", "asset_config.json")
    bot_config_path = os.path.join(ROOT, "src", "execution", "bot_config.json")
    reports_dir = os.path.join(ROOT, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    loader = CSVPolarsLoader(data_dir)
    with open(config_path) as f:
        asset_config = json.load(f)
    with open(bot_config_path) as f:
        bot_config = json.load(f)

    portfolio = bot_config["portfolio"]
    risk_cfg = bot_config["risk_scaling"]
    allocator = DynamicRiskAllocator(**risk_cfg)

    print(f"Portfolio: {len(portfolio)} estrategias con R:R individual")
    print(f"Balance fijo: ${initial_balance:,.0f}")

    # Group by (symbol, magic_time, duration)
    combo_strategies = defaultdict(list)
    for strat in portfolio:
        sym = MT5_TO_INTERNAL.get(strat["sym"], strat["sym"])
        key = (sym, strat["magic_time"], strat["duration"])
        combo_strategies[key].append(strat)

    print(f"Combos unicos: {len(combo_strategies)}")

    # Build enriched post-OR data per combo
    combo_cache = {}
    for (sym, time_start, duration) in combo_strategies:
        cfg = asset_config.get(sym)
        if not cfg:
            continue
        try:
            df_raw = loader.load_data(sym, "M15")
            df_raw = DataEnricher.enrich_with_rsi(df_raw)
            df_enriched = DataEnricher.enrich_with_daily_context(
                df_raw, cfg["pd_start"], cfg["pd_end"])
            df_or = DataEnricher.enrich_with_opening_range(
                df_enriched, time_start, duration)

            post_or = df_or.filter(
                (pl.col("is_post_or") == True) & (pl.col("is_active_session") == True))

            # ATR filter
            daily_atr = df_or.group_by("trade_date").agg(
                pl.col("or_atr_ratio").first())
            valid_days = daily_atr.filter(
                pl.col("or_atr_ratio").is_between(ATR_RATIO_LOW, ATR_RATIO_HIGH)
            ).select("trade_date")
            post_or = post_or.join(valid_days, on="trade_date", how="inner")

            # Context columns
            ctx_cols = []
            for c in ["rsi_at_or_close", "rsi_daily_14", "atr_change",
                       "atr_percentile", "or_position_vs_pd", "or_open_vs_pd_close",
                       "or_open", "pd_or_high", "pd_or_low"]:
                if c in df_or.columns:
                    ctx_cols.append(pl.col(c).first().alias(c))

            daily_ctx = None
            if ctx_cols:
                daily_ctx = df_or.group_by("trade_date").agg(ctx_cols)
                daily_ctx = daily_ctx.with_columns(
                    pl.col("trade_date").cast(pl.Date).dt.weekday().alias("day_of_week"))
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
        except Exception as e:
            print(f"  ERROR {sym} {time_start} {duration}m: {e}")

    # Compute trades per strategy using its individual TP/SL
    all_trades = []
    strat_stats = {}

    for strat in portfolio:
        sym = MT5_TO_INTERNAL.get(strat["sym"], strat["sym"])
        edge = strat["edge"]
        direction = edge.split("_")[-1]
        time_start = strat["magic_time"]
        duration = strat["duration"]
        ctx_label = strat.get("context")
        ctx_filter = resolve_context_filter(ctx_label)
        win_rate_cfg = strat["win_rate"]
        risk_pct = allocator.get_risk_percent(win_rate_cfg)
        friction = FRICTION_INDEX if sym in INDEX_SYMBOLS else FRICTION_FX
        tp_mult = strat.get("tp_mult", 1.0)
        sl_mult = strat.get("sl_mult", 1.5)

        cached = combo_cache.get((sym, time_start, duration))
        if cached is None:
            continue
        post_or, daily_ctx = cached

        # First break direction per day
        brk_up = post_or.filter(pl.col("high") >= pl.col("or_high")).group_by(
            "trade_date").agg(pl.col("mins_from_midnight").min().alias("t_brk_up"))
        brk_dn = post_or.filter(pl.col("low") <= pl.col("or_low")).group_by(
            "trade_date").agg(pl.col("mins_from_midnight").min().alias("t_brk_dn"))

        # TP/SL hit times for this strategy's specific multipliers
        if direction == "UP":
            tp_level_df = post_or.filter(
                pl.col("low") <= (pl.col("or_high") - pl.col("or_width") * tp_mult)
            ).group_by("trade_date").agg(
                pl.col("mins_from_midnight").min().alias("t_tp"))
            sl_level_df = post_or.filter(
                pl.col("high") >= (pl.col("or_high") + pl.col("or_width") * sl_mult)
            ).group_by("trade_date").agg(
                pl.col("mins_from_midnight").min().alias("t_sl"))
        else:
            tp_level_df = post_or.filter(
                pl.col("high") >= (pl.col("or_low") + pl.col("or_width") * tp_mult)
            ).group_by("trade_date").agg(
                pl.col("mins_from_midnight").min().alias("t_tp"))
            sl_level_df = post_or.filter(
                pl.col("low") <= (pl.col("or_low") - pl.col("or_width") * sl_mult)
            ).group_by("trade_date").agg(
                pl.col("mins_from_midnight").min().alias("t_sl"))

        # Build daily result
        base = post_or.select("trade_date").unique()
        result = base.join(brk_up, on="trade_date", how="left")
        result = result.join(brk_dn, on="trade_date", how="left")
        result = result.join(tp_level_df, on="trade_date", how="left")
        result = result.join(sl_level_df, on="trade_date", how="left")

        # first_break_dir
        result = result.with_columns(
            pl.when(pl.col("t_brk_up").is_not_null() & pl.col("t_brk_dn").is_null())
            .then(pl.lit("UP"))
            .when(pl.col("t_brk_dn").is_not_null() & pl.col("t_brk_up").is_null())
            .then(pl.lit("DOWN"))
            .when(pl.col("t_brk_up") < pl.col("t_brk_dn")).then(pl.lit("UP"))
            .when(pl.col("t_brk_dn") < pl.col("t_brk_up")).then(pl.lit("DOWN"))
            .otherwise(pl.lit("NONE"))
            .alias("first_break_dir")
        )

        # Apply context filter
        if daily_ctx is not None:
            ccols = [c for c in daily_ctx.columns if c != "trade_date"]
            result = result.join(
                daily_ctx.select(["trade_date"] + ccols), on="trade_date", how="left")
        if ctx_filter:
            result = StrategyScanner.apply_context_filter(result, ctx_filter)

        # Filter by direction
        if direction == "UP":
            trades = result.filter(pl.col("first_break_dir") == "UP")
        else:
            trades = result.filter(pl.col("first_break_dir") == "DOWN")

        # PnL: TP hit first = win (+tp_mult), SL hit first = loss (-sl_mult)
        trades = trades.with_columns(
            pl.when(
                pl.col("t_tp").is_not_null()
                & (pl.col("t_sl").is_null() | (pl.col("t_tp") < pl.col("t_sl")))
            ).then(pl.lit(tp_mult) - friction)
            .when(
                pl.col("t_sl").is_not_null()
                & (pl.col("t_tp").is_null() | (pl.col("t_sl") <= pl.col("t_tp")))
            ).then(pl.lit(-sl_mult) - friction)
            .otherwise(0.0)
            .alias("pnl_r")
        )

        trades = trades.filter(pl.col("pnl_r") != 0.0)
        if trades.height == 0:
            continue

        # Exec time for dedup priority
        h, m = map(int, time_start.split(":"))
        exec_mins = h * 60 + m + duration

        strat_label = f"{sym}|{strat['session']}|{edge}|{duration}m|{ctx_label or 'BASE'}"
        wins = trades.filter(pl.col("pnl_r") > 0).height
        total = trades.height
        actual_wr = wins / total if total > 0 else 0
        net_r = trades.select(pl.col("pnl_r").sum()).item()

        strat_stats[strat_label] = {
            "trades": total, "wins": wins, "losses": total - wins,
            "wr": actual_wr, "risk_pct": risk_pct, "net_r": net_r,
            "tp_mult": tp_mult, "sl_mult": sl_mult,
        }

        for row in trades.select(["trade_date", "pnl_r"]).iter_rows(named=True):
            all_trades.append({
                "date": str(row["trade_date"]),
                "symbol": sym,
                "edge": edge,
                "session": strat["session"],
                "duration": duration,
                "context": ctx_label or "BASE",
                "pnl_r": row["pnl_r"],
                "risk_pct": risk_pct,
                "exec_mins": exec_mins,
                "strat_label": strat_label,
            })

    print(f"\nTotal trades brutos: {len(all_trades)}")

    # Dedup: 1 trade per day per symbol (earliest session wins)
    all_trades.sort(key=lambda x: (x["date"], x["exec_mins"]))
    seen = set()
    deduped = []
    for t in all_trades:
        key = (t["date"], t["symbol"])
        if key not in seen:
            seen.add(key)
            deduped.append(t)

    print(f"Total trades deduplicados: {len(deduped)}")

    # Fixed balance simulation
    balance = initial_balance
    peak = initial_balance
    max_dd_pct = 0.0
    max_dd_usd = 0.0
    equity_curve = []
    yearly_pnl = defaultdict(lambda: {
        "trades": 0, "wins": 0, "pnl_usd": 0.0, "pnl_r": 0.0})

    for t in deduped:
        risk_amount = initial_balance * t["risk_pct"]
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
            "date": t["date"], "balance": balance, "pnl_usd": dollar_pnl,
            "pnl_r": t["pnl_r"], "dd_pct": dd_pct, "symbol": t["symbol"],
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
    sym_stats = defaultdict(lambda: {
        "trades": 0, "wins": 0, "pnl_r": 0.0, "pnl_usd": 0.0})
    for t in deduped:
        risk_amount = initial_balance * t["risk_pct"]
        sym_stats[t["symbol"]]["trades"] += 1
        sym_stats[t["symbol"]]["pnl_r"] += t["pnl_r"]
        sym_stats[t["symbol"]]["pnl_usd"] += t["pnl_r"] * risk_amount
        if t["pnl_r"] > 0:
            sym_stats[t["symbol"]]["wins"] += 1

    unique_days = len(set(t["date"] for t in deduped))
    first_date = deduped[0]["date"] if deduped else "?"
    last_date = deduped[-1]["date"] if deduped else "?"

    # Monte Carlo
    mc = StatisticalValidator.monte_carlo(pnls_r, n_sims=10000)

    # Walk-Forward
    mid = len(pnls_r) // 2
    tr_p, te_p = pnls_r[:mid], pnls_r[mid:]
    wr_tr = sum(1 for p in tr_p if p > 0) / len(tr_p) if tr_p else 0
    wr_te = sum(1 for p in te_p if p > 0) / len(te_p) if te_p else 0

    # Decay
    dates_list = [t["date"] for t in deduped]
    decay = StatisticalValidator.decay_analysis(pnls_r, dates_list, window_days=365)

    # === Report ===
    report_path = os.path.join(
        reports_dir, "Portfolio_108_RR_Optimized_Backtest.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Portfolio Backtest: 108 Estrategias con R:R Optimizado\n\n")
        f.write(f"> Balance fijo ${initial_balance:,.0f} | Riesgo 1-6% dinamico\n")
        f.write(f"> R:R individual por estrategia (tp_mult/sl_mult de bot_config)\n")
        f.write(f"> Periodo: {first_date} -> {last_date}\n")
        f.write(f"> Dedup: 1 trade/dia/simbolo\n\n")

        f.write("## Resultado Principal\n")
        f.write("| | |\n|:---|:---|\n")
        f.write(f"| **Balance Inicial** | `${initial_balance:,.0f}` |\n")
        f.write(f"| **Balance Final** | `${balance:,.2f}` |\n")
        f.write(f"| **Ganancia Neta** | `${total_pnl_usd:,.2f}` "
                f"({total_pnl_usd/initial_balance:.0%}) |\n")
        f.write(f"| **Retorno Anualizado** | "
                f"`${total_pnl_usd / max(1, len(yearly_pnl)):,.0f}/ano` |\n")
        f.write(f"| **Pico Maximo** | `${peak:,.2f}` |\n")
        f.write(f"| **Max Drawdown %** | `{max_dd_pct:.1%}` |\n")
        f.write(f"| **Max Drawdown $** | `${abs(max_dd_usd):,.0f}` |\n\n")

        f.write("## Dashboard\n")
        f.write("| Metrica | Valor |\n|:---|:---|\n")
        f.write(f"| **Total Trades** | `{total_trades:,}` |\n")
        f.write(f"| **Wins / Losses** | `{total_wins:,} / {total_losses:,}` |\n")
        f.write(f"| **Win Rate** | `{wr:.1%}` |\n")
        f.write(f"| **Profit Factor** | `{pf:.2f}` |\n")
        f.write(f"| **Expectativa** | `{np.mean(pnls_r):.4f} R` |\n")
        f.write(f"| **Net R** | `{net_r:.1f} R` |\n")
        f.write(f"| **Riesgo Promedio/Trade** | `${avg_risk_usd:,.0f}` |\n")
        f.write(f"| **Dias de Trading** | `{unique_days:,}` |\n")
        f.write(f"| **Trades/Dia** | "
                f"`{total_trades / max(1, unique_days):.1f}` |\n\n")

        # Monte Carlo
        f.write("## Monte Carlo (10,000 simulaciones)\n")
        f.write("| Percentil | Net R | PnL ($) |\n|:---|:---|:---|\n")
        for lbl, key in [("P5", "pnl_p5"), ("P25", "pnl_p25"),
                          ("P50", "pnl_p50"), ("P75", "pnl_p75"),
                          ("P95", "pnl_p95")]:
            val = mc[key]
            f.write(f"| **{lbl}** | `{val:.0f}R` | "
                    f"`${val * avg_risk_usd:,.0f}` |\n")
        f.write(f"| **Prob Ruina** | `{mc['prob_ruin']:.1%}` | |\n")
        f.write(f"| **Prob Profit** | `{mc['prob_profit']:.1%}` | |\n")
        f.write(f"| **DD P5** | `{mc['dd_p5']:.0f}R` | |\n")
        f.write(f"| **DD P50** | `{mc['dd_p50']:.0f}R` | |\n\n")

        # Walk-Forward
        f.write("## Walk-Forward (50/50)\n")
        f.write("| | IS (primera mitad) | OOS (segunda mitad) |\n")
        f.write("|:---|:---|:---|\n")
        f.write(f"| **WR** | `{wr_tr:.1%}` | `{wr_te:.1%}` |\n")
        f.write(f"| **Net R** | `{sum(tr_p):.0f}` | `{sum(te_p):.0f}` |\n")
        f.write(f"| **Degradacion** | | `{max(0, wr_tr - wr_te):.1%}` |\n\n")

        # Decay
        f.write("## Decay Analysis\n")
        f.write(f"**Score: `{decay.get('decay_score', 0):.2f}`** -- "
                f"**Tendencia: `{decay.get('trend', '?')}`**\n\n")
        if decay.get("windows"):
            f.write("| Periodo | Trades | WR | Expectativa | PnL (R) |\n")
            f.write("|:---|:---|:---|:---|:---|\n")
            for w in decay["windows"]:
                f.write(f"| {w['period']} | {w['trades']} | `{w['wr']:.1%}` | "
                        f"`{w['expectancy']:.4f}R` | `{w['pnl']:.1f}R` |\n")
            f.write("\n")

        # Yearly breakdown
        f.write("## Rendimiento por Ano\n")
        f.write("| Ano | Trades | Wins | WR | PnL ($) | PnL (R) | Retorno |\n")
        f.write("|:---|:---|:---|:---|:---|:---|:---|\n")
        for year in sorted(yearly_pnl.keys()):
            y = yearly_pnl[year]
            y_wr = y["wins"] / y["trades"] if y["trades"] > 0 else 0
            y_ret = y["pnl_usd"] / initial_balance
            f.write(f"| **{year}** | {y['trades']} | {y['wins']} | "
                    f"`{y_wr:.1%}` | `${y['pnl_usd']:,.0f}` | "
                    f"`{y['pnl_r']:.1f}` | `{y_ret:.1%}` |\n")
        f.write("\n")

        # Per-symbol
        f.write("## Rendimiento por Simbolo\n")
        f.write("| Simbolo | Trades | Wins | WR | PnL ($) | PnL (R) |\n")
        f.write("|:---|:---|:---|:---|:---|:---|\n")
        for sym in sorted(sym_stats.keys(),
                          key=lambda s: sym_stats[s]["pnl_usd"], reverse=True):
            s = sym_stats[sym]
            s_wr = s["wins"] / s["trades"] if s["trades"] > 0 else 0
            f.write(f"| **{sym}** | {s['trades']} | {s['wins']} | "
                    f"`{s_wr:.1%}` | `${s['pnl_usd']:,.0f}` | "
                    f"`{s['pnl_r']:.1f}` |\n")
        f.write("\n")

        # Top/Bottom strategies
        sorted_strats = sorted(
            strat_stats.items(), key=lambda x: x[1]["net_r"], reverse=True)
        f.write("## Top 15 Estrategias\n")
        f.write("| Estrategia | TP:SL | Trades | WR | Net R | Risk% |\n")
        f.write("|:---|:---|:---|:---|:---|:---|\n")
        for label, s in sorted_strats[:15]:
            f.write(f"| {label} | {s['tp_mult']}:{s['sl_mult']} | "
                    f"{s['trades']} | `{s['wr']:.1%}` | `{s['net_r']:.1f}` | "
                    f"`{s['risk_pct']:.1%}` |\n")
        f.write("\n")

        f.write("## Bottom 10 Estrategias\n")
        f.write("| Estrategia | TP:SL | Trades | WR | Net R | Risk% |\n")
        f.write("|:---|:---|:---|:---|:---|:---|\n")
        for label, s in sorted_strats[-10:]:
            f.write(f"| {label} | {s['tp_mult']}:{s['sl_mult']} | "
                    f"{s['trades']} | `{s['wr']:.1%}` | `{s['net_r']:.1f}` | "
                    f"`{s['risk_pct']:.1%}` |\n")
        f.write("\n")

        # Equity curve
        f.write("## Curva de Equity\n```text\n")
        if equity_curve:
            max_bal = max(e["balance"] for e in equity_curve)
            min_bal = min(e["balance"] for e in equity_curve)
            steps = 60
            chunk = max(1, len(equity_curve) // steps)
            for i in range(0, len(equity_curve), chunk):
                e = equity_curve[i]
                bar_len = int(
                    (e["balance"] - min_bal) / max(max_bal - min_bal, 1) * 60)
                f.write(f"{e['date']} | ${e['balance']:>12,.2f} | "
                        f"{'#' * max(bar_len, 0)}\n")
            e = equity_curve[-1]
            bar_len = int(
                (e["balance"] - min_bal) / max(max_bal - min_bal, 1) * 60)
            f.write(f"{e['date']} | ${e['balance']:>12,.2f} | "
                    f"{'#' * max(bar_len, 0)}\n")
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

        f.write("---\n### Arquitectura\n")
        f.write(f"- **Balance fijo:** ${initial_balance:,.0f}\n")
        f.write(f"- **Riesgo dinamico:** 1-6% segun WR\n")
        f.write(f"- **Friccion:** -{FRICTION_FX}R (forex), "
                f"-{FRICTION_INDEX}R (indices/commodities)\n")
        f.write(f"- **Filtro ATR:** {ATR_RATIO_LOW}-{ATR_RATIO_HIGH}\n")
        f.write(f"- **Dedup:** 1 trade/dia/simbolo\n")
        f.write(f"- **R:R:** Individual por estrategia "
                f"(tp_mult/sl_mult en bot_config.json)\n")
        f.write(f"- **FADE gana tp_mult R, pierde sl_mult R "
                f"(neto de friccion)**\n")

    # Console
    print(f"\n{'='*60}")
    print(f"  BACKTEST COMPLETO — R:R OPTIMIZADO")
    print(f"  Balance: ${initial_balance:,.0f} -> ${balance:,.2f}")
    print(f"  Ganancia: ${total_pnl_usd:,.2f} ({total_pnl_usd/initial_balance:.0%})")
    print(f"  Trades: {total_trades:,} | WR: {wr:.1%} | PF: {pf:.2f}")
    print(f"  Net R: {net_r:.1f}")
    print(f"  Max DD: {max_dd_pct:.1%} (${abs(max_dd_usd):,.0f})")
    print(f"  MC: P5={mc['pnl_p5']:.0f}R P50={mc['pnl_p50']:.0f}R "
          f"Ruina={mc['prob_ruin']:.1%}")
    print(f"  WF: IS={wr_tr:.1%} OOS={wr_te:.1%} Deg={max(0, wr_tr-wr_te):.1%}")
    print(f"  Decay: {decay.get('decay_score', 0):.2f} ({decay.get('trend', '?')})")
    print(f"  Reporte: {report_path}")
    print(f"{'='*60}")

    return balance


if __name__ == "__main__":
    balance_arg = float(sys.argv[1]) if len(sys.argv) > 1 else 20000.0
    run_portfolio_backtest_rr(balance_arg)
