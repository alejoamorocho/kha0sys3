"""
Order Manager — Kha0sys3
Ciclo de vida de ordenes con arquitectura defensiva.

Reglas fundamentales (paridad con backtest):
  1. UN trade por activo por edge por dia
  2. Expiracion hardware: ORDER_TIME_SPECIFIED a 8 horas
  3. Cancelacion de pierna opuesta al detectar fill
  4. Position sizing sobre BALANCE (no free_margin)
  5. TREND_UP: solo BUY_STOP, monitoreo software para cancel si DOWN rompe primero
  6. MAGNET_CLOSE: direccion dada por pd_close vs OR
"""

import MetaTrader5 as mt5
from datetime import datetime, timedelta, timezone
from typing import Optional

from src.execution.mt5_client import MT5Client
from src.execution.risk_manager import DynamicRiskAllocator

ORDER_EXPIRATION_HOURS = 8
BOT_MAGIC_NUMBER = 1337


class OrderManager:
    """Maneja el ciclo de vida de las ordenes asegurando arquitectura defensiva."""

    def __init__(self, mt5_client: MT5Client, allocator: DynamicRiskAllocator,
                 telegram=None):
        self.client = mt5_client
        self.allocator = allocator
        self.telegram = telegram
        # Tracking: un trade por activo por edge por dia
        self._daily_trades: dict[str, str] = {}  # "symbol_edge" -> date string
        self._last_daily_reset: str = ""
        # Monitoreo TREND_UP: cancel BUY si precio toca or_low
        # {symbol: {"or_low": float, "order_ticket": int, "edge": str}}
        self._trend_monitors: dict[str, dict] = {}
        self._load_state()

    STATE_FILE = "data/live_state/daily_trades.json"

    def _save_state(self):
        """Persist dedup state to disk."""
        import json as _json
        import os
        os.makedirs(os.path.dirname(self.STATE_FILE), exist_ok=True)
        state = {
            "daily_trades": self._daily_trades,
            "last_reset": self._last_daily_reset,
        }
        with open(self.STATE_FILE, "w") as f:
            _json.dump(state, f)

    def _load_state(self):
        """Restore dedup state from disk on startup."""
        import json as _json
        try:
            with open(self.STATE_FILE, "r") as f:
                state = _json.load(f)
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            if state.get("last_reset") == today:
                self._daily_trades = state.get("daily_trades", {})
                self._last_daily_reset = state["last_reset"]
        except (FileNotFoundError, _json.JSONDecodeError):
            pass

    def _reset_daily_if_needed(self):
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        if today != self._last_daily_reset:
            self._daily_trades.clear()
            self._trend_monitors.clear()
            self._last_daily_reset = today

    def has_traded_today(self, symbol: str, edge: str) -> bool:
        """Verifica si ya hubo un trade para este activo+edge hoy."""
        self._reset_daily_if_needed()
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        key = f"{symbol}_{edge}"
        return self._daily_trades.get(key) == today

    def mark_traded_today(self, symbol: str, edge: str = ""):
        """Marca que este activo+edge ya tuvo su trade del dia."""
        self._reset_daily_if_needed()
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        key = f"{symbol}_{edge}" if edge else symbol
        self._daily_trades[key] = today
        self._save_state()

    def cancel_all_orders(self, symbol: str) -> int:
        """Cancela TODAS las ordenes pendientes de un simbolo."""
        orders = self.client.get_pending_orders(symbol)
        if not orders:
            return 0

        count = 0
        for o in orders:
            if o.magic != BOT_MAGIC_NUMBER:
                continue
            req = {
                "action": mt5.TRADE_ACTION_REMOVE,
                "order": o.ticket,
                "symbol": symbol,
            }
            res = self.client.send_order_raw(req)
            if res.get("retcode") == mt5.TRADE_RETCODE_DONE:
                count += 1

        if count > 0 and self.telegram:
            self.telegram.notify_orphan_cleanup(symbol, count)

        return count

    def cancel_order_by_ticket(self, ticket: int, symbol: str) -> bool:
        """Cancela una orden especifica por ticket."""
        req = {
            "action": mt5.TRADE_ACTION_REMOVE,
            "order": ticket,
            "symbol": symbol,
        }
        res = self.client.send_order_raw(req)
        return res.get("retcode") == mt5.TRADE_RETCODE_DONE

    def cancel_opposite_leg(self, symbol: str):
        """Cancela la pierna opuesta al detectar que una orden se ejecuto."""
        cancelled = self.cancel_all_orders(symbol)
        # Remove from trend monitors if applicable
        self._trend_monitors.pop(symbol, None)

    def wipe_stale_orders(self) -> int:
        """Limpia ordenes del bot que superaron ORDER_EXPIRATION_HOURS."""
        orders = mt5.orders_get()
        if not orders:
            return 0

        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(hours=ORDER_EXPIRATION_HOURS)
        total_wiped = 0
        wiped_symbols = []

        for o in orders:
            if o.magic != BOT_MAGIC_NUMBER:
                continue

            order_time = datetime.fromtimestamp(o.time_setup, tz=timezone.utc)
            if order_time >= cutoff:
                continue

            req = {
                "action": mt5.TRADE_ACTION_REMOVE,
                "order": o.ticket,
                "symbol": o.symbol,
            }
            res = self.client.send_order_raw(req)
            if res.get("retcode") == mt5.TRADE_RETCODE_DONE:
                total_wiped += 1
                if o.symbol not in wiped_symbols:
                    wiped_symbols.append(o.symbol)

        # Clean up trend monitors for wiped orders
        for sym in wiped_symbols:
            self._trend_monitors.pop(sym, None)

        if total_wiped > 0 and self.telegram:
            symbols_str = ", ".join(wiped_symbols)
            self.telegram.send_sync(
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "   🧹 <b>LIMPIEZA ORDENES RANCIAS</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                f"  Eliminadas │ {total_wiped}\n"
                f"  Simbolos   │ {symbols_str}\n"
                f"  Expiracion │ >{ORDER_EXPIRATION_HOURS}h sin ejecutar\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                f"  <i>{now.strftime('%H:%M')} UTC</i>"
            )

        return total_wiped

    def is_already_exposed(self, symbol: str, edge: str) -> bool:
        """Verifica si ya hay posiciones o ordenes pendientes para este edge."""
        positions = self.client.get_open_positions(symbol)
        orders = self.client.get_pending_orders(symbol)
        # For TREND_UP and MAGNET on same symbol, filter by comment
        bot_positions = [p for p in positions if p.magic == BOT_MAGIC_NUMBER]
        bot_orders = [o for o in orders if o.magic == BOT_MAGIC_NUMBER]

        if edge == "MAGNET_CLOSE":
            # MAGNET can coexist with TREND_UP orders
            magnet_pos = [p for p in bot_positions if "MAGNET" in (p.comment or "")]
            magnet_ord = [o for o in bot_orders if "MAGNET" in (o.comment or "")]
            return len(magnet_pos) > 0 or len(magnet_ord) > 0
        elif edge == "TREND_UP":
            trend_pos = [p for p in bot_positions if "TREND" in (p.comment or "")]
            trend_ord = [o for o in bot_orders if "TREND" in (o.comment or "")]
            return len(trend_pos) > 0 or len(trend_ord) > 0

        return len(bot_positions) > 0 or len(bot_orders) > 0

    def _get_filling_mode(self, symbol: str) -> int:
        """Use broker-supported filling mode instead of hardcoded FOK."""
        # Bitmask constants (not all MT5 Python versions export SYMBOL_FILLING_*)
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
        else:
            return mt5.ORDER_FILLING_RETURN

    def _send_stop_order(self, symbol: str, order_type, price: float,
                         sl: float, tp: float, volume: float,
                         comment: str) -> bool:
        """Envia una orden stop con validacion de lotaje y notificacion."""
        sym_info = self.client.get_symbol_info(symbol)
        direction = "BUY_STOP" if order_type == mt5.ORDER_TYPE_BUY_STOP else "SELL_STOP"

        if volume < sym_info.volume_min:
            reason = f"Lotaje insuficiente ({volume:.2f} < {sym_info.volume_min})"
            print(f"OrderManager: {reason} en {symbol}.")
            if self.telegram:
                self.telegram.notify_order_rejected(symbol, reason)
            return False

        expiration_ts = int(
            (datetime.now(timezone.utc) + timedelta(hours=ORDER_EXPIRATION_HOURS)).timestamp()
        )

        req = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": float(volume),
            "type": order_type,
            "price": float(price),
            "sl": float(sl),
            "tp": float(tp),
            "deviation": 10,
            "magic": BOT_MAGIC_NUMBER,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_SPECIFIED,
            "expiration": expiration_ts,
            "type_filling": self._get_filling_mode(symbol),
        }
        res = self.client.send_order_raw(req)
        success = res.get("retcode") == mt5.TRADE_RETCODE_DONE

        if self.telegram:
            try:
                if success:
                    self.telegram.notify_order_placed(symbol, direction, price, sl, tp, volume, comment)
                else:
                    self.telegram.notify_order_rejected(
                        symbol, f"Retcode {res.get('retcode', 'unknown')}"
                    )
            except Exception as e:
                print(f"[WARN] Telegram notification failed: {e}")

        return success

    # ─── TREND_UP Orders ──────────────────────────────────────────

    def place_trend_up_orders(self, symbol: str, or_high: float,
                               or_low: float, tp_up: float) -> bool:
        """Coloca SOLO BUY_STOP para TREND_UP.

        El monitoreo software (check_trend_monitors) se encarga de
        cancelar el BUY_STOP si el precio toca or_low primero.
        Paridad con backtest: first_break_dir == "UP" gate.
        """
        if self.has_traded_today(symbol, "TREND_UP"):
            return False

        if self.is_already_exposed(symbol, "TREND_UP"):
            if self.telegram:
                self.telegram.notify_exposure_blocked(symbol)
            return False

        if not self.client.check_spread_friction(symbol):
            if self.telegram:
                current = self.client.get_current_spread(symbol)
                avg = self.client.get_average_spread(symbol)
                self.telegram.notify_spread_alert(symbol, current, avg)
            return False

        sym_info = self.client.get_symbol_info(symbol)
        balance = self.client.get_account_balance()

        lots = self.allocator.calculate_lots(
            account_balance=balance,
            entry_price=or_high,
            sl_price=or_low,
            tick_value=sym_info.trade_tick_value,
            tick_size=sym_info.trade_tick_size,
            volume_step=sym_info.volume_step,
        )

        success = self._send_stop_order(
            symbol, mt5.ORDER_TYPE_BUY_STOP,
            or_high, or_low, tp_up, lots, "TREND_UP"
        )

        if success:
            # Registrar monitoreo: si precio toca or_low, cancelar BUY
            orders = self.client.get_pending_orders(symbol)
            buy_ticket = None
            for o in orders:
                if o.magic == BOT_MAGIC_NUMBER and o.type == mt5.ORDER_TYPE_BUY_STOP:
                    if "TREND" in (o.comment or ""):
                        buy_ticket = o.ticket
                        break

            self._trend_monitors[symbol] = {
                "or_low": or_low,
                "order_ticket": buy_ticket,
                "edge": "TREND_UP",
            }

        return success

    # ─── MAGNET_CLOSE Orders ──────────────────────────────────────

    def place_magnet_order(self, symbol: str, or_high: float, or_low: float,
                           pd_close: float) -> bool:
        """Coloca orden direccional hacia pd_close.

        Si pd_close > or_high: BUY_STOP @ or_high, TP @ pd_close
        Si pd_close < or_low:  SELL_STOP @ or_low, TP @ pd_close
        Paridad con backtest: direccion dada por posicion de pd_close vs OR.
        """
        if self.has_traded_today(symbol, "MAGNET_CLOSE"):
            return False

        if self.is_already_exposed(symbol, "MAGNET_CLOSE"):
            if self.telegram:
                self.telegram.notify_exposure_blocked(symbol)
            return False

        if not self.client.check_spread_friction(symbol):
            if self.telegram:
                current = self.client.get_current_spread(symbol)
                avg = self.client.get_average_spread(symbol)
                self.telegram.notify_spread_alert(symbol, current, avg)
            return False

        # Skip if pd_close is inside OR (backtest parity)
        if or_low <= pd_close <= or_high:
            print(f"OrderManager: MAGNET {symbol}: pd_close inside OR. Skip.")
            if self.telegram:
                self.telegram.notify_order_rejected(
                    symbol, "MAGNET: pd_close dentro del OR"
                )
            return False

        sym_info = self.client.get_symbol_info(symbol)
        balance = self.client.get_account_balance()

        if pd_close > or_high:
            # BUY direction
            entry = or_high
            sl = or_low
            tp = pd_close
            order_type = mt5.ORDER_TYPE_BUY_STOP
            comment = "MAGNET_UP"
        else:
            # SELL direction
            entry = or_low
            sl = or_high
            tp = pd_close
            order_type = mt5.ORDER_TYPE_SELL_STOP
            comment = "MAGNET_DW"

        lots = self.allocator.calculate_lots(
            account_balance=balance,
            entry_price=entry,
            sl_price=sl,
            tick_value=sym_info.trade_tick_value,
            tick_size=sym_info.trade_tick_size,
            volume_step=sym_info.volume_step,
        )

        return self._send_stop_order(symbol, order_type, entry, sl, tp, lots, comment)

    # ─── Software Monitoring (replaces sentinel) ──────────────────

    def check_trend_monitors(self) -> list[str]:
        """Monitorea precios para cancelar BUY_STOP si DOWN rompe primero.

        Llamado cada 10s desde el loop principal.
        Paridad con backtest: first_break_dir == "DOWN" cancela TREND_UP.
        Retorna lista de simbolos donde se cancelo.
        """
        cancelled = []

        for sym in list(self._trend_monitors.keys()):
            monitor = self._trend_monitors[sym]
            or_low = monitor["or_low"]

            # Obtener precio actual
            tick = mt5.symbol_info_tick(sym)
            if tick is None:
                continue

            # Si precio toco or_low → DOWN rompio primero → cancelar BUY
            if tick.bid <= or_low:
                ticket = monitor.get("order_ticket")
                if ticket:
                    ok = self.cancel_order_by_ticket(ticket, sym)
                    if ok:
                        self.mark_traded_today(sym, "TREND_UP")
                        cancelled.append(sym)
                        if self.telegram:
                            self.telegram.send_sync(
                                f"<b>🔽 DOWN rompio primero: {sym}</b>\n"
                                f"<code>BUY_STOP cancelado (TREND_UP skip)</code>\n"
                                f"<code>Paridad backtest: first_break = DOWN</code>"
                            )
                else:
                    # No ticket, try cancelling all TREND orders
                    self.cancel_all_orders(sym)
                    self.mark_traded_today(sym, "TREND_UP")
                    cancelled.append(sym)

                del self._trend_monitors[sym]

        return cancelled

    # ─── Legacy compatibility ─────────────────────────────────────

    def place_breakout_stop_orders(self, symbol: str, range_high: float,
                                    range_low: float, sl_up: float,
                                    sl_dw: float, tp_up: float,
                                    tp_dw: float) -> bool:
        """Legacy method — kept for backward compatibility.
        Use place_trend_up_orders() or place_magnet_order() instead.
        """
        return self.place_trend_up_orders(symbol, range_high, range_low, tp_up)
