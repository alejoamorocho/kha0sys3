"""Probe maximum M1 history available per symbol on the live MT5 terminal.

Tries copy_rates_from_pos with successively larger N until MT5 returns fewer
bars than requested (= we hit the end of history). Reports oldest bar date,
total count, approx calendar days for the 6 active math symbols plus all
FADE symbols (for reference).
"""
from __future__ import annotations
import sys
from datetime import datetime, timezone
import MetaTrader5 as mt5


SYMBOLS = [
    # math 6
    "XAUUSD+", "GBPAUD+", "NAS100", "EURJPY+",
    # FADE universe (for reference — also on Vantage)
    "EURUSD+", "GBPUSD+", "USDJPY+", "AUDUSD+", "GBPJPY+",
    "XAGUSD", "USOUSD", "UKOUSD", "NG-C", "SP500", "VIX",
]


def probe(symbol: str):
    info = mt5.symbol_info(symbol)
    if info is None:
        return {"symbol": symbol, "error": "symbol_info None"}
    if not info.visible:
        mt5.symbol_select(symbol, True)

    # Try progressively bigger N until we stop getting more bars.
    # MT5 typical limit: broker-dependent. Vantage ECN has varied 200k-1M+.
    best = None
    for N in (50_000, 200_000, 500_000, 1_000_000, 2_000_000, 5_000_000):
        rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, N)
        if rates is None or len(rates) == 0:
            break
        got = len(rates)
        if best is None or got > best["count"]:
            best = {
                "count": got,
                "oldest": datetime.fromtimestamp(int(rates[0]["time"]), tz=timezone.utc),
                "newest": datetime.fromtimestamp(int(rates[-1]["time"]), tz=timezone.utc),
            }
        if got < N:
            # MT5 exhausted its store at this N — no point asking for more
            break
    if best is None:
        return {"symbol": symbol, "error": "no M1 data"}
    span_days = (best["newest"] - best["oldest"]).total_seconds() / 86400
    return {
        "symbol": symbol,
        "count": best["count"],
        "oldest": best["oldest"].strftime("%Y-%m-%d %H:%M"),
        "newest": best["newest"].strftime("%Y-%m-%d %H:%M"),
        "span_days": round(span_days, 1),
        "span_years": round(span_days / 365.25, 2),
    }


def main():
    if not mt5.initialize():
        print("MT5 init failed:", mt5.last_error()); return 1
    print(f"{'SYMBOL':<10} {'BARS':>10} {'OLDEST':<17} {'NEWEST':<17} {'DAYS':>7} {'YEARS':>6}")
    print("-" * 75)
    total = 0
    for sym in SYMBOLS:
        r = probe(sym)
        if "error" in r:
            print(f"{sym:<10} ERROR: {r['error']}")
            continue
        total += r["count"]
        print(f"{sym:<10} {r['count']:>10,} {r['oldest']:<17} {r['newest']:<17} "
              f"{r['span_days']:>7} {r['span_years']:>6}")
    print("-" * 75)
    print(f"TOTAL bars across probed symbols: {total:,}")
    mt5.shutdown()


if __name__ == "__main__":
    sys.exit(main() or 0)
