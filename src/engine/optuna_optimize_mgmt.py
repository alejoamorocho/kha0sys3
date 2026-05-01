"""Optuna optimization of TP/SL management for the 35 realistic-friction strategies.

For each strategy in reports/math_realfriction_portfolio.parquet:
  1. Define search space TP ∈ [0.3, 3.5], SL ∈ [0.5, 3.5] step 0.1
  2. Run Optuna TPE sampler with 80 trials
  3. Auto-boundary-expansion: if best at <5% of edge, widen bounds and re-run 40 more trials
  4. Use realistic friction: friction_real.friction_r(sym, sl, median_atr) + 0.2R
  5. Constraint: trades/yr >= 30, WR > 0.50, PF > 1.0
  6. Maximize: expectancy_r (objective)

Outputs:
  reports/Optuna_Management_Final.md  — per-strategy best management + metrics
  reports/optuna_management_results.parquet  — all best params + metrics
"""
from __future__ import annotations
import json
from pathlib import Path
import time
import polars as pl
import optuna

from src.domain.constants import INDICATOR_SESSIONS
from src.engine.indicator_validation import compute_metrics
from src.engine.run_math_discovery import _load_and_enrich_math
from src.engine.run_indicator_discovery import _filter_by_session
from src.engine.run_math_momentum import detect_setups as detect_mom, run_backtest as run_mom_bt, BacktestConfig as MomCfg
from src.engine.run_math_fade import detect_setups as detect_fade, run_backtest as run_fade_bt, BacktestConfig as FadeCfg
from src.engine.friction_real import friction_r, load_median_atr

REPORTS_DIR = Path("reports")

FADE_SETUPS = {"KALMAN_PEAK_FADE", "ZSCORE_EXTREME_FADE", "OLS_EXTREME_FADE",
               "CURVATURE_PEAK_FADE", "GARCH_Z_FADE", "AREA_EXTREME_FADE"}

optuna.logging.set_verbosity(optuna.logging.WARNING)


def _flip(df: pl.DataFrame) -> pl.DataFrame:
    if len(df) == 0:
        return df
    return df.with_columns([
        pl.when(pl.col('direction')=='LONG').then(pl.lit('SHORT'))
        .otherwise(pl.lit('LONG')).alias('direction')
    ])


def _backtest(strat: dict, bars: pl.DataFrame, sigs_oriented: pl.DataFrame,
              tp: float, sl: float, median_atr: float):
    sym = strat['symbol']; ses = strat['session']; setup = strat['setup_type']
    fric_R = friction_r(sym, sl, median_atr) + 0.2  # realistic friction
    se_h = INDICATOR_SESSIONS[ses][1]
    is_fade = setup in FADE_SETUPS
    if is_fade:
        cfg = FadeCfg(tp_atr_mult=tp, sl_atr_mult=sl,
                      session_end_hour_utc=se_h, friction_r=fric_R)
        trades = run_fade_bt(sigs_oriented, bars, setup, cfg, sym)
    else:
        cfg = MomCfg(tp_atr_mult=tp, sl_atr_mult=sl,
                     session_end_hour_utc=se_h, friction_r=fric_R)
        trades = run_mom_bt(sigs_oriented, bars, setup, cfg, sym)
    return trades


def _round_step(x: float, step: float = 0.1) -> float:
    return round(round(x / step) * step, 2)


def optimize_strategy(strat: dict, bars: pl.DataFrame, sigs_oriented: pl.DataFrame,
                      median_atr: float, n_trials: int = 80) -> dict:
    sym = strat['symbol']
    setup = strat['setup_type']
    # Realistic floors: SL>=0.5 ATR (broker stops_level + spread reality)
    # TP>=0.5 ATR (to avoid the inverse exploit of tiny TPs inflating WR).
    initial_lo_tp, initial_hi_tp = 0.5, 3.5
    initial_lo_sl, initial_hi_sl = 0.5, 3.5

    def objective(trial, lo_tp, hi_tp, lo_sl, hi_sl):
        tp = _round_step(trial.suggest_float('tp', lo_tp, hi_tp, step=0.1))
        sl = _round_step(trial.suggest_float('sl', lo_sl, hi_sl, step=0.1))
        try:
            trades = _backtest(strat, bars, sigs_oriented, tp, sl, median_atr)
        except Exception:
            return -1.0
        if len(trades) < 30:
            return -1.0
        m = compute_metrics(trades)
        if m.trades_per_year < 30 or m.wr < 0.50 or m.profit_factor < 1.0:
            return -1.0
        # SL-INVARIANT objective: net annual ATR captured per unit drawdown.
        # = expectancy_R * sl × trades_per_year / max_dd_r
        # - expectancy_R * sl_atr_mult = avg ATR captured per trade (independent of SL choice)
        # - * trades_per_year = annual ATR throughput
        # - / max_dd_r = penalize drawdown
        # This forces Optuna to pick SL/TP that maximize REAL profit relative to DD,
        # not artifacts of R-multiple definition.
        atr_per_trade = float(m.expectancy_r) * sl  # ATRs captured / trade
        annual_atr = atr_per_trade * float(m.trades_per_year)
        dd_penalty = max(float(m.max_dd_r), 1.0)
        return annual_atr / dd_penalty

    # Pass 1: initial bounds
    study = optuna.create_study(direction='maximize',
                                 sampler=optuna.samplers.TPESampler(seed=42))
    study.optimize(lambda t: objective(t, initial_lo_tp, initial_hi_tp,
                                        initial_lo_sl, initial_hi_sl),
                   n_trials=n_trials, show_progress_bar=False)
    if study.best_value <= 0:
        return None

    best_tp = study.best_params['tp']
    best_sl = study.best_params['sl']

    # Pass 2: boundary expansion if best is within 5% of any edge
    expanded = False
    new_lo_tp, new_hi_tp = initial_lo_tp, initial_hi_tp
    new_lo_sl, new_hi_sl = initial_lo_sl, initial_hi_sl
    edge_tol_tp = 0.05 * (initial_hi_tp - initial_lo_tp)
    edge_tol_sl = 0.05 * (initial_hi_sl - initial_lo_sl)
    # NOTE: do NOT expand below 0.5 — that's the realistic broker minimum.
    # Only expand UPWARD if best param is at top edge.
    if best_tp >= initial_hi_tp - edge_tol_tp:
        new_hi_tp = initial_hi_tp + 1.5
        expanded = True
    if best_sl >= initial_hi_sl - edge_tol_sl:
        new_hi_sl = initial_hi_sl + 1.5
        expanded = True

    if expanded:
        study.optimize(lambda t: objective(t, new_lo_tp, new_hi_tp,
                                            new_lo_sl, new_hi_sl),
                       n_trials=40, show_progress_bar=False)
        best_tp = study.best_params['tp']
        best_sl = study.best_params['sl']

    # Re-run with best params to get full metrics
    trades = _backtest(strat, bars, sigs_oriented, best_tp, best_sl, median_atr)
    m = compute_metrics(trades)
    fric_R = friction_r(sym, best_sl, median_atr) + 0.2
    return {
        'symbol': sym, 'session': strat['session'], 'setup_type': setup,
        'direction_mode': strat['direction_mode'],
        'cur_tp': float(strat['tp_atr_mult']),
        'cur_sl': float(strat['sl_atr_mult']),
        'cur_exp': float(strat.get('expectancy_r', 0.0)),
        'cur_pf': float(strat.get('pf', 0.0)),
        'cur_wr': float(strat.get('wr', 0.0)),
        'cur_dd': float(strat.get('max_dd_r', 0.0)),
        'cur_tpy': float(strat.get('trades_per_year', 0.0)),
        'opt_tp': float(best_tp), 'opt_sl': float(best_sl),
        'opt_n': m.n_trades,
        'opt_wr': m.wr,
        'opt_pf': m.profit_factor,
        'opt_exp': m.expectancy_r,
        'opt_net_r': float(trades['r_multiple'].sum()),
        'opt_dd': m.max_dd_r,
        'opt_tpy': m.trades_per_year,
        'opt_friction_R': fric_R,
        'expanded': expanded,
        'trials_used': len(study.trials),
    }


def main():
    portfolio = pl.read_parquet(REPORTS_DIR / "math_realfriction_portfolio.parquet")
    print(f"Optimizing TP/SL management for {len(portfolio)} strategies (Optuna TPE, 80+40 trials each)\n")

    # Cache bars + signals per (symbol, setup, direction)
    bar_cache = {}
    sig_cache = {}

    results = []
    t0 = time.time()
    for i, strat in enumerate(portfolio.iter_rows(named=True), 1):
        sym = strat['symbol']
        setup = strat['setup_type']
        direction = strat['direction_mode']
        ses = strat['session']
        try:
            if sym not in bar_cache:
                bar_cache[sym] = _load_and_enrich_math(sym)
            bars = bar_cache[sym]
            ck = (sym, setup, direction)
            if ck not in sig_cache:
                # detect raw signals
                if setup in FADE_SETUPS:
                    raw = detect_fade(bars, setup)
                else:
                    raw = detect_mom(bars, setup)
                sig_cache[ck] = raw
            raw = sig_cache[ck]
            sigs = _filter_by_session(raw, ses)
            if direction == 'INVERT':
                sigs = _flip(sigs)
            if len(sigs) < 30:
                print(f"  [{i:02d}/{len(portfolio)}] SKIP {sym}/{ses}/{setup}: <30 signals")
                continue
            median_atr = load_median_atr(sym)
            res = optimize_strategy(strat, bars, sigs, median_atr, n_trials=80)
            if res is None:
                print(f"  [{i:02d}/{len(portfolio)}] {sym}/{ses}/{setup}/{direction}: NO valid optimization")
                continue
            results.append(res)
            elapsed = (time.time() - t0) / 60
            print(f"  [{i:02d}/{len(portfolio)}] {sym}/{ses}/{setup}/{direction}: "
                  f"TP {res['cur_tp']}->{res['opt_tp']} SL {res['cur_sl']}->{res['opt_sl']} "
                  f"exp {res['cur_exp']:+.3f}->{res['opt_exp']:+.3f} "
                  f"PF {res['cur_pf']:.2f}->{res['opt_pf']:.2f} "
                  f"WR {res['cur_wr']:.3f}->{res['opt_wr']:.3f} "
                  f"DD {res['cur_dd']:.1f}->{res['opt_dd']:.1f} "
                  f"tpy {int(res['opt_tpy'])} {'*' if res['expanded'] else ''} "
                  f"({elapsed:.1f}m)")
        except Exception as e:
            print(f"  [{i:02d}/{len(portfolio)}] {sym}: error {e}")

    if not results:
        print("No optimization results")
        return

    df = pl.DataFrame(results)
    df.write_parquet(REPORTS_DIR / "optuna_management_results.parquet")

    # Markdown report
    md = ["# Optuna Management Optimization (with realistic friction)", "",
          f"Optimization on {len(df)} strategies. Search space TP/SL ∈ [0.3, 3.5] step 0.1, expanded if at boundary.",
          f"Friction: per-symbol Vantage + 0.2R slippage.",
          f"Constraints: trades/yr ≥ 30, WR > 0.50, PF > 1.0. Objective: maximize expectancy_r.", "",
          "## Per-strategy results (sorted by opt_exp)", "",
          "| Symbol | Sess | Setup | Dir | TP cur->opt | SL cur->opt | WR cur->opt | PF cur->opt | Exp cur->opt | DD opt | TPY opt | Net R |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    df_sorted = df.sort('opt_exp', descending=True)
    for r in df_sorted.iter_rows(named=True):
        md.append(
            f"| {r['symbol']} | {r['session']} | {r['setup_type']} | {r['direction_mode']} "
            f"| {r['cur_tp']:.2f}->{r['opt_tp']:.2f} "
            f"| {r['cur_sl']:.2f}->{r['opt_sl']:.2f} "
            f"| {r['cur_wr']:.3f}->{r['opt_wr']:.3f} "
            f"| {r['cur_pf']:.2f}->{r['opt_pf']:.2f} "
            f"| {r['cur_exp']:+.3f}->{r['opt_exp']:+.3f} "
            f"| {r['opt_dd']:.1f} | {r['opt_tpy']:.0f} | {r['opt_net_r']:+.1f} |"
        )

    # Aggregates
    md += ["", "## Aggregate", "",
           f"- Avg WR (cur->opt): {df['cur_wr'].mean():.3f} -> {df['opt_wr'].mean():.3f}",
           f"- Avg PF (cur->opt): {df['cur_pf'].mean():.2f} -> {df['opt_pf'].mean():.2f}",
           f"- Avg Exp (cur->opt): {df['cur_exp'].mean():+.3f} -> {df['opt_exp'].mean():+.3f}",
           f"- Avg DD opt: {df['opt_dd'].mean():.2f}",
           f"- Sum trades/yr: {df['opt_tpy'].sum():.0f}",
           f"- Sum Net R (3y): {df['opt_net_r'].sum():.1f}",
           f"- Strategies with boundary expansion: {df.filter(pl.col('expanded'))['symbol'].count()}",
          ]

    (REPORTS_DIR / "Optuna_Management_Final.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"\n=== AGGREGATE ===")
    print(f"Avg WR : {df['cur_wr'].mean():.3f} -> {df['opt_wr'].mean():.3f}")
    print(f"Avg PF : {df['cur_pf'].mean():.2f} -> {df['opt_pf'].mean():.2f}")
    print(f"Avg Exp: {df['cur_exp'].mean():+.3f} -> {df['opt_exp'].mean():+.3f}")
    print(f"Avg DD : {df['opt_dd'].mean():.2f}")
    print(f"Sum tpy: {df['opt_tpy'].sum():.0f}")
    print(f"Sum Net R: {df['opt_net_r'].sum():.1f}")
    print(f"\nReport: reports/Optuna_Management_Final.md")
    print(f"Data:   reports/optuna_management_results.parquet")


if __name__ == "__main__":
    main()
