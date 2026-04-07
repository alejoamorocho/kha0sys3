# Audit Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix all 13 bugs/issues found during the exhaustive audit of KHA0SYS3 trading system

**Architecture:** Each fix is independent and can be implemented in parallel. Fixes are grouped by file to minimize conflicts.

**Tech Stack:** Python 3.12, Polars, NumPy, SciPy, MetaTrader5

---

### Task 1: Fix MAGNET_CLOSE chronological SL verification in alpha_sim.py

**Files:**
- Modify: `src/engine/alpha_sim.py:165-180`

The MAGNET_CLOSE evaluation uses `touches_pd_close > 0` without checking if SL was hit first. We need to add time-based verification using `time_sl_up`/`time_sl_down` and `time_entry_up`/`time_entry_down` columns from TrackerEngine.

- [ ] **Step 1: Fix MAGNET_CLOSE logic in run_simulation**

Replace lines 165-180 in `src/engine/alpha_sim.py`:

```python
                elif setup["edge_type"] == "MAGNET_CLOSE":
                    pd_close = row["pd_close"]
                    or_high = row["or_high"]
                    or_low = row["or_low"]

                    if pd_close is None or or_high is None or or_low is None:
                        continue
                    if or_low <= pd_close <= or_high:
                        continue

                    # Determine magnet direction and check SL chronology
                    if pd_close > or_high:
                        # BUY direction: entry at or_high, SL at or_low
                        time_entry = row["time_entry_up"]
                        time_sl = row["time_sl_up"]
                    else:
                        # SELL direction: entry at or_low, SL at or_high
                        time_entry = row["time_entry_down"]
                        time_sl = row["time_sl_down"]

                    # Must have entry (breakout in magnet direction)
                    if time_entry is None:
                        continue

                    # Check if SL was hit before pd_close was touched
                    if row["touches_pd_close"] > 0:
                        # If SL was also hit, check chronology
                        if time_sl is not None and time_sl <= time_entry:
                            # SL hit before or at entry — loss
                            pnl = -1.0 - FRICTION
                        else:
                            pnl = 1.0 - FRICTION
                    else:
                        pnl = -1.0 - FRICTION
```

- [ ] **Step 2: Verify the fix doesn't break the simulation**

Run: `python -c "from src.engine.alpha_sim import AlphaPortfolioSimulator; print('Import OK')"`

---

### Task 2: Fix MAGNET_CLOSE chronological SL verification in compounding_sim.py

**Files:**
- Modify: `src/engine/compounding_sim.py:56-57`

- [ ] **Step 1: Fix MAGNET_CLOSE logic**

Replace lines 54-57 in `src/engine/compounding_sim.py`:

```python
                    if setup["edge"] == "MAGNET_CLOSE":
                        pd_close_val = row["pd_close"]
                        or_high_val = row["or_high"]
                        or_low_val = row["or_low"]

                        if pd_close_val is None or or_high_val is None or or_low_val is None:
                            continue
                        if or_low_val <= pd_close_val <= or_high_val:
                            continue

                        # Determine direction and check SL chronology
                        if pd_close_val > or_high_val:
                            time_entry = row["time_entry_up"]
                            time_sl = row["time_sl_up"]
                        else:
                            time_entry = row["time_entry_down"]
                            time_sl = row["time_sl_down"]

                        if time_entry is None:
                            continue

                        if row["touches_pd_close"] > 0:
                            if time_sl is not None and time_sl <= time_entry:
                                pnl = -1.0 - FRICTION
                            else:
                                pnl = 1.0 - FRICTION
                        else:
                            pnl = -1.0 - FRICTION
```

---

### Task 3: Fix MAGNET_CLOSE chronological SL verification in portfolio_compounder.py

**Files:**
- Modify: `src/engine/portfolio_compounder.py:99-110`

- [ ] **Step 1: Fix MAGNET_CLOSE logic**

Replace lines 99-110 in `src/engine/portfolio_compounder.py`:

```python
                elif setup["edge"] == "MAGNET_CLOSE":
                    pd_close = row["pd_close"]
                    or_high = row["or_high"]
                    or_low = row["or_low"]
                    if pd_close is None or or_high is None or or_low is None:
                        continue
                    if or_low <= pd_close <= or_high:
                        continue

                    # Determine direction and check SL chronology
                    if pd_close > or_high:
                        time_entry = row["time_entry_up"]
                        time_sl = row["time_sl_up"]
                    else:
                        time_entry = row["time_entry_down"]
                        time_sl = row["time_sl_down"]

                    if time_entry is None:
                        continue

                    if row["touches_pd_close"] > 0:
                        if time_sl is not None and time_sl <= time_entry:
                            pnl = -1.0 - FRICTION
                        else:
                            pnl = 1.0 - FRICTION
                    else:
                        pnl = -1.0 - FRICTION
```

---

### Task 4: Fix Monte Carlo — replace permutation with bootstrap

**Files:**
- Modify: `src/engine/statistical_validator.py:13-50`

- [ ] **Step 1: Replace permutation MC with bootstrap**

Replace `monte_carlo` method:

```python
    @staticmethod
    def monte_carlo(pnls: List[float], n_sims: int = 10000) -> Dict[str, Any]:
        """
        Bootstrap with replacement: resamples trades to generate
        different PnL sequences with varying final outcomes.
        Also computes drawdown distribution from shuffled paths.
        """
        pnls_arr = np.array(pnls)
        n = len(pnls_arr)
        if n == 0:
            return {"error": "No trades"}

        final_pnls = np.zeros(n_sims)
        max_drawdowns = np.zeros(n_sims)

        rng = np.random.default_rng(42)
        for i in range(n_sims):
            # Bootstrap: sample WITH replacement (different total each time)
            sample = rng.choice(pnls_arr, size=n, replace=True)
            equity = np.cumsum(sample)
            final_pnls[i] = equity[-1]
            peak = np.maximum.accumulate(equity)
            max_drawdowns[i] = (equity - peak).min()

        return {
            "n_sims": n_sims,
            "n_trades": n,
            "pnl_p5": float(np.percentile(final_pnls, 5)),
            "pnl_p25": float(np.percentile(final_pnls, 25)),
            "pnl_p50": float(np.percentile(final_pnls, 50)),
            "pnl_p75": float(np.percentile(final_pnls, 75)),
            "pnl_p95": float(np.percentile(final_pnls, 95)),
            "pnl_mean": float(final_pnls.mean()),
            "pnl_std": float(final_pnls.std()),
            "dd_p5": float(np.percentile(max_drawdowns, 5)),
            "dd_p50": float(np.percentile(max_drawdowns, 50)),
            "dd_p95": float(np.percentile(max_drawdowns, 95)),
            "prob_ruin": float((final_pnls < 0).mean()),
            "prob_profit": float((final_pnls > 0).mean()),
        }
```

---

### Task 5: Fix FDR null hypothesis for MAGNET_CLOSE (0.55 breakeven)

**Files:**
- Modify: `src/engine/statistical_validator.py:52-103`
- Modify: `src/engine/alpha_sim.py:366-377`

- [ ] **Step 1: Add edge_type-aware null_wr to FDR**

Replace `multiple_testing_correction` method:

```python
    @staticmethod
    def multiple_testing_correction(
        setup_stats: List[Dict], alpha: float = 0.05, null_wr: float = 0.5
    ) -> Dict[str, Any]:
        """
        Benjamini-Hochberg FDR correction.
        Tests H0: win_rate <= null_wr for each setup.
        MAGNET_CLOSE uses null_wr=0.55 (breakeven = 1.1/(0.9+1.1)).
        TREND uses null_wr=0.50.
        """
        if not setup_stats:
            return {"error": "No setups"}

        results = []
        for s in setup_stats:
            n = s["trades"]
            k = s["wins"]
            if n < 10:
                continue
            # Use edge-specific null if available
            if "MAGNET" in s.get("label", ""):
                effective_null = 0.55
            else:
                effective_null = null_wr
            p_value = 1.0 - scipy_stats.binom.cdf(k - 1, n, effective_null)
            results.append({
                "label": s["label"],
                "trades": n,
                "wins": k,
                "observed_wr": s["observed_wr"],
                "null_wr": effective_null,
                "p_value": p_value
            })

        if not results:
            return {"total_tested": 0, "significant_count": 0, "significant_setups": []}

        results.sort(key=lambda x: x["p_value"])
        m = len(results)

        for i, r in enumerate(results):
            bh_threshold = alpha * (i + 1) / m
            r["p_adj"] = min(r["p_value"] * m / (i + 1), 1.0)
            r["significant"] = r["p_value"] <= bh_threshold

        for i in range(m - 2, -1, -1):
            results[i]["p_adj"] = min(results[i]["p_adj"], results[i + 1]["p_adj"])

        significant = [r for r in results if r["significant"]]

        return {
            "total_tested": m,
            "significant_count": len(significant),
            "alpha": alpha,
            "null_wr": null_wr,
            "significant_setups": results
        }
```

---

### Task 6: Fix Optuna SL chronology verification

**Files:**
- Modify: `src/engine/optuna_runner.py:104-118`

- [ ] **Step 1: Fix calculate_pnl to check SL before TP**

Replace lines 104-118:

```python
                    def calculate_pnl(row):
                        ratio = row["or_atr_ratio"]
                        tp = tp_narrow if ratio < 0.3 else tp_normal if ratio < 0.6 else tp_wide
                        
                        dir = row["first_break_dir"]
                        max_ext = row["max_up"] / row["or_width"] if dir == "UP" else row["max_down"] / row["or_width"]
                        
                        # Check SL chronology: if SL hit before TP, it's a loss
                        time_tp_key = f"time_tp_{dir.lower()}"
                        time_sl_key = f"time_sl_{dir.lower()}"
                        time_tp = row.get(time_tp_key)
                        time_sl = row.get(time_sl_key)
                        
                        if max_ext >= tp:
                            # TP level was reached, but did SL hit first?
                            if time_sl is not None:
                                if time_tp is None or time_sl <= time_tp:
                                    return -1.0 - FRICTION  # SL hit first
                            return tp - FRICTION
                        else:
                            return -1.0 - FRICTION
```

Also fix the final evaluation loop (lines 154-162) similarly:

```python
                    for row in valid_final.iter_rows(named=True):
                        ratio = row["or_atr_ratio"]
                        tp = best['tp_narrow'] if ratio < 0.3 else best['tp_normal'] if ratio < 0.6 else best['tp_wide']
                        
                        dir = row["first_break_dir"]
                        max_ext = row["max_up"] / row["or_width"] if dir == "UP" else row["max_down"] / row["or_width"]
                        trade_date = row["trade_date"]
                        
                        # Check SL chronology
                        time_sl = row.get(f"time_sl_{dir.lower()}")
                        time_tp = row.get(f"time_tp_{dir.lower()}")
                        
                        if max_ext >= tp:
                            if time_sl is not None and (time_tp is None or time_sl <= time_tp):
                                r_net = -1.0 - FRICTION
                            else:
                                r_net = tp - FRICTION
                        else:
                            r_net = -1.0 - FRICTION
```

---

### Task 7: Fix Edge Reports probability calculation (>100% bug)

**Files:**
- Modify: `src/application/statistics.py:111-114`

The `p_touch_pd_close` is correctly using binary filter (`> 0`), but the Edge Reports were generated with old code. The fix is to regenerate reports after all other fixes are applied. No code change needed here — the current `statistics.py` code is correct (uses `.height / total_days` which maxes at 1.0).

- [ ] **Step 1: Verify statistics.py is correct**

Check that line 111 uses binary filter:
```python
t_pd_close = valid_df.filter(pl.col("touches_pd_close") > 0).height / total_days
```
This is correct. Reports just need regeneration.

---

### Task 8: Fix Friction to be asset-specific

**Files:**
- Modify: `src/engine/alpha_sim.py:115`
- Modify: `src/engine/portfolio_compounder.py:60`
- Modify: `src/engine/compounding_sim.py:34`

- [ ] **Step 1: Add asset-specific friction in alpha_sim.py**

Replace line 115:

```python
        # Asset-specific friction: indices have wider spreads in pre-market
        INDEX_SYMBOLS = {"SP500", "NASDAQ100", "VIX"}
        FRICTION_DEFAULT = 0.1
        FRICTION_INDEX = 0.2
```

Then in the trade evaluation (around line 157), use:

```python
                friction = FRICTION_INDEX if sym in INDEX_SYMBOLS else FRICTION_DEFAULT
```

And replace all `FRICTION` references in pnl calculations with `friction`.

- [ ] **Step 2: Apply same pattern in portfolio_compounder.py**

Replace line 60-61:

```python
        INDEX_SYMBOLS = {"SP500", "NASDAQ100", "VIX"}
        FRICTION_DEFAULT = 0.1
        FRICTION_INDEX = 0.2
        friction = FRICTION_INDEX if sym in INDEX_SYMBOLS else FRICTION_DEFAULT
```

- [ ] **Step 3: Apply same pattern in compounding_sim.py**

Replace line 34:

```python
        INDEX_SYMBOLS = {"SP500", "NASDAQ100", "VIX"}
        FRICTION_DEFAULT = 0.1
        FRICTION_INDEX = 0.2
```

Then use per-trade friction based on symbol.

---

### Task 9: Fix /stop to cancel pending orders

**Files:**
- Modify: `src/execution/live_trader.py:89-91`

- [ ] **Step 1: Cancel all pending orders on /stop**

```python
    def _on_stop_command(self):
        with self._control_lock:
            self._paused = True
        # Cancel all pending bot orders
        if self.om:
            orders = mt5.orders_get()
            if orders:
                for o in orders:
                    if o.magic == 1337:
                        self.om.cancel_order_by_ticket(o.ticket, o.symbol)
```

---

### Task 10: Fix FOK hardcoded — use broker's filling mode

**Files:**
- Modify: `src/execution/order_manager.py:201`

- [ ] **Step 1: Query filling mode from symbol info**

Replace line 201:

```python
            "type_filling": self._get_filling_mode(symbol),
```

Add method to OrderManager:

```python
    def _get_filling_mode(self, symbol: str) -> int:
        """Use broker-supported filling mode instead of hardcoded FOK."""
        sym_info = mt5.symbol_info(symbol)
        if sym_info is None:
            return mt5.ORDER_FILLING_FOK
        modes = sym_info.filling_mode
        if modes & mt5.SYMBOL_FILLING_FOK:
            return mt5.ORDER_FILLING_FOK
        elif modes & mt5.SYMBOL_FILLING_IOC:
            return mt5.ORDER_FILLING_IOC
        else:
            return mt5.ORDER_FILLING_RETURN
```

---

### Task 11: Fix state persistence for dedup across restarts

**Files:**
- Modify: `src/execution/order_manager.py`
- Modify: `src/execution/live_trader.py`

- [ ] **Step 1: Add state persistence to OrderManager**

Add to OrderManager:

```python
    STATE_FILE = "data/live_state/daily_trades.json"

    def _save_state(self):
        """Persist dedup state to disk."""
        import json, os
        os.makedirs(os.path.dirname(self.STATE_FILE), exist_ok=True)
        state = {
            "daily_trades": self._daily_trades,
            "last_reset": self._last_daily_reset,
        }
        with open(self.STATE_FILE, "w") as f:
            json.dump(state, f)

    def _load_state(self):
        """Restore dedup state from disk."""
        import json
        try:
            with open(self.STATE_FILE, "r") as f:
                state = json.load(f)
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            if state.get("last_reset") == today:
                self._daily_trades = state.get("daily_trades", {})
                self._last_daily_reset = state["last_reset"]
        except (FileNotFoundError, json.JSONDecodeError):
            pass
```

Call `_load_state()` in `__init__` and `_save_state()` in `mark_traded_today()`.

---

### Task 12: Fix double counting of _trades_today

**Files:**
- Modify: `src/execution/live_trader.py:402-403`

- [ ] **Step 1: Remove duplicate increment**

Remove `self._trades_today += 1` from line 403 in `_process_symbol()`. The increment at line 265 (in `_check_positions_and_fills`) is the correct one — it triggers on actual fill detection.

---

### Task 13: Fix Decay Analysis — use linear regression

**Files:**
- Modify: `src/engine/statistical_validator.py:160-183`

- [ ] **Step 1: Replace ratio-based decay with Spearman correlation**

Replace decay score calculation:

```python
        # Decay score using Spearman rank correlation of expectancies over time
        expectancies = [w["expectancy"] for w in windows]
        if len(expectancies) >= 3:
            from scipy.stats import spearmanr
            x = list(range(len(expectancies)))
            corr, p_value = spearmanr(x, expectancies)
            # Map correlation to decay score: 1.0 = stable, >1 = improving, <1 = degrading
            decay_score = 1.0 + corr  # -1 to +1 mapped to 0 to 2
            decay_p_value = p_value
        else:
            first_half = np.mean(expectancies[:len(expectancies)//2])
            second_half = np.mean(expectancies[len(expectancies)//2:])
            if first_half > 0:
                decay_score = second_half / first_half
            elif first_half == 0:
                decay_score = 1.0 if second_half >= 0 else 0.0
            else:
                decay_score = 0.0
            decay_score = max(0.0, min(2.0, decay_score))
            decay_p_value = None

        return {
            "windows": windows,
            "decay_score": float(decay_score),
            "decay_p_value": float(decay_p_value) if decay_p_value is not None else None,
            "trend": "MEJORANDO" if decay_score > 1.1 else (
                "ESTABLE" if decay_score >= 0.7 else (
                    "DEGRADANDO" if decay_score >= 0.3 else "COLAPSANDO"
                )
            )
        }
```
