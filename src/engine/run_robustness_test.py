"""
Pruebas de Robustez para las 117 estrategias del portfolio.
- Monte Carlo (10k permutaciones): prob de ruina, P5/P50/P95
- Walk-Forward OOS (50/50 train/test): WR train vs WR test, degradación
- Decay Analysis (ventanas anuales): tendencia del edge en el tiempo
- Clasificación: FUERTE / ACEPTABLE / DÉBIL / MUERTA
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
    ATR_RATIO_LOW, ATR_RATIO_HIGH,
)


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


def compute_fade_trades(filtered_df, direction, friction):
    """Compute FADE trade PnL series from filtered stats DataFrame."""
    if direction == "UP":
        trades = filtered_df.filter(pl.col("first_break_dir") == "UP")
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
        trades = filtered_df.filter(pl.col("first_break_dir") == "DOWN")
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


def classify_strategy(mc, wf_degradation, decay_score, net_r, wr_oos):
    """
    Classify strategy robustness:
    - FUERTE: MC profitable P5, WF degradation < 5%, decay stable, positive net_r
    - ACEPTABLE: MC profitable P25, WF degradation < 10%, decay not collapsing
    - DÉBIL: Some red flags but not dead
    - MUERTA: MC P50 negative or WF degradation > 15% or decay collapsing
    """
    red_flags = 0
    reasons = []

    if mc["prob_ruin"] > 0.30:
        red_flags += 2
        reasons.append(f"MC ruina {mc['prob_ruin']:.0%}")
    elif mc["prob_ruin"] > 0.15:
        red_flags += 1
        reasons.append(f"MC ruina {mc['prob_ruin']:.0%}")

    if mc["pnl_p5"] < 0:
        red_flags += 1
        reasons.append(f"MC P5 negativo ({mc['pnl_p5']:.1f}R)")

    if mc["pnl_p50"] < 0:
        red_flags += 2
        reasons.append(f"MC P50 negativo ({mc['pnl_p50']:.1f}R)")

    if wf_degradation > 0.15:
        red_flags += 2
        reasons.append(f"WF degradación {wf_degradation:.1%}")
    elif wf_degradation > 0.08:
        red_flags += 1
        reasons.append(f"WF degradación {wf_degradation:.1%}")

    if wr_oos < 0.55:
        red_flags += 2
        reasons.append(f"WR OOS {wr_oos:.1%}")
    elif wr_oos < 0.58:
        red_flags += 1
        reasons.append(f"WR OOS {wr_oos:.1%}")

    if decay_score < 0.3:
        red_flags += 2
        reasons.append(f"Decay colapsando ({decay_score:.2f})")
    elif decay_score < 0.7:
        red_flags += 1
        reasons.append(f"Decay degradando ({decay_score:.2f})")

    if net_r < 0:
        red_flags += 1
        reasons.append(f"Net R negativo ({net_r:.1f})")

    if red_flags == 0:
        return "FUERTE", reasons
    elif red_flags <= 2:
        return "ACEPTABLE", reasons
    elif red_flags <= 4:
        return "DÉBIL", reasons
    else:
        return "MUERTA", reasons


def run_robustness():
    ROOT = "c:/Proyectos/kha0sys3"
    loader = CSVPolarsLoader(os.path.join(ROOT, "data"))
    with open(os.path.join(ROOT, "src", "infrastructure", "config", "asset_config.json")) as f:
        asset_config = json.load(f)
    with open(os.path.join(ROOT, "src", "execution", "bot_config.json")) as f:
        bot_config = json.load(f)

    portfolio = bot_config["portfolio"]
    reports_dir = os.path.join(ROOT, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    print(f"Analizando robustez de {len(portfolio)} estrategias...")

    # Group by combo to avoid recomputing
    combo_strategies = defaultdict(list)
    for strat in portfolio:
        sym = MT5_TO_INTERNAL.get(strat["sym"], strat["sym"])
        key = (sym, strat["magic_time"], strat["duration"])
        combo_strategies[key].append(strat)

    # Cache expanded stats per combo
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
            stats_df = TrackerEngine.track_events(df_or, tp_multiplier=1.5)

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

    # Analyze each strategy
    results = []
    for idx, strat in enumerate(portfolio):
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
        label = f"{sym}|{strat['session']}|{edge}|{strat['duration']}m|{ctx_label or 'BASE'}"

        filtered = valid
        if ctx_filter:
            filtered = StrategyScanner.apply_context_filter(filtered, ctx_filter)

        trades_df = compute_fade_trades(filtered, direction, friction)
        if trades_df.height < 20:
            continue

        trades_sorted = trades_df.sort("trade_date")
        pnls = trades_sorted["pnl_r"].to_list()
        dates = [str(d) for d in trades_sorted["trade_date"].to_list()]
        total = len(pnls)
        wins = sum(1 for p in pnls if p > 0)
        wr_full = wins / total
        net_r = sum(pnls)

        # --- 1. Monte Carlo ---
        mc = StatisticalValidator.monte_carlo(pnls, n_sims=10000)

        # --- 2. Walk-Forward OOS (50/50) ---
        mid = total // 2
        train_pnls = pnls[:mid]
        test_pnls = pnls[mid:]
        train_wins = sum(1 for p in train_pnls if p > 0)
        test_wins = sum(1 for p in test_pnls if p > 0)
        wr_train = train_wins / len(train_pnls) if train_pnls else 0
        wr_test = test_wins / len(test_pnls) if test_pnls else 0
        wf_degradation = max(0, wr_train - wr_test)
        net_r_train = sum(train_pnls)
        net_r_test = sum(test_pnls)

        # --- 3. Decay Analysis ---
        decay = StatisticalValidator.decay_analysis(pnls, dates, window_days=365)
        decay_score = decay.get("decay_score", 1.0)
        decay_trend = decay.get("trend", "?")

        # Last 2 years window
        if decay.get("windows") and len(decay["windows"]) >= 2:
            last_2 = decay["windows"][-2:]
            wr_recent = np.mean([w["wr"] for w in last_2])
            exp_recent = np.mean([w["expectancy"] for w in last_2])
        else:
            wr_recent = wr_full
            exp_recent = np.mean(pnls)

        # --- 4. Classification ---
        classification, reasons = classify_strategy(mc, wf_degradation, decay_score, net_r, wr_test)

        results.append({
            "label": label,
            "sym": sym,
            "session": strat["session"],
            "edge": edge,
            "duration": strat["duration"],
            "context": ctx_label or "BASE",
            "wr_cfg": strat["win_rate"],
            "total": total,
            "wr_full": wr_full,
            "net_r": net_r,
            # MC
            "mc_p5": mc["pnl_p5"],
            "mc_p50": mc["pnl_p50"],
            "mc_p95": mc["pnl_p95"],
            "mc_prob_ruin": mc["prob_ruin"],
            "mc_prob_profit": mc["prob_profit"],
            # WF
            "wr_train": wr_train,
            "wr_test": wr_test,
            "wf_degradation": wf_degradation,
            "net_r_train": net_r_train,
            "net_r_test": net_r_test,
            # Decay
            "decay_score": decay_score,
            "decay_trend": decay_trend,
            "wr_recent": wr_recent,
            "exp_recent": exp_recent,
            # Classification
            "classification": classification,
            "reasons": reasons,
        })

        status_icon = {"FUERTE": "+", "ACEPTABLE": "~", "DÉBIL": "!", "MUERTA": "X"}
        print(f"  [{status_icon.get(classification, '?')}] {label}: {classification} "
              f"(WR={wr_full:.1%}, MC_ruin={mc['prob_ruin']:.0%}, WF_deg={wf_degradation:.1%}, "
              f"Decay={decay_score:.2f})")

    # --- Generate Report ---
    results.sort(key=lambda x: {"MUERTA": 0, "DÉBIL": 1, "ACEPTABLE": 2, "FUERTE": 3}[x["classification"]])

    counts = defaultdict(int)
    for r in results:
        counts[r["classification"]] += 1

    report_path = os.path.join(reports_dir, "Portfolio_117_Robustness_Report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Pruebas de Robustez — 117 Estrategias\n\n")
        f.write(f"> Monte Carlo 10k | Walk-Forward 50/50 | Decay Anual\n")
        f.write(f"> Período: 2018-01-17 → 2026-03-24\n\n")

        f.write("## Resumen de Clasificación\n")
        f.write("| Clasificación | Cantidad | % |\n|:---|:---|:---|\n")
        for cls in ["FUERTE", "ACEPTABLE", "DÉBIL", "MUERTA"]:
            n = counts.get(cls, 0)
            pct = n / len(results) if results else 0
            f.write(f"| **{cls}** | {n} | `{pct:.0%}` |\n")
        f.write(f"| **TOTAL** | {len(results)} | |\n\n")

        # Criteria explanation
        f.write("## Criterios de Clasificación\n")
        f.write("| Test | FUERTE | ACEPTABLE | DÉBIL | MUERTA |\n")
        f.write("|:---|:---|:---|:---|:---|\n")
        f.write("| MC Prob Ruina | <15% | <30% | <50% | >50% |\n")
        f.write("| MC P5 | >0 | ~0 | <0 | P50<0 |\n")
        f.write("| WF Degradación | <8% | <15% | >15% | >15% |\n")
        f.write("| WR OOS | >58% | >55% | <55% | <55% |\n")
        f.write("| Decay Score | >0.7 | >0.3 | <0.3 | <0.3 |\n\n")

        # MUERTAS y DÉBILES primero (las que importan)
        for cls in ["MUERTA", "DÉBIL"]:
            group = [r for r in results if r["classification"] == cls]
            if not group:
                continue
            f.write(f"## Estrategias {cls}S ({len(group)})\n")
            f.write("| Estrategia | Trades | WR Full | WR Train | WR Test | WF Deg | MC Ruina | MC P5 | Decay | Razones |\n")
            f.write("|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|\n")
            for r in group:
                reasons_str = "; ".join(r["reasons"][:3])
                f.write(f"| **{r['label']}** | {r['total']} | `{r['wr_full']:.1%}` | "
                        f"`{r['wr_train']:.1%}` | `{r['wr_test']:.1%}` | `{r['wf_degradation']:.1%}` | "
                        f"`{r['mc_prob_ruin']:.0%}` | `{r['mc_p5']:.1f}` | `{r['decay_score']:.2f}` | "
                        f"{reasons_str} |\n")
            f.write("\n")

        # ACEPTABLES
        group = [r for r in results if r["classification"] == "ACEPTABLE"]
        if group:
            f.write(f"## Estrategias ACEPTABLES ({len(group)})\n")
            f.write("| Estrategia | Trades | WR Full | WR OOS | WF Deg | MC Ruina | Decay | Razones |\n")
            f.write("|:---|:---|:---|:---|:---|:---|:---|:---|\n")
            for r in sorted(group, key=lambda x: x["net_r"]):
                reasons_str = "; ".join(r["reasons"][:2]) if r["reasons"] else "-"
                f.write(f"| {r['label']} | {r['total']} | `{r['wr_full']:.1%}` | "
                        f"`{r['wr_test']:.1%}` | `{r['wf_degradation']:.1%}` | "
                        f"`{r['mc_prob_ruin']:.0%}` | `{r['decay_score']:.2f}` | {reasons_str} |\n")
            f.write("\n")

        # FUERTES
        group = [r for r in results if r["classification"] == "FUERTE"]
        if group:
            f.write(f"## Estrategias FUERTES ({len(group)})\n")
            f.write("| Estrategia | Trades | WR Full | WR OOS | Net R | MC P50 | Decay |\n")
            f.write("|:---|:---|:---|:---|:---|:---|:---|\n")
            for r in sorted(group, key=lambda x: x["net_r"], reverse=True):
                f.write(f"| {r['label']} | {r['total']} | `{r['wr_full']:.1%}` | "
                        f"`{r['wr_test']:.1%}` | `{r['net_r']:.1f}` | "
                        f"`{r['mc_p50']:.1f}` | `{r['decay_score']:.2f}` |\n")
            f.write("\n")

        # Walk-Forward detail table (all strategies sorted by WF degradation)
        f.write("## Walk-Forward Detail (todas, ordenadas por degradación)\n")
        f.write("| Estrategia | WR Train | WR Test | Degradación | Net R Train | Net R Test | Veredicto |\n")
        f.write("|:---|:---|:---|:---|:---|:---|:---|\n")
        for r in sorted(results, key=lambda x: x["wf_degradation"], reverse=True):
            verdict = "ALERTA" if r["wf_degradation"] > 0.08 else ("OK" if r["wf_degradation"] < 0.03 else "VIGILA")
            f.write(f"| {r['label']} | `{r['wr_train']:.1%}` | `{r['wr_test']:.1%}` | "
                    f"`{r['wf_degradation']:.1%}` | `{r['net_r_train']:.1f}` | `{r['net_r_test']:.1f}` | "
                    f"**{verdict}** |\n")
        f.write("\n")

        # Decay detail
        f.write("## Decay Analysis (todas, ordenadas por decay score)\n")
        f.write("| Estrategia | Decay Score | Tendencia | WR Reciente | Exp Reciente |\n")
        f.write("|:---|:---|:---|:---|:---|\n")
        for r in sorted(results, key=lambda x: x["decay_score"]):
            f.write(f"| {r['label']} | `{r['decay_score']:.2f}` | **{r['decay_trend']}** | "
                    f"`{r['wr_recent']:.1%}` | `{r['exp_recent']:.3f}R` |\n")
        f.write("\n")

        # Monte Carlo summary
        f.write("## Monte Carlo Summary (ordenado por prob de ruina)\n")
        f.write("| Estrategia | Trades | P5 (R) | P50 (R) | P95 (R) | Prob Ruina | Prob Profit |\n")
        f.write("|:---|:---|:---|:---|:---|:---|:---|\n")
        for r in sorted(results, key=lambda x: x["mc_prob_ruin"], reverse=True):
            f.write(f"| {r['label']} | {r['total']} | `{r['mc_p5']:.1f}` | `{r['mc_p50']:.1f}` | "
                    f"`{r['mc_p95']:.1f}` | `{r['mc_prob_ruin']:.0%}` | `{r['mc_prob_profit']:.0%}` |\n")
        f.write("\n")

    print(f"\n{'='*60}")
    print(f"  ROBUSTEZ COMPLETA")
    print(f"  FUERTE: {counts.get('FUERTE', 0)} | ACEPTABLE: {counts.get('ACEPTABLE', 0)} | "
          f"DÉBIL: {counts.get('DÉBIL', 0)} | MUERTA: {counts.get('MUERTA', 0)}")
    print(f"  Reporte: {report_path}")
    print(f"{'='*60}")

    return results


if __name__ == "__main__":
    run_robustness()
