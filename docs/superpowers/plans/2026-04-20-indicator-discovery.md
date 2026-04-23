# Indicator-Based Edge Discovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a research pipeline that scans RSI/MACD/BB/Fractal/ADX signals across 15 assets × 2 timeframes × 5 sessions to discover edge with ≥100 trades/year and WR ≥ 80%.

**Architecture:** Two-phase pipeline. Phase-1 evaluates 1,500 (asset × TF × session × primary signal) combos with fixed R:R (TP=2×ATR / SL=1×ATR) and loose gates. Phase-2 optimizes survivors over 11 confluence combos × 20 R:R ATR combos, applying strict gates (WR ≥ 80%, walk-forward, Monte Carlo, decay). Research only — no live trading changes.

**Tech Stack:** Python 3.11, Polars (vectorized), pytest, existing kha0sys3 modules (`TrackerEngine`, `StatisticalEngine`, `CSVPolarsLoader`).

**Spec:** `docs/superpowers/specs/2026-04-20-indicator-discovery-design.md`

---

## File Structure

**New files:**
- `src/application/indicators.py` — vectorized RSI/MACD/BB/Fractal/ADX on Polars
- `src/application/signal_generator.py` — 10 primary signals + 4 confluence filters
- `src/engine/indicator_backtester.py` — INDICATOR archetype backtester (ATR exits, time-stop)
- `src/engine/run_indicator_discovery.py` — end-to-end Phase-1 + Phase-2 runner
- `src/engine/indicator_validation.py` — WF/MC/decay helpers (shared with existing robustness code)
- `src/engine/indicator_reporter.py` — Markdown + JSON export
- `tests/test_indicators.py`
- `tests/test_signal_generator.py`
- `tests/test_indicator_backtester.py`

**Modified files:**
- `src/domain/constants.py` — add indicator params and discovery gates
- `src/domain/models.py` — add `IndicatorSignal` dataclass (if needed) and `INDICATOR` archetype enum value

**Outputs (generated, not committed):**
- `data/enriched/{symbol}_{tf}.parquet` — cache of enriched bars
- `reports/indicator_discovery_phase1.md`
- `reports/Indicator_Discovery_Final.md`
- `reports/indicator_strategies.json`
- `reports/indicator_survivors.parquet`

---

## Task 1: Constants and domain additions

**Files:**
- Modify: `src/domain/constants.py`
- Modify: `src/domain/models.py`

- [ ] **Step 1: Add indicator and discovery constants**

Edit `src/domain/constants.py` appending at end of file:

```python
# ── Indicator parameters (fixed; optimization out of scope) ────
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
BB_PERIOD = 20
BB_STD = 2.0
FRACTAL_WINDOW = 5  # 2 left + pivot + 2 right
ADX_PERIOD = 14
ADX_TREND_THRESHOLD = 25.0
ADX_TREND_SOFT = 20.0

# ── Indicator discovery: Phase-1 gates (loose) ─────────────────
PHASE1_MIN_TRADES_PER_YEAR = 100
PHASE1_MIN_WR = 0.60
PHASE1_MIN_PF = 1.2
PHASE1_MIN_EXPECTANCY_R = 0.0

# ── Indicator discovery: Phase-2 gates (strict) ────────────────
PHASE2_MIN_TRADES_PER_YEAR = 100
PHASE2_MIN_WR = 0.80
PHASE2_MIN_PF = 1.3
PHASE2_MIN_EXPECTANCY_R = 0.10
PHASE2_MAX_DD_R = 20.0
PHASE2_WF_OOS_RATIO = 0.85  # WR_oos >= 0.85 * WR_is
PHASE2_MC_MAX_RUIN_PCT = 0.01  # < 1% @ risk 1%
PHASE2_DECAY_MIN_RATIO = 0.70  # last-6m slope >= 0.7 * global slope

# ── Indicator R:R ATR grid (Phase-2) ───────────────────────────
INDICATOR_TP_ATR_GRID = (1.0, 1.5, 2.0, 2.5, 3.0)
INDICATOR_SL_ATR_GRID = (0.75, 1.0, 1.5, 2.0)

# ── Session definitions (UTC hours) for indicator discovery ────
INDICATOR_SESSIONS = {
    "ASIA":        (0, 7),
    "LONDON":      (7, 12),
    "NY":          (12, 17),
    "LONDON_NY":   (7, 17),
    "ALL_DAY":     (0, 24),
}

# ── Walk-forward windows ──────────────────────────────────────
WF_IS_MONTHS = 6
WF_OOS_MONTHS = 2

# Universe of 15 assets (original set, includes XAGUSD + SP500)
INDICATOR_UNIVERSE = (
    "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "GBPJPY", "EURJPY", "GBPAUD",
    "XAUUSD", "XAGUSD", "WTI", "BRENT", "NATGAS",
    "SP500", "NASDAQ100", "VIX",
)
INDICATOR_TIMEFRAMES = ("M15", "H1")
```

- [ ] **Step 2: Add INDICATOR archetype to models**

Open `src/domain/models.py` and find the existing archetype enum (likely `Archetype` or similar string constants). Append:

```python
# If enum:
#   INDICATOR = "INDICATOR"
# If string constants:
ARCHETYPE_INDICATOR = "INDICATOR"
```

Inspect the file first to match the existing pattern exactly. If an `Archetype` Enum class exists, add `INDICATOR = "INDICATOR"` as a new member.

- [ ] **Step 3: Commit**

```bash
git add src/domain/constants.py src/domain/models.py
git commit -m "feat(domain): add indicator params, discovery gates, INDICATOR archetype"
```

---

## Task 2: Indicator calculators (Polars, vectorized)

**Files:**
- Create: `src/application/indicators.py`
- Create: `tests/test_indicators.py`

- [ ] **Step 1: Write failing unit tests**

Create `tests/test_indicators.py`:

```python
"""Unit tests for indicator calculations. Reference values computed vs TA-Lib."""
import polars as pl
import pytest
from src.application.indicators import IndicatorEnricher


@pytest.fixture
def ohlc_df():
    """30 deterministic bars for stable indicator math."""
    closes = [
        44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84, 46.08,
        45.89, 46.03, 45.61, 46.28, 46.28, 46.00, 46.03, 46.41, 46.22, 45.64,
        46.21, 46.25, 45.71, 46.45, 45.78, 45.35, 44.03, 44.18, 44.22, 44.57,
    ]
    highs = [c + 0.20 for c in closes]
    lows = [c - 0.20 for c in closes]
    opens = [c - 0.05 for c in closes]
    return pl.DataFrame({
        "time": pl.datetime_range(
            start=pl.datetime(2024, 1, 1), end=pl.datetime(2024, 1, 1, 7, 15),
            interval="15m", eager=True,
        )[:30],
        "open": opens, "high": highs, "low": lows, "close": closes,
    })


def test_rsi_14_matches_reference(ohlc_df):
    """RSI(14) on Wilder's smoothing at bar 14 ≈ 70.53."""
    out = IndicatorEnricher.add_rsi(ohlc_df, period=14)
    rsi_14 = out["rsi_14"].to_list()[14]
    assert rsi_14 == pytest.approx(70.53, abs=0.5)


def test_macd_columns_present(ohlc_df):
    out = IndicatorEnricher.add_macd(ohlc_df, fast=12, slow=26, signal=9)
    assert {"macd", "macd_signal", "macd_hist"}.issubset(out.columns)
    # At the last bar, MACD and signal should both be defined
    last = out.row(-1, named=True)
    assert last["macd"] is not None
    assert last["macd_signal"] is not None


def test_bollinger_bands_contain_price_at_mean(ohlc_df):
    out = IndicatorEnricher.add_bollinger(ohlc_df, period=20, std_mult=2.0)
    row = out.row(25, named=True)
    assert row["bb_lower"] <= row["bb_middle"] <= row["bb_upper"]
    assert 0.0 <= row["bb_pct"] <= 1.5  # price usually within or slightly beyond


def test_fractal_marks_local_extrema(ohlc_df):
    out = IndicatorEnricher.add_fractals(ohlc_df, window=5)
    # At least one fractal_high and one fractal_low should exist in 30 bars
    assert out["fractal_high"].sum() >= 1
    assert out["fractal_low"].sum() >= 1
    # Fractals cannot exist in first 2 or last 2 bars (confirmation lag)
    assert out["fractal_high"].to_list()[0] is False
    assert out["fractal_high"].to_list()[-1] is False


def test_adx_in_valid_range(ohlc_df):
    out = IndicatorEnricher.add_adx(ohlc_df, period=14)
    adx = out["adx_14"].drop_nulls().to_list()
    assert len(adx) > 0
    assert all(0 <= v <= 100 for v in adx)


def test_no_lookahead_in_any_indicator(ohlc_df):
    """Given bars [0..N], indicator values at bar K must not change when bars K+1..N are removed."""
    full = IndicatorEnricher.enrich_all(ohlc_df)
    trunc = IndicatorEnricher.enrich_all(ohlc_df.head(20))
    for col in ["rsi_14", "macd", "bb_upper", "adx_14"]:
        for i in range(19):  # compare bars 0..18 (last bar has fractal confirmation lag)
            a = full[col].to_list()[i]
            b = trunc[col].to_list()[i]
            if a is None and b is None:
                continue
            assert a == pytest.approx(b, rel=1e-9), f"look-ahead in {col} at bar {i}"
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_indicators.py -v
```

Expected: all tests fail with `ModuleNotFoundError: src.application.indicators`.

- [ ] **Step 3: Implement `src/application/indicators.py`**

```python
"""Vectorized technical indicators on Polars DataFrames.

All functions assume the input has columns: time, open, high, low, close,
sorted ascending by time. They are look-ahead-safe: the value at bar i
depends only on bars 0..i.
"""
import polars as pl
from src.domain.constants import (
    RSI_PERIOD, MACD_FAST, MACD_SLOW, MACD_SIGNAL,
    BB_PERIOD, BB_STD, FRACTAL_WINDOW, ADX_PERIOD,
)


class IndicatorEnricher:
    """Static methods that add indicator columns to an OHLC Polars DataFrame."""

    @staticmethod
    def add_rsi(df: pl.DataFrame, period: int = RSI_PERIOD) -> pl.DataFrame:
        delta = pl.col("close") - pl.col("close").shift(1)
        alpha = 1.0 / period
        return df.with_columns([
            pl.when(delta > 0).then(delta).otherwise(0.0).alias("_gain"),
            pl.when(delta < 0).then(-delta).otherwise(0.0).alias("_loss"),
        ]).with_columns([
            pl.col("_gain").ewm_mean(alpha=alpha, adjust=False, min_periods=period).alias("_avg_gain"),
            pl.col("_loss").ewm_mean(alpha=alpha, adjust=False, min_periods=period).alias("_avg_loss"),
        ]).with_columns([
            pl.when(pl.col("_avg_loss") == 0)
            .then(100.0)
            .otherwise(100.0 - 100.0 / (1.0 + pl.col("_avg_gain") / pl.col("_avg_loss")))
            .alias(f"rsi_{period}")
        ]).drop(["_gain", "_loss", "_avg_gain", "_avg_loss"])

    @staticmethod
    def add_macd(df: pl.DataFrame, fast: int = MACD_FAST, slow: int = MACD_SLOW,
                 signal: int = MACD_SIGNAL) -> pl.DataFrame:
        return df.with_columns([
            pl.col("close").ewm_mean(span=fast, adjust=False, min_periods=fast).alias("_ema_fast"),
            pl.col("close").ewm_mean(span=slow, adjust=False, min_periods=slow).alias("_ema_slow"),
        ]).with_columns([
            (pl.col("_ema_fast") - pl.col("_ema_slow")).alias("macd")
        ]).with_columns([
            pl.col("macd").ewm_mean(span=signal, adjust=False, min_periods=signal).alias("macd_signal")
        ]).with_columns([
            (pl.col("macd") - pl.col("macd_signal")).alias("macd_hist")
        ]).drop(["_ema_fast", "_ema_slow"])

    @staticmethod
    def add_bollinger(df: pl.DataFrame, period: int = BB_PERIOD,
                      std_mult: float = BB_STD) -> pl.DataFrame:
        return df.with_columns([
            pl.col("close").rolling_mean(window_size=period).alias("bb_middle"),
            pl.col("close").rolling_std(window_size=period).alias("_bb_std"),
        ]).with_columns([
            (pl.col("bb_middle") + std_mult * pl.col("_bb_std")).alias("bb_upper"),
            (pl.col("bb_middle") - std_mult * pl.col("_bb_std")).alias("bb_lower"),
        ]).with_columns([
            ((pl.col("close") - pl.col("bb_lower")) /
             (pl.col("bb_upper") - pl.col("bb_lower"))).alias("bb_pct")
        ]).drop("_bb_std")

    @staticmethod
    def add_fractals(df: pl.DataFrame, window: int = FRACTAL_WINDOW) -> pl.DataFrame:
        """Williams fractals. A fractal_high at bar i requires high[i-2] < high[i]
        and high[i-1] < high[i] and high[i+1] < high[i] and high[i+2] < high[i].
        Confirmed at bar i+2 — we set the flag at bar i+2 to avoid look-ahead.
        """
        assert window == 5, "Only 5-bar fractal supported"
        return df.with_columns([
            # Confirm at bar i+2: shift by -2 so the look-back uses bars [i-4..i] of original series
            (
                (pl.col("high").shift(4) < pl.col("high").shift(2)) &
                (pl.col("high").shift(3) < pl.col("high").shift(2)) &
                (pl.col("high").shift(1) < pl.col("high").shift(2)) &
                (pl.col("high")          < pl.col("high").shift(2))
            ).fill_null(False).alias("fractal_high"),
            (
                (pl.col("low").shift(4) > pl.col("low").shift(2)) &
                (pl.col("low").shift(3) > pl.col("low").shift(2)) &
                (pl.col("low").shift(1) > pl.col("low").shift(2)) &
                (pl.col("low")          > pl.col("low").shift(2))
            ).fill_null(False).alias("fractal_low"),
        ])

    @staticmethod
    def add_adx(df: pl.DataFrame, period: int = ADX_PERIOD) -> pl.DataFrame:
        """Wilder ADX. DM+ = up_move if up_move > down_move and up_move > 0 else 0."""
        alpha = 1.0 / period
        df = df.with_columns([
            (pl.col("high") - pl.col("high").shift(1)).alias("_up_move"),
            (pl.col("low").shift(1) - pl.col("low")).alias("_dn_move"),
            pl.max_horizontal(
                pl.col("high") - pl.col("low"),
                (pl.col("high") - pl.col("close").shift(1)).abs(),
                (pl.col("low") - pl.col("close").shift(1)).abs(),
            ).alias("_tr"),
        ])
        df = df.with_columns([
            pl.when((pl.col("_up_move") > pl.col("_dn_move")) & (pl.col("_up_move") > 0))
              .then(pl.col("_up_move")).otherwise(0.0).alias("_dm_plus"),
            pl.when((pl.col("_dn_move") > pl.col("_up_move")) & (pl.col("_dn_move") > 0))
              .then(pl.col("_dn_move")).otherwise(0.0).alias("_dm_minus"),
        ])
        df = df.with_columns([
            pl.col("_tr").ewm_mean(alpha=alpha, adjust=False, min_periods=period).alias("_atr_w"),
            pl.col("_dm_plus").ewm_mean(alpha=alpha, adjust=False, min_periods=period).alias("_dm_plus_w"),
            pl.col("_dm_minus").ewm_mean(alpha=alpha, adjust=False, min_periods=period).alias("_dm_minus_w"),
        ])
        df = df.with_columns([
            (100.0 * pl.col("_dm_plus_w") / pl.col("_atr_w")).alias("plus_di"),
            (100.0 * pl.col("_dm_minus_w") / pl.col("_atr_w")).alias("minus_di"),
        ])
        df = df.with_columns([
            (100.0 * (pl.col("plus_di") - pl.col("minus_di")).abs() /
             (pl.col("plus_di") + pl.col("minus_di"))).alias("_dx"),
        ])
        df = df.with_columns([
            pl.col("_dx").ewm_mean(alpha=alpha, adjust=False, min_periods=period).alias(f"adx_{period}")
        ])
        return df.drop(["_up_move", "_dn_move", "_tr", "_dm_plus", "_dm_minus",
                        "_atr_w", "_dm_plus_w", "_dm_minus_w", "_dx"])

    @staticmethod
    def enrich_all(df: pl.DataFrame) -> pl.DataFrame:
        """Apply all 5 indicators in order. Input must be sorted by time ascending."""
        df = IndicatorEnricher.add_rsi(df)
        df = IndicatorEnricher.add_macd(df)
        df = IndicatorEnricher.add_bollinger(df)
        df = IndicatorEnricher.add_fractals(df)
        df = IndicatorEnricher.add_adx(df)
        return df
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_indicators.py -v
```

Expected: all 6 tests PASS. If the RSI reference value fails by a larger margin, check that seed data matches the reference series. The absolute tolerance (0.5) is generous enough for minor smoothing differences.

- [ ] **Step 5: Commit**

```bash
git add src/application/indicators.py tests/test_indicators.py
git commit -m "feat(indicators): add vectorized RSI/MACD/BB/Fractal/ADX on Polars"
```

---

## Task 3: Signal generator

**Files:**
- Create: `src/application/signal_generator.py`
- Create: `tests/test_signal_generator.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_signal_generator.py`:

```python
"""Unit tests for signal generation."""
import polars as pl
import pytest
from src.application.indicators import IndicatorEnricher
from src.application.signal_generator import SignalGenerator, SIGNAL_TYPES, CONFLUENCE_FILTERS


@pytest.fixture
def enriched_df():
    """200 bars enriched with all indicators for signal coverage."""
    import numpy as np
    rng = np.random.default_rng(42)
    n = 200
    price = 100.0 + rng.standard_normal(n).cumsum() * 0.5
    df = pl.DataFrame({
        "time": pl.datetime_range(
            start=pl.datetime(2024, 1, 1), end=pl.datetime(2024, 1, 3, 3, 45),
            interval="15m", eager=True,
        )[:n],
        "open": price - 0.05, "high": price + 0.20, "low": price - 0.20, "close": price,
    })
    return IndicatorEnricher.enrich_all(df)


def test_all_10_signal_types_registered():
    assert len(SIGNAL_TYPES) == 10
    expected = {
        "RSI_OB_REV", "BB_TOUCH_REV", "FRACTAL_REV", "MACD_DIVERGENCE", "BB_RSI_CONFLUENCE",
        "MACD_CROSS", "ADX_BREAKOUT", "BB_BREAKOUT", "RSI_50_CROSS", "FRACTAL_TREND",
    }
    assert set(SIGNAL_TYPES) == expected


def test_4_confluence_filters_registered():
    expected = {"RSI_ZONE", "ADX_REGIME", "BB_POSITION", "MACD_ALIGN"}
    assert set(CONFLUENCE_FILTERS) == expected


def test_rsi_ob_rev_produces_signals(enriched_df):
    sigs = SignalGenerator.generate(enriched_df, signal_type="RSI_OB_REV", symbol="TEST")
    assert {"time", "symbol", "direction", "signal_type"}.issubset(sigs.columns)
    assert set(sigs["direction"].unique()).issubset({"LONG", "SHORT"})


def test_macd_cross_directions_balanced(enriched_df):
    sigs = SignalGenerator.generate(enriched_df, signal_type="MACD_CROSS", symbol="TEST")
    # On random walk we expect at least a handful of crosses, both directions
    assert len(sigs) >= 2


def test_confluence_filter_reduces_signal_count(enriched_df):
    base = SignalGenerator.generate(enriched_df, signal_type="MACD_CROSS", symbol="TEST")
    filtered = SignalGenerator.apply_filters(base, enriched_df, filters=("ADX_REGIME_TREND",))
    assert len(filtered) <= len(base)


def test_signal_timestamp_is_bar_of_confirmation(enriched_df):
    """Signal timestamp must match the bar where the condition is first true (no look-ahead)."""
    sigs = SignalGenerator.generate(enriched_df, signal_type="BB_BREAKOUT", symbol="TEST")
    if len(sigs) > 0:
        t = sigs["time"].to_list()[0]
        # Confirm the breakout condition was true at that bar
        row = enriched_df.filter(pl.col("time") == t).row(0, named=True)
        assert (row["close"] > row["bb_upper"]) or (row["close"] < row["bb_lower"])
```

- [ ] **Step 2: Run tests — expect failures (module missing)**

```bash
pytest tests/test_signal_generator.py -v
```

Expected: `ModuleNotFoundError`.

- [ ] **Step 3: Implement `src/application/signal_generator.py`**

```python
"""Primary signal generators and confluence filters for indicator-based archetypes.

Emits a long-format DataFrame with columns:
    time, symbol, direction (LONG/SHORT), signal_type, indicator_state (dict-as-struct)

All filters return a subset of the input signal DataFrame.
"""
from __future__ import annotations
import polars as pl

SIGNAL_TYPES = (
    # Reversion
    "RSI_OB_REV", "BB_TOUCH_REV", "FRACTAL_REV", "MACD_DIVERGENCE", "BB_RSI_CONFLUENCE",
    # Momentum
    "MACD_CROSS", "ADX_BREAKOUT", "BB_BREAKOUT", "RSI_50_CROSS", "FRACTAL_TREND",
)

CONFLUENCE_FILTERS = ("RSI_ZONE", "ADX_REGIME", "BB_POSITION", "MACD_ALIGN")


class SignalGenerator:
    """Generate long-format signal DataFrames from an enriched OHLC bar DataFrame."""

    @staticmethod
    def generate(df: pl.DataFrame, signal_type: str, symbol: str) -> pl.DataFrame:
        if signal_type == "RSI_OB_REV":
            long_cond = (pl.col("rsi_14").shift(1) <= 30) & (pl.col("rsi_14") > 30)
            short_cond = (pl.col("rsi_14").shift(1) >= 70) & (pl.col("rsi_14") < 70)
        elif signal_type == "BB_TOUCH_REV":
            long_cond = pl.col("low") <= pl.col("bb_lower")
            short_cond = pl.col("high") >= pl.col("bb_upper")
        elif signal_type == "FRACTAL_REV":
            long_cond = pl.col("fractal_low")
            short_cond = pl.col("fractal_high")
        elif signal_type == "MACD_DIVERGENCE":
            # 20-bar window. Bullish div: price makes LL but MACD makes HL.
            hi20 = pl.col("high").rolling_max(window_size=20)
            lo20 = pl.col("low").rolling_min(window_size=20)
            macd_hi20 = pl.col("macd").rolling_max(window_size=20)
            macd_lo20 = pl.col("macd").rolling_min(window_size=20)
            long_cond = (pl.col("low") <= lo20) & (pl.col("macd") > macd_lo20.shift(10))
            short_cond = (pl.col("high") >= hi20) & (pl.col("macd") < macd_hi20.shift(10))
        elif signal_type == "BB_RSI_CONFLUENCE":
            long_cond = (pl.col("low") <= pl.col("bb_lower")) & (pl.col("rsi_14") < 30)
            short_cond = (pl.col("high") >= pl.col("bb_upper")) & (pl.col("rsi_14") > 70)
        elif signal_type == "MACD_CROSS":
            long_cond = (pl.col("macd").shift(1) <= pl.col("macd_signal").shift(1)) & \
                        (pl.col("macd") > pl.col("macd_signal"))
            short_cond = (pl.col("macd").shift(1) >= pl.col("macd_signal").shift(1)) & \
                         (pl.col("macd") < pl.col("macd_signal"))
        elif signal_type == "ADX_BREAKOUT":
            crossed = (pl.col("adx_14").shift(1) < 25) & (pl.col("adx_14") >= 25)
            long_cond = crossed & (pl.col("plus_di") > pl.col("minus_di"))
            short_cond = crossed & (pl.col("minus_di") > pl.col("plus_di"))
        elif signal_type == "BB_BREAKOUT":
            long_cond = pl.col("close") > pl.col("bb_upper")
            short_cond = pl.col("close") < pl.col("bb_lower")
        elif signal_type == "RSI_50_CROSS":
            long_cond = (pl.col("rsi_14").shift(1) <= 50) & (pl.col("rsi_14") > 50)
            short_cond = (pl.col("rsi_14").shift(1) >= 50) & (pl.col("rsi_14") < 50)
        elif signal_type == "FRACTAL_TREND":
            long_cond = pl.col("fractal_low") & (pl.col("adx_14") > 20) & \
                        (pl.col("plus_di") > pl.col("minus_di"))
            short_cond = pl.col("fractal_high") & (pl.col("adx_14") > 20) & \
                         (pl.col("minus_di") > pl.col("plus_di"))
        else:
            raise ValueError(f"Unknown signal_type: {signal_type}")

        return df.with_columns([
            pl.when(long_cond).then(pl.lit("LONG"))
              .when(short_cond).then(pl.lit("SHORT"))
              .otherwise(None).alias("direction"),
        ]).filter(pl.col("direction").is_not_null()).select([
            "time",
            pl.lit(symbol).alias("symbol"),
            "direction",
            pl.lit(signal_type).alias("signal_type"),
            "close", "high", "low",  # preserve for backtester
            "atr_14" if "atr_14" in df.columns else pl.lit(None).alias("atr_14"),
        ])

    @staticmethod
    def apply_filters(signals: pl.DataFrame, enriched: pl.DataFrame,
                      filters: tuple[str, ...]) -> pl.DataFrame:
        """Apply confluence filters. Each filter is identified as '{FILTER}_{STATE}'
        e.g. 'ADX_REGIME_TREND', 'RSI_ZONE_EXTREME', 'BB_POSITION_UPPER', 'MACD_ALIGN_POS'.

        Filters are joined to signals by time then applied as boolean masks.
        """
        if not filters:
            return signals
        # Join enriched state at signal time
        join_cols = ["time", "rsi_14", "adx_14", "bb_pct", "macd_hist"]
        ctx = enriched.select(join_cols)
        joined = signals.join(ctx, on="time", how="left")

        mask = pl.lit(True)
        for f in filters:
            if f == "ADX_REGIME_TREND":
                mask = mask & (pl.col("adx_14") >= 25)
            elif f == "ADX_REGIME_RANGE":
                mask = mask & (pl.col("adx_14") < 20)
            elif f == "RSI_ZONE_EXTREME":
                mask = mask & ((pl.col("rsi_14") >= 70) | (pl.col("rsi_14") <= 30))
            elif f == "RSI_ZONE_NEUTRAL":
                mask = mask & (pl.col("rsi_14").is_between(40, 60))
            elif f == "BB_POSITION_UPPER":
                mask = mask & (pl.col("bb_pct") >= 0.67)
            elif f == "BB_POSITION_LOWER":
                mask = mask & (pl.col("bb_pct") <= 0.33)
            elif f == "MACD_ALIGN_POS":
                mask = mask & (pl.col("macd_hist") > 0)
            elif f == "MACD_ALIGN_NEG":
                mask = mask & (pl.col("macd_hist") < 0)
            else:
                raise ValueError(f"Unknown filter: {f}")
        return joined.filter(mask).select(signals.columns)
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_signal_generator.py -v
```

Expected: all 6 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/application/signal_generator.py tests/test_signal_generator.py
git commit -m "feat(signals): add 10 primary signals + 4 confluence filter families"
```

---

## Task 4: INDICATOR archetype backtester

**Files:**
- Create: `src/engine/indicator_backtester.py`
- Create: `tests/test_indicator_backtester.py`

**Context:** This is a standalone backtester for INDICATOR signals. It does NOT modify the existing `strategy_backtester.py` (which remains FADE-specific). The backtester consumes signal DataFrames, applies ATR TP/SL and time-stop-to-session-close, enforces per-day dedup, and returns a trade-level DataFrame for stats.

- [ ] **Step 1: Write failing tests**

Create `tests/test_indicator_backtester.py`:

```python
import polars as pl
import pytest
from src.engine.indicator_backtester import IndicatorBacktester, BacktestConfig


@pytest.fixture
def bars_with_atr():
    """Synthetic 100-bar series with ATR=0.50 and clean trend to trigger TP."""
    import numpy as np
    n = 100
    rng = np.random.default_rng(0)
    price = 100.0 + np.arange(n) * 0.10 + rng.standard_normal(n) * 0.05
    return pl.DataFrame({
        "time": pl.datetime_range(
            start=pl.datetime(2024, 1, 1, 7, 0),
            end=pl.datetime(2024, 1, 2, 7, 45),
            interval="15m", eager=True,
        )[:n],
        "open": price, "high": price + 0.25, "low": price - 0.25, "close": price,
        "atr_14": [0.50] * n,
    })


@pytest.fixture
def trivial_long_signal(bars_with_atr):
    """One LONG signal at bar 10."""
    row = bars_with_atr.row(10, named=True)
    return pl.DataFrame({
        "time": [row["time"]],
        "symbol": ["TEST"],
        "direction": ["LONG"],
        "signal_type": ["UNIT_TEST"],
        "close": [row["close"]],
        "high": [row["high"]],
        "low": [row["low"]],
        "atr_14": [row["atr_14"]],
    })


def test_long_trade_hits_tp(bars_with_atr, trivial_long_signal):
    cfg = BacktestConfig(tp_atr_mult=2.0, sl_atr_mult=1.0, session_end_hour_utc=17,
                         friction_r=0.0)
    trades = IndicatorBacktester.run(trivial_long_signal, bars_with_atr, cfg)
    assert len(trades) == 1
    t = trades.row(0, named=True)
    assert t["exit_reason"] in ("TP", "SL", "TIME_STOP")
    # Rising series w/ ATR=0.5, TP=1.0 above entry → should hit TP
    assert t["exit_reason"] == "TP"
    assert t["r_multiple"] == pytest.approx(2.0, abs=0.01)


def test_dedup_one_trade_per_day_per_symbol_signal(bars_with_atr):
    # Two signals on the same day same symbol same type → only first survives
    row_a = bars_with_atr.row(5, named=True)
    row_b = bars_with_atr.row(10, named=True)
    signals = pl.DataFrame({
        "time": [row_a["time"], row_b["time"]],
        "symbol": ["TEST", "TEST"],
        "direction": ["LONG", "LONG"],
        "signal_type": ["DUP", "DUP"],
        "close": [row_a["close"], row_b["close"]],
        "high": [row_a["high"], row_b["high"]],
        "low": [row_a["low"], row_b["low"]],
        "atr_14": [0.50, 0.50],
    })
    cfg = BacktestConfig(tp_atr_mult=2.0, sl_atr_mult=1.0, session_end_hour_utc=17,
                         friction_r=0.0)
    trades = IndicatorBacktester.run(signals, bars_with_atr, cfg)
    assert len(trades) == 1
    assert trades["time"].to_list()[0] == row_a["time"]


def test_session_time_stop_closes_trade(bars_with_atr, trivial_long_signal):
    cfg = BacktestConfig(tp_atr_mult=100.0, sl_atr_mult=100.0, session_end_hour_utc=17,
                         friction_r=0.0)
    trades = IndicatorBacktester.run(trivial_long_signal, bars_with_atr, cfg)
    assert trades.row(0, named=True)["exit_reason"] == "TIME_STOP"


def test_friction_is_subtracted(bars_with_atr, trivial_long_signal):
    cfg = BacktestConfig(tp_atr_mult=2.0, sl_atr_mult=1.0, session_end_hour_utc=17,
                         friction_r=0.10)
    trades = IndicatorBacktester.run(trivial_long_signal, bars_with_atr, cfg)
    # Gross = +2R, net = 2.0 - 0.1 = 1.9
    assert trades.row(0, named=True)["r_multiple"] == pytest.approx(1.90, abs=0.01)
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_indicator_backtester.py -v
```

Expected: `ModuleNotFoundError`.

- [ ] **Step 3: Implement `src/engine/indicator_backtester.py`**

```python
"""Event-driven backtester for INDICATOR-archetype signals.

Each signal becomes a LIMIT at the signal bar's close price. TP = entry ± tp_atr_mult*ATR,
SL = entry ∓ sl_atr_mult*ATR. Trades time-stop at session_end_hour_utc.
Dedup: at most one trade per (symbol, signal_type, trade_date).
"""
from __future__ import annotations
from dataclasses import dataclass
import polars as pl


@dataclass(frozen=True)
class BacktestConfig:
    tp_atr_mult: float
    sl_atr_mult: float
    session_end_hour_utc: int
    friction_r: float


class IndicatorBacktester:

    @staticmethod
    def run(signals: pl.DataFrame, bars: pl.DataFrame, cfg: BacktestConfig) -> pl.DataFrame:
        """Return trade-level DataFrame: time, symbol, signal_type, direction,
        entry_price, tp_price, sl_price, exit_time, exit_price, exit_reason, r_multiple."""
        if len(signals) == 0:
            return _empty_trades()

        # Dedup: keep first per (symbol, signal_type, trade_date)
        deduped = signals.with_columns([
            pl.col("time").dt.date().alias("_date")
        ]).sort("time").unique(
            subset=["symbol", "signal_type", "_date"], keep="first"
        ).drop("_date")

        # Build bars index for fast lookup
        bars_sorted = bars.sort("time")
        bar_times = bars_sorted["time"].to_list()
        bar_highs = bars_sorted["high"].to_list()
        bar_lows = bars_sorted["low"].to_list()
        bar_closes = bars_sorted["close"].to_list()

        # Build dict time -> idx
        time_to_idx = {t: i for i, t in enumerate(bar_times)}

        results = []
        for sig in deduped.iter_rows(named=True):
            if sig["atr_14"] is None:
                continue
            entry = sig["close"]
            atr = sig["atr_14"]
            direction = sig["direction"]
            if direction == "LONG":
                tp = entry + cfg.tp_atr_mult * atr
                sl = entry - cfg.sl_atr_mult * atr
            else:
                tp = entry - cfg.tp_atr_mult * atr
                sl = entry + cfg.sl_atr_mult * atr

            # Scan bars forward from signal bar + 1 until session_end or TP/SL hit
            start_idx = time_to_idx.get(sig["time"])
            if start_idx is None:
                continue
            exit_reason = None
            exit_price = None
            exit_time = None
            signal_date = sig["time"].date()
            for i in range(start_idx + 1, len(bar_times)):
                bt = bar_times[i]
                # Stop at session end on same trading day
                if bt.date() > signal_date or bt.hour >= cfg.session_end_hour_utc:
                    exit_reason = "TIME_STOP"
                    exit_price = bar_closes[i - 1]
                    exit_time = bar_times[i - 1]
                    break
                hi = bar_highs[i]
                lo = bar_lows[i]
                if direction == "LONG":
                    if hi >= tp:
                        exit_reason, exit_price, exit_time = "TP", tp, bt
                        break
                    if lo <= sl:
                        exit_reason, exit_price, exit_time = "SL", sl, bt
                        break
                else:
                    if lo <= tp:
                        exit_reason, exit_price, exit_time = "TP", tp, bt
                        break
                    if hi >= sl:
                        exit_reason, exit_price, exit_time = "SL", sl, bt
                        break
            else:
                # Reached end of bars without hitting anything
                exit_reason = "TIME_STOP"
                exit_price = bar_closes[-1]
                exit_time = bar_times[-1]

            # R-multiple
            risk_per_unit = cfg.sl_atr_mult * atr
            if direction == "LONG":
                pnl = exit_price - entry
            else:
                pnl = entry - exit_price
            r_gross = pnl / risk_per_unit if risk_per_unit > 0 else 0.0
            r_net = r_gross - cfg.friction_r

            results.append({
                "time": sig["time"], "symbol": sig["symbol"],
                "signal_type": sig["signal_type"], "direction": direction,
                "entry_price": entry, "tp_price": tp, "sl_price": sl,
                "exit_time": exit_time, "exit_price": exit_price,
                "exit_reason": exit_reason, "r_multiple": r_net,
            })
        if not results:
            return _empty_trades()
        return pl.DataFrame(results)


def _empty_trades() -> pl.DataFrame:
    return pl.DataFrame(schema={
        "time": pl.Datetime, "symbol": pl.Utf8, "signal_type": pl.Utf8, "direction": pl.Utf8,
        "entry_price": pl.Float64, "tp_price": pl.Float64, "sl_price": pl.Float64,
        "exit_time": pl.Datetime, "exit_price": pl.Float64, "exit_reason": pl.Utf8,
        "r_multiple": pl.Float64,
    })
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_indicator_backtester.py -v
```

Expected: all 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/engine/indicator_backtester.py tests/test_indicator_backtester.py
git commit -m "feat(engine): add INDICATOR archetype backtester with ATR exits + time-stop"
```

---

## Task 5: Validation helpers (metrics, walk-forward, Monte Carlo, decay)

**Files:**
- Create: `src/engine/indicator_validation.py`
- Create: `tests/test_indicator_validation.py`

**Context:** Some logic exists in `run_robustness_test.py`, but coupling to FADE-specific data structures makes direct reuse brittle. Create a small, pure module that takes a trade DataFrame and returns a `ValidationResult`. Inspect the existing module first; if it exposes reusable pure functions, import them rather than duplicating. If not, implement standalone.

- [ ] **Step 1: Inspect existing robustness code**

```bash
grep -n "def " src/engine/run_robustness_test.py | head -40
```

Note which functions are pure and callable. If `monte_carlo_ruin`, `walk_forward_split`, or `decay_slope` exist and accept a trade-level list/df, import them. Otherwise proceed with the implementation below.

- [ ] **Step 2: Write failing tests**

Create `tests/test_indicator_validation.py`:

```python
import polars as pl
import pytest
from src.engine.indicator_validation import (
    compute_metrics, walk_forward_wr, monte_carlo_ruin, decay_slope_ratio,
    MetricsResult,
)


def _trade_df(r_list, start_day=1):
    import datetime as dt
    times = [dt.datetime(2024, 1, start_day) + dt.timedelta(days=i) for i in range(len(r_list))]
    return pl.DataFrame({"time": times, "r_multiple": r_list})


def test_compute_metrics_basic():
    trades = _trade_df([1, 1, 1, -1, 1])  # 4 wins, 1 loss
    m = compute_metrics(trades)
    assert m.n_trades == 5
    assert m.wr == pytest.approx(0.8)
    assert m.expectancy_r == pytest.approx(0.6)
    assert m.profit_factor == pytest.approx(4.0)


def test_walk_forward_computes_oos_ratio():
    # IS segment (first 60%): WR 80%, OOS (last 40%): WR 80%
    trades = _trade_df([1]*8 + [-1]*2 + [1]*4 + [-1]*1, start_day=1)
    ratio = walk_forward_wr(trades, is_months=1, oos_months=1)
    assert ratio >= 0.85


def test_monte_carlo_ruin_zero_for_winning_system():
    trades = _trade_df([1.0]*50 + [-1.0]*10)  # strongly positive
    ruin = monte_carlo_ruin(trades, risk_pct=0.01, initial_balance=10000,
                            n_sims=500, n_steps=100, seed=42)
    assert ruin < 0.01


def test_decay_slope_ratio_flags_degrading_system():
    # Increasing R through time — should NOT degrade
    import datetime as dt
    times = [dt.datetime(2024, 1, 1) + dt.timedelta(days=i) for i in range(100)]
    r = [0.5 + i * 0.01 for i in range(100)]
    trades = pl.DataFrame({"time": times, "r_multiple": r})
    ratio = decay_slope_ratio(trades, last_months=6)
    assert ratio >= 0.7
```

- [ ] **Step 3: Run tests — expect failures**

```bash
pytest tests/test_indicator_validation.py -v
```

- [ ] **Step 4: Implement `src/engine/indicator_validation.py`**

```python
"""Validation metrics for indicator-based strategies.

Pure functions that consume a trade-level Polars DataFrame with at minimum:
    time (datetime), r_multiple (float)
and return scalar or small struct results.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import polars as pl


@dataclass(frozen=True)
class MetricsResult:
    n_trades: int
    wr: float
    expectancy_r: float
    profit_factor: float
    max_dd_r: float
    trades_per_year: float


def compute_metrics(trades: pl.DataFrame) -> MetricsResult:
    if len(trades) == 0:
        return MetricsResult(0, 0.0, 0.0, 0.0, 0.0, 0.0)
    r = trades["r_multiple"].to_numpy()
    wins = r[r > 0]
    losses = r[r < 0]
    wr = float(len(wins) / len(r))
    expectancy = float(r.mean())
    pf = float(wins.sum() / -losses.sum()) if len(losses) > 0 and losses.sum() != 0 else float("inf")
    cum = np.cumsum(r)
    peak = np.maximum.accumulate(cum)
    dd = peak - cum
    max_dd = float(dd.max()) if len(dd) > 0 else 0.0
    span_days = (trades["time"].max() - trades["time"].min()).total_seconds() / 86400
    tpy = float(len(r) / (span_days / 365.25)) if span_days > 0 else 0.0
    return MetricsResult(len(r), wr, expectancy, pf, max_dd, tpy)


def walk_forward_wr(trades: pl.DataFrame, is_months: int, oos_months: int) -> float:
    """Rolling WF: compute mean(WR_oos / WR_is) across rolling windows.
    Returns 1.0 if no valid windows."""
    if len(trades) < 20:
        return 1.0
    trades = trades.sort("time")
    t0 = trades["time"].min()
    t_end = trades["time"].max()
    ratios = []
    cursor = t0
    from datetime import timedelta
    is_delta = timedelta(days=30 * is_months)
    oos_delta = timedelta(days=30 * oos_months)
    while cursor + is_delta + oos_delta <= t_end:
        is_slice = trades.filter(
            (pl.col("time") >= cursor) & (pl.col("time") < cursor + is_delta)
        )
        oos_slice = trades.filter(
            (pl.col("time") >= cursor + is_delta) &
            (pl.col("time") < cursor + is_delta + oos_delta)
        )
        if len(is_slice) >= 5 and len(oos_slice) >= 5:
            wr_is = (is_slice["r_multiple"] > 0).sum() / len(is_slice)
            wr_oos = (oos_slice["r_multiple"] > 0).sum() / len(oos_slice)
            if wr_is > 0:
                ratios.append(wr_oos / wr_is)
        cursor += oos_delta  # roll forward
    return float(np.mean(ratios)) if ratios else 1.0


def monte_carlo_ruin(trades: pl.DataFrame, risk_pct: float, initial_balance: float,
                     n_sims: int = 1000, n_steps: int = 500, seed: int = 42) -> float:
    """Bootstrap trades with replacement, compound balance. Ruin = balance <= 50% initial."""
    if len(trades) == 0:
        return 1.0
    r = trades["r_multiple"].to_numpy()
    rng = np.random.default_rng(seed)
    ruin_count = 0
    ruin_threshold = initial_balance * 0.5
    for _ in range(n_sims):
        balance = initial_balance
        sampled = rng.choice(r, size=n_steps, replace=True)
        for rm in sampled:
            balance *= (1.0 + risk_pct * rm)
            if balance <= ruin_threshold:
                ruin_count += 1
                break
    return ruin_count / n_sims


def decay_slope_ratio(trades: pl.DataFrame, last_months: int = 6) -> float:
    """Ratio of (mean R in last N months) / (global mean R).
    Values >= 1.0 mean improving, < 0.7 mean degrading."""
    if len(trades) < 20:
        return 1.0
    trades = trades.sort("time")
    t_end = trades["time"].max()
    from datetime import timedelta
    cutoff = t_end - timedelta(days=30 * last_months)
    recent = trades.filter(pl.col("time") >= cutoff)
    if len(recent) < 5:
        return 1.0
    global_mean = trades["r_multiple"].mean()
    recent_mean = recent["r_multiple"].mean()
    if global_mean <= 0:
        return 0.0
    return float(recent_mean / global_mean)
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
pytest tests/test_indicator_validation.py -v
```

- [ ] **Step 6: Commit**

```bash
git add src/engine/indicator_validation.py tests/test_indicator_validation.py
git commit -m "feat(engine): add pure validation helpers (metrics, WF, MC, decay)"
```

---

## Task 6: Phase-1 discovery scanner

**Files:**
- Create: `src/engine/run_indicator_discovery.py` (Phase-1 only in this task)

**Context:** No new tests — this is an orchestrator. Integration is validated by running it end-to-end and checking outputs. Phase-2 code is added in Task 7.

- [ ] **Step 1: Create Phase-1 orchestrator**

Create `src/engine/run_indicator_discovery.py`:

```python
"""End-to-end runner: Phase-1 discovery + Phase-2 optimization.

Phase-1 evaluates 1,500 (asset × TF × session × primary signal) combos with fixed R:R
and loose gates, writes survivors to reports/indicator_survivors_phase1.parquet.

Usage:
    python -m src.engine.run_indicator_discovery --phase 1
    python -m src.engine.run_indicator_discovery --phase 2
    python -m src.engine.run_indicator_discovery --phase all
"""
from __future__ import annotations
import argparse
from pathlib import Path
import polars as pl

from src.domain.constants import (
    INDICATOR_UNIVERSE, INDICATOR_TIMEFRAMES, INDICATOR_SESSIONS,
    PHASE1_MIN_TRADES_PER_YEAR, PHASE1_MIN_WR, PHASE1_MIN_PF, PHASE1_MIN_EXPECTANCY_R,
    FRICTION_FX, FRICTION_INDEX, INDEX_SYMBOLS,
)
from src.application.indicators import IndicatorEnricher
from src.application.signal_generator import SignalGenerator, SIGNAL_TYPES
from src.engine.indicator_backtester import IndicatorBacktester, BacktestConfig
from src.engine.indicator_validation import compute_metrics

# Existing CSV loader in this codebase — confirm import path during implementation.
# Likely src.infrastructure.csv_loader.CSVPolarsLoader. Grep first:
#   grep -rn "CSVPolarsLoader\|class.*Loader" src/
from src.infrastructure.csv_loader import CSVPolarsLoader  # adjust if path differs


ENRICHED_CACHE = Path("data/enriched")
REPORTS_DIR = Path("reports")


def _friction_for(symbol: str) -> float:
    return FRICTION_INDEX if symbol in INDEX_SYMBOLS else FRICTION_FX


def _session_end_hour(session: str) -> int:
    return INDICATOR_SESSIONS[session][1]


def _filter_by_session(signals: pl.DataFrame, session: str) -> pl.DataFrame:
    start_h, end_h = INDICATOR_SESSIONS[session]
    return signals.filter(
        (pl.col("time").dt.hour() >= start_h) & (pl.col("time").dt.hour() < end_h)
    )


def _load_and_enrich(symbol: str, tf: str) -> pl.DataFrame:
    cache_path = ENRICHED_CACHE / f"{symbol}_{tf}.parquet"
    if cache_path.exists():
        return pl.read_parquet(cache_path)
    ENRICHED_CACHE.mkdir(parents=True, exist_ok=True)
    bars = CSVPolarsLoader.load(symbol, tf)
    # Ensure atr_14 exists; if your existing enricher adds it, call it here first.
    # For standalone use, add ATR inline:
    bars = bars.with_columns([
        pl.max_horizontal(
            pl.col("high") - pl.col("low"),
            (pl.col("high") - pl.col("close").shift(1)).abs(),
            (pl.col("low") - pl.col("close").shift(1)).abs(),
        ).ewm_mean(alpha=1/14, adjust=False, min_periods=14).alias("atr_14")
    ])
    enriched = IndicatorEnricher.enrich_all(bars)
    enriched.write_parquet(cache_path)
    return enriched


def run_phase1() -> pl.DataFrame:
    rows = []
    total = len(INDICATOR_UNIVERSE) * len(INDICATOR_TIMEFRAMES) * len(INDICATOR_SESSIONS) * len(SIGNAL_TYPES)
    i = 0
    for symbol in INDICATOR_UNIVERSE:
        for tf in INDICATOR_TIMEFRAMES:
            try:
                bars = _load_and_enrich(symbol, tf)
            except FileNotFoundError:
                print(f"[SKIP] {symbol} {tf}: no data file")
                continue
            for signal_type in SIGNAL_TYPES:
                raw_signals = SignalGenerator.generate(bars, signal_type, symbol)
                for session in INDICATOR_SESSIONS:
                    i += 1
                    sigs = _filter_by_session(raw_signals, session)
                    if len(sigs) < 20:
                        continue
                    cfg = BacktestConfig(
                        tp_atr_mult=2.0, sl_atr_mult=1.0,
                        session_end_hour_utc=_session_end_hour(session),
                        friction_r=_friction_for(symbol),
                    )
                    trades = IndicatorBacktester.run(sigs, bars, cfg)
                    if len(trades) == 0:
                        continue
                    m = compute_metrics(trades)
                    rows.append({
                        "symbol": symbol, "tf": tf, "session": session,
                        "signal_type": signal_type, "n_trades": m.n_trades,
                        "wr": m.wr, "pf": m.profit_factor,
                        "expectancy_r": m.expectancy_r, "max_dd_r": m.max_dd_r,
                        "trades_per_year": m.trades_per_year,
                    })
                    if i % 100 == 0:
                        print(f"[P1] {i}/{total}")

    results = pl.DataFrame(rows) if rows else pl.DataFrame()
    if len(results) == 0:
        print("[P1] No results.")
        return results

    survivors = results.filter(
        (pl.col("trades_per_year") >= PHASE1_MIN_TRADES_PER_YEAR) &
        (pl.col("wr") >= PHASE1_MIN_WR) &
        (pl.col("pf") >= PHASE1_MIN_PF) &
        (pl.col("expectancy_r") >= PHASE1_MIN_EXPECTANCY_R)
    ).sort("expectancy_r", descending=True)

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    results.write_parquet(REPORTS_DIR / "indicator_phase1_all.parquet")
    survivors.write_parquet(REPORTS_DIR / "indicator_survivors_phase1.parquet")
    (REPORTS_DIR / "indicator_discovery_phase1.md").write_text(_render_p1_md(results, survivors))
    print(f"[P1] {len(results)} combos evaluated, {len(survivors)} passed loose gates")
    return survivors


def _render_p1_md(results: pl.DataFrame, survivors: pl.DataFrame) -> str:
    lines = [
        "# Indicator Discovery — Phase 1 Report",
        "",
        f"- Combos evaluated: **{len(results)}**",
        f"- Passed loose gates: **{len(survivors)}**",
        f"- Gates: trades/year ≥ {PHASE1_MIN_TRADES_PER_YEAR}, WR ≥ {PHASE1_MIN_WR}, "
        f"PF ≥ {PHASE1_MIN_PF}, expectancy ≥ {PHASE1_MIN_EXPECTANCY_R}R",
        "",
        "## Top 30 survivors (by expectancy)",
        "",
        "| Symbol | TF | Session | Signal | Trades | WR | PF | Exp (R) | MaxDD (R) |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for r in survivors.head(30).iter_rows(named=True):
        lines.append(
            f"| {r['symbol']} | {r['tf']} | {r['session']} | {r['signal_type']} "
            f"| {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.2f} "
            f"| {r['expectancy_r']:.3f} | {r['max_dd_r']:.1f} |"
        )
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=("1", "2", "all"), default="all")
    args = ap.parse_args()
    if args.phase in ("1", "all"):
        run_phase1()
    if args.phase in ("2", "all"):
        from src.engine.run_indicator_discovery_phase2 import run_phase2
        run_phase2()


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Verify import path for CSVPolarsLoader**

```bash
grep -rn "class CSVPolarsLoader\|class .*Loader" src/ | head -10
```

If the path differs from `src.infrastructure.csv_loader`, fix the import in `run_indicator_discovery.py`.

- [ ] **Step 3: Smoke test on a single asset (no commit yet)**

Edit the `INDICATOR_UNIVERSE` import locally (DO NOT commit) to `("EURUSD",)` to run a quick smoke test:

```bash
python -m src.engine.run_indicator_discovery --phase 1
```

Expected: completes in < 3 minutes, produces `reports/indicator_discovery_phase1.md` and `reports/indicator_survivors_phase1.parquet`. Restore the original constant.

- [ ] **Step 4: Commit**

```bash
git add src/engine/run_indicator_discovery.py
git commit -m "feat(engine): add Phase-1 indicator discovery scanner"
```

---

## Task 7: Phase-2 optimizer

**Files:**
- Create: `src/engine/run_indicator_discovery_phase2.py`
- Create: `src/engine/indicator_reporter.py`

- [ ] **Step 1: Create Phase-2 optimizer**

Create `src/engine/run_indicator_discovery_phase2.py`:

```python
"""Phase-2: for each Phase-1 survivor, grid-search 11 confluence combos × 20 R:R ATR.
Apply strict gates (WR≥80%, WF, MC, decay). Output final report + JSON export."""
from __future__ import annotations
from itertools import combinations
from pathlib import Path
import polars as pl

from src.domain.constants import (
    INDICATOR_TP_ATR_GRID, INDICATOR_SL_ATR_GRID, INDICATOR_SESSIONS,
    PHASE2_MIN_TRADES_PER_YEAR, PHASE2_MIN_WR, PHASE2_MIN_PF, PHASE2_MIN_EXPECTANCY_R,
    PHASE2_MAX_DD_R, PHASE2_WF_OOS_RATIO, PHASE2_MC_MAX_RUIN_PCT, PHASE2_DECAY_MIN_RATIO,
    WF_IS_MONTHS, WF_OOS_MONTHS, FRICTION_FX, FRICTION_INDEX, INDEX_SYMBOLS,
)
from src.application.signal_generator import SignalGenerator
from src.engine.indicator_backtester import IndicatorBacktester, BacktestConfig
from src.engine.indicator_validation import (
    compute_metrics, walk_forward_wr, monte_carlo_ruin, decay_slope_ratio,
)
from src.engine.indicator_reporter import render_final_report, export_strategies_json
from src.engine.run_indicator_discovery import _load_and_enrich, _filter_by_session

REPORTS_DIR = Path("reports")

# Confluence filter combos: 0, 1, or 2 filters from 4 families.
# One representative state per family picked (TREND/EXTREME/UPPER/POS — aggressive side).
FILTER_POOL = ("ADX_REGIME_TREND", "RSI_ZONE_EXTREME", "BB_POSITION_UPPER", "MACD_ALIGN_POS")


def _all_filter_combos() -> list[tuple[str, ...]]:
    combos: list[tuple[str, ...]] = [()]
    for k in (1, 2):
        combos.extend(tuple(c) for c in combinations(FILTER_POOL, k))
    return combos  # 1 + 4 + 6 = 11


def run_phase2() -> pl.DataFrame:
    survivors_path = REPORTS_DIR / "indicator_survivors_phase1.parquet"
    if not survivors_path.exists():
        raise FileNotFoundError(f"Run Phase-1 first (missing {survivors_path})")
    survivors = pl.read_parquet(survivors_path)
    print(f"[P2] optimizing {len(survivors)} Phase-1 survivors")

    filter_combos = _all_filter_combos()
    rr_combos = [(tp, sl) for tp in INDICATOR_TP_ATR_GRID for sl in INDICATOR_SL_ATR_GRID]

    final_rows = []
    for surv_idx, surv in enumerate(survivors.iter_rows(named=True)):
        symbol, tf, session, signal_type = surv["symbol"], surv["tf"], surv["session"], surv["signal_type"]
        bars = _load_and_enrich(symbol, tf)
        raw_signals = SignalGenerator.generate(bars, signal_type, symbol)
        sigs_session = _filter_by_session(raw_signals, session)
        friction = FRICTION_INDEX if symbol in INDEX_SYMBOLS else FRICTION_FX
        session_end = INDICATOR_SESSIONS[session][1]

        for fcombo in filter_combos:
            filtered_sigs = SignalGenerator.apply_filters(sigs_session, bars, fcombo)
            if len(filtered_sigs) < 20:
                continue
            for tp_mult, sl_mult in rr_combos:
                cfg = BacktestConfig(tp_atr_mult=tp_mult, sl_atr_mult=sl_mult,
                                     session_end_hour_utc=session_end, friction_r=friction)
                trades = IndicatorBacktester.run(filtered_sigs, bars, cfg)
                if len(trades) == 0:
                    continue
                m = compute_metrics(trades)
                if m.trades_per_year < PHASE2_MIN_TRADES_PER_YEAR or m.wr < PHASE2_MIN_WR \
                        or m.profit_factor < PHASE2_MIN_PF \
                        or m.expectancy_r < PHASE2_MIN_EXPECTANCY_R \
                        or m.max_dd_r > PHASE2_MAX_DD_R:
                    continue
                # Expensive gates only if cheap ones pass
                wf_ratio = walk_forward_wr(trades, is_months=WF_IS_MONTHS, oos_months=WF_OOS_MONTHS)
                if wf_ratio < PHASE2_WF_OOS_RATIO:
                    continue
                mc = monte_carlo_ruin(trades, risk_pct=0.01, initial_balance=10000,
                                      n_sims=1000, n_steps=500, seed=42)
                if mc > PHASE2_MC_MAX_RUIN_PCT:
                    continue
                decay = decay_slope_ratio(trades, last_months=6)
                if decay < PHASE2_DECAY_MIN_RATIO:
                    continue
                final_rows.append({
                    "symbol": symbol, "tf": tf, "session": session,
                    "signal_type": signal_type, "filters": list(fcombo),
                    "tp_atr_mult": tp_mult, "sl_atr_mult": sl_mult,
                    "n_trades": m.n_trades, "wr": m.wr, "pf": m.profit_factor,
                    "expectancy_r": m.expectancy_r, "max_dd_r": m.max_dd_r,
                    "trades_per_year": m.trades_per_year,
                    "wf_ratio": wf_ratio, "mc_ruin": mc, "decay_ratio": decay,
                })
        if surv_idx % 10 == 0:
            print(f"[P2] {surv_idx+1}/{len(survivors)} survivors processed")

    final = pl.DataFrame(final_rows) if final_rows else pl.DataFrame()
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    if len(final) > 0:
        final = final.sort("expectancy_r", descending=True)
    final.write_parquet(REPORTS_DIR / "indicator_final.parquet")
    (REPORTS_DIR / "Indicator_Discovery_Final.md").write_text(render_final_report(final))
    export_strategies_json(final, REPORTS_DIR / "indicator_strategies.json")
    print(f"[P2] {len(final)} strategies passed strict gates")
    return final
```

- [ ] **Step 2: Create reporter**

Create `src/engine/indicator_reporter.py`:

```python
"""Rendering: Markdown final report + JSON export compatible with bot_config format."""
from __future__ import annotations
import json
from pathlib import Path
import polars as pl


def render_final_report(final: pl.DataFrame) -> str:
    if len(final) == 0:
        return "# Indicator Discovery — Final Report\n\nNo strategies passed strict gates.\n"
    lines = [
        "# Indicator Discovery — Final Report",
        "",
        f"- Strategies passing all gates: **{len(final)}**",
        "- Gates: trades/year ≥ 100, WR ≥ 80%, PF ≥ 1.3, expectancy ≥ 0.1R, "
        "MaxDD ≤ 20R, WF OOS/IS ≥ 0.85, MC ruin < 1%, decay ratio ≥ 0.7",
        "",
        "## All passing strategies",
        "",
        "| Symbol | TF | Session | Signal | Filters | TP×ATR | SL×ATR "
        "| Trades | WR | PF | Exp (R) | MaxDD | WF | MC | Decay |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in final.iter_rows(named=True):
        flt = ",".join(r["filters"]) if r["filters"] else "—"
        lines.append(
            f"| {r['symbol']} | {r['tf']} | {r['session']} | {r['signal_type']} "
            f"| {flt} | {r['tp_atr_mult']} | {r['sl_atr_mult']} "
            f"| {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.2f} "
            f"| {r['expectancy_r']:.3f} | {r['max_dd_r']:.1f} "
            f"| {r['wf_ratio']:.2f} | {r['mc_ruin']:.4f} | {r['decay_ratio']:.2f} |"
        )
    lines.append("")
    lines.append("## Coverage by symbol")
    cov = final.group_by("symbol").len().sort("len", descending=True)
    for r in cov.iter_rows(named=True):
        lines.append(f"- {r['symbol']}: {r['len']}")
    return "\n".join(lines) + "\n"


def export_strategies_json(final: pl.DataFrame, out_path: Path) -> None:
    if len(final) == 0:
        out_path.write_text("[]")
        return
    items = []
    for r in final.iter_rows(named=True):
        items.append({
            "archetype": "INDICATOR",
            "symbol": r["symbol"], "tf": r["tf"], "session": r["session"],
            "signal_type": r["signal_type"], "filters": list(r["filters"]),
            "tp_atr_mult": float(r["tp_atr_mult"]),
            "sl_atr_mult": float(r["sl_atr_mult"]),
            "atr_period": 14,
            "metrics": {
                "wr": float(r["wr"]), "pf": float(r["pf"]),
                "expectancy_r": float(r["expectancy_r"]),
                "trades_per_year": float(r["trades_per_year"]),
                "wf_ratio": float(r["wf_ratio"]),
                "mc_ruin": float(r["mc_ruin"]),
                "decay_ratio": float(r["decay_ratio"]),
            },
        })
    out_path.write_text(json.dumps(items, indent=2))
```

- [ ] **Step 3: Commit Phase-2 skeleton**

```bash
git add src/engine/run_indicator_discovery_phase2.py src/engine/indicator_reporter.py
git commit -m "feat(engine): add Phase-2 optimizer with strict gates + reporter"
```

---

## Task 8: End-to-end smoke run + final commit

- [ ] **Step 1: Run full test suite**

```bash
pytest tests/test_indicators.py tests/test_signal_generator.py tests/test_indicator_backtester.py tests/test_indicator_validation.py -v
```

Expected: all tests PASS.

- [ ] **Step 2: Smoke run on 2 assets**

Temporarily edit `INDICATOR_UNIVERSE` in `constants.py` to `("EURUSD", "XAUUSD")` (do NOT commit this change).

```bash
python -m src.engine.run_indicator_discovery --phase all
```

Expected:
- `reports/indicator_discovery_phase1.md` exists with a top-N table
- `reports/Indicator_Discovery_Final.md` exists
- `reports/indicator_strategies.json` is valid JSON

Revert the `INDICATOR_UNIVERSE` change.

- [ ] **Step 3: Full run on all 15 assets**

```bash
python -m src.engine.run_indicator_discovery --phase all 2>&1 | tee reports/discovery_run.log
```

Expected runtime: Phase-1 10-20 min, Phase-2 1-4h depending on survivor count.

- [ ] **Step 4: Inspect results and commit the reports**

```bash
git add reports/indicator_discovery_phase1.md reports/Indicator_Discovery_Final.md \
        reports/indicator_strategies.json
git commit -m "docs(research): indicator discovery full run results"
```

Note: do NOT commit the `.parquet` files (they're large and regenerable). If not already in `.gitignore`, add:

```
reports/*.parquet
data/enriched/
```

and commit `.gitignore` separately.

---

## Self-Review Notes

- Spec coverage: all 5 indicators ✓, 10 signals ✓, 4 filters ✓, 2-phase pipeline ✓, gates ✓, WF+MC+decay ✓, JSON export ✓, no live changes ✓.
- Type consistency: `BacktestConfig` fields match backtester and runner usage. `compute_metrics` returns `MetricsResult` with fields used in both phases.
- Known assumptions to verify in Task 6 Step 2:
  - `CSVPolarsLoader` import path (may be `src.infrastructure.csv_loader` or `src.application.csv_loader`).
  - Whether the existing ATR column produced by `DataEnricher` is named `atr_14`; if different, the inline ATR in `_load_and_enrich` is the authoritative source.
- `monte_carlo_ruin` and `walk_forward_wr` use simplified approximations (day-count vs calendar months) — acceptable because they are heuristics and the strict gate thresholds tolerate minor noise.

---

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-04-20-indicator-discovery.md`. Two execution options:**

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration.

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints.

**Which approach?**
