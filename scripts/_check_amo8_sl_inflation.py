"""Inspect the actual SL distances on AMO8 NG-C / WTI / BRENT positions and
compare to the OR-width-based ideal distances from config.

Reveals exactly how much the stops_level guard is inflating SLs and whether
the geometry of trades matches the backtest contract.
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

# Build positions
positions = {}
for d in deals:
    if d.magic != 8338: continue
    if d.entry == 0:
        positions[d.position_id] = {"entry": d, "exits": []}
    else:
        if d.position_id in positions:
            positions[d.position_id]["exits"].append(d)

# For each position: entry.sl, entry.tp (from MT5), compute distance
print(f"{'symbol':<10} {'open_px':>10} {'sl':>10} {'tp':>10} {'sl_dist':>10} {'tp_dist':>10} {'sl_pct':>7} {'rr':>5}  {'vol':>5}  {'comment':<25}")
for pid, pp in positions.items():
    ent = pp["entry"]
    sym = ent.symbol
    if sym not in ("NG-C", "USOUSD", "UKOUSD", "GBPUSD+", "XAGUSD", "XAUUSD+", "SP500", "NAS100"):
        continue
    sl = ent.sl; tp = ent.tp; px = ent.price
    sl_dist = abs(px - sl) if sl else 0
    tp_dist = abs(px - tp) if tp else 0
    sl_pct = (sl_dist / px * 100) if px > 0 else 0
    rr = tp_dist / sl_dist if sl_dist > 0 else 0
    print(f"  {sym:<10} {px:>10.5f} {sl:>10.5f} {tp:>10.5f} {sl_dist:>10.5f} {tp_dist:>10.5f} {sl_pct:>6.3f}% {rr:>5.2f}  {ent.volume:>5.2f}  {(ent.comment or '')[:24]:<25}")

# For NG-C specifically: what does the broker require as min stop dist?
print()
print("=== Broker stops_level / spread per symbol ===")
for sym in ["NG-C", "USOUSD", "UKOUSD", "GBPUSD+", "XAGUSD", "XAUUSD+", "SP500", "NAS100"]:
    info = mt5.symbol_info(sym)
    if not info: continue
    tick = mt5.symbol_info_tick(sym)
    if not tick: continue
    bid = tick.bid; ask = tick.ask
    spread = ask - bid
    stops_lvl_pts = float(info.trade_stops_level)
    point = info.point
    min_stop_pts = stops_lvl_pts * point
    spread3 = 3 * spread
    pct01 = 0.001 * ask  # 0.1% of price (our 3rd guard term)
    bot_guard = max(2*min_stop_pts, spread3, pct01)
    print(f"  {sym:<10} bid={bid:.5f} ask={ask:.5f} spread={spread:.5f}")
    print(f"             stops_level={stops_lvl_pts:.0f}pts × point={point} = {min_stop_pts:.5f}")
    print(f"             bot_guard = max(2×stops_lvl={2*min_stop_pts:.5f}, 3×spread={spread3:.5f}, 0.1%×ask={pct01:.5f}) = {bot_guard:.5f}")
    print(f"             → MIN SL distance bot will allow = {bot_guard:.5f}")

mt5.shutdown()
