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
| `src/execution/order_manager.py` | Order lifecycle: FADE immediate LIMIT + direction guard, SHAKEOUT 3-stage |
| `src/execution/risk_manager.py` | DynamicRiskAllocator: 1-6% risk by WR, SLGuardian |
| `src/execution/mt5_client.py` | MetaTrader5 API wrapper |
| `src/execution/bot_config.json` | 108 active strategies with per-strategy R:R (tp_mult/sl_mult) |
| `src/engine/run_portfolio_backtest_rr.py` | Portfolio backtest using per-strategy R:R from bot_config |
| `src/engine/run_rr_exploration_v2.py` | R:R grid search optimizer (TP x SL per strategy) |
| `src/engine/run_mc_global_vs_individual.py` | Monte Carlo comparison: global vs individual R:R |

## Data Flow

```
CSV (48 files: 15 symbols x 3 TF) → CSVPolarsLoader → DataEnricher (RSI, ATR, OR)
→ TrackerEngine (event timing) → StatisticalEngine (probabilities)
→ StrategyScanner/Backtester (evaluation) → ReportGenerator (MD/HTML output)
```

## Live Trading Flow

```
NSSM Service → scripts/run_bot_supervisor.py → LiveTraderEngine.run()
  → Load 108 strategies from bot_config.json (each with tp_mult/sl_mult)
  → Every 10s: check FADE_GUARD + SHAKEOUT monitors, detect fills, SL Guardian
  → At OR close time: place SELL_LIMIT/BUY_LIMIT at OR boundary with per-strategy TP/SL
  → Direction guard: cancel order if wrong direction breaks first
  → Every 15min: heartbeat → Telegram
```

## Running

- **Live bot (FADE):** `python scripts/run_bot_supervisor.py` (on VPS as service)
- **Live bot (MATH):** `python scripts/run_math_bot_supervisor.py` (on VPS as service, magic 1338)
- **Backtest (R:R):** `python -m src.engine.run_portfolio_backtest_rr`
- **Backtest (legacy 1:1):** `python -m src.engine.run_portfolio_backtest`
- **R:R exploration:** `python -m src.engine.run_rr_exploration_v2`
- **MC comparison:** `python -m src.engine.run_mc_global_vs_individual`
- **Robustness (FADE):** `python -m src.engine.run_robustness_test`
- **Robustness (MATH):** `python -m src.engine.robustness_math_optuna`
- **Strategy discovery:** `python -m src.engine.run_strategy_pipeline`
- **Optuna 3-regime (MATH):** `python -m src.engine.optuna_three_regimes`
- **Build math config from Optuna:** `python scripts/build_bot_config_math_optuna.py`

## Conventions

- **Data processing:** Polars (vectorized, no row-level loops)
- **Risk:** Balance-based (not free_margin), dynamic tiered by balance (<$2k: 2.5-15%, $2k-$8k: 1.67-10%, >$8k: 1-6%)
- **Dedup:** 1 trade per (symbol, edge, session) per day
- **ATR filter:** OR/ATR ratio must be in [0.1, 0.8]
- **Friction:** 0.1R (forex), 0.2R (indices/commodities)
- **R:R:** Per-strategy tp_mult/sl_mult in bot_config.json (see R:R Design below)
- **Constants:** All magic numbers in `src/domain/constants.py`
- **Config secrets:** `config/broker.yaml`, `config/telegram.yaml` (never commit)

## R:R Design (Individual per Strategy)

Each strategy in `bot_config.json` has its own `tp_mult` and `sl_mult` (multiples of OR_WIDTH):

| R:R Config | Count | Description |
|-----------|-------|-------------|
| TP=0.50 SL=2.50 | 59 | Take profit at half OR width, wide stop |
| TP=0.75 SL=2.50 | 37 | Take profit at 3/4 OR width, wide stop |
| TP=0.50 SL=2.00 | 5 | Slightly tighter stop |
| TP=0.75 SL=2.00 | 4 | Mid-range |
| TP=0.75 SL=1.25-1.50 | 3 | Tight stop (XAGUSD London DOWN, SP500 Pre-Market) |

**Why individual R:R:** Grid search (48 combos per strategy) found that 49 strategies
perform better with TP=0.75 instead of the global TP=0.50. The individual approach
yields +$85k (+7.7%) more profit, -1.9% less drawdown, and +209R more Net R vs global.
Validated: MC ruina 0.0%, WF OOS WR 91.5%, decay MEJORANDO. See `reports/RR_Exploration_v2.md`.

**FADE order mechanics (backtest parity):**
- Entry: SELL_LIMIT at OR_HIGH (FADE_UP) / BUY_LIMIT at OR_LOW (FADE_DOWN) placed at OR close
- TP: entry - tp_mult * OR_WIDTH (FADE_UP) / entry + tp_mult * OR_WIDTH (FADE_DOWN)
- SL: entry + sl_mult * OR_WIDTH (FADE_UP) / entry - sl_mult * OR_WIDTH (FADE_DOWN)
- Direction guard: cancels order if opposite OR boundary breaks first (= first_break_dir filter)

## Active Archetypes

- **FADE:** Immediate LIMIT at OR boundary + direction guard. TP/SL optimized per strategy.
- **MOMENTUM:** Direct STOP orders. Dormant — ready for reactivation.
- **SHAKEOUT:** 3-stage monitor (breakout → false break → re-entry). Dormant — ready for reactivation.

## Math Parallel Runner

A second isolated process runs **35 math-indicator strategies** on the SAME
VPS1, Vantage account, and Telegram bot as the FADE bot, but with strict
process separation.

| Component | FADE bot | MATH bot |
|-----------|--------------------|-----------------|
| NSSM service | `Kha0sysBot3` | `Kha0sysMathBot` |
| Entry | `scripts/run_bot_supervisor.py` | `scripts/run_math_bot_supervisor.py` |
| Engine | `src/execution/live_trader.py` | `src/execution/live_math_trader.py` |
| Orders | `src/execution/order_manager.py` | `src/execution/math_order_manager.py` |
| Config | `src/execution/bot_config.json` (108) | `src/execution/bot_config_math.json` (35) |
| Magic | `1337` | `1338` |
| Mechanics | FADE LIMIT + direction guard | STOP at close±0.5×ATR, FLIPPED direction, 5-bar wait, guard cancel |
| Default mode | LIVE | **DRY_RUN** (flip manually after telemetry) |

All MT5 reads in the MATH runner filter by `magic=1338`, so it never observes
or touches FADE orders. `--dry-run` (default) emits `[MATH][DRY]` telegram
messages instead of calling `mt5.order_send`. Deploy with
`python deploy/deploy_math_bot.py`; flip to `--live` manually on the VPS after
observing DRY telemetry for at least one full session.

### Math portfolio (ELITE WR>=65% multi-TF, 2026-05-03)

- **34 strategies** filtered for high WR + low capital deployment: WR≥65%, FUERTE only, MC ruin≤1%, PF OOS≥1.5
- **Timeframes:** M15 (1) + H1 (10) + H4 (23) — single bot, multi-TF dispatch
- **5 setups:** OLS_SLOPE_STRONG, HURST_TREND_MOM, KALMAN_INNOV_EXPAND, SPECTRAL_TREND_MOM, GARCH_Z_FADE
- **9 symbols:** AUDUSD, EURJPY, EURUSD, GBPAUD, GBPJPY, GBPUSD, USDJPY, XAGUSD, XAUUSD
- **5 sessions:** ASIA, LONDON, NY, LONDON_NY, ALL_DAY
- TP/SL Optuna 3-regime per strategy under realistic Vantage friction + 0.2R slippage
- Avg WR=68.98%, Avg PF IS=2.70, Avg PF OOS=2.76, Avg DD=7.25 R, Avg MC ruin=0.0%
- **Multi-TF dispatch:** engine processes M15 setups every :00/:15/:30/:45, H1 setups every HH:00, H4 setups every 0/4/8/12/16/20 broker hour
- **Pre-elite history:** M15-only portfolio of 35 strategies (Optuna 3-regime) preserved in `bot_config_math.json.bak_pre_elite`
- Reports: `reports/elite_wr65_portfolio.parquet`, `reports/Math_H1_Robustness.md`, `reports/Math_H4_Robustness.md`

### Math bot Telegram events

Startup snapshot (with TF distribution and avg WR) · 15-min HEARTBEAT (per-TF setup count) · ORDER PLACED (with TF and R:R fields) · LIVE FILL · LIVE CLOSE (with R-multiple, auto-detected via positions diff) · VIRTUAL FILL/CLOSE (DRY) · GUARD CANCEL · SL GUARDIAN CLOSE · SESSION-END TIME-STOP · STALE SWEEP · retcode handlers (10015/10016/10022/10030) · DRY daily report. All messages structured multi-line, no emojis. MT5 order comment now includes TF: `M|<TF>|<setup>|<sess>`.

## Deploy

- VPS: Windows Server via WinRM (`deploy/` scripts)
- Services: `Kha0sysBot3` (FADE, magic 1337), `Kha0sysMathBot` (MATH inverted momentum, magic 1338, DRY_RUN default), `Kha0sysWatchdog3` (monitoring)
- Telegram: interactive commands via `/status`, `/balance`, `/pnl`, `/positions`, `/health`
