"""Run on VPS to check current ORB breakout state for symbols in 13:00 UTC window."""
import MetaTrader5 as mt5
from datetime import datetime, timezone, date

mt5.initialize()
# CRITICAL: Traders bot subtracts broker offset before checking ORB times,
# so all comparisons must be in REAL UTC. Detect offset from a fresh tick.
def _detect_offset_h():
    import time as _t
    now_real = int(_t.time())
    for sym in ("EURUSD+", "XAUUSD+", "XAGUSD"):
        t = mt5.symbol_info_tick(sym)
        if t and int(t.time) > 0:
            return int(round((int(t.time) - now_real) / 3600))
    return 3  # Vantage default
OFFSET_H = _detect_offset_h()
OFFSET_SEC = OFFSET_H * 3600
print(f"Broker offset detected: {OFFSET_H:+d}h")
print()


def _bar_real_utc(r):
    return datetime.fromtimestamp(int(r["time"]) - OFFSET_SEC, tz=timezone.utc)


ORB_SYMBOLS_1300 = [
    ("USOUSD", 13, 15, 180),
    ("UKOUSD", 13, 30, 180),
    ("NAS100", 13, 30, 180),
    ("SP500", 13, 30, 180),
    ("EURUSD+", 13, 15, 180),
    ("AUDUSD+", 13, 30, 180),
    ("XAGUSD", 13, 30, 180),
]
ORB_SYMBOLS_0700 = [
    ("GBPJPY+", 7, 30, 180),
    ("USDJPY+", 7, 15, 180),
    ("EURJPY+", 7, 15, 180),
    ("XAUUSD+", 7, 30, 180),
    ("GBPUSD+", 7, 15, 180),
    ("GBPAUD+", 7, 30, 180),
]
now = datetime.now(timezone.utc)
now_min = now.hour * 60 + now.minute
print(f"Real UTC now: {now.strftime('%Y-%m-%d %H:%M')} (min_of_day={now_min})")
print()

for label, syms in [("13:00 UTC window", ORB_SYMBOLS_1300), ("07:00 UTC window", ORB_SYMBOLS_0700)]:
    print(f"=== {label} ===")
    for sym, oh, rm, bw in syms:
        range_start_min = oh * 60
        range_end_min = range_start_min + rm
        window_end = range_end_min + bw
        in_window = range_end_min <= now_min < window_end
        rates = mt5.copy_rates_from_pos(sym, mt5.TIMEFRAME_M1, 0, 400)
        if rates is None or len(rates) == 0:
            print(f"  {sym}: NO DATA")
            continue
        # Filter today's range bars (use bar timestamp's date — broker as UTC convention OK for date filtering)
        today = _bar_real_utc(rates[-1]).date()
        # bars whose hour*60+min is within range window AND date is today
        range_bars = []
        for r in rates:
            t = _bar_real_utc(r)
            if t.date() != today:
                continue
            mod = t.hour * 60 + t.minute
            if range_start_min <= mod < range_end_min:
                range_bars.append(r)
        if not range_bars:
            print(f"  {sym} oh={oh} rm={rm}: 0 range bars today (market closed/holiday?)")
            continue
        r_high = max(float(b["high"]) for b in range_bars)
        r_low = min(float(b["low"]) for b in range_bars)
        last_close = float(rates[-1]["close"])
        broken = "YES" if last_close > r_high else "no"
        status = "ACTIVE" if in_window else ("PAST" if now_min >= window_end else "FUTURE")
        print(f"  {sym}: window={status} r=[{r_low:.4f}..{r_high:.4f}] last={last_close:.4f} broken_up={broken}  ({len(range_bars)} bars)")
mt5.shutdown()
