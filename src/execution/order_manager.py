"""
Order Manager — Kha0sys3 v4
Ciclo de vida de ordenes con paridad exacta al backtester.

Paridad backtest-live:
  FADE: SELL_LIMIT/BUY_LIMIT en OR boundary al cierre del OR (entry inmediata)
        TP y SL configurables por estrategia (tp_mult, sl_mult en bot_config)
        Guard de direccion: cancela si la direccion opuesta rompe primero
        (= filtro first_break_dir del backtest)
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

    def _validate_limit_price(self, symbol: str, order_type,
                              limit_price: float) -> tuple[bool, str]:
        """Valida que un precio LIMIT cumpla las reglas del broker.

        Regla MT5:
          SELL_LIMIT: limit_price >= ask + stops_level * point
          BUY_LIMIT:  limit_price <= bid - stops_level * point

        Si no se cumple, el broker rechaza con TRADE_RETCODE_INVALID_PRICE (10015).
        Esto pasa cuando el precio ya cruzo el OR boundary antes de poder enviar
        la orden (carrera entre OR close y exec time, o broker con stops_level alto
        como oil/indices).

        Returns (ok, reason). reason="" si ok=True.
        """
        tick = mt5.symbol_info_tick(symbol)
        info = mt5.symbol_info(symbol)
        if tick is None or info is None:
            return False, "sin tick/symbol_info disponible"

        min_dist = info.trade_stops_level * info.point
        d = info.digits

        if order_type == mt5.ORDER_TYPE_SELL_LIMIT:
            required = tick.ask + min_dist
            if limit_price < required:
                return False, (
                    f"ask={tick.ask:.{d}f} ya cruzo OR_HIGH={limit_price:.{d}f} "
                    f"(min_dist={min_dist:.{d}f})"
                )
        elif order_type == mt5.ORDER_TYPE_BUY_LIMIT:
            required = tick.bid - min_dist
            if limit_price > required:
                return False, (
                    f"bid={tick.bid:.{d}f} ya cruzo OR_LOW={limit_price:.{d}f} "
                    f"(min_dist={min_dist:.{d}f})"
                )
        return True, ""

    def _send_pending_order(self, symbol: str, order_type, price: float,
                            sl: float, tp: float, volume: float,
                            comment: str, win_rate: float = 0.0,
                            risk_pct: float = 0.0) -> Optional[int]:
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

        # Normalizar precios al trade_tick_size del simbolo para evitar 10015
        # por desalineacion aritmetica (ej: or_high + or_width * 2.5 con JPY).
        norm_price = self.client.normalize_price(symbol, price)
        norm_sl = self.client.normalize_price(symbol, sl)
        norm_tp = self.client.normalize_price(symbol, tp)

        req = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": float(volume),
            "type": order_type,
            "price": norm_price,
            "sl": norm_sl,
            "tp": norm_tp,
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
                    self.telegram.notify_order_placed(
                        symbol, direction, price, sl, tp, volume, comment,
                        win_rate=win_rate, risk_pct=risk_pct)
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

    # ─── FADE Orders (immediate LIMIT + direction guard, backtest parity) ──
    #
    # Backtest parity:
    #   1. Entry: SELL_LIMIT at OR_HIGH / BUY_LIMIT at OR_LOW, placed at OR close
    #      (fills the instant price touches the boundary = same as backtest entry)
    #   2. SL: OR_HIGH + OR_WIDTH (FADE_UP) / OR_LOW - OR_WIDTH (FADE_DOWN)
    #      R:R 1:1 — 1R risk, 1R reward
    #   3. TP: OR_LOW (FADE_UP) / OR_HIGH (FADE_DOWN)
    #   4. Direction guard: if opposite boundary breaks BEFORE our limit fills,
    #      cancel the order (matches first_break_dir filter in backtest)
    #
    # Note: backtest loss boundary is at 1.5*OR_WIDTH (MOMENTUM TP reused as FADE
    # loss condition). Live SL at 1*OR_WIDTH is more conservative but gives clean
    # 1:1 R:R matching the backtest's +1R/-1R accounting.

    def place_fade_up(self, symbol: str, or_high: float, or_low: float,
                      or_width: float, win_rate: float, session: str,
                      context: str = "BASE",
                      tp_mult: float = 1.0, sl_mult: float = 1.5) -> bool:
        """FADE_UP: SELL_LIMIT at OR_HIGH. TP/SL configurable por estrategia."""
        if self.has_traded_today(symbol, "FADE_UP", session):
            return False
        if not self.client.check_spread_friction(symbol):
            if self.telegram:
                cur = self.client.get_current_spread(symbol)
                avg = self.client.get_average_spread(symbol)
                self.telegram.notify_order_rejected(
                    symbol, f"Spread anomalo: {cur:.0f} pts (avg {avg:.0f}, max 1.5x)")
            return False
        tp_distance = or_width * tp_mult
        if not self.client.check_spread_vs_tp(symbol, tp_distance):
            if self.telegram:
                spread = self.client.get_spread_in_price(symbol)
                pct = spread / tp_distance * 100 if tp_distance > 0 else 0
                self.telegram.notify_order_rejected(
                    symbol, f"Spread {spread:.5f} = {pct:.0f}% del TP (max 30%)")
            return False

        sym_info = self.client.get_symbol_info(symbol)
        balance = self.client.get_account_balance()

        entry = or_high
        sl = or_high + (or_width * sl_mult)
        tp = or_high - (or_width * tp_mult)

        # Valida que el SELL_LIMIT se pueda colocar: el precio no debe haber
        # cruzado OR_HIGH todavia. Previene retcode 10015 por carrera entre
        # OR close y exec time (especialmente en oil/indices con stops_level 50).
        ok, reason = self._validate_limit_price(symbol, mt5.ORDER_TYPE_SELL_LIMIT, entry)
        if not ok:
            print(f"[FADE_UP] {symbol}: {reason}")
            if self.telegram:
                self.telegram.notify_order_rejected(symbol, f"FADE_UP: {reason}")
            return False

        lots = self.allocator.calculate_lots(
            account_balance=balance, entry_price=entry, sl_price=sl,
            tick_value=sym_info.trade_tick_value, tick_size=sym_info.trade_tick_size,
            volume_step=sym_info.volume_step, win_rate=win_rate,
        )

        risk_pct = self.allocator.get_risk_percent(win_rate)
        ctx_short = context[:8] if context != "BASE" else ""
        comment = f"FU|{session}|{ctx_short}".rstrip("|")
        ticket = self._send_pending_order(
            symbol, mt5.ORDER_TYPE_SELL_LIMIT, entry, sl, tp, lots, comment,
            win_rate=win_rate, risk_pct=risk_pct)

        if ticket:
            self.mark_traded_today(symbol, "FADE_UP", session)
            # Direction guard: cancel if OR_LOW breaks first (first_break_dir != UP)
            key = f"{symbol}_FADE_UP_{session}_{context}"
            self._monitors[key] = {
                "type": "FADE_GUARD",
                "direction": "FADE_UP",
                "symbol": symbol,
                "ticket": ticket,
                "cancel_level": or_low,  # cancel if bid <= or_low
                "or_high": or_high,
                "session": session,
            }
            print(f"[FADE] SELL_LIMIT colocada: {symbol} @ {entry:.5f} | SL={sl:.5f} TP={tp:.5f}")
            return True
        return False

    def place_fade_down(self, symbol: str, or_high: float, or_low: float,
                        or_width: float, win_rate: float, session: str,
                        context: str = "BASE",
                        tp_mult: float = 1.0, sl_mult: float = 1.5) -> bool:
        """FADE_DOWN: BUY_LIMIT at OR_LOW. TP/SL configurable por estrategia."""
        if self.has_traded_today(symbol, "FADE_DOWN", session):
            return False
        if not self.client.check_spread_friction(symbol):
            if self.telegram:
                cur = self.client.get_current_spread(symbol)
                avg = self.client.get_average_spread(symbol)
                self.telegram.notify_order_rejected(
                    symbol, f"Spread anomalo: {cur:.0f} pts (avg {avg:.0f}, max 1.5x)")
            return False
        tp_distance = or_width * tp_mult
        if not self.client.check_spread_vs_tp(symbol, tp_distance):
            if self.telegram:
                spread = self.client.get_spread_in_price(symbol)
                pct = spread / tp_distance * 100 if tp_distance > 0 else 0
                self.telegram.notify_order_rejected(
                    symbol, f"Spread {spread:.5f} = {pct:.0f}% del TP (max 30%)")
            return False

        sym_info = self.client.get_symbol_info(symbol)
        balance = self.client.get_account_balance()

        entry = or_low
        sl = or_low - (or_width * sl_mult)
        tp = or_low + (or_width * tp_mult)

        # Valida que el BUY_LIMIT se pueda colocar: el precio no debe haber
        # cruzado OR_LOW todavia.
        ok, reason = self._validate_limit_price(symbol, mt5.ORDER_TYPE_BUY_LIMIT, entry)
        if not ok:
            print(f"[FADE_DOWN] {symbol}: {reason}")
            if self.telegram:
                self.telegram.notify_order_rejected(symbol, f"FADE_DOWN: {reason}")
            return False

        lots = self.allocator.calculate_lots(
            account_balance=balance, entry_price=entry, sl_price=sl,
            tick_value=sym_info.trade_tick_value, tick_size=sym_info.trade_tick_size,
            volume_step=sym_info.volume_step, win_rate=win_rate,
        )

        risk_pct = self.allocator.get_risk_percent(win_rate)
        ctx_short = context[:8] if context != "BASE" else ""
        comment = f"FD|{session}|{ctx_short}".rstrip("|")
        ticket = self._send_pending_order(
            symbol, mt5.ORDER_TYPE_BUY_LIMIT, entry, sl, tp, lots, comment,
            win_rate=win_rate, risk_pct=risk_pct)

        if ticket:
            self.mark_traded_today(symbol, "FADE_DOWN", session)
            # Direction guard: cancel if OR_HIGH breaks first (first_break_dir != DOWN)
            key = f"{symbol}_FADE_DOWN_{session}_{context}"
            self._monitors[key] = {
                "type": "FADE_GUARD",
                "direction": "FADE_DOWN",
                "symbol": symbol,
                "ticket": ticket,
                "cancel_level": or_high,  # cancel if ask >= or_high
                "or_low": or_low,
                "session": session,
            }
            print(f"[FADE] BUY_LIMIT colocada: {symbol} @ {entry:.5f} | SL={sl:.5f} TP={tp:.5f}")
            return True
        return False

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

        risk_pct = self.allocator.get_risk_percent(win_rate)
        ctx_short = context[:8] if context != "BASE" else ""
        comment = f"MU|{session}|{ctx_short}".rstrip("|")
        ticket = self._send_pending_order(
            symbol, mt5.ORDER_TYPE_BUY_STOP, entry, sl, tp, lots, comment,
            win_rate=win_rate, risk_pct=risk_pct)
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

        risk_pct = self.allocator.get_risk_percent(win_rate)
        ctx_short = context[:8] if context != "BASE" else ""
        comment = f"MD|{session}|{ctx_short}".rstrip("|")
        ticket = self._send_pending_order(
            symbol, mt5.ORDER_TYPE_SELL_STOP, entry, sl, tp, lots, comment,
            win_rate=win_rate, risk_pct=risk_pct)
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
        """Process all active monitors (FADE_GUARD + SHAKEOUT). Called from main loop."""
        for key in list(self._monitors.keys()):
            mon = self._monitors[key]
            sym = mon["symbol"]
            tick = mt5.symbol_info_tick(sym)
            if tick is None:
                continue

            if mon["type"] == "FADE_GUARD":
                self._check_fade_guard(key, mon, tick)
            elif mon["type"] == "SHAKEOUT":
                self._check_shakeout_monitor(key, mon, tick)

    def _check_fade_guard(self, key: str, mon: dict, tick):
        """FADE direction guard: cancel limit order if wrong direction breaks first.

        Backtest parity: FADE_UP only activates when first_break_dir == UP.
        If OR_LOW breaks before the SELL_LIMIT at OR_HIGH fills, cancel it.
        """
        ticket = mon["ticket"]

        # Check if the pending order still exists
        orders = self.client.get_pending_orders(mon["symbol"])
        order_exists = any(o.ticket == ticket and o.magic == MAGIC_NUMBER for o in (orders or []))

        if not order_exists:
            # Order filled or was already cancelled — guard no longer needed
            del self._monitors[key]
            return

        # Check if wrong direction broke first
        if mon["direction"] == "FADE_UP" and tick.bid <= mon["cancel_level"]:
            # OR_LOW broke first → first_break_dir would be DOWN → cancel SELL_LIMIT
            self.cancel_order_by_ticket(ticket, mon["symbol"])
            del self._monitors[key]
            print(f"[FADE_GUARD] {key}: DOWN broke first, SELL_LIMIT cancelada")
            if self.telegram:
                self.telegram.notify_order_rejected(
                    mon["symbol"], "FADE_UP cancelada: breakout DOWN primero")

        elif mon["direction"] == "FADE_DOWN" and tick.ask >= mon["cancel_level"]:
            # OR_HIGH broke first → first_break_dir would be UP → cancel BUY_LIMIT
            self.cancel_order_by_ticket(ticket, mon["symbol"])
            del self._monitors[key]
            print(f"[FADE_GUARD] {key}: UP broke first, BUY_LIMIT cancelada")
            if self.telegram:
                self.telegram.notify_order_rejected(
                    mon["symbol"], "FADE_DOWN cancelada: breakout UP primero")

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
