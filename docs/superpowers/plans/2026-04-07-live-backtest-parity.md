# Live Backtest Parity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Modify the live trading bot to execute identical logic to the validated backtest portfolio with 5 assets, waterfall durations, edge-specific order placement, and 3% risk.

**Architecture:** Update bot_config.json with new portfolio, refactor live_trader.py for waterfall + edge routing, add sentinel/magnet order types to order_manager.py, add pd_close to mt5_client.py, update telegram notifications.

**Tech Stack:** Python 3.12, MetaTrader5, python-telegram-bot, NSSM (Windows service)

---

### Task 1: Update bot_config.json

**Files:**
- Modify: `src/execution/bot_config.json`

- [ ] **Step 1: Replace config with new portfolio**

- [ ] **Step 2: Commit**

---

### Task 2: Add get_previous_day_close to MT5Client

**Files:**
- Modify: `src/execution/mt5_client.py`

- [ ] **Step 1: Add method**
- [ ] **Step 2: Commit**

---

### Task 3: Update OrderManager with TREND_UP sentinel + MAGNET + close_position_market

**Files:**
- Modify: `src/execution/order_manager.py`

- [ ] **Step 1: Add close_position_market()**
- [ ] **Step 2: Add place_trend_up_orders()**
- [ ] **Step 3: Add place_magnet_order()**
- [ ] **Step 4: Update has_traded_today/mark_traded_today to accept edge**
- [ ] **Step 5: Commit**

---

### Task 4: Refactor LiveTraderEngine for waterfall + edge routing + sentinel handling

**Files:**
- Modify: `src/execution/live_trader.py`

- [ ] **Step 1: Update config loading for new portfolio format**
- [ ] **Step 2: Implement waterfall duration scheduling**
- [ ] **Step 3: Implement edge routing in _process_symbol()**
- [ ] **Step 4: Add sentinel fill handling in _check_positions_and_fills()**
- [ ] **Step 5: Update dedup to (symbol, edge)**
- [ ] **Step 6: Commit**

---

### Task 5: Update Telegram notifications for new edge types

**Files:**
- Modify: `src/monitoring/telegram_notifier.py`
- Modify: `src/monitoring/telegram_bot.py`

- [ ] **Step 1: Add edge-aware notifications (TREND_UP, MAGNET, SENTINEL)**
- [ ] **Step 2: Update bot_started to show edge types**
- [ ] **Step 3: Add /portfolio command showing current setups**
- [ ] **Step 4: Commit**

---

### Task 6: Update risk_manager default

**Files:**
- Modify: `src/execution/risk_manager.py`

- [ ] **Step 1: Change default to 0.03**
- [ ] **Step 2: Commit**

---

### Task 7: Create Strategy Guide markdown

**Files:**
- Create: `reports/KHA0SYS3_Strategy_Guide.md`

- [ ] **Step 1: Write comprehensive guide with OOS results**
- [ ] **Step 2: Commit**

---

### Task 8: Update memory + final commit + push

- [ ] **Step 1: Update MEMORY.md**
- [ ] **Step 2: Final git push**

---

### Task 9: VPS deployment script

**Files:**
- Create: `scripts/deploy_new_strategy.ps1`

- [ ] **Step 1: Create PowerShell deployment script**
