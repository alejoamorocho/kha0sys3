"""
Dynamic Risk Allocator — Kha0sys3 v2
Position sizing con riesgo escalado por win rate historico.
Rango: 1% (WR=57%) a 6% (WR=91%), interpolacion lineal.
"""

import math

from src.domain.constants import RISK_MIN_PCT, RISK_MAX_PCT, RISK_TIERS, WR_MIN, WR_MAX, MAGIC_NUMBER, DEFAULT_WIN_RATE


class DynamicRiskAllocator:
    """Calcula volumen de lotes con riesgo dinamico basado en WR del setup.

    Riesgo escalonado por balance:
      < $2k  → 2.5% – 15%  (growth)
      $2k–8k → 1.67% – 10% (consolidation)
      > $8k  → 1% – 6%     (preservation)
    """

    def __init__(self, min_risk: float = RISK_MIN_PCT, max_risk: float = RISK_MAX_PCT,
                 min_wr: float = WR_MIN, max_wr: float = WR_MAX,
                 risk_tiers: list | None = None, tiers: list | None = None):
        self.min_risk = min_risk
        self.max_risk = max_risk
        self.min_wr = min_wr
        self.max_wr = max_wr
        # Accept 'tiers' from bot_config.json (list of dicts) or 'risk_tiers' (list of tuples)
        if risk_tiers:
            self.risk_tiers = risk_tiers
        elif tiers:
            self.risk_tiers = [
                (t.get("max_balance"), t["min_risk"], t["max_risk"])
                for t in tiers
            ]
        else:
            self.risk_tiers = RISK_TIERS

    def _get_tier_limits(self, balance: float | None) -> tuple[float, float]:
        """Retorna (min_risk, max_risk) para el tier correspondiente al balance."""
        if balance is None:
            return self.min_risk, self.max_risk
        for max_bal, tier_min, tier_max in self.risk_tiers:
            if max_bal is None or balance < max_bal:
                return tier_min, tier_max
        return self.min_risk, self.max_risk

    def get_risk_percent(self, win_rate: float, balance: float = None) -> float:
        """Calcula el % de riesgo basado en WR y tier de balance."""
        min_r, max_r = self._get_tier_limits(balance)
        if win_rate <= self.min_wr:
            return min_r
        if win_rate >= self.max_wr:
            return max_r
        # Interpolacion lineal
        ratio = (win_rate - self.min_wr) / (self.max_wr - self.min_wr)
        return min_r + ratio * (max_r - min_r)

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

        risk_pct = self.get_risk_percent(win_rate, balance=account_balance)
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


class BalanceTieredRiskAllocator(DynamicRiskAllocator):
    """Risk allocator with balance-based tiers. Max risk decreases as balance grows.

    Tiers is a list of dicts, each with keys:
      - max_balance (float or None): upper bound of this tier (None = final tier)
      - min_risk:    minimum risk pct for this tier
      - max_risk:    maximum risk pct for this tier

    The right tier is picked every call based on current account balance.
    WR still scales risk linearly inside [min_risk, max_risk] of the active tier.
    """

    def __init__(self, tiers: list[dict], min_wr: float = WR_MIN,
                 max_wr: float = WR_MAX):
        self.tiers = tiers
        self.min_wr = min_wr
        self.max_wr = max_wr
        # Initialize parent with tier 1 defaults (fallback before balance known)
        t0 = tiers[0] if tiers else {"min_risk": RISK_MIN_PCT, "max_risk": RISK_MAX_PCT}
        super().__init__(
            min_risk=t0["min_risk"], max_risk=t0["max_risk"],
            min_wr=min_wr, max_wr=max_wr,
        )

    def _tier_for_balance(self, balance: float) -> dict:
        for t in self.tiers:
            mb = t.get("max_balance")
            if mb is None or balance <= mb:
                return t
        return self.tiers[-1]

    def get_risk_percent(self, win_rate: float, account_balance: float = 0.0) -> float:
        tier = self._tier_for_balance(account_balance)
        min_r = tier["min_risk"]
        max_r = tier["max_risk"]
        if win_rate <= self.min_wr:
            return min_r
        if win_rate >= self.max_wr:
            return max_r
        ratio = (win_rate - self.min_wr) / (self.max_wr - self.min_wr)
        return min_r + ratio * (max_r - min_r)

    def calculate_lots(self, account_balance: float, entry_price: float,
                       sl_price: float, tick_value: float, tick_size: float,
                       volume_step: float, win_rate: float = DEFAULT_WIN_RATE) -> float:
        if tick_value <= 0 or tick_size <= 0 or volume_step <= 0:
            return 0.0
        # Balance-tiered risk pct
        risk_pct = self.get_risk_percent(win_rate, account_balance)
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
        if lots < volume_step:
            lots = volume_step
            actual_risk = (lots * loss_per_1_lot) / account_balance
            tier = self._tier_for_balance(account_balance)
            print(f"[RISK-TIERED] Min lot override: {lots} lots | Target={risk_pct:.2%} "
                  f"Actual={actual_risk:.2%} Tier_max={tier['max_risk']:.1%} bal=${account_balance:.0f}")
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
