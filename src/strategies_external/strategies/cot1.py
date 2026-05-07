"""InsiderWeek COT-1: COT extremes + seasonality + price action.

COT Index > threshold_long → long bias; < threshold_short → short bias.
Confluence: seasonal mean return aligns with bias.
Trigger: pin bar / inside-day breakout / double-bottom on daily.
"""

from datetime import timedelta

import polars as pl

from src.strategies_external.common.signal import Signal
from src.strategies_external.strategies.base import Strategy


def _is_pin_bar(o: float, h: float, l: float, c: float, side: str) -> bool:
    rng = h - l
    if rng <= 0:
        return False
    body = abs(c - o)
    if body / rng >= 0.30:
        return False
    if side == "long":
        lower_wick = min(o, c) - l
        return lower_wick / rng > 0.5 and c > o
    else:
        upper_wick = h - max(o, c)
        return upper_wick / rng > 0.5 and c < o


def _is_inside_day_breakout(prev2: dict, prev1: dict, cur: dict, side: str) -> bool:
    """prev1 inside-day vs prev2; cur rompe extremos en dirección bias."""
    inside_day = prev1["high"] < prev2["high"] and prev1["low"] > prev2["low"]
    if not inside_day:
        return False
    if side == "long":
        return cur["high"] > prev1["high"]
    return cur["low"] < prev1["low"]


class COT1Strategy(Strategy):
    name = "cot1"

    def __init__(
        self,
        cot_threshold_long: float = 80.0,
        cot_threshold_short: float = 20.0,
        seasonal_threshold: float = 0.005,
        cot_lag_days: int = 3,
        atr_window: int = 14,
    ):
        self.cot_threshold_long = cot_threshold_long
        self.cot_threshold_short = cot_threshold_short
        self.seasonal_threshold = seasonal_threshold
        self.cot_lag_days = cot_lag_days
        self.atr_window = atr_window

    def generate_signals(
        self,
        df: pl.DataFrame,
        symbol: str,
        cot_index_series: pl.DataFrame | None = None,
        seasonality: dict[str, float] | None = None,
    ) -> list[Signal]:
        if df.is_empty() or df.shape[0] < self.atr_window + 5:
            return []
        cot_index_series = cot_index_series if cot_index_series is not None else pl.DataFrame()
        seasonality = seasonality or {}

        enriched = (
            df.with_columns(
                pl.max_horizontal(
                    pl.col("high") - pl.col("low"),
                    (pl.col("high") - pl.col("close").shift(1)).abs(),
                    (pl.col("low") - pl.col("close").shift(1)).abs(),
                ).alias("tr")
            )
            .with_columns(pl.col("tr").rolling_mean(self.atr_window).alias("atr"))
        )
        rows = enriched.to_dicts()

        cot_rows = cot_index_series.sort("date").to_dicts() if cot_index_series.shape[0] > 0 else []
        signals: list[Signal] = []

        for i in range(self.atr_window + 1, len(rows)):
            cur = rows[i]
            cur_ts = cur["time"]
            atr_cur = cur.get("atr") or 0.0

            # Find most recent COT publication respecting lag
            applicable_cot = None
            for c in reversed(cot_rows):
                if c["date"] + timedelta(days=self.cot_lag_days) <= cur_ts:
                    applicable_cot = c["cot_index"]
                    break
            if applicable_cot is None:
                continue

            key = cur_ts.strftime("%m-%d")
            seasonal = seasonality.get(key, 0.0)

            anchors = {
                "atr14": atr_cur, "cot_index": applicable_cot,
                "season_5d": seasonal,
                "swing_high_5d": max(rows[i - j]["high"] for j in range(1, 6)),
                "swing_low_5d": min(rows[i - j]["low"] for j in range(1, 6)),
            }
            valid_until = cur_ts + timedelta(days=5)

            # Long bias: pin bar
            if applicable_cot >= self.cot_threshold_long and seasonal >= self.seasonal_threshold:
                if _is_pin_bar(cur["open"], cur["high"], cur["low"], cur["close"], "long"):
                    signals.append(Signal(
                        symbol=symbol, strategy=self.name, side="long",
                        setup_ts=cur_ts, entry_type="stop",
                        entry_price=cur["high"] + 0.01,
                        valid_until=valid_until,
                        stop=0.0, tp1=None, tp2=None,
                        timestop_bars=None,  # Plan 2.5: 5d via valid_until
                        indicator_anchors=anchors,
                    ))
            # Short bias: pin bar
            if applicable_cot <= self.cot_threshold_short and seasonal <= -self.seasonal_threshold:
                if _is_pin_bar(cur["open"], cur["high"], cur["low"], cur["close"], "short"):
                    signals.append(Signal(
                        symbol=symbol, strategy=self.name, side="short",
                        setup_ts=cur_ts, entry_type="stop",
                        entry_price=cur["low"] - 0.01,
                        valid_until=valid_until,
                        stop=0.0, tp1=None, tp2=None,
                        timestop_bars=None,  # Plan 2.5: 5d via valid_until
                        indicator_anchors=anchors,
                    ))

            # Inside-day breakout (Plan 2.5): doc lista 3 triggers válidos
            if i >= 2:
                prev2 = rows[i - 2]
                prev1 = rows[i - 1]
                if applicable_cot >= self.cot_threshold_long and seasonal >= self.seasonal_threshold:
                    if _is_inside_day_breakout(prev2, prev1, cur, "long"):
                        signals.append(Signal(
                            symbol=symbol, strategy=self.name, side="long",
                            setup_ts=cur_ts, entry_type="stop",
                            entry_price=prev1["high"] + 0.01,
                            valid_until=valid_until,
                            stop=0.0, tp1=None, tp2=None,
                            timestop_bars=None,
                            indicator_anchors=anchors,
                        ))
                if applicable_cot <= self.cot_threshold_short and seasonal <= -self.seasonal_threshold:
                    if _is_inside_day_breakout(prev2, prev1, cur, "short"):
                        signals.append(Signal(
                            symbol=symbol, strategy=self.name, side="short",
                            setup_ts=cur_ts, entry_type="stop",
                            entry_price=prev1["low"] - 0.01,
                            valid_until=valid_until,
                            stop=0.0, tp1=None, tp2=None,
                            timestop_bars=None,
                            indicator_anchors=anchors,
                        ))
        return signals
