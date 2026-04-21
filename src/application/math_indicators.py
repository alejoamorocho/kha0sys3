"""Vectorized math-based indicators on Polars DataFrames.

Differential calculus, integral calculus, linear algebra, and statistics
indicators. All functions are look-ahead-safe: bar i depends only on bars 0..i.

Kalman is the exception — inherently sequential, implemented as a Python scan,
applied once per symbol on the cached enriched parquet.
"""
from __future__ import annotations
import polars as pl


class MathIndicatorEnricher:
    """Static methods adding math-based indicator columns to an OHLC Polars DataFrame."""

    # ── Differential calculus ──────────────────────────────────────────

    @staticmethod
    def add_velocity(df: pl.DataFrame, window: int = 10) -> pl.DataFrame:
        """Rate of change: (close[i] - close[i-window]) / window."""
        return df.with_columns(
            ((pl.col("close") - pl.col("close").shift(window)) / window).alias(f"velocity_{window}")
        )

    @staticmethod
    def add_acceleration(df: pl.DataFrame, window: int = 10) -> pl.DataFrame:
        """Second difference of close (smoothed): velocity[i] - velocity[i-1]."""
        vel = (pl.col("close") - pl.col("close").shift(window)) / window
        return df.with_columns(
            (vel - vel.shift(1)).alias(f"accel_{window}")
        )

    @staticmethod
    def add_curvature(df: pl.DataFrame, window: int = 10) -> pl.DataFrame:
        """Curvature: d2P / (1 + dP^2)^1.5 where dP is first diff, d2P is second diff."""
        dP = pl.col("close") - pl.col("close").shift(1)
        d2P = dP - dP.shift(1)
        curvature = d2P / ((1.0 + dP ** 2) ** 1.5)
        return df.with_columns(curvature.alias(f"curvature_{window}"))

    # ── Integral calculus ──────────────────────────────────────────────

    @staticmethod
    def add_vwap_area(df: pl.DataFrame, window: int = 20) -> pl.DataFrame:
        """VWAP area: rolling_sum(close - vwap_proxy, window).
        Uses volume if present, else rolling mean of close as proxy."""
        if "volume" in df.columns:
            vwap = (
                (pl.col("close") * pl.col("volume")).rolling_sum(window_size=window) /
                pl.col("volume").rolling_sum(window_size=window)
            )
        else:
            vwap = pl.col("close").rolling_mean(window_size=window)
        area = (pl.col("close") - vwap).rolling_sum(window_size=window)
        return df.with_columns(area.alias(f"vwap_area_{window}"))

    @staticmethod
    def add_meanrev_area(df: pl.DataFrame, window: int = 50) -> pl.DataFrame:
        """Mean-reversion area: rolling_sum(close - rolling_mean(close, window), window)."""
        deviation = pl.col("close") - pl.col("close").rolling_mean(window_size=window)
        area = deviation.rolling_sum(window_size=window)
        return df.with_columns(area.alias(f"meanrev_area_{window}"))

    # ── Linear algebra ─────────────────────────────────────────────────

    @staticmethod
    def add_ols_regression(df: pl.DataFrame, window: int = 30) -> pl.DataFrame:
        """Rolling OLS: slope and standardised residual of close ~ time_index within window.

        Formulas (avoid matrix inversion):
            x = 0..window-1  (centred x_mean = (window-1)/2)
            slope = cov(x, y) / var(x)
            intercept = mean(y) - slope * mean(x)
            residual = close - predicted
            resid_z = residual / std(residual over window)
        """
        n = window
        # sum of 0..n-1 = n*(n-1)/2; sum of squares = n*(n-1)*(2n-1)/6
        x_mean = (n - 1) / 2.0
        x_var = (n * (n - 1) * (2 * n - 1) / 6.0) / n - x_mean ** 2  # pop var

        # Rolling quantities of y (close)
        y_mean = pl.col("close").rolling_mean(window_size=n)

        # Compute E[x*y] within window using rolling weighted sum
        # weight for position k in window (0=oldest, n-1=newest) is k
        # Using Polars: shift(j) gives close[i-j]; weight = (n-1-j) → multiply then sum
        xy_terms = [
            pl.col("close").shift(j) * float(n - 1 - j)
            for j in range(n)
        ]
        ex_y = sum(xy_terms) / n  # type: ignore[arg-type]

        slope = (ex_y - x_mean * y_mean) / x_var

        # Intercept at last x = n-1
        intercept = y_mean - slope * x_mean
        predicted = intercept + slope * float(n - 1)

        residual = pl.col("close") - predicted
        resid_std = residual.rolling_std(window_size=n)
        resid_z = residual / resid_std

        return df.with_columns([
            slope.alias(f"ols_slope_{window}"),
            resid_z.alias(f"ols_resid_z_{window}"),
        ])

    @staticmethod
    def add_kalman(df: pl.DataFrame) -> pl.DataFrame:
        """1D Kalman filter on close price.
        State = smoothed price, innovation = observation - predicted.
        Process noise Q=1e-4, observation noise R=0.01.
        Inherently sequential — implemented as Python scan (OK, run once per symbol).
        """
        closes = df["close"].to_list()
        n = len(closes)
        Q = 1e-4   # process noise
        R_obs = 0.01  # observation noise

        states = [None] * n
        innovations = [None] * n

        if n == 0:
            return df.with_columns([
                pl.lit(None).cast(pl.Float64).alias("kalman_state"),
                pl.lit(None).cast(pl.Float64).alias("kalman_innovation"),
            ])

        # Initialise with first close
        x_est = closes[0] if closes[0] is not None else 0.0
        P_est = 1.0

        for i in range(n):
            c = closes[i]
            if c is None:
                states[i] = x_est
                innovations[i] = 0.0
                continue

            # Predict
            x_pred = x_est
            P_pred = P_est + Q

            # Update
            K = P_pred / (P_pred + R_obs)
            innov = c - x_pred
            x_est = x_pred + K * innov
            P_est = (1.0 - K) * P_pred

            states[i] = x_est
            innovations[i] = innov

        return df.with_columns([
            pl.Series("kalman_state", states, dtype=pl.Float64),
            pl.Series("kalman_innovation", innovations, dtype=pl.Float64),
        ])

    # ── Statistics ─────────────────────────────────────────────────────

    @staticmethod
    def add_zscore(df: pl.DataFrame, window: int = 30) -> pl.DataFrame:
        """Z-score of close within rolling window."""
        z = (
            (pl.col("close") - pl.col("close").rolling_mean(window_size=window)) /
            pl.col("close").rolling_std(window_size=window)
        )
        return df.with_columns(z.alias(f"zscore_{window}"))

    @staticmethod
    def add_skew_kurt(df: pl.DataFrame, window: int = 50) -> pl.DataFrame:
        """Rolling skewness and kurtosis of returns.
        Approximated via manual moment calculations (Polars lacks native rolling skew/kurt).
        Returns: ret_skew_{window}, ret_kurt_{window}.
        """
        ret = pl.col("close").pct_change()

        # Rolling mean, std, higher moments of returns
        r_mean = ret.rolling_mean(window_size=window)
        r_std = ret.rolling_std(window_size=window)

        # Centralised return  (deviation)
        dev = ret - r_mean

        # Rolling mean of dev^3 and dev^4 via rolling_sum of series
        # We create helper columns, then use rolling_sum
        df = df.with_columns([
            ret.alias("_ret"),
            r_mean.alias("_ret_mean"),
            r_std.alias("_ret_std"),
        ])
        df = df.with_columns([
            (pl.col("_ret") - pl.col("_ret_mean")).alias("_dev")
        ])
        df = df.with_columns([
            (pl.col("_dev") ** 3).alias("_dev3"),
            (pl.col("_dev") ** 4).alias("_dev4"),
        ])
        df = df.with_columns([
            (pl.col("_dev3").rolling_mean(window_size=window) /
             (pl.col("_ret_std") ** 3)).alias(f"ret_skew_{window}"),
            (pl.col("_dev4").rolling_mean(window_size=window) /
             (pl.col("_ret_std") ** 4)).alias(f"ret_kurt_{window}"),
        ])
        return df.drop(["_ret", "_ret_mean", "_ret_std", "_dev", "_dev3", "_dev4"])

    @staticmethod
    def add_hurst(df: pl.DataFrame, window: int = 50) -> pl.DataFrame:
        """Mean-reversion regime proxy via autocorrelation at lag-1 of returns.
        A true R/S Hurst is too slow for 750 combos; autocorr is a reliable proxy:
            autocorr_lag1 < 0 → mean-reverting (Hurst < 0.5 equivalent)
            autocorr_lag1 > 0 → trending (Hurst > 0.5 equivalent)
        Column: mean_rev_regime_{window}
        """
        ret = pl.col("close").pct_change()
        ret_lag = ret.shift(1)

        # Rolling cov(ret, ret_lag) / rolling_var(ret)
        # Use helper columns
        df = df.with_columns([
            ret.alias("_r"),
            ret_lag.alias("_rl"),
        ])
        df = df.with_columns([
            pl.col("_r").rolling_mean(window_size=window).alias("_rm"),
            pl.col("_rl").rolling_mean(window_size=window).alias("_rlm"),
        ])
        df = df.with_columns([
            ((pl.col("_r") - pl.col("_rm")) * (pl.col("_rl") - pl.col("_rlm")))
            .rolling_mean(window_size=window).alias("_cov"),
            ((pl.col("_r") - pl.col("_rm")) ** 2)
            .rolling_mean(window_size=window).alias("_var"),
        ])
        df = df.with_columns(
            (pl.col("_cov") / pl.col("_var").clip(lower_bound=1e-12))
            .alias(f"mean_rev_regime_{window}")
        )
        return df.drop(["_r", "_rl", "_rm", "_rlm", "_cov", "_var"])

    # ── Composite ──────────────────────────────────────────────────────

    @staticmethod
    def enrich_all_math(df: pl.DataFrame) -> pl.DataFrame:
        """Apply all 10 math indicators in order."""
        df = MathIndicatorEnricher.add_velocity(df)
        df = MathIndicatorEnricher.add_acceleration(df)
        df = MathIndicatorEnricher.add_curvature(df)
        df = MathIndicatorEnricher.add_vwap_area(df)
        df = MathIndicatorEnricher.add_meanrev_area(df)
        df = MathIndicatorEnricher.add_ols_regression(df)
        df = MathIndicatorEnricher.add_kalman(df)
        df = MathIndicatorEnricher.add_zscore(df)
        df = MathIndicatorEnricher.add_skew_kurt(df)
        df = MathIndicatorEnricher.add_hurst(df)
        return df
