"""Primary signal generators and confluence filters for indicator-based archetypes.

Emits a long-format DataFrame with columns:
    time, symbol, direction (LONG/SHORT), signal_type, indicator_state (dict-as-struct)

All filters return a subset of the input signal DataFrame.
"""
from __future__ import annotations
import polars as pl

SIGNAL_TYPES = (
    # Reversion
    "RSI_OB_REV", "BB_TOUCH_REV", "FRACTAL_REV", "MACD_DIVERGENCE", "BB_RSI_CONFLUENCE",
    # Momentum
    "MACD_CROSS", "ADX_BREAKOUT", "BB_BREAKOUT", "RSI_50_CROSS", "FRACTAL_TREND",
    # Math indicators (differential calculus, integral, linear algebra, statistics)
    "ZSCORE_REV", "VELOCITY_REV", "ACCEL_SHOCK", "KALMAN_INNOV_REV", "OLS_RESIDUAL_REV",
    "CURVATURE_PEAK", "VWAP_AREA_EXTREME", "MEANREV_AREA_EXTREME", "REGRESSION_BREAKOUT",
    "SKEW_REGIME_REV",
)

CONFLUENCE_FILTERS = ("RSI_ZONE", "ADX_REGIME", "BB_POSITION", "MACD_ALIGN")


class SignalGenerator:
    """Generate long-format signal DataFrames from an enriched OHLC bar DataFrame."""

    @staticmethod
    def generate(df: pl.DataFrame, signal_type: str, symbol: str) -> pl.DataFrame:
        if signal_type == "RSI_OB_REV":
            long_cond = (pl.col("rsi_14").shift(1) <= 30) & (pl.col("rsi_14") > 30)
            short_cond = (pl.col("rsi_14").shift(1) >= 70) & (pl.col("rsi_14") < 70)
        elif signal_type == "BB_TOUCH_REV":
            long_cond = pl.col("low") <= pl.col("bb_lower")
            short_cond = pl.col("high") >= pl.col("bb_upper")
        elif signal_type == "FRACTAL_REV":
            long_cond = pl.col("fractal_low")
            short_cond = pl.col("fractal_high")
        elif signal_type == "MACD_DIVERGENCE":
            # 20-bar window. Bullish div: price makes LL but MACD makes HL.
            hi20 = pl.col("high").rolling_max(window_size=20)
            lo20 = pl.col("low").rolling_min(window_size=20)
            macd_hi20 = pl.col("macd").rolling_max(window_size=20)
            macd_lo20 = pl.col("macd").rolling_min(window_size=20)
            long_cond = (pl.col("low") <= lo20) & (pl.col("macd") > macd_lo20.shift(10))
            short_cond = (pl.col("high") >= hi20) & (pl.col("macd") < macd_hi20.shift(10))
        elif signal_type == "BB_RSI_CONFLUENCE":
            long_cond = (pl.col("low") <= pl.col("bb_lower")) & (pl.col("rsi_14") < 30)
            short_cond = (pl.col("high") >= pl.col("bb_upper")) & (pl.col("rsi_14") > 70)
        elif signal_type == "MACD_CROSS":
            long_cond = (pl.col("macd").shift(1) <= pl.col("macd_signal").shift(1)) & \
                        (pl.col("macd") > pl.col("macd_signal"))
            short_cond = (pl.col("macd").shift(1) >= pl.col("macd_signal").shift(1)) & \
                         (pl.col("macd") < pl.col("macd_signal"))
        elif signal_type == "ADX_BREAKOUT":
            crossed = (pl.col("adx_14").shift(1) < 25) & (pl.col("adx_14") >= 25)
            long_cond = crossed & (pl.col("plus_di") > pl.col("minus_di"))
            short_cond = crossed & (pl.col("minus_di") > pl.col("plus_di"))
        elif signal_type == "BB_BREAKOUT":
            long_cond = pl.col("close") > pl.col("bb_upper")
            short_cond = pl.col("close") < pl.col("bb_lower")
        elif signal_type == "RSI_50_CROSS":
            long_cond = (pl.col("rsi_14").shift(1) <= 50) & (pl.col("rsi_14") > 50)
            short_cond = (pl.col("rsi_14").shift(1) >= 50) & (pl.col("rsi_14") < 50)
        elif signal_type == "FRACTAL_TREND":
            long_cond = pl.col("fractal_low") & (pl.col("adx_14") > 20) & \
                        (pl.col("plus_di") > pl.col("minus_di"))
            short_cond = pl.col("fractal_high") & (pl.col("adx_14") > 20) & \
                         (pl.col("minus_di") > pl.col("plus_di"))
        # ── Math indicators ──────────────────────────────────────────────
        elif signal_type == "ZSCORE_REV":
            # zscore_30 crosses -2 ascending → LONG; crosses +2 descending → SHORT
            long_cond = (pl.col("zscore_30").shift(1) <= -2.0) & (pl.col("zscore_30") > -2.0)
            short_cond = (pl.col("zscore_30").shift(1) >= 2.0) & (pl.col("zscore_30") < 2.0)
        elif signal_type == "VELOCITY_REV":
            # velocity_10 crosses 0 from below after ≥5 bars negative → LONG; mirror → SHORT
            neg_streak = (pl.col("velocity_10").shift(1) < 0) & \
                         (pl.col("velocity_10").shift(2) < 0) & \
                         (pl.col("velocity_10").shift(3) < 0) & \
                         (pl.col("velocity_10").shift(4) < 0) & \
                         (pl.col("velocity_10").shift(5) < 0)
            pos_streak = (pl.col("velocity_10").shift(1) > 0) & \
                         (pl.col("velocity_10").shift(2) > 0) & \
                         (pl.col("velocity_10").shift(3) > 0) & \
                         (pl.col("velocity_10").shift(4) > 0) & \
                         (pl.col("velocity_10").shift(5) > 0)
            long_cond = (pl.col("velocity_10").shift(1) < 0) & (pl.col("velocity_10") >= 0) & neg_streak
            short_cond = (pl.col("velocity_10").shift(1) > 0) & (pl.col("velocity_10") <= 0) & pos_streak
        elif signal_type == "ACCEL_SHOCK":
            # abs(accel_10) > 3 * rolling_std(accel_10, 50); positive spike → LONG, negative → SHORT
            accel_std = pl.col("accel_10").rolling_std(window_size=50)
            shock = pl.col("accel_10").abs() > 3.0 * accel_std
            long_cond = shock & (pl.col("accel_10") > 0)
            short_cond = shock & (pl.col("accel_10") < 0)
        elif signal_type == "KALMAN_INNOV_REV":
            # |kalman_innovation| > 2 * rolling_std(innovation, 50); sign drives reversal
            innov_std = pl.col("kalman_innovation").rolling_std(window_size=50)
            big = pl.col("kalman_innovation").abs() > 2.0 * innov_std
            # positive innovation (price above state) → expect SHORT reversal
            long_cond = big & (pl.col("kalman_innovation") < 0)
            short_cond = big & (pl.col("kalman_innovation") > 0)
        elif signal_type == "OLS_RESIDUAL_REV":
            # ols_resid_z_30 crosses ±2 for mean reversion
            long_cond = (pl.col("ols_resid_z_30").shift(1) <= -2.0) & (pl.col("ols_resid_z_30") > -2.0)
            short_cond = (pl.col("ols_resid_z_30").shift(1) >= 2.0) & (pl.col("ols_resid_z_30") < 2.0)
        elif signal_type == "CURVATURE_PEAK":
            # Local peak in abs(curvature_10) at bar i-2 (shift(2) avoids look-ahead)
            # sign of OLS slope determines direction: positive slope + peak = SHORT
            c_abs = pl.col("curvature_10").abs()
            local_peak = (c_abs.shift(2) > c_abs.shift(3)) & (c_abs.shift(2) > c_abs.shift(1))
            slope_pos = pl.col("ols_slope_30") > 0
            long_cond = local_peak & ~slope_pos
            short_cond = local_peak & slope_pos
        elif signal_type == "VWAP_AREA_EXTREME":
            # vwap_area_20 > 2σ (100-bar) → SHORT mean reversion; < -2σ → LONG
            va_std = pl.col("vwap_area_20").rolling_std(window_size=100)
            long_cond = pl.col("vwap_area_20") < -2.0 * va_std
            short_cond = pl.col("vwap_area_20") > 2.0 * va_std
        elif signal_type == "MEANREV_AREA_EXTREME":
            # meanrev_area_50 > 2σ (100-bar) → SHORT; < -2σ → LONG
            ma_std = pl.col("meanrev_area_50").rolling_std(window_size=100)
            long_cond = pl.col("meanrev_area_50") < -2.0 * ma_std
            short_cond = pl.col("meanrev_area_50") > 2.0 * ma_std
        elif signal_type == "REGRESSION_BREAKOUT":
            # ols_resid_z_30 > 2 → upper channel break → LONG continuation
            # ols_resid_z_30 < -2 → lower channel break → SHORT continuation
            long_cond = (pl.col("ols_resid_z_30").shift(1) <= 2.0) & (pl.col("ols_resid_z_30") > 2.0)
            short_cond = (pl.col("ols_resid_z_30").shift(1) >= -2.0) & (pl.col("ols_resid_z_30") < -2.0)
        elif signal_type == "SKEW_REGIME_REV":
            # ret_skew_50 > 1.5 AND zscore_30 > 1 → SHORT; ret_skew_50 < -1.5 AND zscore_30 < -1 → LONG
            long_cond = (pl.col("ret_skew_50") < -1.5) & (pl.col("zscore_30") < -1.0)
            short_cond = (pl.col("ret_skew_50") > 1.5) & (pl.col("zscore_30") > 1.0)
        else:
            raise ValueError(f"Unknown signal_type: {signal_type}")

        return df.with_columns([
            pl.when(long_cond).then(pl.lit("LONG"))
              .when(short_cond).then(pl.lit("SHORT"))
              .otherwise(None).alias("direction"),
        ]).filter(pl.col("direction").is_not_null()).select([
            "time",
            pl.lit(symbol).alias("symbol"),
            "direction",
            pl.lit(signal_type).alias("signal_type"),
            "close", "high", "low",  # preserve for backtester
            "atr_14" if "atr_14" in df.columns else pl.lit(None).alias("atr_14"),
        ])

    @staticmethod
    def apply_filters(signals: pl.DataFrame, enriched: pl.DataFrame,
                      filters: tuple[str, ...]) -> pl.DataFrame:
        """Apply confluence filters. Each filter is identified as '{FILTER}_{STATE}'
        e.g. 'ADX_REGIME_TREND', 'RSI_ZONE_EXTREME', 'BB_POSITION_UPPER', 'MACD_ALIGN_POS'.

        Filters are joined to signals by time then applied as boolean masks.
        """
        if not filters:
            return signals
        # Join enriched state at signal time
        join_cols = ["time", "rsi_14", "adx_14", "bb_pct", "macd_hist"]
        ctx = enriched.select(join_cols)
        joined = signals.join(ctx, on="time", how="left")

        mask = pl.lit(True)
        for f in filters:
            if f == "ADX_REGIME_TREND":
                mask = mask & (pl.col("adx_14") >= 25)
            elif f == "ADX_REGIME_RANGE":
                mask = mask & (pl.col("adx_14") < 20)
            elif f == "RSI_ZONE_EXTREME":
                mask = mask & ((pl.col("rsi_14") >= 70) | (pl.col("rsi_14") <= 30))
            elif f == "RSI_ZONE_NEUTRAL":
                mask = mask & (pl.col("rsi_14").is_between(40, 60))
            elif f == "BB_POSITION_UPPER":
                mask = mask & (pl.col("bb_pct") >= 0.67)
            elif f == "BB_POSITION_LOWER":
                mask = mask & (pl.col("bb_pct") <= 0.33)
            elif f == "MACD_ALIGN_POS":
                mask = mask & (pl.col("macd_hist") > 0)
            elif f == "MACD_ALIGN_NEG":
                mask = mask & (pl.col("macd_hist") < 0)
            else:
                raise ValueError(f"Unknown filter: {f}")
        return joined.filter(mask).select(signals.columns)
