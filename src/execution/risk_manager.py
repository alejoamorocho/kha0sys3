"""
Dynamic Risk Allocator — Kha0sys3
Calculadora de position sizing basada en BALANCE (no free_margin).
"""

import math


class DynamicRiskAllocator:
    """Calcula volumen exacto de lotes arriesgando un porcentaje fijo del balance."""

    def __init__(self, risk_percent_per_trade: float = 0.035):
        self.risk_pct = risk_percent_per_trade

    def calculate_lots(self, account_balance: float, entry_price: float,
                       sl_price: float, tick_value: float, tick_size: float,
                       volume_step: float) -> float:
        """Determina el volumen de lotes para arriesgar risk_pct del balance.

        Args:
            account_balance: Balance settled de la cuenta (NO free_margin).
            entry_price: Precio de entrada.
            sl_price: Precio del stop loss.
            tick_value: Valor monetario de 1 tick para 1 lote.
            tick_size: Tamaño de 1 tick en precio.
            volume_step: Paso mínimo de volumen del broker.
        """
        if tick_value <= 0:
            return 0.0
        if tick_size <= 0:
            return 0.0
        if volume_step <= 0:
            return 0.0

        risk_money = account_balance * self.risk_pct

        price_diff = abs(entry_price - sl_price)
        if price_diff <= 0:
            return 0.0

        ticks_at_risk = price_diff / tick_size
        loss_per_1_lot = ticks_at_risk * tick_value

        if loss_per_1_lot <= 0:
            return 0.0

        raw_lots = risk_money / loss_per_1_lot
        lots = math.floor(raw_lots / volume_step) * volume_step

        return round(lots, 2)
