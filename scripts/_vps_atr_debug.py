"""Dump per-day max single-M15-bar range to detect outlier bars on Vantage."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from datetime import datetime
import MetaTrader5 as mt5
import polars as pl
import json
import time as _t

mt5.initialize()
now_real = int(_t.time())
offset_h = 3
for sym in ("XAUUSD+","GBPUSD+","XAGUSD"):
    t = mt5.symbol_info_tick(sym)
    if t and int(t.time)>0 and abs(int(t.time)-now_real)<=300:
        offset_h = int(round((int(t.time)-now_real)/3600)); break
offset_sec = offset_h*3600

out = {}
for internal, broker in [("XAUUSD","XAUUSD+"),("GBPUSD","GBPUSD+"),("NASDAQ100","NAS100"),("SP500","SP500"),("NATGAS","NG-C")]:
    rates = mt5.copy_rates_from_pos(broker, mt5.TIMEFRAME_M15, 0, 7960)
    if rates is None: continue
    df = pl.DataFrame({
        "time":[datetime.fromtimestamp(int(r["time"])-offset_sec, tz=None) for r in rates],
        "open":[float(r["open"]) for r in rates],"high":[float(r["high"]) for r in rates],
        "low":[float(r["low"]) for r in rates],"close":[float(r["close"]) for r in rates],
    }).sort("time")
    df = df.with_columns([
        (pl.col("high") - pl.col("low")).alias("bar_range"),
        pl.col("time").dt.date().alias("trade_date"),
    ])
    # per-day stats
    daily = df.group_by("trade_date").agg([
        pl.len().alias("n"),
        pl.col("bar_range").max().alias("max_bar_range"),
        pl.col("bar_range").median().alias("med_bar_range"),
        (pl.col("high").max() - pl.col("low").min()).alias("d_range"),
        pl.col("high").max().alias("d_high"),
        pl.col("low").min().alias("d_low"),
    ]).sort("trade_date")
    # Look for outliers: bars where range >> median
    last_dates = daily.tail(10)
    rows = []
    for r in last_dates.iter_rows(named=True):
        ratio = r["max_bar_range"]/max(r["med_bar_range"],1e-9)
        rows.append({
            "date": str(r["trade_date"]), "n_bars": r["n"],
            "max_bar_range": r["max_bar_range"], "med_bar_range": r["med_bar_range"],
            "outlier_ratio": round(ratio,1), "d_range": r["d_range"],
            "d_high": r["d_high"], "d_low": r["d_low"],
        })
    out[internal] = rows

Path("data").mkdir(exist_ok=True)
Path("data/vps_atr_debug.json").write_text(json.dumps(out, indent=2))
print("OK")
