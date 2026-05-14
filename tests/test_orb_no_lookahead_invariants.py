from pathlib import Path

import polars as pl
import pytest

TRADES = Path("reports/orb/orb_phase_b_trades.parquet")
TRIGGERS = Path("reports/orb/orb_phase_a_triggers.parquet")


@pytest.mark.skipif(not TRADES.exists() or not TRIGGERS.exists(),
                    reason="pipeline outputs not present; run scripts/run_orb_pipeline.py first")
def test_every_fill_strictly_after_trigger():
    trades = pl.read_parquet(TRADES)
    if trades.is_empty():
        pytest.skip("empty trades parquet")
    assert "fill_ts" in trades.columns
    assert (trades["fill_ts"].is_not_null()).all()
    if "exit_ts" in trades.columns:
        nn = trades.filter(pl.col("exit_ts").is_not_null())
        if not nn.is_empty():
            assert (nn["exit_ts"] >= nn["fill_ts"]).all()
