"""
Dynamic Risk Allocator — Kha0sys3 v2
Position sizing con riesgo escalado por win rate historico.
Rango: 1% (WR=57%) a 6% (WR=91%), interpolacion lineal.
"""

import math

from src.domain.constants import RISK_MIN_PCT, RISK_MAX_PCT, WR_MIN, WR_MAX, MAGIC_NUMBER, DEFAULT_WIN_RATE


class DynamicRiskAllocator:
    """Calcula volumen de lotes con riesgo dinamico basado en WR del setup."""

    def __init__(self, min_risk: float = RISK_MIN_PCT, max_risk: float = RISK_MAX_PCT,
                 min_wr: float = WR_MIN, max_wr: float = WR_MAX):
        self.min_risk = min_risk
        self.max_risk = max_risk
        self.min_wr = min_wr
        self.max_wr = max_wr

    def get_risk_percent(self, win_rate: float) -> float:
        """Calcula el % de riesgo basado en el win rate historico del setup."""
        if win_rate <= self.min_wr:
            return self.min_risk
        if win_rate >= self.max_wr:
            return self.max_risk
        # Interpolacion lineal
        ratio = (win_rate - self.min_wr) / (self.max_wr - self.min_wr)
        return self.min_risk + ratio * (self.max_risk - self.min_risk)

    def calculate_lots(self, account_balance: float, entry_price: float,
                       sl_price: float, tick_value: float, tick_size: float,
                       volume_step: float, win_rate: float = DEFAULT_WIN_RATE) -> float:
        """Determina el volumen de lotes arriesgando un % dinamico del balance.

        Args:
            account_balance: Balance settled de la cuenta (NO free_margin).
            entry_price: Precio de entrada.
            sl_price: Precio del stop loss.
            tick_value: Valor monetario de 1 tick para 1 lote.
            tick_size: Tamano de 1 tick en precio.
            volume_step: Paso minimo de volumen del broker.
            win_rate: Win rate historico del setup (para escalar riesgo).
        """
        if tick_value <= 0 or tick_size <= 0 or volume_step <= 0:
            return 0.0

        risk_pct = self.get_risk_percent(win_rate)
        risk_money = account_balance * risk_pct

        price_diff = abs(entry_price - sl_price)
        if price_diff <= 0:
            return 0.0

        ticks_at_risk = price_diff / tick_size
        loss_per_1_lot = ticks_at_risk * tick_value

        if loss_per_1_lot <= 0:
            return 0.0

        raw_lots = risk_money / loss_per_1_lot
        lots = math.floor(raw_lots / volume_step) * volume_step

        # Si el calculo da menos del lote minimo, usar el lote minimo
        # (acepta un leve over-risk en vez de rechazar el trade)
        if lots < volume_step:
            lots = volume_step
            actual_risk = (lots * loss_per_1_lot) / account_balance
            print(f"[RISK] Min lot override: {lots} lots | Target risk={risk_pct:.2%} | Actual risk={actual_risk:.2%}")

        return round(lots, 2)


class SLGuardian:
    """Proteccion contra slippage que salta el SL.

    Cada 10s revisa posiciones abiertas del bot. Si el precio actual
    esta MAS ALLA del SL (gap/flash crash hizo que el SL no se ejecutara),
    cierra la posicion a mercado inmediatamente.
    """

    @staticmethod
    def find_breached_positions(positions, magic: int = MAGIC_NUMBER) -> list:
        breached = []
        if not positions:
            return breached

        for p in positions:
            if p.magic != magic:
                continue
            if p.sl == 0.0:
                continue

            if p.type == 0:  # BUY
                if p.price_current <= p.sl:
                    breached.append(p)
            elif p.type == 1:  # SELL
                if p.price_current >= p.sl:
                    breached.append(p)

        return breached
