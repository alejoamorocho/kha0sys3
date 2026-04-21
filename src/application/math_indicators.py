"""Vectorized math-based indicators on Polars DataFrames.

Differential calculus, integral calculus, linear algebra, and statistics
indicators. All functions are look-ahead-safe: bar i depends only on bars 0..i.

Kalman is the exception — inherently sequential, implemented as a Python scan,
applied once per symbol on the cached enriched parquet.

v2 adds six new families: fractional differentiation (Lopez de Prado), Shannon
entropy of returns, R/S Hurst, FFT spectral power ratio, Kaufman Adaptive MA
slope, and EWMA volatility z-score. All look-ahead-safe.
"""
from __future__ import annotations
import math
import numpy as np
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

    # ── v2: Fractional differentiation (Lopez de Prado) ────────────────

    @staticmethod
    def _ffd_weights(d: float, thres: float = 1e-4, max_k: int = 200) -> np.ndarray:
        """Fixed-width fractional differentiation weights (Lopez de Prado 2018)."""
        w = [1.0]
        for k in range(1, max_k):
            w_k = -w[-1] * (d - k + 1) / k
            if abs(w_k) < thres:
                break
            w.append(w_k)
        return np.array(w, dtype=np.float64)

    @staticmethod
    def add_frac_diff_z(df: pl.DataFrame, d: float = 0.4, window: int = 50) -> pl.DataFrame:
        """Fractionally-differentiated close (d=0.4) z-scored over `window` bars.
        Preserves long memory while producing stationary series. Column: frac_diff_z_{window}.
        """
        closes = df["close"].to_numpy().astype(np.float64)
        n = len(closes)
        w = MathIndicatorEnricher._ffd_weights(d)
        k = len(w)
        ffd = np.full(n, np.nan)
        if n >= k:
            # conv: ffd[i] = sum_j w[j] * close[i-j]  for i >= k-1
            for i in range(k - 1, n):
                ffd[i] = np.dot(w, closes[i - k + 1 : i + 1][::-1])
        s = pl.Series("_ffd", ffd)
        df2 = df.with_columns(s)
        z = (
            (pl.col("_ffd") - pl.col("_ffd").rolling_mean(window_size=window)) /
            pl.col("_ffd").rolling_std(window_size=window)
        )
        return df2.with_columns(z.alias(f"frac_diff_z_{window}")).drop("_ffd")

    # ── v2: Shannon entropy of returns ─────────────────────────────────

    @staticmethod
    def add_shannon_entropy(df: pl.DataFrame, window: int = 50, bins: int = 8) -> pl.DataFrame:
        """Rolling Shannon entropy of binned returns. Information theory regime detector.
        A drop in entropy means returns are concentrating (trend/regime change).
        Columns: shannon_entropy_{window}, shannon_entropy_drop_{window}.
        """
        closes = df["close"].to_numpy().astype(np.float64)
        n = len(closes)
        rets = np.zeros(n)
        rets[1:] = np.diff(closes) / np.where(closes[:-1] != 0, closes[:-1], 1.0)
        ent = np.full(n, np.nan)
        if n >= window + 1:
            for i in range(window, n):
                w_ret = rets[i - window + 1 : i + 1]
                if np.nanstd(w_ret) < 1e-12:
                    ent[i] = 0.0
                    continue
                hist, _ = np.histogram(w_ret, bins=bins)
                p = hist / hist.sum()
                p = p[p > 0]
                ent[i] = float(-np.sum(p * np.log2(p)))
        df2 = df.with_columns(pl.Series(f"shannon_entropy_{window}", ent))
        # drop = entropy - rolling_mean(entropy, 20)  (negative = contraction)
        ent_mean = pl.col(f"shannon_entropy_{window}").rolling_mean(window_size=20)
        return df2.with_columns(
            (pl.col(f"shannon_entropy_{window}") - ent_mean).alias(f"shannon_entropy_drop_{window}")
        )

    # ── v2: Hurst R/S exponent ─────────────────────────────────────────

    @staticmethod
    def _hurst_rs(series: np.ndarray) -> float:
        """Classic rescaled-range Hurst estimator. Returns H in (0, 1)."""
        n = len(series)
        if n < 20:
            return float("nan")
        # Build chunks of size 10, 20, 40... up to n/2
        lags = []
        rs_vals = []
        for lag in (10, 20, 40, min(80, n // 2)):
            if lag >= n:
                break
            chunks = n // lag
            rs_chunk = []
            for c in range(chunks):
                seg = series[c * lag : (c + 1) * lag]
                mean = seg.mean()
                dev = seg - mean
                cum = np.cumsum(dev)
                R = cum.max() - cum.min()
                S = seg.std()
                if S > 1e-12 and R > 0:
                    rs_chunk.append(R / S)
            if rs_chunk:
                lags.append(lag)
                rs_vals.append(np.mean(rs_chunk))
        if len(lags) < 2:
            return float("nan")
        # log-log regression slope
        lx = np.log(lags)
        ly = np.log(rs_vals)
        slope = np.polyfit(lx, ly, 1)[0]
        return float(slope)

    @staticmethod
    def add_hurst_rs(df: pl.DataFrame, window: int = 100) -> pl.DataFrame:
        """Proper R/S Hurst exponent on log-returns. Column: hurst_rs_{window}.
        H < 0.5 mean-reverting; H > 0.5 trending; H ~ 0.5 random walk.
        """
        closes = df["close"].to_numpy().astype(np.float64)
        n = len(closes)
        log_ret = np.zeros(n)
        log_ret[1:] = np.diff(np.log(np.where(closes > 0, closes, 1e-9)))
        h = np.full(n, np.nan)
        if n >= window + 1:
            for i in range(window, n):
                h[i] = MathIndicatorEnricher._hurst_rs(log_ret[i - window + 1 : i + 1])
        return df.with_columns(pl.Series(f"hurst_rs_{window}", h))

    # ── v2: FFT spectral power ratio ───────────────────────────────────

    @staticmethod
    def add_spectral_power_ratio(df: pl.DataFrame, window: int = 64) -> pl.DataFrame:
        """FFT on last `window` returns. ratio = low-freq power / high-freq power.
        Rising ratio = trending regime; falling = choppy. Column: spectral_ratio_{window}.
        """
        closes = df["close"].to_numpy().astype(np.float64)
        n = len(closes)
        rets = np.zeros(n)
        rets[1:] = np.diff(closes)
        sr = np.full(n, np.nan)
        if n >= window + 1:
            half = window // 2
            low_hi = half // 2  # split at quarter-Nyquist
            for i in range(window, n):
                seg = rets[i - window + 1 : i + 1]
                seg = seg - seg.mean()
                spec = np.abs(np.fft.rfft(seg)) ** 2
                low = spec[1 : low_hi + 1].sum()
                high = spec[low_hi + 1 :].sum()
                if high > 1e-12:
                    sr[i] = float(low / high)
        return df.with_columns(pl.Series(f"spectral_ratio_{window}", sr))

    # ── v2: Kaufman Adaptive MA slope ──────────────────────────────────

    @staticmethod
    def add_kama_slope(df: pl.DataFrame, window: int = 10,
                        fast: int = 2, slow: int = 30) -> pl.DataFrame:
        """KAMA: adaptive MA using efficient ratio. Slope = KAMA[i] - KAMA[i-1].
        Columns: kama_{window}, kama_slope_{window}.
        """
        closes = df["close"].to_numpy().astype(np.float64)
        n = len(closes)
        change = np.zeros(n)
        if n > window:
            change[window:] = np.abs(closes[window:] - closes[:-window])
        volatility = np.zeros(n)
        abs_diff = np.zeros(n)
        abs_diff[1:] = np.abs(np.diff(closes))
        # rolling sum of abs_diff over `window` bars
        if n >= window:
            csum = np.cumsum(abs_diff)
            volatility[window:] = csum[window:] - csum[:-window]
        with np.errstate(invalid="ignore", divide="ignore"):
            er = np.where(volatility > 1e-12, change / volatility, 0.0)
        fast_sc = 2.0 / (fast + 1)
        slow_sc = 2.0 / (slow + 1)
        sc = (er * (fast_sc - slow_sc) + slow_sc) ** 2
        kama = np.full(n, np.nan)
        if n > window:
            kama[window] = closes[window]
            for i in range(window + 1, n):
                kama[i] = kama[i - 1] + sc[i] * (closes[i] - kama[i - 1])
        slope = np.full(n, np.nan)
        slope[1:] = np.diff(kama)
        return df.with_columns([
            pl.Series(f"kama_{window}", kama),
            pl.Series(f"kama_slope_{window}", slope),
        ])

    # ── v2: EWMA volatility spike (GARCH proxy) ────────────────────────

    @staticmethod
    def add_garch_vol_spike(df: pl.DataFrame, alpha: float = 0.06,
                             window: int = 50) -> pl.DataFrame:
        """EWMA variance of returns, then z-score over `window` bars.
        Captures volatility clustering without full GARCH fit.
        Column: garch_vol_z_{window}.
        """
        closes = df["close"].to_numpy().astype(np.float64)
        n = len(closes)
        rets = np.zeros(n)
        rets[1:] = np.diff(np.log(np.where(closes > 0, closes, 1e-9)))
        ewvar = np.zeros(n)
        if n > 0:
            ewvar[0] = rets[0] ** 2
            for i in range(1, n):
                ewvar[i] = (1 - alpha) * ewvar[i - 1] + alpha * rets[i] ** 2
        vol = np.sqrt(ewvar)
        s = pl.Series("_ewvol", vol)
        df2 = df.with_columns(s)
        z = (
            (pl.col("_ewvol") - pl.col("_ewvol").rolling_mean(window_size=window)) /
            pl.col("_ewvol").rolling_std(window_size=window)
        )
        return df2.with_columns(z.alias(f"garch_vol_z_{window}")).drop("_ewvol")

    # ── Composite ──────────────────────────────────────────────────────

    @staticmethod
    def enrich_all_math(df: pl.DataFrame) -> pl.DataFrame:
        """Apply all 10 v1 + 6 v2 math indicators in order."""
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
        # v2 additions
        df = MathIndicatorEnricher.add_frac_diff_z(df)
        df = MathIndicatorEnricher.add_shannon_entropy(df)
        df = MathIndicatorEnricher.add_hurst_rs(df)
        df = MathIndicatorEnricher.add_spectral_power_ratio(df)
        df = MathIndicatorEnricher.add_kama_slope(df)
        df = MathIndicatorEnricher.add_garch_vol_spike(df)
        return df
