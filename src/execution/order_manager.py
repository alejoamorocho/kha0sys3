"""
Order Manager — Kha0sys3 v2
Ciclo de vida de ordenes para estrategias FADE, MOMENTUM y SHAKEOUT.

Reglas:
  1. UN trade por (simbolo, edge, session) por dia
  2. Expiracion hardware: ORDER_TIME_SPECIFIED a 8 horas
  3. Position sizing sobre BALANCE con riesgo dinamico por WR
  4. FADE_UP: SELL_LIMIT en OR_HIGH, TP=OR_LOW, SL=OR_HIGH+OR_WIDTH (R:R=1:1)
  5. FADE_DOWN: BUY_LIMIT en OR_LOW, TP=OR_HIGH, SL=OR_LOW-OR_WIDTH (R:R=1:1)
  6. MOMENTUM_UP: BUY_STOP en OR_HIGH, TP=OR_HIGH+1.5*OR_WIDTH, SL=OR_LOW
  7. MOMENTUM_DOWN: SELL_STOP en OR_LOW, TP=OR_LOW-1.5*OR_WIDTH, SL=OR_HIGH
  8. SHAKEOUT: monitoreo software multi-etapa
"""

import MetaTrader5 as mt5
from datetime import datetime, timedelta, timezone
from typing import Optional

from src.execution.mt5_client import MT5Client
from src.execution.risk_manager import DynamicRiskAllocator

ORDER_EXPIRATION_HOURS = 8
BOT_MAGIC_NUMBER = 1337
MOMENTUM_TP_MULT = 1.5


class OrderManager:

    def __init__(self, mt5_client: MT5Client, allocator: DynamicRiskAllocator,
                 telegram=None):
        self.client = mt5_client
        self.allocator = allocator
        self.telegram = telegram
        self._daily_trades: dict[str, str] = {}
        self._last_daily_reset: str = ""
        # Shakeout monitors: {key: {stage, or_high, or_low, or_width, order_ticket}}
        self._shakeout_monitors: dict[str, dict] = {}
        # Fade monitors: {key: {or_high, or_low, order_ticket, cancel_level}}
        self._fade_monitors: dict[str, dict] = {}
        self._load_state()

    STATE_FILE = "data/live_state/daily_trades.json"

    def _save_state(self):
        import json as _json
        import os
        os.makedirs(os.path.dirname(self.STATE_FILE), exist_ok=True)
        state = {"daily_trades": self._daily_trades, "last_reset": self._last_daily_reset}
        with open(self.STATE_FILE, "w") as f:
            _json.dump(state, f)

    def _load_state(self):
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
            self._shakeout_monitors.clear()
            self._fade_monitors.clear()
            self._last_daily_reset = today

    def has_traded_today(self, symbol: str, edge: str, session: str = "") -> bool:
        self._reset_daily_if_needed()
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        key = f"{symbol}_{edge}_{session}"
        return self._daily_trades.get(key) == today

    def mark_traded_today(self, symbol: str, edge: str = "", session: str = ""):
        self._reset_daily_if_needed()
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        key = f"{symbol}_{edge}_{session}"
        self._daily_trades[key] = today
        self._save_state()

    def cancel_order_by_ticket(self, ticket: int, symbol: str) -> bool:
        req = {"action": mt5.TRADE_ACTION_REMOVE, "order": ticket, "symbol": symbol}
        res = self.client.send_order_raw(req)
        return res.get("retcode") == mt5.TRADE_RETCODE_DONE

    def cancel_all_bot_orders(self, symbol: str) -> int:
        orders = self.client.get_pending_orders(symbol)
        if not orders:
            return 0
        count = 0
        for o in orders:
            if o.magic != BOT_MAGIC_NUMBER:
                continue
            req = {"action": mt5.TRADE_ACTION_REMOVE, "order": o.ticket, "symbol": symbol}
            res = self.client.send_order_raw(req)
            if res.get("retcode") == mt5.TRADE_RETCODE_DONE:
                count += 1
        return count

    def wipe_stale_orders(self) -> int:
        orders = mt5.orders_get()
        if not orders:
            return 0

        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(hours=ORDER_EXPIRATION_HOURS)
        total_wiped = 0

        for o in orders:
            if o.magic != BOT_MAGIC_NUMBER:
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
            # Get the ticket of the placed order
            orders = self.client.get_pending_orders(symbol)
            for o in orders:
                if o.magic == BOT_MAGIC_NUMBER and comment in (o.comment or ""):
                    return o.ticket
            return -1  # Placed but couldn't find ticket
        return None

    # ─── FADE Orders ──────────────────────────────────────────────

    def place_fade_up(self, symbol: str, or_high: float, or_low: float,
                      or_width: float, win_rate: float, session: str) -> bool:
        """FADE_UP: SELL_LIMIT en OR_HIGH. Apostamos a falso breakout alcista.
        TP = OR_LOW (1R). SL = OR_HIGH + OR_WIDTH (1R). R:R = 1:1.
        """
        if self.has_traded_today(symbol, "FADE_UP", session):
            return False

        if not self.client.check_spread_friction(symbol):
            return False

        sym_info = self.client.get_symbol_info(symbol)
        balance = self.client.get_account_balance()

        entry = or_high
        sl = or_high + or_width
        tp = or_low

        lots = self.allocator.calculate_lots(
            account_balance=balance, entry_price=entry, sl_price=sl,
            tick_value=sym_info.trade_tick_value, tick_size=sym_info.trade_tick_size,
            volume_step=sym_info.volume_step, win_rate=win_rate,
        )

        comment = f"FADE_UP_{session}"
        ticket = self._send_pending_order(symbol, mt5.ORDER_TYPE_SELL_LIMIT, entry, sl, tp, lots, comment)
        return ticket is not None

    def place_fade_down(self, symbol: str, or_high: float, or_low: float,
                        or_width: float, win_rate: float, session: str) -> bool:
        """FADE_DOWN: BUY_LIMIT en OR_LOW. Apostamos a falso breakout bajista.
        TP = OR_HIGH (1R). SL = OR_LOW - OR_WIDTH (1R). R:R = 1:1.
        """
        if self.has_traded_today(symbol, "FADE_DOWN", session):
            return False

        if not self.client.check_spread_friction(symbol):
            return False

        sym_info = self.client.get_symbol_info(symbol)
        balance = self.client.get_account_balance()

        entry = or_low
        sl = or_low - or_width
        tp = or_high

        lots = self.allocator.calculate_lots(
            account_balance=balance, entry_price=entry, sl_price=sl,
            tick_value=sym_info.trade_tick_value, tick_size=sym_info.trade_tick_size,
            volume_step=sym_info.volume_step, win_rate=win_rate,
        )

        comment = f"FADE_DW_{session}"
        ticket = self._send_pending_order(symbol, mt5.ORDER_TYPE_BUY_LIMIT, entry, sl, tp, lots, comment)
        return ticket is not None

    # ─── MOMENTUM Orders ──────────────────────────────────────────

    def place_momentum_up(self, symbol: str, or_high: float, or_low: float,
                          or_width: float, win_rate: float, session: str) -> bool:
        """MOMENTUM_UP: BUY_STOP en OR_HIGH. TP = 1.5R. SL = OR_LOW."""
        if self.has_traded_today(symbol, "MOMENTUM_UP", session):
            return False

        if not self.client.check_spread_friction(symbol):
            return False

        sym_info = self.client.get_symbol_info(symbol)
        balance = self.client.get_account_balance()

        entry = or_high
        sl = or_low
        tp = or_high + (or_width * MOMENTUM_TP_MULT)

        lots = self.allocator.calculate_lots(
            account_balance=balance, entry_price=entry, sl_price=sl,
            tick_value=sym_info.trade_tick_value, tick_size=sym_info.trade_tick_size,
            volume_step=sym_info.volume_step, win_rate=win_rate,
        )

        comment = f"MOM_UP_{session}"
        ticket = self._send_pending_order(symbol, mt5.ORDER_TYPE_BUY_STOP, entry, sl, tp, lots, comment)
        return ticket is not None

    def place_momentum_down(self, symbol: str, or_high: float, or_low: float,
                            or_width: float, win_rate: float, session: str) -> bool:
        """MOMENTUM_DOWN: SELL_STOP en OR_LOW. TP = 1.5R. SL = OR_HIGH."""
        if self.has_traded_today(symbol, "MOMENTUM_DOWN", session):
            return False

        if not self.client.check_spread_friction(symbol):
            return False

        sym_info = self.client.get_symbol_info(symbol)
        balance = self.client.get_account_balance()

        entry = or_low
        sl = or_high
        tp = or_low - (or_width * MOMENTUM_TP_MULT)

        lots = self.allocator.calculate_lots(
            account_balance=balance, entry_price=entry, sl_price=sl,
            tick_value=sym_info.trade_tick_value, tick_size=sym_info.trade_tick_size,
            volume_step=sym_info.volume_step, win_rate=win_rate,
        )

        comment = f"MOM_DW_{session}"
        ticket = self._send_pending_order(symbol, mt5.ORDER_TYPE_SELL_STOP, entry, sl, tp, lots, comment)
        return ticket is not None

    # ─── SHAKEOUT Orders (software-monitored) ────────────────────

    def setup_shakeout_monitor(self, symbol: str, direction: str,
                               or_high: float, or_low: float, or_width: float,
                               win_rate: float, session: str) -> bool:
        """Registra un monitor de shakeout. No coloca orden inmediatamente.
        Etapas: 1) Espera breakout, 2) Espera false breakout (SL hit), 3) Coloca re-entry.

        SHAKEOUT_UP: Espera UP break -> espera regreso a OR_LOW -> BUY_STOP en OR_HIGH
        SHAKEOUT_DOWN: Espera DOWN break -> espera regreso a OR_HIGH -> SELL_STOP en OR_LOW
        """
        key = f"{symbol}_{direction}_{session}"
        if self.has_traded_today(symbol, direction, session):
            return False

        self._shakeout_monitors[key] = {
            "stage": "WAIT_BREAKOUT",
            "direction": direction,
            "symbol": symbol,
            "or_high": or_high,
            "or_low": or_low,
            "or_width": or_width,
            "win_rate": win_rate,
            "session": session,
            "order_ticket": None,
        }
        print(f"[SHAKEOUT] Monitor registrado: {key} stage=WAIT_BREAKOUT")
        return True

    def check_shakeout_monitors(self):
        """Llamado cada 10s. Avanza los shakeout por sus etapas."""
        for key in list(self._shakeout_monitors.keys()):
            mon = self._shakeout_monitors[key]
            sym = mon["symbol"]
            tick = mt5.symbol_info_tick(sym)
            if tick is None:
                continue

            if mon["stage"] == "WAIT_BREAKOUT":
                if mon["direction"] == "SHAKEOUT_UP" and tick.ask >= mon["or_high"]:
                    mon["stage"] = "WAIT_FALSE_BREAK"
                    print(f"[SHAKEOUT] {key}: UP breakout detectado. Esperando false break...")
                elif mon["direction"] == "SHAKEOUT_DOWN" and tick.bid <= mon["or_low"]:
                    mon["stage"] = "WAIT_FALSE_BREAK"
                    print(f"[SHAKEOUT] {key}: DOWN breakout detectado. Esperando false break...")

            elif mon["stage"] == "WAIT_FALSE_BREAK":
                if mon["direction"] == "SHAKEOUT_UP" and tick.bid <= mon["or_low"]:
                    # False breakout confirmado, colocar re-entry BUY
                    self._place_shakeout_reentry(mon, "BUY")
                    del self._shakeout_monitors[key]
                elif mon["direction"] == "SHAKEOUT_DOWN" and tick.ask >= mon["or_high"]:
                    # False breakout confirmado, colocar re-entry SELL
                    self._place_shakeout_reentry(mon, "SELL")
                    del self._shakeout_monitors[key]

    def _place_shakeout_reentry(self, mon: dict, direction: str):
        """Coloca la orden de re-entry del shakeout."""
        sym = mon["symbol"]
        session = mon["session"]

        sym_info = self.client.get_symbol_info(sym)
        balance = self.client.get_account_balance()

        if direction == "BUY":
            entry = mon["or_high"]
            sl = mon["or_low"]
            tp = mon["or_high"] + mon["or_width"]
            order_type = mt5.ORDER_TYPE_BUY_STOP
            comment = f"SHKO_UP_{session}"
        else:
            entry = mon["or_low"]
            sl = mon["or_high"]
            tp = mon["or_low"] - mon["or_width"]
            order_type = mt5.ORDER_TYPE_SELL_STOP
            comment = f"SHKO_DW_{session}"

        lots = self.allocator.calculate_lots(
            account_balance=balance, entry_price=entry, sl_price=sl,
            tick_value=sym_info.trade_tick_value, tick_size=sym_info.trade_tick_size,
            volume_step=sym_info.volume_step, win_rate=mon["win_rate"],
        )

        ticket = self._send_pending_order(sym, order_type, entry, sl, tp, lots, comment)
        if ticket:
            print(f"[SHAKEOUT] Re-entry colocada: {sym} {comment}")
            self.mark_traded_today(sym, mon["direction"], session)
