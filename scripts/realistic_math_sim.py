"""Realistic 30-day simulation of the math-invert portfolio against REAL MT5 data.

Runs on the VPS where MT5 is connected to Vantage Live. For each of the 17
strategies in bot_config_math.json:
  1. Pulls M15 bars for the last 30 days (enrichment + math indicators source).
  2. Pulls M1 bars for the same window (tick-level fill simulation).
  3. Uses real symbol_info.spread and commission_from_broker (if available).
  4. Runs detect_setups → flip direction → compute STOP at close +/- 0.5*ATR.
  5. Simulates LIMIT wait window with real M1 high/low traversal.
  6. On fill: TP/SL scan in M1 (first-touch semantics).
  7. Applies entry slippage = 1x spread AND commission per side.
  8. Aggregates by strategy and in total.

Output:
  C:\ProgramData\Kha0sysMath\logs\realistic_math_sim.json
  Markdown printed to stdout.
"""
from __future__ import annotations
import json
import os
import sys
import math
from collections import defaultdict
from datetime import datetime, timezone, timedelta

import MetaTrader5 as mt5
import polars as pl

sys.path.insert(0, r"C:\Proyectos\kha0sys3")

from src.application.math_indicators import MathIndicatorEnricher
from src.application.calculators import DataEnricher  # for ATR
from src.engine.run_math_momentum import detect_setups
from src.domain.constants import (
    INDICATOR_SESSIONS, MATH_STOP_ATR_OFFSET, MATH_WAIT_BARS,
)

DAYS = 30
LOG_DIR = r"C:\ProgramData\Kha0sysMath\logs"

# Vantage commission estimate per round-turn per lot (USD)
VANTAGE_FX_COMMISSION_RT = 7.0
VANTAGE_INDEX_COMMISSION_RT = 3.5
INDEX_MT5_SYMBOLS = {"SP500", "NAS100", "VIX", "USOUSD", "UKOUSD", "NG-C", "XAGUSD"}


def _fetch_bars(symbol: str, tf, bars_n: int) -> pl.DataFrame | None:
    """Pull bars from MT5, latest N. Returns Polars DF with time/ohlcv."""
    rates = mt5.copy_rates_from_pos(symbol, tf, 0, bars_n)
    if rates is None or len(rates) == 0:
        return None
    df = pl.DataFrame({
        "time": [datetime.fromtimestamp(r["time"], tz=timezone.utc) for r in rates],
        "open": [float(r["open"]) for r in rates],
        "high": [float(r["high"]) for r in rates],
        "low": [float(r["low"]) for r in rates],
        "close": [float(r["close"]) for r in rates],
        "tick_volume": [int(r["tick_volume"]) for r in rates],
    }).sort("time")
    return df


def _enrich_for_math(bars_m15: pl.DataFrame) -> pl.DataFrame:
    """Add ATR-14 and all math indicators on M15 bars."""
    df = bars_m15.with_columns([
        pl.max_horizontal(
            pl.col("high") - pl.col("low"),
            (pl.col("high") - pl.col("close").shift(1)).abs(),
            (pl.col("low") - pl.col("close").shift(1)).abs(),
        ).alias("_tr"),
    ]).with_columns([
        pl.col("_tr").ewm_mean(alpha=1/14, adjust=False, min_samples=14).alias("atr_14"),
    ]).drop("_tr")
    df = MathIndicatorEnricher.enrich_all_math(df)
    return df


def _session_hours(session: str):
    return INDICATOR_SESSIONS[session]


def _filter_session(df: pl.DataFrame, session: str) -> pl.DataFrame:
    start, end = _session_hours(session)
    return df.filter(
        (pl.col("time").dt.hour() >= start) & (pl.col("time").dt.hour() < end)
    )


def _simulate_one_setup(cfg, bars_m15_enriched, bars_m1, sym_info, commission_rt):
    """For one strategy config, return trade-level list."""
    sym = cfg["sym"]
    setup = cfg["setup_type"]
    tp_atr = float(cfg["tp_atr_mult"])
    sl_atr = float(cfg["sl_atr_mult"])
    session = cfg["session"]
    spread_points = float(sym_info.spread) if hasattr(sym_info, "spread") else 10
    tick_size = float(getattr(sym_info, "trade_tick_size", getattr(sym_info, "point", 1e-5)))
    tick_value = float(getattr(sym_info, "trade_tick_value", 1.0))
    volume_min = float(getattr(sym_info, "volume_min", 0.01))
    spread_price = spread_points * tick_size

    # Detect setups on M15 bars
    try:
        sigs = detect_setups(bars_m15_enriched, setup)
    except Exception as e:
        return [], f"detect_error: {e}"
    sigs = _filter_session(sigs, session)
    if len(sigs) == 0:
        return [], "no_signals"
    # Dedup: first per day per setup
    sigs = sigs.with_columns(pl.col("time").dt.date().alias("_d")) \
        .sort("time").unique(subset=["_d"], keep="first").drop("_d")

    # M1 index for fast lookup
    m1_times = bars_m1["time"].to_list()
    m1_highs = bars_m1["high"].to_list()
    m1_lows = bars_m1["low"].to_list()
    m1_closes = bars_m1["close"].to_list()

    def _bar_index_at(t):
        lo, hi = 0, len(m1_times) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if m1_times[mid] < t:
                lo = mid + 1
            else:
                hi = mid - 1
        return lo

    session_end_h = _session_hours(session)[1]
    trades = []

    for row in sigs.iter_rows(named=True):
        atr = row.get("atr_14")
        close = row["close"]
        orig_dir = row["direction"]
        if atr is None or atr <= 0:
            continue
        # Flip
        flipped = "SHORT" if orig_dir == "LONG" else "LONG"
        # STOP in flipped direction
        if flipped == "LONG":
            stop_price = close + MATH_STOP_ATR_OFFSET * atr
            order_type = "BUY_STOP"
        else:
            stop_price = close - MATH_STOP_ATR_OFFSET * atr
            order_type = "SELL_STOP"

        # Wait window: from signal bar close (M15) +15min to +5*15=75min
        t_start = row["time"] + timedelta(minutes=15)  # next M15 bar
        t_end = row["time"] + timedelta(minutes=15 * MATH_WAIT_BARS)
        i0 = _bar_index_at(t_start)
        i_end = _bar_index_at(t_end)

        # Scan for fill
        filled_at = None
        filled_idx = None
        for i in range(i0, min(i_end, len(m1_times))):
            hi_ = m1_highs[i]
            lo_ = m1_lows[i]
            if flipped == "LONG" and hi_ >= stop_price:
                filled_at = stop_price + spread_price  # entry slippage = 1x spread against
                filled_idx = i
                break
            if flipped == "SHORT" and lo_ <= stop_price:
                filled_at = stop_price - spread_price
                filled_idx = i
                break
        if filled_at is None:
            continue  # STOP not triggered within wait window

        # TP / SL
        if flipped == "LONG":
            tp_price = filled_at + tp_atr * atr
            sl_price = filled_at - sl_atr * atr
        else:
            tp_price = filled_at - tp_atr * atr
            sl_price = filled_at + sl_atr * atr

        # Scan forward for first touch until session end (same day)
        entry_date = m1_times[filled_idx].date()
        exit_reason = None
        exit_price = None
        exit_time = None
        for j in range(filled_idx + 1, len(m1_times)):
            t = m1_times[j]
            # Session time-stop
            if t.date() > entry_date or t.hour >= session_end_h:
                exit_reason, exit_price, exit_time = "TIME_STOP", m1_closes[j - 1], m1_times[j - 1]
                break
            hi_ = m1_highs[j]
            lo_ = m1_lows[j]
            if flipped == "LONG":
                if hi_ >= tp_price:
                    exit_reason, exit_price, exit_time = "TP", tp_price, t
                    break
                if lo_ <= sl_price:
                    exit_reason, exit_price, exit_time = "SL", sl_price, t
                    break
            else:
                if lo_ <= tp_price:
                    exit_reason, exit_price, exit_time = "TP", tp_price, t
                    break
                if hi_ >= sl_price:
                    exit_reason, exit_price, exit_time = "SL", sl_price, t
                    break
        if exit_reason is None:
            exit_reason, exit_price, exit_time = "TIME_STOP", m1_closes[-1], m1_times[-1]

        # PnL in price points
        if flipped == "LONG":
            pnl_price = exit_price - filled_at
        else:
            pnl_price = filled_at - exit_price
        # R-multiple
        risk_price = sl_atr * atr
        r_gross = pnl_price / risk_price if risk_price > 0 else 0.0

        # USD PnL with volume_min + commission
        # 1 tick PnL per 1.0 lot = tick_value; points_moved = pnl_price / tick_size
        points_moved = pnl_price / tick_size if tick_size > 0 else 0
        pnl_usd_1lot = points_moved * tick_value
        pnl_usd = pnl_usd_1lot * volume_min - commission_rt * volume_min

        trades.append({
            "sym": sym, "setup": setup, "session": session,
            "dir_flipped": flipped,
            "entry_time": m1_times[filled_idx].isoformat(),
            "entry_price": filled_at,
            "exit_time": exit_time.isoformat() if hasattr(exit_time, "isoformat") else str(exit_time),
            "exit_price": exit_price,
            "exit_reason": exit_reason,
            "atr": atr,
            "r_gross": round(r_gross, 4),
            "pnl_usd": round(pnl_usd, 4),
            "volume": volume_min,
            "spread_points": spread_points,
            "commission_rt": commission_rt,
        })
    return trades, None


def main():
    if not mt5.initialize():
        print("MT5 init failed:", mt5.last_error())
        return 1

    os.makedirs(LOG_DIR, exist_ok=True)
    acct = mt5.account_info()
    print(f"Account {acct.login} balance=${acct.balance:.2f}")

    cfg_path = r"C:\Proyectos\kha0sys3\src\execution\bot_config_math.json"
    bot_cfg = json.load(open(cfg_path))
    portfolio = bot_cfg["portfolio"]
    print(f"Portfolio: {len(portfolio)} strategies, window {DAYS}d")

    # M15 bars needed for enrichment lookback (Hurst needs 100, etc.) + window
    # Pull generous 1500 M15 bars (~15 days) but extend for 30-day window:
    # 30 days * 96 M15/day = 2880 + 500 buffer = 3380. Round up to 4000.
    m15_n = 4000
    # M1 bars for 30 days: 30 * 1440 = 43200
    m1_n = 45000

    # Group by broker symbol so we fetch each once
    by_sym = defaultdict(list)
    for s in portfolio:
        by_sym[s["sym"]].append(s)

    all_trades = []
    per_strat = []

    for sym, strats in by_sym.items():
        sym_info = mt5.symbol_info(sym)
        if sym_info is None:
            print(f"  [SKIP] {sym}: symbol_info None")
            continue
        # Ensure symbol is selected (visible)
        if not sym_info.visible:
            mt5.symbol_select(sym, True)
            sym_info = mt5.symbol_info(sym)

        internal = sym.replace("+", "").replace("NAS100", "NASDAQ100")
        # Fetch M15 + M1
        bars_m15 = _fetch_bars(sym, mt5.TIMEFRAME_M15, m15_n)
        if bars_m15 is None:
            print(f"  [SKIP] {sym}: no M15 data")
            continue
        bars_m1 = _fetch_bars(sym, mt5.TIMEFRAME_M1, m1_n)
        if bars_m1 is None:
            print(f"  [SKIP] {sym}: no M1 data")
            continue
        # Filter to last 30 days for the signal window (enrichment uses full m15)
        cutoff = datetime.now(timezone.utc) - timedelta(days=DAYS)
        bars_m15_enr = _enrich_for_math(bars_m15)
        bars_m15_win = bars_m15_enr.filter(pl.col("time") >= cutoff)
        bars_m1_win = bars_m1.filter(pl.col("time") >= cutoff)

        # Commission class
        commission = (VANTAGE_INDEX_COMMISSION_RT if internal in INDEX_MT5_SYMBOLS
                      else VANTAGE_FX_COMMISSION_RT)

        print(f"{sym}: m15={len(bars_m15_win)} m1={len(bars_m1_win)} "
              f"spread={sym_info.spread}pt tick_size={sym_info.trade_tick_size} "
              f"tick_val=${sym_info.trade_tick_value} vol_min={sym_info.volume_min} "
              f"commission=${commission}")

        for cfg in strats:
            trades, err = _simulate_one_setup(cfg, bars_m15_win, bars_m1_win,
                                              sym_info, commission)
            n = len(trades)
            if n == 0:
                per_strat.append({
                    "sym": sym, "session": cfg["session"], "setup": cfg["setup_type"],
                    "n": 0, "wr": 0, "net_r": 0.0, "net_usd": 0.0, "err": err,
                })
                continue
            rs = [t["r_gross"] for t in trades]
            wins = sum(1 for r in rs if r > 0)
            net_r = sum(rs)
            net_usd = sum(t["pnl_usd"] for t in trades)
            wr = wins / n
            per_strat.append({
                "sym": sym, "session": cfg["session"], "setup": cfg["setup_type"],
                "n": n, "wr": wr, "net_r": net_r, "net_usd": net_usd, "err": None,
            })
            all_trades.extend(trades)

    # Aggregate
    n = len(all_trades)
    if n == 0:
        print("No trades produced.")
        mt5.shutdown()
        return 0

    rs = [t["r_gross"] for t in all_trades]
    usds = [t["pnl_usd"] for t in all_trades]
    wins = sum(1 for r in rs if r > 0)
    wr = wins / n
    gp = sum(r for r in rs if r > 0)
    gl = abs(sum(r for r in rs if r < 0))
    pf = gp / gl if gl > 0 else float("inf")
    net_r = sum(rs)
    net_usd = sum(usds)
    # Equity curve
    eq = 0.0
    peak = 0.0
    max_dd = 0.0
    for t in sorted(all_trades, key=lambda x: x["exit_time"]):
        eq += t["pnl_usd"]
        peak = max(peak, eq)
        dd = peak - eq
        if dd > max_dd:
            max_dd = dd

    print()
    print("=" * 70)
    print(f"REALISTIC MATH SIM  {DAYS} days  (real MT5 data + spread + commission)")
    print("=" * 70)
    print(f"Trades:       {n}")
    print(f"WR:           {wr:.1%}")
    print(f"PF:           {pf:.2f}")
    print(f"Net R:        {net_r:+.2f}")
    print(f"Net USD:      ${net_usd:+,.2f}  (volume=volume_min per trade)")
    print(f"Max DD USD:   ${max_dd:,.2f}")
    print(f"Avg R/trade:  {net_r/n:+.3f}")
    print()
    print("Per-strategy:")
    print(f"{'SYMBOL':<12} {'SESSION':<10} {'SETUP':<25} {'N':>3} {'WR':>7} {'NetR':>8} {'NetUSD':>10}")
    print("-" * 80)
    for r in sorted(per_strat, key=lambda x: -x["net_usd"]):
        err = f" err={r['err']}" if r.get("err") else ""
        wr_s = f"{r['wr']:.1%}" if r["n"] else "-"
        print(f"{r['sym']:<12} {r['session']:<10} {r['setup']:<25} "
              f"{r['n']:>3} {wr_s:>7} {r['net_r']:>+8.2f} ${r['net_usd']:>+8.2f}{err}")

    out = {
        "days": DAYS, "n_trades": n, "wr": wr, "pf": pf,
        "net_r": net_r, "net_usd": net_usd, "max_dd_usd": max_dd,
        "balance": acct.balance,
        "per_strategy": per_strat, "trades": all_trades,
    }
    with open(os.path.join(LOG_DIR, "realistic_math_sim.json"), "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nSaved: {os.path.join(LOG_DIR, 'realistic_math_sim.json')}")
    mt5.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
