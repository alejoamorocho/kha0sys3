"""R:R grid search on the 6 active math setups, run on VPS with REAL MT5 data.

Pulls from MT5 live connection:
  - M15 bars (~4000) for math indicator enrichment and signal detection
  - M1 bars (~45000 = ~30d) for tick-level fill simulation (real high/low)
  - symbol_info: spread (points), tick_size, tick_value, volume_min/max/step
  - Vantage commission by asset class (FX $7 RT, index $3.5 RT)
  - Intraday spread variation: computed from M1 (high-low mean per session hour)

For each of the 6 setups + each (TP, SL) in grid:
  1. Detect setup on M15, flip direction, compute STOP at close ± 0.5×ATR
  2. Wait window 5 M15 bars (75 M1 bars) for fill
  3. On fill: add entry slippage = spread(hour-of-day), TP/SL scan in M1
  4. Exit: TP / SL / session time-stop (first-touch in M1)
  5. PnL in USD at volume_min, minus commission per round-turn per lot

Output:
  C:\ProgramData\Kha0sysMath\logs\rr_grid_live.json
  Per-setup best R:R + spread stats per symbol.
"""
from __future__ import annotations
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone, timedelta

import MetaTrader5 as mt5
import polars as pl

sys.path.insert(0, r"C:\Proyectos\kha0sys3")

from src.application.math_indicators import MathIndicatorEnricher
from src.engine.run_math_momentum import detect_setups
from src.domain.constants import INDICATOR_SESSIONS, MATH_STOP_ATR_OFFSET, MATH_WAIT_BARS

DAYS = 30
LOG_DIR = r"C:\ProgramData\Kha0sysMath\logs"
VANTAGE_FX_COMMISSION_RT = 7.0
VANTAGE_INDEX_COMMISSION_RT = 3.5
INDEX_SET = {"SP500", "NAS100", "VIX", "USOUSD", "UKOUSD", "NG-C", "XAGUSD"}

# Grid: fine enough to see the landscape, coarse enough to run in reasonable time
TP_GRID = (0.3, 0.5, 0.75, 1.0, 1.25, 1.5)
SL_GRID = (1.0, 1.25, 1.5, 2.0, 2.5)


def _fetch_bars(symbol, tf, n):
    rates = mt5.copy_rates_from_pos(symbol, tf, 0, n)
    if rates is None or len(rates) == 0:
        return None
    return pl.DataFrame({
        "time": [datetime.fromtimestamp(r["time"], tz=timezone.utc) for r in rates],
        "open": [float(r["open"]) for r in rates],
        "high": [float(r["high"]) for r in rates],
        "low": [float(r["low"]) for r in rates],
        "close": [float(r["close"]) for r in rates],
    }).sort("time")


def _enrich(bars_m15):
    df = bars_m15.with_columns([
        pl.max_horizontal(
            pl.col("high") - pl.col("low"),
            (pl.col("high") - pl.col("close").shift(1)).abs(),
            (pl.col("low") - pl.col("close").shift(1)).abs(),
        ).alias("_tr"),
    ]).with_columns([
        pl.col("_tr").ewm_mean(alpha=1/14, adjust=False, min_samples=14).alias("atr_14"),
    ]).drop("_tr")
    return MathIndicatorEnricher.enrich_all_math(df)


def _hourly_spread_table(bars_m1, tick_size, default_spread_price):
    """Proxy for intraday spread variation: uses M1 high-low median per hour.
    Returns dict {hour_utc: spread_price_avg}.
    Caveat: MT5 tick archive would be exact; this is a robust approximation
    that captures session-driven widening (Asia wider than London/NY).
    """
    try:
        hour_stats = (
            bars_m1.with_columns([
                pl.col("time").dt.hour().alias("h"),
                (pl.col("high") - pl.col("low")).alias("range"),
            ]).group_by("h")
              .agg(pl.col("range").median().alias("median_range_price"))
              .sort("h")
        )
        # Use median M1 range as proxy. In live the actual bid-ask spread
        # is typically 10-30% of the M1 range during active session.
        # We scale to max(default_spread_price, 0.15 * median_range) per hour.
        out = {}
        for row in hour_stats.iter_rows(named=True):
            proxy = max(default_spread_price, 0.15 * row["median_range_price"])
            out[row["h"]] = proxy
        return out
    except Exception:
        return {h: default_spread_price for h in range(24)}


def _simulate(cfg, bars_m15_enr, bars_m1, sym_info, commission_rt, tp_atr, sl_atr,
              spread_by_hour):
    setup = cfg["setup_type"]
    session = cfg["session"]
    tick_size = float(getattr(sym_info, "trade_tick_size", getattr(sym_info, "point", 1e-5)))
    tick_value = float(getattr(sym_info, "trade_tick_value", 1.0))
    volume_min = float(getattr(sym_info, "volume_min", 0.01))
    digits = int(getattr(sym_info, "digits", 5))

    try:
        sigs = detect_setups(bars_m15_enr, setup)
    except Exception:
        return []
    start_h, end_h = INDICATOR_SESSIONS[session]
    sigs = sigs.filter(
        (pl.col("time").dt.hour() >= start_h) & (pl.col("time").dt.hour() < end_h)
    )
    if len(sigs) == 0:
        return []
    sigs = sigs.with_columns(pl.col("time").dt.date().alias("_d")) \
        .sort("time").unique(subset=["_d"], keep="first").drop("_d")

    m1_times = bars_m1["time"].to_list()
    m1_highs = bars_m1["high"].to_list()
    m1_lows = bars_m1["low"].to_list()
    m1_closes = bars_m1["close"].to_list()

    def _idx(t):
        lo, hi = 0, len(m1_times) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if m1_times[mid] < t:
                lo = mid + 1
            else:
                hi = mid - 1
        return lo

    trades = []
    for row in sigs.iter_rows(named=True):
        atr = row.get("atr_14")
        close = row["close"]
        if atr is None or atr <= 0:
            continue
        orig_dir = row["direction"]
        flipped = "SHORT" if orig_dir == "LONG" else "LONG"
        if flipped == "LONG":
            stop_price = round(close + MATH_STOP_ATR_OFFSET * atr, digits)
        else:
            stop_price = round(close - MATH_STOP_ATR_OFFSET * atr, digits)

        t_start = row["time"] + timedelta(minutes=15)
        t_end = row["time"] + timedelta(minutes=15 * MATH_WAIT_BARS)
        i0 = _idx(t_start)
        i_end = min(_idx(t_end), len(m1_times))

        filled_at = None
        filled_idx = None
        for i in range(i0, i_end):
            hour_spread = spread_by_hour.get(m1_times[i].hour, tick_size)
            hi_, lo_ = m1_highs[i], m1_lows[i]
            if flipped == "LONG" and hi_ >= stop_price:
                filled_at = round(stop_price + hour_spread, digits)
                filled_idx = i
                break
            if flipped == "SHORT" and lo_ <= stop_price:
                filled_at = round(stop_price - hour_spread, digits)
                filled_idx = i
                break
        if filled_at is None:
            continue

        if flipped == "LONG":
            tp_price = round(filled_at + tp_atr * atr, digits)
            sl_price = round(filled_at - sl_atr * atr, digits)
        else:
            tp_price = round(filled_at - tp_atr * atr, digits)
            sl_price = round(filled_at + sl_atr * atr, digits)

        entry_date = m1_times[filled_idx].date()
        exit_reason = exit_price = exit_time = None
        for j in range(filled_idx + 1, len(m1_times)):
            t = m1_times[j]
            if t.date() > entry_date or t.hour >= end_h:
                exit_reason, exit_price, exit_time = "TIME_STOP", m1_closes[j - 1], m1_times[j - 1]
                break
            hi_, lo_ = m1_highs[j], m1_lows[j]
            if flipped == "LONG":
                if hi_ >= tp_price:
                    exit_reason, exit_price, exit_time = "TP", tp_price, t; break
                if lo_ <= sl_price:
                    exit_reason, exit_price, exit_time = "SL", sl_price, t; break
            else:
                if lo_ <= tp_price:
                    exit_reason, exit_price, exit_time = "TP", tp_price, t; break
                if hi_ >= sl_price:
                    exit_reason, exit_price, exit_time = "SL", sl_price, t; break
        if exit_reason is None:
            exit_reason, exit_price, exit_time = "TIME_STOP", m1_closes[-1], m1_times[-1]

        pnl_price = (exit_price - filled_at) if flipped == "LONG" else (filled_at - exit_price)
        risk_price = sl_atr * atr
        r_gross = pnl_price / risk_price if risk_price > 0 else 0.0
        points_moved = pnl_price / tick_size
        pnl_usd = points_moved * tick_value * volume_min - commission_rt * volume_min

        trades.append({"r_gross": r_gross, "pnl_usd": pnl_usd, "reason": exit_reason})
    return trades


def main():
    if not mt5.initialize():
        print("MT5 init failed:", mt5.last_error())
        return 1
    os.makedirs(LOG_DIR, exist_ok=True)
    acct = mt5.account_info()
    print(f"Account {acct.login} balance=${acct.balance:.2f}")

    cfg = json.load(open(r"C:\Proyectos\kha0sys3\src\execution\bot_config_math.json"))
    portfolio = cfg["portfolio"]
    print(f"Portfolio: {len(portfolio)} setups. Grid: TP {TP_GRID} x SL {SL_GRID} = "
          f"{len(TP_GRID)*len(SL_GRID)} combos/setup ({len(portfolio)*len(TP_GRID)*len(SL_GRID)} total)")

    # Cache per broker symbol
    symbol_cache = {}
    by_sym = defaultdict(list)
    for s in portfolio:
        by_sym[s["sym"]].append(s)

    print("\n--- Fetching data + spread-by-hour per symbol ---")
    for sym in by_sym:
        info = mt5.symbol_info(sym)
        if info is None:
            print(f"  SKIP {sym}: info None"); continue
        if not info.visible:
            mt5.symbol_select(sym, True); info = mt5.symbol_info(sym)
        m15 = _fetch_bars(sym, mt5.TIMEFRAME_M15, 4000)
        m1 = _fetch_bars(sym, mt5.TIMEFRAME_M1, 45000)
        if m15 is None or m1 is None:
            print(f"  SKIP {sym}: no bars"); continue
        cutoff = datetime.now(timezone.utc) - timedelta(days=DAYS)
        m15_enr = _enrich(m15)
        m15_win = m15_enr.filter(pl.col("time") >= cutoff)
        m1_win = m1.filter(pl.col("time") >= cutoff)

        tick_size = float(getattr(info, "trade_tick_size", getattr(info, "point", 1e-5)))
        default_spread_price = float(info.spread) * tick_size
        spread_by_hour = _hourly_spread_table(m1_win, tick_size, default_spread_price)
        avg_spread = sum(spread_by_hour.values()) / len(spread_by_hour)
        internal = sym.replace("+", "").replace("NAS100", "NASDAQ100")
        commission = (VANTAGE_INDEX_COMMISSION_RT if internal in INDEX_SET
                      else VANTAGE_FX_COMMISSION_RT)
        symbol_cache[sym] = {
            "info": info, "m15": m15_win, "m1": m1_win,
            "spread_by_hour": spread_by_hour, "avg_spread": avg_spread,
            "commission": commission, "internal": internal,
        }
        print(f"  {sym}: m15={len(m15_win)} m1={len(m1_win)} "
              f"spread_cur={info.spread}pt avg_hourly_spread=${avg_spread:.6f} "
              f"commission=${commission} vol_min={info.volume_min}")

    # Grid
    results = []
    for s in portfolio:
        sym = s["sym"]
        if sym not in symbol_cache:
            continue
        c = symbol_cache[sym]
        print(f"\n--- {sym} {s['session']} {s['setup_type']} ---")
        for tp in TP_GRID:
            for sl in SL_GRID:
                trades = _simulate(s, c["m15"], c["m1"], c["info"], c["commission"],
                                   tp, sl, c["spread_by_hour"])
                n = len(trades)
                if n == 0:
                    results.append({"sym": sym, "session": s["session"],
                                    "setup": s["setup_type"], "tp": tp, "sl": sl,
                                    "n": 0, "wr": 0, "pf": 0, "net_r": 0, "net_usd": 0})
                    continue
                rs = [t["r_gross"] for t in trades]
                usds = [t["pnl_usd"] for t in trades]
                wins = sum(1 for r in rs if r > 0)
                gp = sum(r for r in rs if r > 0)
                gl = abs(sum(r for r in rs if r < 0))
                pf = gp / gl if gl > 0 else 999.0
                results.append({
                    "sym": sym, "session": s["session"], "setup": s["setup_type"],
                    "tp": tp, "sl": sl, "n": n,
                    "wr": wins / n, "pf": pf,
                    "net_r": sum(rs), "net_usd": sum(usds),
                    "avg_r": sum(rs) / n,
                })
                print(f"  TP={tp}/SL={sl}: n={n:3} WR={wins/n:.2%} PF={pf:.2f} "
                      f"netR={sum(rs):+.2f} netUSD=${sum(usds):+.2f}")

    # Best per setup
    print("\n" + "=" * 80)
    print("BEST R:R PER SETUP (by net_usd, with real spread+commission)")
    print("=" * 80)
    by_setup = defaultdict(list)
    for r in results:
        by_setup[(r["sym"], r["session"], r["setup"])].append(r)
    best_per = []
    for (sym, ses, setup), combos in by_setup.items():
        combos.sort(key=lambda x: -x["net_usd"])
        current_cfg = next((s for s in portfolio if s["sym"] == sym and s["session"] == ses
                            and s["setup_type"] == setup), None)
        current_tp, current_sl = (current_cfg["tp_atr_mult"], current_cfg["sl_atr_mult"]) if current_cfg else (None, None)
        top3 = combos[:3]
        print(f"\n{sym} {ses} {setup}  (current: TP={current_tp}/SL={current_sl})")
        for r in top3:
            mark = " <- CURRENT" if (r["tp"] == current_tp and r["sl"] == current_sl) else ""
            print(f"  TP={r['tp']}/SL={r['sl']}  n={r['n']:3} WR={r['wr']:.2%} "
                  f"PF={r['pf']:.2f} netR={r['net_r']:+.2f} netUSD=${r['net_usd']:+.2f}{mark}")
        if combos:
            best_per.append({
                "sym": sym, "session": ses, "setup": setup,
                "current_tp": current_tp, "current_sl": current_sl,
                "best_tp": combos[0]["tp"], "best_sl": combos[0]["sl"],
                "best_net_usd": combos[0]["net_usd"],
                "best_wr": combos[0]["wr"], "best_pf": combos[0]["pf"],
                "best_n": combos[0]["n"],
            })

    out = {"days": DAYS, "balance": acct.balance,
           "portfolio_size": len(portfolio),
           "tp_grid": list(TP_GRID), "sl_grid": list(SL_GRID),
           "results": results, "best_per_setup": best_per}
    with open(os.path.join(LOG_DIR, "rr_grid_live.json"), "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nSaved: {os.path.join(LOG_DIR, 'rr_grid_live.json')}")
    mt5.shutdown()


if __name__ == "__main__":
    sys.exit(main() or 0)
