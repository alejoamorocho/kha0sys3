"""Same v2 logic but on LOCAL backtest data, last 60 trading days."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import json
from datetime import timedelta
from collections import defaultdict, Counter
import polars as pl
from src.application.calculators import DataEnricher
from src.application.orb_patterns import add_state_columns

cfg = json.loads(Path("src/execution/bot_config_amo8.json").read_text(encoding="utf-8"))
ports = cfg["portfolio"]
slots = defaultdict(list)
for s in ports:
    slots[(s["internal_sym"], s["magic_time"], int(s["or_duration_min"]))].append(s)

SYM_TO_FILE = {
    "XAUUSD":"data/enriched_math_tf/XAUUSD_M15.parquet",
    "GBPUSD":"data/enriched_math_tf/GBPUSD_M15.parquet",
    "NASDAQ100":"data/enriched_math_tf/NASDAQ100_M15.parquet",
    "NATGAS":"data/enriched_math_tf/NATGAS_M15.parquet",
    "SP500":"data/enriched_math_tf/SP500_M15.parquet",
}

# Two windows: ALL 8 years vs LAST 60 trading days
for window_name, lookback in [("ALL 8y", None), ("LAST 60 trading days", 60)]:
    print("="*70)
    print(f"WINDOW: {window_name}")
    print("="*70)
    totals = {"days":0,"expanded":0,"matchable":0,"fires":0}
    for (sym, mt_utc, or_dur), configs in slots.items():
        path = SYM_TO_FILE.get(sym)
        if not Path(path).exists(): continue
        df = pl.read_parquet(path).sort("time")
        enriched = DataEnricher.enrich_with_daily_context(df, "00:00","23:59")
        enriched_or = DataEnricher.enrich_with_opening_range(enriched, mt_utc, or_dur)
        enriched_or = add_state_columns(enriched_or)
        post_or = enriched_or.filter(pl.col("is_post_or")).sort("time")
        if len(post_or)==0: continue
        first = post_or.group_by("trade_date").agg([
            pl.col("or_atr_bucket").first(),
            pl.col("pd_or_overlap_bucket").first(),
            pl.col("or_position_vs_pd").first(),
            pl.col("atr_14").first(),
        ]).sort("trade_date")
        if lookback is not None:
            last_d = first["trade_date"].max()
            first = first.filter(pl.col("trade_date") >= last_d - timedelta(days=lookback))
        days=0; exp=0; match=0; fires=0
        for r in first.iter_rows(named=True):
            if r["atr_14"] is None: continue
            days += 1
            if r["or_atr_bucket"]=="expanded": exp += 1
            matches = [c for c in configs
                if c["or_position"]==r["or_position_vs_pd"]
                and c["or_atr_bucket"]==r["or_atr_bucket"]
                and c["pd_or_bucket"]==r["pd_or_overlap_bucket"]]
            if matches:
                match += 1; fires += len(matches)
        totals["days"]+=days; totals["expanded"]+=exp; totals["matchable"]+=match; totals["fires"]+=fires
        print(f"  {sym:<10} mt={mt_utc} {or_dur}m: days={days:<5} expanded={exp:<5} ({exp/max(days,1)*100:.0f}%) "
              f"matchable={match:<4} fires={fires}")
    print(f"\n  TOTALS: days={totals['days']} expanded={totals['expanded']} "
          f"({totals['expanded']/max(totals['days'],1)*100:.1f}%) "
          f"matchable={totals['matchable']} fires={totals['fires']}")
    if lookback:
        print(f"  fires/day avg: {totals['fires']/lookback:.2f}  (backtest report claims 10.47/day)")
    print()
