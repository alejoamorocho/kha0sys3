# src/strategies_external/strategies/sma18.py
"""Inna Rosputnia SMA-18 — daily trend-following with inside-day filter.

Long: low[t-1] > SMA18[t-1] AND low[t-2] > SMA18[t-2] AND neither is
inside-day. Buy stop @ max(high[t-1], high[t-2]) + 1 tick on bar t.
Short: symmetric.
"""

from datetime import timedelta

import polars as pl

from src.strategies_external.common.signal import Signal
from src.strategies_external.strategies.base import Strategy


_TICK = 0.01


class SMA18Strategy(Strategy):
    name = "sma18"

    def __init__(self, sma_window: int = 18, atr_window: int = 14):
        self.sma_window = sma_window
        self.atr_window = atr_window

    def generate_signals(self, df: pl.DataFrame, symbol: str) -> list[Signal]:
        min_bars = max(self.sma_window, self.atr_window) + 3
        if df.is_empty() or df.shape[0] < min_bars:
            return []

        enriched = (
            df.with_columns(
                pl.col("close").rolling_mean(self.sma_window).alias("sma"),
                pl.max_horizontal(
                    pl.col("high") - pl.col("low"),
                    (pl.col("high") - pl.col("close").shift(1)).abs(),
                    (pl.col("low") - pl.col("close").shift(1)).abs(),
                ).alias("tr"),
            )
            .with_columns(pl.col("tr").rolling_mean(self.atr_window).alias("atr"))
            .with_columns(
                ((pl.col("high") < pl.col("high").shift(1))
                 & (pl.col("low") > pl.col("low").shift(1))).alias("inside")
            )
        )
        rows = enriched.to_dicts()
        signals: list[Signal] = []

        for i in range(2, len(rows)):
            cur = rows[i]
            p1 = rows[i - 1]
            p2 = rows[i - 2]
            sma_p1 = p1.get("sma")
            sma_p2 = p2.get("sma")
            sma_cur = cur.get("sma")
            atr_cur = cur.get("atr") or 0.0
            if sma_p1 is None or sma_p2 is None or sma_cur is None:
                continue

            inside_p1 = bool(p1.get("inside"))
            inside_p2 = bool(p2.get("inside"))
            valid_until = cur["time"] + timedelta(days=1) - timedelta(seconds=1)
            anchors = {"sma18": sma_cur, "atr14": atr_cur,
                       "high_p1": p1["high"], "high_p2": p2["high"],
                       "low_p1": p1["low"], "low_p2": p2["low"]}

            # Long
            if (p1["low"] > sma_p1 and p2["low"] > sma_p2
                    and not inside_p1 and not inside_p2):
                buy_stop = max(p1["high"], p2["high"]) + _TICK
                signals.append(Signal(
                    symbol=symbol, strategy=self.name, side="long",
                    setup_ts=cur["time"], entry_type="stop",
                    entry_price=buy_stop,
                    valid_until=valid_until,
                    stop=0.0, tp1=None, tp2=None,
                    indicator_anchors=anchors,
                ))
            # Short
            elif (p1["high"] < sma_p1 and p2["high"] < sma_p2
                  and not inside_p1 and not inside_p2):
                sell_stop = min(p1["low"], p2["low"]) - _TICK
                signals.append(Signal(
                    symbol=symbol, strategy=self.name, side="short",
                    setup_ts=cur["time"], entry_type="stop",
                    entry_price=sell_stop,
                    valid_until=valid_until,
                    stop=0.0, tp1=None, tp2=None,
                    indicator_anchors=anchors,
                ))
        return signals
