"""Per-symbol real broker friction table (derived from Vantage VPS symbol_info).

Generic 0.1R / 0.2R assumptions are replaced by an explicit per-symbol
USD-per-round-turn figure (spread entry slippage + commission at vol_min).
The USD figure is converted to R-units given a sl_atr_mult and the symbol's
median ATR in CSV cache:

    risk_usd      = sl_atr_mult * median_atr * (tick_value / tick_size) * vol_min
    friction_R    = total_friction_usd / risk_usd

If risk_usd <= 0 (unknown symbol / no ATR) we fall back to 0.1R.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict

# Per-symbol broker friction snapshot (Vantage VPS, April 2026).
# See task prompt for derivation. Keys use INTERNAL symbol (not broker symbol).
REAL_FRICTION_TABLE: Dict[str, Dict[str, float]] = {
    # FX majors
    "EURUSD": {"spread_pt": 1,  "tick_size": 0.00001, "tick_value": 1.00, "vol_min": 0.01,
               "commission_rt_usd": 7.0, "total_friction_usd": 0.0701},
    "GBPUSD": {"spread_pt": 5,  "tick_size": 0.00001, "tick_value": 1.00, "vol_min": 0.01,
               "commission_rt_usd": 7.0, "total_friction_usd": 0.0705},
    "USDJPY": {"spread_pt": 4,  "tick_size": 0.001,   "tick_value": 0.63, "vol_min": 0.01,
               "commission_rt_usd": 7.0, "total_friction_usd": 0.0725},
    "AUDUSD": {"spread_pt": 2,  "tick_size": 0.00001, "tick_value": 1.00, "vol_min": 0.01,
               "commission_rt_usd": 7.0, "total_friction_usd": 0.0702},
    "GBPJPY": {"spread_pt": 4,  "tick_size": 0.001,   "tick_value": 0.63, "vol_min": 0.01,
               "commission_rt_usd": 7.0, "total_friction_usd": 0.0725},
    "EURJPY": {"spread_pt": 4,  "tick_size": 0.001,   "tick_value": 0.63, "vol_min": 0.01,
               "commission_rt_usd": 7.0, "total_friction_usd": 0.0725},
    "GBPAUD": {"spread_pt": 6,  "tick_size": 0.00001, "tick_value": 0.71, "vol_min": 0.01,
               "commission_rt_usd": 7.0, "total_friction_usd": 0.07043},
    # Metals
    "XAUUSD": {"spread_pt": 12, "tick_size": 0.01,    "tick_value": 1.00, "vol_min": 0.01,
               "commission_rt_usd": 7.0, "total_friction_usd": 0.0712},
    "XAGUSD": {"spread_pt": 44, "tick_size": 0.001,   "tick_value": 5.00, "vol_min": 0.01,
               "commission_rt_usd": 3.5, "total_friction_usd": 0.057},
    # Energies
    "WTI":    {"spread_pt": 47, "tick_size": 0.001,   "tick_value": 1.00, "vol_min": 0.01,
               "commission_rt_usd": 3.5, "total_friction_usd": 0.082},
    "BRENT":  {"spread_pt": 47, "tick_size": 0.001,   "tick_value": 1.00, "vol_min": 0.01,
               "commission_rt_usd": 3.5, "total_friction_usd": 0.082},
    "NATGAS": {"spread_pt": 200,"tick_size": 0.001,   "tick_value": 1.00, "vol_min": 0.01,
               "commission_rt_usd": 3.5, "total_friction_usd": 0.235},
    # Indices
    "SP500":     {"spread_pt": 36,  "tick_size": 0.01, "tick_value": 0.01, "vol_min": 0.1,
                  "commission_rt_usd": 3.5, "total_friction_usd": 0.354},
    "NASDAQ100": {"spread_pt": 80,  "tick_size": 0.01, "tick_value": 0.01, "vol_min": 0.1,
                  "commission_rt_usd": 7.0, "total_friction_usd": 0.708},
    "VIX":       {"spread_pt": 103, "tick_size": 0.001,"tick_value": 1.00, "vol_min": 0.1,
                  "commission_rt_usd": 3.5, "total_friction_usd": 0.453},
}

_FALLBACK_R = 0.1
_ENRICHED_CACHE = Path("data/enriched_math")
_MEDIAN_ATR_CACHE: Dict[str, float] = {}


def friction_r(symbol: str, sl_atr_mult: float, median_atr: float) -> float:
    """Convert USD friction to R-units using per-symbol median ATR.

    risk_usd = sl_atr_mult * median_atr * (tick_value / tick_size) * vol_min
    friction_R = total_friction_usd / risk_usd
    """
    entry = REAL_FRICTION_TABLE.get(symbol)
    if entry is None or median_atr is None or median_atr <= 0 or sl_atr_mult <= 0:
        return _FALLBACK_R
    unit_per_point = entry["tick_value"] / entry["tick_size"]
    risk_usd = sl_atr_mult * median_atr * unit_per_point * entry["vol_min"]
    if risk_usd <= 0:
        return _FALLBACK_R
    return entry["total_friction_usd"] / risk_usd


def load_median_atr(symbol: str) -> float:
    """Median ATR(14) from the enriched M15 cache. Memoised."""
    if symbol in _MEDIAN_ATR_CACHE:
        return _MEDIAN_ATR_CACHE[symbol]
    path = _ENRICHED_CACHE / f"{symbol}_M15.parquet"
    if not path.exists():
        _MEDIAN_ATR_CACHE[symbol] = 0.0
        return 0.0
    import polars as pl
    df = pl.read_parquet(path, columns=["atr_14"])
    med = df["atr_14"].median()
    val = float(med) if med is not None else 0.0
    _MEDIAN_ATR_CACHE[symbol] = val
    return val


def friction_r_for(symbol: str, sl_atr_mult: float) -> float:
    """Convenience: auto-load median ATR from cache."""
    return friction_r(symbol, sl_atr_mult, load_median_atr(symbol))


def median_atr_per_symbol(symbols) -> Dict[str, float]:
    """Eagerly load median ATR for a list of symbols."""
    return {s: load_median_atr(s) for s in symbols}
