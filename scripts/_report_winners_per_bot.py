"""Comprehensive winners report per bot: AMO8, MATH, ORB, SWING.

For each magic, breaks down trades by (symbol, strategy comment) showing:
  trades, WR, PF, total PnL, avg PnL/trade, best/worst trade.

Window: last 30 days (full sample post-deployment).
Run on VPS where MT5 is connected.
"""
import MetaTrader5 as mt5
from datetime import datetime, timezone, timedelta
from collections import defaultdict
mt5.initialize()

DAYS = 30
to = datetime.now(timezone.utc)
frm = to - timedelta(days=DAYS)
frm_b = frm + timedelta(hours=3)
to_b = to + timedelta(hours=3)
deals = mt5.history_deals_get(frm_b, to_b) or []

MAGICS = {1338: "MATH", 1339: "SWING", 1340: "ORB", 8338: "AMO8"}

# Build positions: entry + exits
positions = {}
for d in deals:
    if d.magic not in MAGICS:
        continue
    if d.entry == 0:
        positions[d.position_id] = {"ent": d, "exits": []}
    elif d.position_id in positions:
        positions[d.position_id]["exits"].append(d)

# Compute PnL per closed position
closed_trades = []
for pid, pp in positions.items():
    if not pp["exits"]:
        continue
    ent = pp["ent"]
    pnl = sum(d.profit + d.commission + d.swap for d in pp["exits"])
    pnl += ent.commission + ent.swap
    closed_trades.append({
        "magic": ent.magic,
        "sym": ent.symbol,
        "comment": ent.comment or "(empty)",
        "pnl": pnl,
        "vol": ent.volume,
        "open_time": ent.time,
    })

print(f"Last {DAYS} days: {len(closed_trades)} closed trades across all 4 bots\n")


def fmt_pf(wins_sum, losses_sum):
    if losses_sum == 0:
        return "INF" if wins_sum > 0 else "—"
    return f"{wins_sum/losses_sum:.2f}"


def aggregate(trades, group_keys):
    """Group trades by tuple of keys; compute stats."""
    grp = defaultdict(list)
    for t in trades:
        k = tuple(t[k] for k in group_keys)
        grp[k].append(t)
    rows = []
    for k, ts in grp.items():
        pnls = [t["pnl"] for t in ts]
        n = len(pnls)
        wins = [p for p in pnls if p > 0]
        losses = [p for p in pnls if p < 0]
        wins_sum = sum(wins)
        losses_sum = abs(sum(losses))
        wr = len(wins) / n if n else 0
        rows.append({
            "key": k, "n": n,
            "wins": len(wins), "losses": len(losses),
            "wr": wr,
            "pf": (wins_sum / losses_sum) if losses_sum > 0 else (float("inf") if wins_sum > 0 else 0),
            "total_pnl": sum(pnls),
            "avg_pnl": sum(pnls) / n,
            "best": max(pnls) if pnls else 0,
            "worst": min(pnls) if pnls else 0,
        })
    return rows


# ─── Report per bot ──────────────────────────────────────────────────
for mg, bot in MAGICS.items():
    bot_trades = [t for t in closed_trades if t["magic"] == mg]
    if not bot_trades:
        print(f"┌{'─'*70}┐")
        print(f"│ {bot} (magic {mg}): 0 closed trades in window  │")
        print(f"└{'─'*70}┘\n")
        continue

    total_pnl = sum(t["pnl"] for t in bot_trades)
    total_n = len(bot_trades)
    wins = [t for t in bot_trades if t["pnl"] > 0]
    losses = [t for t in bot_trades if t["pnl"] < 0]
    wr = len(wins)/total_n if total_n else 0
    pf = fmt_pf(sum(t["pnl"] for t in wins), abs(sum(t["pnl"] for t in losses)))

    print(f"\n{'='*80}")
    print(f"  {bot}  (magic {mg})  —  {DAYS} days")
    print(f"{'='*80}")
    print(f"  TOTAL:  trades={total_n}   WR={wr*100:.1f}%   PF={pf}   PnL=${total_pnl:+,.2f}\n")

    # Per-symbol breakdown sorted by total PnL
    print(f"  -- PER SYMBOL --")
    print(f"  {'symbol':<12} {'n':>4} {'WR':>6} {'PF':>6} {'total':>11} {'avg':>9} {'best':>9} {'worst':>9}")
    by_sym = aggregate(bot_trades, ["sym"])
    by_sym.sort(key=lambda r: -r["total_pnl"])
    for r in by_sym:
        sym = r["key"][0]
        pf_str = "INF" if r["pf"] == float("inf") else f"{r['pf']:.2f}"
        emoji = "✓" if r["total_pnl"] > 0 else ("·" if r["total_pnl"] == 0 else "✗")
        print(f"  {emoji} {sym:<10} {r['n']:>4} {r['wr']*100:>5.1f}% {pf_str:>6} ${r['total_pnl']:>+9.2f} ${r['avg_pnl']:>+7.2f} ${r['best']:>+7.2f} ${r['worst']:>+7.2f}")

    # Per-strategy (sym + comment short)
    for t in bot_trades:
        c = t["comment"]
        # Trim comment to identifier (strip transient suffixes like SL/TP marks)
        t["strat_short"] = c.replace("[sl ", "").split("]")[0][:30]
    print()
    print(f"  -- PER STRATEGY (sym + comment, top 25 by PnL) --")
    print(f"  {'symbol':<10} {'strategy':<32} {'n':>4} {'WR':>6} {'PF':>6} {'total':>11} {'avg':>9}")
    by_strat = aggregate(bot_trades, ["sym", "strat_short"])
    by_strat.sort(key=lambda r: -r["total_pnl"])
    # Show all with n>=3 + top 25
    shown = 0
    for r in by_strat:
        if r["n"] < 3 and shown >= 25:
            continue
        sym, strat = r["key"]
        pf_str = "INF" if r["pf"] == float("inf") else f"{r['pf']:.2f}"
        emoji = "✓" if r["total_pnl"] > 0 else ("·" if r["total_pnl"] == 0 else "✗")
        print(f"  {emoji} {sym:<8} {strat:<32} {r['n']:>4} {r['wr']*100:>5.1f}% {pf_str:>6} ${r['total_pnl']:>+9.2f} ${r['avg_pnl']:>+7.2f}")
        shown += 1

# ─── Combined ranking: top winners across all bots ────────────────────
print(f"\n\n{'='*80}")
print(f"  TOP 20 WINNING (sym × strategy) ACROSS ALL BOTS  ({DAYS} days, n>=3)")
print(f"{'='*80}")
all_by_strat = aggregate(closed_trades, ["magic", "sym", "strat_short"])
all_by_strat = [r for r in all_by_strat if r["n"] >= 3]
all_by_strat.sort(key=lambda r: -r["total_pnl"])
print(f"  {'bot':<6} {'sym':<10} {'strategy':<28} {'n':>3} {'WR':>5} {'PF':>5} {'total':>10}")
for r in all_by_strat[:20]:
    mg, sym, strat = r["key"]
    bot = MAGICS.get(mg, "?")
    pf_str = "INF" if r["pf"] == float("inf") else f"{r['pf']:.2f}"
    print(f"  {bot:<6} {sym:<10} {strat:<28} {r['n']:>3} {r['wr']*100:>4.0f}% {pf_str:>5} ${r['total_pnl']:>+8.2f}")

print(f"\n  TOP 20 LOSING (sym × strategy)  ({DAYS} days, n>=3)")
print(f"{'─'*80}")
print(f"  {'bot':<6} {'sym':<10} {'strategy':<28} {'n':>3} {'WR':>5} {'PF':>5} {'total':>10}")
for r in all_by_strat[-20:]:
    mg, sym, strat = r["key"]
    bot = MAGICS.get(mg, "?")
    pf_str = "INF" if r["pf"] == float("inf") else f"{r['pf']:.2f}"
    print(f"  {bot:<6} {sym:<10} {strat:<28} {r['n']:>3} {r['wr']*100:>4.0f}% {pf_str:>5} ${r['total_pnl']:>+8.2f}")

mt5.shutdown()
