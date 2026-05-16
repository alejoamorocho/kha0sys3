"""Analyze last N days of MT5 deals across all engines (magic numbers).

Connects via MT5Client to the configured broker.yaml account, pulls
history_deals_get for the date range, and aggregates by:
  - Engine (magic number)
  - Individual strategy (deal.comment)

Identifies discard candidates per engine-strategy:
  - n>=5 and WR == 0%
  - n>=10 and PF < 0.5
  - n>=8 and avg_profit < 0 AND best_trade < |worst_trade|

Usage:
    py -3.12 scripts/analyze_last_week_trades.py [--days 7]
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src.execution.mt5_client import MT5Client

try:
    import MetaTrader5 as mt5  # type: ignore
except Exception:
    mt5 = None  # type: ignore


# Known engines per CLAUDE.md + this session's work
ENGINE_BY_MAGIC = {
    1337: "FADE (retired)",
    1338: "MATH K3M1-75",
    1339: "TRADERS SWING (planned)",
    1340: "TRADERS ORB (planned)",
    8338: "AMO8 ORB (V2)",
}


def _engine_name(magic: int) -> str:
    return ENGINE_BY_MAGIC.get(int(magic), f"UNKNOWN (magic {magic})")


def _fmt_money(x: float) -> str:
    return f"${x:+,.2f}"


def _aggregate(deals: list) -> dict:
    """Trade-level metrics for a deal list (DEAL_ENTRY_OUT only)."""
    if not deals:
        return {
            "n": 0, "wins": 0, "losses": 0, "wr": 0.0,
            "gross_profit": 0.0, "gross_loss": 0.0, "pf": 0.0,
            "net_pnl": 0.0, "avg_profit": 0.0, "avg_loss": 0.0,
            "best": 0.0, "worst": 0.0, "expectancy": 0.0,
            "commissions": 0.0, "swaps": 0.0,
        }
    profits = [float(d.profit) for d in deals]
    commissions = [float(d.commission) for d in deals]
    swaps = [float(d.swap) for d in deals]
    wins = [p for p in profits if p > 0]
    losses = [p for p in profits if p < 0]
    gp = sum(wins)
    gl = abs(sum(losses))
    pf = (gp / gl) if gl > 0 else (float("inf") if gp > 0 else 0.0)
    return {
        "n": len(profits),
        "wins": len(wins),
        "losses": len(losses),
        "wr": (len(wins) / len(profits)) if profits else 0.0,
        "gross_profit": gp,
        "gross_loss": gl,
        "pf": pf,
        "net_pnl": sum(profits) + sum(commissions) + sum(swaps),
        "avg_profit": (gp / len(wins)) if wins else 0.0,
        "avg_loss": (gl / len(losses)) if losses else 0.0,
        "best": max(profits) if profits else 0.0,
        "worst": min(profits) if profits else 0.0,
        "expectancy": (sum(profits) / len(profits)) if profits else 0.0,
        "commissions": sum(commissions),
        "swaps": sum(swaps),
    }


def _is_discard_candidate(m: dict) -> tuple[bool, str]:
    n = m["n"]
    if n >= 5 and m["wr"] == 0.0:
        return True, "0% WR with ≥5 trades"
    if n >= 10 and m["pf"] < 0.5:
        return True, f"PF {m['pf']:.2f} < 0.5 with ≥10 trades"
    if n >= 8 and m["expectancy"] < 0 and m["best"] < abs(m["worst"]):
        return True, "Negative expectancy + max win < max loss"
    return False, ""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--days", type=int, default=7)
    args = p.parse_args()

    if mt5 is None:
        print("ERROR: MetaTrader5 module not installed.")
        sys.exit(1)

    client = MT5Client()
    if not client.ensure_connected():
        print("ERROR: could not connect to MT5. Check broker.yaml.")
        sys.exit(1)

    info = mt5.account_info()
    if info is None:
        print("ERROR: account_info() returned None")
        sys.exit(1)
    print(f"Connected: account={info.login} ({info.server})  "
          f"balance=${info.balance:,.2f}  equity=${info.equity:,.2f}")

    to_date = datetime.now(timezone.utc)
    from_date = to_date - timedelta(days=args.days)
    print(f"\nFetching deals from {from_date.isoformat()} to {to_date.isoformat()}")

    deals = mt5.history_deals_get(from_date, to_date)
    if deals is None:
        print("history_deals_get returned None")
        sys.exit(1)
    deals = list(deals)
    closes = [d for d in deals if d.entry == mt5.DEAL_ENTRY_OUT]
    print(f"  raw deals: {len(deals)}, close deals: {len(closes)}")

    # ─── By engine (magic number) ───
    by_magic: dict[int, list] = defaultdict(list)
    for d in closes:
        by_magic[int(d.magic)].append(d)

    print(f"\n{'='*80}\nENGINE-LEVEL RESULTS (last {args.days} days)\n{'='*80}")
    print(f"\n{'Engine':<25}{'Trades':>8}{'Win%':>8}{'PF':>8}{'Net':>14}{'Best':>12}{'Worst':>12}")
    print("-" * 87)
    total_net = 0.0
    for magic in sorted(by_magic.keys()):
        m = _aggregate(by_magic[magic])
        eng = _engine_name(magic)
        pf_str = f"{m['pf']:.2f}" if m['pf'] != float('inf') else "inf"
        print(f"{eng:<25}{m['n']:>8}{m['wr']*100:>7.1f}%{pf_str:>8}"
              f"{_fmt_money(m['net_pnl']):>14}"
              f"{_fmt_money(m['best']):>12}{_fmt_money(m['worst']):>12}")
        total_net += m['net_pnl']
    print("-" * 87)
    print(f"{'TOTAL':<25}{sum(len(v) for v in by_magic.values()):>8}{'':>8}{'':>8}"
          f"{_fmt_money(total_net):>14}")

    # ─── Per-strategy detail per engine ───
    for magic in sorted(by_magic.keys()):
        eng = _engine_name(magic)
        engine_deals = by_magic[magic]
        # Group by comment
        by_comment: dict[str, list] = defaultdict(list)
        for d in engine_deals:
            # use the comment but strip retcode/SL/TP suffixes added by broker
            c = str(getattr(d, "comment", "")).strip()
            by_comment[c].append(d)

        print(f"\n{'='*80}\n[{eng}] (magic {magic}) — {len(engine_deals)} close trades\n{'='*80}")
        rows: list[tuple] = []
        for comment, dlist in by_comment.items():
            m = _aggregate(dlist)
            discard, reason = _is_discard_candidate(m)
            rows.append((m["net_pnl"], comment, m, discard, reason))
        rows.sort(key=lambda r: r[0], reverse=True)

        print(f"\n{'Strategy / Comment':<40}{'n':>5}{'W':>4}{'L':>4}"
              f"{'WR':>7}{'PF':>7}{'Net':>13}{'Avg':>10}  {'Verdict'}")
        print("-" * 110)
        for net, comment, m, discard, reason in rows:
            wr_str = f"{m['wr']*100:.0f}%"
            pf_str = f"{m['pf']:.2f}" if m['pf'] != float('inf') else "inf"
            verdict = ""
            if discard:
                verdict = f"❌ DISCARD: {reason}"
            elif m["pf"] >= 2.0 and m["n"] >= 3:
                verdict = "⭐ STRONG"
            elif m["pf"] >= 1.3 and m["expectancy"] > 0 and m["n"] >= 3:
                verdict = "✅ keep"
            elif m["pf"] < 1.0 and m["n"] >= 3:
                verdict = "⚠️ watch"
            print(f"{comment[:38]:<40}{m['n']:>5}{m['wins']:>4}{m['losses']:>4}"
                  f"{wr_str:>7}{pf_str:>7}{_fmt_money(m['net_pnl']):>13}"
                  f"{_fmt_money(m['expectancy']):>10}  {verdict}")

    # ─── Discard summary ───
    print(f"\n{'='*80}\nDISCARD CANDIDATES (all engines)\n{'='*80}")
    candidates = []
    for magic, dlist in by_magic.items():
        by_c: dict[str, list] = defaultdict(list)
        for d in dlist:
            by_c[str(getattr(d, "comment", "")).strip()].append(d)
        for c, dl in by_c.items():
            m = _aggregate(dl)
            discard, reason = _is_discard_candidate(m)
            if discard:
                candidates.append((_engine_name(magic), c, m, reason))
    if not candidates:
        print("None — all strategies look reasonable for the window")
    else:
        for eng, comment, m, reason in candidates:
            print(f"  [{eng}] '{comment[:40]}' — n={m['n']} WR={m['wr']*100:.0f}% "
                  f"PF={m['pf']:.2f} net={_fmt_money(m['net_pnl'])}  → {reason}")

    mt5.shutdown()


if __name__ == "__main__":
    main()
