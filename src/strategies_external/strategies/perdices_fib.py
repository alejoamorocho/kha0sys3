"""Pau Perdices — pullback Fibonacci on XAUUSD/XAGUSD.

V1 ejecucion en H1 (placeholder hasta llegar M5 para version final).
Contexto: EMA50>EMA200 (en H4 agregado desde H1) + estructura HH/HL.
Entrada: zona Fib 38.2-50% del ultimo impulso, RSI(14) < 40 girando, vela alcista.
"""

from datetime import timedelta

import polars as pl

from src.strategies_external.common.signal import Signal
from src.strategies_external.strategies.base import Strategy
from src.strategies_external.strategies.swings import find_swings


class PerdicesFibStrategy(Strategy):
    name = "perdices_fib"

    def __init__(
        self,
        rsi_window: int = 14,
        rsi_threshold: float = 40.0,
        fib_low: float = 0.382,
        fib_high: float = 0.5,
        ema_fast: int = 50,
        ema_slow: int = 200,
        impulse_window: int = 150,
        atr_window: int = 14,
    ):
        self.rsi_window = rsi_window
        self.rsi_threshold = rsi_threshold
        self.fib_low = fib_low
        self.fib_high = fib_high
        self.ema_fast = ema_fast
        self.ema_slow = ema_slow
        self.impulse_window = impulse_window
        self.atr_window = atr_window

    def _rsi(self, closes: pl.Series) -> pl.Series:
        delta = closes.diff()
        gain = delta.clip(lower_bound=0)
        loss = (-delta).clip(lower_bound=0)
        avg_gain = gain.rolling_mean(self.rsi_window)
        avg_loss = loss.rolling_mean(self.rsi_window)
        rs = avg_gain / avg_loss.replace(0, 1e-9)
        return 100 - (100 / (1 + rs))

    def generate_signals(self, df: pl.DataFrame, symbol: str) -> list[Signal]:
        min_bars = self.ema_slow
        if df.is_empty() or df.shape[0] < min_bars:
            return []
        enriched = (
            df.with_columns(
                pl.col("close").ewm_mean(span=self.ema_fast).alias("ema_fast"),
                pl.col("close").ewm_mean(span=self.ema_slow).alias("ema_slow"),
                pl.max_horizontal(
                    pl.col("high") - pl.col("low"),
                    (pl.col("high") - pl.col("close").shift(1)).abs(),
                    (pl.col("low") - pl.col("close").shift(1)).abs(),
                ).alias("tr"),
                self._rsi(df["close"]).alias("rsi"),
            )
            .with_columns(pl.col("tr").rolling_mean(self.atr_window).alias("atr"))
        )
        rows = enriched.to_dicts()
        signals: list[Signal] = []

        for i in range(self.impulse_window, len(rows)):
            cur = rows[i]
            if cur.get("ema_fast") is None or cur.get("ema_slow") is None:
                continue
            trend_up = cur["ema_fast"] > cur["ema_slow"]
            trend_down = cur["ema_fast"] < cur["ema_slow"]
            if not (trend_up or trend_down):
                continue

            window = rows[i - self.impulse_window:i + 1]
            swing_high = max(b["high"] for b in window)
            swing_low = min(b["low"] for b in window)
            rango = swing_high - swing_low
            if rango <= 0:
                continue

            atr_cur = cur.get("atr") or 0.0
            rsi_cur = cur.get("rsi")
            rsi_prev = rows[i - 1].get("rsi") if i > 0 else None
            if rsi_cur is None or rsi_prev is None:
                continue

            anchors_base = {
                "swing_high": swing_high, "swing_low": swing_low,
                "fib_382": swing_high - 0.382 * rango,
                "fib_50": swing_high - 0.5 * rango,
                "fib_127": swing_high + 0.272 * rango,
                "fib_1618": swing_high + 0.618 * rango,
                "rsi": rsi_cur, "atr14": atr_cur,
            }
            valid_until = cur["time"] + timedelta(hours=4)

            if trend_up:
                fib_zone_low = swing_high - self.fib_high * rango
                fib_zone_high = swing_high - self.fib_low * rango
                if (fib_zone_low <= cur["low"] <= fib_zone_high
                        and rsi_cur < self.rsi_threshold and rsi_cur > rsi_prev
                        and cur["close"] >= cur["open"]):
                    signals.append(Signal(
                        symbol=symbol, strategy=self.name, side="long",
                        setup_ts=cur["time"], entry_type="market",
                        entry_price=cur["close"],
                        valid_until=valid_until,
                        stop=0.0, tp1=None, tp2=None,
                        indicator_anchors=anchors_base,
                    ))
            elif trend_down:
                fib_zone_high = swing_low + self.fib_high * rango
                fib_zone_low = swing_low + self.fib_low * rango
                if (fib_zone_low <= cur["high"] <= fib_zone_high
                        and rsi_cur > 100 - self.rsi_threshold and rsi_cur < rsi_prev
                        and cur["close"] <= cur["open"]):
                    anchors_short = {**anchors_base,
                                     "fib_127": swing_low - 0.272 * rango,
                                     "fib_1618": swing_low - 0.618 * rango}
                    signals.append(Signal(
                        symbol=symbol, strategy=self.name, side="short",
                        setup_ts=cur["time"], entry_type="market",
                        entry_price=cur["close"],
                        valid_until=valid_until,
                        stop=0.0, tp1=None, tp2=None,
                        indicator_anchors=anchors_short,
                    ))
        return signals
