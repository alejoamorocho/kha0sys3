"""Diagnostico timezone MT5 vs UTC real.

Imprime:
  - hora UTC real actual
  - ultima barra M1 que reporta MT5 (epoch + interpretado as_UTC + as_LOCAL)
  - tick mas reciente (epoch + as_UTC)
  - broker_offset implicado
"""
import sys
import MetaTrader5 as mt5
from datetime import datetime, timezone


def main():
    mt5.initialize()
    now_utc = datetime.now(timezone.utc)
    print(f"Real UTC now:   {now_utc.isoformat()}")
    print(f"Real UTC epoch: {int(now_utc.timestamp())}")
    print()
    rates = mt5.copy_rates_from_pos("XAUUSD", mt5.TIMEFRAME_M1, 0, 3)
    if rates is not None:
        print("MT5 M1 bars (last 3):")
        for r in rates:
            epoch = int(r["time"])
            t_as_utc = datetime.fromtimestamp(epoch, tz=timezone.utc)
            t_naive = datetime.fromtimestamp(epoch)
            offset_h = (epoch - int(now_utc.timestamp())) / 3600
            print(f"  epoch={epoch}  decoded_as_UTC={t_as_utc.isoformat()}  "
                  f"decoded_as_LOCAL={t_naive.isoformat()}  delta_h_vs_now_utc={offset_h:+.2f}")
    tick = mt5.symbol_info_tick("XAUUSD")
    if tick:
        t_tick = datetime.fromtimestamp(int(tick.time), tz=timezone.utc)
        offset = (int(tick.time) - int(now_utc.timestamp())) / 3600
        print(f"\nLast tick XAUUSD: epoch={tick.time}  as_UTC={t_tick.isoformat()}  "
              f"delta_h_vs_now_utc={offset:+.2f}")
        if abs(offset) > 0.5:
            print(f"  -> Broker server is offset by ~{round(offset)}h vs real UTC.")
            print(f"  -> Bars stamped at hour X in broker time = real UTC hour X-{round(offset)}.")
    mt5.shutdown()


if __name__ == "__main__":
    main()
