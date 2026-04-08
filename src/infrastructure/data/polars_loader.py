"""Cargador de datos historicos M15 desde CSV usando Polars."""

import polars as pl
from pathlib import Path
from src.domain.interfaces import IDataLoader

class CSVPolarsLoader(IDataLoader):
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)

    def load_data(self, symbol: str, timeframe: str = "M15") -> pl.DataFrame:
        """
        Loads historical data for a given symbol and timeframe from CSV.
        Expected filename convention: {SYMBOL}_{TIMEFRAME}_*.csv
        """
        # Find the matching file. Since there are dates in there, we use glob.
        pattern = f"{symbol}_{timeframe}_*.csv"
        matching_files = list(self.data_dir.glob(pattern))
        
        if not matching_files:
            raise FileNotFoundError(f"No files found for {symbol} with timeframe {timeframe} in {self.data_dir}")
            
        # We assume one consolidated file per timeframe/symbol or we lazy scan all matching
        file_path = matching_files[0]
        
        # Load using polars lazy frame if possible, or read directly. 
        # Dates are in format 2018-01-01 22:00:00+00:00
        df = pl.read_csv(
            file_path,
            has_header=True
        )
        
        # Clean col names natively
        df = df.rename({col: col.strip().lower() for col in df.columns})
        
        # Convert time to datetime by stripping the +00:00 manually for robustness
        df = df.with_columns(
            pl.col("time").str.slice(0, 19).str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S", strict=False)
        )
        
        # Sort by time just in case
        df = df.sort("time")
        
        # Calculate daily ATR proxy: we can calculate True Range here or in application layer.
        # It's better to do basic technical prep in application layer.
        
        return df
