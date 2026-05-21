"""On VPS: extract per-date OR/ATR stats from Vantage M15 and dump as JSON."""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from datetime import datetime
import MetaTrader5 as mt5
import polars as pl
from src.application.calculators import DataEnricher
from src.application.orb_patterns import add_state_columns
import time as _t

mt5.initialize()
now_real = int(_t.time())
offset_h = 3
for sym in ("XAUUSD+","GBPUSD+","XAGUSD"):
    t = mt5.symbol_info_tick(sym)
    if t and int(t.time)>0 and abs(int(t.time)-now_real)<=300:
        offset_h = int(round((int(t.time)-now_real)/3600)); break
offset_sec = offset_h*3600

PAIRS = [("XAUUSD","XAUUSD+",30),("GBPUSD","GBPUSD+",30),("NASDAQ100","NAS100",60),("SP500","SP500",60),("NATGAS","NG-C",60)]
out = {}
for internal, broker, or_dur in PAIRS:
    rates = mt5.copy_rates_from_pos(broker, mt5.TIMEFRAME_M15, 0, 7960)
    if rates is None: continue
    df = pl.DataFrame({
        "time":[datetime.fromtimestamp(int(r["time"])-offset_sec, tz=None) for r in rates],
        "open":[float(r["open"]) for r in rates],"high":[float(r["high"]) for r in rates],
        "low":[float(r["low"]) for r in rates],"close":[float(r["close"]) for r in rates],
    }).sort("time")
    e = DataEnricher.enrich_with_daily_context(df, "00:00", "23:59")
    eo = DataEnricher.enrich_with_opening_range(e, "00:00", or_dur)
    eo = add_state_columns(eo)
    post = eo.filter(pl.col("is_post_or")).sort("time")
    first = post.group_by("trade_date").agg([
        pl.col("or_high").first(), pl.col("or_low").first(),
        pl.col("atr_14").first(), pl.col("or_atr_ratio").first(),
        pl.col("or_atr_bucket").first(),
    ]).sort("trade_date")
    rows = []
    for r in first.iter_rows(named=True):
        rows.append({
            "date": str(r["trade_date"]),
            "or_high": r["or_high"], "or_low": r["or_low"],
            "atr_14": r["atr_14"], "or_atr_ratio": r["or_atr_ratio"],
            "bucket": r["or_atr_bucket"],
        })
    out[internal] = rows
mt5.shutdown()
Path("data").mkdir(exist_ok=True)
Path("data/vps_amo8_stats.json").write_text(json.dumps(out))
print(f"OK wrote {sum(len(v) for v in out.values())} rows across {len(out)} symbols")
