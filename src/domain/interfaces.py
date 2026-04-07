from abc import ABC, abstractmethod
from typing import Dict, Any, List
from src.domain.models import AssetConfig
import polars as pl

class IConfigRepository(ABC):
    @abstractmethod
    def get_config(self, symbol: str) -> AssetConfig:
        pass
        
    @abstractmethod
    def get_all_symbols(self) -> List[str]:
        pass

class IDataLoader(ABC):
    @abstractmethod
    def load_data(self, symbol: str, timeframe: str = "M15") -> pl.DataFrame:
        """Loads historical data for a given symbol."""
        pass
