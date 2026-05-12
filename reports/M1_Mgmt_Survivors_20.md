# 20 Survivors — M1 Management Realistic Backtest

Filtered from 110 FUERTE non-FADE strategies with M1-mgmt SL-first:
- PF M1 >= 2.0
- WR M1 >= 55%
- Net R M1 > 0

Aggregate: Avg WR 59.0%, Avg PF 3.03, Sum Net R 8y = 10434 R

| # | TF | Symbol | Session | Setup | Dir | TP/SL | RR | WR orig | WR M1 | PF orig | PF M1 | DD M1 | Net R M1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | H4 | GBPJPY | LONDON_NY | HURST_TREND_MOM | INVERT | 3.90/0.30 | 13.00 | 69.8% | 63.2% | 4.21 | 4.56 | 6.8 | 372 |
| 2 | H1 | AUDUSD | NY | OLS_SLOPE_STRONG | INVERT | 3.00/0.30 | 10.00 | 53.6% | 57.6% | 3.10 | 4.49 | 13.5 | 1197 |
| 3 | H1 | EURJPY | NY | OLS_SLOPE_STRONG | INVERT | 3.90/0.30 | 13.00 | 51.2% | 56.9% | 2.70 | 4.04 | 15.0 | 1080 |
| 4 | H4 | USDJPY | LONDON_NY | OLS_SLOPE_STRONG | INVERT | 3.80/0.30 | 12.67 | 64.7% | 62.1% | 3.70 | 3.97 | 7.6 | 502 |
| 5 | H4 | XAGUSD | LONDON_NY | OLS_SLOPE_STRONG | INVERT | 3.60/0.60 | 6.00 | 68.7% | 64.7% | 3.83 | 3.96 | 4.9 | 302 |
| 6 | H4 | GBPAUD | LONDON_NY | OLS_SLOPE_STRONG | INVERT | 2.70/0.40 | 6.75 | 69.0% | 60.6% | 4.29 | 3.61 | 8.6 | 359 |
| 7 | H4 | GBPJPY | LONDON_NY | OLS_SLOPE_STRONG | INVERT | 3.90/0.40 | 9.75 | 67.8% | 61.7% | 3.81 | 3.56 | 5.3 | 333 |
| 8 | H4 | AUDUSD | LONDON_NY | HURST_TREND_MOM | INVERT | 3.80/0.40 | 9.50 | 62.1% | 63.0% | 2.48 | 3.27 | 8.1 | 222 |
| 9 | H1 | XAUUSD | ALL_DAY | HURST_TREND_MOM | INVERT | 1.00/0.30 | 3.33 | 61.2% | 55.1% | 3.37 | 2.81 | 9.2 | 1024 |
| 10 | H1 | GBPJPY | NY | OLS_SLOPE_STRONG | INVERT | 1.30/0.30 | 4.33 | 59.9% | 55.8% | 3.03 | 2.81 | 12.0 | 610 |
| 11 | H1 | XAGUSD | NY | HURST_TREND_MOM | INVERT | 2.00/0.50 | 4.00 | 58.4% | 58.0% | 2.40 | 2.81 | 15.7 | 348 |
| 12 | H4 | EURJPY | LONDON_NY | HURST_TREND_MOM | INVERT | 3.50/0.40 | 8.75 | 68.3% | 61.7% | 3.08 | 2.78 | 6.8 | 176 |
| 13 | H4 | XAGUSD | ALL_DAY | KALMAN_INNOV_EXPAND | INVERT | 1.00/0.40 | 2.50 | 65.9% | 60.1% | 3.08 | 2.52 | 10.0 | 461 |
| 14 | H1 | EURUSD | ALL_DAY | OLS_SLOPE_STRONG | INVERT | 1.30/0.40 | 3.25 | 61.0% | 56.5% | 2.66 | 2.33 | 12.6 | 1123 |
| 15 | H1 | XAUUSD | NY | HURST_TREND_MOM | INVERT | 1.50/0.50 | 3.00 | 55.9% | 56.5% | 1.99 | 2.22 | 9.6 | 292 |
| 16 | H1 | GBPUSD | NY | KALMAN_INNOV_EXPAND | INVERT | 1.00/0.30 | 3.33 | 58.6% | 56.0% | 2.36 | 2.19 | 13.4 | 650 |
| 17 | H4 | GBPJPY | LONDON_NY | KALMAN_INNOV_EXPAND | INVERT | 3.70/0.60 | 6.17 | 66.5% | 58.7% | 2.37 | 2.19 | 8.0 | 110 |
| 18 | H1 | XAUUSD | ALL_DAY | OLS_SLOPE_STRONG | INVERT | 1.00/0.40 | 2.50 | 65.4% | 56.0% | 3.05 | 2.16 | 9.3 | 795 |
| 19 | H4 | EURJPY | LONDON_NY | KALMAN_INNOV_EXPAND | INVERT | 3.60/0.60 | 6.00 | 68.7% | 59.7% | 2.67 | 2.13 | 6.2 | 95 |
| 20 | H1 | EURJPY | NY | HURST_TREND_MOM | INVERT | 1.00/0.30 | 3.33 | 57.6% | 57.1% | 2.07 | 2.10 | 18.4 | 383 |