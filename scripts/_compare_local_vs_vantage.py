"""Compare OR widths and atr_14 day-by-day between LOCAL backtest and VANTAGE
live M15 data, over their overlap window.

Reveals whether the same trading date produces same/different OR widths in
the two sources — which exposes the structural broker difference.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from datetime import datetime, timezone
import polars as pl
import MetaTrader5 as mt5
from src.application.calculators import DataEnricher
from src.application.orb_patterns import add_state_columns

mt5.initialize()
import time as _t
now_real = int(_t.time())
offset_h = 3
for sym in ("XAUUSD+","GBPUSD+","XAGUSD"):
    t = mt5.symbol_info_tick(sym)
    if t and int(t.time) > 0 and abs(int(t.time)-now_real) <= 300:
        offset_h = int(round((int(t.time)-now_real)/3600))
        break
offset_sec = offset_h*3600
print(f"Broker offset: +{offset_h}h\n")

PAIRS = [("GBPUSD","GBPUSD+",30), ("XAUUSD","XAUUSD+",30), ("NASDAQ100","NAS100",60), ("SP500","SP500",60), ("NATGAS","NG-C",60)]
MAGIC_TIME = "00:00"

for internal_sym, broker_sym, or_dur in PAIRS:
    print("="*70)
    print(f"=== {internal_sym} ({broker_sym}) — mt={MAGIC_TIME} dur={or_dur}m ===")
    # LOCAL
    local_path = f"data/enriched_math_tf/{internal_sym}_M15.parquet"
    if not Path(local_path).exists():
        print("  no local file"); continue
    ldf = pl.read_parquet(local_path).sort("time")
    le = DataEnricher.enrich_with_daily_context(ldf, "00:00", "23:59")
    leo = DataEnricher.enrich_with_opening_range(le, MAGIC_TIME, or_dur)
    leo = add_state_columns(leo)
    lpost = leo.filter(pl.col("is_post_or")).sort("time")
    lfirst = lpost.group_by("trade_date").agg([
        pl.col("or_high").first(), pl.col("or_low").first(),
        pl.col("atr_14").first(), pl.col("or_atr_ratio").first(),
        pl.col("or_atr_bucket").first(),
    ]).sort("trade_date")
    last_local_date = lfirst["trade_date"].max()
    print(f"  LOCAL: {len(lfirst)} days, last={last_local_date}")

    # VANTAGE
    rates = mt5.copy_rates_from_pos(broker_sym, mt5.TIMEFRAME_M15, 0, 7960)
    if rates is None:
        print("  no MT5 data"); continue
    vdf = pl.DataFrame({
        "time": [datetime.fromtimestamp(int(r["time"])-offset_sec, tz=None) for r in rates],
        "open": [float(r["open"]) for r in rates],
        "high": [float(r["high"]) for r in rates],
        "low":  [float(r["low"]) for r in rates],
        "close":[float(r["close"]) for r in rates],
    }).sort("time")
    ve = DataEnricher.enrich_with_daily_context(vdf, "00:00", "23:59")
    veo = DataEnricher.enrich_with_opening_range(ve, MAGIC_TIME, or_dur)
    veo = add_state_columns(veo)
    vpost = veo.filter(pl.col("is_post_or")).sort("time")
    vfirst = vpost.group_by("trade_date").agg([
        pl.col("or_high").first(), pl.col("or_low").first(),
        pl.col("atr_14").first(), pl.col("or_atr_ratio").first(),
        pl.col("or_atr_bucket").first(),
    ]).sort("trade_date")
    print(f"  VANTAGE: {len(vfirst)} days, last={vfirst['trade_date'].max()}")

    # Inner-join on trade_date
    join = lfirst.join(vfirst, on="trade_date", how="inner", suffix="_v").sort("trade_date")
    print(f"  OVERLAP: {len(join)} dates in common")
    if len(join) == 0:
        continue

    # Show last 8 overlap dates with side-by-side
    print(f"\n  {'date':<12} | {'L_or_w':>9} {'V_or_w':>9}  | {'L_atr':>9} {'V_atr':>9} | {'L_ratio':>8} {'V_ratio':>8} | {'L_bkt':<11} {'V_bkt':<11}")
    for r in join.tail(10).iter_rows(named=True):
        L_or_w = (r["or_high"] - r["or_low"]) if r["or_high"] and r["or_low"] else None
        V_or_w = (r["or_high_v"] - r["or_low_v"]) if r["or_high_v"] and r["or_low_v"] else None
        print(f"  {str(r['trade_date']):<12} | "
              f"{L_or_w if L_or_w else 'NA':>9.5f} {V_or_w if V_or_w else 'NA':>9.5f}  | "
              f"{r['atr_14'] or 0:>9.5f} {r['atr_14_v'] or 0:>9.5f} | "
              f"{r['or_atr_ratio'] or 0:>8.3f} {r['or_atr_ratio_v'] or 0:>8.3f} | "
              f"{str(r['or_atr_bucket']):<11} {str(r['or_atr_bucket_v']):<11}")

    # Aggregate stats over overlap
    join_clean = join.filter(pl.col("or_atr_ratio").is_not_null() & pl.col("or_atr_ratio_v").is_not_null())
    if len(join_clean) > 0:
        L_med_w = join_clean.select((pl.col("or_high")-pl.col("or_low")).median()).item()
        V_med_w = join_clean.select((pl.col("or_high_v")-pl.col("or_low_v")).median()).item()
        L_med_atr = join_clean["atr_14"].median()
        V_med_atr = join_clean["atr_14_v"].median()
        L_med_ratio = join_clean["or_atr_ratio"].median()
        V_med_ratio = join_clean["or_atr_ratio_v"].median()
        from collections import Counter
        L_bkts = Counter(join_clean["or_atr_bucket"].to_list())
        V_bkts = Counter(join_clean["or_atr_bucket_v"].to_list())
        print(f"\n  MEDIANS over {len(join_clean)} overlap days:")
        print(f"    OR_width:  LOCAL={L_med_w:.5f}  VANTAGE={V_med_w:.5f}  ratio V/L={V_med_w/max(L_med_w,1e-9):.2f}")
        print(f"    ATR(14):   LOCAL={L_med_atr:.5f}  VANTAGE={V_med_atr:.5f}  ratio V/L={V_med_atr/max(L_med_atr,1e-9):.2f}")
        print(f"    OR/ATR:    LOCAL={L_med_ratio:.3f}  VANTAGE={V_med_ratio:.3f}")
        print(f"    bucket counts:  LOCAL={dict(L_bkts)}  VANTAGE={dict(V_bkts)}")
    print()
mt5.shutdown()
