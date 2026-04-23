"""Vectorized technical indicators on Polars DataFrames.

All functions assume the input has columns: time, open, high, low, close,
sorted ascending by time. They are look-ahead-safe: the value at bar i
depends only on bars 0..i.
"""
import polars as pl
from src.domain.constants import (
    RSI_PERIOD, MACD_FAST, MACD_SLOW, MACD_SIGNAL,
    BB_PERIOD, BB_STD, FRACTAL_WINDOW, ADX_PERIOD,
)


class IndicatorEnricher:
    """Static methods that add indicator columns to an OHLC Polars DataFrame."""

    @staticmethod
    def _wilder_smooth(values: list, period: int) -> list:
        """Wilder's smoothing: SMA seed for first window, then (prev*(p-1) + val) / p."""
        result = [None] * len(values)
        avg = None
        for i in range(period - 1, len(values)):
            if avg is None:
                avg = sum(values[: period]) / period
            else:
                avg = (avg * (period - 1) + values[i]) / period
            result[i] = avg
        return result

    @staticmethod
    def add_rsi(df: pl.DataFrame, period: int = RSI_PERIOD) -> pl.DataFrame:
        """RSI using Wilder's smoothing (SMA seed, then smoothed moving average)."""
        closes = df["close"].to_list()
        deltas = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
        gains = [0.0] + [max(d, 0.0) for d in deltas]
        losses = [0.0] + [max(-d, 0.0) for d in deltas]

        # Wilder smooth starting from index period (first complete window uses bars 1..period)
        avg_gains = [None] * len(closes)
        avg_losses = [None] * len(closes)
        avg_g = avg_l = None
        for i in range(period, len(closes)):
            if avg_g is None:
                avg_g = sum(gains[1 : period + 1]) / period
                avg_l = sum(losses[1 : period + 1]) / period
            else:
                avg_g = (avg_g * (period - 1) + gains[i]) / period
                avg_l = (avg_l * (period - 1) + losses[i]) / period
            avg_gains[i] = avg_g
            avg_losses[i] = avg_l

        rsi_vals = [
            None if avg_gains[i] is None
            else (100.0 if avg_losses[i] == 0 else 100.0 - 100.0 / (1.0 + avg_gains[i] / avg_losses[i]))
            for i in range(len(closes))
        ]
        return df.with_columns(
            pl.Series(f"rsi_{period}", rsi_vals, dtype=pl.Float64)
        )

    @staticmethod
    def add_macd(df: pl.DataFrame, fast: int = MACD_FAST, slow: int = MACD_SLOW,
                 signal: int = MACD_SIGNAL) -> pl.DataFrame:
        return df.with_columns([
            pl.col("close").ewm_mean(span=fast, adjust=False, min_samples=fast).alias("_ema_fast"),
            pl.col("close").ewm_mean(span=slow, adjust=False, min_samples=slow).alias("_ema_slow"),
        ]).with_columns([
            (pl.col("_ema_fast") - pl.col("_ema_slow")).alias("macd")
        ]).with_columns([
            pl.col("macd").ewm_mean(span=signal, adjust=False, min_samples=1).alias("macd_signal")
        ]).with_columns([
            (pl.col("macd") - pl.col("macd_signal")).alias("macd_hist")
        ]).drop(["_ema_fast", "_ema_slow"])

    @staticmethod
    def add_bollinger(df: pl.DataFrame, period: int = BB_PERIOD,
                      std_mult: float = BB_STD) -> pl.DataFrame:
        return df.with_columns([
            pl.col("close").rolling_mean(window_size=period).alias("bb_middle"),
            pl.col("close").rolling_std(window_size=period).alias("_bb_std"),
        ]).with_columns([
            (pl.col("bb_middle") + std_mult * pl.col("_bb_std")).alias("bb_upper"),
            (pl.col("bb_middle") - std_mult * pl.col("_bb_std")).alias("bb_lower"),
        ]).with_columns([
            ((pl.col("close") - pl.col("bb_lower")) /
             (pl.col("bb_upper") - pl.col("bb_lower"))).alias("bb_pct")
        ]).drop("_bb_std")

    @staticmethod
    def add_fractals(df: pl.DataFrame, window: int = FRACTAL_WINDOW) -> pl.DataFrame:
        """Williams fractals. A fractal_high at bar i requires high[i-2] < high[i]
        and high[i-1] < high[i] and high[i+1] < high[i] and high[i+2] < high[i].
        Confirmed at bar i+2 — we set the flag at bar i+2 to avoid look-ahead.
        """
        assert window == 5, "Only 5-bar fractal supported"
        return df.with_columns([
            # Confirm at bar i+2: shift by -2 so the look-back uses bars [i-4..i] of original series
            (
                (pl.col("high").shift(4) < pl.col("high").shift(2)) &
                (pl.col("high").shift(3) < pl.col("high").shift(2)) &
                (pl.col("high").shift(1) < pl.col("high").shift(2)) &
                (pl.col("high")          < pl.col("high").shift(2))
            ).fill_null(False).alias("fractal_high"),
            (
                (pl.col("low").shift(4) > pl.col("low").shift(2)) &
                (pl.col("low").shift(3) > pl.col("low").shift(2)) &
                (pl.col("low").shift(1) > pl.col("low").shift(2)) &
                (pl.col("low")          > pl.col("low").shift(2))
            ).fill_null(False).alias("fractal_low"),
        ])

    @staticmethod
    def add_adx(df: pl.DataFrame, period: int = ADX_PERIOD) -> pl.DataFrame:
        """Wilder ADX. DM+ = up_move if up_move > down_move and up_move > 0 else 0."""
        alpha = 1.0 / period
        df = df.with_columns([
            (pl.col("high") - pl.col("high").shift(1)).alias("_up_move"),
            (pl.col("low").shift(1) - pl.col("low")).alias("_dn_move"),
            pl.max_horizontal(
                pl.col("high") - pl.col("low"),
                (pl.col("high") - pl.col("close").shift(1)).abs(),
                (pl.col("low") - pl.col("close").shift(1)).abs(),
            ).alias("_tr"),
        ])
        df = df.with_columns([
            pl.when((pl.col("_up_move") > pl.col("_dn_move")) & (pl.col("_up_move") > 0))
              .then(pl.col("_up_move")).otherwise(0.0).alias("_dm_plus"),
            pl.when((pl.col("_dn_move") > pl.col("_up_move")) & (pl.col("_dn_move") > 0))
              .then(pl.col("_dn_move")).otherwise(0.0).alias("_dm_minus"),
        ])
        df = df.with_columns([
            pl.col("_tr").ewm_mean(alpha=alpha, adjust=False, min_samples=period).alias("_atr_w"),
            pl.col("_dm_plus").ewm_mean(alpha=alpha, adjust=False, min_samples=period).alias("_dm_plus_w"),
            pl.col("_dm_minus").ewm_mean(alpha=alpha, adjust=False, min_samples=period).alias("_dm_minus_w"),
        ])
        df = df.with_columns([
            (100.0 * pl.col("_dm_plus_w") / pl.col("_atr_w")).alias("plus_di"),
            (100.0 * pl.col("_dm_minus_w") / pl.col("_atr_w")).alias("minus_di"),
        ])
        df = df.with_columns([
            (100.0 * (pl.col("plus_di") - pl.col("minus_di")).abs() /
             (pl.col("plus_di") + pl.col("minus_di"))).alias("_dx"),
        ])
        df = df.with_columns([
            pl.col("_dx").ewm_mean(alpha=alpha, adjust=False, min_samples=period).alias(f"adx_{period}")
        ])
        return df.drop(["_up_move", "_dn_move", "_tr", "_dm_plus", "_dm_minus",
                        "_atr_w", "_dm_plus_w", "_dm_minus_w", "_dx"])

    @staticmethod
    def enrich_all(df: pl.DataFrame) -> pl.DataFrame:
        """Apply all 5 indicators in order. Input must be sorted by time ascending."""
        df = IndicatorEnricher.add_rsi(df)
        df = IndicatorEnricher.add_macd(df)
        df = IndicatorEnricher.add_bollinger(df)
        df = IndicatorEnricher.add_fractals(df)
        df = IndicatorEnricher.add_adx(df)
        return df
