"""Verify MT5 broker time vs real UTC and bar timestamps. Run on VPS."""
import MetaTrader5 as mt5
import time
from datetime import datetime, timezone

mt5.initialize()

real_utc = datetime.now(timezone.utc)
print(f"Real UTC now : {real_utc.isoformat()}  (epoch={int(time.time())})")
print()

print("=== symbol_info_tick (live tick time = server clock) ===")
for sym in ["EURUSD+", "XAUUSD+", "GBPUSD+", "AUDUSD+", "XAGUSD"]:
    t = mt5.symbol_info_tick(sym)
    if t is None:
        print(f"  {sym}: tick=None")
        continue
    server_dt = datetime.fromtimestamp(int(t.time), tz=timezone.utc)
    offset = int(t.time) - int(time.time())
    h = round(offset / 3600)
    print(f"  {sym:10s}: server_time={server_dt.isoformat()}  offset={offset}s ({h:+d}h)  bid={t.bid}")

print()
print("=== Latest 3 bars per TF (EURUSD+) ===")
for tf_name, tf_const in [("M15", mt5.TIMEFRAME_M15), ("H1", mt5.TIMEFRAME_H1), ("H4", mt5.TIMEFRAME_H4)]:
    rates = mt5.copy_rates_from_pos("EURUSD+", tf_const, 0, 3)
    if rates is None:
        print(f"  {tf_name}: None")
        continue
    print(f"  {tf_name}:")
    for r in rates:
        bar_dt = datetime.fromtimestamp(int(r["time"]), tz=timezone.utc)
        print(f"    bar_time={bar_dt.isoformat()}  open={r['open']:.5f}  close={r['close']:.5f}")

print()
print("=== Math bot positions/orders (magic=1338) ===")
ps = mt5.positions_get() or []
math_ps = [p for p in ps if p.magic == 1338]
print(f"  Open positions : {len(math_ps)}")
for p in math_ps[:10]:
    setup_dt = datetime.fromtimestamp(int(p.time), tz=timezone.utc)
    print(f"    ticket={p.ticket} {p.symbol} comment='{p.comment}' opened={setup_dt.isoformat()} profit={p.profit:+.2f}")

ords = mt5.orders_get() or []
math_ords = [o for o in ords if o.magic == 1338]
print(f"  Pending orders : {len(math_ords)}")
for o in math_ords[:10]:
    setup_dt = datetime.fromtimestamp(int(o.time_setup), tz=timezone.utc)
    print(f"    ticket={o.ticket} {o.symbol} comment='{o.comment}' placed={setup_dt.isoformat()}")

mt5.shutdown()
