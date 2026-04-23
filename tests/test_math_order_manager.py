"""Tests for MathOrderManager (DRY_RUN semantics, dedup, direction guard, prices)."""
from __future__ import annotations

from datetime import datetime, timedelta
from unittest.mock import MagicMock

import polars as pl
import pytest

from src.domain.constants import (
    MAGIC_NUMBER_MATH, MATH_STOP_ATR_OFFSET, MATH_WAIT_BARS,
)
from src.execution.math_order_manager import MathOrderManager


# ─── Helpers ────────────────────────────────────────────────────

def _make_bars(n: int, close_trend: float = 0.0, start: str = "2024-01-02 00:00",
               overrides: dict | None = None) -> pl.DataFrame:
    base = datetime.fromisoformat(start)
    times = [base + timedelta(minutes=15 * i) for i in range(n)]
    closes = [100.0 + close_trend * i for i in range(n)]
    data = {
        "time": times,
        "open": list(closes),
        "high": [c + 0.1 for c in closes],
        "low":  [c - 0.1 for c in closes],
        "close": list(closes),
        "atr_14": [1.0] * n,
        "velocity_10": [0.0] * n,
        "accel_10": [0.0] * n,
        "kama_10": list(closes),
        "kama_slope_10": [0.0] * n,
        "ols_slope_30": [0.0] * n,
        "hurst_rs_100": [0.5] * n,
        "kalman_innovation": [0.0] * n,
        "spectral_ratio_64": [1.0] * n,
    }
    if overrides:
        data.update(overrides)
    return pl.DataFrame(data)


def _long_ols_setup_on_last_bar(n: int = 80) -> pl.DataFrame:
    """Build bars that fire OLS_SLOPE_STRONG LONG on the last bar."""
    slope = [0.0] * n
    # Early noise to build rolling_std meaningful
    for i in range(5, 60):
        slope[i] = 0.1 * ((i % 5) - 2)
    # Last bars: strong rising positive slope
    slope[-3] = 0.3
    slope[-2] = 0.5
    slope[-1] = 0.9
    return _make_bars(n, overrides={"ols_slope_30": slope})


SETUP_CFG = {
    "sym": "EURUSD+",
    "internal_sym": "EURUSD",
    "tf": "M15",
    "session": "ALL_DAY",
    "setup_type": "OLS_SLOPE_STRONG",
    "direction_mode": "INVERTED",
    "tp_atr_mult": 0.75,
    "sl_atr_mult": 1.5,
    "atr_period": 14,
}


# ─── Tests ──────────────────────────────────────────────────────

def test_dry_run_does_not_call_mt5_order_send(monkeypatch):
    """DRY_RUN must never call mt5.order_send."""
    called = {"n": 0}

    fake_mt5 = MagicMock()
    def _boom(*a, **kw):
        called["n"] += 1
        raise AssertionError("order_send must not be called in DRY_RUN")
    fake_mt5.order_send = _boom

    # Inject fake mt5 into module namespace
    import src.execution.math_order_manager as mm
    monkeypatch.setattr(mm, "mt5", fake_mt5)

    om = MathOrderManager(client=MagicMock(), dry_run=True, telegram=None)
    bars = _long_ols_setup_on_last_bar()
    # Even if detector fires, DRY path skips mt5
    om.detect_and_place(SETUP_CFG, bars)
    assert called["n"] == 0


def test_magic_number_constant_is_1338():
    assert MAGIC_NUMBER_MATH == 1338


def test_dedup_prevents_second_placement_same_day():
    om = MathOrderManager(client=MagicMock(), dry_run=True, telegram=None)
    bars = _long_ols_setup_on_last_bar()

    first = om.detect_and_place(SETUP_CFG, bars)
    assert first is not None, "detector should fire on the last bar"
    assert om.has_pending_or_open_today("EURUSD+", "OLS_SLOPE_STRONG") is True

    second = om.detect_and_place(SETUP_CFG, bars)
    assert second is None, "dedup must block second placement same day"


def test_stop_price_flipped_for_inverted_long_detection():
    """Detector says LONG → INVERTED flips to SHORT → SELL_STOP below close-0.5*ATR."""
    om = MathOrderManager(client=MagicMock(), dry_run=True, telegram=None)
    bars = _long_ols_setup_on_last_bar()
    p = om.detect_and_place(SETUP_CFG, bars)
    assert p is not None
    assert p.original_direction == "LONG"
    assert p.flipped_direction == "SHORT"

    last_close = bars["close"][-1]
    atr = bars["atr_14"][-1]
    expected_stop = last_close - MATH_STOP_ATR_OFFSET * atr
    assert p.stop_price == pytest.approx(expected_stop, rel=1e-9)
    # TP is below entry (SHORT), SL above — validated by ordering:
    assert p.tp_price < p.stop_price < p.sl_price


def test_stop_price_flipped_for_inverted_short_detection():
    """A SHORT detector signal → INVERTED LONG → BUY_STOP above close+0.5*ATR."""
    n = 80
    slope = [0.0] * n
    for i in range(5, 60):
        slope[i] = 0.1 * ((i % 5) - 2)
    # Strong DECLINING slope (negative, strengthening) → SHORT
    slope[-3] = -0.3
    slope[-2] = -0.5
    slope[-1] = -0.9
    bars = _make_bars(n, overrides={"ols_slope_30": slope})

    om = MathOrderManager(client=MagicMock(), dry_run=True, telegram=None)
    p = om.detect_and_place(SETUP_CFG, bars)
    assert p is not None
    assert p.original_direction == "SHORT"
    assert p.flipped_direction == "LONG"

    last_close = bars["close"][-1]
    atr = bars["atr_14"][-1]
    expected_stop = last_close + MATH_STOP_ATR_OFFSET * atr
    assert p.stop_price == pytest.approx(expected_stop, rel=1e-9)
    # LONG: TP above entry, SL below
    assert p.sl_price < p.stop_price < p.tp_price


def test_expiration_is_five_m15_bars():
    om = MathOrderManager(client=MagicMock(), dry_run=True, telegram=None)
    bars = _long_ols_setup_on_last_bar()
    p = om.detect_and_place(SETUP_CFG, bars)
    assert p is not None
    delta = p.expiration_utc - datetime.now(p.expiration_utc.tzinfo)
    # Should be at most 75 min, within a few seconds of it
    assert timedelta(minutes=15 * MATH_WAIT_BARS - 1) < delta <= timedelta(
        minutes=15 * MATH_WAIT_BARS + 1
    )


def test_tick_pending_cancels_when_guard_weakens():
    om = MathOrderManager(client=MagicMock(), dry_run=True, telegram=None)

    # Build bars that fire LONG setup with strong slope
    bars = _long_ols_setup_on_last_bar()
    p = om.detect_and_place(SETUP_CFG, bars)
    assert p is not None
    # Guard at placement was the large positive slope (~0.9)
    assert p.guard_value_at_placement > 0

    # Now emit bars whose last ols_slope_30 value is near zero (weakened < 0.5 * g0)
    n = 80
    slope = [0.0] * n
    for i in range(5, 60):
        slope[i] = 0.1 * ((i % 5) - 2)
    slope[-1] = 0.05  # << 0.5 * 0.9 = 0.45
    weak_bars = _make_bars(n, overrides={"ols_slope_30": slope})

    cancelled = om.tick_pending(SETUP_CFG, weak_bars)
    assert cancelled == 1
    # Pending registry now empty for this key
    assert not any(v.symbol == "EURUSD+" and v.setup_type == "OLS_SLOPE_STRONG"
                   for v in om._pending.values())


def test_tick_pending_noop_when_guard_still_strong():
    om = MathOrderManager(client=MagicMock(), dry_run=True, telegram=None)
    bars = _long_ols_setup_on_last_bar()
    p = om.detect_and_place(SETUP_CFG, bars)
    assert p is not None

    # Guard still strong → no cancel
    n = 80
    slope = [0.0] * n
    for i in range(5, 60):
        slope[i] = 0.1 * ((i % 5) - 2)
    slope[-1] = 0.9  # same strength as placement
    strong_bars = _make_bars(n, overrides={"ols_slope_30": slope})

    cancelled = om.tick_pending(SETUP_CFG, strong_bars)
    assert cancelled == 0
    assert len(om._pending) == 1


def test_dry_run_submit_returns_sentinel_ticket():
    om = MathOrderManager(client=MagicMock(), dry_run=True, telegram=None)
    bars = _long_ols_setup_on_last_bar()
    p = om.detect_and_place(SETUP_CFG, bars)
    assert p is not None
    assert p.ticket == -1
    assert p.dry_run is True
