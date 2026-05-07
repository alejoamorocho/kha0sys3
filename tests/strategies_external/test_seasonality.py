from datetime import datetime, timedelta

import polars as pl
import pytest

from src.strategies_external.data_sources.seasonality import seasonal_mean_return


def test_seasonal_mean_return_basic():
    """All trades on same date over 3 years; mean return per (mm-dd) is returned."""
    base = datetime(2020, 1, 15)
    rows = []
    for year_offset in range(4):
        for day_offset in range(20):
            ts = datetime(2020 + year_offset, 1, 15) + timedelta(days=day_offset)
            close = 100.0 + day_offset + year_offset * 5
            rows.append((ts, close))
    df = pl.DataFrame(
        {"time": [r[0] for r in rows], "close": [r[1] for r in rows]},
        schema={"time": pl.Datetime, "close": pl.Float64},
    )
    out = seasonal_mean_return(df, window_days=5)
    # Should produce some entries
    assert len(out) > 0
    assert all(0 <= len(k) <= 5 for k in out.keys())  # "MM-DD" keys
