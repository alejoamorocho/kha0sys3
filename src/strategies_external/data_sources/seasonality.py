"""Average historical return per (month, day) across N years."""

import polars as pl


def seasonal_mean_return(df: pl.DataFrame, window_days: int = 5) -> dict[str, float]:
    """For each (month, day) key, compute the mean N-day forward return
    across all years in the dataset (excluding the current year's recent data).

    df: DataFrame with `time` (datetime) and `close` columns.
    Returns: dict {"MM-DD": mean_return}.
    """
    if df.is_empty():
        return {}
    enriched = (
        df.sort("time")
        .with_columns(
            (pl.col("close").shift(-window_days) / pl.col("close") - 1.0).alias("ret"),
            pl.col("time").dt.strftime("%m-%d").alias("key"),
        )
        .drop_nulls(["ret"])
    )
    grouped = enriched.group_by("key").agg(pl.col("ret").mean().alias("mean_ret"))
    rows = grouped.to_dicts()
    return {r["key"]: r["mean_ret"] for r in rows}
