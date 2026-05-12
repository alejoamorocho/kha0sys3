"""K3 universe + signal at any TF + M1 management for ALL.

Universe: 15 symbols (FX + metals + indices + commodities, K3 deploy).
Setups: 6 (OLS, HURST, KALMAN, SPECTRAL, KAMA, VELOCITY).
Signal TFs: M1, M15, H1, H4 (each generates signals from its own enriched bars).
Management: ALWAYS on M1 (walk minute-by-minute, SL-first conservative).
Friction: K3 LIGHT (0.05R FX, 0.10R non-FX) — matches K3-97 deploy for direct
comparison.

Pipeline:
  Phase A: full grid scan
  Phase B: filter (PF >= 1.2, WR >= 0.50, trades/yr threshold by TF)
  Phase C: dedup overlap (best per (sym, setup, signal_tf, sess, dir))

Outputs:
  reports/K3M1_phase_a.parquet
  reports/K3M1_phase_b.parquet
  reports/K3M1_FINAL.md
"""
from __future__ import annotations

import gc
import time
from collections import Counter
from datetime import datetime, time as dtime, timedelta
from pathlib import Path

import numpy as np
import polars as pl

from src.domain.constants import INDICATOR_SESSIONS
from src.engine.indicator_validation import compute_metrics
from src.engine.run_math_momentum import (
    detect_setups as detect_mom, _guard_indicator_col,
    BacktestConfig as MomCfg, WAIT_BARS as MOM_WAIT_BARS,
)
from src.engine.run_indicator_discovery import _filter_by_session
from src.engine.friction_real import friction_r as real_friction_r, load_median_atr

REPORTS = Path("reports")
TF_CACHE_DIR = Path("C:/Proyectos/kha0sys3/data/enriched_math_tf")

# CRITICAL: Polars datetime[μs] cast to Int64 returns microseconds since epoch
# treating naive datetimes as UTC. Python's datetime.timestamp() on naive
# datetimes treats them as LOCAL TIME. To stay consistent (treat all naive
# datetimes as UTC), use this helper:
from datetime import timezone as _tz
def _to_us_utc(dt) -> int:
    """Convert naive datetime to microseconds since epoch, treating as UTC."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=_tz.utc)
    return int(dt.timestamp() * 1_000_000)

# K3 universe
SYMBOLS = [
    "AUDUSD", "BRENT", "EURJPY", "EURUSD", "GBPAUD",
    "GBPJPY", "GBPUSD", "NASDAQ100", "NATGAS", "SP500",
    "USDJPY", "WTI", "XAGUSD", "XAUUSD",
    # EURAUD only has M1, handled separately
]
# K3 setups
SETUPS = [
    "OLS_SLOPE_STRONG", "HURST_TREND_MOM",
    "KALMAN_INNOV_EXPAND", "SPECTRAL_TREND_MOM",
    "KAMA_CROSS_MOM", "VELOCITY_ACCEL_GO",
]
SIGNAL_TFS = ["M1", "M15", "H1", "H4"]
SESSIONS = list(INDICATOR_SESSIONS.keys())
DIRECTIONS = ["NORMAL", "INVERT"]

# Grids (trimmed for tractability)
TP_GRID = [0.5, 1.0, 1.5, 2.0]
SL_GRID = [0.5, 1.0, 1.5]

# Filter gates per signal TF (frequency expectations differ)
PB_MIN_TPY_BY_TF = {"M1": 200, "M15": 50, "H1": 15, "H4": 5}
PB_MIN_WR = 0.50
PB_MIN_PF = 1.20
PB_MIN_EXP = 0.05

# REAL Vantage friction model (per-symbol commission + spread + slippage)
# Replaces the K3-light 0.05/0.10R which was unrealistically optimistic.
# Friction is computed PER STRATEGY at the strategy's sl_atr_mult level using
# friction_real.friction_r() + 0.2R slippage.
NON_FX = {"BRENT", "WTI", "NATGAS", "NASDAQ100", "SP500", "XAGUSD", "XAUUSD"}

# Max horizon (in MINUTES) to keep a trade alive after entry.
# No premature same-day session_end truncation — let TP/SL play out.
# Cap is generous: 10x the signal-TF bar duration.
MAX_HOLD_MULT = 10  # 10 H4 bars = 40h, 10 H1 = 10h, 10 M15 = 2.5h, 10 M1 = 10min


def _flip(df: pl.DataFrame) -> pl.DataFrame:
    if len(df) == 0: return df
    return df.with_columns([
        pl.when(pl.col("direction") == "LONG").then(pl.lit("SHORT"))
          .otherwise(pl.lit("LONG")).alias("direction")
    ])


def realistic_friction(sym: str, sl_mult: float, median_atr: float) -> float:
    """Realistic Vantage friction per symbol + 0.2R slippage."""
    return real_friction_r(sym, sl_mult, median_atr) + 0.2


def load_tf(sym: str, tf: str) -> pl.DataFrame | None:
    p = TF_CACHE_DIR / f"{sym}_{tf}.parquet"
    if not p.exists(): return None
    return pl.read_parquet(p)


def _backtest_m1m_mgmt(setups: pl.DataFrame, m1_arr: np.ndarray, m1_times_us: np.ndarray,
                      m1_guard: np.ndarray, cfg: MomCfg, setup_type: str,
                      signal_tf_min: int) -> pl.DataFrame:
    """Universal backtest: signals from any TF, fill+exit walked on M1.
    Args:
        setups: signal DataFrame from detect_setups() at signal TF
        m1_arr: M1 OHLC array (Nx4: open, high, low, close)
        m1_times_us: M1 timestamps in microseconds
        m1_guard: M1 guard indicator values (aligned with m1_arr)
        cfg: BacktestConfig
        setup_type: e.g. OLS_SLOPE_STRONG
        signal_tf_min: minutes per bar at signal TF (1, 15, 60, 240)
    """
    if len(setups) == 0:
        return _empty()
    # Dedup 1/day
    setups = setups.with_columns(pl.col("time").dt.date().alias("_date")) \
        .sort("time").unique(subset=["_date"], keep="first").drop("_date")

    results = []
    # Wait window for STOP fill: ~5 bars of signal TF = 5 * tf_min minutes
    wait_minutes = MOM_WAIT_BARS * signal_tf_min
    wait_us = wait_minutes * 60 * 1_000_000

    for s in setups.iter_rows(named=True):
        atr = s["atr_14"]
        if atr is None or atr <= 0:
            continue
        direction = s["direction"]
        stop_price = s["stop_price"]
        g0 = s["guard_value"]
        if g0 is None or stop_price is None:
            continue
        sig_us = _to_us_utc(s["time"])
        # Signal bar ends at sig_us + signal_tf_min
        bar_end_us = sig_us + signal_tf_min * 60 * 1_000_000
        # Wait window: from bar_end to bar_end + wait_us
        wait_start = int(np.searchsorted(m1_times_us, bar_end_us, side="left"))
        wait_end = int(np.searchsorted(m1_times_us, bar_end_us + wait_us, side="right"))
        if wait_start >= len(m1_arr) or wait_start >= wait_end:
            continue

        g0_sign = 1.0 if g0 > 0 else (-1.0 if g0 < 0 else 0.0)
        weaken_thresh = 0.5 * abs(g0)

        # Find fill on M1 within wait window
        fill_idx = None; cancelled = False
        for i in range(wait_start, wait_end):
            gv = m1_guard[i] if i < len(m1_guard) else np.nan
            if not np.isnan(gv) and g0_sign != 0 and gv * g0_sign < weaken_thresh:
                cancelled = True; break
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

        # MAX HOLD horizon: entry_time + MAX_HOLD_MULT × signal_tf_min.
        # No same-day session_end truncation. Trade runs until TP/SL or horizon.
        entry_time_us = m1_times_us[fill_idx]
        max_hold_us = MAX_HOLD_MULT * signal_tf_min * 60 * 1_000_000
        horizon_us = entry_time_us + max_hold_us

        scan_start = fill_idx + 1
        scan_end = int(np.searchsorted(m1_times_us, horizon_us, side="right"))
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
            exit_price = sl if sl_hit[first] else tp  # SL-first conservative
        else:
            exit_price = float(m1_cl[-1])

        risk = cfg.sl_atr_mult * atr
        pnl = (exit_price - entry) if direction == "LONG" else (entry - exit_price)
        r = (pnl / risk - cfg.friction_r) if risk > 0 else 0
        results.append({"time": s["time"], "r_multiple": float(r),
                        "direction": direction})
    return pl.DataFrame(results) if results else _empty()


def _empty():
    return pl.DataFrame({"time": [], "direction": [], "r_multiple": []},
                        schema={"time": pl.Datetime, "direction": pl.Utf8, "r_multiple": pl.Float64})


def _align_guard_to_m1(m1_times_us: np.ndarray, signal_bars: pl.DataFrame,
                      guard_col: str, signal_tf_min: int) -> np.ndarray:
    """Build an M1-length array of guard values by forward-filling from signal TF bars.
    Each signal-TF bar holds for signal_tf_min minutes."""
    if guard_col not in signal_bars.columns:
        return np.full(len(m1_times_us), np.nan)
    sb = signal_bars.sort("time")
    sig_times_us = sb["time"].cast(pl.Int64).to_numpy()
    sig_guards = sb[guard_col].to_numpy()
    # For each M1 time, find latest signal time <= it
    idx = np.searchsorted(sig_times_us, m1_times_us, side="right") - 1
    idx = np.clip(idx, 0, len(sig_guards) - 1)
    out = sig_guards[idx]
    # Where m1_times < first signal bar, mark NaN
    out = np.where(np.searchsorted(sig_times_us, m1_times_us, side="right") == 0,
                   np.nan, out)
    return out


def _signal_tf_minutes(tf: str) -> int:
    return {"M1": 1, "M15": 15, "H1": 60, "H4": 240}[tf]


def phase_a():
    print(f"=== Phase A — K3 universe + M1 mgmt ===")
    total = (len(SYMBOLS) * len(SETUPS) * len(SIGNAL_TFS) *
             len(SESSIONS) * len(DIRECTIONS) * len(TP_GRID) * len(SL_GRID))
    print(f"Symbols: {len(SYMBOLS)} | Setups: {len(SETUPS)} | "
          f"Signal TFs: {len(SIGNAL_TFS)} | Sessions: {len(SESSIONS)} | "
          f"Dirs: {len(DIRECTIONS)} | Total combos: {total}")
    rows = []
    t0 = time.time()
    for sym_i, sym in enumerate(SYMBOLS, 1):
        print(f"\n[{sym_i}/{len(SYMBOLS)}] {sym}: loading M1+M15+H1+H4 ({time.time()-t0:.0f}s)...")
        m1 = load_tf(sym, "M1")
        if m1 is None:
            print(f"  SKIP {sym}: no M1 cache"); continue
        m1_arr = m1.select(["open","high","low","close"]).to_numpy()
        m1_times = m1["time"].cast(pl.Int64).to_numpy()
        tf_bars = {"M1": m1}
        for tf in ["M15","H1","H4"]:
            b = load_tf(sym, tf)
            if b is not None: tf_bars[tf] = b

        median_atr = load_median_atr(sym)
        kept_sym = 0
        for setup in SETUPS:
            guard_col = _guard_indicator_col(setup)
            # Pre-compute M1-aligned guard for each signal TF
            guard_by_tf = {}
            for tf, bars in tf_bars.items():
                if guard_col in bars.columns:
                    if tf == "M1":
                        guard_by_tf[tf] = bars[guard_col].to_numpy()
                    else:
                        guard_by_tf[tf] = _align_guard_to_m1(m1_times, bars, guard_col,
                                                            _signal_tf_minutes(tf))
            for tf in SIGNAL_TFS:
                if tf not in tf_bars: continue
                bars = tf_bars[tf]
                if guard_col not in bars.columns: continue
                m1_guard = guard_by_tf[tf]
                # Generate signals once per (setup, tf)
                try:
                    raw = detect_mom(bars, setup)
                except Exception:
                    continue
                tf_min = _signal_tf_minutes(tf)
                for direction in DIRECTIONS:
                    sigs_dir = _flip(raw) if direction == "INVERT" else raw
                    for sess in SESSIONS:
                        sigs = _filter_by_session(sigs_dir, sess)
                        if len(sigs) < 50:
                            continue
                        se_h = INDICATOR_SESSIONS[sess][1]
                        for tp in TP_GRID:
                            for sl in SL_GRID:
                                fric_R = realistic_friction(sym, sl, median_atr)
                                cfg = MomCfg(tp_atr_mult=tp, sl_atr_mult=sl,
                                             session_end_hour_utc=se_h, friction_r=fric_R)
                                try:
                                    trades = _backtest_m1m_mgmt(sigs, m1_arr, m1_times,
                                                                m1_guard, cfg, setup, tf_min)
                                except Exception:
                                    continue
                                if len(trades) < 30: continue
                                m = compute_metrics(trades)
                                rows.append({
                                    "symbol": sym, "setup_type": setup, "signal_tf": tf,
                                    "session": sess, "direction_mode": direction,
                                    "tp": tp, "sl": sl, "rr": tp/sl,
                                    "n": m.n_trades, "wr": m.wr,
                                    "pf": m.profit_factor, "exp_r": m.expectancy_r,
                                    "max_dd_r": m.max_dd_r, "tpy": m.trades_per_year,
                                    "friction_r": round(fric_R, 4),
                                })
                                kept_sym += 1
        print(f"  {sym}: {kept_sym} survivors | total cumulative: {len(rows)} | "
              f"elapsed {(time.time()-t0)/60:.1f}m")
        del m1, m1_arr, m1_times, tf_bars
        gc.collect()
    if not rows:
        print("Phase A empty"); return pl.DataFrame()
    df = pl.DataFrame(rows)
    df.write_parquet(REPORTS / "k3m1_phase_a.parquet")
    print(f"\nPhase A: {len(df)} survivors")
    return df


def phase_b(pa: pl.DataFrame) -> pl.DataFrame:
    print(f"\n=== Phase B filter ===")
    df = pa.with_columns(
        pl.when(pl.col("signal_tf") == "M1").then(float(PB_MIN_TPY_BY_TF["M1"]))
          .when(pl.col("signal_tf") == "M15").then(float(PB_MIN_TPY_BY_TF["M15"]))
          .when(pl.col("signal_tf") == "H1").then(float(PB_MIN_TPY_BY_TF["H1"]))
          .when(pl.col("signal_tf") == "H4").then(float(PB_MIN_TPY_BY_TF["H4"]))
          .otherwise(99999.0).alias("_tpy_gate")
    ).filter(
        (pl.col("tpy") >= pl.col("_tpy_gate")) &
        (pl.col("wr") >= PB_MIN_WR) &
        (pl.col("pf") >= PB_MIN_PF) &
        (pl.col("exp_r") >= PB_MIN_EXP)
    ).drop("_tpy_gate")

    # Per (sym, setup, signal_tf, sess, dir), keep best by score
    df = df.with_columns(
        (pl.col("pf") * pl.col("exp_r")).alias("score")
    ).sort("score", descending=True).group_by(
        ["symbol", "setup_type", "signal_tf", "session", "direction_mode"]
    ).agg(pl.all().first()).drop("score")
    df.write_parquet(REPORTS / "k3m1_phase_b.parquet")
    print(f"Phase B: {len(df)} unique survivors")
    return df


def main():
    REPORTS.mkdir(parents=True, exist_ok=True)
    pa = phase_a()
    if len(pa) == 0: return
    pb = phase_b(pa)
    if len(pb) == 0: print("Phase B empty"); return

    # Aggregate report
    print(f"\n=== AGGREGATE Phase B ({len(pb)}) ===")
    print(f"Avg WR: {pb['wr'].mean()*100:.1f}%")
    print(f"Avg PF: {pb['pf'].mean():.2f}")
    print(f"Avg Exp R: {pb['exp_r'].mean():+.3f}")
    print(f"Sum trades/yr: {pb['tpy'].sum():.0f}")
    print()
    print("By signal TF:")
    print(pb.group_by("signal_tf").agg([
        pl.len().alias("n"), pl.col("wr").mean().alias("avg_wr"),
        pl.col("pf").mean().alias("avg_pf"), pl.col("tpy").sum().alias("sum_tpy"),
    ]).sort("n", descending=True))
    print()
    print("By setup:")
    print(pb.group_by("setup_type").agg([
        pl.len().alias("n"), pl.col("pf").mean().alias("avg_pf"),
        pl.col("tpy").sum().alias("sum_tpy"),
    ]).sort("n", descending=True))

    # Markdown
    md = ["# K3 Universe + M1 Management — Full Comparison",
          "",
          f"Re-tested K3-97 universe (15 syms × 6 setups) at 4 signal TFs (M1, M15, H1, H4),",
          f"all with M1 management (SL-first conservative). K3-style friction "
          f"(0.05R FX / 0.10R non-FX).",
          "", "## Phase A → Phase B funnel", "",
          f"- Phase A combos passing minimal gates: **{len(pa)}**",
          f"- Phase B unique survivors (PF≥1.20, WR≥50%, tpy threshold by TF): **{len(pb)}**",
          "", "## Aggregate Phase B", "",
          f"- Avg WR: {pb['wr'].mean()*100:.1f}%",
          f"- Avg PF: {pb['pf'].mean():.2f}",
          f"- Avg Exp R: {pb['exp_r'].mean():+.3f}",
          f"- Sum trades/yr: {pb['tpy'].sum():.0f}",
          "", "## By signal TF", "",
          "| TF | n | Avg WR | Avg PF | Sum trades/yr |",
          "|---|---|---|---|---|"]
    for r in pb.group_by("signal_tf").agg([
        pl.len().alias("n"), pl.col("wr").mean().alias("avg_wr"),
        pl.col("pf").mean().alias("avg_pf"), pl.col("tpy").sum().alias("sum_tpy"),
    ]).sort("n", descending=True).iter_rows(named=True):
        md.append(f"| **{r['signal_tf']}** | {r['n']} | {r['avg_wr']*100:.1f}% | "
                  f"{r['avg_pf']:.2f} | {r['sum_tpy']:.0f} |")
    md += ["", "## By setup", "",
           "| Setup | n | Avg PF | Sum trades/yr |", "|---|---|---|---|"]
    for r in pb.group_by("setup_type").agg([
        pl.len().alias("n"), pl.col("pf").mean().alias("avg_pf"),
        pl.col("tpy").sum().alias("sum_tpy"),
    ]).sort("n", descending=True).iter_rows(named=True):
        md.append(f"| {r['setup_type']} | {r['n']} | {r['avg_pf']:.2f} | "
                  f"{r['sum_tpy']:.0f} |")
    md += ["", "## Top 25 by PF", "",
           "| # | TF | Symbol | Setup | Session | Dir | TP/SL | n | WR | PF | Exp R | tpy |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(pb.sort("pf", descending=True).head(25).iter_rows(named=True), 1):
        md.append(f"| {i} | {r['signal_tf']} | {r['symbol']} | {r['setup_type']} | "
                  f"{r['session']} | {r['direction_mode']} | "
                  f"{r['tp']:.1f}/{r['sl']:.1f} | {r['n']} | {r['wr']*100:.1f}% | "
                  f"{r['pf']:.2f} | {r['exp_r']:+.3f} | {r['tpy']:.0f} |")
    (REPORTS / "K3_M1Mgmt_FINAL.md").write_text("\n".join(md), encoding="utf-8")
    print(f"\nReport: reports/K3_M1Mgmt_FINAL.md")


if __name__ == "__main__":
    main()
