"""Pull last N M15 bars per symbol from VPS MT5 and save to parquet locally."""
import MetaTrader5 as mt5
import polars as pl
from datetime import datetime
import time as _t

mt5.initialize()
now_real = int(_t.time())
offset_h = 3
for sym in ("XAUUSD+","GBPUSD+","XAGUSD"):
    t = mt5.symbol_info_tick(sym)
    if t and int(t.time)>0 and abs(int(t.time)-now_real)<=300:
        offset_h = int(round((int(t.time)-now_real)/3600)); break
offset_sec = offset_h*3600
print(f"offset=+{offset_h}h")

PAIRS = [("XAUUSD","XAUUSD+"),("GBPUSD","GBPUSD+"),("NASDAQ100","NAS100"),
         ("SP500","SP500"),("NATGAS","NG-C")]

import os
os.makedirs("data/vantage_m15", exist_ok=True)
for internal, broker in PAIRS:
    rates = mt5.copy_rates_from_pos(broker, mt5.TIMEFRAME_M15, 0, 7960)
    if rates is None:
        print(f"{broker}: NO DATA"); continue
    df = pl.DataFrame({
        "time":[datetime.fromtimestamp(int(r["time"])-offset_sec, tz=None) for r in rates],
        "open":[float(r["open"]) for r in rates],
        "high":[float(r["high"]) for r in rates],
        "low": [float(r["low"]) for r in rates],
        "close":[float(r["close"]) for r in rates],
    }).sort("time")
    df.write_parquet(f"data/vantage_m15/{internal}_M15.parquet")
    print(f"{internal} ({broker}): {len(df)} bars, range {df['time'].min()} -> {df['time'].max()}")
mt5.shutdown()
