# tests/strategies_external/test_run_perdices_fib_integration.py
from pathlib import Path

import pytest

from src.strategies_external.runners.run_perdices_fib import run_perdices_fib_backtest


@pytest.mark.integration
def test_run_perdices_fib_real_data_produces_report(tmp_path: Path):
    output = tmp_path / "perdices_fib_backtest.md"
    summary = run_perdices_fib_backtest(
        symbols=["XAUUSD", "XAGUSD"],
        data_dir="data",
        output_path=output,
    )
    assert output.exists()
    content = output.read_text()
    assert "perdices_fib" in content.lower()
    assert "XAUUSD" in content
    assert "doc" in summary
    assert "indicator" in summary
    parquet = output.parent / "perdices_fib_trades.parquet"
    assert parquet.exists()
