import MetaTrader5 as mt5
import time
from datetime import datetime
import pytz

from src.execution.mt5_client import MT5Client
from src.execution.risk_manager import DynamicRiskAllocator
from src.execution.order_manager import OrderManager

class LiveTraderEngine:
    def __init__(self, config_path: str = "src/execution/bot_config.json"):
        import json
        with open(config_path, "r") as f:
            cfg = json.load(f)
            
        self.risk_percent = cfg.get("risk_percent_per_trade", 0.035)
        self.target_symbols = cfg.get("trinity_portfolio", [])
        
        self.client = MT5Client()
        self.risk = DynamicRiskAllocator(risk_percent_per_trade=self.risk_percent)
        self.om = None

    def _should_execute(self, setup: dict) -> bool:
        # Simplification: Only execute exactly around `magic_time`
        now_utc = datetime.now(pytz.utc).strftime("%H:%M")
        return now_utc == setup["magic_time"]

    def run(self):
        if not self.client.connect(): return
        self.om = OrderManager(self.client, self.risk)

        print("🚀 Quant Trinity Demonio Iniciado. Modo Espera...")
        
        try:
            while True:
                for setup in self.target_symbols:
                    sym = setup["sym"]
                    
                    # Limpieza Orfana Post-Vela Operativa (Simulación)
                    # En producción esto calcularía el "end" de la caja.
                    # Aquí lo hacemos en otra comprobación
                    
                    if self._should_execute(setup):
                        print(f"⏰ [TICKER] Tiempo de ventana abierta para {sym}!")
                        
                        # Extraer caja cruda de la API en vivo
                        rates = mt5.copy_rates_from_pos(sym, mt5.TIMEFRAME_M15, 0, 1)
                        if not rates: continue
                        last_bar = rates[0]
                        range_high = last_bar['high']
                        range_low  = last_bar['low']
                        
                        # Parámetros ORB estándar
                        sl_up = range_low
                        sl_dw = range_high
                        rng = range_high - range_low
                        
                        tp_up = range_high + (rng * setup["tp_opt"])
                        tp_dw = range_low - (rng * setup["tp_opt"])
                        
                        self.om.place_breakout_stop_orders(
                            symbol=sym,
                            range_high=range_high,
                            range_low=range_low,
                            sl_up=sl_up, sl_dw=sl_dw,
                            tp_up=tp_up, tp_dw=tp_dw
                        )
                        
                        # Sleep robusto para no acribillar el servidor el mismo minuto
                        time.sleep(60)

                # Monitoreo de latidos ligeros
                time.sleep(10)
                
        except KeyboardInterrupt:
            print("\n🛑 Demonio Finalizado manualmente.")
        finally:
            self.client.disconnect()

if __name__ == "__main__":
    bot = LiveTraderEngine(risk_percent=0.035)
    bot.run()
