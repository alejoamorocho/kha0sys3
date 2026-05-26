"""Pull RAW MT5 deal records to confirm magic + comment + symbol of suspected AMO8 trades.

The previous stats showed $17,780 loss attributed to magic=8338 (AMO8). User suspects
they may actually be from magic=1338 (MATH). This script prints raw deal fields
so we can verify the attribution definitively.
"""
import MetaTrader5 as mt5
from datetime import datetime, timezone, timedelta
mt5.initialize()

DAYS = 7
to = datetime.now(timezone.utc)
frm = to - timedelta(days=DAYS)
frm_b = frm + timedelta(hours=3)
to_b = to + timedelta(hours=3)
deals = mt5.history_deals_get(frm_b, to_b) or []

# Show every deal on XAGUSD with non-empty comment, sorted by time
xag = [d for d in deals if d.symbol == "XAGUSD"]
xag.sort(key=lambda d: d.time)
print(f"Total deals last {DAYS} days: {len(deals)}  (XAGUSD: {len(xag)})")
print()
print(f"{'time':<20} {'magic':>6} {'type':>4} {'entry':>5} {'volume':>7} {'price':>9} {'profit':>10} {'comment':<35} {'pos_id':>12}")
for d in xag:
    t = datetime.fromtimestamp(d.time, tz=timezone.utc) - timedelta(hours=3)  # broker -> real UTC
    # type: 0=BUY 1=SELL  entry: 0=IN 1=OUT
    print(f"  {t.strftime('%Y-%m-%d %H:%M:%S'):<18} {d.magic:>6} {d.type:>4} {d.entry:>5} {d.volume:>7.2f} {d.price:>9.4f} {d.profit:>10.2f} {(d.comment or '')[:34]:<35} {d.position_id:>12}")

# Also show summary by magic
print()
print("=== Summary all symbols by magic ===")
from collections import defaultdict
agg = defaultdict(lambda: {"n":0, "pnl":0.0})
pos_in = {}
for d in deals:
    if d.entry == 0:  # entry deal
        pos_in[d.position_id] = d
for d in deals:
    if d.entry == 1 and d.position_id in pos_in:  # exit deal
        ent = pos_in[d.position_id]
        agg[(ent.magic, ent.symbol)]["n"] += 1
        agg[(ent.magic, ent.symbol)]["pnl"] += d.profit + d.commission + d.swap + ent.commission + ent.swap

for (magic, sym), v in sorted(agg.items()):
    print(f"  magic={magic} sym={sym:<10} n={v['n']:<3} pnl={v['pnl']:+.2f}")

mt5.shutdown()
