from datetime import datetime, timedelta

import polars as pl
import pytest

from src.strategies_external.strategies.cot1 import COT1Strategy


@pytest.fixture
def cot_index_series():
    """Weekly series with COT Index = 90 for the last 5 weeks (long bias).

    Base is 2023-09-01 so that week 15 lands ~2023-12-31 and week 19 lands
    ~2024-01-28 — both before the pin bar at 2024-02-08 (day 38).
    With cot_lag_days=3 the most recent applicable COT at Feb-08 is week 19
    (Jan-28 + 3 = Jan-31 <= Feb-08), which has cot_index=90.
    """
    base = datetime(2023, 9, 1)
    return pl.DataFrame(
        {"date": [base + timedelta(weeks=i) for i in range(20)],
         "cot_index": [50.0] * 15 + [90.0] * 5},
        schema={"date": pl.Datetime, "cot_index": pl.Float64},
    )


@pytest.fixture
def daily_with_pin_bar():
    base = datetime(2024, 1, 1)
    rows = []
    for i in range(40):
        if i == 38:
            # pin bar bullish: long lower wick, body in upper third
            rows.append((base + timedelta(days=i), 100.0, 102.0, 95.0, 101.5, 1000.0))
        else:
            v = 100.0 + i * 0.05
            rows.append((base + timedelta(days=i), v, v + 0.3, v - 0.3, v, 1000.0))
    return pl.DataFrame(
        {"time": [r[0] for r in rows],
         "open": [r[1] for r in rows], "high": [r[2] for r in rows],
         "low": [r[3] for r in rows], "close": [r[4] for r in rows],
         "volume": [r[5] for r in rows]},
        schema={"time": pl.Datetime, "open": pl.Float64, "high": pl.Float64,
                "low": pl.Float64, "close": pl.Float64, "volume": pl.Float64},
    )


def test_cot1_long_signal(cot_index_series, daily_with_pin_bar):
    strat = COT1Strategy(cot_threshold_long=80.0, cot_threshold_short=20.0)
    seasonality = {"02-08": 0.01}  # positive seasonality on day idx 38
    sigs = strat.generate_signals(
        daily_with_pin_bar, symbol="XAUUSD",
        cot_index_series=cot_index_series,
        seasonality=seasonality,
    )
    long_sigs = [s for s in sigs if s.side == "long"]
    assert len(long_sigs) >= 1
