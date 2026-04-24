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


# ===== Hardening tests (retcodes, sweep, spread, risk sizing) =====


def _make_mt5_mock(retcode: int = 10009, order_id: int = 12345):
    """Build a fake mt5 module with just the attrs _submit_stop needs."""
    fake = MagicMock()
    fake.TRADE_RETCODE_DONE = 10009
    fake.TRADE_ACTION_PENDING = 5
    fake.TRADE_ACTION_REMOVE = 6
    fake.ORDER_TYPE_BUY_STOP = 4
    fake.ORDER_TYPE_SELL_STOP = 5
    fake.ORDER_TIME_SPECIFIED = 2
    fake.ORDER_FILLING_RETURN = 2
    fake.ORDER_FILLING_IOC = 1
    # symbol_info: volume_min/step, tick_value/size, visible, spread
    sym_info = MagicMock()
    sym_info.volume_min = 0.01
    sym_info.volume_step = 0.01
    sym_info.trade_tick_size = 0.00001
    sym_info.trade_tick_value = 1.0
    sym_info.point = 0.00001
    sym_info.spread = 10
    fake.symbol_info = MagicMock(return_value=sym_info)
    acct = MagicMock()
    acct.balance = 1000.0
    fake.account_info = MagicMock(return_value=acct)
    fake.last_error = MagicMock(return_value="none")
    # Response for order_send
    res = MagicMock()
    res.retcode = retcode
    res.order = order_id
    fake.order_send = MagicMock(return_value=res)
    return fake


def _submit_args():
    from datetime import datetime as _dt, timedelta as _td, timezone as _tz
    return dict(
        symbol="EURUSD+", order_type="BUY_STOP",
        stop_price=1.1000, sl=1.0950, tp=1.1050,
        setup_type="OLS_SLOPE_STRONG", session="ASIA",
        expiration=_dt.now(_tz.utc) + _td(minutes=75),
        expected_wr=0.80,
    )


def test_retcode_10015_handled_without_crash(monkeypatch):
    from src.execution.risk_manager import DynamicRiskAllocator
    fake_mt5 = _make_mt5_mock(retcode=10015)
    import src.execution.math_order_manager as mm
    monkeypatch.setattr(mm, "mt5", fake_mt5)

    om = MathOrderManager(
        client=MagicMock(), dry_run=False, telegram=None,
        risk_allocator=DynamicRiskAllocator(),
    )
    ticket = om._submit_stop(**_submit_args())
    assert ticket is None  # skip, no crash
    assert fake_mt5.order_send.called


def test_retcode_10018_handled_without_crash(monkeypatch):
    from src.execution.risk_manager import DynamicRiskAllocator
    fake_mt5 = _make_mt5_mock(retcode=10018)
    import src.execution.math_order_manager as mm
    monkeypatch.setattr(mm, "mt5", fake_mt5)

    om = MathOrderManager(
        client=MagicMock(), dry_run=False, telegram=None,
        risk_allocator=DynamicRiskAllocator(),
    )
    ticket = om._submit_stop(**_submit_args())
    assert ticket is None  # skip quiet


def test_sweep_stale_cancels_orders_older_than_90min(monkeypatch):
    from datetime import datetime as _dt, timezone as _tz
    fake_mt5 = _make_mt5_mock(retcode=10009)
    # Two MATH orders: one fresh (5min old), one stale (120min old)
    now_ts = int(_dt.now(_tz.utc).timestamp())
    fresh = MagicMock(ticket=1, magic=1338, symbol="EURUSD+",
                      time_setup=now_ts - 5 * 60)
    stale = MagicMock(ticket=2, magic=1338, symbol="EURUSD+",
                      time_setup=now_ts - 120 * 60)
    other = MagicMock(ticket=3, magic=1337, symbol="EURUSD+",  # FADE bot
                      time_setup=now_ts - 180 * 60)
    fake_mt5.orders_get = MagicMock(return_value=[fresh, stale, other])

    import src.execution.math_order_manager as mm
    monkeypatch.setattr(mm, "mt5", fake_mt5)

    om = MathOrderManager(client=MagicMock(), dry_run=False, telegram=None)
    n = om.sweep_stale()
    assert n == 1
    # Verify it targeted ticket=2 with REMOVE action
    calls = fake_mt5.order_send.call_args_list
    assert any(call.args[0].get("order") == 2
               and call.args[0].get("action") == fake_mt5.TRADE_ACTION_REMOVE
               for call in calls)


def test_spread_gate_blocks_when_spread_too_high(monkeypatch):
    from src.execution.risk_manager import DynamicRiskAllocator
    fake_mt5 = _make_mt5_mock(retcode=10009)
    import src.execution.math_order_manager as mm
    monkeypatch.setattr(mm, "mt5", fake_mt5)

    om = MathOrderManager(
        client=MagicMock(), dry_run=False, telegram=None,
        risk_allocator=DynamicRiskAllocator(),
    )
    # Seed typical spread at 10
    om._typical_spread = {"EURUSD+": 10.0}
    # Now broker reports spread=100 (10x typical > 2.5x limit)
    fake_mt5.symbol_info.return_value.spread = 100
    ticket = om._submit_stop(**_submit_args())
    assert ticket is None
    # order_send must NOT have been called (gate blocked before request)
    assert fake_mt5.order_send.call_count == 0


def test_compute_volume_respects_expected_wr(monkeypatch):
    """Higher WR -> bigger lot; lower WR -> smaller lot."""
    from src.execution.risk_manager import DynamicRiskAllocator
    fake_mt5 = _make_mt5_mock(retcode=10009)
    import src.execution.math_order_manager as mm
    monkeypatch.setattr(mm, "mt5", fake_mt5)

    alloc = DynamicRiskAllocator(min_risk=0.01, max_risk=0.15,
                                  min_wr=0.57, max_wr=1.00)
    om = MathOrderManager(
        client=MagicMock(), dry_run=False, telegram=None,
        risk_allocator=alloc,
    )
    sym_info = fake_mt5.symbol_info.return_value
    lots_high = om._compute_volume(sym_info, entry=1.1000, sl=1.0950,
                                   expected_wr=1.00)
    lots_low = om._compute_volume(sym_info, entry=1.1000, sl=1.0950,
                                  expected_wr=0.57)
    assert lots_high > lots_low
    # Sanity: 15x ratio roughly matches risk scale (allow slop for lot rounding)
    assert lots_high / max(lots_low, 0.01) > 5.0
