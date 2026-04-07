"""
Dynamic Risk Allocator — Kha0sys3
Calculadora de position sizing basada en BALANCE (no free_margin).
"""

import math


class DynamicRiskAllocator:
    """Calcula volumen exacto de lotes arriesgando un porcentaje fijo del balance."""

    def __init__(self, risk_percent_per_trade: float = 0.03):
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


class SLGuardian:
    """Proteccion contra slippage que salta el SL.

    Cada 10s revisa posiciones abiertas del bot. Si el precio actual
    esta MAS ALLA del SL (gap/flash crash hizo que el SL no se ejecutara),
    cierra la posicion a mercado inmediatamente.
    """

    SL_BREACH_MARGIN = 0.0001  # tolerancia minima para evitar falsos positivos

    @staticmethod
    def find_breached_positions(positions, magic: int = 1337) -> list:
        """Retorna posiciones donde el precio paso el SL sin cerrarse.

        Args:
            positions: lista de posiciones de mt5.positions_get()
            magic: magic number del bot

        Returns:
            lista de posiciones que deben cerrarse de emergencia
        """
        breached = []
        if not positions:
            return breached

        for p in positions:
            if p.magic != magic:
                continue
            if p.sl == 0.0:
                continue

            # BUY: SL esta debajo del precio de entrada. Si bid <= SL, el SL fallo.
            if p.type == 0:  # POSITION_TYPE_BUY
                if p.price_current <= p.sl:
                    breached.append(p)
            # SELL: SL esta arriba del precio de entrada. Si ask >= SL, el SL fallo.
            elif p.type == 1:  # POSITION_TYPE_SELL
                if p.price_current >= p.sl:
                    breached.append(p)

        return breached
