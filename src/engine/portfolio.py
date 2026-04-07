import polars as pl
from typing import List

class PortfolioEvaluator:
    @staticmethod
    def evaluate(individual_results: List[pl.DataFrame], initial_capital: float = 100000, risk_per_trade: float = 0.005) -> pl.DataFrame:
        """
        Combines all trade logs from multiple assets, assumes `risk_per_trade` (e.g. 0.005 = 0.5% percent)
        and computes global equity curve and drawdowns.
        """
        combined = pl.DataFrame()
        for res in individual_results:
            df_filtered = res.filter(pl.col("r_multiple") != 0.0).select([
                "trade_date", "first_break_dir", "r_multiple"
            ])
            if combined.is_empty():
                combined = df_filtered
            else:
                combined = pl.concat([combined, df_filtered])
                
        # Sort entirely by date
        combined = combined.sort("trade_date")
        
        # Calculate capital curve
        combined_pd = combined.to_pandas()
        capital = initial_capital
        equity_curve = []
        for idx, row in combined_pd.iterrows():
            trade_pnl = capital * risk_per_trade * row["r_multiple"]
            capital += trade_pnl
            equity_curve.append(capital)
            
        combined_pd["equity"] = equity_curve
        combined_pd["high_water_mark"] = combined_pd["equity"].cummax()
        combined_pd["drawdown"] = (combined_pd["equity"] / combined_pd["high_water_mark"]) - 1.0
        
        # Output total stats
        max_dd = combined_pd["drawdown"].min()
        total_ret = (combined_pd["equity"].iloc[-1] / initial_capital) - 1.0
        
        print("=== PORTFOLIO STATS ===")
        print(f"Total Trades: {len(combined_pd)}")
        print(f"Total Return: {total_ret:.2%}")
        print(f"Max Drawdown: {max_dd:.2%}")
        
        return pl.from_pandas(combined_pd)
    
