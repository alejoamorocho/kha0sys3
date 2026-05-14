import polars as pl

from src.engine.orb_robustness import dedup_best_per_slot, REALISTIC_FILTER


def test_dedup_keeps_best_pf_log_trades():
    df = pl.DataFrame({
        "symbol": ["EURUSD"]*3,
        "magic_time": ["07:00"]*3,
        "or_duration_min": [60]*3,
        "pattern_id": ["BREAK_UP_X_compressed_inside"]*3,
        "direction": ["LONG"]*3,
        "entry_mode": ["MARKET", "STOP_RETEST", "LIMIT_PULLBACK"],
        "pf": [1.5, 2.0, 1.8],
        "trades_per_year": [50, 30, 60],
        "win_rate": [0.6, 0.65, 0.7],
        "expectancy_r": [0.2, 0.3, 0.25],
        "combo_id": ["c1", "c2", "c3"],
    })
    out = dedup_best_per_slot(df)
    assert len(out) == 1
    assert out["combo_id"].item() == "c3"


def test_realistic_filter_thresholds():
    assert REALISTIC_FILTER["wr_min"] == 0.55
    assert REALISTIC_FILTER["wr_max"] == 0.90
    assert REALISTIC_FILTER["pf_min"] == 1.5
    assert REALISTIC_FILTER["pf_max"] == 10.0
