# tests/strategies_external/test_run_sma18_integration.py
from pathlib import Path

import pytest

from src.strategies_external.runners.run_sma18 import run_sma18_backtest


@pytest.mark.integration
def test_run_sma18_real_data_produces_report(tmp_path: Path):
    output = tmp_path / "sma18_backtest.md"
    summary = run_sma18_backtest(
        symbols=["XAUUSD", "XAGUSD"],
        data_dir="data",
        output_path=output,
    )
    assert output.exists()
    content = output.read_text()
    assert "SMA18" in content
    assert "XAUUSD" in content
    assert "doc" in summary
    assert "indicator" in summary
    parquet = output.parent / "sma18_trades.parquet"
    assert parquet.exists()
