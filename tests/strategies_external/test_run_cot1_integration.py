"""Integration test for run_cot1 runner.

Pre-places mock COT parquet files in tmp_path/cot/ to avoid live HTTP
downloads. Real OHLCV data from data/ is used for the actual backtest.
"""
from datetime import date, timedelta
from pathlib import Path

import polars as pl
import pytest

from src.strategies_external.runners.run_cot1 import run_cot1_backtest


def _make_mock_cot_parquet(cot_dir: Path, safe_keyword: str, year: int) -> None:
    """Write a minimal valid COT parquet for one year."""
    base = date(year, 1, 1)
    n_weeks = 52
    dates = [base + timedelta(weeks=i) for i in range(n_weeks)]
    # Simple COT: alternating long/short with net going from low to high
    longs = [100_000 + i * 1_000 for i in range(n_weeks)]
    shorts = [120_000 - i * 500 for i in range(n_weeks)]
    nets = [l - s for l, s in zip(longs, shorts)]
    df = pl.DataFrame(
        {"date": dates, "long": longs, "short": shorts, "net": nets},
        schema={"date": pl.Date, "long": pl.Int64, "short": pl.Int64, "net": pl.Int64},
    )
    cot_dir.mkdir(parents=True, exist_ok=True)
    df.write_parquet(cot_dir / f"{safe_keyword}_{year}.parquet")


@pytest.mark.integration
def test_run_cot1_real_data_produces_report(tmp_path: Path):
    cot_dir = tmp_path / "cot"

    # Pre-place mock COT parquets for XAUUSD (keyword=GOLD → safe=gold)
    for year in range(2018, 2026):
        _make_mock_cot_parquet(cot_dir, "gold", year)

    output = tmp_path / "cot1_backtest.md"
    summary = run_cot1_backtest(
        symbols=["XAUUSD"],
        data_dir="data",
        output_path=output,
        cot_dir=str(cot_dir),
        years=range(2018, 2026),
    )
    assert output.exists()
    assert "doc" in summary
    assert "indicator" in summary
    parquet = tmp_path / "cot1_trades.parquet"
    assert parquet.exists()
