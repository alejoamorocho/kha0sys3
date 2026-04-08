# KHA0SYS3 — Opening Range Breakout Trading System

## Architecture

Layered architecture with strict dependency direction: `domain → application → engine → execution → monitoring`.

```
domain/          Data models, interfaces, constants (zero dependencies)
application/     Enrichment calculators, event trackers, statistics
engine/          Backtesting, strategy scanning, optimization, reporting
execution/       Live trading: MT5 client, order manager, risk allocator
monitoring/      Telegram bot, system health, MT5 reporting
```

## Key Modules

| Module | Purpose |
|--------|---------|
| `src/domain/constants.py` | Single source of truth for all magic numbers |
| `src/domain/models.py` | AssetConfig, TradeSignal, DailyMetrics dataclasses |
| `src/application/calculators.py` | DataEnricher: RSI, ATR, Opening Range, daily context |
| `src/application/trackers.py` | TrackerEngine: chronological event tracking (entries, TP, SL hits) |
| `src/application/statistics.py` | StatisticalEngine: conditional probability computation |
| `src/engine/strategy_scanner.py` | Exhaustive permutation scanner (archetype x session x duration x context) |
| `src/engine/strategy_backtester.py` | FADE/MOMENTUM/SHAKEOUT rules engine |
| `src/engine/run_portfolio_backtest.py` | Portfolio-level backtest with dedup |
| `src/engine/run_robustness_test.py` | Walk-forward validation + Monte Carlo + decay analysis |
| `src/execution/live_trader.py` | LiveTraderEngine: main trading loop (NSSM service entry) |
| `src/execution/order_manager.py` | Order lifecycle, multi-stage monitors (FADE 2-stage, SHAKEOUT 3-stage) |
| `src/execution/risk_manager.py` | DynamicRiskAllocator: 1-6% risk by WR, SLGuardian |
| `src/execution/mt5_client.py` | MetaTrader5 API wrapper |
| `src/execution/bot_config.json` | 108 active strategies (live portfolio definition) |

## Data Flow

```
CSV (48 files: 15 symbols x 3 TF) → CSVPolarsLoader → DataEnricher (RSI, ATR, OR)
→ TrackerEngine (event timing) → StatisticalEngine (probabilities)
→ StrategyScanner/Backtester (evaluation) → ReportGenerator (MD/HTML output)
```

## Live Trading Flow

```
NSSM Service → scripts/run_bot_supervisor.py → LiveTraderEngine.run()
  → Load 108 strategies from bot_config.json
  → Every 10s: check monitors (FADE/SHAKEOUT), detect fills, SL Guardian
  → At OR close time: evaluate setup, place orders via OrderManager
  → Every 15min: heartbeat → Telegram
```

## Running

- **Live bot:** `python scripts/run_bot_supervisor.py` (on VPS as service)
- **Backtest:** `python -m src.engine.run_portfolio_backtest`
- **Robustness:** `python -m src.engine.run_robustness_test`
- **Strategy discovery:** `python -m src.engine.run_strategy_pipeline`

## Conventions

- **Data processing:** Polars (vectorized, no row-level loops)
- **Risk:** Balance-based (not free_margin), dynamic 1-6% by WR
- **Dedup:** 1 trade per (symbol, edge, session) per day
- **ATR filter:** OR/ATR ratio must be in [0.1, 0.8]
- **Friction:** 0.1R (forex), 0.2R (indices/commodities)
- **Constants:** All magic numbers in `src/domain/constants.py`
- **Config secrets:** `config/broker.yaml`, `config/telegram.yaml` (never commit)

## Active Archetypes

- **FADE:** 2-stage monitor (wait breakout → counter-order). Main live strategy.
- **MOMENTUM:** Direct STOP orders. Dormant — ready for reactivation.
- **SHAKEOUT:** 3-stage monitor (breakout → false break → re-entry). Dormant — ready for reactivation.

## Deploy

- VPS: Windows Server via WinRM (`deploy/` scripts)
- Services: `Kha0sysBot3` (trading), `Kha0sysWatchdog3` (monitoring)
- Telegram: interactive commands via `/status`, `/balance`, `/pnl`, `/positions`, `/health`
