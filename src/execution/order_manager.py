"""
Order Manager — Kha0sys3
Ciclo de vida de órdenes con arquitectura defensiva.

Reglas fundamentales (consistentes con backtest):
  1. UN trade por activo por día — si first_break_dir ya ocurrió, no se re-entra
  2. Expiración hardware: ORDER_TIME_SPECIFIED a 8 horas
  3. Cancelación de pierna opuesta al detectar fill
  4. Position sizing sobre BALANCE (no free_margin)
"""

import MetaTrader5 as mt5
from datetime import datetime, timedelta, timezone
from typing import Optional

from src.execution.mt5_client import MT5Client
from src.execution.risk_manager import DynamicRiskAllocator

ORDER_EXPIRATION_HOURS = 8
BOT_MAGIC_NUMBER = 1337


class OrderManager:
    """Maneja el ciclo de vida de las órdenes asegurando arquitectura defensiva."""

    def __init__(self, mt5_client: MT5Client, allocator: DynamicRiskAllocator,
                 telegram=None):
        self.client = mt5_client
        self.allocator = allocator
        self.telegram = telegram
        # Tracking: un trade por activo por día
        self._daily_trades: dict[str, str] = {}  # symbol -> date string
        self._last_daily_reset: str = ""

    def _reset_daily_if_needed(self):
        """Reset del tracker diario a medianoche UTC."""
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        if today != self._last_daily_reset:
            self._daily_trades.clear()
            self._last_daily_reset = today

    def has_traded_today(self, symbol: str) -> bool:
        """Verifica si ya hubo un trade (first_break) para este activo hoy."""
        self._reset_daily_if_needed()
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        return self._daily_trades.get(symbol) == today

    def mark_traded_today(self, symbol: str):
        """Marca que este activo ya tuvo su trade del día."""
        self._reset_daily_if_needed()
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        self._daily_trades[symbol] = today

    def cancel_all_orders(self, symbol: str) -> int:
        """Cancela TODAS las órdenes pendientes de un símbolo (pierna opuesta)."""
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

    def cancel_opposite_leg(self, symbol: str):
        """Cancela la pierna opuesta al detectar que una orden se ejecutó.

        Llamado desde el loop principal cuando se detecta una nueva posición.
        """
        cancelled = self.cancel_all_orders(symbol)
        if cancelled > 0:
            self.mark_traded_today(symbol)

    def wipe_stale_orders(self) -> int:
        """Limpia órdenes del bot que superaron ORDER_EXPIRATION_HOURS.

        Capa software complementaria a la expiración hardware.
        """
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

    def is_already_exposed(self, symbol: str) -> bool:
        """Verifica si ya hay posiciones o órdenes pendientes."""
        positions = self.client.get_open_positions(symbol)
        orders = self.client.get_pending_orders(symbol)
        return len(positions) > 0 or len(orders) > 0

    def place_breakout_stop_orders(
        self,
        symbol: str,
        range_high: float,
        range_low: float,
        sl_up: float,
        sl_dw: float,
        tp_up: float,
        tp_dw: float,
    ) -> bool:
        """Envía BUY_STOP y SELL_STOP con TP/SL fijos.

        Reglas:
        - Un trade por activo por día (consistente con backtest)
        - Expiración hardware a ORDER_EXPIRATION_HOURS
        - Position sizing sobre BALANCE
        """

        # 1. Un trade por día por activo
        if self.has_traded_today(symbol):
            print(f"OrderManager: {symbol} ya operó hoy. Skip.")
            return False

        # 2. Exposición existente
        if self.is_already_exposed(symbol):
            print(f"OrderManager: Exposición existente en {symbol}. Standby.")
            if self.telegram:
                self.telegram.notify_exposure_blocked(symbol)
            return False

        # 3. Spread filter
        if not self.client.check_spread_friction(symbol):
            if self.telegram:
                current = self.client.get_current_spread(symbol)
                avg = self.client.get_average_spread(symbol)
                self.telegram.notify_spread_alert(symbol, current, avg)
            return False

        # 4. Datos del símbolo y BALANCE
        sym_info = self.client.get_symbol_info(symbol)
        balance = self.client.get_account_balance()

        lots_up = self.allocator.calculate_lots(
            account_balance=balance,
            entry_price=range_high,
            sl_price=sl_up,
            tick_value=sym_info.trade_tick_value,
            tick_size=sym_info.trade_tick_size,
            volume_step=sym_info.volume_step,
        )

        lots_dw = self.allocator.calculate_lots(
            account_balance=balance,
            entry_price=range_low,
            sl_price=sl_dw,
            tick_value=sym_info.trade_tick_value,
            tick_size=sym_info.trade_tick_size,
            volume_step=sym_info.volume_step,
        )

        # Expiración hardware (timezone-aware UTC)
        expiration_ts = int(
            (datetime.now(timezone.utc) + timedelta(hours=ORDER_EXPIRATION_HOURS)).timestamp()
        )

        def send_stop(tipo, price, sl, tp, volume, comment):
            direction = "BUY_STOP" if tipo == mt5.ORDER_TYPE_BUY_STOP else "SELL_STOP"

            if volume < sym_info.volume_min:
                reason = f"Lotaje insuficiente ({volume:.2f} < {sym_info.volume_min})"
                print(f"OrderManager: {reason} en {symbol}.")
                if self.telegram:
                    self.telegram.notify_order_rejected(symbol, reason)
                return False

            req = {
                "action": mt5.TRADE_ACTION_PENDING,
                "symbol": symbol,
                "volume": float(volume),
                "type": tipo,
                "price": float(price),
                "sl": float(sl),
                "tp": float(tp),
                "deviation": 10,
                "magic": BOT_MAGIC_NUMBER,
                "comment": comment,
                "type_time": mt5.ORDER_TIME_SPECIFIED,
                "expiration": expiration_ts,
                "type_filling": mt5.ORDER_FILLING_FOK,
            }
            res = self.client.send_order_raw(req)
            success = res.get("retcode") == mt5.TRADE_RETCODE_DONE

            if success and self.telegram:
                self.telegram.notify_order_placed(symbol, direction, price, sl, tp, volume)
            elif not success and self.telegram:
                self.telegram.notify_order_rejected(
                    symbol, f"Retcode {res.get('retcode', 'unknown')}"
                )

            return success

        up_ok = send_stop(
            mt5.ORDER_TYPE_BUY_STOP, range_high, sl_up, tp_up, lots_up, "ORB_Quant_UP"
        )
        dw_ok = send_stop(
            mt5.ORDER_TYPE_SELL_STOP, range_low, sl_dw, tp_dw, lots_dw, "ORB_Quant_DW"
        )

        return up_ok or dw_ok
