"""Pull MT5 deal history grouped by magic, last N days (post-purge window). Run on VPS."""
import MetaTrader5 as mt5
from datetime import datetime, timezone, timedelta
from collections import defaultdict
mt5.initialize()

DAYS = 5
to = datetime.now(timezone.utc)
frm = to - timedelta(days=DAYS)
frm_b = frm + timedelta(hours=3)
to_b = to + timedelta(hours=3)

deals = mt5.history_deals_get(frm_b, to_b) or []
MAGICS = {1338: "MATH", 1339: "SWING", 1340: "ORB", 8338: "AMO8"}

pos_deals = defaultdict(list)
for d in deals:
    if d.magic not in MAGICS:
        continue
    pos_deals[d.position_id].append(d)

trades = []
for pid, ds in pos_deals.items():
    ds.sort(key=lambda x: x.time)
    if len(ds) < 2: continue
    ent = ds[0]
    exits = ds[1:]
    pnl = sum(d.profit + d.commission + d.swap for d in exits) + (ent.commission + ent.swap)
    trades.append((ent.magic, ent.symbol, ent.comment, pnl))

print(f"Post-purge {DAYS}-day window: {len(trades)} trades\n")

strat_agg = defaultdict(lambda: {"n":0,"wins":0,"pnl":0.0})
for magic, sym, comment, pnl in trades:
    key = (magic, sym, comment[:35] if comment else "")
    strat_agg[key]["n"] += 1
    if pnl > 0: strat_agg[key]["wins"] += 1
    strat_agg[key]["pnl"] += pnl

for mg, name in MAGICS.items():
    rows = sorted([(k,v) for k,v in strat_agg.items() if k[0]==mg], key=lambda x:x[1]["pnl"])
    if not rows:
        print(f"=== {name} (magic {mg}): 0 trades post-purge ===\n")
        continue
    total_n = sum(r[1]["n"] for r in rows)
    total_pnl = sum(r[1]["pnl"] for r in rows)
    total_w = sum(r[1]["wins"] for r in rows)
    wr = total_w/total_n if total_n else 0
    print(f"=== {name} (magic {mg}): n={total_n} WR={wr*100:.1f}% PnL=${total_pnl:+.2f} ===")
    for (mg_, sym, comment), v in rows:
        wr_s = v["wins"]/v["n"]*100 if v["n"] else 0
        marker = "LOSS" if v["pnl"] < 0 else ("WIN " if v["pnl"] > 0 else "BE  ")
        print(f"  {marker} {sym:<10} {comment:<35} n={v['n']:<3} WR={wr_s:>5.1f}% PnL=${v['pnl']:+.2f}")
    print()
mt5.shutdown()
