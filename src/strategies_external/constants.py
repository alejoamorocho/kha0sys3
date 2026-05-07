"""Constantes locales del módulo strategies_external.

Replicamos friction y risk del bot live para que las métricas sean comparables.
NO importamos de src/domain/constants.py para mantener el aislamiento.
"""

from typing import Final

# Friction en R aplicado al cierre de cada trade.
FRICTION_R_FOREX: Final[float] = 0.1
FRICTION_R_COMMODITY_INDEX: Final[float] = 0.2

# Position sizing default (parametrizable por runner).
RISK_PER_TRADE_PCT_DEFAULT: Final[float] = 0.005

# Slippage en la entrada por orden tipo stop/limit.
SLIPPAGE_PIPS_FX: Final[float] = 0.5
SLIPPAGE_TICKS_INDEX_COMMODITY: Final[int] = 1

# Asset class mapping.
ASSET_CLASS_FOREX: Final[frozenset[str]] = frozenset({
    "AUDUSD", "EURJPY", "EURUSD", "GBPAUD", "GBPJPY", "GBPUSD", "USDJPY",
})
ASSET_CLASS_METALS: Final[frozenset[str]] = frozenset({"XAUUSD", "XAGUSD"})
ASSET_CLASS_ENERGY: Final[frozenset[str]] = frozenset({"WTI", "BRENT", "NATGAS"})
ASSET_CLASS_INDEX: Final[frozenset[str]] = frozenset({"SP500", "NASDAQ100", "VIX"})


def friction_for(symbol: str) -> float:
    """Friction en R según asset class del símbolo."""
    if symbol in ASSET_CLASS_FOREX:
        return FRICTION_R_FOREX
    return FRICTION_R_COMMODITY_INDEX
