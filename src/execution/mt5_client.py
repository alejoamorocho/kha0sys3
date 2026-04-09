"""
MT5 Client — Kha0sys3
Gateway stateless para MetaTrader 5 con reconexión automática y cálculo de ATR14.
"""

import MetaTrader5 as mt5
import time
import math
from datetime import datetime, timezone
from typing import Optional


class MT5Client:
    """Gateway interface para MetaTrader 5. Stateless con reconexión automática."""

    MAX_RECONNECT_ATTEMPTS = 3
    RECONNECT_DELAY_BASE = 2  # segundos, escala exponencial

    def __init__(self):
        self.connected = False

    def connect(self) -> bool:
        """Inicializa conexion con MetaTrader 5."""
        if not mt5.initialize():
            print("MT5Client: initialize() failed. Check MT5 Terminal.")
            mt5.shutdown()
            return False
        self.connected = True
        print("MT5Client: Conectado a MetaTrader 5.")
        return True

    def ensure_connected(self) -> bool:
        """Verifica conexión y reconecta automáticamente si es necesario."""
        term = mt5.terminal_info()
        if term and term.connected:
            self.connected = True
            return True

        print("MT5Client: Conexión perdida. Intentando reconectar...")
        for attempt in range(self.MAX_RECONNECT_ATTEMPTS):
            mt5.shutdown()
            time.sleep(self.RECONNECT_DELAY_BASE ** attempt)
            if mt5.initialize():
                self.connected = True
                print(f"MT5Client: Reconectado en intento {attempt + 1}.")
                return True

        self.connected = False
        print("MT5Client: Reconexión fallida tras todos los intentos.")
        return False

    def disconnect(self):
        """Cierra la conexion con MetaTrader 5."""
        if self.connected:
            mt5.shutdown()
            self.connected = False

    def get_account_balance(self) -> float:
        """Devuelve el balance settled de la cuenta (base para position sizing)."""
        info = mt5.account_info()
        if info is None:
            raise ConnectionError("No se pudo obtener información de cuenta.")
        return info.balance

    def get_account_info(self):
        """Devuelve el objeto completo de cuenta MT5."""
        info = mt5.account_info()
        if info is None:
            raise ConnectionError("No se pudo obtener información de cuenta.")
        return info

    def get_symbol_info(self, symbol: str):
        """Obtiene info del simbolo MT5. Activa el simbolo si no es visible."""
        info = mt5.symbol_info(symbol)
        if info is None:
            raise ValueError(f"Símbolo {symbol} no encontrado.")
        if not info.visible:
            mt5.symbol_select(symbol, True)
            info = mt5.symbol_info(symbol)
        return info

    def get_current_spread(self, symbol: str) -> float:
        """Devuelve el spread actual en puntos reales del broker."""
        info = self.get_symbol_info(symbol)
        return info.spread

    def get_average_spread(self, symbol: str, lookback_bars: int = 10) -> float:
        """Calcula el spread promedio reciente basándose en barras M15."""
        rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 0, lookback_bars)
        if rates is None or len(rates) == 0:
            return float("inf")
        spreads = [r["spread"] for r in rates]
        return sum(spreads) / len(spreads)

    def check_spread_friction(self, symbol: str, threshold_multiplier: float = 1.5,
                              min_spread_floor: float = 5.0) -> bool:
        """Valida si el spread actual es atípicamente alto comparado con la media.

        Usa un piso mínimo para evitar falsos positivos cuando spread promedio es 0.
        """
        current = self.get_current_spread(symbol)
        avg = self.get_average_spread(symbol)
        baseline = max(avg, min_spread_floor)
        safe = current <= (baseline * threshold_multiplier)
        if not safe:
            print(f"Spread {symbol}: Actual={current} | Baseline={baseline:.1f} | Rechazado.")
        return safe

    def get_spread_in_price(self, symbol: str) -> float:
        """Devuelve el spread actual en unidades de precio (ask - bid)."""
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            return float("inf")
        return tick.ask - tick.bid

    def check_spread_vs_tp(self, symbol: str, tp_distance: float,
                           max_spread_pct: float = 0.30) -> bool:
        """Valida que el spread no supere max_spread_pct del TP distance.

        Protege contra spreads que se comen la ganancia.
        Con TP=0.5*OR_WIDTH, un spread del 30% del TP = 15% del OR_WIDTH.

        Args:
            symbol: Simbolo MT5.
            tp_distance: Distancia en precio del entry al TP (tp_mult * or_width).
            max_spread_pct: Maximo % del TP que el spread puede representar.

        Returns:
            True si el spread es aceptable, False si es demasiado alto.
        """
        if tp_distance <= 0:
            return False
        spread = self.get_spread_in_price(symbol)
        pct = spread / tp_distance
        safe = pct <= max_spread_pct
        if not safe:
            print(f"[SPREAD] {symbol}: spread={spread:.5f} | TP_dist={tp_distance:.5f} | "
                  f"{pct:.1%} del TP (max {max_spread_pct:.0%}) | Rechazado.")
        return safe

    def get_open_positions(self, symbol: str):
        """Posiciones activas para un símbolo."""
        positions = mt5.positions_get(symbol=symbol)
        if positions is None:
            return []
        return positions

    def get_pending_orders(self, symbol: str):
        """Órdenes pendientes para un símbolo."""
        orders = mt5.orders_get(symbol=symbol)
        if orders is None:
            return []
        return orders

    def send_order_raw(self, request: dict) -> dict:
        """Envía solicitud raw al servidor con guard contra None."""
        result = mt5.order_send(request)
        if result is None:
            print(f"order_send returned None para {request.get('symbol')}: {mt5.last_error()}")
            return {"retcode": -1}
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Error orden {request.get('symbol')}: {result.retcode} - {mt5.last_error()}")
        return result._asdict()

    def calculate_atr14(self, symbol: str) -> Optional[float]:
        """Calcula ATR(14) desde barras D1 de MT5.

        Usa True Range: max(H-L, |H-PrevClose|, |L-PrevClose|)
        ATR = SMA(14) del True Range, shifted 1 día (sin look-ahead).
        """
        # Necesitamos 15 barras D1 (14 para ATR + 1 para el shift)
        rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_D1, 0, 16)
        if rates is None or len(rates) < 15:
            return None

        true_ranges = []
        for i in range(1, len(rates)):
            high = rates[i]['high']
            low = rates[i]['low']
            prev_close = rates[i - 1]['close']

            tr = max(
                high - low,
                abs(high - prev_close),
                abs(low - prev_close),
            )
            true_ranges.append(tr)

        if len(true_ranges) < 14:
            return None

        # SMA de los últimos 14 TRs (excluyendo el día actual = shifted)
        atr14 = sum(true_ranges[-15:-1]) / 14
        return atr14

    def get_previous_day_close(self, symbol: str) -> Optional[float]:
        """Obtiene el cierre del D1 anterior (para MAGNET_CLOSE).

        Consistente con backtest: d_close.shift(1) = cierre del día completado anterior.
        """
        rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_D1, 1, 1)
        if rates is None or len(rates) == 0:
            return None
        return rates[0]['close']

    def get_or_from_closed_bars(self, symbol: str, duration_mins: int = 15) -> Optional[dict]:
        """Obtiene Opening Range de las barras M15 CERRADAS necesarias.

        Si duration_mins=30, agrupa las últimas 2 velas de 15m.
        Retorna dict con high, low, width o None si no hay datos.
        """
        n_bars = int(duration_mins / 15)
        rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 1, n_bars)
        if rates is None or len(rates) < n_bars:
            return None

        # Agregación de High y Low sobre el bloque de velas
        highs = [r['high'] for r in rates]
        lows = [r['low'] for r in rates]

        o_high = max(highs)
        o_low = min(lows)

        return {
            "high": o_high,
            "low": o_low,
            "width": o_high - o_low,
            "open": rates[-1]['open'],   # Apertura de la primera vela (la mas vieja en el array)
            "close": rates[0]['close'],  # Cierre de la ultima vela (la mas reciente)
            "time": rates[0]['time'],
        }
