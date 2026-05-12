"""M1 signal + M1 management full discovery pipeline.

Uses the same math setups (OLS_SLOPE_STRONG, HURST_TREND_MOM,
KALMAN_INNOV_EXPAND, SPECTRAL_TREND_MOM) but on M1 bars for BOTH:
  - Signal generation (math indicators computed on M1 bars in enriched_math_tf)
  - Exit management (TP/SL walked minute-by-minute on the same M1 bars)

Pipeline:
  Phase A: full grid (9 syms × 4 setups × 5 sessions × NORMAL/INVERT × TP × SL)
  Phase B: filter (trades/yr ≥ 100, WR > 0.50, PF > 1.0)
  Phase C: 3-regime Optuna per survivor
  Phase D: robustness (MC + WF + decay)

Friction: realistic Vantage + 0.2R slippage (same as other pipelines).
Wait window: 5 M1 bars (5 min) for STOP fill (matches M15 5-bar wait scaled).

Outputs:
  reports/Math_M1_Phase_A.md / .parquet
  reports/Math_M1_Phase_B.md / .parquet
  reports/Math_M1_Optuna.md / .parquet
  reports/Math_M1_Robustness.md / .parquet
"""
from __future__ import annotations

import time
from collections import Counter
from pathlib import Path

import numpy as np
import optuna
import polars as pl

from src.domain.constants import INDICATOR_SESSIONS
from src.engine.indicator_validation import compute_metrics
from src.engine.run_math_momentum import (
    detect_setups as detect_mom, _guard_indicator_col,
    BacktestConfig as MomCfg, WAIT_BARS as MOM_WAIT_BARS,
)
from src.engine.run_indicator_discovery import _filter_by_session
from src.engine.friction_real import friction_r, load_median_atr

REPORTS = Path("reports")
M1_CACHE = Path("C:/Proyectos/kha0sys3/data/enriched_math_tf")
TF = "M1"
TF_MIN = 1

SYMBOLS = ["AUDUSD", "EURJPY", "EURUSD", "GBPAUD", "GBPJPY",
           "GBPUSD", "USDJPY", "XAGUSD", "XAUUSD"]
SETUPS = ["OLS_SLOPE_STRONG", "HURST_TREND_MOM",
          "KALMAN_INNOV_EXPAND", "SPECTRAL_TREND_MOM"]
SESSIONS = list(INDICATOR_SESSIONS.keys())
DIRECTIONS = ["NORMAL", "INVERT"]

# Phase A grid (tight to be tractable on M1)
TP_GRID_A = [0.5, 1.0, 1.5, 2.0]
SL_GRID_A = [0.5, 1.0, 1.5]

# Phase B filter
PB_MIN_TPY = 100
PB_MIN_WR = 0.50
PB_MIN_PF = 1.0
PB_MIN_EXP = 0.02

# Optuna
N_TRIALS_PER_REGIME = 40
SEED = 42
REGIMES = {
    "HIGH_RR":  {"tp_lo": 1.0, "tp_hi": 4.0, "sl_lo": 0.3, "sl_hi": 1.5},
    "BALANCED": {"tp_lo": 0.5, "tp_hi": 2.0, "sl_lo": 0.5, "sl_hi": 2.0},
    "HIGH_WR":  {"tp_lo": 0.3, "tp_hi": 1.5, "sl_lo": 1.0, "sl_hi": 4.0},
}

optuna.logging.set_verbosity(optuna.logging.WARNING)


def _flip(df: pl.DataFrame) -> pl.DataFrame:
    if len(df) == 0: return df
    return df.with_columns([
        pl.when(pl.col("direction") == "LONG").then(pl.lit("SHORT"))
          .otherwise(pl.lit("LONG")).alias("direction")
    ])


def _load_m1(symbol: str) -> pl.DataFrame:
    """Load enriched M1 bars (3M rows × 41 cols, ~700MB on disk)."""
    return pl.read_parquet(M1_CACHE / f"{symbol}_M1.parquet")


def _backtest_m1m1(setups: pl.DataFrame, m1: pl.DataFrame,
                   m1_arr: np.ndarray, m1_times: np.ndarray,
                   cfg: MomCfg, setup_type: str) -> pl.DataFrame:
    """Backtest with M1 signal + M1 mgmt. Mirror of run_math_momentum semantics
    but everything happens on M1 bars; exit scan walks minute by minute."""
    if len(setups) == 0:
        return _empty()
    # Dedup 1/day
    setups = setups.with_columns(pl.col("time").dt.date().alias("_date")) \
        .sort("time").unique(subset=["_date"], keep="first").drop("_date")
    if len(setups) == 0:
        return _empty()

    guard_col = _guard_indicator_col(setup_type)
    if guard_col not in m1.columns:
        return _empty()

    # Build index: time -> row in m1
    m1_sorted = m1.sort("time")
    bar_times_us = m1_sorted["time"].cast(pl.Int64).to_numpy()

    # m1_arr cols: 0=open, 1=high, 2=low, 3=close
    # We also need guard values at each row
    guard_vals = m1_sorted[guard_col].to_numpy()

    results = []
    for s in setups.iter_rows(named=True):
        atr = s["atr_14"]
        if atr is None or atr <= 0:
            continue
        direction = s["direction"]
        stop_price = s["stop_price"]
        g0 = s["guard_value"]
        if g0 is None or stop_price is None:
            continue
        sig_us = int(s["time"].timestamp() * 1_000_000)
        start_idx = int(np.searchsorted(bar_times_us, sig_us, side="left"))
        if start_idx >= len(m1_arr):
            continue

        g0_sign = 1.0 if g0 > 0 else (-1.0 if g0 < 0 else 0.0)
        weaken_thresh = 0.5 * abs(g0)

        # STOP fill wait window (5 M1 bars)
        end_wait = min(start_idx + 1 + MOM_WAIT_BARS, len(m1_arr))
        fill_idx = None
        cancelled = False
        for i in range(start_idx + 1, end_wait):
            gv = guard_vals[i]
            if not np.isnan(gv) and g0_sign != 0 and gv * g0_sign < weaken_thresh:
                cancelled = True
                break
            hi, lo = m1_arr[i, 1], m1_arr[i, 2]
            if direction == "LONG":
                if hi >= stop_price:
                    fill_idx = i; break
            else:
                if lo <= stop_price:
                    fill_idx = i; break
        if cancelled or fill_idx is None:
            continue

        entry = stop_price
        if direction == "LONG":
            tp = entry + cfg.tp_atr_mult * atr
            sl = entry - cfg.sl_atr_mult * atr
        else:
            tp = entry - cfg.tp_atr_mult * atr
            sl = entry + cfg.sl_atr_mult * atr

        # Exit scan starts at fill_idx + 1
        # Time stop: end_of_day OR session_end_hour
        signal_date = s["time"].date()
        from datetime import datetime, time as dtime
        if cfg.session_end_hour_utc >= 24:
            ts_dt = datetime.combine(signal_date, dtime(23, 59, 59))
        else:
            ts_dt = datetime.combine(signal_date, dtime(hour=cfg.session_end_hour_utc, minute=0))
        ts_us = int(ts_dt.timestamp() * 1_000_000)

        scan_start = fill_idx + 1
        scan_end = int(np.searchsorted(bar_times_us, ts_us, side="right"))
        if scan_end <= scan_start:
            continue

        m1_hi = m1_arr[scan_start:scan_end, 1]
        m1_lo = m1_arr[scan_start:scan_end, 2]
        m1_cl = m1_arr[scan_start:scan_end, 3]
        if direction == "LONG":
            tp_hit = m1_hi >= tp
            sl_hit = m1_lo <= sl
        else:
            tp_hit = m1_lo <= tp
            sl_hit = m1_hi >= sl
        any_hit = tp_hit | sl_hit
        if any_hit.any():
            first = int(np.argmax(any_hit))
            # SL-first conservative
            if sl_hit[first]:
                exit_price = sl
            else:
                exit_price = tp
        else:
            exit_price = float(m1_cl[-1])

        risk = cfg.sl_atr_mult * atr
        if direction == "LONG":
            pnl = exit_price - entry
        else:
            pnl = entry - exit_price
        r = (pnl / risk - cfg.friction_r) if risk > 0 else 0
        results.append({
            "time": s["time"], "direction": direction,
            "r_multiple": float(r),
        })
    return pl.DataFrame(results) if results else _empty()


def _empty():
    return pl.DataFrame({"time": [], "direction": [], "r_multiple": []},
                        schema={"time": pl.Datetime, "direction": pl.Utf8, "r_multiple": pl.Float64})


def _backtest_strat(sym, setup, sess, direction_mode, tp, sl, m1, m1_arr, m1_times, median_atr):
    raw = detect_mom(m1, setup)
    if direction_mode == "INVERT":
        raw = _flip(raw)
    sigs = _filter_by_session(raw, sess)
    if len(sigs) < 100:
        return None
    se_h = INDICATOR_SESSIONS[sess][1]
    fric_R = friction_r(sym, sl, median_atr) + 0.2
    cfg = MomCfg(tp_atr_mult=tp, sl_atr_mult=sl,
                 session_end_hour_utc=se_h, friction_r=fric_R)
    trades = _backtest_m1m1(sigs, m1, m1_arr, m1_times, cfg, setup)
    if len(trades) < 30:
        return None
    m = compute_metrics(trades)
    return trades, m


# ─── Phase A ──────────────────────────────────────────────────────────

def phase_a():
    print(f"=== Phase A (M1 signal + M1 mgmt) ===")
    total = (len(SYMBOLS) * len(SETUPS) * len(SESSIONS) *
             len(DIRECTIONS) * len(TP_GRID_A) * len(SL_GRID_A))
    print(f"Total combos: {total}")
    rows = []
    t0 = time.time()
    for sym_i, sym in enumerate(SYMBOLS, 1):
        print(f"\n[{sym_i}/{len(SYMBOLS)}] {sym}: loading M1 ({time.time()-t0:.0f}s)...")
        try:
            m1 = _load_m1(sym)
        except Exception as e:
            print(f"  SKIP {sym}: {e}")
            continue
        m1_arr = m1.select(["open","high","low","close"]).to_numpy()
        m1_times = m1["time"].cast(pl.Int64).to_numpy()
        median_atr = load_median_atr(sym)
        sym_kept = 0
        for setup in SETUPS:
            for direction in DIRECTIONS:
                for sess in SESSIONS:
                    for tp in TP_GRID_A:
                        for sl in SL_GRID_A:
                            try:
                                res = _backtest_strat(sym, setup, sess, direction, tp, sl,
                                                      m1, m1_arr, m1_times, median_atr)
                                if res is None: continue
                                trades, m = res
                                rows.append({
                                    "symbol": sym, "setup_type": setup, "session": sess,
                                    "direction_mode": direction, "tp": tp, "sl": sl,
                                    "rr": tp/sl, "n": m.n_trades, "wr": m.wr,
                                    "pf": m.profit_factor, "exp_r": m.expectancy_r,
                                    "max_dd_r": m.max_dd_r, "tpy": m.trades_per_year,
                                })
                                sym_kept += 1
                            except Exception as e:
                                pass
        elapsed = (time.time()-t0)/60
        print(f"  {sym}: {sym_kept} survivors so far | {elapsed:.1f}m")
        del m1, m1_arr, m1_times
    if not rows:
        print("Phase A: no rows"); return pl.DataFrame()
    df = pl.DataFrame(rows)
    df.write_parquet(REPORTS / "math_m1_phase_a.parquet")
    print(f"\nPhase A done: {len(df)} surviving combos")
    return df


# ─── Phase B ──────────────────────────────────────────────────────────

def phase_b(pa: pl.DataFrame) -> pl.DataFrame:
    print(f"\n=== Phase B filter ===")
    df = pa.filter(
        (pl.col("tpy") >= PB_MIN_TPY) &
        (pl.col("wr") >= PB_MIN_WR) &
        (pl.col("pf") >= PB_MIN_PF) &
        (pl.col("exp_r") >= PB_MIN_EXP)
    )
    # Per (sym, setup, sess, dir), best by (pf × exp_r)
    df = df.with_columns(
        (pl.col("pf") * pl.col("exp_r")).alias("score")
    ).sort("score", descending=True).group_by(
        ["symbol","setup_type","session","direction_mode"]
    ).agg(pl.all().first()).drop("score")
    df.write_parquet(REPORTS / "math_m1_phase_b.parquet")
    print(f"Phase B: {len(df)} unique survivors")
    return df


# ─── Phase C: 3-regime Optuna ────────────────────────────────────────

def phase_c(pb: pl.DataFrame, m1_cache: dict) -> pl.DataFrame:
    print(f"\n=== Phase C: 3-regime Optuna on {len(pb)} survivors ===")

    def optimize_strat(strat, m1, m1_arr, m1_times, median_atr, regime_name, bounds):
        sym = strat["symbol"]; setup = strat["setup_type"]
        sess = strat["session"]; direction_mode = strat["direction_mode"]
        def objective(trial):
            tp = round(trial.suggest_float("tp", bounds["tp_lo"], bounds["tp_hi"], step=0.1), 2)
            sl = round(trial.suggest_float("sl", bounds["sl_lo"], bounds["sl_hi"], step=0.1), 2)
            res = _backtest_strat(sym, setup, sess, direction_mode, tp, sl, m1, m1_arr, m1_times, median_atr)
            if res is None: return -1.0
            trades, m = res
            if m.trades_per_year < PB_MIN_TPY or m.wr < 0.50 or m.profit_factor < 1.0:
                return -1.0
            atr_per_trade = float(m.expectancy_r) * sl
            annual_atr = atr_per_trade * float(m.trades_per_year)
            dd_pen = max(float(m.max_dd_r), 1.0)
            return annual_atr / dd_pen
        study = optuna.create_study(direction="maximize",
                                    sampler=optuna.samplers.TPESampler(seed=SEED))
        study.optimize(objective, n_trials=N_TRIALS_PER_REGIME, show_progress_bar=False)
        if study.best_value <= 0: return None
        tp = study.best_params["tp"]; sl = study.best_params["sl"]
        res = _backtest_strat(sym, setup, sess, direction_mode, tp, sl, m1, m1_arr, m1_times, median_atr)
        if res is None: return None
        trades, m = res
        return {"regime": regime_name, "tp": float(tp), "sl": float(sl),
                "rr": round(tp/sl,2), "n": m.n_trades, "wr": m.wr,
                "pf": m.profit_factor, "exp_r": m.expectancy_r,
                "dd_r": m.max_dd_r, "tpy": m.trades_per_year,
                "objective_score": float(study.best_value)}

    best_rows = []
    t0 = time.time()
    for i, strat in enumerate(pb.iter_rows(named=True), 1):
        sym = strat["symbol"]
        if sym not in m1_cache:
            print(f"  loading {sym} M1 for Optuna...")
            m1 = _load_m1(sym)
            m1_cache[sym] = (m1, m1.select(["open","high","low","close"]).to_numpy(),
                             m1["time"].cast(pl.Int64).to_numpy())
        m1, m1_arr, m1_times = m1_cache[sym]
        median_atr = load_median_atr(sym)
        results = []
        for rn, b in REGIMES.items():
            try:
                r = optimize_strat(strat, m1, m1_arr, m1_times, median_atr, rn, b)
                if r:
                    r.update({"symbol": sym, "setup_type": strat["setup_type"],
                              "session": strat["session"],
                              "direction_mode": strat["direction_mode"]})
                    results.append(r)
            except Exception as e:
                print(f"    {rn} err: {e}")
        if not results: continue
        best = max(results, key=lambda x: x["objective_score"])
        best_rows.append(best)
        elapsed = (time.time()-t0)/60
        print(f"  [{i:02d}/{len(pb)}] {sym}/{strat['session']}/{strat['setup_type']}/{strat['direction_mode']}: "
              f"best={best['regime']} TP={best['tp']}/SL={best['sl']} "
              f"PF={best['pf']:.2f} ({elapsed:.1f}m)")
    if not best_rows:
        return pl.DataFrame()
    df = pl.DataFrame(best_rows)
    df.write_parquet(REPORTS / "math_m1_optuna.parquet")
    print(f"\nRegime distribution: {Counter(r['regime'] for r in best_rows)}")
    return df


# ─── Phase D: robustness ────────────────────────────────────────────

MC_N = 10_000
RUIN_DD = 30.0


def mc_ruin(r, n=MC_N, ruin=RUIN_DD):
    if len(r) < 30: return {"ruin_pct": 100.0, "p5": 0.0}
    rng = np.random.default_rng(SEED)
    nets = np.empty(n); ruins = 0
    for i in range(n):
        idx = rng.permutation(len(r))
        cum = np.cumsum(r[idx])
        peak = np.maximum.accumulate(cum)
        if (peak - cum).max() >= ruin:
            ruins += 1
        nets[i] = cum[-1]
    return {"ruin_pct": 100*ruins/n, "p5": float(np.percentile(nets,5))}


def walk_forward(trades):
    if len(trades) < 40: return None
    s = trades.sort("time")
    mid = len(s)//2
    tr = compute_metrics(s[:mid]); te = compute_metrics(s[mid:])
    return {"pf_tr": tr.profit_factor, "pf_te": te.profit_factor,
            "deg_wr": (tr.wr - te.wr)/max(tr.wr,0.01)*100}


def classify(mc, wf, net_r):
    flags = []
    if mc["ruin_pct"] > 5: flags.append("ruin>5%")
    if mc["p5"] < 0: flags.append("MC P5<0")
    if wf and abs(wf["deg_wr"]) > 15: flags.append("WF deg>15%")
    if wf and wf["pf_te"] < 1.0: flags.append("PF OOS<1")
    if net_r < 0: flags.append("net-")
    if not flags and mc["ruin_pct"] < 1 and (wf is None or abs(wf["deg_wr"]) < 5):
        return "FUERTE", flags
    if mc["ruin_pct"] < 5 and mc["p5"] >= 0 and (wf is None or wf["pf_te"] >= 1.0):
        return "ACEPTABLE", flags
    if mc["ruin_pct"] > 20 or (wf and wf["pf_te"] < 0.8):
        return "MUERTA", flags
    return "DEBIL", flags


def phase_d(opt: pl.DataFrame, m1_cache: dict) -> pl.DataFrame:
    print(f"\n=== Phase D: robustness on {len(opt)} ===")
    rows = []
    for i, strat in enumerate(opt.iter_rows(named=True), 1):
        sym = strat["symbol"]
        if sym not in m1_cache:
            m1 = _load_m1(sym)
            m1_cache[sym] = (m1, m1.select(["open","high","low","close"]).to_numpy(),
                             m1["time"].cast(pl.Int64).to_numpy())
        m1, m1_arr, m1_times = m1_cache[sym]
        median_atr = load_median_atr(sym)
        res = _backtest_strat(sym, strat["setup_type"], strat["session"],
                              strat["direction_mode"], float(strat["tp"]), float(strat["sl"]),
                              m1, m1_arr, m1_times, median_atr)
        if res is None: continue
        trades, m = res
        r_arr = trades["r_multiple"].to_numpy()
        net_r = float(r_arr.sum())
        mc = mc_ruin(r_arr); wf = walk_forward(trades)
        label, flags = classify(mc, wf, net_r)
        rows.append({**dict(strat),
                     "net_r": net_r, "mc_ruin": mc["ruin_pct"], "mc_p5": mc["p5"],
                     "wf_pf_te": wf["pf_te"] if wf else None,
                     "wf_deg_wr": wf["deg_wr"] if wf else None,
                     "label": label, "flags": ",".join(flags) or "-"})
        print(f"  [{i:02d}/{len(opt)}] {sym}/{strat['session']}/{strat['setup_type']}/{strat['direction_mode']}: "
              f"{label} PF={m.profit_factor:.2f} OOS={wf['pf_te']:.2f} ruin={mc['ruin_pct']:.1f}%")
    if not rows: return pl.DataFrame()
    df = pl.DataFrame(rows)
    df.write_parquet(REPORTS / "math_m1_robustness.parquet")
    cls = Counter(r["label"] for r in rows)
    print(f"\n=== Classification: {dict(cls)} ===")
    keep = [r for r in rows if r["label"] in ("FUERTE","ACEPTABLE")]
    print(f"Keepable: {len(keep)}/{len(rows)}")
    if keep:
        print(f"  Avg WR: {np.mean([r['wr'] for r in keep])*100:.1f}%")
        print(f"  Avg PF: {np.mean([r['pf'] for r in keep]):.2f}")
        print(f"  Avg PF OOS: {np.mean([r['wf_pf_te'] for r in keep if r['wf_pf_te']]):.2f}")
        print(f"  Sum Net R: {sum(r['net_r'] for r in keep):.0f}")
    return df


def main():
    REPORTS.mkdir(parents=True, exist_ok=True)
    pa = phase_a()
    if len(pa) == 0: return
    pb = phase_b(pa)
    if len(pb) == 0: print("Phase B empty"); return
    m1_cache = {}
    opt = phase_c(pb, m1_cache)
    if len(opt) == 0: print("Optuna empty"); return
    phase_d(opt, m1_cache)


if __name__ == "__main__":
    main()
