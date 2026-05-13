"""Phase A integration test using a tiny in-memory dataset."""
from datetime import datetime

import polars as pl
import pytest

from src.engine.orb_universe_m1_mgmt import (
    aggregate_edge_per_pattern,
    PhaseAConfig,
)


def _trigger_row(pattern_id, direction, mfe_r, mae_r):
    return {
        "pattern_id": pattern_id,
        "direction": direction,
        "mfe_long_r": mfe_r if direction == "LONG" else 0.0,
        "mae_long_r": mae_r if direction == "LONG" else 0.0,
        "mfe_short_r": mfe_r if direction == "SHORT" else 0.0,
        "mae_short_r": mae_r if direction == "SHORT" else 0.0,
        "trigger_ts": datetime(2026, 1, 1, 8, 0),
    }


def test_aggregate_edge_filters_by_count_per_year():
    rows = [
        _trigger_row("BREAK_UP_ABOVE_PD_HIGH_compressed_gap_up", "LONG", 1.5, 0.5)
        for _ in range(20)
    ]
    span_days = 365
    df = pl.DataFrame(rows)
    out = aggregate_edge_per_pattern(df, span_days=span_days, cfg=PhaseAConfig())
    assert len(out) == 0, "pattern with <50/yr must be filtered"


def test_aggregate_edge_passes_when_count_and_edge_score_ok():
    rows = [
        _trigger_row("BREAK_UP_ABOVE_PD_HIGH_compressed_gap_up", "LONG", 1.5, 0.5)
        for _ in range(60)
    ]
    df = pl.DataFrame(rows)
    out = aggregate_edge_per_pattern(df, span_days=365, cfg=PhaseAConfig())
    assert len(out) == 1
    row = out.row(0, named=True)
    assert row["count"] == 60
    assert row["count_per_year"] == pytest.approx(60.0, rel=1e-2)
    assert row["p50_mfe_r"] == pytest.approx(1.5)
    assert row["p50_mae_r"] == pytest.approx(0.5)
    assert row["edge_score"] == pytest.approx(1.0)


def test_aggregate_edge_filters_low_mfe():
    rows = [
        _trigger_row("BREAK_UP_X_normal_inside", "LONG", 0.5, 0.4)
        for _ in range(60)
    ]
    df = pl.DataFrame(rows)
    out = aggregate_edge_per_pattern(df, span_days=365, cfg=PhaseAConfig())
    assert len(out) == 0
