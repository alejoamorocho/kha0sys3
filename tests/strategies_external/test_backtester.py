from datetime import datetime, timedelta

import polars as pl
import pytest

from src.strategies_external.common.backtester import run_backtest
from src.strategies_external.common.signal import Signal


def _m15_track(rows):
    """Helper: construye DataFrame M15 desde lista de tuplas (ts, o, h, l, c)."""
    return pl.DataFrame(
        {
            "time": [r[0] for r in rows],
            "open": [r[1] for r in rows],
            "high": [r[2] for r in rows],
            "low": [r[3] for r in rows],
            "close": [r[4] for r in rows],
            "volume": [100.0] * len(rows),
        },
        schema={"time": pl.Datetime, "open": pl.Float64, "high": pl.Float64,
                "low": pl.Float64, "close": pl.Float64, "volume": pl.Float64},
    )


def test_long_stop_order_fills_on_high_breakout():
    """Una buy stop a 100.5 se llena cuando el high de la barra alcanza 100.5."""
    base = datetime(2024, 1, 5, 0, 0)
    df = _m15_track([
        (base, 100.0, 100.4, 99.8, 100.2),
        (base + timedelta(minutes=15), 100.2, 100.6, 100.1, 100.5),  # llena aquí
        (base + timedelta(minutes=30), 100.5, 102.0, 100.3, 101.8),  # tp = 102
        (base + timedelta(minutes=45), 101.8, 102.5, 101.5, 102.0),  # tp1 ya golpeado
    ])
    sig = Signal(
        symbol="SP500", strategy="oops", side="long",
        setup_ts=base - timedelta(minutes=15),
        entry_type="stop", entry_price=100.5,
        valid_until=base + timedelta(hours=8),
        stop=99.5, tp1=102.0, tp2=None,
    )
    trades = run_backtest([sig], df, exit_mode="doc")
    assert len(trades) == 1
    t = trades[0]
    assert t.exit_reason == "tp1"
    # entry con slippage: SP500 es índice → 1 tick adverso (asumimos 0.05 para test)
    # PnL bruto en R: (102 - 100.5) / (100.5 - 99.5) = 1.5R
    # Friction 0.2R → pnl_R = 1.5 - 0.2 = 1.3R
    assert t.pnl_R == pytest.approx(1.3, abs=0.05)


def test_long_stop_hit_before_tp_in_same_bar_resolves_as_stop():
    """Si una barra toca stop y tp simultáneamente, gana stop (worst-case conservador)."""
    base = datetime(2024, 1, 5, 0, 0)
    df = _m15_track([
        (base, 100.0, 100.4, 99.8, 100.2),
        (base + timedelta(minutes=15), 100.2, 100.6, 100.5, 100.5),
        (base + timedelta(minutes=30), 100.5, 102.5, 99.0, 101.0),  # toca stop y tp en la misma vela
    ])
    sig = Signal(
        symbol="SP500", strategy="oops", side="long",
        setup_ts=base - timedelta(minutes=15),
        entry_type="stop", entry_price=100.5,
        valid_until=base + timedelta(hours=8),
        stop=99.5, tp1=102.0, tp2=None,
    )
    trades = run_backtest([sig], df, exit_mode="doc")
    assert len(trades) == 1
    assert trades[0].exit_reason == "stop"
    # PnL: -1R (stop) - 0.2R (friction index) = -1.2R
    assert trades[0].pnl_R == pytest.approx(-1.2, abs=0.05)


def test_signal_expires_without_fill():
    base = datetime(2024, 1, 5, 0, 0)
    df = _m15_track([
        (base, 100.0, 100.2, 99.8, 100.1),
        (base + timedelta(minutes=15), 100.1, 100.3, 99.9, 100.2),
    ])
    sig = Signal(
        symbol="SP500", strategy="oops", side="long",
        setup_ts=base - timedelta(minutes=15),
        entry_type="stop", entry_price=101.0,  # nunca se alcanza
        valid_until=base + timedelta(minutes=30),
        stop=100.0, tp1=102.0, tp2=None,
    )
    trades = run_backtest([sig], df, exit_mode="doc")
    assert trades == []


def test_long_eod_close_when_no_tp_hit():
    """Si valid_until expira con la posición abierta y sin tp/stop, cierra al close de la última barra."""
    base = datetime(2024, 1, 5, 0, 0)
    df = _m15_track([
        (base, 100.0, 100.6, 99.8, 100.5),  # llena
        (base + timedelta(minutes=15), 100.5, 100.8, 100.2, 100.7),
        (base + timedelta(minutes=30), 100.7, 100.9, 100.4, 100.6),  # close final
    ])
    sig = Signal(
        symbol="SP500", strategy="oops", side="long",
        setup_ts=base - timedelta(minutes=15),
        entry_type="stop", entry_price=100.5,
        valid_until=base + timedelta(minutes=30),
        stop=99.5, tp1=999.0, tp2=None,
    )
    trades = run_backtest([sig], df, exit_mode="doc")
    assert len(trades) == 1
    assert trades[0].exit_reason == "eod"
    # entry slipped 100.5 → 100.55. PnL bruto = (100.6 - 100.55)/1.0 = 0.05R.
    # neto = 0.05 - 0.2 (friction index) = -0.15R
    assert trades[0].pnl_R == pytest.approx(-0.15, abs=0.02)
