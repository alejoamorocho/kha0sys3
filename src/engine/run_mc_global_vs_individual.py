"""
Monte Carlo + Walk-Forward + Decay: Global TP=0.5 SL=2.5 vs Individual R:R.
"""

import json, os, sys, numpy as np, polars as pl
from collections import defaultdict

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


def load_all():
    loader = CSVPolarsLoader(ROOT + "/data")
    with open(ROOT + "/src/infrastructure/config/asset_config.json") as f:
        ac = json.load(f)
    with open(ROOT + "/src/execution/bot_config.json") as f:
        bc = json.load(f)

    portfolio = bc["portfolio"]
    alloc = DynamicRiskAllocator(**bc["risk_scaling"])
    all_tp = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
    all_sl = [0.75, 1.0, 1.25, 1.5, 2.0, 2.5]

    combos = defaultdict(list)
    for s in portfolio:
        sym = MT5_TO_INTERNAL.get(s["sym"], s["sym"])
        combos[(sym, s["magic_time"], s["duration"])].append(s)

    ccache = {}
    for (sym, ts, dur) in combos:
        cfg = ac.get(sym)
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
            ccache[(sym, ts, dur)] = (po, dc)
        except Exception as e:
            print(f"  ERR {sym}: {e}")

    mcache = {}
    for (sym, ts, dur), (po, dc) in ccache.items():
        for d in ["UP", "DOWN"]:
            mdf = track_multi_level(po, d, all_tp, all_sl)
            if dc is not None:
                ccols = [c for c in dc.columns if c != "trade_date"]
                mdf = mdf.join(dc.select(["trade_date"] + ccols), on="trade_date", how="left")
            mcache[(sym, ts, dur, d)] = mdf

    return portfolio, alloc, mcache


def build(portfolio, mcache, alloc, tp_ov=None, sl_ov=None):
    out = []
    for s in portfolio:
        sym = MT5_TO_INTERNAL.get(s["sym"], s["sym"])
        d = s["edge"].split("_")[-1]
        cf = resolve_context_filter(s.get("context"))
        fr = FRICTION_INDEX if sym in INDEX_SYMBOLS else FRICTION_FX
        rp = alloc.get_risk_percent(s["win_rate"])
        h, m_ = map(int, s["magic_time"].split(":"))
        em = h * 60 + m_ + s["duration"]
        tp = tp_ov if tp_ov is not None else s["tp_mult"]
        sl = sl_ov if sl_ov is not None else s["sl_mult"]
        mdf = mcache.get((sym, s["magic_time"], s["duration"], d))
        if mdf is None or mdf.height == 0:
            continue
        f = mdf
        if cf:
            f = StrategyScanner.apply_context_filter(f, cf)
        r = eval_rr(f, d, tp, sl, fr)
        for dt, p in zip(r["dates"], r["pnls"]):
            out.append({"date": dt, "symbol": sym, "pnl_r": p, "risk_pct": rp, "exec_mins": em})
    return out


def dedup_sim(trades, bal=20000.0):
    trades.sort(key=lambda x: (x["date"], x["exec_mins"]))
    seen = set()
    dd = []
    for t in trades:
        k = (t["date"], t["symbol"])
        if k not in seen:
            seen.add(k)
            dd.append(t)
    b = bal
    pk = bal
    mdd = 0
    pnls = []
    dates = []
    yearly = defaultdict(lambda: {"trades": 0, "wins": 0, "pnl_usd": 0.0})
    for t in dd:
        ra = bal * t["risk_pct"]
        dp = t["pnl_r"] * ra
        b += dp
        pk = max(pk, b)
        d = (b - pk) / pk if pk > 0 else 0
        mdd = min(mdd, d)
        pnls.append(t["pnl_r"])
        dates.append(t["date"])
        yr = t["date"][:4]
        yearly[yr]["trades"] += 1
        yearly[yr]["pnl_usd"] += dp
        if t["pnl_r"] > 0:
            yearly[yr]["wins"] += 1
    n = len(dd)
    w = sum(1 for p in pnls if p > 0)
    gp = sum(p for p in pnls if p > 0)
    gl = abs(sum(p for p in pnls if p < 0))
    return {
        "balance": b, "pnl": b - bal, "trades": n, "wins": w,
        "wr": w / n if n > 0 else 0, "pf": gp / gl if gl > 0 else 99,
        "net_r": sum(pnls), "max_dd": mdd, "yearly": dict(yearly),
        "pnls": pnls, "dates": dates,
    }


def wf_stats(pnls):
    m = len(pnls) // 2
    tr, te = pnls[:m], pnls[m:]
    wr_tr = sum(1 for p in tr if p > 0) / len(tr) if tr else 0
    wr_te = sum(1 for p in te if p > 0) / len(te) if te else 0
    gp_tr = sum(p for p in tr if p > 0)
    gl_tr = abs(sum(p for p in tr if p < 0))
    gp_te = sum(p for p in te if p > 0)
    gl_te = abs(sum(p for p in te if p < 0))
    return {
        "wr_tr": wr_tr, "wr_te": wr_te,
        "nr_tr": sum(tr), "nr_te": sum(te),
        "pf_tr": gp_tr / gl_tr if gl_tr > 0 else 99,
        "pf_te": gp_te / gl_te if gl_te > 0 else 99,
    }


def p(label, va, vb):
    print(f"  {label:<25} {va:>26} {vb:>24}")


def main():
    portfolio, alloc, mcache = load_all()

    print("Building Global TP=0.5 SL=2.5...")
    tg = build(portfolio, mcache, alloc, tp_ov=0.5, sl_ov=2.5)
    rg = dedup_sim(tg)

    print("Building Individual R:R...")
    ti = build(portfolio, mcache, alloc)
    ri = dedup_sim(ti)

    print("Monte Carlo 10k x2...")
    mcg = StatisticalValidator.monte_carlo(rg["pnls"], 10000)
    mci = StatisticalValidator.monte_carlo(ri["pnls"], 10000)

    wfg = wf_stats(rg["pnls"])
    wfi = wf_stats(ri["pnls"])

    dg = StatisticalValidator.decay_analysis(rg["pnls"], rg["dates"], 365)
    di = StatisticalValidator.decay_analysis(ri["pnls"], ri["dates"], 365)

    avg_rg = np.mean([20000 * t["risk_pct"] for t in tg[:rg["trades"]]])
    avg_ri = np.mean([20000 * t["risk_pct"] for t in ti[:ri["trades"]]])

    sep = "=" * 78
    print()
    print(sep)
    print("  COMPARACION COMPLETA: GLOBAL vs INDIVIDUAL R:R")
    print(sep)

    print()
    print("  --- PORTFOLIO ---")
    p("Metrica", "A) GLOBAL 0.5:2.5", "B) INDIVIDUAL")
    print("  " + "-" * 75)
    p("Balance Final", f"${rg['balance']:,.0f}", f"${ri['balance']:,.0f}")
    p("Ganancia", f"${rg['pnl']:,.0f}", f"${ri['pnl']:,.0f}")
    p("Trades", f"{rg['trades']:,}", f"{ri['trades']:,}")
    p("Win Rate", f"{rg['wr']:.1%}", f"{ri['wr']:.1%}")
    p("Profit Factor", f"{rg['pf']:.2f}", f"{ri['pf']:.2f}")
    p("Net R", f"{rg['net_r']:.0f}R", f"{ri['net_r']:.0f}R")
    p("Max Drawdown", f"{rg['max_dd']:.1%}", f"{ri['max_dd']:.1%}")

    print()
    print("  --- MONTE CARLO (10,000 sims) ---")
    p("Metrica", "A) GLOBAL 0.5:2.5", "B) INDIVIDUAL")
    print("  " + "-" * 75)
    p("P5 (peor caso)", f"{mcg['pnl_p5']:.0f}R (${mcg['pnl_p5']*avg_rg:,.0f})",
      f"{mci['pnl_p5']:.0f}R (${mci['pnl_p5']*avg_ri:,.0f})")
    p("P25", f"{mcg['pnl_p25']:.0f}R", f"{mci['pnl_p25']:.0f}R")
    p("P50 (mediana)", f"{mcg['pnl_p50']:.0f}R (${mcg['pnl_p50']*avg_rg:,.0f})",
      f"{mci['pnl_p50']:.0f}R (${mci['pnl_p50']*avg_ri:,.0f})")
    p("P75", f"{mcg['pnl_p75']:.0f}R", f"{mci['pnl_p75']:.0f}R")
    p("P95 (mejor caso)", f"{mcg['pnl_p95']:.0f}R (${mcg['pnl_p95']*avg_rg:,.0f})",
      f"{mci['pnl_p95']:.0f}R (${mci['pnl_p95']*avg_ri:,.0f})")
    p("Prob Ruina", f"{mcg['prob_ruin']:.1%}", f"{mci['prob_ruin']:.1%}")
    p("Prob Profit", f"{mcg['prob_profit']:.1%}", f"{mci['prob_profit']:.1%}")
    p("DD P5 (peor DD)", f"{mcg['dd_p5']:.0f}R", f"{mci['dd_p5']:.0f}R")
    p("DD P50 (DD tipico)", f"{mcg['dd_p50']:.0f}R", f"{mci['dd_p50']:.0f}R")

    print()
    print("  --- WALK-FORWARD (50/50) ---")
    p("Metrica", "A) GLOBAL 0.5:2.5", "B) INDIVIDUAL")
    print("  " + "-" * 75)
    p("IS Win Rate", f"{wfg['wr_tr']:.1%}", f"{wfi['wr_tr']:.1%}")
    p("OOS Win Rate", f"{wfg['wr_te']:.1%}", f"{wfi['wr_te']:.1%}")
    p("Degradacion WR", f"{max(0, wfg['wr_tr']-wfg['wr_te']):.1%}",
      f"{max(0, wfi['wr_tr']-wfi['wr_te']):.1%}")
    p("IS Net R", f"{wfg['nr_tr']:.0f}R", f"{wfi['nr_tr']:.0f}R")
    p("OOS Net R", f"{wfg['nr_te']:.0f}R", f"{wfi['nr_te']:.0f}R")
    p("IS Profit Factor", f"{wfg['pf_tr']:.2f}", f"{wfi['pf_tr']:.2f}")
    p("OOS Profit Factor", f"{wfg['pf_te']:.2f}", f"{wfi['pf_te']:.2f}")

    print()
    print("  --- DECAY ANALYSIS ---")
    p("Metrica", "A) GLOBAL 0.5:2.5", "B) INDIVIDUAL")
    print("  " + "-" * 75)
    p("Decay Score", f"{dg.get('decay_score', 0):.2f}", f"{di.get('decay_score', 0):.2f}")
    p("Tendencia", dg.get("trend", "?"), di.get("trend", "?"))

    if dg.get("windows") and di.get("windows"):
        print()
        print("  Ventanas anuales:")
        hdr = f"  {'Periodo':<28} {'A WR':>6} {'A Exp':>7} {'A PnL':>7} {'B WR':>6} {'B Exp':>7} {'B PnL':>7}"
        print(hdr)
        print("  " + "-" * 72)
        maxw = min(len(dg["windows"]), len(di["windows"]))
        for i in range(maxw):
            wg = dg["windows"][i]
            wi = di["windows"][i]
            print(f"  {wg['period']:<28} {wg['wr']:>6.1%} {wg['expectancy']:>7.4f} {wg['pnl']:>7.0f} "
                  f"{wi['wr']:>6.1%} {wi['expectancy']:>7.4f} {wi['pnl']:>7.0f}")

    print()
    print(sep)
    diff = ri["pnl"] - rg["pnl"]
    pct = diff / rg["pnl"] * 100 if rg["pnl"] > 0 else 0
    print(f"  VEREDICTO:")
    print(f"    Individual R:R: +${diff:,.0f} ({pct:+.1f}%) vs Global")
    print(f"    Drawdown: {ri['max_dd']:.1%} vs {rg['max_dd']:.1%}")
    print(f"    MC Ruina: {mci['prob_ruin']:.1%} vs {mcg['prob_ruin']:.1%}")
    print(f"    MC P50:   {mci['pnl_p50']:.0f}R vs {mcg['pnl_p50']:.0f}R")
    print(f"    WF OOS:   {wfi['wr_te']:.1%} vs {wfg['wr_te']:.1%}")
    print(sep)


if __name__ == "__main__":
    main()
