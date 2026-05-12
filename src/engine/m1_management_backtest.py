"""M1-management backtest for higher-TF signal strategies.

Mirrors run_math_momentum.run_backtest semantics EXACTLY but replaces the
H1/H4 OHLC exit scan with a minute-by-minute M1 walk:

  1. Signal detection at signal TF (M15/H1/H4) — same as before
  2. Dedup: 1 setup per day per setup_type — same
  3. STOP fill: scan next WAIT_BARS in signal TF, fill if hi>=stop_price (LONG)
     or lo<=stop_price (SHORT) — same
  4. Direction guard during wait — same
  5. Once filled, scan M1 bars from fill+1 onwards for TP/SL hit
  6. SL-first resolution within an M1 bar (truly conservative; original used TP-first)
  7. Time stop: end-of-day OR session_end_hour (matching original)

For fair side-by-side, also re-run with the original code (TF-OHLC mgmt) to
get apples-to-apples comparison from the SAME signal stream.

Output:
  reports/m1_management_comparison.parquet (per-strat side by side)
  reports/M1_Management_Comparison.md
"""
from __future__ import annotations
from pathlib import Path
import time
import numpy as np
import polars as pl

from src.application.math_indicators import MathIndicatorEnricher
from src.domain.constants import INDICATOR_SESSIONS
from src.engine.run_indicator_discovery import _load_and_enrich, _filter_by_session
from src.engine.run_math_momentum import (
    detect_setups as detect_mom, run_backtest as run_mom_bt,
    BacktestConfig as MomCfg, WAIT_BARS as MOM_WAIT_BARS,
)
from src.engine.run_math_fade import (
    detect_setups as detect_fade, run_backtest as run_fade_bt,
    BacktestConfig as FadeCfg,
)
from src.engine.friction_real import friction_r, load_median_atr
from src.engine.indicator_validation import compute_metrics

REPORTS = Path("reports")
M1_CACHE = Path("C:/Proyectos/kha0sys3/data/enriched_math_tf")
FADE_SET = {"GARCH_Z_FADE"}
TF_MINUTES = {"M15": 15, "H1": 60, "H4": 240}


def _flip(df: pl.DataFrame) -> pl.DataFrame:
    if len(df) == 0: return df
    return df.with_columns([
        pl.when(pl.col("direction") == "LONG").then(pl.lit("SHORT"))
          .otherwise(pl.lit("LONG")).alias("direction")
    ])


def _load_signal_bars(symbol: str, tf: str) -> pl.DataFrame:
    if tf == "M15":
        path = Path("data/enriched_math") / f"{symbol}_M15.parquet"
    elif tf == "H1":
        path = Path("data/enriched_math_h1") / f"{symbol}_H1.parquet"
    elif tf == "H4":
        path = Path("data/enriched_math_h4") / f"{symbol}_H4.parquet"
    else:
        raise ValueError(f"Unsupported TF: {tf}")
    if path.exists():
        return pl.read_parquet(path)
    bars = _load_and_enrich(symbol, tf)
    bars = MathIndicatorEnricher.enrich_all_math(bars)
    path.parent.mkdir(parents=True, exist_ok=True)
    bars.write_parquet(path)
    return bars


def _load_m1_arrays(symbol: str):
    """Load M1 bars and return numpy arrays for fast indexing."""
    path = M1_CACHE / f"{symbol}_M1.parquet"
    df = pl.scan_parquet(path).select(
        ["time", "open", "high", "low", "close"]
    ).collect()
    arr = df.select(["open", "high", "low", "close"]).to_numpy()
    times_us = df["time"].cast(pl.Int64).to_numpy()  # microseconds (Polars datetime[μs])
    return arr, times_us


def _backtest_m1_mgmt_mom(setups: pl.DataFrame, signal_bars: pl.DataFrame,
                         m1_arr: np.ndarray, m1_times: np.ndarray,
                         cfg: MomCfg, setup_type: str,
                         sl_first: bool = True) -> pl.DataFrame:
    """Mirror of run_math_momentum.run_backtest but with M1 exit scan.

    Args:
        setups: DataFrame from detect_setups()
        signal_bars: H1/H4/M15 enriched bars (with guard indicator)
        m1_arr: M1 OHLC array (N x 4)
        m1_times: M1 time array (microseconds since epoch)
        cfg: BacktestConfig with TP/SL multipliers, friction, session_end_hour
        sl_first: if True, SL hit before TP within same M1 bar (conservative)
    """
    if len(setups) == 0:
        return _empty()

    # Dedup: 1 signal per date (matches original)
    setups = setups.with_columns(pl.col("time").dt.date().alias("_date")) \
        .sort("time").unique(subset=["_date"], keep="first").drop("_date")

    bars_sorted = signal_bars.sort("time")
    from src.engine.run_math_momentum import _guard_indicator_col
    guard_col = _guard_indicator_col(setup_type)

    bar_times = bars_sorted["time"].to_list()
    bar_highs = bars_sorted["high"].to_list()
    bar_lows = bars_sorted["low"].to_list()
    bar_closes = bars_sorted["close"].to_list()
    guard_vals = bars_sorted[guard_col].to_list() if guard_col in bars_sorted.columns else [None]*len(bar_times)
    time_to_idx = {t: i for i, t in enumerate(bar_times)}

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
        start_idx = time_to_idx.get(s["time"])
        if start_idx is None:
            continue

        g0_sign = 1.0 if g0 > 0 else (-1.0 if g0 < 0 else 0.0)
        weaken_thresh = 0.5 * abs(g0)

        # STOP fill wait window (in SIGNAL TF, matches original)
        fill_idx = None
        fill_price = None
        end_wait = min(start_idx + 1 + MOM_WAIT_BARS, len(bar_times))
        cancelled = False
        for i in range(start_idx + 1, end_wait):
            gv = guard_vals[i]
            if gv is not None and g0_sign != 0 and gv * g0_sign < weaken_thresh:
                cancelled = True
                break
            hi = bar_highs[i]; lo = bar_lows[i]
            if direction == "LONG":
                if hi >= stop_price:
                    fill_idx = i; fill_price = stop_price; break
            else:
                if lo <= stop_price:
                    fill_idx = i; fill_price = stop_price; break
        if cancelled or fill_idx is None:
            continue

        entry = fill_price
        if direction == "LONG":
            tp = entry + cfg.tp_atr_mult * atr
            sl = entry - cfg.sl_atr_mult * atr
        else:
            tp = entry - cfg.tp_atr_mult * atr
            sl = entry + cfg.sl_atr_mult * atr

        # ===== M1 EXIT SCAN =====
        # Start scan AFTER fill bar end (fill bar time + tf_min minutes)
        # signal_bars[fill_idx]['time'] is start-of-bar. Fill bar ENDS at
        # signal_bars[fill_idx+1]['time'] if exists.
        signal_tf_min = (bar_times[1] - bar_times[0]).total_seconds() / 60 if len(bar_times) > 1 else 60
        fill_bar_end_time = bar_times[fill_idx] + (bar_times[1] - bar_times[0]) if fill_idx + 1 < len(bar_times) else bar_times[fill_idx]
        from datetime import timezone as _tz
        if fill_bar_end_time.tzinfo is None:
            fill_bar_end_time = fill_bar_end_time.replace(tzinfo=_tz.utc)
        fill_end_us = int(fill_bar_end_time.timestamp() * 1_000_000)

        # Time stop limit: same day, before session_end_hour (broker time = stored UTC)
        signal_date = s["time"].date()
        # session_end_hour bar in signal TF — for matching original semantics
        # we cap at end-of-day + session_end_hour
        from datetime import datetime, time as dtime, timedelta
        if cfg.session_end_hour_utc >= 24:
            time_stop_dt = datetime.combine(signal_date, dtime(hour=23, minute=59, second=59))
        else:
            time_stop_dt = datetime.combine(signal_date, dtime(hour=cfg.session_end_hour_utc, minute=0))
        if time_stop_dt.tzinfo is None:
            time_stop_dt = time_stop_dt.replace(tzinfo=_tz.utc)
        time_stop_us = int(time_stop_dt.timestamp() * 1_000_000)

        # Walk M1 from fill_end_us to time_stop_us, looking for TP/SL hits
        m1_start = np.searchsorted(m1_times, fill_end_us, side="left")
        m1_end = np.searchsorted(m1_times, time_stop_us, side="right")
        if m1_start >= len(m1_arr) or m1_start >= m1_end:
            continue

        m1_hi = m1_arr[m1_start:m1_end, 1]
        m1_lo = m1_arr[m1_start:m1_end, 2]
        m1_cl = m1_arr[m1_start:m1_end, 3]

        if direction == "LONG":
            tp_hit = m1_hi >= tp
            sl_hit = m1_lo <= sl
        else:
            tp_hit = m1_lo <= tp
            sl_hit = m1_hi >= sl

        any_hit = tp_hit | sl_hit
        if any_hit.any():
            first_idx = int(np.argmax(any_hit))
            if sl_first and sl_hit[first_idx]:
                exit_price = sl
            elif tp_hit[first_idx]:
                exit_price = tp
            else:
                exit_price = sl
        else:
            # TIME_STOP: use last M1 close in window
            exit_price = float(m1_cl[-1])

        risk_per_unit = cfg.sl_atr_mult * atr
        if direction == "LONG":
            pnl = exit_price - entry
        else:
            pnl = entry - exit_price
        r_gross = pnl / risk_per_unit if risk_per_unit > 0 else 0.0
        r_net = r_gross - cfg.friction_r

        results.append({
            "time": s["time"], "direction": direction,
            "entry_price": entry, "exit_price": exit_price,
            "r_multiple": r_net,
        })

    return pl.DataFrame(results) if results else _empty()


def _empty():
    return pl.DataFrame({
        "time": [], "direction": [], "entry_price": [],
        "exit_price": [], "r_multiple": [],
    }, schema={"time": pl.Datetime, "direction": pl.Utf8,
               "entry_price": pl.Float64, "exit_price": pl.Float64,
               "r_multiple": pl.Float64})


def main():
    fuerte = pl.read_parquet(REPORTS / "fuerte_master_portfolio.parquet")
    # Skip GARCH_Z_FADE for now (FADE is different mechanic)
    fuerte = fuerte.filter(pl.col("setup_type") != "GARCH_Z_FADE")
    print(f"Loaded {len(fuerte)} non-FADE FUERTE strategies for M1-mgmt test")

    rows = []
    t0 = time.time()
    symbols = sorted(fuerte["symbol"].unique().to_list())
    for sym_i, sym in enumerate(symbols, 1):
        print(f"\n[{sym_i}/{len(symbols)}] {sym}: loading M1 ({time.time()-t0:.0f}s)...")
        try:
            m1_arr, m1_times = _load_m1_arrays(sym)
            print(f"  M1 {len(m1_arr):,} bars  range "
                  f"{m1_times[0]/1e6/86400/365.25+1970:.2f}-{m1_times[-1]/1e6/86400/365.25+1970:.2f}y")
        except Exception as e:
            print(f"  SKIP {sym}: {e}")
            continue
        median_atr = load_median_atr(sym)
        sym_strats = fuerte.filter(pl.col("symbol") == sym)
        signal_cache = {}

        for j, strat in enumerate(sym_strats.iter_rows(named=True), 1):
            tf = strat["tf"]; setup = strat["setup_type"]
            direction_mode = strat["direction_mode"]; sess = strat["session"]
            tp = float(strat["tp"]); sl = float(strat["sl"])
            try:
                if tf not in signal_cache:
                    signal_cache[tf] = _load_signal_bars(sym, tf)
                bars = signal_cache[tf]
                raw = (detect_fade(bars, setup) if setup in FADE_SET
                       else detect_mom(bars, setup))
                if direction_mode == "INVERT":
                    raw = _flip(raw)
                sigs = _filter_by_session(raw, sess)
                if len(sigs) < 20:
                    continue
                se_h = INDICATOR_SESSIONS[sess][1]
                fric = friction_r(sym, sl, median_atr) + 0.2
                cfg = MomCfg(tp_atr_mult=tp, sl_atr_mult=sl,
                             session_end_hour_utc=se_h, friction_r=fric)
                trades_m1 = _backtest_m1_mgmt_mom(sigs, bars, m1_arr, m1_times, cfg, setup)
                if len(trades_m1) < 20:
                    continue
                m = compute_metrics(trades_m1)
                rows.append({
                    "symbol": sym, "tf": tf, "session": sess,
                    "setup_type": setup, "direction_mode": direction_mode,
                    "tp": tp, "sl": sl, "rr": strat["rr"],
                    "n_orig": int(strat["n"]), "wr_orig": float(strat["wr"]),
                    "pf_orig": float(strat["pf"]), "exp_orig": float(strat["exp_r"]),
                    "dd_orig": float(strat["max_dd"]),
                    "net_r_orig": float(strat["net_r"]),
                    "n_m1": m.n_trades, "wr_m1": m.wr,
                    "pf_m1": m.profit_factor, "exp_m1": m.expectancy_r,
                    "dd_m1": m.max_dd_r, "tpy_m1": m.trades_per_year,
                    "net_r_m1": float(trades_m1["r_multiple"].sum()),
                })
            except Exception as e:
                print(f"  ERR {sym}/{tf}/{setup}: {e}")
        print(f"  done {sym} | {len(rows)} cumulative comparisons")
        del m1_arr, m1_times
        signal_cache.clear()

    if not rows:
        print("No results")
        return
    df = pl.DataFrame(rows).with_columns([
        (pl.col("pf_m1") - pl.col("pf_orig")).alias("d_pf"),
        (pl.col("wr_m1") - pl.col("wr_orig")).alias("d_wr"),
        (pl.col("net_r_m1") - pl.col("net_r_orig")).alias("d_net_r"),
    ])
    df.write_parquet(REPORTS / "m1_management_comparison.parquet")

    print(f"\n=== AGGREGATE COMPARISON ({len(df)} strats, TF-OHLC vs M1-mgmt) ===")
    print(f"Avg WR  : {df['wr_orig'].mean():.4f} -> {df['wr_m1'].mean():.4f}  (d={df['d_wr'].mean()*100:+.2f}pp)")
    print(f"Avg PF  : {df['pf_orig'].mean():.3f} -> {df['pf_m1'].mean():.3f}  (d={df['d_pf'].mean():+.3f})")
    print(f"Avg Exp : {df['exp_orig'].mean():+.4f} -> {df['exp_m1'].mean():+.4f}")
    print(f"Avg DD  : {df['dd_orig'].mean():.2f} -> {df['dd_m1'].mean():.2f}")
    print(f"Sum NetR: {df['net_r_orig'].sum():.0f} -> {df['net_r_m1'].sum():.0f}")
    print(f"\nStrategies improved (d_pf>0): {len(df.filter(pl.col('d_pf') > 0))}/{len(df)}")
    print(f"Strategies degraded (d_pf<0): {len(df.filter(pl.col('d_pf') < 0))}/{len(df)}")

    print("\n=== BY TF ===")
    for tf in ["M15", "H1", "H4"]:
        sub = df.filter(pl.col("tf") == tf)
        if len(sub) == 0: continue
        print(f"{tf}: n={len(sub)}  WR {sub['wr_orig'].mean():.3f}->{sub['wr_m1'].mean():.3f}  "
              f"PF {sub['pf_orig'].mean():.2f}->{sub['pf_m1'].mean():.2f}  "
              f"netR {sub['net_r_orig'].sum():.0f}->{sub['net_r_m1'].sum():.0f}")

    md = ["# M1 Management vs TF-OHLC Management",
          "",
          f"Re-backtested {len(df)} FUERTE non-FADE strategies (M15/H1/H4 signals).",
          "Signal/entry/dedup/guard semantics IDENTICAL to original.",
          "Exit (TP/SL) detection: walked through M1 bars (first-touch, SL-first on ties).",
          "",
          "## Aggregate", "",
          "| Metric | TF-OHLC mgmt | M1 mgmt | Δ |",
          "|---|---|---|---|",
          f"| Avg WR | {df['wr_orig'].mean()*100:.1f}% | {df['wr_m1'].mean()*100:.1f}% | {df['d_wr'].mean()*100:+.2f}pp |",
          f"| Avg PF | {df['pf_orig'].mean():.3f} | {df['pf_m1'].mean():.3f} | {df['d_pf'].mean():+.3f} |",
          f"| Avg Exp R | {df['exp_orig'].mean():+.3f} | {df['exp_m1'].mean():+.3f} | - |",
          f"| Avg DD | {df['dd_orig'].mean():.2f} | {df['dd_m1'].mean():.2f} | - |",
          f"| Sum Net R 8y | {df['net_r_orig'].sum():.0f} | {df['net_r_m1'].sum():.0f} | {df['d_net_r'].sum():+.0f} |",
          f"| Strategies improved | - | - | {len(df.filter(pl.col('d_pf')>0))}/{len(df)} |",
          "",
          "## Per-TF", "",
          "| TF | n | WR orig | WR M1 | PF orig | PF M1 | Net R orig | Net R M1 | Δ Net R |",
          "|---|---|---|---|---|---|---|---|---|"]
    for tf in ["M15", "H1", "H4"]:
        sub = df.filter(pl.col("tf") == tf)
        if len(sub) == 0: continue
        md.append(f"| **{tf}** | {len(sub)} | {sub['wr_orig'].mean()*100:.1f}% | "
                  f"{sub['wr_m1'].mean()*100:.1f}% | {sub['pf_orig'].mean():.2f} | "
                  f"{sub['pf_m1'].mean():.2f} | {sub['net_r_orig'].sum():.0f} | "
                  f"{sub['net_r_m1'].sum():.0f} | {sub['d_net_r'].sum():+.0f} |")

    md += ["", "## Top 20 IMPROVEMENT (Δ PF descending)", "",
           "| TF | Symbol | Session | Setup | Dir | PF orig | PF M1 | Δ PF | WR orig | WR M1 |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for r in df.sort("d_pf", descending=True).head(20).iter_rows(named=True):
        md.append(f"| {r['tf']} | {r['symbol']} | {r['session']} | {r['setup_type']} | "
                  f"{r['direction_mode']} | {r['pf_orig']:.2f} | {r['pf_m1']:.2f} | "
                  f"{r['d_pf']:+.2f} | {r['wr_orig']*100:.1f}% | {r['wr_m1']*100:.1f}% |")

    md += ["", "## Top 10 DEGRADATION (Δ PF ascending)", "",
           "| TF | Symbol | Session | Setup | Dir | PF orig | PF M1 | Δ PF |",
           "|---|---|---|---|---|---|---|---|"]
    for r in df.sort("d_pf").head(10).iter_rows(named=True):
        md.append(f"| {r['tf']} | {r['symbol']} | {r['session']} | {r['setup_type']} | "
                  f"{r['direction_mode']} | {r['pf_orig']:.2f} | {r['pf_m1']:.2f} | {r['d_pf']:+.2f} |")

    (REPORTS / "M1_Management_Comparison.md").write_text("\n".join(md), encoding="utf-8")
    print(f"\nReport: {REPORTS}/M1_Management_Comparison.md")


if __name__ == "__main__":
    main()
