"""
Order Manager — Kha0sys3 v3
Ciclo de vida de ordenes con paridad exacta al backtester.

Paridad backtest-live:
  FADE: Monitor 2 etapas — espera breakout, luego entra CONTRA el breakout
  MOMENTUM: BUY_STOP/SELL_STOP en OR boundary (primera rotura = entry)
  SHAKEOUT: Monitor 3 etapas — breakout, false break, re-entry

Reglas:
  1. UN trade por (simbolo, edge, session) por dia
  2. Expiracion hardware: 8 horas
  3. Position sizing sobre BALANCE con riesgo dinamico por WR
"""

import MetaTrader5 as mt5
from datetime import datetime, timedelta, timezone
from typing import Optional

from src.execution.mt5_client import MT5Client
from src.execution.risk_manager import DynamicRiskAllocator
from src.domain.constants import MAGIC_NUMBER, ORDER_EXPIRATION_HOURS, DEFAULT_TP_MULTIPLIER


class OrderManager:

    def __init__(self, mt5_client: MT5Client, allocator: DynamicRiskAllocator,
                 telegram=None):
        self.client = mt5_client
        self.allocator = allocator
        self.telegram = telegram
        self._daily_trades: dict[str, str] = {}
        self._last_daily_reset: str = ""
        # Monitors: software-monitored multi-stage strategies
        # {key: {stage, direction, symbol, or_high, or_low, or_width, win_rate, session}}
        self._monitors: dict[str, dict] = {}
        self._load_state()

    STATE_FILE = "data/live_state/daily_trades.json"

    def _save_state(self):
        """Persiste estado de trades diarios a disco."""
        import json as _json
        import os
        os.makedirs(os.path.dirname(self.STATE_FILE), exist_ok=True)
        state = {"daily_trades": self._daily_trades, "last_reset": self._last_daily_reset}
        with open(self.STATE_FILE, "w") as f:
            _json.dump(state, f)

    def _load_state(self):
        """Carga estado de trades diarios desde disco. Silencia FileNotFoundError."""
        import json as _json
        try:
            with open(self.STATE_FILE, "r") as f:
                state = _json.load(f)
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            if state.get("last_reset") == today:
                self._daily_trades = state.get("daily_trades", {})
                self._last_daily_reset = state["last_reset"]
        except (FileNotFoundError, _json.JSONDecodeError):
            # Missing state file is a valid initial state — intentional silencing
            pass

    def _reset_daily_if_needed(self):
        """Resetea contadores si el dia UTC cambio."""
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        if today != self._last_daily_reset:
            self._daily_trades.clear()
            self._monitors.clear()
            self._last_daily_reset = today

    def has_traded_today(self, symbol: str, edge: str, session: str = "") -> bool:
        """Verifica si ya se opero hoy para esta combinacion simbolo/edge/sesion."""
        self._reset_daily_if_needed()
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        key = f"{symbol}_{edge}_{session}"
        return self._daily_trades.get(key) == today

    def mark_traded_today(self, symbol: str, edge: str = "", session: str = ""):
        """Marca una combinacion como operada hoy."""
        self._reset_daily_if_needed()
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        key = f"{symbol}_{edge}_{session}"
        self._daily_trades[key] = today
        self._save_state()

    def cancel_order_by_ticket(self, ticket: int, symbol: str) -> bool:
        """Cancela una orden pendiente por ticket."""
        req = {"action": mt5.TRADE_ACTION_REMOVE, "order": ticket, "symbol": symbol}
        res = self.client.send_order_raw(req)
        return res.get("retcode") == mt5.TRADE_RETCODE_DONE

    def cancel_all_bot_orders(self, symbol: str) -> int:
        """Cancela todas las ordenes pendientes del bot para un simbolo."""
        orders = self.client.get_pending_orders(symbol)
        if not orders:
            return 0
        count = 0
        for o in orders:
            if o.magic != MAGIC_NUMBER:
                continue
            req = {"action": mt5.TRADE_ACTION_REMOVE, "order": o.ticket, "symbol": symbol}
            res = self.client.send_order_raw(req)
            if res.get("retcode") == mt5.TRADE_RETCODE_DONE:
                count += 1
        return count

    def wipe_stale_orders(self) -> int:
        """Elimina ordenes pendientes que superaron el tiempo de expiracion."""
        orders = mt5.orders_get()
        if not orders:
            return 0

        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(hours=ORDER_EXPIRATION_HOURS)
        total_wiped = 0

        for o in orders:
            if o.magic != MAGIC_NUMBER:
                continue
            order_time = datetime.fromtimestamp(o.time_setup, tz=timezone.utc)
            if order_time >= cutoff:
                continue
            req = {"action": mt5.TRADE_ACTION_REMOVE, "order": o.ticket, "symbol": o.symbol}
            res = self.client.send_order_raw(req)
            if res.get("retcode") == mt5.TRADE_RETCODE_DONE:
                total_wiped += 1

        if total_wiped > 0 and self.telegram:
            self.telegram.send_sync(
                f"🧹 <b>Limpieza:</b> {total_wiped} ordenes expiradas eliminadas"
            )
        return total_wiped

    def _get_filling_mode(self, symbol: str) -> int:
        _FILL_FOK = 1
        _FILL_IOC = 2
        sym_info = mt5.symbol_info(symbol)
        if sym_info is None:
            return mt5.ORDER_FILLING_FOK
        modes = sym_info.filling_mode
        if modes & _FILL_FOK:
            return mt5.ORDER_FILLING_FOK
        elif modes & _FILL_IOC:
            return mt5.ORDER_FILLING_IOC
        return mt5.ORDER_FILLING_RETURN

    def _send_pending_order(self, symbol: str, order_type, price: float,
                            sl: float, tp: float, volume: float,
                            comment: str) -> Optional[int]:
        """Envia orden pendiente. Retorna ticket si exitoso, None si fallo."""
        sym_info = self.client.get_symbol_info(symbol)

        if volume < sym_info.volume_min:
            reason = f"Lotaje insuficiente ({volume:.2f} < {sym_info.volume_min})"
            print(f"[OM] {symbol}: {reason}")
            if self.telegram:
                self.telegram.notify_order_rejected(symbol, reason)
            return None

        expiration_ts = int(
            (datetime.now(timezone.utc) + timedelta(hours=ORDER_EXPIRATION_HOURS)).timestamp()
        )

        type_names = {
            mt5.ORDER_TYPE_BUY_STOP: "BUY_STOP",
            mt5.ORDER_TYPE_SELL_STOP: "SELL_STOP",
            mt5.ORDER_TYPE_BUY_LIMIT: "BUY_LIMIT",
            mt5.ORDER_TYPE_SELL_LIMIT: "SELL_LIMIT",
        }

        req = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": float(volume),
            "type": order_type,
            "price": float(price),
            "sl": float(sl),
            "tp": float(tp),
            "deviation": 10,
            "magic": MAGIC_NUMBER,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_SPECIFIED,
            "expiration": expiration_ts,
            "type_filling": self._get_filling_mode(symbol),
        }
        res = self.client.send_order_raw(req)
        success = res.get("retcode") == mt5.TRADE_RETCODE_DONE

        if self.telegram:
            try:
                direction = type_names.get(order_type, str(order_type))
                if success:
                    self.telegram.notify_order_placed(symbol, direction, price, sl, tp, volume, comment)
                else:
                    self.telegram.notify_order_rejected(
                        symbol, f"{direction} retcode {res.get('retcode', '?')}"
                    )
            except Exception as e:
                print(f"[WARN] Telegram notification failed: {e}")

        if success:
            orders = self.client.get_pending_orders(symbol)
            for o in orders:
                if o.magic == MAGIC_NUMBER and comment in (o.comment or ""):
                    return o.ticket
            return -1
        return None

    # ─── FADE Orders (2-stage monitor, backtest parity) ───────────
    #
    # Backtest: first_break_dir = UP -> trade activates -> wins if SL (OR_LOW) hit before TP
    # Live parity:
    #   Stage 1 (WAIT_BREAKOUT): Monitor price until it breaks OR boundary
    #   Stage 2 (ORDER_PLACED): Place counter-direction STOP order at opposite OR boundary
    #
    # FADE_UP:  Wait for UP breakout (price >= OR_HIGH) -> place SELL_STOP at OR_LOW
    #           SL = OR_HIGH + OR_WIDTH, TP = OR_LOW - OR_WIDTH...
    #           No: TP is already at entry (OR_LOW). The "win" in backtest is price
    #           reaching OR_LOW. So the SELL_STOP at OR_LOW IS the entry.
    #           TP = OR_LOW - OR_WIDTH (profit = 1R beyond entry)? No...
    #
    # Actually rethinking: In backtest FADE, R:R is 1:1 where:
    #   - Entry = at breakout level (OR_HIGH for UP break)
    #   - TP = opposite OR boundary (OR_LOW) = 1x OR_WIDTH profit
    #   - SL = entry + 1x OR_WIDTH = OR_HIGH + OR_WIDTH = 1x OR_WIDTH loss
    #
    # Live parity: After breakout UP confirmed, sell at market near OR_HIGH
    #   - But we can't guarantee exact fill at OR_HIGH with a market order
    #   - Better: SELL_LIMIT at OR_HIGH (price already broke up, will likely
    #     retest OR_HIGH from above — common price action)
    #   - This is actually the same as before BUT gated by breakout confirmation
    #
    # Final design:
    #   Stage 1: Monitor until breakout confirmed (tick crosses OR boundary)
    #   Stage 2: Place SELL_LIMIT at OR_HIGH (for FADE_UP) or BUY_LIMIT at OR_LOW (for FADE_DOWN)
    #            with proper SL/TP. The limit order fills when price retests the level.

    def setup_fade_monitor(self, symbol: str, direction: str,
                           or_high: float, or_low: float, or_width: float,
                           win_rate: float, session: str, context: str = "BASE") -> bool:
        """Register a FADE monitor. Waits for breakout, then places counter-order."""
        edge = f"FADE_{direction.split('_')[-1]}" if "FADE" in direction else direction
        key = f"{symbol}_{direction}_{session}_{context}"

        if self.has_traded_today(symbol, edge, session):
            return False

        self._monitors[key] = {
            "type": "FADE",
            "stage": "WAIT_BREAKOUT",
            "direction": direction,
            "symbol": symbol,
            "or_high": or_high,
            "or_low": or_low,
            "or_width": or_width,
            "win_rate": win_rate,
            "session": session,
            "context": context,
        }
        print(f"[FADE] Monitor: {key} WAIT_BREAKOUT")
        return True

    # ─── MOMENTUM Orders (direct STOP orders, backtest parity) ────
    #
    # Backtest: first_break_dir determines entry. BUY_STOP at OR_HIGH, SELL_STOP at OR_LOW.
    # This is already exact parity — STOP order triggers on breakout.

    def place_momentum_up(self, symbol: str, or_high: float, or_low: float,
                          or_width: float, win_rate: float, session: str,
                          context: str = "BASE") -> bool:
        """MOMENTUM_UP: BUY_STOP en OR_HIGH. TP = 1.5R. SL = OR_LOW."""
        if self.has_traded_today(symbol, "MOMENTUM_UP", session):
            return False
        if not self.client.check_spread_friction(symbol):
            return False

        sym_info = self.client.get_symbol_info(symbol)
        balance = self.client.get_account_balance()

        entry = or_high
        sl = or_low
        tp = or_high + (or_width * DEFAULT_TP_MULTIPLIER)

        lots = self.allocator.calculate_lots(
            account_balance=balance, entry_price=entry, sl_price=sl,
            tick_value=sym_info.trade_tick_value, tick_size=sym_info.trade_tick_size,
            volume_step=sym_info.volume_step, win_rate=win_rate,
        )

        ctx_short = context[:8] if context != "BASE" else ""
        comment = f"MU|{session}|{ctx_short}".rstrip("|")
        ticket = self._send_pending_order(symbol, mt5.ORDER_TYPE_BUY_STOP, entry, sl, tp, lots, comment)
        return ticket is not None

    def place_momentum_down(self, symbol: str, or_high: float, or_low: float,
                            or_width: float, win_rate: float, session: str,
                            context: str = "BASE") -> bool:
        """MOMENTUM_DOWN: SELL_STOP en OR_LOW. TP = 1.5R. SL = OR_HIGH."""
        if self.has_traded_today(symbol, "MOMENTUM_DOWN", session):
            return False
        if not self.client.check_spread_friction(symbol):
            return False

        sym_info = self.client.get_symbol_info(symbol)
        balance = self.client.get_account_balance()

        entry = or_low
        sl = or_high
        tp = or_low - (or_width * DEFAULT_TP_MULTIPLIER)

        lots = self.allocator.calculate_lots(
            account_balance=balance, entry_price=entry, sl_price=sl,
            tick_value=sym_info.trade_tick_value, tick_size=sym_info.trade_tick_size,
            volume_step=sym_info.volume_step, win_rate=win_rate,
        )

        ctx_short = context[:8] if context != "BASE" else ""
        comment = f"MD|{session}|{ctx_short}".rstrip("|")
        ticket = self._send_pending_order(symbol, mt5.ORDER_TYPE_SELL_STOP, entry, sl, tp, lots, comment)
        return ticket is not None

    # ─── SHAKEOUT Orders (3-stage monitor, backtest parity) ───────
    #
    # Backtest: false breakout (breakout + SL hit) -> re-entry in original direction
    # Live: Stage 1 = wait breakout, Stage 2 = wait false break (SL level), Stage 3 = place re-entry STOP

    def setup_shakeout_monitor(self, symbol: str, direction: str,
                               or_high: float, or_low: float, or_width: float,
                               win_rate: float, session: str, context: str = "BASE") -> bool:
        """Register a SHAKEOUT monitor (3 stages)."""
        key = f"{symbol}_{direction}_{session}_{context}"
        if self.has_traded_today(symbol, direction, session):
            return False

        self._monitors[key] = {
            "type": "SHAKEOUT",
            "stage": "WAIT_BREAKOUT",
            "direction": direction,
            "symbol": symbol,
            "or_high": or_high,
            "or_low": or_low,
            "or_width": or_width,
            "win_rate": win_rate,
            "session": session,
            "context": context,
        }
        print(f"[SHAKEOUT] Monitor: {key} WAIT_BREAKOUT")
        return True

    # ─── Unified Monitor Check (called every 10s) ────────────────

    def check_monitors(self):
        """Process all active monitors (FADE + SHAKEOUT). Called from main loop."""
        for key in list(self._monitors.keys()):
            mon = self._monitors[key]
            sym = mon["symbol"]
            tick = mt5.symbol_info_tick(sym)
            if tick is None:
                continue

            if mon["type"] == "FADE":
                self._check_fade_monitor(key, mon, tick)
            elif mon["type"] == "SHAKEOUT":
                self._check_shakeout_monitor(key, mon, tick)

    def _check_fade_monitor(self, key: str, mon: dict, tick):
        """FADE 2-stage: WAIT_BREAKOUT -> place counter-order."""
        if mon["stage"] != "WAIT_BREAKOUT":
            return

        if mon["direction"] == "FADE_UP" and tick.ask >= mon["or_high"]:
            # UP breakout confirmed -> place SELL_LIMIT at OR_HIGH
            print(f"[FADE] {key}: UP breakout confirmed @ {tick.ask:.5f}. Placing SELL_LIMIT...")
            self._place_fade_order(mon, "SELL")
            del self._monitors[key]

        elif mon["direction"] == "FADE_DOWN" and tick.bid <= mon["or_low"]:
            # DOWN breakout confirmed -> place BUY_LIMIT at OR_LOW
            print(f"[FADE] {key}: DOWN breakout confirmed @ {tick.bid:.5f}. Placing BUY_LIMIT...")
            self._place_fade_order(mon, "BUY")
            del self._monitors[key]

    def _place_fade_order(self, mon: dict, side: str):
        """Place the counter-direction order after breakout confirmation."""
        sym = mon["symbol"]
        session = mon["session"]
        context = mon.get("context", "BASE")

        if not self.client.check_spread_friction(sym):
            return

        sym_info = self.client.get_symbol_info(sym)
        balance = self.client.get_account_balance()

        if side == "SELL":
            entry = mon["or_high"]
            sl = mon["or_high"] + mon["or_width"]
            tp = mon["or_low"]
            order_type = mt5.ORDER_TYPE_SELL_LIMIT
            # MT5 comment max ~31 chars, keep it concise but auditable
            ctx_short = context[:8] if context != "BASE" else ""
            comment = f"FU|{session}|{ctx_short}".rstrip("|")
            edge = "FADE_UP"
        else:
            entry = mon["or_low"]
            sl = mon["or_low"] - mon["or_width"]
            tp = mon["or_high"]
            order_type = mt5.ORDER_TYPE_BUY_LIMIT
            ctx_short = context[:8] if context != "BASE" else ""
            comment = f"FD|{session}|{ctx_short}".rstrip("|")
            edge = "FADE_DOWN"

        lots = self.allocator.calculate_lots(
            account_balance=balance, entry_price=entry, sl_price=sl,
            tick_value=sym_info.trade_tick_value, tick_size=sym_info.trade_tick_size,
            volume_step=sym_info.volume_step, win_rate=mon["win_rate"],
        )

        ticket = self._send_pending_order(sym, order_type, entry, sl, tp, lots, comment)
        if ticket:
            self.mark_traded_today(sym, edge, session)
            print(f"[FADE] Orden colocada: {sym} {comment}")

    def _check_shakeout_monitor(self, key: str, mon: dict, tick):
        """SHAKEOUT 3-stage: WAIT_BREAKOUT -> WAIT_FALSE_BREAK -> place re-entry."""
        if mon["stage"] == "WAIT_BREAKOUT":
            if mon["direction"] == "SHAKEOUT_UP" and tick.ask >= mon["or_high"]:
                mon["stage"] = "WAIT_FALSE_BREAK"
                print(f"[SHAKEOUT] {key}: UP breakout. Esperando false break...")
            elif mon["direction"] == "SHAKEOUT_DOWN" and tick.bid <= mon["or_low"]:
                mon["stage"] = "WAIT_FALSE_BREAK"
                print(f"[SHAKEOUT] {key}: DOWN breakout. Esperando false break...")

        elif mon["stage"] == "WAIT_FALSE_BREAK":
            if mon["direction"] == "SHAKEOUT_UP" and tick.bid <= mon["or_low"]:
                self._place_shakeout_reentry(mon, "BUY")
                del self._monitors[key]
            elif mon["direction"] == "SHAKEOUT_DOWN" and tick.ask >= mon["or_high"]:
                self._place_shakeout_reentry(mon, "SELL")
                del self._monitors[key]

    def _place_shakeout_reentry(self, mon: dict, side: str):
        """Place re-entry STOP order after false breakout confirmed."""
        sym = mon["symbol"]
        session = mon["session"]
        context = mon.get("context", "BASE")

        sym_info = self.client.get_symbol_info(sym)
        balance = self.client.get_account_balance()

        ctx_short = context[:8] if context != "BASE" else ""
        if side == "BUY":
            entry = mon["or_high"]
            sl = mon["or_low"]
            tp = mon["or_high"] + mon["or_width"]
            order_type = mt5.ORDER_TYPE_BUY_STOP
            comment = f"SU|{session}|{ctx_short}".rstrip("|")
        else:
            entry = mon["or_low"]
            sl = mon["or_high"]
            tp = mon["or_low"] - mon["or_width"]
            order_type = mt5.ORDER_TYPE_SELL_STOP
            comment = f"SD|{session}|{ctx_short}".rstrip("|")

        lots = self.allocator.calculate_lots(
            account_balance=balance, entry_price=entry, sl_price=sl,
            tick_value=sym_info.trade_tick_value, tick_size=sym_info.trade_tick_size,
            volume_step=sym_info.volume_step, win_rate=mon["win_rate"],
        )

        ticket = self._send_pending_order(sym, order_type, entry, sl, tp, lots, comment)
        if ticket:
            self.mark_traded_today(sym, mon["direction"], session)
            print(f"[SHAKEOUT] Re-entry colocada: {sym} {comment}")
