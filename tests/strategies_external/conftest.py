"""Fixtures sintéticos para tests del módulo strategies_external."""

from datetime import datetime, timedelta
import polars as pl
import pytest


def _make_ohlc(rows: list[tuple[datetime, float, float, float, float, float]]) -> pl.DataFrame:
    """Helper: crea DataFrame OHLCV polars con schema canónico."""
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


@pytest.fixture
def df_h1_two_days() -> pl.DataFrame:
    """48 barras H1 (2 días completos) con valores deterministas."""
    base = datetime(2024, 1, 1, 0, 0, 0)
    rows = []
    for i in range(48):
        ts = base + timedelta(hours=i)
        # día 1: precio sube de 100 → 105 ; día 2: baja de 105 → 100
        if i < 24:
            o = 100.0 + i * 0.2
        else:
            o = 105.0 - (i - 24) * 0.2
        h = o + 0.5
        l = o - 0.5
        c = o + 0.1
        rows.append((ts, o, h, l, c, 1000.0))
    return _make_ohlc(rows)


@pytest.fixture
def df_daily_oops_long() -> pl.DataFrame:
    """5 barras daily diseñadas para que la barra final dispare OOPS LONG.

    Esquema:
      día 0..3: relleno
      día 3: high=110, low=105, close=108
      día 4: open=104 (gap bajo low[t-1]=105), high=109 (cruza low[t-1]=105 hacia arriba), low=103, close=108
    """
    base = datetime(2024, 1, 1)
    rows = [
        (base + timedelta(days=0), 100.0, 102.0, 99.0, 101.0, 1000.0),
        (base + timedelta(days=1), 101.0, 103.0, 100.0, 102.0, 1000.0),
        (base + timedelta(days=2), 102.0, 105.0, 101.0, 104.0, 1000.0),
        (base + timedelta(days=3), 104.0, 110.0, 105.0, 108.0, 1000.0),  # prev_low=105
        (base + timedelta(days=4), 104.0, 109.0, 103.0, 108.0, 1000.0),  # gap < prev_low, cruza arriba
    ]
    return _make_ohlc(rows)


@pytest.fixture
def df_daily_oops_short() -> pl.DataFrame:
    """Espejo del anterior: dispara OOPS SHORT en barra final."""
    base = datetime(2024, 1, 1)
    rows = [
        (base + timedelta(days=0), 100.0, 102.0, 99.0, 101.0, 1000.0),
        (base + timedelta(days=1), 101.0, 103.0, 100.0, 102.0, 1000.0),
        (base + timedelta(days=2), 102.0, 105.0, 101.0, 104.0, 1000.0),
        (base + timedelta(days=3), 104.0, 110.0, 105.0, 108.0, 1000.0),  # prev_high=110
        (base + timedelta(days=4), 112.0, 113.0, 109.0, 110.0, 1000.0),  # gap > prev_high, cruza abajo
    ]
    return _make_ohlc(rows)


@pytest.fixture
def df_m15_oops_long_tracking(df_daily_oops_long: pl.DataFrame) -> pl.DataFrame:
    """M15 que cubre el día 4 del fixture daily_oops_long.

    La barra daily t=4 tiene open=104, high=109, low=103, close=108.
    Construimos un tracking M15 (96 barras) que respeta esos extremos.
    Secuencia: open en 104, baja a 103 (low del día), sube a 109 (high del día), cierra a 108.
    """
    base = datetime(2024, 1, 5, 0, 0, 0)  # día 4 del fixture daily
    rows = []
    # 96 barras = 24h × 4 (M15)
    # Construcción manual: 104 → 103 → 109 → 108
    sequence = (
        [104.0] * 4   # primera hora
        + [104.0 - i * 0.05 for i in range(20)]   # baja hasta 103.0
        + [103.0 + i * 0.075 for i in range(40)]  # sube hasta ~106
        + [106.0 + i * 0.075 for i in range(40)]  # sube hasta 109
        # close
    )
    sequence = sequence[:96]
    sequence[-1] = 108.0  # forzar último close
    for i, price in enumerate(sequence):
        ts = base + timedelta(minutes=15 * i)
        h = price + 0.05
        l = price - 0.05
        rows.append((ts, price, h, l, price, 100.0))
    # Forzar low absoluto = 103 y high absoluto = 109
    rows[24] = (rows[24][0], 103.05, 103.10, 103.00, 103.05, 100.0)
    rows[60] = (rows[60][0], 108.95, 109.00, 108.90, 108.95, 100.0)
    return _make_ohlc(rows)
