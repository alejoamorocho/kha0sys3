# Math-Invert Portfolio (diversified)

- Strategies: **17**
- Avg WR: 0.815
- Avg PF: 1.669
- Avg expectancy: 0.120R
- Expected trades/year (sum): 2682
- Expected annual R (sum): 328.6

## Rules applied
- Session-overlap elimination per (symbol, setup)
- Max 3 setups per symbol
- Max 40% share per setup family

## Portfolio

| # | Symbol | Session | Setup | TP | SL | WR | PF | Exp(R) | Trades/yr | WF | MC | Decay |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | XAGUSD | ALL_DAY | OLS_SLOPE_STRONG | 0.75 | 1.5 | 0.850 | 2.15 | 0.182 | 264 | 1.00 | 0.000 | 0.70 |
| 2 | GBPUSD | ASIA | OLS_SLOPE_STRONG | 0.75 | 1.5 | 0.819 | 2.03 | 0.181 | 91 | 1.00 | 0.000 | 0.76 |
| 3 | VIX | LONDON | KALMAN_INNOV_EXPAND | 1.0 | 1.5 | 0.801 | 1.98 | 0.174 | 90 | 1.00 | 0.000 | 0.85 |
| 4 | EURJPY | ASIA | OLS_SLOPE_STRONG | 0.75 | 1.5 | 0.824 | 1.90 | 0.159 | 142 | 1.00 | 0.000 | 0.80 |
| 5 | EURUSD | ASIA | OLS_SLOPE_STRONG | 0.75 | 1.5 | 0.818 | 1.83 | 0.153 | 93 | 1.01 | 0.000 | 1.02 |
| 6 | EURUSD | NY | OLS_SLOPE_STRONG | 0.75 | 1.5 | 0.820 | 1.82 | 0.146 | 209 | 1.00 | 0.000 | 1.30 |
| 7 | EURJPY | NY | OLS_SLOPE_STRONG | 0.75 | 1.5 | 0.821 | 1.82 | 0.146 | 183 | 1.01 | 0.000 | 1.66 |
| 8 | XAUUSD | LONDON | OLS_SLOPE_STRONG | 0.75 | 1.5 | 0.806 | 1.76 | 0.141 | 156 | 1.00 | 0.000 | 0.99 |
| 9 | AUDUSD | ALL_DAY | OLS_SLOPE_STRONG | 0.75 | 1.5 | 0.823 | 1.74 | 0.141 | 268 | 1.00 | 0.000 | 0.80 |
| 10 | GBPAUD | ASIA | OLS_SLOPE_STRONG | 0.75 | 1.5 | 0.803 | 1.75 | 0.138 | 149 | 1.00 | 0.000 | 1.06 |
| 11 | GBPAUD | NY | OLS_SLOPE_STRONG | 0.75 | 1.5 | 0.804 | 1.66 | 0.126 | 176 | 1.01 | 0.000 | 0.87 |
| 12 | USDJPY | ALL_DAY | HURST_TREND_MOM | 0.75 | 1.5 | 0.805 | 1.54 | 0.113 | 227 | 1.00 | 0.000 | 0.78 |
| 13 | VIX | ASIA | KALMAN_INNOV_EXPAND | 0.75 | 1.5 | 0.802 | 1.44 | 0.069 | 57 | 1.01 | 0.000 | 1.13 |
| 14 | XAUUSD | ASIA | HURST_TREND_MOM | 0.5 | 1.5 | 0.847 | 1.37 | 0.056 | 132 | 1.00 | 0.000 | 0.73 |
| 15 | WTI | ASIA | HURST_TREND_MOM | 0.75 | 1.5 | 0.800 | 1.27 | 0.053 | 85 | 1.01 | 0.000 | 1.41 |
| 16 | NASDAQ100 | LONDON | HURST_TREND_MOM | 0.75 | 1.5 | 0.807 | 1.21 | 0.043 | 135 | 1.01 | 0.000 | 2.69 |
| 17 | SP500 | ALL_DAY | HURST_TREND_MOM | 0.75 | 1.5 | 0.802 | 1.10 | 0.021 | 226 | 1.00 | 0.001 | 0.69 |
