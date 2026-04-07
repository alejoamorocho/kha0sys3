"""
Symbol Mapper — Kha0sys3
Traduce entre nombres internos del sistema y nombres reales del broker MT5 (Vantage).
"""

from pathlib import Path
from typing import Optional


class SymbolMapper:
    """Mapeo bidireccional entre nombres internos y nombres MT5 Vantage."""

    def __init__(self, config_path: str = "config/symbol_mapping.yaml"):
        self._internal_to_mt5: dict[str, str] = {}
        self._mt5_to_internal: dict[str, str] = {}
        self._load(config_path)

    def _load(self, config_path: str):
        path = Path(config_path)
        if path.exists():
            import yaml
            with open(path, "r") as f:
                cfg = yaml.safe_load(f)
            mapping = cfg.get("mapping", {})
            for internal, mt5_name in mapping.items():
                self._internal_to_mt5[internal] = mt5_name
                self._mt5_to_internal[mt5_name] = internal
        else:
            # Fallback hardcodeado (Vantage International)
            defaults = {
                "AUDUSD": "AUDUSD+",
                "BRENT": "UKOUSD",
                "EURJPY": "EURJPY+",
                "EURUSD": "EURUSD+",
                "GBPAUD": "GBPAUD+",
                "GBPJPY": "GBPJPY+",
                "GBPUSD": "GBPUSD+",
                "NASDAQ100": "NAS100",
                "NATGAS": "NG-C",
                "SP500": "SP500",
                "USDJPY": "USDJPY+",
                "WTI": "USOUSD",
                "XAGUSD": "XAGUSD",
                "XAUUSD": "XAUUSD+",
            }
            for internal, mt5_name in defaults.items():
                self._internal_to_mt5[internal] = mt5_name
                self._mt5_to_internal[mt5_name] = internal

    def to_mt5(self, internal_name: str) -> str:
        """Convierte nombre interno a nombre MT5 del broker."""
        return self._internal_to_mt5.get(internal_name, internal_name)

    def to_internal(self, mt5_name: str) -> str:
        """Convierte nombre MT5 del broker a nombre interno."""
        return self._mt5_to_internal.get(mt5_name, mt5_name)

    def get_all_mt5_symbols(self) -> list[str]:
        """Devuelve todos los simbolos MT5 disponibles."""
        return list(self._internal_to_mt5.values())

    def get_all_internal_symbols(self) -> list[str]:
        """Devuelve todos los nombres internos."""
        return list(self._internal_to_mt5.keys())
