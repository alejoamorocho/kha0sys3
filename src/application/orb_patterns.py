"""ORB pattern definitions: state classifiers + event detectors.

State (categorical context at OR close):
  - or_position_vs_pd: 5 values from DataEnricher (ABOVE_PD_HIGH, etc.)
  - or_atr_bucket: 3 values (compressed <= 0.3, normal, expanded >= 0.7)
  - pd_or_overlap_bucket: 3 values (gap_up, gap_down, inside)

Events (dynamic post-OR triggers, detected on M1):
  - BREAK_UP / BREAK_DOWN
  - FALSE_BREAK_UP / FALSE_BREAK_DOWN
  - MITIG_PD_MID / MITIG_PD_CLOSE
  - REENTRY_PD_OR_HIGH / REENTRY_PD_OR_LOW

Pattern ID format: f"{EVENT}_{or_position}_{or_atr_bucket}_{pd_or_bucket}"
"""
from __future__ import annotations

import polars as pl

OR_ATR_BUCKETS = ["compressed", "normal", "expanded"]
PD_OR_BUCKETS = ["gap_up", "gap_down", "inside"]

EVENTS = [
    "BREAK_UP", "BREAK_DOWN",
    "FALSE_BREAK_UP", "FALSE_BREAK_DOWN",
    "MITIG_PD_MID", "MITIG_PD_CLOSE",
    "REENTRY_PD_OR_HIGH", "REENTRY_PD_OR_LOW",
]


def add_state_columns(df: pl.DataFrame) -> pl.DataFrame:
    """Add `or_atr_bucket` and `pd_or_overlap_bucket` columns.

    Assumes `df` already has `or_atr_ratio`, `or_high`, `or_low`,
    `pd_or_high`, `pd_or_low` from `DataEnricher.enrich_with_opening_range`.
    """
    return df.with_columns([
        pl.when(pl.col("or_atr_ratio").is_null())
          .then(pl.lit(None, dtype=pl.Utf8))
          .when(pl.col("or_atr_ratio") <= 0.3)
          .then(pl.lit("compressed"))
          .when(pl.col("or_atr_ratio") >= 0.7)
          .then(pl.lit("expanded"))
          .otherwise(pl.lit("normal"))
          .alias("or_atr_bucket"),

        pl.when(pl.col("pd_or_high").is_null() | pl.col("pd_or_low").is_null())
          .then(pl.lit(None, dtype=pl.Utf8))
          .when(pl.col("or_low") > pl.col("pd_or_high"))
          .then(pl.lit("gap_up"))
          .when(pl.col("or_high") < pl.col("pd_or_low"))
          .then(pl.lit("gap_down"))
          .otherwise(pl.lit("inside"))
          .alias("pd_or_overlap_bucket"),
    ])
