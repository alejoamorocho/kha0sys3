from datetime import datetime, timedelta

import polars as pl
import pytest

from src.strategies_external.common.backtester import run_backtest
from src.strategies_external.common.signal import Signal


def _daily_df(rows):
    """Helper: construye DataFrame daily desde lista de tuplas (ts, o, h, l, c)."""
    return pl.DataFrame(
        {
            "time": [r[0] for r in rows],
            "open": [r[1] for r in rows],
            "high": [r[2] for r in rows],
            "low": [r[3] for r in rows],
            "close": [r[4] for r in rows],
            "volume": [1000.0] * len(rows),
        },
        schema={"time": pl.Datetime, "open": pl.Float64, "high": pl.Float64,
                "low": pl.Float64, "close": pl.Float64, "volume": pl.Float64},
    )


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


def test_exit_on_two_closes_against_long():
    """SMA-18 long: 2 cierres daily consecutivos bajo el nivel -> salir."""
    base = datetime(2024, 1, 1, 0, 0)
    # signal df: daily bars (00:00 each day)
    signal_rows = [
        (base, 100.0, 102.0, 99.0, 101.0),                            # day 0 close=101 above 100
        (base + timedelta(days=1), 101.0, 103.0, 100.0, 102.0),        # day 1 close=102 above
        (base + timedelta(days=2), 102.0, 102.5, 99.5, 99.8),          # day 2 close=99.8 below <- 1
        (base + timedelta(days=3), 99.8, 100.5, 99.0, 99.5),           # day 3 close=99.5 below <- 2 -> exit
        (base + timedelta(days=4), 99.5, 101.0, 99.0, 100.5),
    ]
    signal_df = _daily_df(signal_rows)

    # Tracking df: hourly bars over the 5 days
    tracking_rows = []
    for i in range(5 * 24):
        ts = base + timedelta(hours=i)
        day_idx = i // 24
        c = signal_rows[day_idx][4]
        tracking_rows.append((ts, c, c + 0.2, c - 0.2, c))

    tracking_df = pl.DataFrame(
        {
            "time": [r[0] for r in tracking_rows],
            "open": [r[1] for r in tracking_rows],
            "high": [r[2] for r in tracking_rows],
            "low": [r[3] for r in tracking_rows],
            "close": [r[4] for r in tracking_rows],
            "volume": [100.0] * len(tracking_rows),
        },
        schema={"time": pl.Datetime, "open": pl.Float64, "high": pl.Float64,
                "low": pl.Float64, "close": pl.Float64, "volume": pl.Float64},
    )
    sig = Signal(
        symbol="XAUUSD", strategy="sma18", side="long",
        setup_ts=base + timedelta(hours=1),  # fill on day 0
        entry_type="market", entry_price=101.0,
        valid_until=base + timedelta(days=10),
        stop=80.0,   # far away, won't hit
        tp1=None, tp2=None,
        exit_on_two_closes_against=100.0,   # SMA level
        exit_close_count_required=2,
    )
    trades = run_backtest([sig], tracking_df, exit_mode="doc",
                          signal_df=signal_df, risk_pct=0.01)
    assert len(trades) == 1
    t = trades[0]
    assert t.exit_reason == "signal_inverso"
    # exit at end of day 3 (close=99.5)
    assert t.exit == pytest.approx(99.5, abs=0.5)


def test_exit_after_bars_if_below_R_perdices():
    """Si tras N bars el pnl < threshold R, cerrar; si lo supera, no."""
    base = datetime(2024, 1, 1, 0, 0)
    rows = []
    # 300 bars; price drift very slowly -- never reaches 1R in 240 bars
    for i in range(300):
        ts = base + timedelta(minutes=i)
        c = 100.0 + i * 0.001   # very slow drift (0.001/bar, need 1.0 to hit 1R)
        rows.append((ts, c, c + 0.05, c - 0.05, c))

    df = pl.DataFrame(
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
    sig = Signal(
        symbol="XAUUSD", strategy="perdices_fib", side="long",
        setup_ts=base - timedelta(minutes=1),
        entry_type="market", entry_price=100.0,
        valid_until=base + timedelta(days=1),
        stop=99.0,   # R = 1.0
        tp1=None, tp2=None,
        exit_after_bars_if_below_R=(240, 1.0),   # 240 bars, 1R threshold
    )
    trades = run_backtest([sig], df, exit_mode="doc", risk_pct=0.005)
    assert len(trades) == 1
    assert trades[0].exit_reason == "timestop"
    assert trades[0].bars_in_trade == 240


def test_risk_pct_propagates_to_pnl_pct():
    """pnl_pct usa el risk_pct del runner, no el global default."""
    base = datetime(2024, 1, 1)
    rows = [(base + timedelta(minutes=i), 100.0 + i * 0.1,
             100.0 + i * 0.1 + 0.1, 100.0 + i * 0.1 - 0.1,
             100.0 + i * 0.1, 100.0) for i in range(20)]
    df = pl.DataFrame(
        {
            "time": [r[0] for r in rows],
            "open": [r[1] for r in rows],
            "high": [r[2] for r in rows],
            "low": [r[3] for r in rows],
            "close": [r[4] for r in rows],
            "volume": [r[5] for r in rows],
        },
        schema={"time": pl.Datetime, "open": pl.Float64, "high": pl.Float64,
                "low": pl.Float64, "close": pl.Float64, "volume": pl.Float64},
    )
    sig = Signal(
        symbol="SP500", strategy="oops", side="long",
        setup_ts=base - timedelta(minutes=1),
        entry_type="market", entry_price=100.0,
        valid_until=base + timedelta(minutes=20),
        stop=99.0, tp1=101.0, tp2=None,
    )
    # Use risk_pct=0.01 (1%) instead of default 0.005
    trades = run_backtest([sig], df, exit_mode="doc", risk_pct=0.01)
    assert len(trades) == 1
    # pnl_pct = pnl_R * 0.01 (not 0.005)
    assert trades[0].pnl_pct == pytest.approx(trades[0].pnl_R * 0.01, abs=1e-6)
