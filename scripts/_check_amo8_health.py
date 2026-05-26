"""Health check on AMO8 live state: comment prefixes, volume sanity per
symbol, broker_offset, timing alignment.

Run on VPS.
"""
import MetaTrader5 as mt5
from datetime import datetime, timezone, timedelta
from collections import defaultdict, Counter
import json
import time as _t

mt5.initialize()

# ─── 1) Broker offset (real test) ─────────────────────────────────────
now_real = int(_t.time())
deltas = []
for s in ("EURUSD+","XAUUSD+","GBPUSD+","XAGUSD","NG-C","USOUSD","NAS100"):
    t = mt5.symbol_info_tick(s)
    if t and int(t.time) > 0:
        d = int(t.time) - now_real
        deltas.append((s, d, d/3600))
print("=== BROKER OFFSET (tick.time - real_utc_now) ===")
for s, d, dh in deltas:
    print(f"  {s:<10} delta={d:+d}s = {dh:+.2f}h")
print()

# ─── 2) AMO8 trade history with full comment + volume ─────────────────
DAYS = 7
to = datetime.now(timezone.utc)
frm = to - timedelta(days=DAYS)
offset_sec = int(round(deltas[0][1]) if deltas else 0)
frm_b = frm + timedelta(seconds=offset_sec)
to_b = to + timedelta(seconds=offset_sec)
deals = mt5.history_deals_get(frm_b, to_b) or []

# Build position records
positions = {}
for d in deals:
    if d.magic != 8338: continue
    if d.entry == 0:
        positions[d.position_id] = {"entry": d, "exits": []}
    else:
        if d.position_id in positions:
            positions[d.position_id]["exits"].append(d)

print(f"=== AMO8 positions last {DAYS} days: {len(positions)} ===")
prefix_count = Counter()
sym_count = Counter()
sym_volume = defaultdict(list)
for pid, pp in positions.items():
    ent = pp["entry"]
    com = (ent.comment or "")
    prefix = com.split("|")[0] if com else "(empty)"
    prefix_count[prefix] += 1
    sym_count[ent.symbol] += 1
    sym_volume[ent.symbol].append(ent.volume)

print("\nComment prefix distribution (A8 = pre-2026-05-26 fix, AMO = post-fix):")
for p, n in prefix_count.most_common():
    print(f"  {p:<10} n={n}")
print("\nPer-symbol volume distribution:")
for sym in sorted(sym_volume):
    vols = sym_volume[sym]
    print(f"  {sym:<10} n={len(vols):<3}  min={min(vols):.2f}  median={sorted(vols)[len(vols)//2]:.2f}  max={max(vols):.2f}  unique={sorted(set(vols))}")

# ─── 3) Volume sanity check per symbol ────────────────────────────────
# Risk per trade = 0.0005, balance = ~current
acc = mt5.account_info()
balance = float(acc.balance) if acc else 0
risk_per_trade = 0.0005
print(f"\n=== Volume sanity check (balance=${balance:.0f}, risk_per_trade={risk_per_trade*100}%) ===")
print(f"Expected USD risk per trade: ${balance * risk_per_trade:.2f}")
print()

# Check NG-C specifically per user concern
for sym in ["NG-C", "XAGUSD", "USOUSD", "UKOUSD", "XAUUSD+", "GBPUSD+"]:
    info = mt5.symbol_info(sym)
    if not info: continue
    tick_size = info.trade_tick_size
    tick_value = info.trade_tick_value
    vol_min = info.volume_min
    vol_step = info.volume_step
    point = info.point
    # Typical OR width for the OR_dur each symbol uses
    # NG-C, USOUSD, UKOUSD typically 15min
    # Rough estimate: 0.5×OR_width as SL distance, sample current ATR
    rates_m15 = mt5.copy_rates_from_pos(sym, mt5.TIMEFRAME_M15, 0, 200)
    if rates_m15 is not None and len(rates_m15) > 14:
        ranges = [(r["high"] - r["low"]) for r in rates_m15[-50:]]
        median_range = sorted(ranges)[len(ranges)//2]
        # Assume SL = 0.5 × OR_width ≈ 0.5 × median_15min_range as proxy
        approx_sl_distance = 0.5 * median_range
        # USD per 1.0 lot per 1.0 price unit movement
        usd_per_price_per_lot = tick_value / tick_size if tick_size > 0 else 0
        # For risk_usd = volume × usd_per_price_per_lot × sl_distance
        # → volume = risk_usd / (usd_per_price_per_lot × sl_distance)
        risk_usd = balance * risk_per_trade
        ideal_vol = risk_usd / (usd_per_price_per_lot * approx_sl_distance) if (usd_per_price_per_lot * approx_sl_distance) > 0 else 0
        ideal_vol_rounded = round(ideal_vol / vol_step) * vol_step if vol_step > 0 else ideal_vol
        ideal_vol_rounded = max(ideal_vol_rounded, vol_min)
        print(f"  {sym:<10} tick_size={tick_size:<8} tick_value=${tick_value:<6.4f} vol_min={vol_min:<5} vol_step={vol_step:<5}")
        print(f"             median_M15_range={median_range:.5f}  approx_SL={approx_sl_distance:.5f}")
        print(f"             usd_per_lot_per_unit=${usd_per_price_per_lot:.2f}")
        print(f"             ideal_vol_for_${risk_usd:.2f}_risk = {ideal_vol:.4f} lots (rounded: {ideal_vol_rounded:.2f})")
        # What actually got traded
        if sym in sym_volume:
            actual = sorted(set(sym_volume[sym]))
            print(f"             ACTUAL volumes used: {actual}")
        print()
mt5.shutdown()
