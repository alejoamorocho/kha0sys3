"""Audit REAL trade history on the live MT5 for BOTH runners.

Reads deals for magic 1337 (FADE) and 1338 (MATH) over a window (default 60d).
Aggregates WR/PF/avg/net, per-symbol, equity curve.

Run on the VPS:
    python scripts/live_pnl_audit.py --days 60
    python scripts/live_pnl_audit.py --days 60 --magic 1338
"""
from __future__ import annotations
import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone, timedelta

import MetaTrader5 as mt5


def _aggregate(trades):
    if not trades:
        return None
    n = len(trades)
    wins = sum(1 for t in trades if t["profit_usd"] > 0)
    losses = n - wins
    wr = wins / n
    gross_p = sum(t["profit_usd"] for t in trades if t["profit_usd"] > 0)
    gross_l = abs(sum(t["profit_usd"] for t in trades if t["profit_usd"] < 0))
    pf = gross_p / gross_l if gross_l > 0 else float("inf")
    avg_win = gross_p / wins if wins else 0.0
    avg_loss = gross_l / losses if losses else 0.0
    net = sum(t["profit_usd"] for t in trades)
    eq = 0.0
    peak = 0.0
    max_dd = 0.0
    for t in trades:
        eq += t["profit_usd"]
        peak = max(peak, eq)
        dd = peak - eq
        if dd > max_dd:
            max_dd = dd
    return {
        "n": n, "wins": wins, "losses": losses,
        "wr": wr, "pf": pf,
        "avg_win": avg_win, "avg_loss": avg_loss,
        "net_usd": net, "max_dd": max_dd,
    }


def _trades_for_magic(deals, magic):
    sel = [d for d in deals if d.magic == magic]
    pos_groups = defaultdict(list)
    for d in sel:
        pos_groups[d.position_id].append(d)
    out = []
    for pid, dl in pos_groups.items():
        if len(dl) < 2:
            continue
        dl_s = sorted(dl, key=lambda x: x.time)
        entry = dl_s[0]
        exit_d = dl_s[-1]
        profit = sum(d.profit + d.swap + d.commission for d in dl)
        out.append({
            "pos": pid, "symbol": entry.symbol,
            "entry_time": datetime.fromtimestamp(entry.time, tz=timezone.utc),
            "exit_time": datetime.fromtimestamp(exit_d.time, tz=timezone.utc),
            "entry_price": entry.price, "exit_price": exit_d.price,
            "volume": entry.volume, "profit_usd": profit,
        })
    out.sort(key=lambda t: t["exit_time"])
    return out


def _print_summary(label, magic, trades, stats):
    print()
    print("=" * 60)
    print(f"{label}  (magic {magic})  — {len(trades)} closed positions")
    print("=" * 60)
    if not stats:
        print("No closed positions in window.")
        return
    print(f"Wins / Losses:     {stats['wins']} / {stats['losses']}")
    print(f"WR:                {stats['wr']:.1%}")
    print(f"PF:                {stats['pf']:.2f}")
    print(f"Avg win:           ${stats['avg_win']:+,.2f}")
    print(f"Avg loss:          ${-stats['avg_loss']:+,.2f}")
    print(f"Net P&L:           ${stats['net_usd']:+,.2f}")
    print(f"Max running DD:    ${stats['max_dd']:+,.2f}")

    # Per-symbol
    sym = defaultdict(lambda: {"n": 0, "w": 0, "pnl": 0.0})
    for t in trades:
        sym[t["symbol"]]["n"] += 1
        sym[t["symbol"]]["pnl"] += t["profit_usd"]
        if t["profit_usd"] > 0:
            sym[t["symbol"]]["w"] += 1
    print(f"\n{'SYMBOL':<10} {'N':>4} {'WR':>7} {'PnL':>14}")
    print("-" * 40)
    for s, st in sorted(sym.items(), key=lambda x: x[1]["pnl"]):
        w = st["w"] / st["n"] if st["n"] else 0
        print(f"{s:<10} {st['n']:>4} {w:>6.1%} ${st['pnl']:>+12,.2f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=60)
    args = ap.parse_args()

    if not mt5.initialize():
        print("MT5 init failed:", mt5.last_error())
        return 1
    acct = mt5.account_info()
    print(f"Account: {acct.login}  balance=${acct.balance:,.2f}  equity=${acct.equity:,.2f}")

    to_dt = datetime.now(timezone.utc)
    from_dt = to_dt - timedelta(days=args.days)
    print(f"Window: {from_dt.date()} -> {to_dt.date()} ({args.days} days)")

    deals = mt5.history_deals_get(from_dt, to_dt)
    if deals is None:
        print("history_deals_get None:", mt5.last_error())
        mt5.shutdown()
        return 1
    print(f"Total deals in window: {len(deals)}")

    for magic, label in [(1337, "FADE"), (1338, "MATH-INVERT")]:
        tr = _trades_for_magic(deals, magic)
        stats = _aggregate(tr)
        _print_summary(label, magic, tr, stats)

    # Save both as JSON
    out = {}
    for magic, label in [(1337, "fade"), (1338, "math")]:
        tr = _trades_for_magic(deals, magic)
        out[label] = [{
            "pos": t["pos"], "symbol": t["symbol"],
            "entry_time": t["entry_time"].isoformat(),
            "exit_time": t["exit_time"].isoformat(),
            "entry_price": t["entry_price"], "exit_price": t["exit_price"],
            "volume": t["volume"], "profit_usd": t["profit_usd"],
        } for t in tr]
    import os
    os.makedirs(r"C:\ProgramData\Kha0sysMath\logs", exist_ok=True)
    with open(r"C:\ProgramData\Kha0sysMath\logs\live_pnl_audit.json", "w") as f:
        json.dump(out, f, indent=2)
    print(r"\nRaw deals saved to C:\ProgramData\Kha0sysMath\logs\live_pnl_audit.json")
    mt5.shutdown()


if __name__ == "__main__":
    sys.exit(main() or 0)
