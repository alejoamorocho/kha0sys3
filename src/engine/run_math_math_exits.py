"""Pure-math exit management on Phase-A survivors.

Complements run_math_dynamic_mgmt.py (which uses classical indicators).
Here exits are driven exclusively by the math indicators (calculus / linear
algebra / statistics). Each exit has a crisp mathematical meaning:

Exit styles:
  VELOCITY_FLIP      — close when velocity_10 changes sign
                       (dP/dt flips → momentum exhausted)
  ACCEL_ZERO         — close when accel_10 crosses 0
                       (d2P/dt2 = 0 → inflection point)
  OLS_RESID_ZERO     — close when ols_resid_z_30 crosses 0
                       (price back on regression line)
  MEANREV_AREA_ZERO  — close when meanrev_area_50 crosses 0
                       (cumulative area = 0 → SMA reached)
  KALMAN_STATE_CROSS — close when price crosses kalman_state
                       (filter caught up with observation)

All share hard SL = 2.5*ATR and time-stop at session end.

Usage:
    python -m src.engine.run_math_math_exits
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
EXIT_STYLES = ("VELOCITY_FLIP", "ACCEL_ZERO", "OLS_RESID_ZERO",
               "MEANREV_AREA_ZERO", "KALMAN_STATE_CROSS")
HARD_SL_ATR = 2.5


def _friction_for(symbol: str) -> float:
    return FRICTION_INDEX if symbol in INDEX_SYMBOLS else FRICTION_FX


def _sign_cross(prev, curr) -> bool:
    """True if prev and curr have opposite signs (non-zero)."""
    if prev is None or curr is None:
        return False
    return prev * curr < 0


def _run(signals: pl.DataFrame, bars: pl.DataFrame, exit_style: str,
         session_end_hour: int, friction_r: float) -> pl.DataFrame:
    if len(signals) == 0:
        return pl.DataFrame()

    deduped = signals.with_columns([
        pl.col("time").dt.date().alias("_date")
    ]).sort("time").unique(
        subset=["symbol", "signal_type", "_date"], keep="first"
    ).drop("_date")

    bars_s = bars.sort("time")
    cols = bars_s.columns

    def _get(name: str):
        return bars_s[name].to_list() if name in cols else [None] * len(bars_s)

    bt = bars_s["time"].to_list()
    bh = bars_s["high"].to_list()
    bl = bars_s["low"].to_list()
    bc = bars_s["close"].to_list()
    vel = _get("velocity_10")
    acc = _get("accel_10")
    resz = _get("ols_resid_z_30")
    area = _get("meanrev_area_50")
    kst = _get("kalman_state")

    t2i = {t: i for i, t in enumerate(bt)}
    results = []

    for sig in deduped.iter_rows(named=True):
        if sig["atr_14"] is None:
            continue
        entry = sig["close"]
        atr = sig["atr_14"]
        is_long = sig["direction"] == "LONG"
        hard_sl = entry - HARD_SL_ATR * atr if is_long else entry + HARD_SL_ATR * atr
        risk = HARD_SL_ATR * atr

        start = t2i.get(sig["time"])
        if start is None:
            continue

        exit_reason = exit_price = exit_time = None
        signal_date = sig["time"].date()

        for i in range(start + 1, len(bt)):
            t = bt[i]
            if t.date() > signal_date or t.hour >= session_end_hour:
                exit_reason, exit_price, exit_time = "TIME_STOP", bc[i - 1], bt[i - 1]
                break
            hi, lo = bh[i], bl[i]
            # Hard SL
            if is_long and lo <= hard_sl:
                exit_reason, exit_price, exit_time = "HARD_SL", hard_sl, t
                break
            if (not is_long) and hi >= hard_sl:
                exit_reason, exit_price, exit_time = "HARD_SL", hard_sl, t
                break

            if exit_style == "VELOCITY_FLIP":
                if _sign_cross(vel[i-1], vel[i]):
                    exit_reason, exit_price, exit_time = "VEL_FLIP", bc[i], t
                    break
            elif exit_style == "ACCEL_ZERO":
                if _sign_cross(acc[i-1], acc[i]):
                    exit_reason, exit_price, exit_time = "ACC_ZERO", bc[i], t
                    break
            elif exit_style == "OLS_RESID_ZERO":
                if _sign_cross(resz[i-1], resz[i]):
                    exit_reason, exit_price, exit_time = "OLS_ZERO", bc[i], t
                    break
            elif exit_style == "MEANREV_AREA_ZERO":
                if _sign_cross(area[i-1], area[i]):
                    exit_reason, exit_price, exit_time = "AREA_ZERO", bc[i], t
                    break
            elif exit_style == "KALMAN_STATE_CROSS":
                ks = kst[i]
                ks_prev = kst[i-1] if i > 0 else None
                if ks is None or ks_prev is None:
                    continue
                # LONG entered below state → exit when close crosses above state
                if is_long and bc[i-1] < ks_prev and bc[i] >= ks:
                    exit_reason, exit_price, exit_time = "KSTATE_UP", bc[i], t
                    break
                if (not is_long) and bc[i-1] > ks_prev and bc[i] <= ks:
                    exit_reason, exit_price, exit_time = "KSTATE_DN", bc[i], t
                    break
        else:
            exit_reason, exit_price, exit_time = "TIME_STOP", bc[-1], bt[-1]

        pnl = (exit_price - entry) if is_long else (entry - exit_price)
        r_gross = pnl / risk if risk > 0 else 0.0
        r_net = r_gross - friction_r
        results.append({
            "time": sig["time"], "symbol": sig["symbol"],
            "signal_type": sig["signal_type"], "direction": sig["direction"],
            "exit_reason": exit_reason, "r_multiple": r_net,
        })

    return pl.DataFrame(results) if results else pl.DataFrame()


def main():
    surv_path = REPORTS_DIR / "math_phase_a_survivors.parquet"
    if not surv_path.exists():
        raise FileNotFoundError(surv_path)
    survivors = pl.read_parquet(surv_path)
    print(f"[MathExits] {len(survivors)} Phase-A x {len(EXIT_STYLES)} styles = "
          f"{len(survivors) * len(EXIT_STYLES)} backtests")

    rows = []
    for i, s in enumerate(survivors.iter_rows(named=True)):
        if i % 25 == 0:
            print(f"[MathExits] {i}/{len(survivors)}", flush=True)
        sym, ses, sig_type = s["symbol"], s["session"], s["signal_type"]
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
        se = INDICATOR_SESSIONS[ses][1]
        for style in EXIT_STYLES:
            trades = _run(sigs, bars, style, se, fric)
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
        print("[MathExits] No combos produced trades.")
        return
    df = pl.DataFrame(rows).sort("expectancy_r", descending=True)
    df.write_parquet(REPORTS_DIR / "math_math_exits.parquet")

    print(f"\nTotal: {len(df)}")
    print(f"PF>=1.2 AND WR>=0.60: {len(df.filter((pl.col('pf')>=1.2)&(pl.col('wr')>=0.60)))}")
    print(f"PF>=1.2 AND WR>=0.70: {len(df.filter((pl.col('pf')>=1.2)&(pl.col('wr')>=0.70)))}")
    print(f"PF>=1.2 AND WR>=0.80: {len(df.filter((pl.col('pf')>=1.2)&(pl.col('wr')>=0.80)))}")
    print()
    for style in EXIT_STYLES:
        sub = df.filter(pl.col("exit_style") == style).sort("pf", descending=True).head(3)
        print(f"\n--- {style} ---")
        for r in sub.iter_rows(named=True):
            print(f"  {r['symbol']}/{r['session']}/{r['signal_type']}: "
                  f"WR={r['wr']:.3f} PF={r['pf']:.3f} exp={r['expectancy_r']:.3f}R "
                  f"n={r['n_trades']} tpy={r['trades_per_year']:.0f}")

    md = ["# Math Discovery - Math-Indicator Exits Report", "",
          f"- Total: **{len(df)}**", f"- Hard SL: {HARD_SL_ATR}xATR", "",
          "## Top 30 by expectancy", "",
          "| Symbol | Session | Signal | Exit | Trades | WR | PF | Exp(R) | MaxDD | TPY |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for r in df.head(30).iter_rows(named=True):
        md.append(f"| {r['symbol']} | {r['session']} | {r['signal_type']} | {r['exit_style']} "
                  f"| {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.2f} "
                  f"| {r['expectancy_r']:.3f} | {r['max_dd_r']:.1f} | {r['trades_per_year']:.0f} |")
    (REPORTS_DIR / "Math_Math_Exits.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
