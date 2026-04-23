"""Dynamic indicator-driven exit management on Phase-A survivors.

Instead of fixed ATR TP/SL, this runner tests 5 exit styles that close trades
based on indicator state changes. Hard SL = 2.5*ATR is kept as catastrophe backstop.

Each exit style has explicit logic: close the trade when the ENTRY CONDITION
has been neutralized (mean-reversion signals) or when the trend momentum fades
(momentum signals). This is the key design choice — exits align with WHY we entered.

Exit styles tested:
  ATR_TRAIL_15   — trailing stop at 1.5*ATR from high-water mark. Logic:
                   hold while the move continues, exit on pullback. Best for
                   momentum/breakout signals.
  RSI_50_EXIT    — LONG: exit when RSI crosses 50 upward (was oversold,
                   now neutral); SHORT: mirror. Logic: entry was at extreme;
                   exit when price has mean-reverted to neutral zone.
  ZSCORE_ZERO    — exit when zscore_30 crosses 0. Logic: entry thesis was
                   "price far from mean → revert"; once price is AT mean,
                   reversion is complete.
  KALMAN_FLIP    — exit when kalman_innovation sign flips. Logic: entry was
                   on large innovation (price diverged from state); exit when
                   state has caught up and innovation crosses zero.
  BB_MID_TOUCH   — exit when price reaches bb_middle. Logic: classic BB
                   reversion. Entry at band extremum, exit at middle.

All styles share: hard SL = 2.5*ATR (catastrophe backstop) and time-stop at
session end (ultimate exit).

Usage:
    python -m src.engine.run_math_dynamic_mgmt
"""
from __future__ import annotations
from pathlib import Path
import polars as pl

from src.domain.constants import (
    INDICATOR_SESSIONS, FRICTION_FX, FRICTION_INDEX, INDEX_SYMBOLS,
)
from src.application.signal_generator import SignalGenerator
from src.engine.indicator_validation import compute_metrics
from src.engine.run_math_discovery import _load_and_enrich_math
from src.engine.run_indicator_discovery import _filter_by_session

REPORTS_DIR = Path("reports")

EXIT_STYLES = ("ATR_TRAIL_15", "RSI_50_EXIT", "ZSCORE_ZERO", "KALMAN_FLIP", "BB_MID_TOUCH")

HARD_SL_ATR = 2.5
TRAIL_ATR_MULT = 1.5


def _friction_for(symbol: str) -> float:
    return FRICTION_INDEX if symbol in INDEX_SYMBOLS else FRICTION_FX


def _run_dynamic_backtest(signals: pl.DataFrame, bars: pl.DataFrame,
                          exit_style: str, session_end_hour: int,
                          friction_r: float) -> pl.DataFrame:
    """Event-driven backtester with indicator-driven exits.

    For each signal:
        Entry = close of signal bar
        Hard SL = entry ± HARD_SL_ATR * atr_14
        Exit condition depends on exit_style (see below)
        Time-stop at session_end_hour (same-day)
    """
    if len(signals) == 0:
        return pl.DataFrame()

    # Dedup: one trade per (symbol, signal_type, date)
    deduped = signals.with_columns([
        pl.col("time").dt.date().alias("_date")
    ]).sort("time").unique(
        subset=["symbol", "signal_type", "_date"], keep="first"
    ).drop("_date")

    # Prepare lookup arrays
    bars_sorted = bars.sort("time")
    bt = bars_sorted["time"].to_list()
    bh = bars_sorted["high"].to_list()
    bl = bars_sorted["low"].to_list()
    bc = bars_sorted["close"].to_list()
    # Indicator series for exit rules
    rsi = bars_sorted["rsi_14"].to_list() if "rsi_14" in bars_sorted.columns else [None] * len(bt)
    zsc = bars_sorted["zscore_30"].to_list() if "zscore_30" in bars_sorted.columns else [None] * len(bt)
    kin = bars_sorted["kalman_innovation"].to_list() if "kalman_innovation" in bars_sorted.columns else [None] * len(bt)
    bbm = bars_sorted["bb_middle"].to_list() if "bb_middle" in bars_sorted.columns else [None] * len(bt)

    time_to_idx = {t: i for i, t in enumerate(bt)}
    results = []

    for sig in deduped.iter_rows(named=True):
        if sig["atr_14"] is None:
            continue
        entry = sig["close"]
        atr = sig["atr_14"]
        direction = sig["direction"]
        is_long = direction == "LONG"
        hard_sl = entry - HARD_SL_ATR * atr if is_long else entry + HARD_SL_ATR * atr
        risk_per_unit = HARD_SL_ATR * atr

        start = time_to_idx.get(sig["time"])
        if start is None:
            continue

        # Trailing stop state
        hw_price = entry  # high-water mark for LONG, low-water for SHORT
        trail_stop = entry - TRAIL_ATR_MULT * atr if is_long else entry + TRAIL_ATR_MULT * atr

        exit_reason = None
        exit_price = None
        exit_time = None
        signal_date = sig["time"].date()

        for i in range(start + 1, len(bt)):
            t = bt[i]
            # Time-stop
            if t.date() > signal_date or t.hour >= session_end_hour:
                exit_reason = "TIME_STOP"
                exit_price = bc[i - 1]
                exit_time = bt[i - 1]
                break
            hi = bh[i]
            lo = bl[i]
            # Hard SL check (all styles)
            if is_long and lo <= hard_sl:
                exit_reason, exit_price, exit_time = "HARD_SL", hard_sl, t
                break
            if (not is_long) and hi >= hard_sl:
                exit_reason, exit_price, exit_time = "HARD_SL", hard_sl, t
                break

            # Style-specific exits
            if exit_style == "ATR_TRAIL_15":
                # Update trailing stop
                if is_long:
                    if hi > hw_price:
                        hw_price = hi
                        trail_stop = hw_price - TRAIL_ATR_MULT * atr
                    if lo <= trail_stop:
                        exit_reason, exit_price, exit_time = "TRAIL", trail_stop, t
                        break
                else:
                    if lo < hw_price:
                        hw_price = lo
                        trail_stop = hw_price + TRAIL_ATR_MULT * atr
                    if hi >= trail_stop:
                        exit_reason, exit_price, exit_time = "TRAIL", trail_stop, t
                        break

            elif exit_style == "RSI_50_EXIT":
                r = rsi[i]
                if r is None:
                    continue
                if is_long and r >= 50 and rsi[i-1] is not None and rsi[i-1] < 50:
                    exit_reason, exit_price, exit_time = "RSI_50", bc[i], t
                    break
                if (not is_long) and r <= 50 and rsi[i-1] is not None and rsi[i-1] > 50:
                    exit_reason, exit_price, exit_time = "RSI_50", bc[i], t
                    break

            elif exit_style == "ZSCORE_ZERO":
                z = zsc[i]
                zp = zsc[i-1] if i > 0 else None
                if z is None or zp is None:
                    continue
                # LONG entered at z<<0; exit when z crosses 0 upward
                if is_long and zp <= 0 and z > 0:
                    exit_reason, exit_price, exit_time = "ZZERO", bc[i], t
                    break
                if (not is_long) and zp >= 0 and z < 0:
                    exit_reason, exit_price, exit_time = "ZZERO", bc[i], t
                    break

            elif exit_style == "KALMAN_FLIP":
                k = kin[i]
                kp = kin[i-1] if i > 0 else None
                if k is None or kp is None:
                    continue
                # Sign flip
                if kp * k < 0:
                    exit_reason, exit_price, exit_time = "KFLIP", bc[i], t
                    break

            elif exit_style == "BB_MID_TOUCH":
                mid = bbm[i]
                if mid is None:
                    continue
                if is_long and hi >= mid:
                    exit_reason, exit_price, exit_time = "BB_MID", mid, t
                    break
                if (not is_long) and lo <= mid:
                    exit_reason, exit_price, exit_time = "BB_MID", mid, t
                    break
        else:
            exit_reason = "TIME_STOP"
            exit_price = bc[-1]
            exit_time = bt[-1]

        # R-multiple
        pnl = (exit_price - entry) if is_long else (entry - exit_price)
        r_gross = pnl / risk_per_unit if risk_per_unit > 0 else 0.0
        r_net = r_gross - friction_r

        results.append({
            "time": sig["time"], "symbol": sig["symbol"],
            "signal_type": sig["signal_type"], "direction": direction,
            "exit_reason": exit_reason, "r_multiple": r_net,
        })

    if not results:
        return pl.DataFrame()
    return pl.DataFrame(results)


def run_dynamic_mgmt() -> pl.DataFrame:
    surv_path = REPORTS_DIR / "math_phase_a_survivors.parquet"
    if not surv_path.exists():
        raise FileNotFoundError(f"Phase-A survivors not yet written: {surv_path}")
    survivors = pl.read_parquet(surv_path)
    if len(survivors) == 0:
        print("[DynMgmt] No Phase-A survivors to test.")
        return pl.DataFrame()

    print(f"[DynMgmt] Testing {len(survivors)} Phase-A survivors x {len(EXIT_STYLES)} exit styles "
          f"= {len(survivors) * len(EXIT_STYLES)} backtests")

    rows = []
    for i, surv in enumerate(survivors.iter_rows(named=True)):
        if i % 25 == 0:
            print(f"[DynMgmt] {i}/{len(survivors)}", flush=True)
        sym, ses, sig_type = surv["symbol"], surv["session"], surv["signal_type"]
        try:
            bars = _load_and_enrich_math(sym)
        except FileNotFoundError:
            continue
        try:
            raw = SignalGenerator.generate(bars, sig_type, sym)
        except Exception:
            continue
        sigs = _filter_by_session(raw, ses)
        if len(sigs) < 20:
            continue
        fric = _friction_for(sym)
        session_end = INDICATOR_SESSIONS[ses][1]
        for style in EXIT_STYLES:
            trades = _run_dynamic_backtest(sigs, bars, style, session_end, fric)
            if len(trades) < 30:
                continue
            m = compute_metrics(trades)
            if m.trades_per_year < 30:
                continue
            rows.append({
                "symbol": sym, "session": ses, "signal_type": sig_type,
                "exit_style": style,
                "n_trades": m.n_trades, "wr": m.wr, "pf": m.profit_factor,
                "expectancy_r": m.expectancy_r, "max_dd_r": m.max_dd_r,
                "trades_per_year": m.trades_per_year,
            })

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    if not rows:
        print("[DynMgmt] No combos produced trades.")
        return pl.DataFrame()
    df = pl.DataFrame(rows).sort("expectancy_r", descending=True)
    df.write_parquet(REPORTS_DIR / "math_dynamic_mgmt.parquet")

    # Summary
    print()
    print(f"Total combos: {len(df)}")
    print(f"PF>=1.2 AND WR>=0.60: {len(df.filter((pl.col('pf')>=1.2)&(pl.col('wr')>=0.60)))}")
    print(f"PF>=1.2 AND WR>=0.70: {len(df.filter((pl.col('pf')>=1.2)&(pl.col('wr')>=0.70)))}")
    print(f"PF>=1.2 AND WR>=0.80: {len(df.filter((pl.col('pf')>=1.2)&(pl.col('wr')>=0.80)))}")
    print()
    print("Best per exit_style:")
    for style in EXIT_STYLES:
        sub = df.filter(pl.col("exit_style") == style).sort("pf", descending=True).head(3)
        print(f"\n--- {style} ---")
        if len(sub) > 0:
            for r in sub.iter_rows(named=True):
                print(f"  {r['symbol']}/{r['session']}/{r['signal_type']}: "
                      f"WR={r['wr']:.3f} PF={r['pf']:.3f} exp={r['expectancy_r']:.3f}R "
                      f"n={r['n_trades']} tpy={r['trades_per_year']:.0f}")

    # Markdown report
    md_lines = [
        "# Math Discovery - Dynamic Management Report",
        "",
        f"- Total combos: **{len(df)}**",
        f"- Hard SL backstop: {HARD_SL_ATR}xATR",
        "",
        "## Top 30 by expectancy",
        "",
        "| Symbol | Session | Signal | Exit | Trades | WR | PF | Exp(R) | MaxDD | Trades/yr |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in df.head(30).iter_rows(named=True):
        md_lines.append(
            f"| {r['symbol']} | {r['session']} | {r['signal_type']} | {r['exit_style']} "
            f"| {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.2f} "
            f"| {r['expectancy_r']:.3f} | {r['max_dd_r']:.1f} | {r['trades_per_year']:.0f} |"
        )
    (REPORTS_DIR / "Math_Dynamic_Mgmt.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    return df


if __name__ == "__main__":
    run_dynamic_mgmt()
