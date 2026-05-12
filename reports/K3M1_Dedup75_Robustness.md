# K3+M1mgmt 75-strategy Robustness (FINAL)

Strategies: 75. All M1 management with realistic Vantage friction.
Backtest: 2018-01 → 2026-05 (~8.3 years). MC=10k bootstrap, WF 50/50, decay yearly.

## Classification distribution

| Label | Count |
|---|---|
| **FUERTE** | 59 |
| **ACEPTABLE** | 16 |
| **DEBIL** | 0 |
| **MUERTA** | 0 |

## Aggregate (FUERTE + ACEPTABLE)

- Avg WR: 74.8%
- Avg PF (IS): 2.86
- Avg PF (OOS): 2.88
- Avg MC ruin: 0.09%
- Sum Net R 8y: 42858
- Sum trades/year: 11928

## Per-strategy (sorted by label then by PF OOS)

| TF | Symbol | Setup | Sess | Dir | TP/SL | n | WR | PF IS | PF OOS | DegWR% | Ruin% | Decay | Label | Flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| H1 | XAGUSD | OLS_SLOPE_STRONG | ASIA | INVERT | 0.5/0.5 | 725 | 89.9% | 5.45 | 6.54 | -3.5 | 0.0 | MEJORANDO | **FUERTE** | - |
| M15 | XAGUSD | HURST_TREND_MOM | ALL_DAY | INVERT | 0.5/0.5 | 1629 | 89.7% | 5.34 | 6.40 | -3.5 | 0.0 | MEJORANDO | **FUERTE** | - |
| H1 | XAGUSD | KALMAN_INNOV_EXPAND | NY | INVERT | 0.5/0.5 | 914 | 89.9% | 5.45 | 5.73 | -1.0 | 0.0 | ESTABLE | **FUERTE** | - |
| M15 | XAUUSD | OLS_SLOPE_STRONG | NY | INVERT | 0.5/0.5 | 1545 | 88.9% | 4.65 | 5.38 | -3.1 | 0.0 | MEJORANDO | **FUERTE** | - |
| M15 | XAGUSD | SPECTRAL_TREND_MOM | ALL_DAY | INVERT | 0.5/0.5 | 411 | 88.1% | 4.51 | 5.38 | -4.0 | 0.0 | MEJORANDO | **FUERTE** | - |
| M15 | XAGUSD | KALMAN_INNOV_EXPAND | ASIA | INVERT | 0.5/0.5 | 1390 | 89.1% | 5.01 | 5.36 | -1.5 | 0.0 | ESTABLE | **FUERTE** | - |
| M15 | XAUUSD | KALMAN_INNOV_EXPAND | LONDON_NY | INVERT | 0.5/0.5 | 1770 | 90.0% | 5.20 | 5.17 | +0.1 | 0.0 | ESTABLE | **FUERTE** | - |
| H1 | BRENT | HURST_TREND_MOM | NY | INVERT | 0.5/0.5 | 565 | 88.8% | 4.37 | 5.00 | -2.9 | 0.0 | ESTABLE | **FUERTE** | - |
| M15 | WTI | OLS_SLOPE_STRONG | NY | INVERT | 0.5/0.5 | 1736 | 89.4% | 4.58 | 4.64 | -0.3 | 0.0 | ESTABLE | **FUERTE** | - |
| M15 | WTI | KALMAN_INNOV_EXPAND | ALL_DAY | INVERT | 0.5/0.5 | 1957 | 89.6% | 4.67 | 4.57 | +0.4 | 0.0 | ESTABLE | **FUERTE** | - |
| M15 | BRENT | OLS_SLOPE_STRONG | NY | INVERT | 0.5/0.5 | 1614 | 89.9% | 4.88 | 4.54 | +1.5 | 0.0 | ESTABLE | **FUERTE** | - |
| M15 | BRENT | KALMAN_INNOV_EXPAND | ALL_DAY | INVERT | 0.5/0.5 | 1869 | 89.9% | 4.87 | 4.53 | +1.5 | 0.0 | ESTABLE | **FUERTE** | - |
| M15 | XAUUSD | HURST_TREND_MOM | LONDON_NY | INVERT | 0.5/0.5 | 1484 | 89.9% | 5.14 | 4.47 | +3.0 | 0.0 | ESTABLE | **FUERTE** | - |
| H1 | WTI | KALMAN_INNOV_EXPAND | NY | INVERT | 0.5/0.5 | 978 | 87.6% | 3.85 | 4.47 | -3.6 | 0.0 | ESTABLE | **FUERTE** | - |
| H1 | BRENT | KALMAN_INNOV_EXPAND | NY | INVERT | 0.5/0.5 | 929 | 87.7% | 3.92 | 4.45 | -3.0 | 0.0 | ESTABLE | **FUERTE** | - |
| M15 | BRENT | HURST_TREND_MOM | NY | INVERT | 0.5/0.5 | 1226 | 89.7% | 4.79 | 4.40 | +1.8 | 0.0 | ESTABLE | **FUERTE** | - |
| M15 | GBPUSD | KALMAN_INNOV_EXPAND | ASIA | INVERT | 0.5/0.5 | 1341 | 89.2% | 3.82 | 4.39 | -2.9 | 0.0 | MEJORANDO | **FUERTE** | - |
| M15 | GBPJPY | OLS_SLOPE_STRONG | LONDON | INVERT | 0.5/0.5 | 1568 | 89.9% | 3.97 | 4.36 | -1.9 | 0.0 | ESTABLE | **FUERTE** | - |
| H1 | XAUUSD | HURST_TREND_MOM | NY | INVERT | 0.5/0.5 | 623 | 89.1% | 4.79 | 4.30 | +2.1 | 0.0 | ESTABLE | **FUERTE** | - |
| M15 | WTI | HURST_TREND_MOM | LONDON_NY | INVERT | 0.5/0.5 | 1576 | 88.4% | 4.13 | 4.26 | -0.7 | 0.0 | MEJORANDO | **FUERTE** | - |
| H1 | XAUUSD | KALMAN_INNOV_EXPAND | NY | INVERT | 0.5/0.5 | 897 | 88.1% | 4.27 | 4.23 | +0.2 | 0.0 | ESTABLE | **FUERTE** | - |
| M15 | GBPJPY | KALMAN_INNOV_EXPAND | NY | INVERT | 0.5/0.5 | 1554 | 90.0% | 4.02 | 3.70 | +1.7 | 0.0 | ESTABLE | **FUERTE** | - |
| M15 | GBPUSD | HURST_TREND_MOM | ASIA | INVERT | 0.5/0.5 | 1001 | 89.2% | 3.86 | 3.66 | +1.3 | 0.0 | ESTABLE | **FUERTE** | - |
| M15 | AUDUSD | KALMAN_INNOV_EXPAND | LONDON | INVERT | 0.5/0.5 | 1487 | 89.9% | 3.35 | 3.57 | -1.2 | 0.0 | ESTABLE | **FUERTE** | - |
| M15 | XAUUSD | SPECTRAL_TREND_MOM | ALL_DAY | INVERT | 0.5/0.5 | 466 | 87.1% | 3.91 | 3.27 | +4.8 | 0.0 | ESTABLE | **FUERTE** | - |
| M15 | EURJPY | KALMAN_INNOV_EXPAND | ASIA | INVERT | 0.5/0.5 | 1541 | 88.9% | 3.07 | 3.26 | -1.3 | 0.0 | ESTABLE | **FUERTE** | - |
| M15 | GBPUSD | SPECTRAL_TREND_MOM | ALL_DAY | INVERT | 0.5/0.5 | 507 | 87.0% | 3.10 | 3.10 | -0.1 | 0.0 | ESTABLE | **FUERTE** | - |
| M15 | EURJPY | HURST_TREND_MOM | LONDON_NY | INVERT | 0.5/0.5 | 1477 | 88.7% | 3.01 | 2.99 | +0.1 | 0.0 | ESTABLE | **FUERTE** | - |
| M15 | GBPJPY | HURST_TREND_MOM | LONDON_NY | INVERT | 0.5/0.5 | 1531 | 87.4% | 3.11 | 2.95 | +1.3 | 0.0 | ESTABLE | **FUERTE** | - |
| M15 | AUDUSD | HURST_TREND_MOM | ASIA | INVERT | 0.5/0.5 | 1285 | 89.5% | 3.20 | 2.94 | +1.9 | 0.0 | ESTABLE | **FUERTE** | - |
| M15 | EURUSD | KALMAN_INNOV_EXPAND | NY | INVERT | 0.5/0.5 | 1642 | 87.6% | 2.82 | 2.67 | +1.4 | 0.0 | ESTABLE | **FUERTE** | - |
| M15 | EURUSD | OLS_SLOPE_STRONG | LONDON | INVERT | 1.0/0.5 | 1537 | 69.1% | 2.46 | 2.47 | -0.2 | 0.0 | MEJORANDO | **FUERTE** | - |
| M15 | USDJPY | KALMAN_INNOV_EXPAND | ALL_DAY | INVERT | 0.5/0.5 | 2004 | 88.5% | 2.49 | 2.43 | +0.6 | 0.0 | ESTABLE | **FUERTE** | - |
| M15 | EURUSD | HURST_TREND_MOM | ASIA | INVERT | 1.0/0.5 | 1015 | 69.2% | 2.46 | 2.34 | +3.0 | 0.0 | ESTABLE | **FUERTE** | - |
| M15 | WTI | SPECTRAL_TREND_MOM | LONDON_NY | INVERT | 1.0/0.5 | 458 | 63.8% | 2.31 | 2.31 | +0.0 | 0.0 | MEJORANDO | **FUERTE** | - |
| M15 | GBPUSD | OLS_SLOPE_STRONG | LONDON_NY | INVERT | 1.0/0.5 | 2009 | 66.5% | 2.37 | 2.31 | +1.7 | 0.0 | ESTABLE | **FUERTE** | - |
| H4 | XAUUSD | VELOCITY_ACCEL_GO | LONDON_NY | INVERT | 0.5/0.5 | 595 | 79.3% | 2.34 | 2.30 | -1.4 | 0.0 | ESTABLE | **FUERTE** | - |
| M15 | USDJPY | SPECTRAL_TREND_MOM | ALL_DAY | INVERT | 0.5/0.5 | 432 | 88.2% | 2.43 | 2.18 | +2.6 | 0.0 | ESTABLE | **FUERTE** | - |
| M1 | XAGUSD | HURST_TREND_MOM | ASIA | INVERT | 1.0/0.5 | 1850 | 57.7% | 1.93 | 2.02 | -3.4 | 0.0 | ESTABLE | **FUERTE** | - |
| H4 | GBPUSD | VELOCITY_ACCEL_GO | LONDON_NY | INVERT | 0.5/0.5 | 579 | 78.6% | 1.89 | 1.87 | -0.1 | 0.0 | MEJORANDO | **FUERTE** | - |
| M1 | XAGUSD | KALMAN_INNOV_EXPAND | ASIA | INVERT | 1.0/0.5 | 1746 | 55.9% | 1.79 | 1.87 | -3.8 | 0.1 | ESTABLE | **FUERTE** | - |
| M1 | BRENT | SPECTRAL_TREND_MOM | ALL_DAY | INVERT | 1.0/0.5 | 1732 | 58.8% | 1.90 | 1.85 | +1.8 | 0.1 | ESTABLE | **FUERTE** | - |
| M1 | BRENT | HURST_TREND_MOM | NY | INVERT | 1.0/0.5 | 1884 | 57.4% | 1.78 | 1.85 | -3.2 | 0.1 | MEJORANDO | **FUERTE** | - |
| M1 | GBPUSD | HURST_TREND_MOM | NY | INVERT | 1.0/0.5 | 1900 | 59.0% | 1.72 | 1.82 | -4.6 | 0.1 | ESTABLE | **FUERTE** | - |
| M1 | GBPAUD | HURST_TREND_MOM | ASIA | INVERT | 1.0/0.5 | 1898 | 59.3% | 1.78 | 1.80 | -0.5 | 0.1 | ESTABLE | **FUERTE** | - |
| M1 | XAUUSD | SPECTRAL_TREND_MOM | ALL_DAY | INVERT | 1.0/0.5 | 1919 | 55.9% | 1.73 | 1.79 | -2.7 | 0.2 | ESTABLE | **FUERTE** | - |
| M1 | GBPAUD | KALMAN_INNOV_EXPAND | NY | INVERT | 1.0/0.5 | 1796 | 58.5% | 1.73 | 1.79 | -2.9 | 0.2 | ESTABLE | **FUERTE** | - |
| H4 | XAGUSD | VELOCITY_ACCEL_GO | NY | INVERT | 1.0/0.5 | 497 | 56.9% | 1.83 | 1.78 | +3.9 | 0.0 | ESTABLE | **FUERTE** | - |
| M1 | GBPJPY | OLS_SLOPE_STRONG | LONDON_NY | INVERT | 1.0/0.5 | 2137 | 59.2% | 1.70 | 1.78 | -3.8 | 0.3 | ESTABLE | **FUERTE** | - |
| H4 | WTI | VELOCITY_ACCEL_GO | NY | INVERT | 1.0/0.5 | 493 | 59.0% | 1.89 | 1.78 | +3.8 | 0.0 | ESTABLE | **FUERTE** | - |
| M15 | USDJPY | HURST_TREND_MOM | ALL_DAY | INVERT | 1.0/0.5 | 1838 | 64.3% | 1.77 | 1.76 | +0.7 | 0.1 | ESTABLE | **FUERTE** | - |
| M15 | XAGUSD | VELOCITY_ACCEL_GO | LONDON | INVERT | 0.5/0.5 | 1541 | 75.5% | 1.88 | 1.73 | +4.0 | 0.0 | ESTABLE | **FUERTE** | - |
| H1 | BRENT | VELOCITY_ACCEL_GO | NY | INVERT | 1.0/0.5 | 793 | 55.9% | 1.66 | 1.70 | -3.0 | 0.1 | ESTABLE | **FUERTE** | - |
| H1 | XAUUSD | VELOCITY_ACCEL_GO | NY | INVERT | 1.0/0.5 | 829 | 56.0% | 1.73 | 1.68 | +1.9 | 0.1 | ESTABLE | **FUERTE** | - |
| M1 | BRENT | KALMAN_INNOV_EXPAND | NY | INVERT | 1.0/0.5 | 1820 | 55.5% | 1.65 | 1.68 | -1.6 | 0.3 | ESTABLE | **FUERTE** | - |
| M1 | GBPUSD | KALMAN_INNOV_EXPAND | NY | INVERT | 1.0/0.5 | 1856 | 58.5% | 1.68 | 1.67 | +0.6 | 0.3 | ESTABLE | **FUERTE** | - |
| M1 | GBPJPY | HURST_TREND_MOM | NY | INVERT | 1.0/0.5 | 1868 | 58.2% | 1.63 | 1.67 | -1.7 | 0.5 | MEJORANDO | **FUERTE** | - |
| H1 | GBPAUD | VELOCITY_ACCEL_GO | NY | INVERT | 0.5/0.5 | 866 | 77.8% | 1.70 | 1.57 | +3.5 | 0.0 | ESTABLE | **FUERTE** | - |
| M1 | GBPJPY | KALMAN_INNOV_EXPAND | NY | INVERT | 1.0/0.5 | 1805 | 57.7% | 1.60 | 1.54 | +3.3 | 0.7 | ESTABLE | **FUERTE** | - |
| M1 | GBPAUD | OLS_SLOPE_STRONG | ALL_DAY | INVERT | 1.5/0.5 | 2585 | 55.6% | 2.42 | 2.29 | +5.5 | 0.0 | ESTABLE | **ACEPTABLE** | - |
| M15 | EURUSD | SPECTRAL_TREND_MOM | ALL_DAY | INVERT | 1.0/0.5 | 452 | 68.1% | 2.33 | 2.22 | +2.6 | 0.0 | DEGRADANDO | **ACEPTABLE** | decay- |
| H4 | GBPJPY | VELOCITY_ACCEL_GO | LONDON | INVERT | 1.0/0.5 | 272 | 59.9% | 1.76 | 2.03 | -11.7 | 0.0 | MEJORANDO | **ACEPTABLE** | - |
| M15 | USDJPY | OLS_SLOPE_STRONG | LONDON_NY | INVERT | 1.0/0.5 | 1807 | 66.5% | 1.97 | 1.87 | +3.4 | 0.0 | DEGRADANDO | **ACEPTABLE** | decay- |
| H4 | BRENT | VELOCITY_ACCEL_GO | NY | INVERT | 1.0/0.5 | 496 | 56.0% | 1.69 | 1.83 | -10.6 | 0.0 | MEJORANDO | **ACEPTABLE** | - |
| M1 | XAUUSD | HURST_TREND_MOM | LONDON_NY | INVERT | 1.0/0.5 | 1869 | 58.7% | 1.94 | 1.75 | +8.3 | 0.0 | ESTABLE | **ACEPTABLE** | - |
| H1 | XAGUSD | VELOCITY_ACCEL_GO | NY | INVERT | 1.0/0.5 | 814 | 57.2% | 1.86 | 1.74 | +5.0 | 0.0 | DEGRADANDO | **ACEPTABLE** | decay- |
| M1 | GBPUSD | SPECTRAL_TREND_MOM | ALL_DAY | INVERT | 1.0/0.5 | 1934 | 56.9% | 1.58 | 1.70 | -7.0 | 0.9 | MEJORANDO | **ACEPTABLE** | - |
| M1 | WTI | HURST_TREND_MOM | LONDON_NY | INVERT | 1.0/0.5 | 1875 | 58.4% | 1.85 | 1.69 | +7.0 | 0.1 | DEGRADANDO | **ACEPTABLE** | decay- |
| H4 | GBPAUD | VELOCITY_ACCEL_GO | LONDON | INVERT | 0.5/0.5 | 260 | 78.1% | 1.72 | 1.68 | +1.0 | 0.0 | DEGRADANDO | **ACEPTABLE** | decay- |
| H1 | WTI | VELOCITY_ACCEL_GO | LONDON_NY | INVERT | 0.5/0.5 | 982 | 77.4% | 1.86 | 1.62 | +6.1 | 0.0 | ESTABLE | **ACEPTABLE** | - |
| H4 | EURUSD | VELOCITY_ACCEL_GO | LONDON_NY | INVERT | 0.5/0.5 | 584 | 80.1% | 1.82 | 1.59 | +5.8 | 0.0 | ESTABLE | **ACEPTABLE** | - |
| H1 | GBPJPY | VELOCITY_ACCEL_GO | NY | INVERT | 0.5/0.5 | 904 | 79.8% | 1.77 | 1.52 | +6.2 | 0.0 | DEGRADANDO | **ACEPTABLE** | decay- |
| M1 | AUDUSD | SPECTRAL_TREND_MOM | ALL_DAY | INVERT | 1.0/0.5 | 1908 | 58.9% | 1.52 | 1.52 | +0.2 | 1.9 | ESTABLE | **ACEPTABLE** | - |
| H1 | GBPUSD | VELOCITY_ACCEL_GO | NY | INVERT | 0.5/0.5 | 970 | 78.1% | 1.66 | 1.46 | +5.6 | 0.0 | DEGRADANDO | **ACEPTABLE** | decay- |
| M1 | EURUSD | KALMAN_INNOV_EXPAND | NY | INVERT | 1.0/0.5 | 1850 | 59.3% | 1.60 | 1.45 | +7.9 | 0.6 | DEGRADANDO | **ACEPTABLE** | decay- |