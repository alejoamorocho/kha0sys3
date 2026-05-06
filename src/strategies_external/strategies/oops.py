"""OOPS — Larry Williams gap-reversal pattern.

Long: open[t] < low[t-1] AND high[t] > low[t-1] → buy stop @ low[t-1] + 1 tick.
Short: open[t] > high[t-1] AND low[t] < high[t-1] → sell stop @ high[t-1] - 1 tick.

Tick assumption: 0.01 (indices and commodities in CFDs on Vantage). The backtester
applies additional slippage according to asset class.
"""

from datetime import timedelta

import polars as pl

from src.strategies_external.common.signal import Signal
from src.strategies_external.strategies.base import Strategy


_TICK = 0.01


class OOPSStrategy(Strategy):
    name = "oops"

    def __init__(self, atr_window: int = 14):
        self.atr_window = atr_window

    def generate_signals(self, df: pl.DataFrame, symbol: str) -> list[Signal]:
        if df.is_empty() or df.shape[0] < self.atr_window + 2:
            return []

        # Compute ATR(atr_window) over daily bars
        atr_df = (
            df.with_columns(
                pl.max_horizontal(
                    pl.col("high") - pl.col("low"),
                    (pl.col("high") - pl.col("close").shift(1)).abs(),
                    (pl.col("low") - pl.col("close").shift(1)).abs(),
                ).alias("tr")
            )
            .with_columns(
                pl.col("tr").rolling_mean(self.atr_window).alias("atr")
            )
        )

        rows = atr_df.to_dicts()
        signals: list[Signal] = []

        for i in range(1, len(rows)):
            prev = rows[i - 1]
            cur = rows[i]
            prev_high = prev["high"]
            prev_low = prev["low"]
            prev_range = prev_high - prev_low
            atr = cur.get("atr") or 0.0
            today_ts = cur["time"]
            valid_until = today_ts + timedelta(days=1) - timedelta(seconds=1)

            anchors = {
                "prev_high": prev_high,
                "prev_low": prev_low,
                "prev_range": prev_range,
                "prev_close": prev["close"],
                "today_open": cur["open"],
                "today_high": cur["high"],
                "today_low": cur["low"],
                "atr14": atr,
            }

            # Long OOPS: open gaps below prev_low, then recovers above prev_low
            if cur["open"] < prev_low and cur["high"] > prev_low:
                signals.append(Signal(
                    symbol=symbol,
                    strategy=self.name,
                    side="long",
                    setup_ts=today_ts,
                    entry_type="stop",
                    entry_price=prev_low + _TICK,
                    valid_until=valid_until,
                    stop=0.0,
                    tp1=None,
                    tp2=None,
                    indicator_anchors=anchors,
                ))
            # Short OOPS: open gaps above prev_high, then falls below prev_high
            elif cur["open"] > prev_high and cur["low"] < prev_high:
                signals.append(Signal(
                    symbol=symbol,
                    strategy=self.name,
                    side="short",
                    setup_ts=today_ts,
                    entry_type="stop",
                    entry_price=prev_high - _TICK,
                    valid_until=valid_until,
                    stop=0.0,
                    tp1=None,
                    tp2=None,
                    indicator_anchors=anchors,
                ))

        return signals
