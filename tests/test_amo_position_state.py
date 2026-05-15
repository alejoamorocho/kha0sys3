"""Tests for the AMO8 DOC + SWING state machines."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from src.execution.amo_position_state import (
    Action,
    AmoPosition,
    Decision,
    PositionStateStore,
    apply_decision,
    evaluate,
    evaluate_doc,
    evaluate_swing,
)


# ─────────────────────────── helpers ───────────────────────────


def _doc_position(direction: str = "LONG",
                  entry: float = 1.10,
                  atr: float = 0.01,
                  or_width: float = 0.01,
                  initial_vol: float = 1.0,
                  placed_offset_min: int = 0) -> AmoPosition:
    """Build a typical DOC position. sl=1xOR, tp1=1xOR(50%), tp2=2xOR(50%)."""
    placed = datetime(2026, 1, 1, 10, 0, tzinfo=timezone.utc) + timedelta(minutes=placed_offset_min)
    p = AmoPosition(
        ticket=1001,
        strategy_id="AMO8_TEST_DOC",
        mode="DOC",
        direction=direction,
        broker_sym="EURUSD+",
        internal_sym="EURUSD",
        entry_price=entry,
        initial_volume=initial_vol,
        placed_at_iso=placed.isoformat(),
        max_hold_min=300,
        atr_at_setup=atr,
        or_width=or_width,
        sl_distance_initial=1.0 * or_width,
        tp1_distance=1.0 * or_width,
        tp2_distance=2.0 * or_width,
        tp1_fraction=0.5,
        tp2_fraction=0.5,
        midpoint_mfe_min_r=0.5,
    )
    p.init_levels()
    return p


def _swing_position(direction: str = "LONG",
                    entry: float = 1.10,
                    atr: float = 0.01,
                    initial_vol: float = 1.0,
                    sma_period: int = 3,
                    placed_offset_min: int = 0) -> AmoPosition:
    """Build a typical SWING position. sl=1xATR, tp1=2R(25%), tp2=4R(25%), trail SMA."""
    placed = datetime(2026, 1, 1, 10, 0, tzinfo=timezone.utc) + timedelta(minutes=placed_offset_min)
    risk_per_r = 0.5 * atr
    p = AmoPosition(
        ticket=2001,
        strategy_id="AMO8_TEST_SWING",
        mode="SWING",
        direction=direction,
        broker_sym="XAUUSD+",
        internal_sym="XAUUSD",
        entry_price=entry,
        initial_volume=initial_vol,
        placed_at_iso=placed.isoformat(),
        max_hold_min=600,
        atr_at_setup=atr,
        or_width=0.005,  # unused for SWING
        sl_distance_initial=1.0 * atr,
        tp1_distance=2.0 * risk_per_r,  # 2R
        tp2_distance=4.0 * risk_per_r,  # 4R
        tp1_fraction=0.25,
        tp2_fraction=0.25,
        sma_period=sma_period,
        swing_tp2_lock_r=1.0,
    )
    p.init_levels()
    return p


def _tick_args(now_offset_min: int,
               bid: float,
               ask: float,
               last_m1_high: float | None = None,
               last_m1_low: float | None = None,
               last_m1_close: float | None = None,
               base_now: datetime | None = None) -> dict:
    if base_now is None:
        base_now = datetime(2026, 1, 1, 10, 0, tzinfo=timezone.utc)
    return {
        "now": base_now + timedelta(minutes=now_offset_min),
        "bid": bid,
        "ask": ask,
        "last_m1_high": last_m1_high if last_m1_high is not None else ask,
        "last_m1_low": last_m1_low if last_m1_low is not None else bid,
        "last_m1_close": last_m1_close if last_m1_close is not None else (bid + ask) / 2,
    }


# ─────────────────────────── DOC tests ───────────────────────────


def test_doc_initial_state():
    """At placement, SL is set, no TPs hit, all volume remaining."""
    p = _doc_position()
    assert p.current_sl == pytest.approx(1.09)  # entry - 1×OR = 1.10 - 0.01
    assert p.tp1_price == pytest.approx(1.11)
    assert p.tp2_price == pytest.approx(1.12)
    assert p.remaining_volume == 1.0
    assert not p.tp1_hit and not p.tp2_hit


def test_doc_tp1_hit_partial_close_and_be_shift_long():
    p = _doc_position(direction="LONG", entry=1.10, or_width=0.01)
    # 1 min into trade, price spikes to 1.115 (high), bid/ask near 1.114
    args = _tick_args(1, bid=1.113, ask=1.114, last_m1_high=1.115, last_m1_low=1.111)
    d = evaluate_doc(p, **args)
    assert d.action == Action.PARTIAL_CLOSE
    assert d.fraction == pytest.approx(0.5)
    assert d.new_sl_price == pytest.approx(1.10)  # BE = entry
    assert d.reason == "DOC_TP1"
    apply_decision(p, d)
    assert p.tp1_hit
    assert p.remaining_volume == pytest.approx(0.5)
    assert p.current_sl == pytest.approx(1.10)


def test_doc_tp1_then_tp2_close_all():
    p = _doc_position(direction="LONG", entry=1.10, or_width=0.01)
    # TP1 hit
    apply_decision(p, evaluate_doc(p, **_tick_args(1, 1.113, 1.114, last_m1_high=1.115)))
    # Later, price spikes to 1.125 (TP2)
    d = evaluate_doc(p, **_tick_args(5, 1.123, 1.124, last_m1_high=1.125))
    assert d.action == Action.CLOSE_ALL
    assert d.reason == "DOC_TP2"
    apply_decision(p, d)
    assert p.tp2_hit
    assert p.remaining_volume == 0.0


def test_doc_midpoint_time_stop_low_mfe():
    """At max_hold/2 (150min), MFE has only been 0.3R (< 0.5R) → close all."""
    p = _doc_position()  # max_hold=300min, risk_per_r=0.005
    # 10 min in, MFE reaches only 0.003 = 0.6×0.005 = ... wait, MFE in PRICE units
    # 0.6R = 0.6 × 0.005 = 0.003. We want MFE < 0.5R = 0.0025
    # So set highs to 1.102 (only +0.002 = 0.4R MFE)
    apply_decision(p, evaluate_doc(p, **_tick_args(10, 1.101, 1.102, last_m1_high=1.102)))
    # No partial yet, mfe_price_unit = 0.002
    assert p.mfe_price_unit == pytest.approx(0.002)
    assert not p.tp1_hit
    # At 150 min midpoint: MFE still 0.002 < 0.5R=0.0025 → time-stop
    d = evaluate_doc(p, **_tick_args(150, 1.099, 1.100, last_m1_high=1.102))
    assert d.action == Action.CLOSE_ALL
    assert d.reason == "DOC_TIME_STOP_LOW_MFE"


def test_doc_midpoint_skipped_if_tp1_already_hit():
    p = _doc_position()
    apply_decision(p, evaluate_doc(p, **_tick_args(1, 1.113, 1.114, last_m1_high=1.115)))
    # Midpoint hits but TP1 already hit → no time-stop, HOLD
    d = evaluate_doc(p, **_tick_args(150, 1.100, 1.101, last_m1_high=1.115))
    assert d.action == Action.HOLD


def test_doc_max_hold_close():
    p = _doc_position()  # max_hold=300min
    d = evaluate_doc(p, **_tick_args(310, 1.099, 1.100))
    assert d.action == Action.CLOSE_ALL
    assert d.reason == "DOC_MAX_HOLD"


def test_doc_short_direction_mirror():
    p = _doc_position(direction="SHORT", entry=1.10, or_width=0.01)
    # tp1 = entry - 1×OR = 1.09
    assert p.tp1_price == pytest.approx(1.09)
    # Price drops to 1.089 (M1 low) — favorable for SHORT
    d = evaluate_doc(p, **_tick_args(1, 1.089, 1.090, last_m1_low=1.089, last_m1_high=1.091))
    assert d.action == Action.PARTIAL_CLOSE
    assert d.reason == "DOC_TP1"


# ─────────────────────────── SWING tests ───────────────────────────


def test_swing_initial_state():
    p = _swing_position()
    # SL = entry - 1×ATR = 1.10 - 0.01 = 1.09
    assert p.current_sl == pytest.approx(1.09)
    # tp1 = entry + 2R = 1.10 + 2×0.005 = 1.11
    assert p.tp1_price == pytest.approx(1.11)
    # tp2 = entry + 4R = 1.12
    assert p.tp2_price == pytest.approx(1.12)
    assert p.tp1_fraction == 0.25
    assert p.tp2_fraction == 0.25


def test_swing_tp1_then_tp2_then_trail():
    p = _swing_position(sma_period=3)
    # TP1 at +2R
    d = evaluate_swing(p, **_tick_args(1, 1.108, 1.109, last_m1_high=1.115, last_m1_close=1.108))
    assert d.action == Action.PARTIAL_CLOSE
    assert d.fraction == pytest.approx(0.25)
    assert d.new_sl_price == pytest.approx(1.10)  # BE
    assert d.reason == "SWING_TP1"
    apply_decision(p, d)
    assert p.remaining_volume == pytest.approx(0.75)
    # TP2 at +4R (price spikes to 1.125)
    d = evaluate_swing(p, **_tick_args(2, 1.118, 1.119, last_m1_high=1.125, last_m1_close=1.118))
    assert d.action == Action.PARTIAL_CLOSE
    assert d.fraction == pytest.approx(0.25)
    # Locked SL = entry + 1R = 1.105
    assert d.new_sl_price == pytest.approx(1.105)
    assert d.reason == "SWING_TP2"
    apply_decision(p, d)
    assert p.remaining_volume == pytest.approx(0.5)
    # Now trail with SMA. Build window: 3 closes around 1.12
    for offset, close in [(3, 1.121), (4, 1.122), (5, 1.119)]:
        d = evaluate_swing(p, **_tick_args(offset, 1.118, 1.119,
                                             last_m1_high=1.123, last_m1_close=close))
        # SMA is being built; close > sma typically, HOLD expected
        # SMA(3) at offset=5 = (1.121+1.122+1.119)/3 = 1.1207
        # close=1.119 < 1.1207 → trail triggers
    # Last iteration above should have triggered TRAIL_SMA
    assert d.action == Action.CLOSE_ALL
    assert d.reason == "SWING_TRAIL_SMA"


def test_swing_sl_before_tp1_holds_no_action():
    """SL is on the broker; state machine returns HOLD when no TP hit."""
    p = _swing_position()
    d = evaluate_swing(p, **_tick_args(1, 1.091, 1.092, last_m1_high=1.095, last_m1_low=1.091))
    # MFE is +0.005 (1.095-1.10? wait, 1.095<1.10 so MFE doesn't grow). High=1.095<entry=1.10 → no fav excursion
    # Actually for LONG, MFE = high - entry. 1.095-1.10 = -0.005. We clamp to non-positive→0.
    # So mfe_price_unit stays 0.
    assert d.action == Action.HOLD
    assert p.mfe_price_unit == 0.0


def test_swing_trail_not_active_before_tp2():
    """SMA trail only kicks in AFTER TP2. Before TP2, SMA cross is ignored."""
    p = _swing_position(sma_period=2)
    # Feed bars that build SMA but no TP hits
    for offset, close in [(1, 1.099), (2, 1.098), (3, 1.097)]:
        d = evaluate_swing(p, **_tick_args(offset, 1.096, 1.097,
                                             last_m1_high=1.099, last_m1_close=close))
        assert d.action == Action.HOLD


def test_swing_max_hold():
    p = _swing_position()  # max_hold=600
    d = evaluate_swing(p, **_tick_args(601, 1.099, 1.100))
    assert d.action == Action.CLOSE_ALL
    assert d.reason == "SWING_MAX_HOLD"


# ─────────────────────────── Dispatcher tests ───────────────────────────


def test_evaluate_dispatches_by_mode():
    p_doc = _doc_position()
    p_swing = _swing_position()
    p_atr = _doc_position()
    p_atr.mode = "ATR"
    args = _tick_args(1, 1.099, 1.100)
    assert evaluate(p_doc, **args).action == Action.HOLD
    assert evaluate(p_swing, **args).action == Action.HOLD
    # ATR positions don't use state machine
    assert evaluate(p_atr, **args).action == Action.HOLD


# ─────────────────────────── Persistence tests ───────────────────────────


def test_store_save_load_roundtrip(tmp_path):
    store = PositionStateStore(tmp_path)
    p = _doc_position()
    # Mutate state a bit
    apply_decision(p, evaluate_doc(p, **_tick_args(1, 1.113, 1.114, last_m1_high=1.115)))
    store.upsert(p)
    loaded = store.load()
    assert 1001 in loaded
    rp = loaded[1001]
    assert rp.tp1_hit is True
    assert rp.remaining_volume == pytest.approx(0.5)
    assert rp.current_sl == pytest.approx(1.10)
    assert rp.mode == "DOC"


def test_store_remove(tmp_path):
    store = PositionStateStore(tmp_path)
    store.upsert(_doc_position())
    assert 1001 in store.load()
    store.remove(1001)
    assert 1001 not in store.load()


def test_store_load_missing_file_returns_empty(tmp_path):
    store = PositionStateStore(tmp_path / "subdir")
    assert store.load() == {}


def test_store_load_corrupt_file_returns_empty(tmp_path):
    store = PositionStateStore(tmp_path)
    store.path.write_text("not valid json {{{", encoding="utf-8")
    assert store.load() == {}


def test_apply_decision_partial_close_decrements_volume():
    p = _doc_position(initial_vol=1.0)
    apply_decision(p, Decision(Action.PARTIAL_CLOSE, fraction=0.5, new_sl_price=1.10))
    assert p.remaining_volume == pytest.approx(0.5)
    assert p.current_sl == pytest.approx(1.10)


def test_apply_decision_partial_close_floors_at_zero():
    p = _doc_position(initial_vol=1.0)
    apply_decision(p, Decision(Action.PARTIAL_CLOSE, fraction=0.5))
    apply_decision(p, Decision(Action.PARTIAL_CLOSE, fraction=0.8))
    assert p.remaining_volume == 0.0


def test_apply_decision_close_all():
    p = _doc_position(initial_vol=1.0)
    apply_decision(p, Decision(Action.CLOSE_ALL))
    assert p.remaining_volume == 0.0
