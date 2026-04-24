"""Full-grid R:R optimization for the 6 active math setups.

Uses Polars-vectorized data loads + existing MOM inverted backtester.
For each of the 6 strategies in bot_config_math.json, sweep:
    TP ∈ {0.3, 0.4, 0.5, 0.6, 0.75, 0.9, 1.0, 1.25, 1.5}
    SL ∈ {0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0}
  = 9 * 8 = 72 combos/setup × 6 = 432 total grid evaluations.

Apply WF + MC + decay; report top-5 per setup sorted by expectancy_r.

Output:
  reports/RR_Math6_Grid.md   (per-setup best + full grid heatmap)
  reports/rr_math6_grid.parquet  (all 432 rows)
"""
from __future__ import annotations
import json
from pathlib import Path
import polars as pl

from src.domain.constants import (
    INDICATOR_SESSIONS, FRICTION_FX, FRICTION_INDEX, INDEX_SYMBOLS,
    WF_IS_MONTHS, WF_OOS_MONTHS,
)
from src.engine.indicator_validation import (
    compute_metrics, walk_forward_wr, monte_carlo_ruin, decay_slope_ratio,
)
from src.engine.run_math_momentum import detect_setups, run_backtest, BacktestConfig
from src.engine.run_math_discovery import _load_and_enrich_math
from src.engine.run_indicator_discovery import _filter_by_session

REPORTS_DIR = Path("reports")

TP_GRID = (0.3, 0.4, 0.5, 0.6, 0.75, 0.9, 1.0, 1.25, 1.5)
SL_GRID = (0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0)


def _flip(df: pl.DataFrame) -> pl.DataFrame:
    if len(df) == 0:
        return df
    return df.with_columns([
        pl.when(pl.col("direction") == "LONG").then(pl.lit("SHORT"))
        .otherwise(pl.lit("LONG")).alias("direction")
    ])


def _friction(sym: str) -> float:
    return FRICTION_INDEX if sym in INDEX_SYMBOLS else FRICTION_FX


def main():
    cfg = json.loads(Path("src/execution/bot_config_math.json").read_text(encoding="utf-8"))
    portfolio = cfg["portfolio"]
    print(f"Grid sweep: {len(portfolio)} setups x {len(TP_GRID)*len(SL_GRID)} R:R combos "
          f"= {len(portfolio) * len(TP_GRID) * len(SL_GRID)} evaluations")

    rows = []
    for i, s in enumerate(portfolio, 1):
        internal = s["internal_sym"]
        sym = s["sym"]
        session = s["session"]
        setup = s["setup_type"]
        print(f"\n[{i}/{len(portfolio)}] {internal} {session} {setup}")
        try:
            bars = _load_and_enrich_math(internal)
        except FileNotFoundError:
            print(f"  SKIP {internal}: no enriched_math cache")
            continue
        raw = detect_setups(bars, setup)
        sigs = _filter_by_session(raw, session)
        sigs_inv = _flip(sigs)
        fric = _friction(internal)
        se = INDICATOR_SESSIONS[session][1]

        for tp in TP_GRID:
            for sl in SL_GRID:
                bcfg = BacktestConfig(tp_atr_mult=tp, sl_atr_mult=sl,
                                      session_end_hour_utc=se, friction_r=fric)
                trades = run_backtest(sigs_inv, bars, setup, bcfg, internal)
                if len(trades) < 30:
                    rows.append({
                        "symbol": internal, "session": session, "setup_type": setup,
                        "tp_atr_mult": tp, "sl_atr_mult": sl,
                        "n_trades": len(trades), "wr": 0.0, "pf": 0.0,
                        "expectancy_r": 0.0, "net_r": 0.0, "max_dd_r": 0.0,
                        "wf_ratio": 0.0, "mc_ruin": 1.0, "decay_ratio": 0.0,
                        "trades_per_year": 0.0,
                    })
                    continue
                m = compute_metrics(trades)
                try:
                    wf = walk_forward_wr(trades, WF_IS_MONTHS, WF_OOS_MONTHS)
                    mc = monte_carlo_ruin(trades, risk_pct=0.02, initial_balance=10_000)
                    decay = decay_slope_ratio(trades, last_months=6)
                except Exception:
                    wf, mc, decay = 0.0, 1.0, 0.0
                rows.append({
                    "symbol": internal, "session": session, "setup_type": setup,
                    "tp_atr_mult": tp, "sl_atr_mult": sl,
                    "n_trades": m.n_trades, "wr": m.wr, "pf": m.profit_factor,
                    "expectancy_r": m.expectancy_r,
                    "net_r": float(trades["r_multiple"].sum()),
                    "max_dd_r": m.max_dd_r,
                    "wf_ratio": wf, "mc_ruin": mc, "decay_ratio": decay,
                    "trades_per_year": m.trades_per_year,
                })

    df = pl.DataFrame(rows)
    df.write_parquet(REPORTS_DIR / "rr_math6_grid.parquet")

    # Per-setup best
    print("\n" + "=" * 80)
    print("BEST R:R per setup (gate: WF>=0.80, MC<=0.02, decay>=0.60, PF>=1.2)")
    print("=" * 80)
    md = ["# R:R Grid Search — 6 Active Math Setups", "",
          f"- Grid: TP {TP_GRID} x SL {SL_GRID} = {len(TP_GRID)*len(SL_GRID)} combos per setup",
          f"- Applied: WF>=0.80 + MC<=0.02 + decay>=0.60 + PF>=1.2", ""]
    for i, s in enumerate(portfolio, 1):
        internal = s["internal_sym"]
        session = s["session"]
        setup = s["setup_type"]
        sub = df.filter(
            (pl.col("symbol") == internal) &
            (pl.col("session") == session) &
            (pl.col("setup_type") == setup) &
            (pl.col("wf_ratio") >= 0.80) &
            (pl.col("mc_ruin") <= 0.02) &
            (pl.col("decay_ratio") >= 0.60) &
            (pl.col("pf") >= 1.2)
        ).sort("expectancy_r", descending=True)
        print(f"\n[{i}] {internal} {session} {setup}  (current: TP={s['tp_atr_mult']} SL={s['sl_atr_mult']})")
        md.append(f"\n## {i}. {internal} {session} {setup}")
        md.append(f"- Current live: TP={s['tp_atr_mult']} SL={s['sl_atr_mult']} "
                  f"(expected WR={s.get('expected_wr','?')})")
        if len(sub) == 0:
            print("  NONE passed all gates in the grid")
            md.append("- **No combo passes all gates in the grid.** Keep current.")
            continue
        md.append("\n| TP | SL | N | WR | PF | Exp/R | NetR | MaxDD | WF | MC | Decay |")
        md.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for r in sub.head(5).iter_rows(named=True):
            star = " **BEST**" if r == sub.row(0, named=True) else ""
            print(f"  TP={r['tp_atr_mult']:<5} SL={r['sl_atr_mult']:<5} "
                  f"n={r['n_trades']:<5} WR={r['wr']:.3f} PF={r['pf']:.2f} "
                  f"exp={r['expectancy_r']:+.3f}R  netR={r['net_r']:+.1f}{star}")
            md.append(f"| {r['tp_atr_mult']} | {r['sl_atr_mult']} | {r['n_trades']} "
                      f"| {r['wr']:.3f} | {r['pf']:.2f} | {r['expectancy_r']:+.3f} "
                      f"| {r['net_r']:+.1f} | {r['max_dd_r']:.1f} "
                      f"| {r['wf_ratio']:.2f} | {r['mc_ruin']:.3f} | {r['decay_ratio']:.2f} |")
        best = sub.row(0, named=True)
        cur_tp, cur_sl = s["tp_atr_mult"], s["sl_atr_mult"]
        if best["tp_atr_mult"] == cur_tp and best["sl_atr_mult"] == cur_sl:
            md.append("\n**Verdict:** Current R:R is already the best in this grid.")
        else:
            md.append(f"\n**Verdict:** BEST is TP={best['tp_atr_mult']} SL={best['sl_atr_mult']} "
                      f"(currently TP={cur_tp} SL={cur_sl}). "
                      f"Net R gain: {best['net_r'] - df.filter((pl.col('symbol')==internal)&(pl.col('session')==session)&(pl.col('setup_type')==setup)&(pl.col('tp_atr_mult')==cur_tp)&(pl.col('sl_atr_mult')==cur_sl)).row(0,named=True)['net_r']:+.2f}")

    (REPORTS_DIR / "RR_Math6_Grid.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"\nSaved: reports/RR_Math6_Grid.md + reports/rr_math6_grid.parquet")


if __name__ == "__main__":
    main()
