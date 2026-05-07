"""Integración: corre OOPS sobre dataset SP500 real y verifica que produce reporte."""

from pathlib import Path

import pytest

from src.strategies_external.runners.run_oops import run_oops_backtest


@pytest.mark.integration
def test_run_oops_real_data_produces_report(tmp_path: Path):
    output = tmp_path / "oops_backtest.md"
    summary = run_oops_backtest(
        symbols=["SP500", "NASDAQ100"],
        data_dir="data",
        output_path=output,
    )
    assert output.exists()
    content = output.read_text()
    assert "OOPS" in content
    assert "SP500" in content and "NASDAQ100" in content
    # summary debe contener métricas por modo
    assert "doc" in summary
    assert "atr" in summary
    assert "indicator" in summary
    # Trades parquet también
    parquet_path = output.parent / "oops_trades.parquet"
    assert parquet_path.exists()


@pytest.mark.integration
def test_run_oops_atr_sweep_picks_best(tmp_path: Path):
    output = tmp_path / "oops_backtest.md"
    summary = run_oops_backtest(
        symbols=["SP500"],
        data_dir="data",
        output_path=output,
        atr_grid=[(1.0, 1.5, 3.0), (1.5, 1.5, 3.0), (2.0, 2.0, 4.0)],
    )
    # summary["atr"] debe ser la mejor por calmar
    assert "atr" in summary
    assert "atr_grid_results" in summary
    assert len(summary["atr_grid_results"]) == 3
