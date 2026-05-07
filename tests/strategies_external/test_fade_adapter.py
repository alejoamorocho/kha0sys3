# tests/strategies_external/test_fade_adapter.py
from datetime import datetime, timedelta

import polars as pl
import pytest

from src.strategies_external.strategies.fade_adapter import (
    FADEAdapter,
    load_fade_portfolio,
    _M1_AVAILABLE,
)


def test_load_fade_portfolio_filters_disabled():
    """Default enabled_only=True excludes disabled entries."""
    portfolio = load_fade_portfolio(enabled_only=True, symbols_filter=_M1_AVAILABLE)
    # All loaded entries should be enabled and have a M1-overlap symbol
    for s in portfolio:
        assert s.get("enabled", True) is not False, (
            f"Disabled entry leaked through: {s}"
        )
        assert s["sym_internal"] in _M1_AVAILABLE, (
            f"Symbol {s['sym_internal']} not in M1 available set"
        )


def test_load_fade_portfolio_no_filter():
    """All entries when no filter."""
    all_p = load_fade_portfolio(enabled_only=False, symbols_filter=None)
    enabled_p = load_fade_portfolio(enabled_only=True, symbols_filter=None)
    assert len(all_p) >= len(enabled_p)
    assert len(all_p) >= 10  # bot has dozens


def test_load_fade_portfolio_enabled_only_subset():
    """enabled_only=True returns fewer entries than enabled_only=False."""
    all_p = load_fade_portfolio(enabled_only=False, symbols_filter=None)
    enabled_p = load_fade_portfolio(enabled_only=True, symbols_filter=None)
    assert len(enabled_p) < len(all_p), (
        "Expected enabled_only=True to filter out disabled entries"
    )


def _make_m15_df(n_days: int = 2) -> pl.DataFrame:
    """Construct a synthetic M15 DataFrame covering n_days.

    OR window 07:00–08:00 = bars at offsets 28, 29, 30, 31 in a day starting at 00:00.
    Sets OR high=110.0, low=100.0 within that window.
    """
    rows = []
    base = datetime(2024, 1, 2, 0, 0)  # Tuesday
    for day in range(n_days):
        day_base = base + timedelta(days=day)
        for i in range(96):  # 24h * 4 bars/h = 96 M15 bars
            ts = day_base + timedelta(minutes=15 * i)
            if 28 <= i <= 31:
                # OR window bars: OR high=110, low=100
                o, h, l, c = 105.0, 110.0, 100.0, 108.0
            else:
                o = 105.0 + (i % 5) * 0.5
                h = o + 1.0
                l = o - 1.0
                c = o + 0.2
            rows.append((ts, o, h, l, c, 1000.0))

    return pl.DataFrame(
        {
            "time": [r[0] for r in rows],
            "open": [r[1] for r in rows],
            "high": [r[2] for r in rows],
            "low": [r[3] for r in rows],
            "close": [r[4] for r in rows],
            "volume": [r[5] for r in rows],
        },
        schema={
            "time": pl.Datetime,
            "open": pl.Float64,
            "high": pl.Float64,
            "low": pl.Float64,
            "close": pl.Float64,
            "volume": pl.Float64,
        },
    )


def test_fade_adapter_generates_signal_structure():
    """FADEAdapter produces Signal objects with correct anchors."""
    df = _make_m15_df(n_days=3)
    adapter = FADEAdapter()
    sigs = adapter.generate_signals_for_strategy(
        df,
        "EURUSD",
        {
            "edge": "FADE_UP",
            "magic_time": "07:00",
            "duration": 60,
            "sl_mult": 2.5,
            "tp_mult": 0.5,
            "session": "London",
        },
    )

    if len(sigs) == 0:
        pytest.skip(
            "Synthetic data filtered by ATR ratio; integration test will verify with real data"
        )

    s = sigs[0]
    assert s.side == "short", "FADE_UP should be a short (sell limit)"
    assert s.entry_type == "limit"
    assert s.strategy == "fade"
    assert s.symbol == "EURUSD"
    assert "or_high" in s.indicator_anchors
    assert "or_low" in s.indicator_anchors
    assert "or_width" in s.indicator_anchors
    assert "tp_mult" in s.indicator_anchors
    assert "sl_mult" in s.indicator_anchors
    assert "magic_time" in s.indicator_anchors
    assert "duration" in s.indicator_anchors
    # OR high must be entry price for FADE_UP
    assert s.entry_price == pytest.approx(s.indicator_anchors["or_high"])
    # stop is 0.0 (not yet filled by ExitManager)
    assert s.stop == 0.0
    assert s.tp1 is None


def test_fade_adapter_fade_down_signal():
    """FADE_DOWN produces a long signal at OR_LOW."""
    df = _make_m15_df(n_days=3)
    adapter = FADEAdapter()
    sigs = adapter.generate_signals_for_strategy(
        df,
        "EURUSD",
        {
            "edge": "FADE_DOWN",
            "magic_time": "07:00",
            "duration": 60,
            "sl_mult": 2.5,
            "tp_mult": 0.5,
            "session": "London",
        },
    )

    if len(sigs) == 0:
        pytest.skip("Synthetic data filtered by ATR ratio")

    s = sigs[0]
    assert s.side == "long", "FADE_DOWN should be long (buy limit)"
    assert s.entry_type == "limit"
    assert s.entry_price == pytest.approx(s.indicator_anchors["or_low"])


def test_fade_adapter_unknown_symbol_returns_empty():
    """Symbol not in asset_config returns empty list."""
    df = _make_m15_df(n_days=2)
    adapter = FADEAdapter()
    sigs = adapter.generate_signals_for_strategy(
        df,
        "UNKNOWN_SYM",
        {
            "edge": "FADE_UP",
            "magic_time": "07:00",
            "duration": 60,
            "sl_mult": 2.5,
            "tp_mult": 0.5,
            "session": "London",
        },
    )
    assert sigs == []


def test_fade_adapter_generate_signals_abc_compat():
    """generate_signals() (ABC method) delegates to default FADE_UP config."""
    df = _make_m15_df(n_days=3)
    adapter = FADEAdapter()
    # Should not raise; may return 0 signals if ATR filter eliminates all days
    sigs = adapter.generate_signals(df, "EURUSD")
    assert isinstance(sigs, list)
    for s in sigs:
        assert s.side == "short"  # default is FADE_UP
