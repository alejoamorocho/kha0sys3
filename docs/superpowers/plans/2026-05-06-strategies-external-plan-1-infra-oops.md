# Strategies External — Plan 1: Infra + OOPS Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Montar la infraestructura común del módulo `src/strategies_external/` (data loader extension, tipos Signal/Trade, ExitManagers, backtester, metrics, walk-forward, monte carlo, report writer) y validarla acabando con la estrategia OOPS (Larry Williams) backtesteada de punta a punta sobre SP500 y NASDAQ100, con reporte en `reports/external/oops_backtest.md`.

**Architecture:** Módulo aislado del bot live (FADE/MATH). Reusa `CSVPolarsLoader` de `src/infrastructure/data/polars_loader.py`. Polars vectorizado en todo. Daily-signal + intra-bar tracking sobre el TF más fino disponible (M1>M5>M15). Tres modos de exit comparables (`doc`, `atr`, `indicator`) seleccionables por runner.

**Tech Stack:** Python 3.11+, polars, pytest, scipy (find_peaks reservado para Plan 2), numpy. **No** pandas dentro del módulo.

**Spec de referencia:** `docs/superpowers/specs/2026-05-06-strategies-external-design.md`.

**Convención TDD:** RED → GREEN → COMMIT por task. Cada commit es atómico y revertible.

---

## File Structure (alcance Plan 1)

```
src/strategies_external/
├── __init__.py
├── constants.py
├── data_loader.py              # Extiende CSVPolarsLoader con aggregate_to_daily, load_m1, load_m5, best_tracking_tf
├── exit_managers.py            # ExitManager ABC + DocExitManager + ATRExitManager + IndicatorExitManager
├── common/
│   ├── __init__.py
│   ├── signal.py               # @dataclass Signal
│   ├── trade.py                # @dataclass Trade
│   ├── backtester.py           # run() loop genérico
│   ├── metrics.py              # evaluate(trades) → dict
│   ├── walk_forward.py         # rolling 70/30
│   └── monte_carlo.py          # bootstrap 10k
├── strategies/
│   ├── __init__.py
│   ├── base.py                 # Strategy ABC
│   └── oops.py                 # OOPS implementation
├── reporting/
│   ├── __init__.py
│   └── markdown.py             # write_backtest_report
└── runners/
    ├── __init__.py
    └── run_oops.py             # Entry point ejecutable

tests/strategies_external/
├── __init__.py
├── conftest.py                 # Fixtures de DataFrames sintéticos
├── test_data_loader.py
├── test_signal.py
├── test_trade.py
├── test_exit_managers.py
├── test_backtester.py
├── test_metrics.py
├── test_walk_forward.py
├── test_monte_carlo.py
├── test_oops_strategy.py
├── test_markdown_report.py
└── test_run_oops_integration.py

docs/superpowers/specs/
└── 2026-05-06-strategies-external-design.md   (ya existe)

reports/external/
└── (output del runner — generado, no committed)
```

**Files que NO se tocan en Plan 1:** todo `src/execution/`, `src/engine/`, `src/domain/`, `src/application/`, `bot_config*.json`, `scripts/`.

---

## Task 1: Crear estructura del módulo y constantes

**Files:**
- Create: `src/strategies_external/__init__.py`
- Create: `src/strategies_external/constants.py`
- Create: `src/strategies_external/common/__init__.py`
- Create: `src/strategies_external/strategies/__init__.py`
- Create: `src/strategies_external/reporting/__init__.py`
- Create: `src/strategies_external/runners/__init__.py`
- Create: `tests/strategies_external/__init__.py`

- [ ] **Step 1: Crear los `__init__.py` vacíos**

```python
# src/strategies_external/__init__.py
"""External strategies research module.

Backtest-only. Aislado del bot live (FADE/MATH).
Spec: docs/superpowers/specs/2026-05-06-strategies-external-design.md
"""
```

Los demás `__init__.py` quedan vacíos (un único caracter de salto de línea).

- [ ] **Step 2: Crear `constants.py` con constantes locales**

```python
# src/strategies_external/constants.py
"""Constantes locales del módulo strategies_external.

Replicamos friction y risk del bot live para que las métricas sean comparables.
NO importamos de src/domain/constants.py para mantener el aislamiento.
"""

from typing import Final

# Friction en R aplicado al cierre de cada trade.
FRICTION_R_FOREX: Final[float] = 0.1
FRICTION_R_COMMODITY_INDEX: Final[float] = 0.2

# Position sizing default (parametrizable por runner).
RISK_PER_TRADE_PCT_DEFAULT: Final[float] = 0.005

# Slippage en la entrada por orden tipo stop/limit.
SLIPPAGE_PIPS_FX: Final[float] = 0.5
SLIPPAGE_TICKS_INDEX_COMMODITY: Final[int] = 1

# Asset class mapping.
ASSET_CLASS_FOREX: Final[frozenset[str]] = frozenset({
    "AUDUSD", "EURJPY", "EURUSD", "GBPAUD", "GBPJPY", "GBPUSD", "USDJPY",
})
ASSET_CLASS_METALS: Final[frozenset[str]] = frozenset({"XAUUSD", "XAGUSD"})
ASSET_CLASS_ENERGY: Final[frozenset[str]] = frozenset({"WTI", "BRENT", "NATGAS"})
ASSET_CLASS_INDEX: Final[frozenset[str]] = frozenset({"SP500", "NASDAQ100", "VIX"})


def friction_for(symbol: str) -> float:
    """Friction en R según asset class del símbolo."""
    if symbol in ASSET_CLASS_FOREX:
        return FRICTION_R_FOREX
    return FRICTION_R_COMMODITY_INDEX
```

- [ ] **Step 3: Verificar estructura**

Run:
```bash
python -c "import src.strategies_external; from src.strategies_external.constants import friction_for; print(friction_for('XAUUSD'), friction_for('EURUSD'))"
```

Expected: `0.2 0.1`

- [ ] **Step 4: Commit**

```bash
git add src/strategies_external tests/strategies_external/__init__.py
git commit -m "feat(strategies_external): scaffold module structure and constants"
```

---

## Task 2: conftest.py con fixtures sintéticos

**Files:**
- Create: `tests/strategies_external/conftest.py`

- [ ] **Step 1: Escribir conftest con fixtures que cubren los casos de test**

```python
# tests/strategies_external/conftest.py
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
```

- [ ] **Step 2: Verificar que los fixtures cargan sin errores**

Run:
```bash
pytest tests/strategies_external/conftest.py --collect-only
```

Expected: collected 0 items (sin tests todavía, pero sin errores de import)

- [ ] **Step 3: Commit**

```bash
git add tests/strategies_external/conftest.py
git commit -m "test(strategies_external): add OHLC fixtures for unit tests"
```

---

## Task 3: data_loader — `aggregate_to_daily`

**Files:**
- Create: `src/strategies_external/data_loader.py`
- Create: `tests/strategies_external/test_data_loader.py`

- [ ] **Step 1: Escribir el test failing**

```python
# tests/strategies_external/test_data_loader.py
"""Tests para data_loader del módulo strategies_external."""

import polars as pl
import pytest

from src.strategies_external.data_loader import aggregate_to_daily


def test_aggregate_to_daily_two_full_days(df_h1_two_days: pl.DataFrame):
    """48 barras H1 → 2 barras daily. OHLC se calcula correctamente."""
    daily = aggregate_to_daily(df_h1_two_days)

    assert daily.shape[0] == 2

    day1 = daily.row(0, named=True)
    # día 1 (i=0..23): open[0]=100.0, max high = 100+23*0.2+0.5=105.1, min low=99.5, close[23]=104.7
    assert day1["open"] == pytest.approx(100.0)
    assert day1["high"] == pytest.approx(105.1)
    assert day1["low"] == pytest.approx(99.5)
    assert day1["close"] == pytest.approx(104.7)

    day2 = daily.row(1, named=True)
    # día 2 (i=24..47): o(i)=105-(i-24)*0.2 → o(47)=100.4, h(47)=100.9, l(47)=99.9, c(47)=100.5
    # max h del día está en i=24 (105.5); min l del día está en i=47 (99.9); close = c(47) = 100.5
    assert day2["open"] == pytest.approx(105.0)
    assert day2["high"] == pytest.approx(105.5)
    assert day2["low"] == pytest.approx(99.9)
    assert day2["close"] == pytest.approx(100.5)


def test_aggregate_to_daily_volume_sum(df_h1_two_days: pl.DataFrame):
    """volume diario = sum de las 24 barras H1."""
    daily = aggregate_to_daily(df_h1_two_days)
    assert daily["volume"].to_list() == [24000.0, 24000.0]


def test_aggregate_to_daily_empty():
    """DataFrame vacío produce DataFrame vacío con schema correcto."""
    empty = pl.DataFrame(schema={
        "time": pl.Datetime, "open": pl.Float64, "high": pl.Float64,
        "low": pl.Float64, "close": pl.Float64, "volume": pl.Float64,
    })
    daily = aggregate_to_daily(empty)
    assert daily.shape[0] == 0
    assert daily.columns == ["time", "open", "high", "low", "close", "volume"]
```

- [ ] **Step 2: Run test — verificar que falla por ImportError**

Run:
```bash
pytest tests/strategies_external/test_data_loader.py -v
```

Expected: ImportError "No module named 'src.strategies_external.data_loader'"

- [ ] **Step 3: Implementar `aggregate_to_daily`**

```python
# src/strategies_external/data_loader.py
"""Extensiones del cargador de datos para strategies_external.

Reusa CSVPolarsLoader de src/infrastructure/data/polars_loader.py.
Añade resampling y selección de tracking timeframe.
"""

from pathlib import Path

import polars as pl

from src.infrastructure.data.polars_loader import CSVPolarsLoader


_OHLC_COLS = ["time", "open", "high", "low", "close", "volume"]


def aggregate_to_daily(df: pl.DataFrame) -> pl.DataFrame:
    """Resamplea OHLCV a daily.

    Reglas: open=first, high=max, low=min, close=last, volume=sum.
    Asume `time` ya es polars Datetime y el DataFrame está ordenado.
    Devuelve un DataFrame con las mismas columnas; `time` queda al inicio del día.
    """
    if df.is_empty():
        return df.select(_OHLC_COLS)

    return (
        df.sort("time")
        .group_by_dynamic("time", every="1d", closed="left", label="left")
        .agg(
            pl.col("open").first(),
            pl.col("high").max(),
            pl.col("low").min(),
            pl.col("close").last(),
            pl.col("volume").sum(),
        )
        .select(_OHLC_COLS)
    )
```

- [ ] **Step 4: Run test — verificar que pasa**

Run:
```bash
pytest tests/strategies_external/test_data_loader.py -v
```

Expected: 3 passed

- [ ] **Step 5: Commit**

```bash
git add src/strategies_external/data_loader.py tests/strategies_external/test_data_loader.py
git commit -m "feat(strategies_external): aggregate_to_daily resampler"
```

---

## Task 4: data_loader — `load_m1`, `load_m5`, `load_csv` wrapper

**Files:**
- Modify: `src/strategies_external/data_loader.py`
- Modify: `tests/strategies_external/test_data_loader.py`

- [ ] **Step 1: Añadir tests failing**

Append a `tests/strategies_external/test_data_loader.py`:

```python
from src.strategies_external.data_loader import load_csv, load_m1, load_m5


def test_load_csv_returns_polars_with_canonical_schema(tmp_path):
    """load_csv lee un CSV con el formato del proyecto y normaliza schema."""
    csv_file = tmp_path / "EURUSD_H1_20180101_20180101.csv"
    csv_file.write_text(
        "time,open,high,low,close,volume\n"
        "2018-01-01 00:00:00+00:00,1.20,1.21,1.19,1.205,1000.0\n"
        "2018-01-01 01:00:00+00:00,1.205,1.215,1.20,1.21,1500.0\n"
    )
    df = load_csv("EURUSD", "H1", data_dir=str(tmp_path))
    assert df.columns == ["time", "open", "high", "low", "close", "volume"]
    assert df["time"].dtype == pl.Datetime
    assert df.shape[0] == 2


def test_load_csv_missing_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_csv("NOPE", "H1", data_dir=str(tmp_path))


def test_load_m1_returns_none_when_missing(tmp_path):
    """load_m1 devuelve None si no existe data/M1/<symbol>.csv."""
    assert load_m1("EURUSD", data_dir=str(tmp_path)) is None


def test_load_m5_returns_none_when_missing(tmp_path):
    assert load_m5("EURUSD", data_dir=str(tmp_path)) is None


def test_load_m1_loads_when_present(tmp_path):
    m1_dir = tmp_path / "M1"
    m1_dir.mkdir()
    (m1_dir / "EURUSD.csv").write_text(
        "time,open,high,low,close,volume\n"
        "2024-01-01 00:00:00+00:00,1.10,1.11,1.09,1.105,500.0\n"
    )
    df = load_m1("EURUSD", data_dir=str(tmp_path))
    assert df is not None
    assert df.shape[0] == 1
    assert df["time"].dtype == pl.Datetime
```

- [ ] **Step 2: Run failing tests**

Run:
```bash
pytest tests/strategies_external/test_data_loader.py::test_load_csv_returns_polars_with_canonical_schema -v
```

Expected: ImportError "load_csv"

- [ ] **Step 3: Implementar `load_csv`, `load_m1`, `load_m5`**

Append a `src/strategies_external/data_loader.py`:

```python
def load_csv(symbol: str, tf: str, data_dir: str = "data") -> pl.DataFrame:
    """Carga el CSV histórico para (symbol, tf) reusando CSVPolarsLoader.

    Devuelve DataFrame con columnas canónicas en orden _OHLC_COLS.
    """
    loader = CSVPolarsLoader(data_dir)
    df = loader.load_data(symbol, tf)
    return df.select(_OHLC_COLS)


def _load_fine_tf(symbol: str, subdir: str, data_dir: str) -> pl.DataFrame | None:
    """Helper: lee data_dir/<subdir>/<symbol>.csv si existe, sino None."""
    path = Path(data_dir) / subdir / f"{symbol}.csv"
    if not path.is_file():
        return None
    df = pl.read_csv(path, has_header=True)
    df = df.rename({c: c.strip().lower() for c in df.columns})
    df = df.with_columns(
        pl.col("time")
        .str.slice(0, 19)
        .str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S", strict=False)
    )
    return df.sort("time").select(_OHLC_COLS)


def load_m1(symbol: str, data_dir: str = "data") -> pl.DataFrame | None:
    """Lee data/M1/<symbol>.csv si existe; None si no."""
    return _load_fine_tf(symbol, "M1", data_dir)


def load_m5(symbol: str, data_dir: str = "data") -> pl.DataFrame | None:
    """Lee data/M5/<symbol>.csv si existe; None si no."""
    return _load_fine_tf(symbol, "M5", data_dir)
```

- [ ] **Step 4: Run tests**

Run:
```bash
pytest tests/strategies_external/test_data_loader.py -v
```

Expected: 8 passed

- [ ] **Step 5: Commit**

```bash
git add src/strategies_external/data_loader.py tests/strategies_external/test_data_loader.py
git commit -m "feat(strategies_external): load_csv/load_m1/load_m5 helpers"
```

---

## Task 5: data_loader — `best_tracking_tf`

**Files:**
- Modify: `src/strategies_external/data_loader.py`
- Modify: `tests/strategies_external/test_data_loader.py`

- [ ] **Step 1: Añadir test failing**

Append a `tests/strategies_external/test_data_loader.py`:

```python
from src.strategies_external.data_loader import best_tracking_tf


def test_best_tracking_tf_prefers_m1(tmp_path):
    """Si existe M1, devuelve ('M1', df)."""
    (tmp_path / "M1").mkdir()
    (tmp_path / "M5").mkdir()
    (tmp_path / "M1" / "EURUSD.csv").write_text(
        "time,open,high,low,close,volume\n"
        "2024-01-01 00:00:00+00:00,1.10,1.11,1.09,1.105,500.0\n"
    )
    (tmp_path / "M5" / "EURUSD.csv").write_text(
        "time,open,high,low,close,volume\n"
        "2024-01-01 00:00:00+00:00,1.10,1.11,1.09,1.105,500.0\n"
    )
    tf, df = best_tracking_tf("EURUSD", data_dir=str(tmp_path))
    assert tf == "M1"
    assert df.shape[0] == 1


def test_best_tracking_tf_falls_back_to_m5(tmp_path):
    (tmp_path / "M5").mkdir()
    (tmp_path / "M5" / "EURUSD.csv").write_text(
        "time,open,high,low,close,volume\n"
        "2024-01-01 00:00:00+00:00,1.10,1.11,1.09,1.105,500.0\n"
    )
    # Crear M15 también
    (tmp_path / "EURUSD_M15_20240101_20240101.csv").write_text(
        "time,open,high,low,close,volume\n"
        "2024-01-01 00:00:00+00:00,1.10,1.11,1.09,1.105,500.0\n"
    )
    tf, _ = best_tracking_tf("EURUSD", data_dir=str(tmp_path))
    assert tf == "M5"


def test_best_tracking_tf_falls_back_to_m15(tmp_path):
    (tmp_path / "EURUSD_M15_20240101_20240101.csv").write_text(
        "time,open,high,low,close,volume\n"
        "2024-01-01 00:00:00+00:00,1.10,1.11,1.09,1.105,500.0\n"
    )
    tf, _ = best_tracking_tf("EURUSD", data_dir=str(tmp_path))
    assert tf == "M15"


def test_best_tracking_tf_raises_when_nothing(tmp_path):
    with pytest.raises(FileNotFoundError):
        best_tracking_tf("EURUSD", data_dir=str(tmp_path))
```

- [ ] **Step 2: Run failing test**

Run:
```bash
pytest tests/strategies_external/test_data_loader.py::test_best_tracking_tf_prefers_m1 -v
```

Expected: ImportError

- [ ] **Step 3: Implementar `best_tracking_tf`**

Append a `src/strategies_external/data_loader.py`:

```python
def best_tracking_tf(symbol: str, data_dir: str = "data") -> tuple[str, pl.DataFrame]:
    """Devuelve (tf_label, df) eligiendo el TF más fino disponible: M1 > M5 > M15.

    Raises:
        FileNotFoundError: si no hay datos para el símbolo en ningún TF.
    """
    df_m1 = load_m1(symbol, data_dir)
    if df_m1 is not None:
        return "M1", df_m1
    df_m5 = load_m5(symbol, data_dir)
    if df_m5 is not None:
        return "M5", df_m5
    return "M15", load_csv(symbol, "M15", data_dir)
```

- [ ] **Step 4: Run tests**

Run:
```bash
pytest tests/strategies_external/test_data_loader.py -v
```

Expected: 12 passed

- [ ] **Step 5: Commit**

```bash
git add src/strategies_external/data_loader.py tests/strategies_external/test_data_loader.py
git commit -m "feat(strategies_external): best_tracking_tf with M1>M5>M15 fallback"
```

---

## Task 6: `Signal` dataclass

**Files:**
- Create: `src/strategies_external/common/signal.py`
- Create: `tests/strategies_external/test_signal.py`

- [ ] **Step 1: Escribir el test failing**

```python
# tests/strategies_external/test_signal.py
from datetime import datetime

import pytest

from src.strategies_external.common.signal import Signal


def test_signal_minimal_long():
    s = Signal(
        symbol="SP500",
        strategy="oops",
        side="long",
        setup_ts=datetime(2024, 1, 5),
        entry_type="stop",
        entry_price=4500.0,
        valid_until=datetime(2024, 1, 5, 23, 59),
        stop=4490.0,
        tp1=4520.0,
        tp2=None,
    )
    assert s.side == "long"
    assert s.tp1_size_pct == 0.5  # default
    assert s.indicator_anchors == {}


def test_signal_with_anchors():
    s = Signal(
        symbol="XAUUSD",
        strategy="sma18",
        side="long",
        setup_ts=datetime(2024, 1, 5),
        entry_type="stop",
        entry_price=2050.0,
        valid_until=datetime(2024, 1, 5, 23, 59),
        stop=2030.0,
        tp1=None,
        tp2=None,
        timestop_bars=20,
        indicator_anchors={"sma18": 2025.0, "atr14": 15.0},
    )
    assert s.indicator_anchors["sma18"] == 2025.0
    assert s.timestop_bars == 20


def test_signal_is_frozen():
    s = Signal(
        symbol="SP500", strategy="oops", side="long",
        setup_ts=datetime(2024, 1, 5), entry_type="stop", entry_price=4500.0,
        valid_until=datetime(2024, 1, 5, 23, 59), stop=4490.0, tp1=None, tp2=None,
    )
    with pytest.raises((AttributeError, TypeError)):
        s.entry_price = 5000.0  # frozen
```

- [ ] **Step 2: Run test failing**

Run:
```bash
pytest tests/strategies_external/test_signal.py -v
```

Expected: ImportError

- [ ] **Step 3: Implementar `Signal`**

```python
# src/strategies_external/common/signal.py
"""Signal: estructura de salida de cada estrategia."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal


@dataclass(frozen=True)
class Signal:
    """Una orden potencial generada por una estrategia.

    El backtester resuelve su fill y exit; los ExitManagers pueden modificar
    stop/tp1/tp2 a partir de los indicator_anchors antes de pasar al backtester.
    """

    symbol: str
    strategy: str
    side: Literal["long", "short"]
    setup_ts: datetime
    entry_type: Literal["market", "stop", "limit"]
    entry_price: float
    valid_until: datetime
    stop: float
    tp1: float | None
    tp2: float | None
    tp1_size_pct: float = 0.5
    timestop_bars: int | None = None
    indicator_anchors: dict[str, float] = field(default_factory=dict)
```

- [ ] **Step 4: Run tests**

Run:
```bash
pytest tests/strategies_external/test_signal.py -v
```

Expected: 3 passed

- [ ] **Step 5: Commit**

```bash
git add src/strategies_external/common/signal.py tests/strategies_external/test_signal.py
git commit -m "feat(strategies_external): Signal dataclass"
```

---

## Task 7: `Trade` dataclass

**Files:**
- Create: `src/strategies_external/common/trade.py`
- Create: `tests/strategies_external/test_trade.py`

- [ ] **Step 1: Test failing**

```python
# tests/strategies_external/test_trade.py
from datetime import datetime

import pytest

from src.strategies_external.common.trade import Trade


def test_trade_minimal():
    t = Trade(
        symbol="SP500", strategy="oops", exit_mode="doc", side="long",
        entry_ts=datetime(2024, 1, 5, 9), entry=4500.0, stop=4490.0,
        tp1=4520.0, tp2=None,
        exit_ts=datetime(2024, 1, 5, 16), exit=4520.0,
        exit_reason="tp1", R=10.0, pnl_R=2.0, pnl_pct=0.01, bars_in_trade=420,
    )
    assert t.pnl_R == 2.0
    assert t.exit_reason == "tp1"


def test_trade_is_frozen():
    t = Trade(
        symbol="SP500", strategy="oops", exit_mode="doc", side="long",
        entry_ts=datetime(2024, 1, 5, 9), entry=4500.0, stop=4490.0,
        tp1=None, tp2=None,
        exit_ts=datetime(2024, 1, 5, 16), exit=4500.0,
        exit_reason="eod", R=10.0, pnl_R=0.0, pnl_pct=0.0, bars_in_trade=420,
    )
    with pytest.raises((AttributeError, TypeError)):
        t.pnl_R = 5.0
```

- [ ] **Step 2: Run failing**

```bash
pytest tests/strategies_external/test_trade.py -v
```

Expected: ImportError

- [ ] **Step 3: Implementar Trade**

```python
# src/strategies_external/common/trade.py
"""Trade: resultado de un Signal ejecutado por el backtester."""

from dataclasses import dataclass
from datetime import datetime
from typing import Literal


ExitReason = Literal["tp1", "tp2", "stop", "timestop", "signal_inverso", "eod"]


@dataclass(frozen=True)
class Trade:
    """Trade cerrado, después de friction y slippage."""

    symbol: str
    strategy: str
    exit_mode: Literal["doc", "atr", "indicator"]
    side: Literal["long", "short"]
    entry_ts: datetime
    entry: float
    stop: float
    tp1: float | None
    tp2: float | None
    exit_ts: datetime
    exit: float
    exit_reason: ExitReason
    R: float
    pnl_R: float
    pnl_pct: float
    bars_in_trade: int
```

- [ ] **Step 4: Run pass**

```bash
pytest tests/strategies_external/test_trade.py -v
```

Expected: 2 passed

- [ ] **Step 5: Commit**

```bash
git add src/strategies_external/common/trade.py tests/strategies_external/test_trade.py
git commit -m "feat(strategies_external): Trade dataclass"
```

---

## Task 8: ExitManager ABC + DocExitManager para OOPS

**Files:**
- Create: `src/strategies_external/exit_managers.py`
- Create: `tests/strategies_external/test_exit_managers.py`

- [ ] **Step 1: Tests failing**

```python
# tests/strategies_external/test_exit_managers.py
from datetime import datetime

import pytest

from src.strategies_external.common.signal import Signal
from src.strategies_external.exit_managers import (
    ATRExitManager,
    DocExitManager,
    IndicatorExitManager,
)


def _signal_long_oops_raw() -> Signal:
    """Signal OOPS long sin stop/tp todavía (los pone el ExitManager)."""
    return Signal(
        symbol="SP500", strategy="oops", side="long",
        setup_ts=datetime(2024, 1, 5),
        entry_type="stop", entry_price=4500.0,
        valid_until=datetime(2024, 1, 5, 23, 59),
        stop=0.0, tp1=None, tp2=None,
        indicator_anchors={"prev_high": 4540.0, "prev_low": 4500.0,
                           "prev_range": 40.0, "today_open": 4480.0,
                           "atr14": 50.0, "today_low": 4470.0},
    )


def test_doc_exit_manager_oops_long():
    raw = _signal_long_oops_raw()
    mgr = DocExitManager(strategy="oops")
    s = mgr.attach_levels(raw)
    # Doc OOPS long: stop = today_low, tp = entry + 2R, eod fallback
    assert s.stop == pytest.approx(4470.0)
    R = 4500.0 - 4470.0
    assert s.tp1 == pytest.approx(4500.0 + 2 * R)
    assert s.timestop_bars is None  # eod handled by backtester via valid_until


def test_atr_exit_manager_oops_long():
    raw = _signal_long_oops_raw()
    mgr = ATRExitManager(sl_mult=1.5, tp1_mult=1.5, tp2_mult=3.0)
    s = mgr.attach_levels(raw)
    atr = 50.0
    assert s.stop == pytest.approx(4500.0 - 1.5 * atr)
    assert s.tp1 == pytest.approx(4500.0 + 1.5 * atr)
    assert s.tp2 == pytest.approx(4500.0 + 3.0 * atr)


def test_indicator_exit_manager_oops_long():
    raw = _signal_long_oops_raw()
    mgr = IndicatorExitManager(strategy="oops")
    s = mgr.attach_levels(raw)
    # Indicator OOPS long: stop = today_low (mismo doc), tp1 = mid prev_range, tp2 = prev_close + prev_range
    assert s.stop == pytest.approx(4470.0)
    # mid del rango previo respecto al precio de entrada: prev_low + prev_range/2 = 4520
    assert s.tp1 == pytest.approx(4520.0)
    # prev_high + prev_range = 4540 + 40 = 4580
    assert s.tp2 == pytest.approx(4580.0)


def test_exit_manager_unknown_strategy_raises():
    raw = _signal_long_oops_raw()
    with pytest.raises(ValueError, match="unknown strategy"):
        DocExitManager(strategy="not_a_strategy").attach_levels(raw)
```

- [ ] **Step 2: Run failing**

```bash
pytest tests/strategies_external/test_exit_managers.py -v
```

Expected: ImportError

- [ ] **Step 3: Implementar ExitManagers**

```python
# src/strategies_external/exit_managers.py
"""ExitManagers: tres modos de calcular stop/tp1/tp2 para una señal raw.

- DocExitManager: reglas tal cual del documento por estrategia.
- ATRExitManager: multipliers de ATR (uniforme).
- IndicatorExitManager: anclas estructurales por estrategia.
"""

from abc import ABC, abstractmethod
from dataclasses import replace
from typing import ClassVar, Literal

from src.strategies_external.common.signal import Signal


_KNOWN_STRATEGIES = frozenset({"oops", "sma18", "double_bottom", "perdices_fib", "cot1"})


class ExitManager(ABC):
    name: ClassVar[Literal["doc", "atr", "indicator"]]

    @abstractmethod
    def attach_levels(self, signal_raw: Signal) -> Signal:
        """Devuelve una nueva Signal con stop/tp1/tp2 calculados."""


def _require_anchor(signal: Signal, key: str) -> float:
    if key not in signal.indicator_anchors:
        raise ValueError(
            f"strategy={signal.strategy} side={signal.side} requires anchor '{key}' "
            f"but only {sorted(signal.indicator_anchors)} are present"
        )
    return signal.indicator_anchors[key]


class DocExitManager(ExitManager):
    """Reglas de salida copiadas del documento fuente."""

    name = "doc"

    def __init__(self, strategy: str):
        if strategy not in _KNOWN_STRATEGIES:
            raise ValueError(f"unknown strategy: {strategy}")
        self.strategy = strategy

    def attach_levels(self, signal_raw: Signal) -> Signal:
        if self.strategy == "oops":
            return self._oops(signal_raw)
        # Otras estrategias: implementadas en Plan 2.
        raise ValueError(f"unknown strategy: {self.strategy}")

    def _oops(self, s: Signal) -> Signal:
        if s.side == "long":
            stop = _require_anchor(s, "today_low")
            R = s.entry_price - stop
            tp1 = s.entry_price + 2 * R
        else:
            stop = _require_anchor(s, "today_high")
            R = stop - s.entry_price
            tp1 = s.entry_price - 2 * R
        return replace(s, stop=stop, tp1=tp1, tp2=None)


class ATRExitManager(ExitManager):
    """Stops/TPs uniformes como múltiplos de ATR."""

    name = "atr"

    def __init__(self, sl_mult: float, tp1_mult: float, tp2_mult: float | None):
        if tp2_mult is not None and tp2_mult <= tp1_mult:
            raise ValueError("tp2_mult must be > tp1_mult")
        self.sl_mult = sl_mult
        self.tp1_mult = tp1_mult
        self.tp2_mult = tp2_mult

    def attach_levels(self, signal_raw: Signal) -> Signal:
        atr = _require_anchor(signal_raw, "atr14")
        if signal_raw.side == "long":
            stop = signal_raw.entry_price - self.sl_mult * atr
            tp1 = signal_raw.entry_price + self.tp1_mult * atr
            tp2 = signal_raw.entry_price + self.tp2_mult * atr if self.tp2_mult else None
        else:
            stop = signal_raw.entry_price + self.sl_mult * atr
            tp1 = signal_raw.entry_price - self.tp1_mult * atr
            tp2 = signal_raw.entry_price - self.tp2_mult * atr if self.tp2_mult else None
        return replace(signal_raw, stop=stop, tp1=tp1, tp2=tp2)


class IndicatorExitManager(ExitManager):
    """Stops/TPs anclados a indicadores estructurales por estrategia."""

    name = "indicator"

    def __init__(self, strategy: str):
        if strategy not in _KNOWN_STRATEGIES:
            raise ValueError(f"unknown strategy: {strategy}")
        self.strategy = strategy

    def attach_levels(self, signal_raw: Signal) -> Signal:
        if self.strategy == "oops":
            return self._oops(signal_raw)
        raise ValueError(f"unknown strategy: {self.strategy}")

    def _oops(self, s: Signal) -> Signal:
        prev_high = _require_anchor(s, "prev_high")
        prev_low = _require_anchor(s, "prev_low")
        prev_range = _require_anchor(s, "prev_range")
        if s.side == "long":
            stop = _require_anchor(s, "today_low")
            tp1 = prev_low + prev_range / 2.0
            tp2 = prev_high + prev_range
        else:
            stop = _require_anchor(s, "today_high")
            tp1 = prev_high - prev_range / 2.0
            tp2 = prev_low - prev_range
        return replace(s, stop=stop, tp1=tp1, tp2=tp2)
```

- [ ] **Step 4: Run pass**

```bash
pytest tests/strategies_external/test_exit_managers.py -v
```

Expected: 4 passed

- [ ] **Step 5: Commit**

```bash
git add src/strategies_external/exit_managers.py tests/strategies_external/test_exit_managers.py
git commit -m "feat(strategies_external): ExitManager ABC + Doc/ATR/Indicator for OOPS"
```

---

## Task 9: Backtester — fill + intra-bar exit

**Files:**
- Create: `src/strategies_external/common/backtester.py`
- Create: `tests/strategies_external/test_backtester.py`

- [ ] **Step 1: Tests del backtester**

```python
# tests/strategies_external/test_backtester.py
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
    # PnL bruto = (100.6 - 100.5) / 1.0 = 0.1R, neto -0.1R
    assert trades[0].pnl_R == pytest.approx(-0.1, abs=0.05)
```

- [ ] **Step 2: Run failing**

```bash
pytest tests/strategies_external/test_backtester.py -v
```

Expected: ImportError

- [ ] **Step 3: Implementar backtester**

```python
# src/strategies_external/common/backtester.py
"""Backtester genérico: signal → fill → intra-bar tracking → Trade."""

from typing import Literal

import polars as pl

from src.strategies_external.common.signal import Signal
from src.strategies_external.common.trade import Trade
from src.strategies_external.constants import friction_for


ExitMode = Literal["doc", "atr", "indicator"]


def _filter_window(df: pl.DataFrame, signal: Signal) -> pl.DataFrame:
    """Barras del tracking_tf relevantes para la señal."""
    return df.filter(
        (pl.col("time") > signal.setup_ts) & (pl.col("time") <= signal.valid_until)
    ).sort("time")


def _fill_condition(side: str, entry_type: str, price: float,
                    bar_open: float, bar_high: float, bar_low: float) -> bool:
    """¿La barra llena la orden?"""
    if entry_type == "market":
        return True
    if entry_type == "stop":
        if side == "long":
            return bar_high >= price
        return bar_low <= price
    if entry_type == "limit":
        if side == "long":
            return bar_low <= price
        return bar_high >= price
    raise ValueError(f"unknown entry_type: {entry_type}")


def run_backtest(
    signals: list[Signal],
    tracking_df: pl.DataFrame,
    exit_mode: ExitMode,
) -> list[Trade]:
    """Ejecuta cada señal contra el DataFrame de tracking_tf.

    Resolución conservadora intra-bar: si una barra toca stop y tp en la
    misma vela, gana stop (worst case).
    """
    trades: list[Trade] = []
    for sig in signals:
        bars = _filter_window(tracking_df, sig)
        if bars.is_empty():
            continue

        rows = bars.to_dicts()
        filled = False
        entry_price = sig.entry_price
        entry_ts = sig.setup_ts
        first_idx = 0

        # Busca fill
        for i, bar in enumerate(rows):
            if _fill_condition(sig.side, sig.entry_type,
                               sig.entry_price, bar["open"], bar["high"], bar["low"]):
                filled = True
                entry_ts = bar["time"]
                # Slippage: 1 tick adverso. Usamos 0.05 como proxy genérico
                # para índices/commodities; FX se maneja con pip-equiv abajo.
                slip = 0.05 if sig.symbol not in {"EURUSD", "GBPUSD", "USDJPY",
                                                   "AUDUSD", "EURJPY", "GBPAUD",
                                                   "GBPJPY"} else 0.00005
                entry_price = sig.entry_price + slip if sig.side == "long" else sig.entry_price - slip
                first_idx = i
                break

        if not filled:
            continue

        R = abs(entry_price - sig.stop)
        if R == 0:
            continue

        exit_reason = None
        exit_price = None
        exit_ts = None
        bars_in_trade = 0

        # Tracking intra-bar
        for j in range(first_idx, len(rows)):
            bar = rows[j]
            bars_in_trade = j - first_idx + 1
            high = bar["high"]
            low = bar["low"]
            close = bar["close"]

            if sig.side == "long":
                touches_stop = low <= sig.stop
                touches_tp1 = sig.tp1 is not None and high >= sig.tp1
                touches_tp2 = sig.tp2 is not None and high >= sig.tp2
                if touches_stop:
                    exit_reason = "stop"; exit_price = sig.stop; exit_ts = bar["time"]; break
                if touches_tp2:
                    exit_reason = "tp2"; exit_price = sig.tp2; exit_ts = bar["time"]; break
                if touches_tp1:
                    exit_reason = "tp1"; exit_price = sig.tp1; exit_ts = bar["time"]; break
            else:
                touches_stop = high >= sig.stop
                touches_tp1 = sig.tp1 is not None and low <= sig.tp1
                touches_tp2 = sig.tp2 is not None and low <= sig.tp2
                if touches_stop:
                    exit_reason = "stop"; exit_price = sig.stop; exit_ts = bar["time"]; break
                if touches_tp2:
                    exit_reason = "tp2"; exit_price = sig.tp2; exit_ts = bar["time"]; break
                if touches_tp1:
                    exit_reason = "tp1"; exit_price = sig.tp1; exit_ts = bar["time"]; break

            if sig.timestop_bars is not None and bars_in_trade >= sig.timestop_bars:
                exit_reason = "timestop"; exit_price = close; exit_ts = bar["time"]; break

        if exit_reason is None:
            # Cierre por valid_until (eod): tomamos close de la última barra
            last_bar = rows[-1]
            exit_reason = "eod"; exit_price = last_bar["close"]; exit_ts = last_bar["time"]

        # PnL bruto en R
        if sig.side == "long":
            pnl_gross_R = (exit_price - entry_price) / R
        else:
            pnl_gross_R = (entry_price - exit_price) / R

        pnl_net_R = pnl_gross_R - friction_for(sig.symbol)

        # pnl_pct con risk 0.5%
        from src.strategies_external.constants import RISK_PER_TRADE_PCT_DEFAULT
        pnl_pct = pnl_net_R * RISK_PER_TRADE_PCT_DEFAULT

        trades.append(Trade(
            symbol=sig.symbol,
            strategy=sig.strategy,
            exit_mode=exit_mode,
            side=sig.side,
            entry_ts=entry_ts,
            entry=entry_price,
            stop=sig.stop,
            tp1=sig.tp1,
            tp2=sig.tp2,
            exit_ts=exit_ts,
            exit=exit_price,
            exit_reason=exit_reason,
            R=R,
            pnl_R=pnl_net_R,
            pnl_pct=pnl_pct,
            bars_in_trade=bars_in_trade,
        ))

    return trades
```

- [ ] **Step 4: Run pass**

```bash
pytest tests/strategies_external/test_backtester.py -v
```

Expected: 4 passed

- [ ] **Step 5: Commit**

```bash
git add src/strategies_external/common/backtester.py tests/strategies_external/test_backtester.py
git commit -m "feat(strategies_external): backtester with intra-bar conservative resolution"
```

---

## Task 10: Metrics — `evaluate(trades)`

**Files:**
- Create: `src/strategies_external/common/metrics.py`
- Create: `tests/strategies_external/test_metrics.py`

- [ ] **Step 1: Tests**

```python
# tests/strategies_external/test_metrics.py
from datetime import datetime, timedelta

import pytest

from src.strategies_external.common.metrics import evaluate
from src.strategies_external.common.trade import Trade


def _make(pnl_R: float, ts: datetime, R: float = 10.0) -> Trade:
    return Trade(
        symbol="SP500", strategy="oops", exit_mode="doc", side="long",
        entry_ts=ts, entry=100.0, stop=99.0, tp1=None, tp2=None,
        exit_ts=ts + timedelta(hours=1), exit=100.0 + pnl_R,
        exit_reason="tp1" if pnl_R > 0 else "stop",
        R=R, pnl_R=pnl_R, pnl_pct=pnl_R * 0.005, bars_in_trade=4,
    )


def test_evaluate_empty_returns_zeros():
    m = evaluate([])
    assert m["n_trades"] == 0
    assert m["win_rate"] == 0.0
    assert m["profit_factor"] == 0.0
    assert m["expectancy_R"] == 0.0


def test_evaluate_simple_2_wins_1_loss():
    base = datetime(2024, 1, 1)
    trades = [
        _make(2.0, base),
        _make(2.0, base + timedelta(days=1)),
        _make(-1.0, base + timedelta(days=2)),
    ]
    m = evaluate(trades)
    assert m["n_trades"] == 3
    assert m["win_rate"] == pytest.approx(2 / 3)
    assert m["profit_factor"] == pytest.approx(4.0)  # 4 / 1
    assert m["expectancy_R"] == pytest.approx(1.0)   # (4-1)/3 = 1


def test_evaluate_max_dd_R():
    base = datetime(2024, 1, 1)
    trades = [
        _make(2.0, base),
        _make(-1.0, base + timedelta(days=1)),
        _make(-1.0, base + timedelta(days=2)),
        _make(-1.0, base + timedelta(days=3)),  # equity: 2, 1, 0, -1 → DD = 3R
        _make(3.0, base + timedelta(days=4)),
    ]
    m = evaluate(trades)
    assert m["max_dd_R"] == pytest.approx(3.0)


def test_evaluate_sharpe_when_zero_std():
    base = datetime(2024, 1, 1)
    trades = [_make(1.0, base + timedelta(days=i)) for i in range(5)]
    m = evaluate(trades)
    # std = 0 → sharpe convention: 0
    assert m["sharpe"] == 0.0
```

- [ ] **Step 2: Run failing**

```bash
pytest tests/strategies_external/test_metrics.py -v
```

Expected: ImportError

- [ ] **Step 3: Implementar**

```python
# src/strategies_external/common/metrics.py
"""Métricas estándar para evaluar listas de Trade."""

import math

from src.strategies_external.common.trade import Trade


def evaluate(trades: list[Trade]) -> dict[str, float]:
    if not trades:
        return {
            "n_trades": 0, "win_rate": 0.0, "profit_factor": 0.0,
            "expectancy_R": 0.0, "avg_win_R": 0.0, "avg_loss_R": 0.0,
            "max_dd_R": 0.0, "max_dd_pct": 0.0, "sharpe": 0.0,
            "sortino": 0.0, "calmar": 0.0, "total_R": 0.0,
        }

    sorted_trades = sorted(trades, key=lambda t: t.entry_ts)
    pnl_Rs = [t.pnl_R for t in sorted_trades]
    n = len(pnl_Rs)
    wins = [r for r in pnl_Rs if r > 0]
    losses = [r for r in pnl_Rs if r <= 0]
    win_rate = len(wins) / n
    sum_wins = sum(wins)
    sum_losses_abs = abs(sum(losses))
    profit_factor = (sum_wins / sum_losses_abs) if sum_losses_abs > 0 else float("inf")
    expectancy = sum(pnl_Rs) / n
    avg_win = (sum_wins / len(wins)) if wins else 0.0
    avg_loss = (sum(losses) / len(losses)) if losses else 0.0

    # Drawdown sobre equity acumulado (en R)
    equity = []
    cum = 0.0
    for r in pnl_Rs:
        cum += r
        equity.append(cum)
    peak = equity[0]
    max_dd = 0.0
    for v in equity:
        peak = max(peak, v)
        dd = peak - v
        if dd > max_dd:
            max_dd = dd

    pnl_pcts = [t.pnl_pct for t in sorted_trades]
    cum_pct = 0.0
    peak_pct = 0.0
    max_dd_pct = 0.0
    for r in pnl_pcts:
        cum_pct += r
        peak_pct = max(peak_pct, cum_pct)
        max_dd_pct = max(max_dd_pct, peak_pct - cum_pct)

    # Sharpe / Sortino: convención simple, mean / std de pnl_R; rf=0.
    mean_r = sum(pnl_Rs) / n
    var = sum((r - mean_r) ** 2 for r in pnl_Rs) / n
    std = math.sqrt(var)
    sharpe = (mean_r / std) if std > 0 else 0.0

    downside = [min(0.0, r - mean_r) for r in pnl_Rs]
    down_var = sum(d ** 2 for d in downside) / n
    down_std = math.sqrt(down_var)
    sortino = (mean_r / down_std) if down_std > 0 else 0.0

    total_R = sum(pnl_Rs)
    calmar = (total_R / max_dd) if max_dd > 0 else 0.0

    return {
        "n_trades": n,
        "win_rate": win_rate,
        "profit_factor": profit_factor,
        "expectancy_R": expectancy,
        "avg_win_R": avg_win,
        "avg_loss_R": avg_loss,
        "max_dd_R": max_dd,
        "max_dd_pct": max_dd_pct,
        "sharpe": sharpe,
        "sortino": sortino,
        "calmar": calmar,
        "total_R": total_R,
    }
```

- [ ] **Step 4: Run pass**

```bash
pytest tests/strategies_external/test_metrics.py -v
```

Expected: 4 passed

- [ ] **Step 5: Commit**

```bash
git add src/strategies_external/common/metrics.py tests/strategies_external/test_metrics.py
git commit -m "feat(strategies_external): metrics evaluate(trades)"
```

---

## Task 11: Walk-forward — 5 ventanas 70/30

**Files:**
- Create: `src/strategies_external/common/walk_forward.py`
- Create: `tests/strategies_external/test_walk_forward.py`

- [ ] **Step 1: Tests**

```python
# tests/strategies_external/test_walk_forward.py
from datetime import datetime, timedelta

import pytest

from src.strategies_external.common.trade import Trade
from src.strategies_external.common.walk_forward import walk_forward_split


def _trade(day: int, pnl_R: float) -> Trade:
    base = datetime(2024, 1, 1)
    return Trade(
        symbol="SP500", strategy="oops", exit_mode="doc", side="long",
        entry_ts=base + timedelta(days=day), entry=100.0, stop=99.0,
        tp1=None, tp2=None,
        exit_ts=base + timedelta(days=day, hours=1), exit=100.0 + pnl_R,
        exit_reason="tp1" if pnl_R > 0 else "stop",
        R=10.0, pnl_R=pnl_R, pnl_pct=pnl_R * 0.005, bars_in_trade=4,
    )


def test_walk_forward_5_windows_70_30():
    trades = [_trade(i, (1.0 if i % 2 == 0 else -1.0)) for i in range(100)]
    windows = walk_forward_split(trades, n_windows=5, is_pct=0.7)
    assert len(windows) == 5
    for w in windows:
        is_, oos = w
        # cada ventana = 20 trades; IS=14, OOS=6
        assert len(is_) == 14
        assert len(oos) == 6
    # Las ventanas no se solapan
    all_is = [t.entry_ts for w in windows for t in w[0]]
    assert len(all_is) == len(set(all_is))


def test_walk_forward_too_few_trades():
    trades = [_trade(i, 1.0) for i in range(3)]
    with pytest.raises(ValueError, match="too few trades"):
        walk_forward_split(trades, n_windows=5, is_pct=0.7)
```

- [ ] **Step 2: Run failing**

```bash
pytest tests/strategies_external/test_walk_forward.py -v
```

Expected: ImportError

- [ ] **Step 3: Implementar**

```python
# src/strategies_external/common/walk_forward.py
"""Walk-forward split: divide trades en N ventanas con split IS/OOS."""

from src.strategies_external.common.trade import Trade


def walk_forward_split(
    trades: list[Trade], n_windows: int = 5, is_pct: float = 0.7
) -> list[tuple[list[Trade], list[Trade]]]:
    """Particiona trades cronológicamente en ventanas no solapadas.

    Args:
        trades: lista de Trade.
        n_windows: número de ventanas.
        is_pct: fracción de cada ventana usada como in-sample (resto OOS).

    Returns:
        Lista de tuplas (in_sample, out_of_sample) para cada ventana.
    """
    if not (0.0 < is_pct < 1.0):
        raise ValueError("is_pct must be in (0, 1)")
    sorted_trades = sorted(trades, key=lambda t: t.entry_ts)
    n = len(sorted_trades)
    if n < n_windows * 2:
        raise ValueError(f"too few trades ({n}) for {n_windows} windows")

    window_size = n // n_windows
    is_size = int(window_size * is_pct)
    windows = []
    for w in range(n_windows):
        start = w * window_size
        end = start + window_size if w < n_windows - 1 else n
        chunk = sorted_trades[start:end]
        is_chunk = chunk[:is_size]
        oos_chunk = chunk[is_size:is_size + (window_size - is_size)]
        windows.append((is_chunk, oos_chunk))
    return windows
```

- [ ] **Step 4: Run pass**

```bash
pytest tests/strategies_external/test_walk_forward.py -v
```

Expected: 2 passed

- [ ] **Step 5: Commit**

```bash
git add src/strategies_external/common/walk_forward.py tests/strategies_external/test_walk_forward.py
git commit -m "feat(strategies_external): walk_forward_split"
```

---

## Task 12: Monte Carlo — bootstrap

**Files:**
- Create: `src/strategies_external/common/monte_carlo.py`
- Create: `tests/strategies_external/test_monte_carlo.py`

- [ ] **Step 1: Tests**

```python
# tests/strategies_external/test_monte_carlo.py
from datetime import datetime, timedelta

import pytest

from src.strategies_external.common.monte_carlo import monte_carlo_bootstrap
from src.strategies_external.common.trade import Trade


def _make(pnl_R: float, day: int) -> Trade:
    base = datetime(2024, 1, 1)
    return Trade(
        symbol="SP500", strategy="oops", exit_mode="doc", side="long",
        entry_ts=base + timedelta(days=day), entry=100.0, stop=99.0,
        tp1=None, tp2=None,
        exit_ts=base + timedelta(days=day, hours=1), exit=100.0 + pnl_R,
        exit_reason="tp1" if pnl_R > 0 else "stop",
        R=10.0, pnl_R=pnl_R, pnl_pct=pnl_R * 0.005, bars_in_trade=4,
    )


def test_monte_carlo_winning_system_low_ruin():
    """Sistema con expectancy positiva → prob_ruin baja."""
    trades = [_make(2.0 if i % 3 != 0 else -1.0, i) for i in range(60)]
    res = monte_carlo_bootstrap(trades, n_simulations=2000, ruin_threshold_R=-15.0, seed=42)
    assert res["prob_ruin"] < 0.05
    assert res["dd_q50_R"] < res["dd_q95_R"]


def test_monte_carlo_losing_system_high_ruin():
    """Sistema perdedor → prob_ruin alta."""
    trades = [_make(-1.0 if i % 3 != 0 else 0.5, i) for i in range(60)]
    res = monte_carlo_bootstrap(trades, n_simulations=2000, ruin_threshold_R=-15.0, seed=42)
    assert res["prob_ruin"] > 0.5


def test_monte_carlo_empty_trades():
    with pytest.raises(ValueError, match="empty trade list"):
        monte_carlo_bootstrap([], n_simulations=100, ruin_threshold_R=-15.0)
```

- [ ] **Step 2: Run failing**

```bash
pytest tests/strategies_external/test_monte_carlo.py -v
```

Expected: ImportError

- [ ] **Step 3: Implementar**

```python
# src/strategies_external/common/monte_carlo.py
"""Bootstrap Monte Carlo de listas de trades."""

import random

from src.strategies_external.common.trade import Trade


def monte_carlo_bootstrap(
    trades: list[Trade],
    n_simulations: int = 10_000,
    ruin_threshold_R: float = -15.0,
    seed: int | None = None,
) -> dict[str, float]:
    """Re-ordena trades aleatoriamente N veces; calcula prob_ruin y DD quantiles.

    `prob_ruin` = fracción de simulaciones cuyo equity (en R) tocó ruin_threshold_R.
    """
    if not trades:
        raise ValueError("empty trade list")

    rng = random.Random(seed)
    pnl_Rs = [t.pnl_R for t in trades]
    n = len(pnl_Rs)

    ruin_count = 0
    dds: list[float] = []
    finals: list[float] = []

    for _ in range(n_simulations):
        permuted = rng.sample(pnl_Rs, n)
        cum = 0.0
        peak = 0.0
        max_dd = 0.0
        ruined = False
        for r in permuted:
            cum += r
            if cum <= ruin_threshold_R:
                ruined = True
            peak = max(peak, cum)
            max_dd = max(max_dd, peak - cum)
        if ruined:
            ruin_count += 1
        dds.append(max_dd)
        finals.append(cum)

    dds.sort(); finals.sort()

    def q(arr: list[float], pct: float) -> float:
        idx = int(pct * (len(arr) - 1))
        return arr[idx]

    return {
        "prob_ruin": ruin_count / n_simulations,
        "dd_q5_R": q(dds, 0.05),
        "dd_q50_R": q(dds, 0.50),
        "dd_q95_R": q(dds, 0.95),
        "final_q5_R": q(finals, 0.05),
        "final_q50_R": q(finals, 0.50),
        "final_q95_R": q(finals, 0.95),
        "n_simulations": n_simulations,
    }
```

- [ ] **Step 4: Run pass**

```bash
pytest tests/strategies_external/test_monte_carlo.py -v
```

Expected: 3 passed

- [ ] **Step 5: Commit**

```bash
git add src/strategies_external/common/monte_carlo.py tests/strategies_external/test_monte_carlo.py
git commit -m "feat(strategies_external): monte carlo bootstrap"
```

---

## Task 13: Strategy ABC

**Files:**
- Create: `src/strategies_external/strategies/base.py`

- [ ] **Step 1: Implementar (no necesita tests propios; será cubierto por OOPS)**

```python
# src/strategies_external/strategies/base.py
"""Strategy ABC: contrato común de las estrategias."""

from abc import ABC, abstractmethod

import polars as pl

from src.strategies_external.common.signal import Signal


class Strategy(ABC):
    """Una estrategia produce señales raw (sin stop/tp; eso lo pone el ExitManager)."""

    name: str

    @abstractmethod
    def generate_signals(self, df: pl.DataFrame, symbol: str) -> list[Signal]:
        """df: barras del TF de señal (típicamente daily). symbol: ticker."""
```

- [ ] **Step 2: Commit**

```bash
git add src/strategies_external/strategies/base.py
git commit -m "feat(strategies_external): Strategy ABC"
```

---

## Task 14: OOPS strategy — `generate_signals`

**Files:**
- Create: `src/strategies_external/strategies/oops.py`
- Create: `tests/strategies_external/test_oops_strategy.py`

- [ ] **Step 1: Tests con fixtures daily_oops_long/short**

```python
# tests/strategies_external/test_oops_strategy.py
import pytest

from src.strategies_external.strategies.oops import OOPSStrategy


def test_oops_long_signal_detected(df_daily_oops_long):
    strat = OOPSStrategy()
    signals = strat.generate_signals(df_daily_oops_long, symbol="SP500")
    # En el fixture, el día 4 dispara (open=104 < prev_low=105 ∧ high=109 > prev_low=105)
    assert len(signals) == 1
    s = signals[0]
    assert s.side == "long"
    assert s.entry_price == pytest.approx(105.0)  # prev_low
    assert s.entry_type == "stop"
    # anchors poblados
    for k in ("prev_high", "prev_low", "prev_range", "today_open", "atr14",
             "today_low", "today_high"):
        assert k in s.indicator_anchors


def test_oops_short_signal_detected(df_daily_oops_short):
    strat = OOPSStrategy()
    signals = strat.generate_signals(df_daily_oops_short, symbol="SP500")
    assert len(signals) == 1
    s = signals[0]
    assert s.side == "short"
    assert s.entry_price == pytest.approx(110.0)  # prev_high


def test_oops_no_signal_when_no_gap(df_h1_two_days):
    """Sin gaps no hay señales."""
    from src.strategies_external.data_loader import aggregate_to_daily
    daily = aggregate_to_daily(df_h1_two_days)
    strat = OOPSStrategy()
    sigs = strat.generate_signals(daily, symbol="EURUSD")
    assert sigs == []
```

- [ ] **Step 2: Run failing**

```bash
pytest tests/strategies_external/test_oops_strategy.py -v
```

Expected: ImportError

- [ ] **Step 3: Implementar OOPS**

```python
# src/strategies_external/strategies/oops.py
"""OOPS — Larry Williams gap-reversal pattern.

Long: open[t] < low[t-1] AND high[t] > low[t-1] → buy stop @ low[t-1] + 1 tick.
Short: open[t] > high[t-1] AND low[t] < high[t-1] → sell stop @ high[t-1] - 1 tick.

Tick assumption: 0.01 (índices y commodities en CFDs Vantage). El backtester
aplica slippage adicional según asset class.
"""

from datetime import time, timedelta

import polars as pl

from src.strategies_external.common.signal import Signal
from src.strategies_external.strategies.base import Strategy


_TICK = 0.01


class OOPSStrategy(Strategy):
    name = "oops"

    def __init__(self, atr_window: int = 14):
        self.atr_window = atr_window

    def generate_signals(self, df: pl.DataFrame, symbol: str) -> list[Signal]:
        if df.is_empty() or df.shape[0] < self.atr_window + 2:
            return []

        # ATR(14) sobre daily
        atr_df = (
            df.with_columns(
                pl.max_horizontal(
                    pl.col("high") - pl.col("low"),
                    (pl.col("high") - pl.col("close").shift(1)).abs(),
                    (pl.col("low") - pl.col("close").shift(1)).abs(),
                ).alias("tr")
            )
            .with_columns(pl.col("tr").rolling_mean(self.atr_window).alias("atr"))
        )

        rows = atr_df.to_dicts()
        signals: list[Signal] = []

        for i in range(1, len(rows)):
            prev = rows[i - 1]
            cur = rows[i]
            prev_high = prev["high"]
            prev_low = prev["low"]
            prev_range = prev_high - prev_low
            atr = cur.get("atr") or 0.0
            today_ts = cur["time"]
            valid_until = today_ts + timedelta(days=1) - timedelta(seconds=1)

            anchors = {
                "prev_high": prev_high, "prev_low": prev_low,
                "prev_range": prev_range, "prev_close": prev["close"],
                "today_open": cur["open"], "today_high": cur["high"],
                "today_low": cur["low"], "atr14": atr,
            }

            # Long
            if cur["open"] < prev_low and cur["high"] > prev_low:
                signals.append(Signal(
                    symbol=symbol, strategy=self.name, side="long",
                    setup_ts=today_ts, entry_type="stop",
                    entry_price=prev_low + _TICK,
                    valid_until=valid_until,
                    stop=0.0, tp1=None, tp2=None,
                    indicator_anchors=anchors,
                ))
            # Short
            elif cur["open"] > prev_high and cur["low"] < prev_high:
                signals.append(Signal(
                    symbol=symbol, strategy=self.name, side="short",
                    setup_ts=today_ts, entry_type="stop",
                    entry_price=prev_high - _TICK,
                    valid_until=valid_until,
                    stop=0.0, tp1=None, tp2=None,
                    indicator_anchors=anchors,
                ))

        return signals
```

- [ ] **Step 4: Run pass**

```bash
pytest tests/strategies_external/test_oops_strategy.py -v
```

Expected: 3 passed

- [ ] **Step 5: Commit**

```bash
git add src/strategies_external/strategies/oops.py src/strategies_external/strategies/__init__.py tests/strategies_external/test_oops_strategy.py
git commit -m "feat(strategies_external): OOPS strategy generate_signals"
```

---

## Task 15: Markdown report writer

**Files:**
- Create: `src/strategies_external/reporting/markdown.py`
- Create: `tests/strategies_external/test_markdown_report.py`

- [ ] **Step 1: Test**

```python
# tests/strategies_external/test_markdown_report.py
from datetime import datetime, timedelta
from pathlib import Path

from src.strategies_external.common.trade import Trade
from src.strategies_external.reporting.markdown import write_backtest_report


def _trade(day: int, pnl_R: float, mode: str = "doc") -> Trade:
    base = datetime(2024, 1, 1)
    return Trade(
        symbol="SP500", strategy="oops", exit_mode=mode, side="long",
        entry_ts=base + timedelta(days=day), entry=100.0, stop=99.0,
        tp1=None, tp2=None,
        exit_ts=base + timedelta(days=day, hours=1), exit=100.0 + pnl_R,
        exit_reason="tp1" if pnl_R > 0 else "stop",
        R=10.0, pnl_R=pnl_R, pnl_pct=pnl_R * 0.005, bars_in_trade=4,
    )


def test_report_includes_metrics_and_modes(tmp_path: Path):
    trades_by_mode = {
        "doc": [_trade(0, 1.0), _trade(1, -1.0), _trade(2, 2.0)],
        "atr": [_trade(0, 0.5, "atr"), _trade(1, 0.5, "atr")],
        "indicator": [_trade(0, 1.5, "indicator")],
    }
    report_path = tmp_path / "oops_backtest.md"
    write_backtest_report(
        report_path,
        strategy_name="oops",
        symbols=["SP500"],
        trades_by_mode=trades_by_mode,
        config={"period": "2018-01-01..2026-03-24", "risk_pct": 0.005},
    )
    content = report_path.read_text()
    assert "# OOPS backtest report" in content
    assert "doc" in content
    assert "atr" in content
    assert "indicator" in content
    assert "win_rate" in content
    assert "SP500" in content
```

- [ ] **Step 2: Run failing**

```bash
pytest tests/strategies_external/test_markdown_report.py -v
```

Expected: ImportError

- [ ] **Step 3: Implementar**

```python
# src/strategies_external/reporting/markdown.py
"""Generador de reportes Markdown para backtests del módulo strategies_external."""

from datetime import datetime
from pathlib import Path

from src.strategies_external.common.metrics import evaluate
from src.strategies_external.common.trade import Trade


_FIELDS = ["n_trades", "win_rate", "profit_factor", "expectancy_R",
           "avg_win_R", "avg_loss_R", "max_dd_R", "sharpe", "sortino",
           "calmar", "total_R"]


def _fmt(v: float) -> str:
    if isinstance(v, int):
        return str(v)
    if v == float("inf"):
        return "∞"
    return f"{v:.3f}"


def write_backtest_report(
    path: Path,
    strategy_name: str,
    symbols: list[str],
    trades_by_mode: dict[str, list[Trade]],
    config: dict,
) -> None:
    """Escribe report Markdown con métricas por modo de exit y por activo."""
    lines: list[str] = []
    lines.append(f"# {strategy_name.upper()} backtest report")
    lines.append("")
    lines.append(f"**Generated:** {datetime.utcnow().isoformat()}Z")
    lines.append(f"**Symbols:** {', '.join(symbols)}")
    lines.append(f"**Period:** {config.get('period', 'n/a')}")
    lines.append(f"**Risk per trade:** {config.get('risk_pct', 0.005) * 100:.2f}%")
    lines.append("")

    # Tabla cruzada modo × métrica
    lines.append("## Comparativa modos de exit")
    lines.append("")
    header = "| metric | " + " | ".join(trades_by_mode.keys()) + " |"
    sep = "|--------|" + "|".join(["--------"] * len(trades_by_mode)) + "|"
    lines.append(header)
    lines.append(sep)
    metrics_by_mode = {m: evaluate(ts) for m, ts in trades_by_mode.items()}
    for f in _FIELDS:
        row = f"| {f} | " + " | ".join(_fmt(metrics_by_mode[m][f]) for m in trades_by_mode) + " |"
        lines.append(row)
    lines.append("")

    # Per-symbol breakdown del modo "doc" como referencia
    lines.append("## Breakdown por activo (modo doc)")
    lines.append("")
    lines.append("| symbol | n | wr | pf | exp_R | dd_R | calmar |")
    lines.append("|--------|---|-----|-----|-------|------|--------|")
    doc_trades = trades_by_mode.get("doc", [])
    for sym in symbols:
        sym_trades = [t for t in doc_trades if t.symbol == sym]
        m = evaluate(sym_trades)
        lines.append(
            f"| {sym} | {m['n_trades']} | {_fmt(m['win_rate'])} | "
            f"{_fmt(m['profit_factor'])} | {_fmt(m['expectancy_R'])} | "
            f"{_fmt(m['max_dd_R'])} | {_fmt(m['calmar'])} |"
        )
    lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
```

- [ ] **Step 4: Run pass**

```bash
pytest tests/strategies_external/test_markdown_report.py -v
```

Expected: 1 passed

- [ ] **Step 5: Commit**

```bash
git add src/strategies_external/reporting/markdown.py src/strategies_external/reporting/__init__.py tests/strategies_external/test_markdown_report.py
git commit -m "feat(strategies_external): markdown backtest report writer"
```

---

## Task 16: Runner — `run_oops`

**Files:**
- Create: `src/strategies_external/runners/run_oops.py`
- Create: `tests/strategies_external/test_run_oops_integration.py`

- [ ] **Step 1: Test integración**

```python
# tests/strategies_external/test_run_oops_integration.py
"""Integración: corre OOPS sobre dataset SP500 real y verifica que produce reporte."""

from pathlib import Path

import pytest

from src.strategies_external.runners.run_oops import run_oops_backtest


@pytest.mark.integration
def test_run_oops_real_data_produces_report(tmp_path: Path):
    output = tmp_path / "oops_backtest.md"
    summary = run_oops_backtest(
        symbols=["SP500", "NASDAQ100"],
        data_dir="data",
        output_path=output,
    )
    assert output.exists()
    content = output.read_text()
    assert "OOPS" in content
    assert "SP500" in content and "NASDAQ100" in content
    # summary debe contener métricas por modo
    assert "doc" in summary
    assert "atr" in summary
    assert "indicator" in summary
    # Trades parquet también
    parquet_path = output.parent / "oops_trades.parquet"
    assert parquet_path.exists()
```

- [ ] **Step 2: Run failing**

```bash
pytest tests/strategies_external/test_run_oops_integration.py -v -m integration
```

Expected: ImportError

- [ ] **Step 3: Implementar runner**

```python
# src/strategies_external/runners/run_oops.py
"""Runner OOPS: ejecuta backtest con 3 modos de exit sobre los símbolos dados,
escribe reporte Markdown y trades en parquet.
"""

from pathlib import Path

import polars as pl

from src.strategies_external.common.backtester import run_backtest
from src.strategies_external.common.metrics import evaluate
from src.strategies_external.common.trade import Trade
from src.strategies_external.data_loader import (
    aggregate_to_daily, best_tracking_tf, load_csv,
)
from src.strategies_external.exit_managers import (
    ATRExitManager, DocExitManager, IndicatorExitManager,
)
from src.strategies_external.reporting.markdown import write_backtest_report
from src.strategies_external.strategies.oops import OOPSStrategy


def _trades_to_parquet(trades: list[Trade], path: Path) -> None:
    if not trades:
        path.touch()
        return
    df = pl.DataFrame([{
        "symbol": t.symbol, "strategy": t.strategy, "exit_mode": t.exit_mode,
        "side": t.side, "entry_ts": t.entry_ts, "entry": t.entry,
        "stop": t.stop, "tp1": t.tp1, "tp2": t.tp2,
        "exit_ts": t.exit_ts, "exit": t.exit, "exit_reason": t.exit_reason,
        "R": t.R, "pnl_R": t.pnl_R, "pnl_pct": t.pnl_pct,
        "bars_in_trade": t.bars_in_trade,
    } for t in trades])
    df.write_parquet(path)


def run_oops_backtest(
    symbols: list[str],
    data_dir: str = "data",
    output_path: Path | str = "reports/external/oops_backtest.md",
    atr_grid: list[tuple[float, float, float]] | None = None,
) -> dict[str, dict]:
    """Corre OOPS sobre los símbolos dados con 3 modos de exit.

    Returns: dict mode → metrics dict.
    """
    if atr_grid is None:
        # Multipliers por defecto del documento (sweep en V2 si hace falta)
        atr_grid = [(1.5, 1.5, 3.0)]

    output_path = Path(output_path)
    strategy = OOPSStrategy()
    doc_mgr = DocExitManager(strategy="oops")
    ind_mgr = IndicatorExitManager(strategy="oops")

    trades_by_mode: dict[str, list[Trade]] = {"doc": [], "atr": [], "indicator": []}

    for sym in symbols:
        df_h1 = load_csv(sym, "H1", data_dir=data_dir)
        df_daily = aggregate_to_daily(df_h1)
        _, df_track = best_tracking_tf(sym, data_dir=data_dir)

        signals_raw = strategy.generate_signals(df_daily, symbol=sym)

        trades_by_mode["doc"].extend(
            run_backtest([doc_mgr.attach_levels(s) for s in signals_raw],
                         df_track, exit_mode="doc")
        )
        # ATR mode (primer punto del grid, V2 hará sweep completo)
        sl, tp1, tp2 = atr_grid[0]
        atr_mgr = ATRExitManager(sl_mult=sl, tp1_mult=tp1, tp2_mult=tp2)
        trades_by_mode["atr"].extend(
            run_backtest([atr_mgr.attach_levels(s) for s in signals_raw],
                         df_track, exit_mode="atr")
        )
        trades_by_mode["indicator"].extend(
            run_backtest([ind_mgr.attach_levels(s) for s in signals_raw],
                         df_track, exit_mode="indicator")
        )

    write_backtest_report(
        output_path,
        strategy_name="oops",
        symbols=symbols,
        trades_by_mode=trades_by_mode,
        config={"period": "2018-01-01..today", "risk_pct": 0.005,
                "atr_grid": atr_grid},
    )

    # Combina trades en un único parquet
    all_trades = trades_by_mode["doc"] + trades_by_mode["atr"] + trades_by_mode["indicator"]
    _trades_to_parquet(all_trades, output_path.parent / "oops_trades.parquet")

    return {m: evaluate(ts) for m, ts in trades_by_mode.items()}


if __name__ == "__main__":
    summary = run_oops_backtest(
        symbols=["SP500", "NASDAQ100"],
        data_dir="data",
        output_path="reports/external/oops_backtest.md",
    )
    print("Backtest finished. Summary:")
    for mode, m in summary.items():
        print(f"  [{mode}] n={m['n_trades']} wr={m['win_rate']:.3f} "
              f"pf={m['profit_factor']:.3f} exp_R={m['expectancy_R']:.3f} "
              f"dd_R={m['max_dd_R']:.3f}")
```

- [ ] **Step 4: Configurar pytest marker en `pyproject.toml` o `pytest.ini` si no existe**

Verificar el archivo de config existente:

```bash
cat C:/Proyectos/kha0sys3/pyproject.toml 2>&1 | grep -A 5 "markers"
```

Si no existe sección `[tool.pytest.ini_options]` con markers, añadir:

```toml
[tool.pytest.ini_options]
markers = [
    "integration: tests que cargan datos reales del proyecto",
]
```

- [ ] **Step 5: Run integration test**

```bash
pytest tests/strategies_external/test_run_oops_integration.py -v -m integration
```

Expected: 1 passed

- [ ] **Step 6: Run runner standalone para ver el reporte real**

```bash
python -m src.strategies_external.runners.run_oops
```

Expected: imprime resumen y crea `reports/external/oops_backtest.md` y `reports/external/oops_trades.parquet`.

- [ ] **Step 7: Commit**

```bash
git add src/strategies_external/runners tests/strategies_external/test_run_oops_integration.py reports/external/oops_backtest.md reports/external/oops_trades.parquet pyproject.toml
git commit -m "feat(strategies_external): run_oops runner with doc/atr/indicator modes"
```

---

## Task 17: Walk-forward + Monte Carlo en el reporte OOPS

**Files:**
- Modify: `src/strategies_external/runners/run_oops.py`
- Modify: `src/strategies_external/reporting/markdown.py`
- Modify: `tests/strategies_external/test_markdown_report.py`
- Modify: `tests/strategies_external/test_run_oops_integration.py`

- [ ] **Step 1: Añadir test de inclusión WF/MC en el reporte**

Modificar `tests/strategies_external/test_markdown_report.py` añadiendo:

```python
from src.strategies_external.common.walk_forward import walk_forward_split
from src.strategies_external.common.monte_carlo import monte_carlo_bootstrap


def test_report_includes_wf_and_mc(tmp_path: Path):
    base = datetime(2024, 1, 1)
    trades = [_trade(i, 0.5 if i % 3 != 0 else -1.0) for i in range(60)]
    trades_by_mode = {"doc": trades}
    wf = walk_forward_split(trades, n_windows=5, is_pct=0.7)
    mc = monte_carlo_bootstrap(trades, n_simulations=1000, ruin_threshold_R=-15.0, seed=1)
    report_path = tmp_path / "oops_backtest.md"
    write_backtest_report(
        report_path, strategy_name="oops", symbols=["SP500"],
        trades_by_mode=trades_by_mode,
        config={"period": "2018..", "risk_pct": 0.005},
        walk_forward_windows=wf, monte_carlo_results=mc,
    )
    content = report_path.read_text()
    assert "Walk-forward" in content
    assert "Monte Carlo" in content
    assert "prob_ruin" in content
```

- [ ] **Step 2: Run failing**

```bash
pytest tests/strategies_external/test_markdown_report.py::test_report_includes_wf_and_mc -v
```

Expected: TypeError (función no acepta `walk_forward_windows`)

- [ ] **Step 3: Extender `write_backtest_report`**

Modificar `src/strategies_external/reporting/markdown.py`. Cambiar la firma de `write_backtest_report` añadiendo dos kwargs opcionales:

```python
def write_backtest_report(
    path: Path,
    strategy_name: str,
    symbols: list[str],
    trades_by_mode: dict[str, list[Trade]],
    config: dict,
    walk_forward_windows: list | None = None,
    monte_carlo_results: dict | None = None,
) -> None:
```

Añadir al final de la función (antes del `path.write_text`):

```python
    if walk_forward_windows:
        lines.append("## Walk-forward (modo doc)")
        lines.append("")
        lines.append("| window | IS n | IS pf | IS wr | OOS n | OOS pf | OOS wr |")
        lines.append("|--------|------|-------|-------|-------|--------|--------|")
        for i, (is_, oos) in enumerate(walk_forward_windows, 1):
            mi = evaluate(is_); mo = evaluate(oos)
            lines.append(
                f"| {i} | {mi['n_trades']} | {_fmt(mi['profit_factor'])} | "
                f"{_fmt(mi['win_rate'])} | {mo['n_trades']} | "
                f"{_fmt(mo['profit_factor'])} | {_fmt(mo['win_rate'])} |"
            )
        lines.append("")

    if monte_carlo_results:
        lines.append("## Monte Carlo (modo doc, 10k bootstrap)")
        lines.append("")
        lines.append("| metric | value |")
        lines.append("|--------|-------|")
        for k, v in monte_carlo_results.items():
            lines.append(f"| {k} | {_fmt(v)} |")
        lines.append("")
```

- [ ] **Step 4: Run pass**

```bash
pytest tests/strategies_external/test_markdown_report.py -v
```

Expected: 2 passed

- [ ] **Step 5: Integrar WF y MC en el runner**

En `src/strategies_external/runners/run_oops.py`, modificar `run_oops_backtest` para que después de generar `trades_by_mode["doc"]` calcule WF y MC y los pase al writer:

```python
    from src.strategies_external.common.walk_forward import walk_forward_split
    from src.strategies_external.common.monte_carlo import monte_carlo_bootstrap

    doc_trades = trades_by_mode["doc"]
    try:
        wf = walk_forward_split(doc_trades, n_windows=5, is_pct=0.7)
    except ValueError:
        wf = None
    mc = monte_carlo_bootstrap(doc_trades, n_simulations=10_000,
                                ruin_threshold_R=-15.0, seed=42) if doc_trades else None

    write_backtest_report(
        output_path,
        strategy_name="oops",
        symbols=symbols,
        trades_by_mode=trades_by_mode,
        config={"period": "2018-01-01..today", "risk_pct": 0.005,
                "atr_grid": atr_grid},
        walk_forward_windows=wf,
        monte_carlo_results=mc,
    )
```

- [ ] **Step 6: Re-run runner real**

```bash
python -m src.strategies_external.runners.run_oops
```

Verificar que `reports/external/oops_backtest.md` ahora contiene secciones "Walk-forward" y "Monte Carlo".

- [ ] **Step 7: Commit**

```bash
git add src/strategies_external/runners/run_oops.py src/strategies_external/reporting/markdown.py tests/strategies_external/test_markdown_report.py reports/external/oops_backtest.md
git commit -m "feat(strategies_external): walk-forward + monte carlo in OOPS report"
```

---

## Task 18: ATR sweep en el runner OOPS

**Files:**
- Modify: `src/strategies_external/runners/run_oops.py`
- Modify: `src/strategies_external/reporting/markdown.py`
- Modify: `tests/strategies_external/test_run_oops_integration.py`

- [ ] **Step 1: Añadir test del sweep**

En `tests/strategies_external/test_run_oops_integration.py` añadir:

```python
@pytest.mark.integration
def test_run_oops_atr_sweep_picks_best(tmp_path: Path):
    output = tmp_path / "oops_backtest.md"
    summary = run_oops_backtest(
        symbols=["SP500"],
        data_dir="data",
        output_path=output,
        atr_grid=[(1.0, 1.5, 3.0), (1.5, 1.5, 3.0), (2.0, 2.0, 4.0)],
    )
    # summary["atr"] debe ser la mejor por calmar
    assert "atr" in summary
    assert "atr_grid_results" in summary
    assert len(summary["atr_grid_results"]) == 3
```

- [ ] **Step 2: Run failing**

```bash
pytest tests/strategies_external/test_run_oops_integration.py::test_run_oops_atr_sweep_picks_best -v -m integration
```

Expected: KeyError "atr_grid_results"

- [ ] **Step 3: Implementar sweep en el runner**

En `run_oops_backtest`, sustituir el bloque de ATR fijo por un sweep que itere todo el grid, evalúe cada combinación, elija el mejor por `calmar`, y reporte todos los puntos del grid:

```python
    atr_grid_results = []
    best_atr_trades: list[Trade] = []
    best_atr_calmar = -float("inf")

    for sl, tp1, tp2 in atr_grid:
        cand_trades: list[Trade] = []
        for sym in symbols:
            df_h1 = load_csv(sym, "H1", data_dir=data_dir)
            df_daily = aggregate_to_daily(df_h1)
            _, df_track = best_tracking_tf(sym, data_dir=data_dir)
            sigs = strategy.generate_signals(df_daily, symbol=sym)
            atr_mgr = ATRExitManager(sl_mult=sl, tp1_mult=tp1, tp2_mult=tp2)
            cand_trades.extend(
                run_backtest([atr_mgr.attach_levels(s) for s in sigs],
                             df_track, exit_mode="atr")
            )
        m = evaluate(cand_trades)
        atr_grid_results.append({"sl": sl, "tp1": tp1, "tp2": tp2, **m})
        if m["calmar"] > best_atr_calmar:
            best_atr_calmar = m["calmar"]
            best_atr_trades = cand_trades

    trades_by_mode["atr"] = best_atr_trades
```

(Eliminar el código previo de ATR fijo en el loop principal de símbolos.)

Y al final del runner, devolver:

```python
    summary = {m: evaluate(ts) for m, ts in trades_by_mode.items()}
    summary["atr_grid_results"] = atr_grid_results
    return summary
```

- [ ] **Step 4: Añadir tabla del grid en el reporte**

En `markdown.py`, añadir una sección extra controlada por kwarg `atr_grid_results`:

```python
def write_backtest_report(
    path: Path,
    strategy_name: str,
    symbols: list[str],
    trades_by_mode: dict[str, list[Trade]],
    config: dict,
    walk_forward_windows=None,
    monte_carlo_results=None,
    atr_grid_results: list[dict] | None = None,
) -> None:
```

Y el bloque al final (antes del write):

```python
    if atr_grid_results:
        lines.append("## ATR exit sweep")
        lines.append("")
        lines.append("| sl | tp1 | tp2 | n | wr | pf | exp_R | dd_R | calmar |")
        lines.append("|----|-----|-----|---|-----|-----|-------|------|--------|")
        for r in atr_grid_results:
            lines.append(
                f"| {r['sl']} | {r['tp1']} | {r['tp2']} | "
                f"{r['n_trades']} | {_fmt(r['win_rate'])} | {_fmt(r['profit_factor'])} | "
                f"{_fmt(r['expectancy_R'])} | {_fmt(r['max_dd_R'])} | {_fmt(r['calmar'])} |"
            )
        lines.append("")
```

Y pasar `atr_grid_results=atr_grid_results` desde el runner.

- [ ] **Step 5: Run tests**

```bash
pytest tests/strategies_external/ -v -m "not integration"
pytest tests/strategies_external/test_run_oops_integration.py -v -m integration
```

Expected: todos passed.

- [ ] **Step 6: Re-run runner real con grid completo**

Modificar el `__main__` del runner para que use el grid documentado en el spec:

```python
if __name__ == "__main__":
    grid = [(sl, tp1, tp2)
            for sl in (1.0, 1.5, 2.0, 2.5)
            for tp1 in (1.0, 1.5, 2.0)
            for tp2 in (2.0, 3.0, 4.0)
            if tp2 > tp1]
    summary = run_oops_backtest(
        symbols=["SP500", "NASDAQ100"],
        data_dir="data",
        output_path="reports/external/oops_backtest.md",
        atr_grid=grid,
    )
    print("OOPS backtest done.")
    for mode in ("doc", "atr", "indicator"):
        m = summary[mode]
        print(f"  [{mode}] n={m['n_trades']} wr={m['win_rate']:.3f} "
              f"pf={m['profit_factor']:.3f} dd_R={m['max_dd_R']:.3f} "
              f"calmar={m['calmar']:.3f}")
    best = max(summary["atr_grid_results"], key=lambda r: r["calmar"])
    print(f"  best ATR: sl={best['sl']} tp1={best['tp1']} tp2={best['tp2']} "
          f"calmar={best['calmar']:.3f}")
```

```bash
python -m src.strategies_external.runners.run_oops
```

Expected: reporte con tabla "ATR exit sweep" de 27 filas.

- [ ] **Step 7: Commit final**

```bash
git add src/strategies_external/runners/run_oops.py src/strategies_external/reporting/markdown.py tests/strategies_external/test_run_oops_integration.py reports/external/oops_backtest.md reports/external/oops_trades.parquet
git commit -m "feat(strategies_external): ATR exit sweep in OOPS runner"
```

---

## Task 19: Documentación inline del módulo

**Files:**
- Modify: `src/strategies_external/__init__.py`

- [ ] **Step 1: Actualizar docstring del módulo principal con el estado del Plan 1**

```python
# src/strategies_external/__init__.py
"""External strategies research module — Plan 1 (infra + OOPS).

Backtest-only. Aislado del bot live (FADE/MATH).

Implementado en Plan 1:
- Infraestructura: data_loader, ExitManagers (doc/atr/indicator),
  backtester, metrics, walk_forward, monte_carlo, markdown report.
- Estrategia OOPS (Larry Williams) con runner ejecutable:
    python -m src.strategies_external.runners.run_oops

Pendiente (Plan 2):
- SMA-18, Doble Suelo, Perdices Fib, COT-1.
- COT downloader y estacionalidad.
- Reporte comparativo cross-estrategias.

Specs:
- docs/superpowers/specs/2026-05-06-strategies-external-design.md
"""
```

- [ ] **Step 2: Commit**

```bash
git add src/strategies_external/__init__.py
git commit -m "docs(strategies_external): document Plan 1 status in module docstring"
```

---

## Self-Review (post-plan)

**1. Spec coverage:** repaso secciones del spec contra tasks de este plan:

| Spec section | Cubierto por |
|--------------|--------------|
| §3.1 Layout (Plan 1 scope) | T1 |
| §3.3 data_loader | T3, T4, T5 |
| §3.3 Signal | T6 |
| §3.3 Trade | T7 |
| §3.3 backtester | T9 |
| §3.3 metrics | T10 |
| §3.3 walk_forward | T11 |
| §3.3 monte_carlo | T12 |
| §3.4 ExitManagers (Doc/ATR/Indicator) — solo OOPS | T8 |
| §4.1 OOPS strategy | T14 |
| §6 Reportes (markdown + parquet) | T15, T16, T17, T18 |
| §5 Validación (WF + MC + sweep) | T17, T18 |

Plan 2 cubrirá: SMA-18, Doble Suelo, Perdices Fib, COT-1, comparación cross.

**2. Placeholder scan:** revisado el plan completo. Sin TBD/TODO/etc.

**3. Type consistency:** repasado:
- `Signal.indicator_anchors: dict[str, float]` consistente entre OOPS, ExitManagers y backtester.
- `Trade.exit_reason: Literal[...]` con los 6 valores usados consistentemente: tp1, tp2, stop, timestop, signal_inverso, eod.
- `run_backtest(signals, df, exit_mode)` firma idéntica en todos los call sites.
- `evaluate(trades) -> dict` retorno tipado uniforme.
- ExitManager `attach_levels(signal_raw) -> Signal` consistente.

Plan listo.

---

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-05-06-strategies-external-plan-1-infra-oops.md`. Two execution options:**

**1. Subagent-Driven (recommended)** - dispatch un subagent fresco por task, review entre tasks, iteración rápida.

**2. Inline Execution** - ejecutar tasks en esta misma sesión usando executing-plans, batch con checkpoints.

**¿Cuál prefieres?**
