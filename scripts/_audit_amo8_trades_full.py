"""Show ENTRY deals (not just exits) of the 56 AMO8 XAGUSD positions.

Verifies once-for-all that magic=8338 (AMO8) was the originator, not 1338 (MATH).
"""
import MetaTrader5 as mt5
from datetime import datetime, timezone, timedelta
from collections import defaultdict
mt5.initialize()

DAYS = 7
to = datetime.now(timezone.utc)
frm = to - timedelta(days=DAYS)
frm_b = frm + timedelta(hours=3)
to_b = to + timedelta(hours=3)
deals = mt5.history_deals_get(frm_b, to_b) or []

# Build position -> [entry_deal, exit_deals]
positions = defaultdict(lambda: {"entry": None, "exits": []})
for d in deals:
    if d.entry == 0:
        positions[d.position_id]["entry"] = d
    else:
        positions[d.position_id]["exits"].append(d)

# Filter to AMO8 (magic 8338) + XAGUSD
amo8_xag = []
for pid, pp in positions.items():
    ent = pp["entry"]
    if ent is None: continue
    if ent.magic != 8338: continue
    if ent.symbol != "XAGUSD": continue
    amo8_xag.append((pid, pp))

# Sort by entry time
amo8_xag.sort(key=lambda x: x[1]["entry"].time)
print(f"AMO8 (magic=8338) XAGUSD positions in last {DAYS} days: {len(amo8_xag)}")
print()
print(f"{'open_utc':<20} {'magic':>6} {'sym':<8} {'type':>4} {'vol':>5} {'open_px':>9} "
      f"{'close_utc':<20} {'close_px':>9} {'pnl':>10} {'hold':>8} {'entry_comment':<35} {'pos_id':>12}")

bot_hours = []
for pid, pp in amo8_xag:
    ent = pp["entry"]
    exits = sorted(pp["exits"], key=lambda d: d.time)
    last_exit = exits[-1] if exits else None
    open_utc = datetime.fromtimestamp(ent.time, tz=timezone.utc) - timedelta(hours=3)
    close_utc_str = ""; close_px = 0; pnl = 0; hold = ""
    if last_exit:
        close_utc = datetime.fromtimestamp(last_exit.time, tz=timezone.utc) - timedelta(hours=3)
        close_utc_str = close_utc.strftime("%Y-%m-%d %H:%M:%S")
        close_px = last_exit.price
        pnl = sum(d.profit + d.commission + d.swap for d in exits) + ent.commission + ent.swap
        hold_sec = (close_utc - open_utc).total_seconds()
        hold = f"{hold_sec/60:.0f}min" if hold_sec < 3600 else f"{hold_sec/3600:.1f}h"
        bot_hours.append(hold_sec)
    print(f"  {open_utc.strftime('%Y-%m-%d %H:%M:%S'):<18} {ent.magic:>6} {ent.symbol:<8} "
          f"{ent.type:>4} {ent.volume:>5.2f} {ent.price:>9.4f} "
          f"{close_utc_str:<20} {close_px:>9.4f} {pnl:>10.2f} {hold:>8} "
          f"{(ent.comment or '')[:34]:<35} {pid:>12}")

# Summary by entry hour (real UTC)
print()
print("=== AMO8 XAGUSD entries grouped by open hour (real UTC) ===")
hour_counts = defaultdict(int)
for pid, pp in amo8_xag:
    ent = pp["entry"]
    h = (datetime.fromtimestamp(ent.time, tz=timezone.utc) - timedelta(hours=3)).strftime("%Y-%m-%d %H:00")
    hour_counts[h] += 1
for k in sorted(hour_counts.keys()):
    print(f"  {k}: {hour_counts[k]} entries")

# Hold time distribution
if bot_hours:
    import statistics
    print()
    print(f"=== Hold time stats ({len(bot_hours)} closed positions) ===")
    print(f"  min:    {min(bot_hours)/60:.1f} min")
    print(f"  median: {statistics.median(bot_hours)/60:.1f} min")
    print(f"  max:    {max(bot_hours)/3600:.2f} h")

mt5.shutdown()
