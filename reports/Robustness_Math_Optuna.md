# Robustness — Optuna 3-Regime Math Portfolio

Tested on 35 strategies with optimized TP/SL.
Realistic Vantage friction + 0.2R slippage. MC=10k.

## Classification distribution

- **FUERTE**: 25
- **ACEPTABLE**: 10
- **DEBIL**: 0
- **MUERTA**: 0

## Per-strategy results

| Symbol | Sess | Setup | Dir | TP/SL | RR | n | WR | PF | PF OOS | DegWR% | Ruin% | P5 | Decay | Label | Flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| XAGUSD | NY | OLS_SLOPE_STRONG | INVERT | 1.20/0.30 | 4.00 | 1562 | 0.608 | 4.37 | 4.61 | -4.5 | 0.0 | +2581.9 | MEJORANDO | **FUERTE** | - |
| XAGUSD | NY | GARCH_Z_FADE | NORMAL | 1.10/0.30 | 3.67 | 997 | 0.595 | 3.89 | 4.02 | -2.9 | 0.0 | +1473.4 | ESTABLE | **FUERTE** | - |
| GBPAUD | NY | OLS_SLOPE_STRONG | INVERT | 1.00/0.30 | 3.33 | 1442 | 0.610 | 3.08 | 3.34 | -5.9 | 0.0 | +1664.5 | MEJORANDO | **FUERTE** | - |
| XAGUSD | ALL_DAY | HURST_TREND_MOM | INVERT | 1.00/0.40 | 2.50 | 1653 | 0.627 | 2.98 | 2.89 | +2.0 | 0.0 | +1532.2 | ESTABLE | **FUERTE** | - |
| XAUUSD | ALL_DAY | SPECTRAL_TREND_MOM | INVERT | 1.00/0.30 | 3.33 | 473 | 0.564 | 2.95 | 2.92 | -0.3 | 0.0 | +534.8 | MEJORANDO | **FUERTE** | - |
| EURUSD | LONDON | OLS_SLOPE_STRONG | INVERT | 1.20/0.30 | 4.00 | 1562 | 0.582 | 2.94 | 2.95 | -0.2 | 0.0 | +1987.9 | ESTABLE | **FUERTE** | - |
| GBPAUD | ALL_DAY | KALMAN_INNOV_EXPAND | INVERT | 1.20/0.30 | 4.00 | 1986 | 0.531 | 2.76 | 2.86 | -2.7 | 0.1 | +2371.3 | MEJORANDO | **FUERTE** | - |
| GBPAUD | ALL_DAY | HURST_TREND_MOM | INVERT | 1.00/0.30 | 3.33 | 1720 | 0.580 | 2.73 | 2.63 | +3.2 | 0.0 | +1802.8 | ESTABLE | **FUERTE** | - |
| XAUUSD | ASIA | HURST_TREND_MOM | INVERT | 1.00/0.40 | 2.50 | 1082 | 0.614 | 2.72 | 2.59 | +4.7 | 0.0 | +913.4 | ESTABLE | **FUERTE** | - |
| XAGUSD | ALL_DAY | SPECTRAL_TREND_MOM | INVERT | 0.80/0.50 | 1.60 | 417 | 0.710 | 2.70 | 3.11 | -7.9 | 0.0 | +254.0 | MEJORANDO | **FUERTE** | - |
| XAUUSD | NY | GARCH_Z_FADE | NORMAL | 1.00/0.40 | 2.50 | 1006 | 0.603 | 2.65 | 2.78 | -3.7 | 0.0 | +829.8 | MEJORANDO | **FUERTE** | - |
| EURJPY | NY | OLS_SLOPE_STRONG | INVERT | 1.20/0.40 | 3.00 | 1504 | 0.608 | 2.51 | 2.48 | +0.2 | 0.0 | +1294.1 | MEJORANDO | **FUERTE** | - |
| EURJPY | NY | HURST_TREND_MOM | INVERT | 1.00/0.30 | 3.33 | 1259 | 0.596 | 2.44 | 2.56 | -3.6 | 0.0 | +1165.2 | MEJORANDO | **FUERTE** | - |
| GBPUSD | ASIA | OLS_SLOPE_STRONG | INVERT | 1.40/0.60 | 2.33 | 751 | 0.610 | 2.30 | 2.15 | +4.5 | 0.0 | +510.9 | ESTABLE | **FUERTE** | - |
| GBPJPY | ALL_DAY | KALMAN_INNOV_EXPAND | INVERT | 1.10/0.30 | 3.67 | 2047 | 0.525 | 2.30 | 2.21 | +4.3 | 0.4 | +1895.6 | ESTABLE | **FUERTE** | - |
| GBPJPY | ASIA | HURST_TREND_MOM | INVERT | 1.20/0.40 | 3.00 | 1157 | 0.563 | 2.26 | 2.12 | +4.7 | 0.1 | +914.9 | ESTABLE | **FUERTE** | - |
| AUDUSD | ASIA | KALMAN_INNOV_EXPAND | INVERT | 1.00/0.30 | 3.33 | 1614 | 0.575 | 2.24 | 2.35 | -3.5 | 0.2 | +1376.7 | ESTABLE | **FUERTE** | - |
| AUDUSD | LONDON | HURST_TREND_MOM | INVERT | 1.00/0.30 | 3.33 | 1134 | 0.569 | 2.22 | 2.18 | +2.1 | 0.1 | +950.9 | ESTABLE | **FUERTE** | - |
| AUDUSD | LONDON_NY | OLS_SLOPE_STRONG | INVERT | 1.20/0.40 | 3.00 | 1819 | 0.573 | 2.17 | 2.39 | -9.1 | 0.1 | +1355.9 | MEJORANDO | **FUERTE** | - |
| EURUSD | LONDON_NY | GARCH_Z_FADE | NORMAL | 1.10/0.30 | 3.67 | 1245 | 0.524 | 2.16 | 2.37 | -9.1 | 0.6 | +1077.6 | MEJORANDO | **FUERTE** | - |
| USDJPY | ALL_DAY | HURST_TREND_MOM | INVERT | 1.00/0.30 | 3.33 | 1867 | 0.588 | 2.16 | 2.09 | +2.1 | 0.4 | +1533.2 | ESTABLE | **FUERTE** | - |
| USDJPY | ALL_DAY | SPECTRAL_TREND_MOM | INVERT | 1.20/0.30 | 4.00 | 442 | 0.516 | 2.05 | 1.99 | +1.7 | 0.4 | +380.8 | ESTABLE | **FUERTE** | - |
| EURJPY | LONDON_NY | SPECTRAL_TREND_MOM | INVERT | 1.20/0.50 | 2.40 | 267 | 0.577 | 1.82 | 2.05 | -16.0 | 0.0 | +128.8 | MEJORANDO | **FUERTE** | - |
| XAUUSD | LONDON | OLS_SLOPE_STRONG | INVERT | 1.50/0.80 | 1.88 | 1276 | 0.590 | 1.81 | 1.91 | -3.5 | 0.1 | +502.4 | ESTABLE | **FUERTE** | - |
| GBPAUD | NY | GARCH_Z_FADE | NORMAL | 1.10/0.90 | 1.22 | 634 | 0.634 | 1.34 | 1.31 | +3.9 | 0.1 | +91.9 | ESTABLE | **FUERTE** | - |
| GBPUSD | ALL_DAY | HURST_TREND_MOM | INVERT | 1.20/0.30 | 4.00 | 1779 | 0.535 | 2.72 | 2.45 | +8.9 | 0.1 | +2099.7 | DEGRADANDO | **ACEPTABLE** | decay- |
| GBPJPY | ASIA | OLS_SLOPE_STRONG | INVERT | 1.30/0.30 | 4.33 | 1072 | 0.531 | 2.66 | 2.47 | +7.8 | 0.4 | +1332.7 | ESTABLE | **ACEPTABLE** | - |
| GBPUSD | ALL_DAY | SPECTRAL_TREND_MOM | INVERT | 1.10/0.30 | 3.67 | 514 | 0.547 | 2.59 | 2.15 | +15.1 | 0.0 | +547.6 | DEGRADANDO | **ACEPTABLE** | WF deg WR>15%,decay- |
| USDJPY | LONDON | OLS_SLOPE_STRONG | INVERT | 1.10/0.30 | 3.67 | 1320 | 0.578 | 2.33 | 2.01 | +13.0 | 0.4 | +1256.4 | DEGRADANDO | **ACEPTABLE** | decay- |
| EURUSD | ASIA | HURST_TREND_MOM | INVERT | 1.00/0.50 | 2.00 | 1033 | 0.665 | 2.12 | 1.99 | +6.1 | 0.0 | +565.0 | ESTABLE | **ACEPTABLE** | - |
| EURJPY | ALL_DAY | KALMAN_INNOV_EXPAND | INVERT | 1.10/0.30 | 3.67 | 1991 | 0.515 | 2.01 | 2.04 | -1.5 | 2.1 | +1564.3 | ESTABLE | **ACEPTABLE** | - |
| EURUSD | ASIA | KALMAN_INNOV_EXPAND | INVERT | 1.10/0.40 | 2.75 | 1337 | 0.583 | 1.96 | 1.85 | +6.1 | 2.2 | +838.7 | ESTABLE | **ACEPTABLE** | - |
| GBPUSD | ASIA | KALMAN_INNOV_EXPAND | INVERT | 1.10/0.40 | 2.75 | 1366 | 0.562 | 1.91 | 1.97 | -1.6 | 1.5 | +818.5 | MEJORANDO | **ACEPTABLE** | - |
| AUDUSD | LONDON_NY | GARCH_Z_FADE | NORMAL | 1.00/0.40 | 2.50 | 911 | 0.538 | 1.53 | 1.72 | -11.9 | 2.1 | +331.0 | MEJORANDO | **ACEPTABLE** | - |
| GBPJPY | NY | GARCH_Z_FADE | NORMAL | 1.20/0.50 | 2.40 | 585 | 0.506 | 1.47 | 1.83 | -20.5 | 1.5 | +182.1 | MEJORANDO | **ACEPTABLE** | - |
