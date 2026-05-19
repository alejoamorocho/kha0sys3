"""Check M15 bars at 00:00-00:30 broker time for each AMO8 symbol."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import MetaTrader5 as mt5
from datetime import datetime, timezone

mt5.initialize()

SYMS = ["XAUUSD+", "GBPUSD+", "NAS100", "NG-C", "SP500"]

for sym in SYMS:
    rates = mt5.copy_rates_from_pos(sym, mt5.TIMEFRAME_M15, 0, 200)
    if rates is None or len(rates) == 0:
        print(f"{sym}: NO M15 BARS"); continue
    today_date = datetime.fromtimestamp(int(rates[-1]["time"]), tz=timezone.utc).date()
    print(f"\n=== {sym} (M15, n={len(rates)}, last bar broker-time {datetime.fromtimestamp(int(rates[-1]['time']), tz=timezone.utc)}) ===")
    # Show bars from today date 00:00 to 01:00 broker
    for r in rates[-200:]:
        t = datetime.fromtimestamp(int(r["time"]), tz=timezone.utc)
        if t.date() == today_date and t.hour == 0:
            print(f"  {t}  o={r['open']:.5f} h={r['high']:.5f} l={r['low']:.5f} c={r['close']:.5f}")
    # also yesterday
    print(f"  -- yesterday 00:00-01:00 --")
    from datetime import timedelta
    yest = today_date - timedelta(days=1)
    for r in rates[-200:]:
        t = datetime.fromtimestamp(int(r["time"]), tz=timezone.utc)
        if t.date() == yest and t.hour == 0:
            print(f"  {t}  o={r['open']:.5f} h={r['high']:.5f} l={r['low']:.5f} c={r['close']:.5f}")
mt5.shutdown()
