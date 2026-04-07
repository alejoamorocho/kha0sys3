import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt

from src.engine.backtester import BacktestPipeline
from src.engine.portfolio import PortfolioEvaluator

def run_portfolio():
    data_dir = "c:/Proyectos/kha0sys3/data"
    config_path = "c:/Proyectos/kha0sys3/src/infrastructure/config/asset_config.json"
    
    pb = BacktestPipeline(data_dir, config_path)
    evaluator = PortfolioEvaluator()
    
    symbols = list(pb.config.keys())
    results = []
    
    for sym in symbols:
        try:
            res = pb.run_asset(sym)
            results.append(res)
        except Exception as e:
            print(f"Skipping {sym} due to error/missing data: {e}")
            
    print("\n--- Aggregating Portfolio ---")
    portfolio_df = evaluator.evaluate(results, initial_capital=100000, risk_per_trade=0.005) # 0.5% risk
    
    # Plotting
    pdf = portfolio_df.to_pandas()
    
    plt.figure(figsize=(10, 6))
    plt.plot(pdf["trade_date"], pdf["equity"], label="Portfolio Equity", color="blue", linewidth=1.5)
    plt.title("ORB Strategy - Global Portfolio Equity Curve (0.5% Risk/Trade)")
    plt.xlabel("Date")
    plt.ylabel("Capital ($)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("c:/Proyectos/kha0sys3/portfolio_curve.png")
    print("Saved portfolio equity curve to c:/Proyectos/kha0sys3/portfolio_curve.png")

if __name__ == "__main__":
    run_portfolio()
