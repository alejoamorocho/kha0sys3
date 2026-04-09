"""
R:R Exploration v2 — Baseline correcto TP=1.0 SL=1.5 (paridad backtest).
Prueba grilla TP x SL, selecciona optimo por estrategia,
luego valida con Monte Carlo 10k + Walk-Forward rolling.

Restricciones:
  1. No disminuir trades vs baseline
  2. Aumentar PnL neto
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


# Baseline = backtest actual: TP at 1.0*width, loss boundary at 1.5*width
BASELINE_TP = 1.0
BASELINE_SL = 1.5

TP_MULTS = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
SL_MULTS = [0.75, 1.0, 1.25, 1.5, 2.0, 2.5]


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


def track_multi_level(post_or_df: pl.DataFrame, direction: str,
                      tp_mults: list, sl_mults: list) -> pl.DataFrame:
    """Track first hit times for multiple TP/SL levels per day."""
    df = post_or_df.filter(pl.col("is_active_session") == True)
    if df.height == 0:
        return pl.DataFrame()

    agg_exprs = []

    if direction == "UP":
        for tp in tp_mults:
            col = f"t_tp_{tp:.2f}"
            tp_df = df.filter(
                pl.col("low") <= (pl.col("or_high") - pl.col("or_width") * tp)
            ).group_by("trade_date").agg(pl.col("mins_from_midnight").min().alias(col))
            agg_exprs.append((col, tp_df))

        for sl in sl_mults:
            col = f"t_sl_{sl:.2f}"
            sl_df = df.filter(
                pl.col("high") >= (pl.col("or_high") + pl.col("or_width") * sl)
            ).group_by("trade_date").agg(pl.col("mins_from_midnight").min().alias(col))
            agg_exprs.append((col, sl_df))

        brk_up = df.filter(pl.col("high") >= pl.col("or_high")).group_by("trade_date").agg(
            pl.col("mins_from_midnight").min().alias("t_brk_up"))
        brk_dn = df.filter(pl.col("low") <= pl.col("or_low")).group_by("trade_date").agg(
            pl.col("mins_from_midnight").min().alias("t_brk_dn"))
    else:
        for tp in tp_mults:
            col = f"t_tp_{tp:.2f}"
            tp_df = df.filter(
                pl.col("high") >= (pl.col("or_low") + pl.col("or_width") * tp)
            ).group_by("trade_date").agg(pl.col("mins_from_midnight").min().alias(col))
            agg_exprs.append((col, tp_df))

        for sl in sl_mults:
            col = f"t_sl_{sl:.2f}"
            sl_df = df.filter(
                pl.col("low") <= (pl.col("or_low") - pl.col("or_width") * sl)
            ).group_by("trade_date").agg(pl.col("mins_from_midnight").min().alias(col))
            agg_exprs.append((col, sl_df))

        brk_up = df.filter(pl.col("high") >= pl.col("or_high")).group_by("trade_date").agg(
            pl.col("mins_from_midnight").min().alias("t_brk_up"))
        brk_dn = df.filter(pl.col("low") <= pl.col("or_low")).group_by("trade_date").agg(
            pl.col("mins_from_midnight").min().alias("t_brk_dn"))

    base = df.select("trade_date").unique()
    result = base.join(brk_up, on="trade_date", how="left")
    result = result.join(brk_dn, on="trade_date", how="left")
    for col, level_df in agg_exprs:
        result = result.join(level_df, on="trade_date", how="left")

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
    return result


def eval_rr(multi_df: pl.DataFrame, direction: str,
            tp_m: float, sl_m: float, friction: float) -> dict:
    """Evaluate one TP/SL combo. Returns trades list with dates + pnl."""
    tc = f"t_tp_{tp_m:.2f}"
    sc = f"t_sl_{sl_m:.2f}"
    if tc not in multi_df.columns or sc not in multi_df.columns:
        return {"trades": 0, "wins": 0, "wr": 0, "net_r": 0, "pnls": [], "dates": []}

    filt = multi_df.filter(
        pl.col("first_break_dir") == ("UP" if direction == "UP" else "DOWN"))

    filt = filt.with_columns(
        pl.when(pl.col(tc).is_not_null()
                & (pl.col(sc).is_null() | (pl.col(tc) < pl.col(sc))))
        .then(pl.lit(tp_m) - friction)
        .when(pl.col(sc).is_not_null()
              & (pl.col(tc).is_null() | (pl.col(sc) <= pl.col(tc))))
        .then(pl.lit(-sl_m) - friction)
        .otherwise(0.0)
        .alias("pnl_r")
    )
    resolved = filt.filter(pl.col("pnl_r") != 0.0).sort("trade_date")
    n = resolved.height
    if n == 0:
        return {"trades": 0, "wins": 0, "wr": 0, "net_r": 0, "pnls": [], "dates": []}

    pnls = resolved["pnl_r"].to_list()
    dates = [str(d) for d in resolved["trade_date"].to_list()]
    wins = sum(1 for p in pnls if p > 0)
    return {
        "trades": n, "wins": wins, "wr": wins / n,
        "net_r": sum(pnls), "pnls": pnls, "dates": dates,
    }


def run():
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

    print(f"=== R:R Exploration v2: {len(portfolio)} estrategias ===")
    print(f"  Baseline: TP={BASELINE_TP} SL={BASELINE_SL} (paridad backtest)")
    print(f"  TP grid: {TP_MULTS}")
    print(f"  SL grid: {SL_MULTS}")

    # Ensure baseline SL is in the grid
    all_tp = sorted(set(TP_MULTS + [BASELINE_TP]))
    all_sl = sorted(set(SL_MULTS + [BASELINE_SL]))

    # Load and cache data
    combo_strategies = defaultdict(list)
    for strat in portfolio:
        sym = MT5_TO_INTERNAL.get(strat["sym"], strat["sym"])
        key = (sym, strat["magic_time"], strat["duration"])
        combo_strategies[key].append(strat)

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
            post_or = df_or.filter(pl.col("is_post_or") == True)

            daily_atr = df_or.group_by("trade_date").agg(pl.col("or_atr_ratio").first())
            valid_days = daily_atr.filter(
                pl.col("or_atr_ratio").is_between(ATR_RATIO_LOW, ATR_RATIO_HIGH)
            ).select("trade_date")
            post_or = post_or.join(valid_days, on="trade_date", how="inner")

            # Context columns
            ctx_cols = []
            for c in ["rsi_at_or_close", "rsi_daily_14", "atr_change", "atr_percentile",
                       "or_position_vs_pd", "or_open_vs_pd_close", "or_open", "pd_or_high", "pd_or_low"]:
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

    # Track multi-level events
    multi_cache = {}
    for (sym, ts, dur), (post_or, daily_ctx) in combo_cache.items():
        for d in ["UP", "DOWN"]:
            mdf = track_multi_level(post_or, d, all_tp, all_sl)
            if daily_ctx is not None:
                ccols = [c for c in daily_ctx.columns if c != "trade_date"]
                mdf = mdf.join(daily_ctx.select(["trade_date"] + ccols), on="trade_date", how="left")
            multi_cache[(sym, ts, dur, d)] = mdf

    # === Evaluate each strategy ===
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
        risk_pct = allocator.get_risk_percent(strat["win_rate"])
        label = f"{sym}|{strat['session']}|{edge}|{duration}m|{ctx_label or 'BASE'}"

        mdf = multi_cache.get((sym, time_start, duration, direction))
        if mdf is None or mdf.height == 0:
            continue

        filtered = mdf
        if ctx_filter:
            filtered = StrategyScanner.apply_context_filter(filtered, ctx_filter)
        if filtered.height == 0:
            continue

        # Baseline
        bl = eval_rr(filtered, direction, BASELINE_TP, BASELINE_SL, friction)
        if bl["trades"] < 20:
            continue

        # Grid search
        best = {"tp": BASELINE_TP, "sl": BASELINE_SL, **bl, "improvement": 0.0}
        grid = []
        for tp in all_tp:
            for sl in all_sl:
                r = eval_rr(filtered, direction, tp, sl, friction)
                grid.append({"tp": tp, "sl": sl, **r})
                if (r["trades"] >= bl["trades"]
                        and r["net_r"] > bl["net_r"]
                        and r["net_r"] > best["net_r"]):
                    best = {"tp": tp, "sl": sl, **r, "improvement": r["net_r"] - bl["net_r"]}

        results.append({
            "label": label, "symbol": sym, "session": strat["session"],
            "direction": direction, "duration": duration, "risk_pct": risk_pct,
            "baseline": bl, "best": best, "grid": grid,
        })

        changed = best["tp"] != BASELINE_TP or best["sl"] != BASELINE_SL
        tag = "MEJOR" if changed else "= baseline"
        print(f"  {label}: {tag} TP={best['tp']:.2f} SL={best['sl']:.2f} "
              f"| Net R: {bl['net_r']:.1f} -> {best['net_r']:.1f} "
              f"({best['improvement']:+.1f}) | WR: {bl['wr']:.1%} -> {best['wr']:.1%} "
              f"| Trades: {bl['trades']}->{best['trades']}")

    # === Validation: MC + WF on optimized strategies ===
    print(f"\n--- Validacion Monte Carlo + Walk-Forward ---")
    changed = [r for r in results if r["best"]["tp"] != BASELINE_TP or r["best"]["sl"] != BASELINE_SL]
    unchanged = [r for r in results if r["best"]["tp"] == BASELINE_TP and r["best"]["sl"] == BASELINE_SL]

    for r in results:
        b = r["best"]
        pnls = b["pnls"]
        dates = b["dates"]
        if len(pnls) < 30:
            r["mc"] = None
            r["wf"] = None
            r["decay"] = None
            continue

        # Monte Carlo
        mc = StatisticalValidator.monte_carlo(pnls, n_sims=10000)
        r["mc"] = mc

        # Walk-Forward 50/50
        mid = len(pnls) // 2
        tr_p, te_p = pnls[:mid], pnls[mid:]
        wr_tr = sum(1 for p in tr_p if p > 0) / len(tr_p) if tr_p else 0
        wr_te = sum(1 for p in te_p if p > 0) / len(te_p) if te_p else 0
        nr_tr = sum(tr_p)
        nr_te = sum(te_p)
        r["wf"] = {"wr_train": wr_tr, "wr_test": wr_te, "deg": max(0, wr_tr - wr_te),
                    "net_r_train": nr_tr, "net_r_test": nr_te}

        # Decay
        decay = StatisticalValidator.decay_analysis(pnls, dates, window_days=365)
        r["decay"] = decay

        is_changed = b["tp"] != BASELINE_TP or b["sl"] != BASELINE_SL
        if is_changed:
            print(f"  {r['label']}: MC_ruin={mc['prob_ruin']:.0%} "
                  f"WF_deg={r['wf']['deg']:.1%} WR_OOS={wr_te:.1%} "
                  f"Decay={decay.get('decay_score', 0):.2f}")

    # === Portfolio-level MC on deduped trades ===
    print(f"\n--- Portfolio Monte Carlo (baseline vs optimized) ---")

    def build_portfolio_trades(results_list, use_best):
        all_t = []
        for r in results_list:
            src = r["best"] if use_best else r["baseline"]
            risk = r["risk_pct"]
            h, m_ = 0, 0
            # exec_mins from label
            for s in portfolio:
                sym_i = MT5_TO_INTERNAL.get(s["sym"], s["sym"])
                lbl = f"{sym_i}|{s['session']}|{s['edge']}|{s['duration']}m|{s.get('context') or 'BASE'}"
                if lbl == r["label"]:
                    h, m_ = map(int, s["magic_time"].split(":"))
                    exec_mins = h * 60 + m_ + s["duration"]
                    break
            else:
                exec_mins = 0
            for d, p in zip(src["dates"], src["pnls"]):
                all_t.append({"date": d, "symbol": r["symbol"], "pnl_r": p,
                              "risk_pct": risk, "exec_mins": exec_mins})
        all_t.sort(key=lambda x: (x["date"], x["exec_mins"]))
        seen = set()
        deduped = []
        for t in all_t:
            k = (t["date"], t["symbol"])
            if k not in seen:
                seen.add(k)
                deduped.append(t)
        return deduped

    init_bal = 20000.0
    bl_trades = build_portfolio_trades(results, False)
    opt_trades = build_portfolio_trades(results, True)

    def sim_portfolio(trades, bal):
        b = bal
        pk = bal
        mdd = 0
        yearly = defaultdict(lambda: {"trades": 0, "wins": 0, "pnl_usd": 0.0, "pnl_r": 0.0})
        pnls = []
        for t in trades:
            ra = bal * t["risk_pct"]
            dp = t["pnl_r"] * ra
            b += dp
            pk = max(pk, b)
            dd = (b - pk) / pk if pk > 0 else 0
            mdd = min(mdd, dd)
            pnls.append(t["pnl_r"])
            yr = t["date"][:4]
            yearly[yr]["trades"] += 1
            yearly[yr]["pnl_usd"] += dp
            yearly[yr]["pnl_r"] += t["pnl_r"]
            if t["pnl_r"] > 0:
                yearly[yr]["wins"] += 1
        n = len(trades)
        w = sum(1 for t in trades if t["pnl_r"] > 0)
        gp = sum(p for p in pnls if p > 0)
        gl = abs(sum(p for p in pnls if p < 0))
        return {
            "balance": b, "pnl_usd": b - bal, "trades": n, "wins": w,
            "wr": w / n if n > 0 else 0, "pf": gp / gl if gl > 0 else 99,
            "net_r": sum(pnls), "max_dd": mdd, "yearly": dict(yearly), "pnls": pnls,
        }

    bl_sim = sim_portfolio(bl_trades, init_bal)
    opt_sim = sim_portfolio(opt_trades, init_bal)

    print(f"  Baseline TP={BASELINE_TP} SL={BASELINE_SL}:")
    print(f"    ${bl_sim['pnl_usd']:,.0f} | WR {bl_sim['wr']:.1%} | PF {bl_sim['pf']:.2f} | "
          f"DD {bl_sim['max_dd']:.1%} | {bl_sim['trades']} trades")
    print(f"  Optimizado por estrategia:")
    print(f"    ${opt_sim['pnl_usd']:,.0f} | WR {opt_sim['wr']:.1%} | PF {opt_sim['pf']:.2f} | "
          f"DD {opt_sim['max_dd']:.1%} | {opt_sim['trades']} trades")

    # MC on portfolio
    mc_bl = StatisticalValidator.monte_carlo(bl_sim["pnls"], n_sims=10000)
    mc_opt = StatisticalValidator.monte_carlo(opt_sim["pnls"], n_sims=10000)

    print(f"\n  MC Baseline:   P5={mc_bl['pnl_p5']:.0f}R P50={mc_bl['pnl_p50']:.0f}R "
          f"Ruina={mc_bl['prob_ruin']:.1%}")
    print(f"  MC Optimizado: P5={mc_opt['pnl_p5']:.0f}R P50={mc_opt['pnl_p50']:.0f}R "
          f"Ruina={mc_opt['prob_ruin']:.1%}")

    # WF on portfolio
    for name, pnls_list, dates_list in [
        ("Baseline", [t["pnl_r"] for t in bl_trades], [t["date"] for t in bl_trades]),
        ("Optimizado", [t["pnl_r"] for t in opt_trades], [t["date"] for t in opt_trades]),
    ]:
        mid = len(pnls_list) // 2
        tr, te = pnls_list[:mid], pnls_list[mid:]
        wr_tr = sum(1 for p in tr if p > 0) / len(tr) if tr else 0
        wr_te = sum(1 for p in te if p > 0) / len(te) if te else 0
        nr_tr, nr_te = sum(tr), sum(te)
        print(f"  WF {name}: IS WR={wr_tr:.1%} Net={nr_tr:.0f}R | OOS WR={wr_te:.1%} Net={nr_te:.0f}R | "
              f"Deg={max(0, wr_tr - wr_te):.1%}")

    # Decay on portfolio
    decay_bl = StatisticalValidator.decay_analysis(bl_sim["pnls"],
                                                    [t["date"] for t in bl_trades], 365)
    decay_opt = StatisticalValidator.decay_analysis(opt_sim["pnls"],
                                                     [t["date"] for t in opt_trades], 365)
    print(f"  Decay Baseline:   {decay_bl.get('decay_score', 0):.2f} ({decay_bl.get('trend', '?')})")
    print(f"  Decay Optimizado: {decay_opt.get('decay_score', 0):.2f} ({decay_opt.get('trend', '?')})")

    # === Report ===
    report_path = os.path.join(reports_dir, "RR_Exploration_v2.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# R:R Exploration v2 -- Baseline TP=1.0 SL=1.5 (backtest parity)\n\n")
        f.write(f"> TP grid: {all_tp} | SL grid: {all_sl}\n")
        f.write(f"> Restriccion: trades >= baseline AND net_r > baseline\n\n")

        # Portfolio comparison
        f.write("## Portfolio: Baseline vs Optimizado\n\n")
        f.write("| Metrica | Baseline (TP=1.0 SL=1.5) | Optimizado |\n|:---|:---|:---|\n")
        f.write(f"| **Balance** | `${bl_sim['balance']:,.0f}` | `${opt_sim['balance']:,.0f}` |\n")
        f.write(f"| **PnL** | `${bl_sim['pnl_usd']:,.0f}` | `${opt_sim['pnl_usd']:,.0f}` |\n")
        f.write(f"| **Trades** | `{bl_sim['trades']:,}` | `{opt_sim['trades']:,}` |\n")
        f.write(f"| **Win Rate** | `{bl_sim['wr']:.1%}` | `{opt_sim['wr']:.1%}` |\n")
        f.write(f"| **Profit Factor** | `{bl_sim['pf']:.2f}` | `{opt_sim['pf']:.2f}` |\n")
        f.write(f"| **Net R** | `{bl_sim['net_r']:.0f}` | `{opt_sim['net_r']:.0f}` |\n")
        f.write(f"| **Max Drawdown** | `{bl_sim['max_dd']:.1%}` | `{opt_sim['max_dd']:.1%}` |\n")
        f.write(f"| **MC P5** | `{mc_bl['pnl_p5']:.0f}R` | `{mc_opt['pnl_p5']:.0f}R` |\n")
        f.write(f"| **MC P50** | `{mc_bl['pnl_p50']:.0f}R` | `{mc_opt['pnl_p50']:.0f}R` |\n")
        f.write(f"| **MC Prob Ruina** | `{mc_bl['prob_ruin']:.1%}` | `{mc_opt['prob_ruin']:.1%}` |\n")
        f.write(f"| **Decay Score** | `{decay_bl.get('decay_score', 0):.2f}` | "
                f"`{decay_opt.get('decay_score', 0):.2f}` |\n\n")

        # Yearly comparison
        all_years = sorted(set(list(bl_sim["yearly"].keys()) + list(opt_sim["yearly"].keys())))
        f.write("## Rendimiento Anual\n\n")
        f.write("| Ano | BL Trades | BL WR | BL PnL$ | OPT Trades | OPT WR | OPT PnL$ |\n")
        f.write("|:---|:---|:---|:---|:---|:---|:---|\n")
        for yr in all_years:
            yb = bl_sim["yearly"].get(yr, {"trades": 0, "wins": 0, "pnl_usd": 0})
            yo = opt_sim["yearly"].get(yr, {"trades": 0, "wins": 0, "pnl_usd": 0})
            wr_b = yb["wins"] / yb["trades"] if yb["trades"] > 0 else 0
            wr_o = yo["wins"] / yo["trades"] if yo["trades"] > 0 else 0
            f.write(f"| **{yr}** | {yb['trades']} | `{wr_b:.1%}` | `${yb['pnl_usd']:,.0f}` | "
                    f"{yo['trades']} | `{wr_o:.1%}` | `${yo['pnl_usd']:,.0f}` |\n")
        f.write("\n")

        # Strategies that improved
        f.write(f"## Estrategias Mejoradas ({len(changed)})\n\n")
        f.write("| Estrategia | BL TP:SL | BL Net R | OPT TP:SL | OPT Net R | +R | "
                "BL WR | OPT WR | MC Ruina | WF Deg | Decay |\n")
        f.write("|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|\n")
        changed.sort(key=lambda x: x["best"]["improvement"], reverse=True)
        for r in changed:
            b, o = r["baseline"], r["best"]
            mc = r.get("mc", {}) or {}
            wf = r.get("wf", {}) or {}
            dc = r.get("decay", {}) or {}
            f.write(f"| {r['label']} | {BASELINE_TP}:{BASELINE_SL} | `{b['net_r']:.1f}` | "
                    f"**{o['tp']:.1f}:{o['sl']:.1f}** | `{o['net_r']:.1f}` | "
                    f"`+{o['improvement']:.1f}` | `{b['wr']:.1%}` | `{o['wr']:.1%}` | "
                    f"`{mc.get('prob_ruin', 0):.0%}` | `{wf.get('deg', 0):.1%}` | "
                    f"`{dc.get('decay_score', 0):.2f}` |\n")
        if changed:
            total_imp = sum(r["best"]["improvement"] for r in changed)
            f.write(f"\n**Total mejora: +{total_imp:.0f}R**\n\n")

        # Strategies at baseline
        f.write(f"## Estrategias Optimas con Baseline ({len(unchanged)})\n\n")
        if unchanged:
            f.write("| Estrategia | Net R | WR | Trades | MC Ruina | Decay |\n")
            f.write("|:---|:---|:---|:---|:---|:---|\n")
            for r in sorted(unchanged, key=lambda x: x["baseline"]["net_r"], reverse=True):
                b = r["baseline"]
                mc = r.get("mc", {}) or {}
                dc = r.get("decay", {}) or {}
                f.write(f"| {r['label']} | `{b['net_r']:.1f}` | `{b['wr']:.1%}` | {b['trades']} | "
                        f"`{mc.get('prob_ruin', 0):.0%}` | `{dc.get('decay_score', 0):.2f}` |\n")
        else:
            f.write("Ninguna -- todas mejoran con R:R optimizado.\n")
        f.write("\n")

        # Distribution of optimal R:R
        f.write("## Distribucion de R:R Optimos\n\n")
        tp_dist = defaultdict(int)
        sl_dist = defaultdict(int)
        combo_dist = defaultdict(int)
        for r in changed:
            tp_dist[r["best"]["tp"]] += 1
            sl_dist[r["best"]["sl"]] += 1
            combo_dist[(r["best"]["tp"], r["best"]["sl"])] += 1

        f.write("| TP:SL Combo | Cantidad |\n|:---|:---|\n")
        for (tp, sl), n in sorted(combo_dist.items(), key=lambda x: -x[1]):
            f.write(f"| **TP={tp:.1f} SL={sl:.1f}** | {n} |\n")
        f.write("\n")

        # Decay windows for optimized portfolio
        if decay_opt.get("windows"):
            f.write("## Decay Portfolio Optimizado\n\n")
            f.write("| Periodo | Trades | WR | Expectativa |\n|:---|:---|:---|:---|\n")
            for w in decay_opt["windows"]:
                f.write(f"| {w['period']} | {w['trades']} | `{w['wr']:.1%}` | `{w['expectancy']:.3f}R` |\n")
            f.write("\n")

    print(f"\n{'='*70}")
    print(f"  R:R EXPLORATION v2 COMPLETA")
    print(f"  {len(changed)} mejoran, {len(unchanged)} en baseline")
    print(f"  Baseline:   ${bl_sim['pnl_usd']:,.0f} | Optimizado: ${opt_sim['pnl_usd']:,.0f}")
    print(f"  MC Baseline: P50={mc_bl['pnl_p50']:.0f}R Ruina={mc_bl['prob_ruin']:.1%}")
    print(f"  MC Optim:    P50={mc_opt['pnl_p50']:.0f}R Ruina={mc_opt['prob_ruin']:.1%}")
    print(f"  Reporte: {report_path}")
    print(f"{'='*70}")


if __name__ == "__main__":
    run()
