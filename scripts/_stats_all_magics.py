"""Pull MT5 deal history grouped by magic, last N days. Run on VPS."""
import MetaTrader5 as mt5
from datetime import datetime, timezone, timedelta
from collections import defaultdict
mt5.initialize()

DAYS = 14
to = datetime.now(timezone.utc)
frm = to - timedelta(days=DAYS)
# Shift to broker time (EEST +3) because history_deals_get uses broker time
frm_b = frm + timedelta(hours=3)
to_b = to + timedelta(hours=3)

deals = mt5.history_deals_get(frm_b, to_b) or []
print(f"Total deals last {DAYS} days: {len(deals)}")

MAGICS = {1338: "MATH", 1339: "SWING", 1340: "ORB", 8338: "AMO8"}

# Group by (magic, symbol, strategy_id from comment)
agg = defaultdict(lambda: {"n": 0, "wins": 0, "losses": 0, "profit": 0.0, "rrs": []})
# Match deals into trades by position id
pos_deals = defaultdict(list)
for d in deals:
    if d.magic not in MAGICS:
        continue
    pos_deals[d.position_id].append(d)

trades = []
for pid, ds in pos_deals.items():
    ds.sort(key=lambda x: x.time)
    if len(ds) < 2:
        continue
    ent = ds[0]
    exits = ds[1:]
    pnl = sum(d.profit + d.commission + d.swap for d in exits) + (ent.commission + ent.swap)
    sym = ent.symbol
    magic = ent.magic
    comment = ent.comment
    trades.append((magic, sym, comment, pnl))

# Group by magic
by_magic = defaultdict(lambda: {"n":0,"win":0,"pnl":0.0,"wins_pnl":0.0,"loss_pnl":0.0})
by_magic_sym = defaultdict(lambda: {"n":0,"win":0,"pnl":0.0})
by_magic_strat = defaultdict(lambda: {"n":0,"win":0,"pnl":0.0})

for magic, sym, comment, pnl in trades:
    by_magic[magic]["n"] += 1
    by_magic[magic]["pnl"] += pnl
    by_magic_sym[(magic, sym)]["n"] += 1
    by_magic_sym[(magic, sym)]["pnl"] += pnl
    by_magic_strat[(magic, comment)]["n"] += 1
    by_magic_strat[(magic, comment)]["pnl"] += pnl
    if pnl > 0:
        by_magic[magic]["win"] += 1
        by_magic[magic]["wins_pnl"] += pnl
        by_magic_sym[(magic, sym)]["win"] += 1
        by_magic_strat[(magic, comment)]["win"] += 1
    else:
        by_magic[magic]["loss_pnl"] += abs(pnl)

print(f"\n=== AGGREGATE per MAGIC (last {DAYS} days) ===")
for mag, name in MAGICS.items():
    d = by_magic[mag]
    if d["n"] == 0:
        print(f"  {mag} {name:<8}: 0 trades")
        continue
    wr = d["win"]/d["n"]*100
    pf = d["wins_pnl"]/d["loss_pnl"] if d["loss_pnl"]>0 else float("inf")
    print(f"  {mag} {name:<8}: n={d['n']:<4} WR={wr:5.1f}% PnL=${d['pnl']:>+10.2f} PF={pf:.2f}")

print(f"\n=== PER SYMBOL per MAGIC ===")
for mag, name in MAGICS.items():
    keys = [k for k in by_magic_sym if k[0]==mag]
    if not keys: continue
    print(f"  --- {mag} {name} ---")
    for k in sorted(keys, key=lambda x: by_magic_sym[x]["pnl"]):
        d = by_magic_sym[k]
        wr = d["win"]/d["n"]*100 if d["n"]>0 else 0
        print(f"    {k[1]:<12} n={d['n']:<3} WR={wr:5.1f}% PnL=${d['pnl']:>+10.2f}")

print(f"\n=== BOTTOM 15 STRATEGIES (by PnL, n>=3) ===")
worst = sorted([(k,v) for k,v in by_magic_strat.items() if v["n"]>=3], key=lambda x: x[1]["pnl"])[:15]
for (mag, comment), d in worst:
    wr = d["win"]/d["n"]*100
    print(f"  {MAGICS.get(mag,mag):<8} {comment:<40} n={d['n']:<3} WR={wr:5.1f}% PnL=${d['pnl']:>+10.2f}")
print(f"\n=== TOP 15 STRATEGIES ===")
best = sorted([(k,v) for k,v in by_magic_strat.items() if v["n"]>=3], key=lambda x: -x[1]["pnl"])[:15]
for (mag, comment), d in best:
    wr = d["win"]/d["n"]*100
    print(f"  {MAGICS.get(mag,mag):<8} {comment:<40} n={d['n']:<3} WR={wr:5.1f}% PnL=${d['pnl']:>+10.2f}")

mt5.shutdown()
