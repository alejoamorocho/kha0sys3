# KHA0SYS3 Strategy Guide

## Overview

Kha0sys3 is a quantitative trading system based on Opening Range Breakout (ORB) methodology with statistical edge validation. It trades 5 instruments across 3 sessions using TREND_UP edge, validated through walk-forward out-of-sample testing with Monte Carlo confidence intervals.

## Portfolio (Live — April 2026)

| Symbol | MT5 Symbol | Session | Edge | Time (UTC) | OR Durations |
|---|---|---|---|---|---|
| USDJPY | USDJPY+ | Tokyo | TREND_UP | 00:00 | 15m, 30m |
| Gold | XAUUSD+ | London | TREND_UP | 07:00 | 15m, 30m |
| EURUSD | EURUSD+ | London | TREND_UP | 07:00 | 15m, 30m |
| Oil (WTI) | USOUSD | London | TREND_UP | 07:00 | 15m, 30m |
| S&P 500 | SP500 | Pre-Market | TREND_UP | 12:00 | 15m, 30m |

**Decorrelation:**
- 3 time zones (Tokyo / London / Pre-Market)
- 5 asset classes (JPY FX, Metal, EUR FX, Commodity, Index)

Note: MAGNET_CLOSE edge was removed from the live portfolio. The code still supports it but no active setups use it.

## Edge Types

### TREND_UP

**Logic:** After the Opening Range forms, if price breaks above OR high first, enter long targeting 1.5x OR width.

- **Entry:** BUY_STOP at OR high
- **TP:** OR high + (OR width x 1.5) = net +1.4R after friction
- **SL:** OR low = -1.1R after friction
- **Gate:** If price breaks OR low first (DOWN), cancel BUY_STOP (software monitoring). Backtest equivalent: `first_break_dir == "UP"`

### MAGNET_CLOSE

**Logic:** After OR forms, if previous day's close (pd_close) is outside the OR, price tends to gravitate toward it. Enter in the direction of pd_close.

- **If pd_close > OR high:** BUY_STOP at OR high, TP at pd_close
- **If pd_close < OR low:** SELL_STOP at OR low, TP at pd_close
- **Skip:** If pd_close is inside OR (already reached)
- **SL:** Opposite OR boundary

## Filters

### ATR14 Filter
- `or_atr_ratio = OR_width / ATR(14)`
- Valid range: `[0.1, 0.8]`
- Below 0.1: OR too narrow (noise)
- Above 0.8: OR too wide (volatile, SL too large)
- ATR(14) = SMA of 14 True Ranges from D1, shifted 1 day (no look-ahead)

### Spread Filter
- Current spread must be <= 1.5x average spread
- Floor minimum of 5 points to avoid false positives

### Waterfall Duration
- Try 15m OR first. If ATR filter rejects it, try 30m OR
- If both fail, skip the day for that asset

## Risk Management

| Parameter | Value |
|---|---|
| Risk per trade | 3% of account balance |
| Position sizing | Based on BALANCE (not free_margin) |
| Max concurrent | 5 setups (5 symbols, all TREND_UP) |
| Dedup | 1 trade/day per (symbol, edge) |
| Order expiration | 8 hours from OR close |
| Session window | magic_time + OR duration to magic_time + 8h |

### Position Sizing Formula
```
risk_money = balance x 0.03
ticks_at_risk = |entry - SL| / tick_size
loss_per_lot = ticks_at_risk x tick_value
lots = floor(risk_money / loss_per_lot / volume_step) x volume_step
```

## OOS Validation Results

### Walk-Forward (5 folds, expanding window)

| Fold | Train Period | Test Period | Setups | OOS Trades | OOS PnL | OOS WR |
|---|---|---|---|---|---|---|
| 1 | -> 2022-02 | 2022-02 -> 2022-12 | 94 | 1,366 | +783 R | 68.7% |
| 2 | -> 2022-12 | 2022-12 -> 2023-10 | 97 | 1,478 | +815 R | 68.9% |
| 3 | -> 2023-10 | 2023-10 -> 2024-07 | 88 | 1,264 | +892 R | 75.3% |
| 4 | -> 2024-07 | 2024-07 -> 2025-05 | 90 | 1,302 | +715 R | 69.0% |
| 5 | -> 2025-05 | 2025-05 -> 2026-03 | 91 | 1,336 | +769 R | 69.2% |

### Portfolio Performance (OOS)

| Metric | Value |
|---|---|
| Win Rate | 69.9% |
| Profit Factor | 2.76 |
| Expectancy | 0.583 R per trade |
| Max Drawdown | -11.2% |
| Trades/Year | ~1,022 |
| Decay Score | 0.92 (stable) |

### Per-Setup Breakdown (OOS)

| Setup | Trades | WR | PF | PnL (R) |
|---|---|---|---|---|
| XAUUSD London TREND_UP | 698 | 72.3% | 3.44 | +494.7 |
| EURUSD London TREND_UP | 744 | 68.0% | 2.88 | +446.6 |
| USDJPY Tokyo TREND_UP | 729 | 68.3% | 3.46 | +443.1 |
| WTI London TREND_UP | 646 | 70.7% | 3.48 | +431.9 |
| SP500 Pre-Market TREND_UP | 604 | 71.7% | 4.22 | +418.1 |
| EURUSD London MAGNET_CLOSE | 790 | 69.0% | 2.27 | +221.0 |

### Monte Carlo (10,000 permutations)

| Metric | P5 | P50 | P95 |
|---|---|---|---|
| Max Drawdown | -20.9% | -13.1% | -9.6% |
| Prob reaching $20k from $1k | 100% | | |
| Prob of ruin (<$100) | 0% | | |

### Edge Decay Analysis

| Period | Trades | WR | Expectancy | Status |
|---|---|---|---|---|
| 2022-02 to 2023-02 | 1,058 | 69.2% | 0.567 R | STABLE |
| 2023-02 to 2024-02 | 1,012 | 71.9% | 0.627 R | STABLE |
| 2024-02 to 2025-02 | 1,002 | 71.0% | 0.617 R | STABLE |
| 2025-02 to 2026-02 | 1,032 | 67.9% | 0.532 R | STABLE |

### FDR Correction (Benjamini-Hochberg)

23 out of 28 setups are statistically significant at alpha=0.05 after multiple testing correction. All 6 setups in the live portfolio passed FDR.

## Compounding Projection ($1,000 -> $20,000)

With 3% risk compounding:
- $2,000 reached at trade #31
- $5,000 reached at trade #85
- $10,000 reached at trade #119
- $20,000 reached at trade #156 (~2 months OOS)

## System Architecture

### Live Trading
- **Engine:** `src/execution/live_trader.py` (LiveTraderEngine)
- **Orders:** `src/execution/order_manager.py` (OrderManager)
- **MT5 Gateway:** `src/execution/mt5_client.py` (MT5Client)
- **Risk:** `src/execution/risk_manager.py` (DynamicRiskAllocator)
- **Config:** `src/execution/bot_config.json`

### Monitoring
- **Telegram Bot:** Interactive commands (/status, /balance, /pnl, /positions, etc.)
- **System Health:** CPU, RAM, Disk, MT5 process monitoring
- **Watchdog:** Independent NSSM service monitors bot heartbeat

### Backtesting
- **Alpha Sim:** `src/engine/alpha_sim.py` (walk-forward OOS)
- **Compounder:** `src/engine/portfolio_compounder.py` (compounding simulation)
- **Validator:** `src/engine/statistical_validator.py` (Monte Carlo, FDR, decay)

## Broker

- **Broker:** Vantage International (ECN)
- **Server:** VantageInternational-Live 5
- **Leverage:** 1:500
- **Platform:** MetaTrader 5

## Backtest-Live Parity Checklist

| Element | Backtest | Live | Match |
|---|---|---|---|
| OR source | M15 closed bars | get_or_from_closed_bars() | Yes |
| ATR14 | SMA(14) TR, D1, shift 1 | calculate_atr14() | Yes |
| ATR filter | [0.1, 0.8] | _passes_atr_filter() | Yes |
| TREND gate | first_break_dir==UP | Software monitor + cancel | Yes |
| TREND TP | 1.5x OR width | Fixed 1.5R | Yes |
| MAGNET dir | pd_close vs OR | pd_close vs OR | Yes |
| Dedup | (date, sym, edge) | has_traded_today(sym, edge) | Yes |
| Waterfall | 15m then 30m | Scheduled retry | Yes |
| Risk | 3% balance | 3% balance | Yes |
| Expiration | 8h window | ORDER_TIME_SPECIFIED 8h | Yes |
