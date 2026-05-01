"""Optuna 3-regime search: explore both TP>SL (momentum) and TP<SL (high WR fade).

Per strategy, run 3 separate Optuna studies in distinct R:R regimes:
  REGIME_HIGH_RR   — TP>SL (momentum, low WR, big wins): TP∈[1.0,4.0], SL∈[0.3,1.5]
  REGIME_BALANCED  — TP≈SL (mixed): TP∈[0.5,2.0], SL∈[0.5,2.0]
  REGIME_HIGH_WR   — TP<SL (fade, high WR, small wins): TP∈[0.3,1.5], SL∈[1.0,4.0]

Each runs 60 trials with TPE.

Final per-strategy = best of 3 regimes by SL-invariant objective:
  score = (expectancy_R * SL * trades_per_year) / max_dd_R

Constraints same: trades/yr >= 30, WR > 0.50, PF > 1.0.
Friction: realistic per-symbol Vantage + 0.2R slippage.

Output:
  reports/optuna_3regime_results.parquet (every regime tested per strategy)
  reports/Optuna_3Regime_Final.md (best regime per strategy + comparison)
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
FADE_SETUPS = {"KALMAN_PEAK_FADE","ZSCORE_EXTREME_FADE","OLS_EXTREME_FADE",
               "CURVATURE_PEAK_FADE","GARCH_Z_FADE","AREA_EXTREME_FADE"}

optuna.logging.set_verbosity(optuna.logging.WARNING)

REGIMES = {
    'HIGH_RR':    {'tp_lo':1.0, 'tp_hi':4.0, 'sl_lo':0.3, 'sl_hi':1.5},  # TP>SL
    'BALANCED':   {'tp_lo':0.5, 'tp_hi':2.0, 'sl_lo':0.5, 'sl_hi':2.0},  # mixed
    'HIGH_WR':    {'tp_lo':0.3, 'tp_hi':1.5, 'sl_lo':1.0, 'sl_hi':4.0},  # TP<SL
}


def _flip(df: pl.DataFrame) -> pl.DataFrame:
    if len(df) == 0:
        return df
    return df.with_columns([
        pl.when(pl.col('direction')=='LONG').then(pl.lit('SHORT'))
        .otherwise(pl.lit('LONG')).alias('direction')
    ])


def _backtest(strat: dict, bars: pl.DataFrame, sigs: pl.DataFrame,
              tp: float, sl: float, median_atr: float):
    sym = strat['symbol']; ses = strat['session']; setup = strat['setup_type']
    fric_R = friction_r(sym, sl, median_atr) + 0.2
    se_h = INDICATOR_SESSIONS[ses][1]
    if setup in FADE_SETUPS:
        cfg = FadeCfg(tp_atr_mult=tp, sl_atr_mult=sl, session_end_hour_utc=se_h, friction_r=fric_R)
        trades = run_fade_bt(sigs, bars, setup, cfg, sym)
    else:
        cfg = MomCfg(tp_atr_mult=tp, sl_atr_mult=sl, session_end_hour_utc=se_h, friction_r=fric_R)
        trades = run_mom_bt(sigs, bars, setup, cfg, sym)
    return trades


def optimize_regime(strat, bars, sigs, median_atr, regime_name, regime_bounds, n_trials=60):
    def objective(trial):
        tp = round(trial.suggest_float('tp', regime_bounds['tp_lo'], regime_bounds['tp_hi'], step=0.1), 2)
        sl = round(trial.suggest_float('sl', regime_bounds['sl_lo'], regime_bounds['sl_hi'], step=0.1), 2)
        try:
            trades = _backtest(strat, bars, sigs, tp, sl, median_atr)
        except Exception:
            return -1.0
        if len(trades) < 30:
            return -1.0
        m = compute_metrics(trades)
        if m.trades_per_year < 30 or m.wr < 0.50 or m.profit_factor < 1.0:
            return -1.0
        atr_per_trade = float(m.expectancy_r) * sl
        annual_atr = atr_per_trade * float(m.trades_per_year)
        dd_pen = max(float(m.max_dd_r), 1.0)
        return annual_atr / dd_pen

    study = optuna.create_study(direction='maximize',
                                sampler=optuna.samplers.TPESampler(seed=42))
    study.optimize(objective, n_trials=n_trials, show_progress_bar=False)
    if study.best_value <= 0:
        return None
    tp = study.best_params['tp']; sl = study.best_params['sl']
    trades = _backtest(strat, bars, sigs, tp, sl, median_atr)
    m = compute_metrics(trades)
    return {
        'regime': regime_name,
        'tp': float(tp), 'sl': float(sl),
        'rr_ratio': round(tp/sl, 2),
        'n': m.n_trades, 'wr': m.wr, 'pf': m.profit_factor,
        'exp_r': m.expectancy_r, 'net_r': float(trades['r_multiple'].sum()),
        'dd_r': m.max_dd_r, 'tpy': m.trades_per_year,
        'objective_score': float(study.best_value),
    }


def main():
    portfolio = pl.read_parquet(REPORTS_DIR / "math_realfriction_portfolio.parquet")
    print(f"3-regime Optuna on {len(portfolio)} strategies "
          f"({len(REGIMES)} regimes x 60 trials each = {3 * 60 * len(portfolio)} total trials)\n")

    bar_cache = {}; sig_cache = {}
    all_rows = []; best_rows = []
    t0 = time.time()

    for i, strat in enumerate(portfolio.iter_rows(named=True), 1):
        sym = strat['symbol']; setup = strat['setup_type']
        direction = strat['direction_mode']; ses = strat['session']
        try:
            if sym not in bar_cache:
                bar_cache[sym] = _load_and_enrich_math(sym)
            bars = bar_cache[sym]
            ck = (sym, setup, direction)
            if ck not in sig_cache:
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
                continue
            median_atr = load_median_atr(sym)

            results_per_regime = []
            for regime_name, bounds in REGIMES.items():
                r = optimize_regime(strat, bars, sigs, median_atr, regime_name, bounds, n_trials=60)
                if r is None:
                    continue
                r.update({'symbol': sym, 'session': ses, 'setup_type': setup,
                          'direction_mode': direction})
                all_rows.append(r)
                results_per_regime.append(r)

            if not results_per_regime:
                print(f"  [{i:02d}/{len(portfolio)}] {sym}/{ses}/{setup}/{direction}: no valid regime")
                continue

            best = max(results_per_regime, key=lambda x: x['objective_score'])
            # Also fetch metrics for OTHER regimes to show comparison
            by_regime = {r['regime']: r for r in results_per_regime}
            best_rows.append({
                'symbol': sym, 'session': ses, 'setup_type': setup, 'direction_mode': direction,
                'cur_tp': float(strat['tp_atr_mult']), 'cur_sl': float(strat['sl_atr_mult']),
                'cur_pf': float(strat.get('pf', 0.0)), 'cur_wr': float(strat.get('wr', 0.0)),
                'cur_exp': float(strat.get('expectancy_r', 0.0)), 'cur_dd': float(strat.get('max_dd_r', 0.0)),
                'best_regime': best['regime'],
                'best_tp': best['tp'], 'best_sl': best['sl'], 'best_rr': best['rr_ratio'],
                'best_wr': best['wr'], 'best_pf': best['pf'], 'best_exp': best['exp_r'],
                'best_dd': best['dd_r'], 'best_tpy': best['tpy'], 'best_score': best['objective_score'],
                'high_rr_score': by_regime.get('HIGH_RR', {}).get('objective_score', 0),
                'balanced_score': by_regime.get('BALANCED', {}).get('objective_score', 0),
                'high_wr_score': by_regime.get('HIGH_WR', {}).get('objective_score', 0),
            })

            elapsed = (time.time()-t0)/60
            print(f"  [{i:02d}/{len(portfolio)}] {sym}/{ses}/{setup}: "
                  f"best={best['regime']} TP={best['tp']}/SL={best['sl']} (rr={best['rr_ratio']}) "
                  f"WR={best['wr']:.3f} PF={best['pf']:.2f} exp={best['exp_r']:+.3f} ({elapsed:.1f}m)")
        except Exception as e:
            print(f"  [{i:02d}/{len(portfolio)}] {sym} err: {e}")

    if not best_rows:
        print("No results")
        return

    df_all = pl.DataFrame(all_rows)
    df_best = pl.DataFrame(best_rows)
    df_all.write_parquet(REPORTS_DIR / "optuna_3regime_all.parquet")
    df_best.write_parquet(REPORTS_DIR / "optuna_3regime_results.parquet")

    # Distribution of best regime choice
    from collections import Counter
    regime_counter = Counter(r['best_regime'] for r in best_rows)
    print('\n=== BEST REGIME DISTRIBUTION ===')
    for k, n in regime_counter.most_common():
        print(f'  {k}: {n} strategies')

    # Aggregate
    print('\n=== AGGREGATE (best regime per strategy) ===')
    print(f"Avg WR : {df_best['cur_wr'].mean():.3f} -> {df_best['best_wr'].mean():.3f}")
    print(f"Avg PF : {df_best['cur_pf'].mean():.2f} -> {df_best['best_pf'].mean():.2f}")
    print(f"Avg Exp: {df_best['cur_exp'].mean():+.3f} -> {df_best['best_exp'].mean():+.3f}")
    print(f"Avg DD : {df_best['cur_dd'].mean():.2f} -> {df_best['best_dd'].mean():.2f}")
    print(f"Sum NetR base of best regime: {df_best['best_score'].sum():.1f}")

    # Markdown
    md = ["# Optuna 3-Regime Comparison", "",
          f"Per-strategy: optimized in 3 distinct R:R regimes; best chosen by SL-invariant score.",
          f"- HIGH_RR (TP>SL): TP∈[1.0,4.0], SL∈[0.3,1.5]",
          f"- BALANCED (TP≈SL): TP∈[0.5,2.0], SL∈[0.5,2.0]",
          f"- HIGH_WR (TP<SL): TP∈[0.3,1.5], SL∈[1.0,4.0]", "",
          "## Best-regime distribution",
          ""]
    for k,n in regime_counter.most_common():
        md.append(f"- **{k}**: {n} strategies")
    md += ["", "## Per-strategy best regime + comparison",
           "",
           "| Symbol | Sess | Setup | Dir | Best R | TP/SL | RR | WR | PF | Exp | DD | tpy |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(best_rows, key=lambda x: -x['best_pf']):
        md.append(
            f"| {r['symbol']} | {r['session']} | {r['setup_type']} | {r['direction_mode']} "
            f"| **{r['best_regime']}** | {r['best_tp']:.2f}/{r['best_sl']:.2f} | {r['best_rr']:.2f} "
            f"| {r['best_wr']:.3f} | {r['best_pf']:.2f} | {r['best_exp']:+.3f} "
            f"| {r['best_dd']:.1f} | {r['best_tpy']:.0f} |"
        )
    (REPORTS_DIR / "Optuna_3Regime_Final.md").write_text("\n".join(md) + "\n", encoding='utf-8')
    print(f"\nReport: reports/Optuna_3Regime_Final.md")


if __name__ == "__main__":
    main()
