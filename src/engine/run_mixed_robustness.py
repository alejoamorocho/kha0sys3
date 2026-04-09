"""
Robustness Validation for MIXED Portfolio (101 FADE + 7 MOMENTUM).
- Walk-Forward Rolling: 3 folds (60% train / 40% test), rolling windows
- Monte Carlo: 10k permutaciones a nivel portfolio (deduplicado)
- Decay Analysis: ventanas anuales sobre equity curve del portfolio
- Per-strategy breakdown: WR IS/OOS + degradación para cada estrategia individual
"""

import json
import os
import sys
import numpy as np
import polars as pl
from collections import defaultdict
from datetime import date

from src.infrastructure.data.polars_loader import CSVPolarsLoader
from src.application.calculators import DataEnricher
from src.application.trackers import TrackerEngine
from src.engine.strategy_scanner import StrategyScanner
from src.engine.statistical_validator import StatisticalValidator
from src.domain.constants import (
    MT5_TO_INTERNAL, INDEX_SYMBOLS, FRICTION_FX, FRICTION_INDEX,
    ATR_RATIO_LOW, ATR_RATIO_HIGH, DEFAULT_TP_MULTIPLIER,
)
from src.execution.risk_manager import DynamicRiskAllocator


# === 7 strategies that perform better as MOMENTUM (from comparison backtest) ===
MOMENTUM_OVERRIDES = {
    "GBPUSD|London|FADE_DOWN|60m|BASE",
    "GBPJPY|London|FADE_DOWN|45m|BASE",
    "XAGUSD|London|FADE_DOWN|60m|BASE",
    "XAGUSD|London|FADE_DOWN|15m|BASE",
    "XAGUSD|London|FADE_DOWN|15m|GapSmall",
    "BRENT|London|FADE_DOWN|30m|BASE",
    "XAGUSD|London|FADE_DOWN|30m|BASE",
}


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


def run_mixed_robustness(initial_balance=20000.0):
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

    print(f"=== MIXED Portfolio Robustness: {len(portfolio)} estrategias ===")
    print(f"  101 FADE (LIMIT) + 7 MOMENTUM (STOP)")

    # Group by combo
    combo_strategies = defaultdict(list)
    for strat in portfolio:
        sym = MT5_TO_INTERNAL.get(strat["sym"], strat["sym"])
        key = (sym, strat["magic_time"], strat["duration"])
        combo_strategies[key].append(strat)

    # Build expanded stats cache
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
            stats_df = TrackerEngine.track_events(df_or, tp_multiplier=DEFAULT_TP_MULTIPLIER)

            agg_cols = [pl.col("or_open").first(), pl.col("pd_or_high").first(), pl.col("pd_or_low").first()]
            for c in ["rsi_at_or_close", "rsi_daily_14", "atr_change",
                       "atr_percentile", "or_position_vs_pd", "or_open_vs_pd_close"]:
                if c in df_or.columns:
                    agg_cols.append(pl.col(c).first())

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

            combo_cache[(sym, time_start, duration)] = valid
        except Exception as e:
            print(f"  ERROR loading {sym} {time_start} {duration}m: {e}")

    # =========================================================================
    # STEP 1: Collect ALL trades per strategy with dates (for WF and portfolio)
    # =========================================================================
    all_strat_trades = []  # list of dicts with all trade info
    strat_results = []     # per-strategy analysis

    for strat in portfolio:
        sym = MT5_TO_INTERNAL.get(strat["sym"], strat["sym"])
        key = (sym, strat["magic_time"], strat["duration"])
        valid = combo_cache.get(key)
        if valid is None or valid.height == 0:
            continue

        edge = strat["edge"]
        direction = edge.split("_")[-1]
        ctx_label = strat.get("context")
        ctx_filter = resolve_context_filter(ctx_label)
        friction = FRICTION_INDEX if sym in INDEX_SYMBOLS else FRICTION_FX
        win_rate_cfg = strat["win_rate"]
        risk_pct = allocator.get_risk_percent(win_rate_cfg)
        label = f"{sym}|{strat['session']}|{edge}|{strat['duration']}m|{ctx_label or 'BASE'}"

        h, m_ = map(int, strat["magic_time"].split(':'))
        exec_mins = h * 60 + m_ + strat["duration"]

        filtered = valid
        if ctx_filter:
            filtered = StrategyScanner.apply_context_filter(filtered, ctx_filter)

        # Determine order type: MOMENTUM for overrides, FADE for the rest
        is_momentum = label in MOMENTUM_OVERRIDES
        order_type = "STOP" if is_momentum else "LIMIT"

        if is_momentum:
            trades_df = compute_trades_momentum(filtered, direction, friction, DEFAULT_TP_MULTIPLIER)
            effective_edge = f"MOMENTUM_{direction}"
        else:
            trades_df = compute_trades_fade(filtered, direction, friction)
            effective_edge = edge

        if trades_df.height < 10:
            continue

        trades_sorted = trades_df.sort("trade_date")
        pnls = trades_sorted["pnl_r"].to_list()
        dates_list = [str(d) for d in trades_sorted["trade_date"].to_list()]

        # Store for portfolio aggregation
        for row in trades_sorted.select(["trade_date", "pnl_r"]).iter_rows(named=True):
            all_strat_trades.append({
                "date": str(row["trade_date"]),
                "symbol": sym,
                "edge": effective_edge,
                "session": strat["session"],
                "duration": strat["duration"],
                "pnl_r": row["pnl_r"],
                "risk_pct": risk_pct,
                "exec_mins": exec_mins,
                "strat_label": label,
                "order_type": order_type,
            })

        # Per-strategy analysis
        total = len(pnls)
        wins = sum(1 for p in pnls if p > 0)
        wr_full = wins / total
        net_r = sum(pnls)

        # Walk-Forward 3-fold rolling (60/40)
        fold_size = total // 5
        wf_folds = []
        for fold_start in range(0, total - fold_size * 2, fold_size):
            train_end = fold_start + int(total * 0.6)
            if train_end >= total:
                break
            train = pnls[fold_start:train_end]
            test = pnls[train_end:min(train_end + int(total * 0.4), total)]
            if len(train) < 10 or len(test) < 10:
                continue
            wr_tr = sum(1 for p in train if p > 0) / len(train)
            wr_te = sum(1 for p in test if p > 0) / len(test)
            wf_folds.append({"wr_train": wr_tr, "wr_test": wr_te, "deg": max(0, wr_tr - wr_te)})

        if wf_folds:
            avg_wr_train = np.mean([f["wr_train"] for f in wf_folds])
            avg_wr_test = np.mean([f["wr_test"] for f in wf_folds])
            avg_deg = np.mean([f["deg"] for f in wf_folds])
        else:
            mid = total // 2
            train_p = pnls[:mid]
            test_p = pnls[mid:]
            avg_wr_train = sum(1 for p in train_p if p > 0) / len(train_p) if train_p else 0
            avg_wr_test = sum(1 for p in test_p if p > 0) / len(test_p) if test_p else 0
            avg_deg = max(0, avg_wr_train - avg_wr_test)

        # Monte Carlo per strategy
        mc = StatisticalValidator.monte_carlo(pnls, n_sims=10000)

        # Decay
        decay = StatisticalValidator.decay_analysis(pnls, dates_list, window_days=365)

        strat_results.append({
            "label": label,
            "order_type": order_type,
            "total": total,
            "wr_full": wr_full,
            "net_r": net_r,
            "wr_train": avg_wr_train,
            "wr_test": avg_wr_test,
            "wf_deg": avg_deg,
            "mc_p5": mc["pnl_p5"],
            "mc_p50": mc["pnl_p50"],
            "mc_p95": mc["pnl_p95"],
            "mc_ruin": mc["prob_ruin"],
            "mc_profit": mc["prob_profit"],
            "decay_score": decay.get("decay_score", 1.0),
            "decay_trend": decay.get("trend", "?"),
        })

        icon = "S" if order_type == "STOP" else "L"
        print(f"  [{icon}] {label}: WR={wr_full:.1%} IS={avg_wr_train:.1%} OOS={avg_wr_test:.1%} "
              f"Deg={avg_deg:.1%} MC_ruin={mc['prob_ruin']:.0%} Decay={decay.get('decay_score', 0):.2f}")

    # =========================================================================
    # STEP 2: Portfolio-level simulation and analysis
    # =========================================================================
    print(f"\n--- Portfolio-level analysis ---")

    # Dedup and sort
    all_strat_trades.sort(key=lambda x: (x["date"], x["exec_mins"]))
    seen = set()
    deduped = []
    for t in all_strat_trades:
        key = (t["date"], t["symbol"])
        if key not in seen:
            seen.add(key)
            deduped.append(t)

    print(f"  Trades brutos: {len(all_strat_trades)}, deduplicados: {len(deduped)}")

    # Equity curve
    balance = initial_balance
    peak = initial_balance
    max_dd_pct = 0.0
    portfolio_pnls = []
    portfolio_dates = []
    yearly = defaultdict(lambda: {"trades": 0, "wins": 0, "pnl_usd": 0.0, "pnl_r": 0.0})

    for t in deduped:
        risk_amount = initial_balance * t["risk_pct"]
        dollar_pnl = t["pnl_r"] * risk_amount
        balance += dollar_pnl
        peak = max(peak, balance)
        dd = (balance - peak) / peak if peak > 0 else 0
        max_dd_pct = min(max_dd_pct, dd)

        portfolio_pnls.append(t["pnl_r"])
        portfolio_dates.append(t["date"])

        yr = t["date"][:4]
        yearly[yr]["trades"] += 1
        yearly[yr]["pnl_usd"] += dollar_pnl
        yearly[yr]["pnl_r"] += t["pnl_r"]
        if t["pnl_r"] > 0:
            yearly[yr]["wins"] += 1

    total_trades = len(deduped)
    total_wins = sum(1 for t in deduped if t["pnl_r"] > 0)
    wr = total_wins / total_trades if total_trades > 0 else 0
    gross_p = sum(p for p in portfolio_pnls if p > 0)
    gross_l = abs(sum(p for p in portfolio_pnls if p < 0))
    pf = gross_p / gross_l if gross_l > 0 else 99.9
    net_r = sum(portfolio_pnls)
    pnl_usd = balance - initial_balance

    print(f"  Balance: ${initial_balance:,.0f} -> ${balance:,.2f}")
    print(f"  PnL: ${pnl_usd:,.2f} | WR: {wr:.1%} | PF: {pf:.2f} | DD: {max_dd_pct:.1%}")

    # =========================================================================
    # STEP 3: Portfolio Monte Carlo (10k sims on deduped trade stream)
    # =========================================================================
    print(f"\n--- Monte Carlo Portfolio (10k sims) ---")
    mc_portfolio = StatisticalValidator.monte_carlo(portfolio_pnls, n_sims=10000)
    print(f"  P5={mc_portfolio['pnl_p5']:.1f}R  P50={mc_portfolio['pnl_p50']:.1f}R  "
          f"P95={mc_portfolio['pnl_p95']:.1f}R")
    print(f"  Prob Ruina={mc_portfolio['prob_ruin']:.1%}  Prob Profit={mc_portfolio['prob_profit']:.1%}")
    print(f"  DD P5={mc_portfolio['dd_p5']:.1f}R  DD P50={mc_portfolio['dd_p50']:.1f}R")

    # Convert to USD for report
    avg_risk_usd = np.mean([initial_balance * t["risk_pct"] for t in deduped])
    mc_usd = {k: v * avg_risk_usd if "pnl" in k or "dd" in k else v
              for k, v in mc_portfolio.items() if isinstance(v, (int, float))}

    # =========================================================================
    # STEP 4: Portfolio Walk-Forward (3 rolling folds)
    # =========================================================================
    print(f"\n--- Walk-Forward Portfolio (3 folds rolling 60/40) ---")
    n = len(portfolio_pnls)
    wf_portfolio_folds = []

    # 3 rolling folds
    fold_offsets = [0, n // 5, 2 * n // 5]
    for offset in fold_offsets:
        train_end = offset + int(n * 0.6)
        if train_end >= n:
            break
        test_end = min(train_end + int(n * 0.4), n)
        train = portfolio_pnls[offset:train_end]
        test = portfolio_pnls[train_end:test_end]
        if len(train) < 50 or len(test) < 50:
            continue

        wr_tr = sum(1 for p in train if p > 0) / len(train)
        wr_te = sum(1 for p in test if p > 0) / len(test)
        net_tr = sum(train)
        net_te = sum(test)
        pf_tr = sum(p for p in train if p > 0) / abs(sum(p for p in train if p < 0)) if any(p < 0 for p in train) else 99
        pf_te = sum(p for p in test if p > 0) / abs(sum(p for p in test if p < 0)) if any(p < 0 for p in test) else 99

        fold_dates_train = (portfolio_dates[offset], portfolio_dates[train_end - 1])
        fold_dates_test = (portfolio_dates[train_end], portfolio_dates[test_end - 1])

        wf_portfolio_folds.append({
            "train_period": f"{fold_dates_train[0]} → {fold_dates_train[1]}",
            "test_period": f"{fold_dates_test[0]} → {fold_dates_test[1]}",
            "train_trades": len(train), "test_trades": len(test),
            "wr_train": wr_tr, "wr_test": wr_te,
            "pf_train": pf_tr, "pf_test": pf_te,
            "net_r_train": net_tr, "net_r_test": net_te,
            "degradation": max(0, wr_tr - wr_te),
        })
        print(f"  Fold: Train {fold_dates_train[0]}->{fold_dates_train[1]} "
              f"(WR={wr_tr:.1%}, PF={pf_tr:.2f}) | "
              f"Test {fold_dates_test[0]}->{fold_dates_test[1]} "
              f"(WR={wr_te:.1%}, PF={pf_te:.2f}) | Deg={max(0, wr_tr - wr_te):.1%}")

    # =========================================================================
    # STEP 5: Portfolio Decay Analysis
    # =========================================================================
    print(f"\n--- Decay Analysis Portfolio ---")
    decay_portfolio = StatisticalValidator.decay_analysis(portfolio_pnls, portfolio_dates, window_days=365)
    print(f"  Score={decay_portfolio.get('decay_score', 0):.2f} Trend={decay_portfolio.get('trend', '?')}")
    if decay_portfolio.get("windows"):
        for w in decay_portfolio["windows"]:
            print(f"    {w['period']}: {w['trades']} trades, WR={w['wr']:.1%}, Exp={w['expectancy']:.3f}R")

    # =========================================================================
    # STEP 6: Generate Report
    # =========================================================================
    report_path = os.path.join(reports_dir, "Mixed_Portfolio_Robustness.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Validación de Robustez — Portfolio MIXTO (101 FADE + 7 MOMENTUM)\n\n")
        f.write(f"> Balance: ${initial_balance:,.0f} | Riesgo dinámico 1-6%\n")
        f.write(f"> 101 FADE (LIMIT) + 7 MOMENTUM (STOP)\n\n")

        # Main results
        f.write("## Resultado del Portfolio\n")
        f.write("| Métrica | Valor |\n|:---|:---|\n")
        f.write(f"| **Balance Final** | `${balance:,.2f}` |\n")
        f.write(f"| **Ganancia** | `${pnl_usd:,.2f}` ({pnl_usd/initial_balance:.0%}) |\n")
        f.write(f"| **Trades** | `{total_trades:,}` |\n")
        f.write(f"| **Win Rate** | `{wr:.1%}` |\n")
        f.write(f"| **Profit Factor** | `{pf:.2f}` |\n")
        f.write(f"| **Net R** | `{net_r:.1f}` |\n")
        f.write(f"| **Max Drawdown** | `{max_dd_pct:.1%}` |\n\n")

        # Yearly
        f.write("## Rendimiento Anual\n")
        f.write("| Año | Trades | Wins | WR | PnL ($) | PnL (R) |\n")
        f.write("|:---|:---|:---|:---|:---|:---|\n")
        for yr in sorted(yearly.keys()):
            y = yearly[yr]
            y_wr = y["wins"] / y["trades"] if y["trades"] > 0 else 0
            f.write(f"| **{yr}** | {y['trades']} | {y['wins']} | `{y_wr:.1%}` | "
                    f"`${y['pnl_usd']:,.0f}` | `{y['pnl_r']:.1f}` |\n")
        f.write("\n")

        # Monte Carlo Portfolio
        f.write("## Monte Carlo — Portfolio (10,000 simulaciones)\n\n")
        f.write("| Percentil | Net R | PnL ($) |\n|:---|:---|:---|\n")
        for pct_label, pct_key in [("P5 (peor)", "pnl_p5"), ("P25", "pnl_p25"),
                                    ("P50 (mediana)", "pnl_p50"), ("P75", "pnl_p75"),
                                    ("P95 (mejor)", "pnl_p95")]:
            val_r = mc_portfolio[pct_key]
            val_usd = val_r * avg_risk_usd
            f.write(f"| **{pct_label}** | `{val_r:.1f}R` | `${val_usd:,.0f}` |\n")
        f.write(f"| **Prob Ruina** | `{mc_portfolio['prob_ruin']:.1%}` | |\n")
        f.write(f"| **Prob Profit** | `{mc_portfolio['prob_profit']:.1%}` | |\n")
        f.write(f"| **DD P5** | `{mc_portfolio['dd_p5']:.1f}R` | |\n")
        f.write(f"| **DD P50** | `{mc_portfolio['dd_p50']:.1f}R` | |\n\n")

        # Walk-Forward Portfolio
        f.write("## Walk-Forward — Portfolio (3 folds rolling 60/40)\n\n")
        f.write("| Fold | Train Period | Test Period | WR Train | WR Test | PF Train | PF Test | Degradación |\n")
        f.write("|:---|:---|:---|:---|:---|:---|:---|:---|\n")
        for i, fold in enumerate(wf_portfolio_folds):
            f.write(f"| **{i+1}** | {fold['train_period']} | {fold['test_period']} | "
                    f"`{fold['wr_train']:.1%}` | `{fold['wr_test']:.1%}` | "
                    f"`{fold['pf_train']:.2f}` | `{fold['pf_test']:.2f}` | "
                    f"`{fold['degradation']:.1%}` |\n")
        if wf_portfolio_folds:
            avg_deg = np.mean([f["degradation"] for f in wf_portfolio_folds])
            avg_wr_oos = np.mean([f["wr_test"] for f in wf_portfolio_folds])
            avg_pf_oos = np.mean([f["pf_test"] for f in wf_portfolio_folds])
            f.write(f"| **Promedio** | | | | `{avg_wr_oos:.1%}` | | `{avg_pf_oos:.2f}` | `{avg_deg:.1%}` |\n")
        f.write("\n")

        # Decay Portfolio
        f.write("## Decay Analysis — Portfolio\n\n")
        f.write(f"**Decay Score: `{decay_portfolio.get('decay_score', 0):.2f}`** — "
                f"**Tendencia: `{decay_portfolio.get('trend', '?')}`**\n\n")
        if decay_portfolio.get("windows"):
            f.write("| Período | Trades | WR | Expectativa | PnL (R) |\n")
            f.write("|:---|:---|:---|:---|:---|\n")
            for w in decay_portfolio["windows"]:
                f.write(f"| {w['period']} | {w['trades']} | `{w['wr']:.1%}` | "
                        f"`{w['expectancy']:.3f}R` | `{w['pnl']:.1f}R` |\n")
            f.write("\n")

        # 7 MOMENTUM strategies detail
        f.write("## Las 7 Estrategias MOMENTUM (STOP)\n\n")
        f.write("Estas estrategias usan **SELL STOP / BUY STOP** en lugar de LIMIT:\n\n")
        f.write("| Estrategia | Tipo Orden | Trades | WR | WR OOS | MC Ruina | Decay |\n")
        f.write("|:---|:---|:---|:---|:---|:---|:---|\n")
        for r in strat_results:
            if r["order_type"] != "STOP":
                continue
            f.write(f"| {r['label']} | **STOP** | {r['total']} | `{r['wr_full']:.1%}` | "
                    f"`{r['wr_test']:.1%}` | `{r['mc_ruin']:.0%}` | `{r['decay_score']:.2f}` |\n")
        f.write("\n")

        # Per-strategy WF summary (sorted by OOS degradation)
        f.write("## Walk-Forward por Estrategia (todas, por degradación)\n\n")
        f.write("| Estrategia | Orden | Trades | WR IS | WR OOS | Deg | MC Ruina | Decay | Veredicto |\n")
        f.write("|:---|:---|:---|:---|:---|:---|:---|:---|:---|\n")
        strat_results.sort(key=lambda x: x["wf_deg"], reverse=True)
        for r in strat_results:
            verdict = "ALERTA" if r["wf_deg"] > 0.08 else ("OK" if r["wf_deg"] < 0.03 else "VIGILA")
            if r["mc_ruin"] > 0.30:
                verdict = "ALERTA"
            if r["decay_score"] < 0.3:
                verdict = "ALERTA"
            f.write(f"| {r['label']} | {r['order_type']} | {r['total']} | "
                    f"`{r['wr_train']:.1%}` | `{r['wr_test']:.1%}` | `{r['wf_deg']:.1%}` | "
                    f"`{r['mc_ruin']:.0%}` | `{r['decay_score']:.2f}` | **{verdict}** |\n")
        f.write("\n")

        # Classification summary
        n_ok = sum(1 for r in strat_results if r["wf_deg"] < 0.03 and r["mc_ruin"] < 0.15)
        n_watch = sum(1 for r in strat_results if 0.03 <= r["wf_deg"] <= 0.08 and r["mc_ruin"] < 0.30)
        n_alert = sum(1 for r in strat_results if r["wf_deg"] > 0.08 or r["mc_ruin"] >= 0.30 or r["decay_score"] < 0.3)
        f.write(f"### Resumen: {n_ok} OK, {n_watch} VIGILA, {n_alert} ALERTA\n\n")

        # Architecture
        f.write("---\n### Configuración del Portfolio MIXTO\n\n")
        f.write("**101 FADE (LIMIT):** Sell Limit / Buy Limit en OR boundary.\n")
        f.write("Fadian el breakout. Ganan cuando el precio revierte.\n\n")
        f.write("**7 MOMENTUM (STOP):** Sell Stop / Buy Stop en OR boundary.\n")
        f.write("Siguen el breakout. Ganan cuando el precio continúa 1.5R.\n\n")
        f.write("| Estrategia STOP | Símbolo | Sesión | Duración | Lógica |\n")
        f.write("|:---|:---|:---|:---|:---|\n")
        for lbl in sorted(MOMENTUM_OVERRIDES):
            parts = lbl.split("|")
            f.write(f"| {lbl} | {parts[0]} | {parts[1]} | {parts[3]} | "
                    f"Breakout DOWN continúa en {parts[1]} → SELL STOP en OR_LOW |\n")
        f.write("\n")
        f.write("> **Nota:** La selección FADE/MOMENTUM se hizo con hindsight sobre datos completos.\n")
        f.write("> Los resultados Walk-Forward validan si el edge se sostiene out-of-sample.\n")

    print(f"\n{'='*70}")
    print(f"  ROBUSTEZ COMPLETA — Portfolio MIXTO")
    print(f"  Balance: ${initial_balance:,.0f} -> ${balance:,.2f}")
    print(f"  MC P50: {mc_portfolio['pnl_p50']:.1f}R | Prob Ruina: {mc_portfolio['prob_ruin']:.1%}")
    if wf_portfolio_folds:
        print(f"  WF Avg OOS WR: {avg_wr_oos:.1%} | Avg Degradación: {avg_deg:.1%}")
    print(f"  Decay: {decay_portfolio.get('decay_score', 0):.2f} ({decay_portfolio.get('trend', '?')})")
    print(f"  Reporte: {report_path}")
    print(f"{'='*70}")


if __name__ == "__main__":
    bal = float(sys.argv[1]) if len(sys.argv) > 1 else 20000.0
    run_mixed_robustness(bal)
