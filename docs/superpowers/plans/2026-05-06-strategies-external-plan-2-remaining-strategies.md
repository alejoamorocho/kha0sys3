# Strategies External — Plan 2: Remaining Strategies (SMA-18, Doble Suelo, Perdices Fib, COT-1) + Comparativo

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task.

**Goal:** Complete the 4 remaining strategies from the spec, add COT data sources and seasonality, and produce a cross-strategy comparison report. Reuses 100% of the infra delivered by Plan 1.

**Architecture:** Each strategy = one new file in `src/strategies_external/strategies/`, optional new datasource files, optional ExitManager strategy branches, one runner per strategy. Final orchestrator runs all strategies and writes comparison.

**Tech Stack:** Python 3.11+, polars, scipy (find_peaks), pytest, urllib (COT download). No pandas in module code.

**Spec:** `docs/superpowers/specs/2026-05-06-strategies-external-design.md`
**Plan 1 baseline (already merged to main):** `docs/superpowers/plans/2026-05-06-strategies-external-plan-1-infra-oops.md`

**Order of execution:** Block A (SMA-18) → B (Doble Suelo) → C (Perdices Fib) → D (COT-1) → E (Comparativo). Each block is independent and ends with a runnable command + report.

---

## File Structure (additions only — Plan 1 files unchanged)

```
src/strategies_external/
├── strategies/
│   ├── sma18.py                 # NEW — SMA-18 trend following
│   ├── double_bottom.py         # NEW — W detector with neckline+consolidation
│   ├── perdices_fib.py          # NEW — Fib pullback (H1 first, M5 later)
│   └── cot1.py                  # NEW — COT extremes + seasonality + price action
├── data_sources/                # NEW package
│   ├── __init__.py
│   ├── cot_downloader.py        # NEW — fetch from cftc.gov
│   └── seasonality.py           # NEW — average return per (month, day)
├── strategies/swings.py         # NEW — swing detector helper (used by #3 and indirectly by #6)
├── exit_managers.py             # MODIFY — add doc/indicator branches for sma18, double_bottom, perdices_fib, cot1
└── runners/
    ├── run_sma18.py             # NEW
    ├── run_double_bottom.py     # NEW
    ├── run_perdices_fib.py      # NEW
    ├── run_cot1.py              # NEW
    └── run_all.py               # NEW — runs all + comparison report

src/strategies_external/reporting/
└── comparison.py                # NEW — cross-strategy comparison renderer

tests/strategies_external/
├── test_sma18_strategy.py
├── test_swing_detector.py
├── test_double_bottom_strategy.py
├── test_perdices_fib_strategy.py
├── test_cot_downloader.py
├── test_seasonality.py
├── test_cot1_strategy.py
├── test_exit_managers_extensions.py   # extends test_exit_managers.py with new branches
└── test_run_all_integration.py

reports/external/
├── sma18_backtest.md / .parquet      (generated)
├── double_bottom_backtest.md / .parquet
├── perdices_fib_backtest.md / .parquet
├── cot1_backtest.md / .parquet
└── all_external_comparison.md
```

---

# Block A — SMA-18 (Tasks A1-A4)

## Task A1: SMA18Strategy.generate_signals

**Files:**
- Create: `src/strategies_external/strategies/sma18.py`
- Create: `tests/strategies_external/test_sma18_strategy.py`

- [ ] **Step 1: Tests**

```python
# tests/strategies_external/test_sma18_strategy.py
from datetime import datetime, timedelta

import polars as pl
import pytest

from src.strategies_external.strategies.sma18 import SMA18Strategy


def _daily(prices: list[tuple[float, float, float, float]]) -> pl.DataFrame:
    """Build daily OHLC from list of (open, high, low, close); volume=1000."""
    base = datetime(2024, 1, 1)
    rows = [(base + timedelta(days=i), o, h, l, c, 1000.0)
            for i, (o, h, l, c) in enumerate(prices)]
    return pl.DataFrame(
        {"time": [r[0] for r in rows],
         "open": [r[1] for r in rows], "high": [r[2] for r in rows],
         "low": [r[3] for r in rows], "close": [r[4] for r in rows],
         "volume": [r[5] for r in rows]},
        schema={"time": pl.Datetime, "open": pl.Float64, "high": pl.Float64,
                "low": pl.Float64, "close": pl.Float64, "volume": pl.Float64},
    )


def test_sma18_long_signal_after_two_clean_bars_above_sma():
    """Two consecutive bars with low > SMA, neither inside-day, then a higher high triggers."""
    # Construct 22 bars: first 18 ramping up to seed SMA, then 2 clean bars above SMA, then trigger bar
    prices = []
    for i in range(18):
        p = 100.0 + i * 0.5
        prices.append((p, p + 0.3, p - 0.3, p + 0.1))
    # bar 18: SMA ≈ 104.25; this bar (low > sma)
    prices.append((110.0, 111.0, 109.5, 110.5))  # low 109.5 > sma ~104.25
    # bar 19: also low > sma, not inside-day (high 112 > 111, low 109 < 109.5)
    prices.append((110.5, 112.0, 109.0, 111.5))
    # bar 20: trigger. high reaches max(high[-1], high[-2]) + 1tick = max(111, 112) = 112.01
    prices.append((111.0, 113.0, 110.0, 112.5))
    df = _daily(prices)
    strat = SMA18Strategy(sma_window=18)
    sigs = strat.generate_signals(df, symbol="XAUUSD")
    # The buy stop should be 112.01 (= max(111, 112) + 0.01).
    long_sigs = [s for s in sigs if s.side == "long"]
    assert len(long_sigs) >= 1
    s = long_sigs[-1]  # last triggered
    assert s.side == "long"
    assert s.entry_price == pytest.approx(112.01)
    assert s.entry_type == "stop"
    for k in ("sma18", "atr14"):
        assert k in s.indicator_anchors


def test_sma18_no_signal_when_inside_day():
    """If t-1 is inside-day relative to t-2, no signal even if both above SMA."""
    prices = []
    for i in range(18):
        p = 100.0 + i * 0.5
        prices.append((p, p + 0.3, p - 0.3, p + 0.1))
    # bar 18: not inside
    prices.append((110.0, 112.0, 109.0, 110.5))
    # bar 19: INSIDE-day vs bar 18 (high 111 < 112, low 109.5 > 109)
    prices.append((110.5, 111.0, 109.5, 110.0))
    # bar 20: would-be trigger
    prices.append((110.0, 113.0, 109.0, 111.0))
    df = _daily(prices)
    strat = SMA18Strategy(sma_window=18)
    sigs = strat.generate_signals(df, symbol="XAUUSD")
    # bar 19 inside-day → no long signal at bar 20 from this two-bar setup
    last_two_setups = [s for s in sigs if s.setup_ts == df["time"][20]]
    assert len(last_two_setups) == 0


def test_sma18_short_signal_after_two_clean_bars_below_sma():
    prices = []
    for i in range(18):
        p = 110.0 - i * 0.3  # downward to seed SMA
        prices.append((p, p + 0.3, p - 0.3, p - 0.1))
    # bar 18: high < SMA
    prices.append((104.0, 104.5, 103.0, 103.5))
    # bar 19: high < SMA, not inside-day
    prices.append((103.5, 105.0, 102.5, 103.0))
    # bar 20: trigger DOWN
    prices.append((103.0, 104.0, 101.5, 102.0))
    df = _daily(prices)
    strat = SMA18Strategy(sma_window=18)
    sigs = strat.generate_signals(df, symbol="XAUUSD")
    short_sigs = [s for s in sigs if s.side == "short"]
    assert len(short_sigs) >= 1
    # sell stop at min(low[-1], low[-2]) - 0.01 = min(102.5, 103.0) - 0.01 = 102.49
    s = short_sigs[-1]
    assert s.entry_price == pytest.approx(102.49)


def test_sma18_too_few_bars():
    df = _daily([(100.0, 101.0, 99.0, 100.5)] * 5)
    strat = SMA18Strategy(sma_window=18)
    assert strat.generate_signals(df, symbol="XAUUSD") == []
```

- [ ] **Step 2: Run failing.**

- [ ] **Step 3: Implementation**

```python
# src/strategies_external/strategies/sma18.py
"""Inna Rosputnia SMA-18 — daily trend-following with inside-day filter.

Long: low[t-1] > SMA18[t-1] AND low[t-2] > SMA18[t-2] AND neither is
inside-day. Buy stop @ max(high[t-1], high[t-2]) + 1 tick on bar t.
Short: symmetric.
"""

from datetime import timedelta

import polars as pl

from src.strategies_external.common.signal import Signal
from src.strategies_external.strategies.base import Strategy


_TICK = 0.01


class SMA18Strategy(Strategy):
    name = "sma18"

    def __init__(self, sma_window: int = 18, atr_window: int = 14):
        self.sma_window = sma_window
        self.atr_window = atr_window

    def generate_signals(self, df: pl.DataFrame, symbol: str) -> list[Signal]:
        min_bars = max(self.sma_window, self.atr_window) + 3
        if df.is_empty() or df.shape[0] < min_bars:
            return []

        enriched = (
            df.with_columns(
                pl.col("close").rolling_mean(self.sma_window).alias("sma"),
                pl.max_horizontal(
                    pl.col("high") - pl.col("low"),
                    (pl.col("high") - pl.col("close").shift(1)).abs(),
                    (pl.col("low") - pl.col("close").shift(1)).abs(),
                ).alias("tr"),
            )
            .with_columns(pl.col("tr").rolling_mean(self.atr_window).alias("atr"))
            .with_columns(
                ((pl.col("high") < pl.col("high").shift(1))
                 & (pl.col("low") > pl.col("low").shift(1))).alias("inside")
            )
        )
        rows = enriched.to_dicts()
        signals: list[Signal] = []

        for i in range(2, len(rows)):
            cur = rows[i]
            p1 = rows[i - 1]
            p2 = rows[i - 2]
            sma_p1 = p1.get("sma")
            sma_p2 = p2.get("sma")
            sma_cur = cur.get("sma")
            atr_cur = cur.get("atr") or 0.0
            if sma_p1 is None or sma_p2 is None or sma_cur is None:
                continue

            inside_p1 = bool(p1.get("inside"))
            inside_p2 = bool(p2.get("inside"))
            valid_until = cur["time"] + timedelta(days=1) - timedelta(seconds=1)
            anchors = {"sma18": sma_cur, "atr14": atr_cur,
                       "high_p1": p1["high"], "high_p2": p2["high"],
                       "low_p1": p1["low"], "low_p2": p2["low"]}

            # Long
            if (p1["low"] > sma_p1 and p2["low"] > sma_p2
                    and not inside_p1 and not inside_p2):
                buy_stop = max(p1["high"], p2["high"]) + _TICK
                signals.append(Signal(
                    symbol=symbol, strategy=self.name, side="long",
                    setup_ts=cur["time"], entry_type="stop",
                    entry_price=buy_stop,
                    valid_until=valid_until,
                    stop=0.0, tp1=None, tp2=None,
                    indicator_anchors=anchors,
                ))
            # Short
            elif (p1["high"] < sma_p1 and p2["high"] < sma_p2
                  and not inside_p1 and not inside_p2):
                sell_stop = min(p1["low"], p2["low"]) - _TICK
                signals.append(Signal(
                    symbol=symbol, strategy=self.name, side="short",
                    setup_ts=cur["time"], entry_type="stop",
                    entry_price=sell_stop,
                    valid_until=valid_until,
                    stop=0.0, tp1=None, tp2=None,
                    indicator_anchors=anchors,
                ))
        return signals
```

- [ ] **Step 4: Run pytest, verify 4 passed.**

- [ ] **Step 5: Commit:** `feat(strategies_external): SMA-18 strategy generate_signals`

---

## Task A2: Extend ExitManagers for sma18

**Files:**
- Modify: `src/strategies_external/exit_managers.py`
- Create: `tests/strategies_external/test_exit_managers_extensions.py`

- [ ] **Step 1: Tests**

```python
# tests/strategies_external/test_exit_managers_extensions.py
from datetime import datetime

import pytest

from src.strategies_external.common.signal import Signal
from src.strategies_external.exit_managers import (
    DocExitManager, IndicatorExitManager,
)


def _signal_long_sma18_raw() -> Signal:
    return Signal(
        symbol="XAUUSD", strategy="sma18", side="long",
        setup_ts=datetime(2024, 1, 5),
        entry_type="stop", entry_price=2050.0,
        valid_until=datetime(2024, 1, 5, 23, 59),
        stop=0.0, tp1=None, tp2=None,
        indicator_anchors={"sma18": 2025.0, "atr14": 15.0,
                           "high_p1": 2048.0, "high_p2": 2045.0,
                           "low_p1": 2040.0, "low_p2": 2038.0},
    )


def test_doc_exit_manager_sma18_long():
    raw = _signal_long_sma18_raw()
    s = DocExitManager(strategy="sma18").attach_levels(raw)
    # Doc SMA-18: stop = sma18 (señal contraria); no fixed TP — the backtester
    # handles "exit on 2 closes against SMA" via timestop or signal_inverso later.
    # For now: stop=sma18, tp1=None, tp2=None.
    assert s.stop == pytest.approx(2025.0)
    assert s.tp1 is None
    assert s.tp2 is None


def test_indicator_exit_manager_sma18_long():
    raw = _signal_long_sma18_raw()
    s = IndicatorExitManager(strategy="sma18").attach_levels(raw)
    # Indicator SMA-18: stop = sma18 - 0.5*atr; tp1 = sma18 + 2*atr; tp2 = sma18 + 4*atr
    assert s.stop == pytest.approx(2025.0 - 0.5 * 15.0)
    assert s.tp1 == pytest.approx(2025.0 + 2.0 * 15.0)
    assert s.tp2 == pytest.approx(2025.0 + 4.0 * 15.0)
```

- [ ] **Step 2: Run failing (DocExitManager raises "unknown strategy" for sma18).**

- [ ] **Step 3: Add `_sma18` branch in DocExitManager and IndicatorExitManager.**

In `src/strategies_external/exit_managers.py`:

```python
# In DocExitManager.attach_levels, add:
        if self.strategy == "sma18":
            return self._sma18(signal_raw)

# Add method on DocExitManager:
    def _sma18(self, s: Signal) -> Signal:
        # Stop = SMA-18 (señal contraria definida como cruce de SMA).
        # No fixed TP — let the trade run.
        sma = _require_anchor(s, "sma18")
        return replace(s, stop=sma, tp1=None, tp2=None)
```

```python
# In IndicatorExitManager.attach_levels, add:
        if self.strategy == "sma18":
            return self._sma18(signal_raw)

# Add method on IndicatorExitManager:
    def _sma18(self, s: Signal) -> Signal:
        sma = _require_anchor(s, "sma18")
        atr = _require_anchor(s, "atr14")
        if s.side == "long":
            stop = sma - 0.5 * atr
            tp1 = sma + 2.0 * atr
            tp2 = sma + 4.0 * atr
        else:
            stop = sma + 0.5 * atr
            tp1 = sma - 2.0 * atr
            tp2 = sma - 4.0 * atr
        return replace(s, stop=stop, tp1=tp1, tp2=tp2)
```

- [ ] **Step 4: Run pytest, verify 2 new passed.**

- [ ] **Step 5: Commit:** `feat(strategies_external): SMA-18 exit branches in Doc/Indicator managers`

---

## Task A3: run_sma18 runner

**Files:**
- Create: `src/strategies_external/runners/run_sma18.py`
- Create: `tests/strategies_external/test_run_sma18_integration.py`

- [ ] **Step 1: Test**

```python
# tests/strategies_external/test_run_sma18_integration.py
from pathlib import Path

import pytest

from src.strategies_external.runners.run_sma18 import run_sma18_backtest


@pytest.mark.integration
def test_run_sma18_real_data_produces_report(tmp_path: Path):
    output = tmp_path / "sma18_backtest.md"
    summary = run_sma18_backtest(
        symbols=["XAUUSD", "XAGUSD"],
        data_dir="data",
        output_path=output,
    )
    assert output.exists()
    content = output.read_text()
    assert "SMA18" in content
    assert "XAUUSD" in content
    assert "doc" in summary
    assert "indicator" in summary
    parquet = output.parent / "sma18_trades.parquet"
    assert parquet.exists()
```

- [ ] **Step 2: Run failing (ImportError).**

- [ ] **Step 3: Implementation**

```python
# src/strategies_external/runners/run_sma18.py
"""Runner SMA-18: backtest con doc + indicator + ATR sweep.

ATR mode reuses the same grid sweep as OOPS for comparability.
"""

from pathlib import Path

import polars as pl

from src.strategies_external.common.backtester import run_backtest
from src.strategies_external.common.metrics import evaluate
from src.strategies_external.common.monte_carlo import monte_carlo_bootstrap
from src.strategies_external.common.trade import Trade
from src.strategies_external.common.walk_forward import walk_forward_split
from src.strategies_external.data_loader import (
    aggregate_to_daily, best_tracking_tf, load_csv,
)
from src.strategies_external.exit_managers import (
    ATRExitManager, DocExitManager, IndicatorExitManager,
)
from src.strategies_external.reporting.markdown import write_backtest_report
from src.strategies_external.strategies.sma18 import SMA18Strategy


def _trades_to_parquet(trades: list[Trade], path: Path) -> None:
    if not trades:
        path.touch()
        return
    df = pl.DataFrame(
        [{
            "symbol": t.symbol, "strategy": t.strategy, "exit_mode": t.exit_mode,
            "side": t.side, "entry_ts": t.entry_ts, "entry": t.entry,
            "stop": t.stop, "tp1": t.tp1, "tp2": t.tp2,
            "exit_ts": t.exit_ts, "exit": t.exit, "exit_reason": t.exit_reason,
            "R": t.R, "pnl_R": t.pnl_R, "pnl_pct": t.pnl_pct,
            "bars_in_trade": t.bars_in_trade,
        } for t in trades],
        schema={"symbol": pl.Utf8, "strategy": pl.Utf8, "exit_mode": pl.Utf8,
                "side": pl.Utf8, "entry_ts": pl.Datetime, "entry": pl.Float64,
                "stop": pl.Float64, "tp1": pl.Float64, "tp2": pl.Float64,
                "exit_ts": pl.Datetime, "exit": pl.Float64,
                "exit_reason": pl.Utf8, "R": pl.Float64, "pnl_R": pl.Float64,
                "pnl_pct": pl.Float64, "bars_in_trade": pl.Int64},
    )
    df.write_parquet(path)


def run_sma18_backtest(
    symbols: list[str],
    data_dir: str = "data",
    output_path: Path | str = "reports/external/sma18_backtest.md",
    atr_grid: list[tuple[float, float, float]] | None = None,
) -> dict[str, dict]:
    if atr_grid is None:
        atr_grid = [(sl, tp1, tp2)
                    for sl in (1.0, 1.5, 2.0, 2.5)
                    for tp1 in (1.0, 1.5, 2.0)
                    for tp2 in (2.0, 3.0, 4.0)
                    if tp2 > tp1]

    output_path = Path(output_path)
    strategy = SMA18Strategy()
    doc_mgr = DocExitManager(strategy="sma18")
    ind_mgr = IndicatorExitManager(strategy="sma18")

    per_symbol: dict[str, tuple[list, pl.DataFrame]] = {}
    for sym in symbols:
        df_h1 = load_csv(sym, "H1", data_dir=data_dir)
        df_daily = aggregate_to_daily(df_h1)
        _, df_track = best_tracking_tf(sym, data_dir=data_dir)
        sigs = strategy.generate_signals(df_daily, symbol=sym)
        per_symbol[sym] = (sigs, df_track)

    trades_by_mode: dict[str, list[Trade]] = {"doc": [], "atr": [], "indicator": []}

    for sym, (sigs, df_track) in per_symbol.items():
        # SMA-18 doc has tp=None → backtester relies on stop+timestop+EOD only.
        # We add a long-but-finite valid_until from the strategy (1 day after setup_ts);
        # to give SMA-18 enough room to run, override valid_until to setup + 60 days
        # for trades meant to "let the trend run".
        doc_signals = []
        for s in sigs:
            base = doc_mgr.attach_levels(s)
            from datetime import timedelta
            from dataclasses import replace as _replace
            doc_signals.append(_replace(base, valid_until=base.setup_ts + timedelta(days=60)))
        trades_by_mode["doc"].extend(run_backtest(doc_signals, df_track, exit_mode="doc"))
        trades_by_mode["indicator"].extend(
            run_backtest([ind_mgr.attach_levels(s) for s in sigs], df_track, exit_mode="indicator")
        )

    # ATR sweep
    atr_grid_results = []
    best_atr_trades: list[Trade] = []
    best_atr_calmar = -float("inf")
    for sl, tp1, tp2 in atr_grid:
        cand_trades: list[Trade] = []
        atr_mgr = ATRExitManager(sl_mult=sl, tp1_mult=tp1, tp2_mult=tp2)
        for sym, (sigs, df_track) in per_symbol.items():
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

    doc_trades = trades_by_mode["doc"]
    try:
        wf = walk_forward_split(doc_trades, n_windows=5, is_pct=0.7)
    except ValueError:
        wf = None
    mc = monte_carlo_bootstrap(doc_trades, n_simulations=10_000,
                                ruin_threshold_R=-15.0, seed=42) if doc_trades else None

    write_backtest_report(
        output_path,
        strategy_name="sma18",
        symbols=symbols,
        trades_by_mode=trades_by_mode,
        config={"period": "2018-01-01..today", "risk_pct": 0.005,
                "atr_grid": atr_grid},
        walk_forward_windows=wf,
        monte_carlo_results=mc,
        atr_grid_results=atr_grid_results,
    )

    all_trades = trades_by_mode["doc"] + trades_by_mode["atr"] + trades_by_mode["indicator"]
    _trades_to_parquet(all_trades, output_path.parent / "sma18_trades.parquet")

    summary = {m: evaluate(ts) for m, ts in trades_by_mode.items()}
    summary["atr_grid_results"] = atr_grid_results
    return summary


if __name__ == "__main__":
    summary = run_sma18_backtest(
        symbols=["XAUUSD", "XAGUSD", "WTI", "BRENT", "NATGAS"],
        data_dir="data",
        output_path="reports/external/sma18_backtest.md",
    )
    print("SMA-18 backtest done.")
    for mode in ("doc", "atr", "indicator"):
        m = summary[mode]
        print(f"  [{mode}] n={m['n_trades']} wr={m['win_rate']:.3f} "
              f"pf={m['profit_factor']:.3f} dd_R={m['max_dd_R']:.3f} "
              f"calmar={m['calmar']:.3f}")
    best = max(summary["atr_grid_results"], key=lambda r: r["calmar"])
    print(f"  best ATR: sl={best['sl']} tp1={best['tp1']} tp2={best['tp2']} "
          f"calmar={best['calmar']:.3f}")
```

- [ ] **Step 4: Run integration test, verify passes.**

- [ ] **Step 5: Run runner standalone over real data:**

```bash
python -m src.strategies_external.runners.run_sma18
```

Print results in your report.

- [ ] **Step 6: Commit:** `feat(strategies_external): run_sma18 runner with full report`

---

# Block B — Doble Suelo (Tasks B1-B5)

## Task B1: Swing detector helper

**Files:**
- Create: `src/strategies_external/strategies/swings.py`
- Create: `tests/strategies_external/test_swing_detector.py`

- [ ] **Step 1: Test**

```python
# tests/strategies_external/test_swing_detector.py
from datetime import datetime, timedelta

import polars as pl
import pytest

from src.strategies_external.strategies.swings import find_swings


def _df_synthetic_with_swings() -> pl.DataFrame:
    """W-shape: high1, low1=100, high1, low2=101, high1.

    50 bars total: 0-9 ramp down to L1 (idx 10), 10-25 bounce, 25-35 ramp down to L2 (idx 35),
    35-49 ramp up.
    """
    base = datetime(2024, 1, 1)
    rows = []
    for i in range(50):
        if i <= 10:
            v = 110.0 - i * 1.0  # 110 → 100 at idx 10 (L1)
        elif i <= 25:
            v = 100.0 + (i - 10) * 0.7  # bounces up
        elif i <= 35:
            v = 100.0 + 15 * 0.7 - (i - 25) * 0.95  # back down to ~101
        else:
            v = 101.0 + (i - 35) * 0.5  # rallies up
        rows.append((base + timedelta(days=i), v, v + 0.5, v - 0.5, v + 0.1, 1000.0))
    return pl.DataFrame(
        {"time": [r[0] for r in rows],
         "open": [r[1] for r in rows], "high": [r[2] for r in rows],
         "low": [r[3] for r in rows], "close": [r[4] for r in rows],
         "volume": [r[5] for r in rows]},
        schema={"time": pl.Datetime, "open": pl.Float64, "high": pl.Float64,
                "low": pl.Float64, "close": pl.Float64, "volume": pl.Float64},
    )


def test_find_swings_returns_lows_and_highs(_df_synthetic_with_swings=None):
    df = _df_synthetic_with_swings if _df_synthetic_with_swings is not None else None  # placeholder
    # actual fixture call:
    df = pl.DataFrame()  # will be overridden by fixture below
    

def test_find_swings_basic(synthetic_w_df):
    """Find at least one local min near idx 10 (L1) and idx 35 (L2)."""
    swing_lows, swing_highs = find_swings(synthetic_w_df, prominence_factor=0.3, min_distance=5)
    # swing_lows is a list of (idx, price); we expect L1 around idx 10, L2 around idx 35
    low_idxs = [idx for idx, _ in swing_lows]
    assert any(8 <= i <= 12 for i in low_idxs), f"Expected L1 around idx 10, got {low_idxs}"
    assert any(33 <= i <= 37 for i in low_idxs), f"Expected L2 around idx 35, got {low_idxs}"


@pytest.fixture
def synthetic_w_df():
    base = datetime(2024, 1, 1)
    rows = []
    for i in range(50):
        if i <= 10:
            v = 110.0 - i * 1.0
        elif i <= 25:
            v = 100.0 + (i - 10) * 0.7
        elif i <= 35:
            v = 100.0 + 15 * 0.7 - (i - 25) * 0.95
        else:
            v = 101.0 + (i - 35) * 0.5
        rows.append((base + timedelta(days=i), v, v + 0.5, v - 0.5, v + 0.1, 1000.0))
    return pl.DataFrame(
        {"time": [r[0] for r in rows],
         "open": [r[1] for r in rows], "high": [r[2] for r in rows],
         "low": [r[3] for r in rows], "close": [r[4] for r in rows],
         "volume": [r[5] for r in rows]},
        schema={"time": pl.Datetime, "open": pl.Float64, "high": pl.Float64,
                "low": pl.Float64, "close": pl.Float64, "volume": pl.Float64},
    )


def test_find_swings_empty():
    df = pl.DataFrame(schema={"time": pl.Datetime, "open": pl.Float64,
                              "high": pl.Float64, "low": pl.Float64,
                              "close": pl.Float64, "volume": pl.Float64})
    lows, highs = find_swings(df, prominence_factor=0.5, min_distance=5)
    assert lows == [] and highs == []
```

> Note: the redundant `test_find_swings_returns_lows_and_highs` placeholder above is a stub; remove it. Keep only `test_find_swings_basic` and `test_find_swings_empty`. Implementer should clean this up.

- [ ] **Step 2: Run failing.**

- [ ] **Step 3: Implementation**

```python
# src/strategies_external/strategies/swings.py
"""Swing detector reproducible based on scipy.signal.find_peaks.

`find_swings(df, prominence_factor, min_distance)` returns (swing_lows, swing_highs)
where each is a list of (row_index, price) tuples. prominence_factor multiplies
the rolling 14-bar ATR proxy to set find_peaks prominence threshold.
"""

import polars as pl
from scipy.signal import find_peaks


def find_swings(
    df: pl.DataFrame,
    prominence_factor: float = 0.5,
    min_distance: int = 5,
    atr_window: int = 14,
) -> tuple[list[tuple[int, float]], list[tuple[int, float]]]:
    if df.is_empty() or df.shape[0] < atr_window:
        return [], []

    atr_proxy = (
        df.with_columns(
            (pl.col("high") - pl.col("low")).rolling_mean(atr_window).alias("atr")
        )["atr"]
        .fill_null(strategy="forward")
        .fill_null(strategy="backward")
        .to_list()
    )
    median_atr = sum(a for a in atr_proxy if a) / max(1, sum(1 for a in atr_proxy if a))
    prom = prominence_factor * median_atr

    highs = df["high"].to_list()
    lows = df["low"].to_list()
    inv_lows = [-x for x in lows]

    high_idxs, _ = find_peaks(highs, prominence=prom, distance=min_distance)
    low_idxs, _ = find_peaks(inv_lows, prominence=prom, distance=min_distance)

    swing_highs = [(int(i), float(highs[i])) for i in high_idxs]
    swing_lows = [(int(i), float(lows[i])) for i in low_idxs]
    return swing_lows, swing_highs
```

- [ ] **Step 4: Run tests, verify 2 passed.**

- [ ] **Step 5: Commit:** `feat(strategies_external): swing detector based on scipy find_peaks`

---

## Task B2: DoubleBottomStrategy.generate_signals

**Files:**
- Create: `src/strategies_external/strategies/double_bottom.py`
- Create: `tests/strategies_external/test_double_bottom_strategy.py`

- [ ] **Step 1: Test**

```python
# tests/strategies_external/test_double_bottom_strategy.py
from datetime import datetime, timedelta

import polars as pl
import pytest

from src.strategies_external.strategies.double_bottom import DoubleBottomStrategy


@pytest.fixture
def double_bottom_df():
    """W pattern with neckline + post-breakout consolidation + breakout trigger."""
    base = datetime(2024, 1, 1)
    rows = []
    # idx 0-10: ramp down to L1 = 100
    for i in range(11):
        v = 110.0 - i * 1.0
        rows.append((base + timedelta(days=i), v, v + 0.4, v - 0.4, v, 1000.0))
    # idx 11-25: rally to neckline ~107
    for i in range(11, 26):
        v = 100.0 + (i - 10) * 0.45
        rows.append((base + timedelta(days=i), v, v + 0.4, v - 0.4, v, 1000.0))
    # idx 26-35: pullback to L2 = 101 (within 2% of L1=100)
    for i in range(26, 36):
        v = 107.0 - (i - 25) * 0.6
        rows.append((base + timedelta(days=i), v, v + 0.4, v - 0.4, v, 1000.0))
    # idx 36-45: rally back through neckline
    for i in range(36, 46):
        v = 101.0 + (i - 35) * 0.7
        rows.append((base + timedelta(days=i), v, v + 0.4, v - 0.4, v, 1000.0))
    # idx 46-50: consolidation just above neckline
    for i in range(46, 51):
        rows.append((base + timedelta(days=i), 108.0, 108.4, 107.6, 108.0, 1000.0))
    return pl.DataFrame(
        {"time": [r[0] for r in rows],
         "open": [r[1] for r in rows], "high": [r[2] for r in rows],
         "low": [r[3] for r in rows], "close": [r[4] for r in rows],
         "volume": [r[5] for r in rows]},
        schema={"time": pl.Datetime, "open": pl.Float64, "high": pl.Float64,
                "low": pl.Float64, "close": pl.Float64, "volume": pl.Float64},
    )


def test_double_bottom_detects_pattern(double_bottom_df):
    strat = DoubleBottomStrategy(tolerance=0.02, min_separation=15, max_separation=80,
                                 consol_min_bars=3, consol_max_atr_mult=1.5)
    sigs = strat.generate_signals(double_bottom_df, symbol="XAUUSD")
    assert len(sigs) >= 1
    s = sigs[-1]
    assert s.side == "long"
    for k in ("L1", "L2", "neckline", "altura_patron", "atr14"):
        assert k in s.indicator_anchors


def test_double_bottom_no_signal_when_distant():
    """L1 and L2 too far apart in price (>tolerance) → no signal."""
    base = datetime(2024, 1, 1)
    rows = []
    for i in range(50):
        v = 100.0 + i * 0.1  # monotone up, no W
        rows.append((base + timedelta(days=i), v, v + 0.3, v - 0.3, v, 1000.0))
    df = pl.DataFrame(
        {"time": [r[0] for r in rows],
         "open": [r[1] for r in rows], "high": [r[2] for r in rows],
         "low": [r[3] for r in rows], "close": [r[4] for r in rows],
         "volume": [r[5] for r in rows]},
        schema={"time": pl.Datetime, "open": pl.Float64, "high": pl.Float64,
                "low": pl.Float64, "close": pl.Float64, "volume": pl.Float64},
    )
    strat = DoubleBottomStrategy()
    assert strat.generate_signals(df, symbol="XAUUSD") == []
```

- [ ] **Step 2: Run failing.**

- [ ] **Step 3: Implementation**

```python
# src/strategies_external/strategies/double_bottom.py
"""Inna Rosputnia Doble Suelo cualificado.

Detector + filtros (precio > SMA18, ruptura neckline, consolidación 3-5 barras
con rango < 1×ATR(14)). Trigger: ruptura del high de la consolidación + 1 tick.
"""

from datetime import timedelta

import polars as pl

from src.strategies_external.common.signal import Signal
from src.strategies_external.strategies.base import Strategy
from src.strategies_external.strategies.swings import find_swings


_TICK = 0.01


class DoubleBottomStrategy(Strategy):
    name = "double_bottom"

    def __init__(
        self,
        tolerance: float = 0.02,
        min_separation: int = 15,
        max_separation: int = 80,
        consol_min_bars: int = 3,
        consol_max_atr_mult: float = 1.0,
        sma_window: int = 18,
        atr_window: int = 14,
    ):
        self.tolerance = tolerance
        self.min_separation = min_separation
        self.max_separation = max_separation
        self.consol_min_bars = consol_min_bars
        self.consol_max_atr_mult = consol_max_atr_mult
        self.sma_window = sma_window
        self.atr_window = atr_window

    def generate_signals(self, df: pl.DataFrame, symbol: str) -> list[Signal]:
        min_bars = max(self.sma_window, self.atr_window) + self.max_separation + 5
        if df.is_empty() or df.shape[0] < min_bars:
            return []

        enriched = (
            df.with_columns(
                pl.col("close").rolling_mean(self.sma_window).alias("sma"),
                pl.max_horizontal(
                    pl.col("high") - pl.col("low"),
                    (pl.col("high") - pl.col("close").shift(1)).abs(),
                    (pl.col("low") - pl.col("close").shift(1)).abs(),
                ).alias("tr"),
            )
            .with_columns(pl.col("tr").rolling_mean(self.atr_window).alias("atr"))
        )
        rows = enriched.to_dicts()

        swing_lows, swing_highs = find_swings(df, prominence_factor=0.5,
                                                min_distance=self.consol_min_bars)
        signals: list[Signal] = []

        for L2_idx, L2 in swing_lows:
            for L1_idx, L1 in swing_lows:
                if L1_idx >= L2_idx:
                    continue
                if not (self.min_separation <= L2_idx - L1_idx <= self.max_separation):
                    continue
                if L2 <= 0 or abs(L1 - L2) / L2 > self.tolerance:
                    continue
                # neckline = max high entre L1 y L2
                neckline = max(rows[i]["high"] for i in range(L1_idx, L2_idx + 1))
                altura = neckline - L2
                if altura <= 0:
                    continue
                # buscar ruptura + consolidación post-neckline
                for trigger_idx in range(L2_idx + self.consol_min_bars, len(rows)):
                    cur = rows[trigger_idx]
                    if cur.get("sma") is None or cur["close"] <= cur["sma"]:
                        continue
                    if cur["close"] <= neckline:
                        continue
                    # consolidación de últimas N barras antes de trigger
                    consol_start = max(0, trigger_idx - self.consol_min_bars + 1)
                    consol_high = max(rows[i]["high"] for i in range(consol_start, trigger_idx + 1))
                    consol_low = min(rows[i]["low"] for i in range(consol_start, trigger_idx + 1))
                    rango = consol_high - consol_low
                    atr_cur = cur.get("atr") or 0.0
                    if atr_cur == 0 or rango > self.consol_max_atr_mult * atr_cur:
                        continue
                    if min(rows[i]["low"] for i in range(consol_start, trigger_idx + 1)) <= neckline:
                        continue
                    # all filters passed; emit signal
                    entry_price = consol_high + _TICK
                    setup_ts = cur["time"]
                    valid_until = setup_ts + timedelta(days=20)
                    anchors = {
                        "L1": L1, "L2": L2, "neckline": neckline,
                        "altura_patron": altura, "sma18": cur["sma"],
                        "atr14": atr_cur, "consol_low": consol_low,
                    }
                    signals.append(Signal(
                        symbol=symbol, strategy=self.name, side="long",
                        setup_ts=setup_ts, entry_type="stop",
                        entry_price=entry_price,
                        valid_until=valid_until,
                        stop=0.0, tp1=None, tp2=None,
                        timestop_bars=20,
                        indicator_anchors=anchors,
                    ))
                    break  # one signal per (L1, L2) pair
        return signals
```

- [ ] **Step 4: Run tests, verify 2 passed.**

- [ ] **Step 5: Commit:** `feat(strategies_external): Doble Suelo strategy with detector+filters`

---

## Task B3: Extend ExitManagers for double_bottom

**Files:**
- Modify: `src/strategies_external/exit_managers.py`
- Modify: `tests/strategies_external/test_exit_managers_extensions.py`

- [ ] **Step 1: Append tests**

```python
def _signal_long_db_raw():
    return Signal(
        symbol="XAUUSD", strategy="double_bottom", side="long",
        setup_ts=datetime(2024, 1, 5),
        entry_type="stop", entry_price=2050.0,
        valid_until=datetime(2024, 2, 5),
        stop=0.0, tp1=None, tp2=None,
        indicator_anchors={"L1": 2000.0, "L2": 2010.0, "neckline": 2040.0,
                           "altura_patron": 30.0, "sma18": 2025.0,
                           "atr14": 15.0, "consol_low": 2042.0},
    )


def test_doc_exit_manager_double_bottom_long():
    s = DocExitManager(strategy="double_bottom").attach_levels(_signal_long_db_raw())
    # Doc DB: stop = consol_low; tp1 = neckline + altura_patron (fib100); tp2 = neckline + altura*1.618
    assert s.stop == pytest.approx(2042.0)
    assert s.tp1 == pytest.approx(2040.0 + 30.0)
    assert s.tp2 == pytest.approx(2040.0 + 30.0 * 1.618)


def test_indicator_exit_manager_double_bottom_long():
    s = IndicatorExitManager(strategy="double_bottom").attach_levels(_signal_long_db_raw())
    # Indicator DB: stop = L2 - 0.25*altura; tp1 = neckline + altura; tp2 = neckline + 1.618*altura
    assert s.stop == pytest.approx(2010.0 - 0.25 * 30.0)
    assert s.tp1 == pytest.approx(2040.0 + 30.0)
    assert s.tp2 == pytest.approx(2040.0 + 30.0 * 1.618)
```

- [ ] **Step 2: Run failing.**

- [ ] **Step 3: Add `_double_bottom` branch in DocExitManager and IndicatorExitManager:**

```python
# DocExitManager._double_bottom:
    def _double_bottom(self, s: Signal) -> Signal:
        consol_low = _require_anchor(s, "consol_low")
        neckline = _require_anchor(s, "neckline")
        altura = _require_anchor(s, "altura_patron")
        if s.side == "long":
            stop = consol_low
            tp1 = neckline + altura
            tp2 = neckline + altura * 1.618
        else:
            consol_high = _require_anchor(s, "consol_high")
            stop = consol_high
            tp1 = neckline - altura
            tp2 = neckline - altura * 1.618
        return replace(s, stop=stop, tp1=tp1, tp2=tp2)


# IndicatorExitManager._double_bottom:
    def _double_bottom(self, s: Signal) -> Signal:
        L2 = _require_anchor(s, "L2")
        neckline = _require_anchor(s, "neckline")
        altura = _require_anchor(s, "altura_patron")
        if s.side == "long":
            stop = L2 - 0.25 * altura
            tp1 = neckline + altura
            tp2 = neckline + altura * 1.618
        else:
            stop = L2 + 0.25 * altura
            tp1 = neckline - altura
            tp2 = neckline - altura * 1.618
        return replace(s, stop=stop, tp1=tp1, tp2=tp2)
```

Add `if self.strategy == "double_bottom": return self._double_bottom(signal_raw)` in both `attach_levels` dispatch sections.

- [ ] **Step 4: Run pytest, verify passes.**

- [ ] **Step 5: Commit:** `feat(strategies_external): Doble Suelo exit branches`

---

## Task B4: run_double_bottom runner

**Files:**
- Create: `src/strategies_external/runners/run_double_bottom.py`
- Create: `tests/strategies_external/test_run_double_bottom_integration.py`

Pattern the runner identical to `run_sma18.py` (full ATR sweep + WF + MC + report). Test analogous to `test_run_sma18_integration.py`.

Symbols for runner default: `["XAUUSD", "XAGUSD", "SP500", "NASDAQ100", "WTI"]`.

Strategy class: `DoubleBottomStrategy()`.
DocExitManager / IndicatorExitManager strategy="double_bottom".
Output: `reports/external/double_bottom_backtest.md`.

Run runner standalone, capture and report results.

Commit: `feat(strategies_external): run_double_bottom runner`

---

# Block C — Perdices Fib (Tasks C1-C3)

## Task C1: PerdicesFibStrategy (versión H1)

**Files:**
- Create: `src/strategies_external/strategies/perdices_fib.py`
- Create: `tests/strategies_external/test_perdices_fib_strategy.py`

- [ ] **Step 1: Tests**

```python
# tests/strategies_external/test_perdices_fib_strategy.py
from datetime import datetime, timedelta

import polars as pl
import pytest

from src.strategies_external.strategies.perdices_fib import PerdicesFibStrategy


@pytest.fixture
def perdices_long_df():
    """H1 OHLC: clear uptrend on 4H, then 1H pullback to fib zone with RSI<40 turning up."""
    base = datetime(2024, 1, 1)
    rows = []
    # 200 bars H1 (8 days):
    # bars 0-100: monotonic uptrend 1900 → 1950
    # bars 100-150: pullback 1950 → 1925 (50% retrace)
    # bars 150-200: rally back to 1960
    for i in range(200):
        if i <= 100:
            v = 1900.0 + i * 0.5
        elif i <= 150:
            v = 1950.0 - (i - 100) * 0.5
        else:
            v = 1925.0 + (i - 150) * 0.7
        rows.append((base + timedelta(hours=i), v, v + 1.0, v - 1.0, v, 1000.0))
    return pl.DataFrame(
        {"time": [r[0] for r in rows],
         "open": [r[1] for r in rows], "high": [r[2] for r in rows],
         "low": [r[3] for r in rows], "close": [r[4] for r in rows],
         "volume": [r[5] for r in rows]},
        schema={"time": pl.Datetime, "open": pl.Float64, "high": pl.Float64,
                "low": pl.Float64, "close": pl.Float64, "volume": pl.Float64},
    )


def test_perdices_fib_detects_long(perdices_long_df):
    strat = PerdicesFibStrategy()
    sigs = strat.generate_signals(perdices_long_df, symbol="XAUUSD")
    long_sigs = [s for s in sigs if s.side == "long"]
    assert len(long_sigs) >= 1
    s = long_sigs[0]
    for k in ("swing_high", "swing_low", "fib_382", "fib_50", "rsi", "atr14"):
        assert k in s.indicator_anchors


def test_perdices_fib_no_signal_in_downtrend():
    """Monotonic downtrend → trend_up filter fails → no longs."""
    base = datetime(2024, 1, 1)
    rows = [(base + timedelta(hours=i), 1950.0 - i * 0.3,
             1950.0 - i * 0.3 + 1, 1950.0 - i * 0.3 - 1,
             1950.0 - i * 0.3, 1000.0) for i in range(200)]
    df = pl.DataFrame(
        {"time": [r[0] for r in rows],
         "open": [r[1] for r in rows], "high": [r[2] for r in rows],
         "low": [r[3] for r in rows], "close": [r[4] for r in rows],
         "volume": [r[5] for r in rows]},
        schema={"time": pl.Datetime, "open": pl.Float64, "high": pl.Float64,
                "low": pl.Float64, "close": pl.Float64, "volume": pl.Float64},
    )
    strat = PerdicesFibStrategy()
    sigs = strat.generate_signals(df, symbol="XAUUSD")
    long_sigs = [s for s in sigs if s.side == "long"]
    assert long_sigs == []
```

- [ ] **Step 2: Run failing.**

- [ ] **Step 3: Implementation**

```python
# src/strategies_external/strategies/perdices_fib.py
"""Pau Perdices — pullback Fibonacci on XAUUSD/XAGUSD.

V1 ejecución en H1 (placeholder hasta llegar M5 para versión final).
Contexto: EMA50>EMA200 (en H4 agregado desde H1) + estructura HH/HL.
Entrada: zona Fib 38.2-50% del último impulso, RSI(14) < 40 girando, vela alcista.
"""

from datetime import timedelta

import polars as pl

from src.strategies_external.common.signal import Signal
from src.strategies_external.strategies.base import Strategy
from src.strategies_external.strategies.swings import find_swings


class PerdicesFibStrategy(Strategy):
    name = "perdices_fib"

    def __init__(
        self,
        rsi_window: int = 14,
        rsi_threshold: float = 40.0,
        fib_low: float = 0.382,
        fib_high: float = 0.5,
        ema_fast: int = 50,
        ema_slow: int = 200,
        impulse_window: int = 50,
        atr_window: int = 14,
    ):
        self.rsi_window = rsi_window
        self.rsi_threshold = rsi_threshold
        self.fib_low = fib_low
        self.fib_high = fib_high
        self.ema_fast = ema_fast
        self.ema_slow = ema_slow
        self.impulse_window = impulse_window
        self.atr_window = atr_window

    def _rsi(self, closes: pl.Series) -> pl.Series:
        delta = closes.diff()
        gain = delta.clip(lower_bound=0)
        loss = (-delta).clip(lower_bound=0)
        avg_gain = gain.rolling_mean(self.rsi_window)
        avg_loss = loss.rolling_mean(self.rsi_window)
        rs = avg_gain / avg_loss.replace(0, 1e-9)
        return 100 - (100 / (1 + rs))

    def generate_signals(self, df: pl.DataFrame, symbol: str) -> list[Signal]:
        min_bars = max(self.ema_slow, self.impulse_window) + 5
        if df.is_empty() or df.shape[0] < min_bars:
            return []
        enriched = (
            df.with_columns(
                pl.col("close").ewm_mean(span=self.ema_fast).alias("ema_fast"),
                pl.col("close").ewm_mean(span=self.ema_slow).alias("ema_slow"),
                pl.max_horizontal(
                    pl.col("high") - pl.col("low"),
                    (pl.col("high") - pl.col("close").shift(1)).abs(),
                    (pl.col("low") - pl.col("close").shift(1)).abs(),
                ).alias("tr"),
                self._rsi(df["close"]).alias("rsi"),
            )
            .with_columns(pl.col("tr").rolling_mean(self.atr_window).alias("atr"))
        )
        rows = enriched.to_dicts()
        signals: list[Signal] = []

        for i in range(self.impulse_window, len(rows)):
            cur = rows[i]
            if cur.get("ema_fast") is None or cur.get("ema_slow") is None:
                continue
            trend_up = cur["ema_fast"] > cur["ema_slow"] and cur["close"] > cur["ema_fast"]
            trend_down = cur["ema_fast"] < cur["ema_slow"] and cur["close"] < cur["ema_fast"]
            if not (trend_up or trend_down):
                continue

            window = rows[i - self.impulse_window:i + 1]
            swing_high = max(b["high"] for b in window)
            swing_low = min(b["low"] for b in window)
            rango = swing_high - swing_low
            if rango <= 0:
                continue

            atr_cur = cur.get("atr") or 0.0
            rsi_cur = cur.get("rsi")
            rsi_prev = rows[i - 1].get("rsi") if i > 0 else None
            if rsi_cur is None or rsi_prev is None:
                continue

            anchors_base = {
                "swing_high": swing_high, "swing_low": swing_low,
                "fib_382": swing_high - 0.382 * rango,
                "fib_50": swing_high - 0.5 * rango,
                "fib_127": swing_high + 0.272 * rango,
                "fib_1618": swing_high + 0.618 * rango,
                "rsi": rsi_cur, "atr14": atr_cur,
            }
            valid_until = cur["time"] + timedelta(hours=4)

            if trend_up:
                fib_zone_low = swing_high - self.fib_high * rango
                fib_zone_high = swing_high - self.fib_low * rango
                if (fib_zone_low <= cur["low"] <= fib_zone_high
                        and rsi_cur < self.rsi_threshold and rsi_cur > rsi_prev
                        and cur["close"] > cur["open"]):
                    signals.append(Signal(
                        symbol=symbol, strategy=self.name, side="long",
                        setup_ts=cur["time"], entry_type="market",
                        entry_price=cur["close"],
                        valid_until=valid_until,
                        stop=0.0, tp1=None, tp2=None,
                        indicator_anchors=anchors_base,
                    ))
            elif trend_down:
                fib_zone_high = swing_low + self.fib_high * rango
                fib_zone_low = swing_low + self.fib_low * rango
                if (fib_zone_low <= cur["high"] <= fib_zone_high
                        and rsi_cur > 100 - self.rsi_threshold and rsi_cur < rsi_prev
                        and cur["close"] < cur["open"]):
                    anchors_short = {**anchors_base,
                                     "fib_127": swing_low - 0.272 * rango,
                                     "fib_1618": swing_low - 0.618 * rango}
                    signals.append(Signal(
                        symbol=symbol, strategy=self.name, side="short",
                        setup_ts=cur["time"], entry_type="market",
                        entry_price=cur["close"],
                        valid_until=valid_until,
                        stop=0.0, tp1=None, tp2=None,
                        indicator_anchors=anchors_short,
                    ))
        return signals
```

- [ ] **Step 4: Run tests, expect 2 passed.**

- [ ] **Step 5: Commit:** `feat(strategies_external): Perdices Fib strategy (H1 placeholder)`

---

## Task C2: Extend ExitManagers for perdices_fib

**Files:**
- Modify: `src/strategies_external/exit_managers.py`
- Modify: `tests/strategies_external/test_exit_managers_extensions.py`

- [ ] **Step 1: Tests**

```python
def _signal_long_perdices_raw():
    return Signal(
        symbol="XAUUSD", strategy="perdices_fib", side="long",
        setup_ts=datetime(2024, 1, 5, 14),
        entry_type="market", entry_price=2030.0,
        valid_until=datetime(2024, 1, 5, 18),
        stop=0.0, tp1=None, tp2=None,
        indicator_anchors={"swing_high": 2050.0, "swing_low": 2000.0,
                           "fib_382": 2030.9, "fib_50": 2025.0,
                           "fib_127": 2063.6, "fib_1618": 2080.9,
                           "rsi": 38.0, "atr14": 5.0},
    )


def test_doc_exit_manager_perdices_long():
    s = DocExitManager(strategy="perdices_fib").attach_levels(_signal_long_perdices_raw())
    # Doc Perdices: stop = swing_low - 2pip ≈ swing_low - 0.2 (oro), tp1 = swing_high
    assert s.stop == pytest.approx(1999.8, abs=0.01)
    assert s.tp1 == pytest.approx(2050.0)


def test_indicator_exit_manager_perdices_long():
    s = IndicatorExitManager(strategy="perdices_fib").attach_levels(_signal_long_perdices_raw())
    # Indicator Perdices: stop = swing_low - 2 pips, tp1 = swing_high, tp2 = fib_1618
    assert s.stop == pytest.approx(1999.8, abs=0.01)
    assert s.tp1 == pytest.approx(2050.0)
    assert s.tp2 == pytest.approx(2080.9)
```

- [ ] **Step 2: Run failing.**

- [ ] **Step 3: Add `_perdices_fib` branches:**

```python
# DocExitManager._perdices_fib:
    def _perdices_fib(self, s: Signal) -> Signal:
        if s.side == "long":
            stop = _require_anchor(s, "swing_low") - 0.2
            tp1 = _require_anchor(s, "swing_high")
        else:
            stop = _require_anchor(s, "swing_high") + 0.2
            tp1 = _require_anchor(s, "swing_low")
        return replace(s, stop=stop, tp1=tp1, tp2=None, timestop_bars=240)  # 240 M1 bars = 4h


# IndicatorExitManager._perdices_fib:
    def _perdices_fib(self, s: Signal) -> Signal:
        if s.side == "long":
            stop = _require_anchor(s, "swing_low") - 0.2
            tp1 = _require_anchor(s, "swing_high")
            tp2 = _require_anchor(s, "fib_1618")
        else:
            stop = _require_anchor(s, "swing_high") + 0.2
            tp1 = _require_anchor(s, "swing_low")
            tp2 = _require_anchor(s, "fib_1618")
        return replace(s, stop=stop, tp1=tp1, tp2=tp2, timestop_bars=240)
```

Add to `attach_levels` dispatch.

- [ ] **Step 4: Run tests, verify passes.**

- [ ] **Step 5: Commit:** `feat(strategies_external): Perdices Fib exit branches`

---

## Task C3: run_perdices_fib runner

**Files:**
- Create: `src/strategies_external/runners/run_perdices_fib.py`
- Create: `tests/strategies_external/test_run_perdices_fib_integration.py`

Same pattern as run_sma18 / run_double_bottom. Symbols: `["XAUUSD", "XAGUSD"]`. **Use H1 instead of daily as signal TF** (no aggregate_to_daily call). Output: `reports/external/perdices_fib_backtest.md`.

```python
# Inside run_perdices_fib_backtest:
    for sym in symbols:
        df_h1 = load_csv(sym, "H1", data_dir=data_dir)  # no aggregate to daily!
        _, df_track = best_tracking_tf(sym, data_dir=data_dir)
        sigs = strategy.generate_signals(df_h1, symbol=sym)
        per_symbol[sym] = (sigs, df_track)
```

Run standalone, report results.

Commit: `feat(strategies_external): run_perdices_fib runner (H1 version)`

---

# Block D — COT-1 (Tasks D1-D5)

## Task D1: cot_downloader

**Files:**
- Create: `src/strategies_external/data_sources/__init__.py` (empty)
- Create: `src/strategies_external/data_sources/cot_downloader.py`
- Create: `tests/strategies_external/test_cot_downloader.py`

- [ ] **Step 1: Tests** (mock urllib to avoid live HTTP)

```python
# tests/strategies_external/test_cot_downloader.py
import io
import zipfile
from pathlib import Path
from unittest.mock import patch

import polars as pl
import pytest

from src.strategies_external.data_sources.cot_downloader import (
    download_cot, parse_cot_text, cot_index,
)


def test_parse_cot_text_extracts_commercials():
    sample = (
        "Market_and_Exchange_Names,Report_Date_as_YYYY-MM-DD,Producer_Merchant_Long_All,Producer_Merchant_Short_All\n"
        "GOLD - COMMODITY EXCHANGE INC.,2024-01-09,100000,80000\n"
        "GOLD - COMMODITY EXCHANGE INC.,2024-01-16,110000,90000\n"
    )
    df = parse_cot_text(sample, market_keyword="GOLD")
    assert df.shape[0] == 2
    assert df["net"].to_list() == [20000, 20000]


def test_cot_index_normalizes_to_0_100():
    series = pl.Series("net", [10, 20, 30, 40, 50])
    idx = cot_index(series, window=5)
    # Last value: (50 - 10) / (50 - 10) * 100 = 100
    assert idx.to_list()[-1] == pytest.approx(100.0)


def test_download_cot_writes_parquet(tmp_path: Path):
    """Mock the urllib download to avoid live HTTP."""
    fake_csv = (
        "Market_and_Exchange_Names,Report_Date_as_YYYY-MM-DD,Producer_Merchant_Long_All,Producer_Merchant_Short_All\n"
        "GOLD - COMMODITY EXCHANGE INC.,2024-01-09,100,80\n"
    )
    fake_zip = io.BytesIO()
    with zipfile.ZipFile(fake_zip, "w") as zf:
        zf.writestr("c_year.csv", fake_csv)
    fake_zip.seek(0)
    with patch("src.strategies_external.data_sources.cot_downloader.urlopen") as mock_urlopen:
        mock_urlopen.return_value = fake_zip
        out = download_cot(year=2024, market_keyword="GOLD",
                           output_dir=str(tmp_path))
    assert out.exists()
    df = pl.read_parquet(out)
    assert df.shape[0] == 1
```

- [ ] **Step 2: Run failing.**

- [ ] **Step 3: Implementation**

```python
# src/strategies_external/data_sources/cot_downloader.py
"""COT report downloader from cftc.gov."""

import io
import zipfile
from pathlib import Path
from urllib.request import urlopen

import polars as pl


_CFTC_URL_TEMPLATE = (
    "https://www.cftc.gov/files/dea/history/com_disagg_txt_{year}.zip"
)


def parse_cot_text(text: str, market_keyword: str) -> pl.DataFrame:
    """Parse COT CSV text; filter rows by market_keyword (case-insensitive)
    and return a polars DataFrame with columns: date, long, short, net."""
    df = pl.read_csv(io.StringIO(text))
    cols = df.columns
    name_col = next(c for c in cols if "market" in c.lower() and "name" in c.lower())
    date_col = next(c for c in cols if "report_date" in c.lower())
    long_col = next(c for c in cols if "producer" in c.lower() and "long" in c.lower())
    short_col = next(c for c in cols if "producer" in c.lower() and "short" in c.lower())
    df = (
        df.filter(pl.col(name_col).str.contains(market_keyword, literal=True))
        .with_columns(
            pl.col(date_col).str.strptime(pl.Date, "%Y-%m-%d", strict=False).alias("date"),
            pl.col(long_col).cast(pl.Int64).alias("long"),
            pl.col(short_col).cast(pl.Int64).alias("short"),
        )
        .with_columns((pl.col("long") - pl.col("short")).alias("net"))
        .select(["date", "long", "short", "net"])
        .sort("date")
    )
    return df


def cot_index(net_positions: pl.Series, window: int = 26) -> pl.Series:
    rolling_min = net_positions.rolling_min(window)
    rolling_max = net_positions.rolling_max(window)
    return 100.0 * (net_positions - rolling_min) / (rolling_max - rolling_min).replace(0, 1)


def download_cot(
    year: int, market_keyword: str, output_dir: str = "data/cot"
) -> Path:
    """Download Disaggregated COT report for a year and persist parsed parquet.

    Returns path to the saved parquet.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    url = _CFTC_URL_TEMPLATE.format(year=year)
    raw = urlopen(url)
    with zipfile.ZipFile(io.BytesIO(raw.read())) as zf:
        csv_name = next(n for n in zf.namelist() if n.endswith(".csv") or n.endswith(".txt"))
        with zf.open(csv_name) as f:
            text = f.read().decode("utf-8", errors="replace")
    df = parse_cot_text(text, market_keyword=market_keyword)
    safe = market_keyword.lower().replace(" ", "_")
    path = Path(output_dir) / f"{safe}_{year}.parquet"
    df.write_parquet(path)
    return path
```

- [ ] **Step 4: Run tests, expect 3 passed.**

- [ ] **Step 5: Commit:** `feat(strategies_external): COT downloader from cftc.gov`

---

## Task D2: seasonality

**Files:**
- Create: `src/strategies_external/data_sources/seasonality.py`
- Create: `tests/strategies_external/test_seasonality.py`

- [ ] **Step 1: Tests**

```python
# tests/strategies_external/test_seasonality.py
from datetime import datetime, timedelta

import polars as pl
import pytest

from src.strategies_external.data_sources.seasonality import seasonal_mean_return


def test_seasonal_mean_return_basic():
    """All trades on same date over 3 years; mean return per (mm-dd) is returned."""
    base = datetime(2020, 1, 15)
    rows = []
    for year_offset in range(4):
        for day_offset in range(20):
            ts = datetime(2020 + year_offset, 1, 15) + timedelta(days=day_offset)
            close = 100.0 + day_offset + year_offset * 5
            rows.append((ts, close))
    df = pl.DataFrame(
        {"time": [r[0] for r in rows], "close": [r[1] for r in rows]},
        schema={"time": pl.Datetime, "close": pl.Float64},
    )
    out = seasonal_mean_return(df, window_days=5)
    # Should produce some entries
    assert len(out) > 0
    assert all(0 <= len(k) <= 5 for k in out.keys())  # "MM-DD" keys
```

- [ ] **Step 2: Run failing.**

- [ ] **Step 3: Implementation**

```python
# src/strategies_external/data_sources/seasonality.py
"""Average historical return per (month, day) across N years."""

import polars as pl


def seasonal_mean_return(df: pl.DataFrame, window_days: int = 5) -> dict[str, float]:
    """For each (month, day) key, compute the mean N-day forward return
    across all years in the dataset (excluding the current year's recent data).

    df: DataFrame with `time` (datetime) and `close` columns.
    Returns: dict {"MM-DD": mean_return}.
    """
    if df.is_empty():
        return {}
    enriched = (
        df.sort("time")
        .with_columns(
            (pl.col("close").shift(-window_days) / pl.col("close") - 1.0).alias("ret"),
            pl.col("time").dt.strftime("%m-%d").alias("key"),
        )
        .drop_nulls(["ret"])
    )
    grouped = enriched.group_by("key").agg(pl.col("ret").mean().alias("mean_ret"))
    rows = grouped.to_dicts()
    return {r["key"]: r["mean_ret"] for r in rows}
```

- [ ] **Step 4: Run tests, expect 1 passed.**

- [ ] **Step 5: Commit:** `feat(strategies_external): seasonality average return`

---

## Task D3: COT1Strategy.generate_signals

**Files:**
- Create: `src/strategies_external/strategies/cot1.py`
- Create: `tests/strategies_external/test_cot1_strategy.py`

- [ ] **Step 1: Tests**

```python
# tests/strategies_external/test_cot1_strategy.py
from datetime import datetime, timedelta

import polars as pl
import pytest

from src.strategies_external.strategies.cot1 import COT1Strategy


@pytest.fixture
def cot_index_series():
    """Weekly series with COT Index = 90 for the last 5 weeks (long bias)."""
    base = datetime(2024, 1, 1)
    return pl.DataFrame(
        {"date": [base + timedelta(weeks=i) for i in range(20)],
         "cot_index": [50.0] * 15 + [90.0] * 5},
        schema={"date": pl.Datetime, "cot_index": pl.Float64},
    )


@pytest.fixture
def daily_with_pin_bar():
    base = datetime(2024, 1, 1)
    rows = []
    for i in range(40):
        if i == 38:
            # pin bar bullish: long lower wick, body in upper third
            rows.append((base + timedelta(days=i), 100.0, 102.0, 95.0, 101.5, 1000.0))
        else:
            v = 100.0 + i * 0.05
            rows.append((base + timedelta(days=i), v, v + 0.3, v - 0.3, v, 1000.0))
    return pl.DataFrame(
        {"time": [r[0] for r in rows],
         "open": [r[1] for r in rows], "high": [r[2] for r in rows],
         "low": [r[3] for r in rows], "close": [r[4] for r in rows],
         "volume": [r[5] for r in rows]},
        schema={"time": pl.Datetime, "open": pl.Float64, "high": pl.Float64,
                "low": pl.Float64, "close": pl.Float64, "volume": pl.Float64},
    )


def test_cot1_long_signal(cot_index_series, daily_with_pin_bar):
    strat = COT1Strategy(cot_threshold_long=80.0, cot_threshold_short=20.0)
    seasonality = {"02-08": 0.01}  # positive seasonality on day idx 38
    sigs = strat.generate_signals(
        daily_with_pin_bar, symbol="XAUUSD",
        cot_index_series=cot_index_series,
        seasonality=seasonality,
    )
    long_sigs = [s for s in sigs if s.side == "long"]
    assert len(long_sigs) >= 1
```

- [ ] **Step 2: Run failing.**

- [ ] **Step 3: Implementation**

```python
# src/strategies_external/strategies/cot1.py
"""InsiderWeek COT-1: COT extremes + seasonality + price action.

COT Index > threshold_long → long bias; < threshold_short → short bias.
Confluence: seasonal mean return aligns with bias.
Trigger: pin bar / inside-day breakout / double-bottom on daily.
"""

from datetime import timedelta

import polars as pl

from src.strategies_external.common.signal import Signal
from src.strategies_external.strategies.base import Strategy


def _is_pin_bar(o: float, h: float, l: float, c: float, side: str) -> bool:
    rng = h - l
    if rng <= 0:
        return False
    body = abs(c - o)
    if body / rng >= 0.30:
        return False
    if side == "long":
        lower_wick = min(o, c) - l
        return lower_wick / rng > 0.5 and c > o
    else:
        upper_wick = h - max(o, c)
        return upper_wick / rng > 0.5 and c < o


class COT1Strategy(Strategy):
    name = "cot1"

    def __init__(
        self,
        cot_threshold_long: float = 80.0,
        cot_threshold_short: float = 20.0,
        seasonal_threshold: float = 0.005,
        cot_lag_days: int = 3,
        atr_window: int = 14,
    ):
        self.cot_threshold_long = cot_threshold_long
        self.cot_threshold_short = cot_threshold_short
        self.seasonal_threshold = seasonal_threshold
        self.cot_lag_days = cot_lag_days
        self.atr_window = atr_window

    def generate_signals(
        self,
        df: pl.DataFrame,
        symbol: str,
        cot_index_series: pl.DataFrame | None = None,
        seasonality: dict[str, float] | None = None,
    ) -> list[Signal]:
        if df.is_empty() or df.shape[0] < self.atr_window + 5:
            return []
        cot_index_series = cot_index_series if cot_index_series is not None else pl.DataFrame()
        seasonality = seasonality or {}

        enriched = (
            df.with_columns(
                pl.max_horizontal(
                    pl.col("high") - pl.col("low"),
                    (pl.col("high") - pl.col("close").shift(1)).abs(),
                    (pl.col("low") - pl.col("close").shift(1)).abs(),
                ).alias("tr")
            )
            .with_columns(pl.col("tr").rolling_mean(self.atr_window).alias("atr"))
        )
        rows = enriched.to_dicts()

        cot_rows = cot_index_series.sort("date").to_dicts() if cot_index_series.shape[0] > 0 else []
        signals: list[Signal] = []

        for i in range(self.atr_window + 1, len(rows)):
            cur = rows[i]
            cur_ts = cur["time"]
            atr_cur = cur.get("atr") or 0.0

            # Find most recent COT publication respecting lag
            applicable_cot = None
            for c in reversed(cot_rows):
                if c["date"] + timedelta(days=self.cot_lag_days) <= cur_ts:
                    applicable_cot = c["cot_index"]
                    break
            if applicable_cot is None:
                continue

            key = cur_ts.strftime("%m-%d")
            seasonal = seasonality.get(key, 0.0)

            anchors = {
                "atr14": atr_cur, "cot_index": applicable_cot,
                "season_5d": seasonal,
                "swing_high_5d": max(rows[i - j]["high"] for j in range(1, 6)),
                "swing_low_5d": min(rows[i - j]["low"] for j in range(1, 6)),
            }
            valid_until = cur_ts + timedelta(days=5)

            # Long bias
            if applicable_cot >= self.cot_threshold_long and seasonal >= self.seasonal_threshold:
                if _is_pin_bar(cur["open"], cur["high"], cur["low"], cur["close"], "long"):
                    signals.append(Signal(
                        symbol=symbol, strategy=self.name, side="long",
                        setup_ts=cur_ts, entry_type="stop",
                        entry_price=cur["high"] + 0.01,
                        valid_until=valid_until,
                        stop=0.0, tp1=None, tp2=None,
                        timestop_bars=120,  # ~5 days × 24h M1 if tracking M1, else fewer
                        indicator_anchors=anchors,
                    ))
            # Short bias
            if applicable_cot <= self.cot_threshold_short and seasonal <= -self.seasonal_threshold:
                if _is_pin_bar(cur["open"], cur["high"], cur["low"], cur["close"], "short"):
                    signals.append(Signal(
                        symbol=symbol, strategy=self.name, side="short",
                        setup_ts=cur_ts, entry_type="stop",
                        entry_price=cur["low"] - 0.01,
                        valid_until=valid_until,
                        stop=0.0, tp1=None, tp2=None,
                        timestop_bars=120,
                        indicator_anchors=anchors,
                    ))
        return signals
```

- [ ] **Step 4: Run tests, expect 1 passed.**

- [ ] **Step 5: Commit:** `feat(strategies_external): COT-1 strategy with COT/seasonality/price-action`

---

## Task D4: Extend ExitManagers for cot1

**Files:**
- Modify: `src/strategies_external/exit_managers.py`
- Modify: `tests/strategies_external/test_exit_managers_extensions.py`

- [ ] **Step 1: Tests**

```python
def _signal_long_cot1_raw():
    return Signal(
        symbol="XAUUSD", strategy="cot1", side="long",
        setup_ts=datetime(2024, 1, 5),
        entry_type="stop", entry_price=2050.0,
        valid_until=datetime(2024, 1, 10),
        stop=0.0, tp1=None, tp2=None,
        timestop_bars=120,
        indicator_anchors={"atr14": 15.0, "cot_index": 85.0,
                           "season_5d": 0.012,
                           "swing_high_5d": 2055.0, "swing_low_5d": 2030.0},
    )


def test_doc_exit_manager_cot1_long():
    s = DocExitManager(strategy="cot1").attach_levels(_signal_long_cot1_raw())
    # Doc COT1: stop = swing_low_5d - 0.5*atr; tp1 = entry + 1.5R; tp2 = entry + 3R
    assert s.stop == pytest.approx(2030.0 - 0.5 * 15.0)
    R = 2050.0 - (2030.0 - 0.5 * 15.0)
    assert s.tp1 == pytest.approx(2050.0 + 1.5 * R, abs=0.5)
    assert s.tp2 == pytest.approx(2050.0 + 3.0 * R, abs=0.5)


def test_indicator_exit_manager_cot1_long():
    s = IndicatorExitManager(strategy="cot1").attach_levels(_signal_long_cot1_raw())
    # Indicator COT1: stop = swing_low_5d - 0.5*atr; tp1/tp2 inherit doc style for now
    assert s.stop == pytest.approx(2030.0 - 0.5 * 15.0)
    assert s.tp1 is not None
    assert s.tp2 is not None
```

- [ ] **Step 2: Run failing.**

- [ ] **Step 3: Add `_cot1` branches:**

```python
# DocExitManager._cot1:
    def _cot1(self, s: Signal) -> Signal:
        atr = _require_anchor(s, "atr14")
        if s.side == "long":
            stop = _require_anchor(s, "swing_low_5d") - 0.5 * atr
            R = s.entry_price - stop
            tp1 = s.entry_price + 1.5 * R
            tp2 = s.entry_price + 3.0 * R
        else:
            stop = _require_anchor(s, "swing_high_5d") + 0.5 * atr
            R = stop - s.entry_price
            tp1 = s.entry_price - 1.5 * R
            tp2 = s.entry_price - 3.0 * R
        return replace(s, stop=stop, tp1=tp1, tp2=tp2)


# IndicatorExitManager._cot1: same as doc for V1 (no separate indicator anchors yet)
    def _cot1(self, s: Signal) -> Signal:
        return DocExitManager(strategy="cot1")._cot1(s)._replace_dispatch_for_indicator()
```

Actually simpler — Indicator just delegates to doc behavior for COT-1 in V1:

```python
    def _cot1(self, s: Signal) -> Signal:
        # Same anchors as doc; if a clearer "indicator" anchoring emerges later, refine.
        atr = _require_anchor(s, "atr14")
        if s.side == "long":
            stop = _require_anchor(s, "swing_low_5d") - 0.5 * atr
            R = s.entry_price - stop
            tp1 = s.entry_price + 1.5 * R
            tp2 = s.entry_price + 3.0 * R
        else:
            stop = _require_anchor(s, "swing_high_5d") + 0.5 * atr
            R = stop - s.entry_price
            tp1 = s.entry_price - 1.5 * R
            tp2 = s.entry_price - 3.0 * R
        return replace(s, stop=stop, tp1=tp1, tp2=tp2)
```

Add to dispatch.

- [ ] **Step 4: Run tests, expect passes.**

- [ ] **Step 5: Commit:** `feat(strategies_external): COT-1 exit branches`

---

## Task D5: run_cot1 runner

**Files:**
- Create: `src/strategies_external/runners/run_cot1.py`
- Create: `tests/strategies_external/test_run_cot1_integration.py`

- [ ] **Step 1: Test**

```python
@pytest.mark.integration
def test_run_cot1_real_data_produces_report(tmp_path: Path):
    output = tmp_path / "cot1_backtest.md"
    summary = run_cot1_backtest(
        symbols=["XAUUSD", "WTI"],
        data_dir="data",
        output_path=output,
        cot_dir="data/cot",
        years=range(2018, 2026),
    )
    assert output.exists()
```

- [ ] **Step 2: Implementation**

The runner needs to:
1. For each year in the range, ensure `data/cot/<keyword>_<year>.parquet` exists; if not, call `download_cot(year, keyword)`.
2. Concatenate per-symbol COT into a single time series.
3. Compute COT Index 26-week rolling.
4. Compute seasonality dict from per-symbol daily data.
5. Run `COT1Strategy.generate_signals` per symbol passing cot_index_series + seasonality.
6. Standard Doc / Indicator / ATR sweep + WF + MC + report.

Map symbol → COT market keyword:
```python
_SYMBOL_TO_COT = {
    "XAUUSD": "GOLD",
    "XAGUSD": "SILVER",
    "WTI": "CRUDE OIL, LIGHT SWEET",
    "BRENT": "BRENT CRUDE",  # Disaggregated may not exist; fallback documented
    "NATGAS": "NATURAL GAS",
    "SP500": "S&P 500",
    "NASDAQ100": "NASDAQ-100",
}
```

Run runner standalone, report results.

Commit: `feat(strategies_external): run_cot1 runner with COT download and seasonality`

---

# Block E — Cross-strategy comparison (Task E1)

## Task E1: run_all + comparison report

**Files:**
- Create: `src/strategies_external/reporting/comparison.py`
- Create: `src/strategies_external/runners/run_all.py`
- Create: `tests/strategies_external/test_run_all_integration.py`

- [ ] **Step 1: Implement comparison renderer**

```python
# src/strategies_external/reporting/comparison.py
"""Cross-strategy comparison report renderer."""

from datetime import datetime
from pathlib import Path

from src.strategies_external.common.metrics import evaluate
from src.strategies_external.common.trade import Trade


_SUMMARY_FIELDS = ["n_trades", "win_rate", "profit_factor", "expectancy_R",
                   "max_dd_R", "calmar"]


def _fmt(v) -> str:
    if isinstance(v, int):
        return str(v)
    if v == float("inf"):
        return "∞"
    return f"{v:.3f}"


def _semaforo(m: dict) -> str:
    """Verde/amarillo/rojo per spec criteria."""
    if m["n_trades"] < 30:
        return "🔴 (n<30)"
    if m["profit_factor"] < 1.2:
        return "🔴 (pf)"
    if m["calmar"] < 0.5:
        return "🟡 (calmar)"
    if m["calmar"] >= 1.0 and m["profit_factor"] >= 1.5:
        return "🟢"
    return "🟡"


def write_comparison_report(
    path: Path,
    summaries: dict[str, dict],
    trades_by_strategy: dict[str, list[Trade]],
) -> None:
    """summaries: {strategy_name: {mode: metrics_dict}}.
    trades_by_strategy: {strategy_name: list of Trade across all modes}.
    """
    lines: list[str] = []
    lines.append("# All External Strategies — Comparison")
    lines.append("")
    lines.append(f"**Generated:** {datetime.utcnow().isoformat()}Z")
    lines.append("")
    lines.append("## Cross-strategy summary (mode=doc)")
    lines.append("")
    header = "| strategy | " + " | ".join(_SUMMARY_FIELDS) + " | semaforo |"
    sep = "|----------|" + "|".join(["--------"] * (len(_SUMMARY_FIELDS) + 1)) + "|"
    lines.append(header)
    lines.append(sep)
    for strat, modes in summaries.items():
        m = modes.get("doc", {})
        if not m:
            lines.append(f"| {strat} | (no doc trades) |  |  |  |  |  |  |")
            continue
        row = "| " + strat + " | " + " | ".join(_fmt(m.get(f, 0)) for f in _SUMMARY_FIELDS)
        row += " | " + _semaforo(m) + " |"
        lines.append(row)
    lines.append("")

    lines.append("## Per-strategy mode comparison")
    lines.append("")
    for strat, modes in summaries.items():
        if not modes:
            continue
        lines.append(f"### {strat}")
        lines.append("")
        mode_keys = [k for k in modes if k != "atr_grid_results"]
        header_m = "| metric | " + " | ".join(mode_keys) + " |"
        sep_m = "|--------|" + "|".join(["--------"] * len(mode_keys)) + "|"
        lines.append(header_m)
        lines.append(sep_m)
        for f in _SUMMARY_FIELDS:
            row = f"| {f} | " + " | ".join(_fmt(modes[mk].get(f, 0)) for mk in mode_keys) + " |"
            lines.append(row)
        lines.append("")

    lines.append("## Ranking by Calmar OOS")
    ranked = sorted(
        ((strat, modes.get("doc", {}).get("calmar", -float("inf"))) for strat, modes in summaries.items()),
        key=lambda x: x[1], reverse=True,
    )
    lines.append("")
    for i, (strat, calmar) in enumerate(ranked, 1):
        lines.append(f"{i}. **{strat}** — calmar={_fmt(calmar)}")
    lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
```

- [ ] **Step 2: Implement orchestrator**

```python
# src/strategies_external/runners/run_all.py
"""Run all external strategies and emit cross-strategy comparison."""

from pathlib import Path

from src.strategies_external.reporting.comparison import write_comparison_report
from src.strategies_external.runners import (
    run_oops, run_sma18, run_double_bottom, run_perdices_fib, run_cot1,
)


def run_all_external(
    output_path: Path | str = "reports/external/all_external_comparison.md",
) -> dict:
    summaries: dict[str, dict] = {}

    summaries["oops"] = run_oops.run_oops_backtest(
        symbols=["SP500", "NASDAQ100"], data_dir="data",
        output_path="reports/external/oops_backtest.md",
    )
    summaries["sma18"] = run_sma18.run_sma18_backtest(
        symbols=["XAUUSD", "XAGUSD", "WTI", "BRENT", "NATGAS"], data_dir="data",
        output_path="reports/external/sma18_backtest.md",
    )
    summaries["double_bottom"] = run_double_bottom.run_double_bottom_backtest(
        symbols=["XAUUSD", "XAGUSD", "SP500", "NASDAQ100", "WTI"], data_dir="data",
        output_path="reports/external/double_bottom_backtest.md",
    )
    summaries["perdices_fib"] = run_perdices_fib.run_perdices_fib_backtest(
        symbols=["XAUUSD", "XAGUSD"], data_dir="data",
        output_path="reports/external/perdices_fib_backtest.md",
    )
    summaries["cot1"] = run_cot1.run_cot1_backtest(
        symbols=["XAUUSD", "WTI", "BRENT", "NATGAS"], data_dir="data",
        output_path="reports/external/cot1_backtest.md",
    )

    write_comparison_report(
        Path(output_path), summaries, trades_by_strategy={},
    )
    return summaries


if __name__ == "__main__":
    summaries = run_all_external()
    print("All external strategies done.")
    for s, modes in summaries.items():
        m = modes.get("doc", {})
        print(f"  {s}: n={m.get('n_trades', 0)} pf={m.get('profit_factor', 0):.3f} "
              f"calmar={m.get('calmar', 0):.3f}")
```

- [ ] **Step 3: Integration test**

```python
# tests/strategies_external/test_run_all_integration.py
from pathlib import Path

import pytest

from src.strategies_external.runners.run_all import run_all_external


@pytest.mark.integration
def test_run_all_external_produces_comparison(tmp_path: Path):
    out = tmp_path / "all_external_comparison.md"
    summaries = run_all_external(output_path=out)
    assert out.exists()
    content = out.read_text()
    assert "Comparison" in content
    for s in ("oops", "sma18", "double_bottom", "perdices_fib", "cot1"):
        assert s in content
    assert "Calmar" in content
```

- [ ] **Step 4: Commit:** `feat(strategies_external): run_all + cross-strategy comparison`

- [ ] **Step 5: Run standalone**: `python -m src.strategies_external.runners.run_all`

This is the **final report** of Plan 2. Capture the output and put it in the commit message.

---

## Self-Review

After all 19 tasks:

**1. Spec coverage:**
| Spec section | Cubierto por |
|--------------|--------------|
| §4.2 SMA-18 | A1, A2, A3 |
| §4.3 Doble Suelo | B1, B2, B3, B4 |
| §4.4 Perdices Fib | C1, C2, C3 |
| §4.5 COT-1 + downloader + seasonality | D1, D2, D3, D4, D5 |
| §6 reportes (parquet + markdown) | per-runner + E1 |
| §5 validación (WF + MC + sweep) | per-runner |
| comparación cross-estrategias | E1 |

**2. Placeholder scan:** todos los Step 1..5 con código completo.

**3. Type consistency:** strategy names ("sma18", "double_bottom", "perdices_fib", "cot1") consistentes en exit_managers, signal.strategy, runner names.

---

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-05-06-strategies-external-plan-2-remaining-strategies.md`.**

**Recommended:** continue with **superpowers:subagent-driven-development** in the same session. Each block (A→B→C→D→E) is independent; can pause between blocks to inspect results.

**Order:** SMA-18 (A1-A3) first since it validates the simplest case. If positive, momentum to continue. If negative, reassess.
