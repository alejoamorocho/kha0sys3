"""Swing detector reproducible based on scipy.signal.find_peaks.

`find_swings(df, prominence_factor, min_distance)` returns (swing_lows, swing_highs)
where each is a list of (row_index, price) tuples. prominence_factor multiplies
the rolling 14-bar ATR proxy to set find_peaks prominence threshold.
"""

import polars as pl
from scipy.signal import find_peaks


def find_swings(
    df: pl.DataFrame,
    prominence_factor: float = 0.5,
    min_distance: int = 5,
    atr_window: int = 14,
) -> tuple[list[tuple[int, float]], list[tuple[int, float]]]:
    if df.is_empty() or df.shape[0] < atr_window:
        return [], []

    atr_proxy = (
        df.with_columns(
            (pl.col("high") - pl.col("low")).rolling_mean(atr_window).alias("atr")
        )["atr"]
        .fill_null(strategy="forward")
        .fill_null(strategy="backward")
        .to_list()
    )
    median_atr = sum(a for a in atr_proxy if a) / max(1, sum(1 for a in atr_proxy if a))
    prom = prominence_factor * median_atr

    highs = df["high"].to_list()
    lows = df["low"].to_list()
    inv_lows = [-x for x in lows]

    high_idxs, _ = find_peaks(highs, prominence=prom, distance=min_distance)
    low_idxs, _ = find_peaks(inv_lows, prominence=prom, distance=min_distance)

    swing_highs = [(int(i), float(highs[i])) for i in high_idxs]
    swing_lows = [(int(i), float(lows[i])) for i in low_idxs]
    return swing_lows, swing_highs
