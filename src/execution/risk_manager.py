class DynamicRiskAllocator:
    """Calculadora centralizada de gestión de riesgo financiero."""
    
    def __init__(self, risk_percent_per_trade: float = 0.035):
        # 3.5% default as requested by Kamikaze Model
        self.risk_pct = risk_percent_per_trade
        
    def calculate_lots(self, free_margin: float, entry_price: float, sl_price: float, tick_value: float, tick_size: float, volume_step: float) -> float:
        """
        Determina el volumen exacto de lotes para arriesgar el R-Percent exacto del balance libre.
        """
        risk_money = free_margin * self.risk_pct
        
        # Diferencia en precio
        price_diff = abs(entry_price - sl_price)
        if price_diff <= 0:
            return 0.0
            
        # Cuantos ticks/puntos hay de distancia al StopLoss
        ticks_at_risk = price_diff / tick_size
        
        # Dinero que se pierde operando 1 Lote base
        loss_per_1_lot = ticks_at_risk * tick_value
        if loss_per_1_lot <= 0:
            return 0.0
            
        # Cuantos lotes puedo comprar
        raw_lots = risk_money / loss_per_1_lot
        
        # Redondear al Volume Step del broker (Ej: 0.01)
        import math
        lots = math.floor(raw_lots / volume_step) * volume_step
        
        # Redondear decimales para MT5
        return round(lots, 2)
