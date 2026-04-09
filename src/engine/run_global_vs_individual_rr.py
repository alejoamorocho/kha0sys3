"""
Comparacion: Global TP=0.5 SL=2.5 (live actual) vs Individual R:R optimizado.
"""

import json
import os
import sys
import numpy as np
import polars as pl
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.infrastructure.data.polars_loader import CSVPolarsLoader
from src.application.calculators import DataEnricher
from src.engine.strategy_scanner import StrategyScanner
from src.engine.statistical_validator import StatisticalValidator
from src.domain.constants import (
    MT5_TO_INTERNAL, INDEX_SYMBOLS, FRICTION_FX, FRICTION_INDEX,
    ATR_RATIO_LOW, ATR_RATIO_HIGH,
)
from src.execution.risk_manager import DynamicRiskAllocator
from src.engine.run_rr_exploration_v2 import (
    track_multi_level, eval_rr, resolve_context_filter,
)

ROOT = "c:/Proyectos/kha0sys3"


def load_data(portfolio):
    loader = CSVPolarsLoader(f"{ROOT}/data")
    with open(f"{ROOT}/src/infrastructure/config/asset_config.json") as f:
        asset_config = json.load(f)

    all_tp = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
    all_sl = [0.75, 1.0, 1.25, 1.5, 2.0, 2.5]

    combo_strategies = defaultdict(list)
    for s in portfolio:
        sym = MT5_TO_INTERNAL.get(s["sym"], s["sym"])
        combo_strategies[(sym, s["magic_time"], s["duration"])].append(s)

    combo_cache = {}
    for (sym, ts, dur) in combo_strategies:
        cfg = asset_config.get(sym)
        if not cfg:
            continue
        try:
            df = loader.load_data(sym, "M15")
            df = DataEnricher.enrich_with_rsi(df)
            df = DataEnricher.enrich_with_daily_context(df, cfg["pd_start"], cfg["pd_end"])
            df = DataEnricher.enrich_with_opening_range(df, ts, dur)
            po = df.filter((pl.col("is_post_or") == True) & (pl.col("is_active_session") == True))
            da = df.group_by("trade_date").agg(pl.col("or_atr_ratio").first())
            vd = da.filter(pl.col("or_atr_ratio").is_between(ATR_RATIO_LOW, ATR_RATIO_HIGH)).select("trade_date")
            po = po.join(vd, on="trade_date", how="inner")

            cc = []
            for c in ["rsi_at_or_close", "rsi_daily_14", "atr_change", "atr_percentile",
                       "or_position_vs_pd", "or_open_vs_pd_close", "or_open", "pd_or_high", "pd_or_low"]:
                if c in df.columns:
                    cc.append(pl.col(c).first().alias(c))
            dc = None
            if cc:
                dc = df.group_by("trade_date").agg(cc)
                dc = dc.with_columns(pl.col("trade_date").cast(pl.Date).dt.weekday().alias("day_of_week"))
                if "or_width" in po.columns:
                    ow = po.group_by("trade_date").agg(pl.col("or_width").first())
                    q25 = ow.select(pl.col("or_width").quantile(0.25)).item()
                    q75 = ow.select(pl.col("or_width").quantile(0.75)).item()
                    if q25 is not None and q75 is not None:
                        dc = dc.join(ow, on="trade_date", how="left")
                        dc = dc.with_columns([
                            (pl.col("or_width") <= q25).alias("or_width_q1"),
                            (pl.col("or_width") >= q75).alias("or_width_q4"),
                        ])
            combo_cache[(sym, ts, dur)] = (po, dc)
        except Exception as e:
            print(f"  ERR {sym}: {e}")

    multi_cache = {}
    for (sym, ts, dur), (po, dc) in combo_cache.items():
        for d in ["UP", "DOWN"]:
            mdf = track_multi_level(po, d, all_tp, all_sl)
            if dc is not None:
                ccols = [c for c in dc.columns if c != "trade_date"]
                mdf = mdf.join(dc.select(["trade_date"] + ccols), on="trade_date", how="left")
            multi_cache[(sym, ts, dur, d)] = mdf

    return multi_cache


def build_trades(portfolio, mc_cache, allocator, tp_override=None, sl_override=None):
    all_t = []
    strat_stats = {}
    for s in portfolio:
        sym = MT5_TO_INTERNAL.get(s["sym"], s["sym"])
        direction = s["edge"].split("_")[-1]
        ctx_filter = resolve_context_filter(s.get("context"))
        friction = FRICTION_INDEX if sym in INDEX_SYMBOLS else FRICTION_FX
        risk_pct = allocator.get_risk_percent(s["win_rate"])
        h, m_ = map(int, s["magic_time"].split(":"))
        exec_mins = h * 60 + m_ + s["duration"]
        label = f"{sym}|{s['session']}|{s['edge']}|{s['duration']}m|{s.get('context') or 'BASE'}"

        tp = tp_override if tp_override is not None else s["tp_mult"]
        sl = sl_override if sl_override is not None else s["sl_mult"]

        mdf = mc_cache.get((sym, s["magic_time"], s["duration"], direction))
        if mdf is None or mdf.height == 0:
            continue
        filt = mdf
        if ctx_filter:
            filt = StrategyScanner.apply_context_filter(filt, ctx_filter)
        r = eval_rr(filt, direction, tp, sl, friction)
        if r["trades"] == 0:
            continue

        strat_stats[label] = {
            "trades": r["trades"], "wins": r["wins"], "wr": r["wr"],
            "net_r": r["net_r"], "tp": tp, "sl": sl, "risk_pct": risk_pct,
        }

        for d, p in zip(r["dates"], r["pnls"]):
            all_t.append({
                "date": d, "symbol": sym, "pnl_r": p,
                "risk_pct": risk_pct, "exec_mins": exec_mins, "label": label,
            })
    return all_t, strat_stats


def sim_portfolio(trades, bal=20000.0):
    trades.sort(key=lambda x: (x["date"], x["exec_mins"]))
    seen = set()
    deduped = []
    for t in trades:
        k = (t["date"], t["symbol"])
        if k not in seen:
            seen.add(k)
            deduped.append(t)

    b = bal
    pk = bal
    mdd = 0
    pnls = []
    yearly = defaultdict(lambda: {"trades": 0, "wins": 0, "pnl_usd": 0.0, "pnl_r": 0.0})

    for t in deduped:
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

    n = len(deduped)
    w = sum(1 for p in pnls if p > 0)
    gp = sum(p for p in pnls if p > 0)
    gl = abs(sum(p for p in pnls if p < 0))
    dates = [t["date"] for t in deduped]

    return {
        "balance": b, "pnl": b - bal, "trades": n, "wins": w,
        "wr": w / n if n > 0 else 0,
        "pf": gp / gl if gl > 0 else 99,
        "net_r": sum(pnls), "max_dd": mdd,
        "yearly": dict(yearly), "pnls": pnls, "dates": dates,
    }


def main():
    with open(f"{ROOT}/src/execution/bot_config.json") as f:
        bot_config = json.load(f)

    portfolio = bot_config["portfolio"]
    risk_cfg = bot_config["risk_scaling"]
    allocator = DynamicRiskAllocator(**risk_cfg)

    print(f"=== Comparacion: Global TP=0.5 SL=2.5 vs Individual R:R ===")
    print(f"  {len(portfolio)} estrategias\n")

    print("Cargando datos...")
    mc_cache = load_data(portfolio)

    # A) Global TP=0.5 SL=2.5
    print("A) Global TP=0.5 SL=2.5...")
    trades_a, stats_a = build_trades(portfolio, mc_cache, allocator, tp_override=0.5, sl_override=2.5)
    res_a = sim_portfolio(trades_a)

    # B) Individual
    print("B) Individual R:R...")
    trades_b, stats_b = build_trades(portfolio, mc_cache, allocator)
    res_b = sim_portfolio(trades_b)

    # MC + WF + Decay
    mc_a = StatisticalValidator.monte_carlo(res_a["pnls"], 10000)
    mc_b = StatisticalValidator.monte_carlo(res_b["pnls"], 10000)
    decay_a = StatisticalValidator.decay_analysis(res_a["pnls"], res_a["dates"], 365)
    decay_b = StatisticalValidator.decay_analysis(res_b["pnls"], res_b["dates"], 365)

    mid_a = len(res_a["pnls"]) // 2
    mid_b = len(res_b["pnls"]) // 2
    wf_a_is = sum(1 for p in res_a["pnls"][:mid_a] if p > 0) / mid_a if mid_a else 0
    wf_a_oos = sum(1 for p in res_a["pnls"][mid_a:] if p > 0) / max(1, len(res_a["pnls"]) - mid_a)
    wf_b_is = sum(1 for p in res_b["pnls"][:mid_b] if p > 0) / mid_b if mid_b else 0
    wf_b_oos = sum(1 for p in res_b["pnls"][mid_b:] if p > 0) / max(1, len(res_b["pnls"]) - mid_b)

    # Print comparison
    print()
    hdr = "=" * 75
    print(hdr)
    print(f"  {'Metrica':<23} {'A) GLOBAL 0.5:2.5':>23} {'B) INDIVIDUAL':>23}")
    print(hdr)

    bal_a = f"${res_a['balance']:,.0f}"
    bal_b = f"${res_b['balance']:,.0f}"
    pnl_a = f"${res_a['pnl']:,.0f}"
    pnl_b = f"${res_b['pnl']:,.0f}"

    rows = [
        ("Balance Final", bal_a, bal_b),
        ("Ganancia", pnl_a, pnl_b),
        ("Trades", f"{res_a['trades']:,}", f"{res_b['trades']:,}"),
        ("Win Rate", f"{res_a['wr']:.1%}", f"{res_b['wr']:.1%}"),
        ("Profit Factor", f"{res_a['pf']:.2f}", f"{res_b['pf']:.2f}"),
        ("Net R", f"{res_a['net_r']:.0f}R", f"{res_b['net_r']:.0f}R"),
        ("Max Drawdown", f"{res_a['max_dd']:.1%}", f"{res_b['max_dd']:.1%}"),
        ("MC P5", f"{mc_a['pnl_p5']:.0f}R", f"{mc_b['pnl_p5']:.0f}R"),
        ("MC P50", f"{mc_a['pnl_p50']:.0f}R", f"{mc_b['pnl_p50']:.0f}R"),
        ("MC Prob Ruina", f"{mc_a['prob_ruin']:.1%}", f"{mc_b['prob_ruin']:.1%}"),
        ("WF IS WR", f"{wf_a_is:.1%}", f"{wf_b_is:.1%}"),
        ("WF OOS WR", f"{wf_a_oos:.1%}", f"{wf_b_oos:.1%}"),
        ("Decay Score", f"{decay_a.get('decay_score', 0):.2f}", f"{decay_b.get('decay_score', 0):.2f}"),
    ]
    for label, va, vb in rows:
        print(f"  {label:<23} {va:>23} {vb:>23}")
    print(hdr)

    # Yearly
    print()
    print(f"  {'Ano':<6} {'A Trades':>8} {'A WR':>7} {'A PnL$':>12} {'B Trades':>9} {'B WR':>7} {'B PnL$':>12}")
    print("  " + "-" * 63)
    all_yrs = sorted(set(list(res_a["yearly"].keys()) + list(res_b["yearly"].keys())))
    for yr in all_yrs:
        ya = res_a["yearly"].get(yr, {"trades": 0, "wins": 0, "pnl_usd": 0})
        yb = res_b["yearly"].get(yr, {"trades": 0, "wins": 0, "pnl_usd": 0})
        wa = ya["wins"] / ya["trades"] if ya["trades"] > 0 else 0
        wb = yb["wins"] / yb["trades"] if yb["trades"] > 0 else 0
        pnl_ya = f"${ya['pnl_usd']:,.0f}"
        pnl_yb = f"${yb['pnl_usd']:,.0f}"
        print(f"  {yr:<6} {ya['trades']:>8} {wa:>7.1%} {pnl_ya:>12} "
              f"{yb['trades']:>9} {wb:>7.1%} {pnl_yb:>12}")

    diff = res_b["pnl"] - res_a["pnl"]
    pct = diff / res_a["pnl"] * 100 if res_a["pnl"] != 0 else 0
    print()
    print(f"  Diferencia: ${diff:+,.0f} ({pct:+.1f}%)")

    # Per-strategy differences
    print()
    print("  Estrategias donde INDIVIDUAL difiere de GLOBAL:")
    diffs = []
    for label in stats_b:
        sb = stats_b[label]
        sa = stats_a.get(label, {"net_r": 0, "trades": 0})
        if sb["tp"] != 0.5 or sb["sl"] != 2.5:
            d = sb["net_r"] - sa["net_r"]
            diffs.append((label, sa["net_r"], sb["net_r"], d, sb["tp"], sb["sl"]))

    diffs.sort(key=lambda x: x[3], reverse=True)
    print(f"  {'Estrategia':<52} {'Glob NR':>8} {'Indv NR':>8} {'Diff':>7} {'TP:SL':>7}")
    print("  " + "-" * 85)
    for label, gnr, inr, d, tp, sl in diffs:
        rr = f"{tp}:{sl}"
        print(f"  {label:<52} {gnr:>8.1f} {inr:>8.1f} {d:>+7.1f} {rr:>7}")


if __name__ == "__main__":
    main()
