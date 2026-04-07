# Live Trading Backtest Parity — Design Spec

## Goal

Modify the live trading bot to execute the exact same logic as the validated backtest portfolio. Every trade decision in live must produce the same outcome as the backtest given the same market data.

## Portfolio

| Symbol (Vantage) | Session | Edge | magic_time | Durations |
|---|---|---|---|---|
| USDJPY+ | Tokyo | TREND_UP | 00:00 | [15, 30] |
| XAUUSD | London | TREND_UP | 07:00 | [15, 30] |
| EURUSD+ | London | TREND_UP | 07:00 | [15, 30] |
| EURUSD+ | London | MAGNET_CLOSE | 07:00 | [15, 30] |
| WTI (verify Vantage name) | London Initial | TREND_UP | 07:00 | [15, 30] |
| SP500 (verify Vantage name) | Pre-Market | TREND_UP | 12:00 | [15, 30] |

Risk: 3% per trade. Dedup: 1 trade/day per (symbol, edge).

## Changes by File

### 1. `src/execution/bot_config.json`

Replace the entire config:

```json
{
  "portfolio": [
    {"sym": "USDJPY+",  "magic_time": "00:00", "edge": "TREND_UP",     "durations": [15, 30]},
    {"sym": "XAUUSD",   "magic_time": "07:00", "edge": "TREND_UP",     "durations": [15, 30]},
    {"sym": "EURUSD+",  "magic_time": "07:00", "edge": "TREND_UP",     "durations": [15, 30]},
    {"sym": "EURUSD+",  "magic_time": "07:00", "edge": "MAGNET_CLOSE", "durations": [15, 30]},
    {"sym": "USOIL",    "magic_time": "07:00", "edge": "TREND_UP",     "durations": [15, 30]},
    {"sym": "SP500",    "magic_time": "12:00", "edge": "TREND_UP",     "durations": [15, 30]}
  ],
  "risk_percent_per_trade": 0.03
}
```

Note: WTI/SP500 Vantage symbol names must be verified before deploy.

### 2. `src/execution/live_trader.py`

#### 2a. Config loading

Read `portfolio` instead of `trinity_portfolio`. Each setup has `edge` and `durations` fields.

#### 2b. Waterfall duration logic

Replace the single `_process_symbol()` call with a waterfall approach:

```
At magic_time + durations[0] minutes:
  1. Get OR for duration[0] (e.g., 15m)
  2. If ATR filter passes → place orders → done
  3. If ATR fails → schedule retry for duration[1] (e.g., 30m)

At magic_time + durations[1] minutes:
  1. Get OR for duration[1] (e.g., 30m)
  2. If ATR filter passes → place orders → done
  3. If ATR fails → skip day
```

Implementation: change `_should_execute()` to check against `magic_time + duration` instead of just `magic_time`. Track which duration index each setup is at via `_waterfall_state: dict[str, int]`.

The dedup key for `_last_fired` changes to `(sym, edge, duration_index)` to allow retries at different durations.

#### 2c. Edge routing in `_process_symbol()`

After OR and ATR checks pass, route based on `setup["edge"]`:

**TREND_UP:**
- TP = or_high + (or_width * 1.5)
- SL_up = or_low
- Call `om.place_trend_up_orders(sym, or_high, or_low, tp_up)`

**MAGNET_CLOSE:**
- Get pd_close via `client.get_previous_day_close(sym)`
- Skip if pd_close is inside OR (or_low <= pd_close <= or_high)
- If pd_close > or_high: BUY direction, TP = pd_close
- If pd_close < or_low: SELL direction, TP = pd_close
- Call `om.place_magnet_order(sym, or_high, or_low, pd_close, direction)`

#### 2d. Dedup per (symbol, edge)

Change `has_traded_today()` and `mark_traded_today()` to accept `edge` parameter. The key becomes `f"{symbol}_{edge}"`.

#### 2e. Sentinel fill handling

In `_check_positions_and_fills()`, when detecting a new fill:
- Check the position's `comment` field
- If comment == "SENTINEL": close position immediately via market order, cancel opposite pending orders, mark traded_today. Do NOT notify as a real trade.
- If comment == "TREND_UP" or "MAGNET_xxx": normal flow (cancel opposite leg, mark traded)

### 3. `src/execution/order_manager.py`

#### 3a. `place_trend_up_orders(symbol, or_high, or_low, tp_up)`

Places 2 orders:
1. **BUY_STOP** at `or_high`, SL = `or_low`, TP = `tp_up`, comment = `"TREND_UP"`
2. **SELL_STOP sentinel** at `or_low`, SL = `or_low`, TP = `or_low`, comment = `"SENTINEL"`

The sentinel has SL=TP=entry so it effectively closes at breakeven. However, MT5 may reject SL/TP at entry price. Fallback: set SL 1 tick below entry (minimal loss), TP at entry. The key is that when it fills, the 10s loop detects it and closes immediately.

Actually, simplest approach: sentinel SELL_STOP has normal SL/TP (same as a real trade), but the comment "SENTINEL" tells the fill handler to close it immediately. This avoids broker rejection issues.

Sentinel SELL_STOP: entry = or_low, SL = or_high, TP = or_low - (width * 1.5), comment = "SENTINEL". These SL/TP values won't matter because the position gets closed immediately on fill detection.

#### 3b. `place_magnet_order(symbol, or_high, or_low, pd_close, direction)`

Places 1 order:
- If direction == "UP": BUY_STOP at `or_high`, SL = `or_low`, TP = `pd_close`, comment = `"MAGNET_UP"`
- If direction == "DOWN": SELL_STOP at `or_low`, SL = `or_high`, TP = `pd_close`, comment = `"MAGNET_DW"`

No sentinel needed — the trade direction is predetermined by pd_close position.

#### 3c. `close_position_market(ticket)`

New method to immediately close a sentinel fill via market order.

```python
def close_position_market(self, ticket: int, symbol: str, volume: float, position_type: int):
    close_type = mt5.ORDER_TYPE_SELL if position_type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY
    price = mt5.symbol_info_tick(symbol).bid if close_type == mt5.ORDER_TYPE_SELL else mt5.symbol_info_tick(symbol).ask
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": close_type,
        "position": ticket,
        "price": price,
        "deviation": 20,
        "magic": BOT_MAGIC_NUMBER,
        "comment": "SENTINEL_CLOSE",
    }
    return self.client.send_order_raw(request)
```

#### 3d. Update `has_traded_today` / `mark_traded_today`

Accept `edge` parameter. Key changes from `symbol` to `f"{symbol}_{edge}"`.

### 4. `src/execution/mt5_client.py`

#### 4a. `get_previous_day_close(symbol)`

```python
def get_previous_day_close(self, symbol: str) -> Optional[float]:
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_D1, 1, 1)
    if rates is None or len(rates) == 0:
        return None
    return rates[0].close
```

This returns yesterday's D1 close. Shifted by 1 (index 1 = previous completed day).

Consistency with backtest: `DataEnricher.enrich_with_daily_context()` uses `pl.col("d_close").shift(1)` which is the same — the close of the previous day.

### 5. `src/execution/risk_manager.py`

Change default from 0.035 to 0.03. This is also set via config, so the config value takes precedence.

## Backtest-Live Parity Audit Checklist

| # | Element | Backtest Code | Live Code | Parity |
|---|---|---|---|---|
| 1 | OR source | M15 closed bars, aggregated | `get_or_from_closed_bars(sym, dur)` | Same |
| 2 | ATR14 | SMA(14) of TR, D1, shift 1 | `calculate_atr14()` — same formula | Same |
| 3 | ATR filter | `or_atr_ratio in [0.1, 0.8]` | `_passes_atr_filter()` — same range | Same |
| 4 | TREND_UP gate | `first_break_dir == "UP"` | BUY_STOP + sentinel SELL_STOP | Same outcome |
| 5 | TREND_UP TP | `or_high + 1.5 * or_width` | Fixed 1.5R | Same |
| 6 | TREND_UP SL | `or_low` (opposite OR boundary) | SL = or_low | Same |
| 7 | TREND_UP pnl | Win: +1.4R, Loss: -1.1R | TP hit: ~+1.4R, SL hit: ~-1.1R | Same (real spread varies) |
| 8 | MAGNET direction | pd_close outside OR determines dir | pd_close vs or_high/or_low | Same |
| 9 | MAGNET skip | `or_low <= pd_close <= or_high` → skip | Same check | Same |
| 10 | MAGNET TP | `touches_pd_close > 0` → win | TP at pd_close price | Same |
| 11 | MAGNET SL | -1.1R | SL at opposite OR boundary | Same |
| 12 | Dedup | `(date, symbol, edge)` | `has_traded_today(symbol, edge)` | Same |
| 13 | Waterfall | Try all durations, take earliest | 15m first, 30m if ATR fails | Same net effect |
| 14 | Risk sizing | 3% of balance, compounded | 3% of balance via allocator | Same |
| 15 | Session window | 8h post-OR | ORDER_EXPIRATION_HOURS = 8 | Same |
| 16 | Friction | -0.1R simulated flat | Real spread + commission | Live is more accurate |
| 17 | Timezone | UTC throughout | UTC throughout | Same |
| 18 | pd_close source | `d_close.shift(1)` from daily agg | `copy_rates D1, index 1` | Same |

## Known Differences (Acceptable)

1. **Friction**: Backtest uses flat -0.1R. Live pays real spread + commission. Live is more realistic.
2. **Fill timing**: Backtest assumes instant fill at OR boundary. Live may get slight slippage (deviation=10 points).
3. **Sentinel cost**: The sentinel SELL_STOP, when filled, costs a small spread before closing. Backtest has no equivalent cost. Acceptable — it's a few cents per sentinel fill.

## Deployment Notes

1. Verify Vantage symbol names: XAUUSD, WTI (may be USOIL, OIL, or CRUDEOIL), SP500 (may be US500 or SPX500)
2. Update bot_config.json on VPS
3. Restart NSSM service Kha0sysBot3
4. Monitor first few trades via Telegram to verify order placement
