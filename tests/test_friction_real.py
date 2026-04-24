"""Tests for real-broker friction_r conversions."""
from __future__ import annotations

import math

import pytest

from src.engine.friction_real import (
    REAL_FRICTION_TABLE,
    friction_r,
)


def test_table_has_all_15_universe_symbols():
    expected = {
        "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "GBPJPY", "EURJPY", "GBPAUD",
        "XAUUSD", "XAGUSD", "WTI", "BRENT", "NATGAS",
        "SP500", "NASDAQ100", "VIX",
    }
    assert set(REAL_FRICTION_TABLE.keys()) == expected


def test_friction_r_unknown_symbol_returns_fallback():
    assert friction_r("UNKNOWN", 2.5, 0.0006) == pytest.approx(0.1)


def test_friction_r_zero_atr_returns_fallback():
    assert friction_r("EURUSD", 2.5, 0.0) == pytest.approx(0.1)


def test_eurusd_friction_low():
    """EURUSD median ATR ~ 0.000612 => friction_R ~ 0.046."""
    r = friction_r("EURUSD", sl_atr_mult=2.5, median_atr=0.000612)
    assert 0.03 < r < 0.06


def test_xauusd_friction_moderate():
    """XAUUSD median ATR ~ 2.12 => tick_val/tick_size = 100, vol_min=0.01.
    risk_usd = 2.5 * 2.12 * 100 * 0.01 = 5.3; fric = 0.0712 / 5.3 = 0.0134."""
    r = friction_r("XAUUSD", sl_atr_mult=2.5, median_atr=2.12)
    assert math.isclose(r, 0.0712 / (2.5 * 2.12 * 100 * 0.01), rel_tol=1e-6)


def test_nas100_friction_higher_than_fx():
    """NAS100 ATR ~19, tick_val/tick_size=1, vol_min=0.1.
    risk_usd = 2.5*19*1*0.1 = 4.75; fric = 0.708/4.75 ≈ 0.149."""
    r = friction_r("NASDAQ100", sl_atr_mult=2.5, median_atr=19.14)
    assert r > friction_r("EURUSD", 2.5, 0.000612)
    assert 0.10 < r < 0.25


def test_natgas_friction_moderate():
    """NATGAS ATR ~ 0.0114. tick_val/tick_size=1000, vol_min=0.01.
    risk_usd = 2.5*0.0114*1000*0.01=0.285; fric=0.235/0.285=0.82."""
    r = friction_r("NATGAS", sl_atr_mult=2.5, median_atr=0.01139)
    assert r > 0.5  # NATGAS is meaningfully worse than FX


def test_friction_r_scales_inverse_with_sl_mult():
    r1 = friction_r("EURUSD", sl_atr_mult=1.0, median_atr=0.000612)
    r2 = friction_r("EURUSD", sl_atr_mult=2.5, median_atr=0.000612)
    assert math.isclose(r1, r2 * 2.5, rel_tol=1e-6)
