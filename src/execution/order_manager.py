import MetaTrader5 as mt5
from src.execution.mt5_client import MT5Client
from src.execution.risk_manager import DynamicRiskAllocator

class OrderManager:
    """Maneja el ciclo de vida de las ordenes asegurando arquitectura defensiva."""
    
    def __init__(self, mt5_client: MT5Client, allocator: DynamicRiskAllocator):
        self.client = mt5_client
        self.allocator = allocator
        
    def cancel_orphan_orders(self, symbol: str):
        """Elimina ordenes pendientes que no detonaron durante la vela operativa."""
        orders = self.client.get_pending_orders(symbol)
        if not orders: return 0
        
        count = 0
        for o in orders:
            req = {
                "action": mt5.TRADE_ACTION_REMOVE,
                "order": o.ticket,
                "symbol": symbol
            }
            res = self.client.send_order_raw(req)
            if res.get('retcode') == mt5.TRADE_RETCODE_DONE:
                count += 1
        return count

    def is_already_exposed(self, symbol: str) -> bool:
        """Verifica puramente en el broker si ya estamos comprados/vendidos o con limites clavados en este activo."""
        positions = self.client.get_open_positions(symbol)
        orders = self.client.get_pending_orders(symbol)
        return len(positions) > 0 or len(orders) > 0

    def place_breakout_stop_orders(self, symbol: str,
                                   range_high: float, range_low: float, 
                                   sl_up: float, sl_dw: float, 
                                   tp_up: float, tp_dw: float):
        """Envía OCO Limits (StopBuy y StopSell) anclados a hardware con TP/SL fijos calculando Kamikaze Risk."""
        
        # 1. Chequeo Defensivo: No rebotar ordenes si ya estamos expuestos 
        if self.is_already_exposed(symbol):
            print(f"🛡️ OrderManager: Exposición existente en {symbol}. Standby.")
            return False
            
        # 2. Chequeo Defensivo: Spread Filter
        if not self.client.check_spread_friction(symbol):
            return False
            
        # 3. Matemática de Riesgo Kamikaze
        sym_info = self.client.get_symbol_info(symbol)
        margin = self.client.get_account_free_margin()
        
        # BUY STOP Calcs
        lots_up = self.allocator.calculate_lots(
            free_margin=margin, 
            entry_price=range_high, 
            sl_price=sl_up, 
            tick_value=sym_info.trade_tick_value, 
            tick_size=sym_info.trade_tick_size, 
            volume_step=sym_info.volume_step
        )
        
        # SELL STOP Calcs
        lots_dw = self.allocator.calculate_lots(
            free_margin=margin, 
            entry_price=range_low, 
            sl_price=sl_dw, 
            tick_value=sym_info.trade_tick_value, 
            tick_size=sym_info.trade_tick_size, 
            volume_step=sym_info.volume_step
        )
        
        def send_stop(tipo, price, sl, tp, volume, comment):
            if volume < sym_info.volume_min:
                print(f"⚠️ Margen libre pobre para lotaje en {symbol}.")
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
                "magic": 1337,
                "comment": comment,
                "type_time": mt5.ORDER_TIME_GTC, # Dependemos de nuestra limpieza Stateless
                "type_filling": mt5.ORDER_FILLING_FOK
            }
            res = self.client.send_order_raw(req)
            return res.get('retcode') == mt5.TRADE_RETCODE_DONE

        # Enviar doble tiro periférico
        up_ok = send_stop(mt5.ORDER_TYPE_BUY_STOP, range_high, sl_up, tp_up, lots_up, "ORB_Quant_UP")
        dw_ok = send_stop(mt5.ORDER_TYPE_SELL_STOP, range_low, sl_dw, tp_dw, lots_dw, "ORB_Quant_DW")
        
        return up_ok or dw_ok
