import MetaTrader5 as mt5
import time
import pandas as pd
from typing import Optional, List, Dict

class MT5Client:
    """Gateway interface para interactuar con MetaTrader 5 asumiendo filosofía Stateless."""
    
    def __init__(self):
        self.connected = False

    def connect(self) -> bool:
        if not mt5.initialize():
            print("❌ MT5Client: initialize() failed. Check MT5 Terminal.")
            mt5.shutdown()
            return False
        self.connected = True
        print("✅ MT5Client: Conectado a MetaTrader 5.")
        return True

    def disconnect(self):
        if self.connected:
            mt5.shutdown()
            self.connected = False
            
    def get_account_free_margin(self) -> float:
        info = mt5.account_info()
        if info is None:
            raise ConnectionError("No se pudo obtener información de cuenta.")
        return info.margin_free
        
    def get_symbol_info(self, symbol: str):
        info = mt5.symbol_info(symbol)
        if info is None:
            raise ValueError(f"Símbolo {symbol} no encontrado.")
        if not info.visible:
            mt5.symbol_select(symbol, True)
            info = mt5.symbol_info(symbol)
        return info

    def get_current_spread(self, symbol: str) -> float:
        """Devuelve el spread actual en Puntos reales del broker"""
        info = self.get_symbol_info(symbol)
        return info.spread
        
    def get_average_spread(self, symbol: str, lookback_bars: int = 10) -> float:
        """Calcula el spread promedio reciente basándose en barras M15."""
        rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 0, lookback_bars)
        if rates is None or len(rates) == 0:
            return float('inf')
        spreads = [r['spread'] for r in rates]
        return sum(spreads) / len(spreads)
        
    def check_spread_friction(self, symbol: str, threshold_multiplier: float = 1.5) -> bool:
        """Valida si el spread actual es atípicamente alto comparado con la media reciente."""
        current = self.get_current_spread(symbol)
        avg = self.get_average_spread(symbol)
        # Si el spread actual supera por más de X veces el promedio, hay fricción peligrosa.
        safe = current <= (avg * threshold_multiplier)
        if not safe:
            print(f"⚠️ Alerta Spread {symbol}: Actual={current} | Media={avg:.1f} | Rechazado.")
        return safe

    def get_open_positions(self, symbol: str):
        """Lectura In-Vivo de posiciones activas. Diseño Stateless."""
        positions = mt5.positions_get(symbol=symbol)
        if positions is None:
            return []
        return positions

    def get_pending_orders(self, symbol: str):
        """Lectura In-Vivo de órdenes limit/stop pendientes no ejecutadas."""
        orders = mt5.orders_get(symbol=symbol)
        if orders is None:
            return []
        return orders

    def send_order_raw(self, request: dict) -> dict:
        """Envía solicitud raw al servidor."""
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"❌ Error enviando Orden a {request.get('symbol')}: {result.retcode} - {mt5.last_error()}")
        return result._asdict() if result else {}
