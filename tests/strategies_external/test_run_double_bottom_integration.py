# tests/strategies_external/test_run_double_bottom_integration.py
from pathlib import Path

import pytest

from src.strategies_external.runners.run_double_bottom import run_double_bottom_backtest


@pytest.mark.integration
def test_run_double_bottom_real_data_produces_report(tmp_path: Path):
    output = tmp_path / "double_bottom_backtest.md"
    summary = run_double_bottom_backtest(
        symbols=["XAUUSD", "XAGUSD"],
        data_dir="data",
        output_path=output,
    )
    assert output.exists()
    content = output.read_text()
    assert "double_bottom" in content.lower()
    assert "XAUUSD" in content
    assert "doc" in summary
    assert "indicator" in summary
    parquet = output.parent / "double_bottom_trades.parquet"
    assert parquet.exists()
