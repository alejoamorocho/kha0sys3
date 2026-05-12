# Wavelet Filter Study (db4 SWT)

- Source: `reports/optuna_3regime_results.parquet` (35 strategies)
- Wavelet: causal Stationary WT, db4, levels 1..4
- Trend reconstruction: approx_4 + detail_4
- Noise reconstruction: detail_1 + detail_2
- Sign smoothing: EMA window 50 on first-difference of trend/noise
- Friction: realistic Vantage table + 0.2R slippage

## Filter variants

- **AGREE** — keep trade where `trend_sign` agrees with trade direction.
- **DOUBLE** — AGREE plus `noise_sign` also aligned with trade direction.

## Aggregate

| Metric | Original | AGREE | DOUBLE |
|---|---|---|---|
| Avg PF | 2.424 | 2.505 | 2.514 |
| Avg trades kept | 100% | 49.8% | 24.0% |
| Sum Net R | 38660.7 | 19727.1 | 9399.0 |
| #strats with PF lift | — | 26/35 | 20/35 |

## Per-strategy detail

| Symbol | Sess | Setup | Dir | TP/SL | n_orig | PF_orig | PF_agree (kept%) | PF_double (kept%) | NetR_orig | NetR_agree | NetR_double |
|---|---|---|---|---|---|---|---|---|---|---|---|
| XAGUSD | NY | OLS_SLOPE_STRONG | INVERT | 1.20/0.30 | 1562 | 4.37 | 4.98 (51%) | 5.49 (24%) | +2581.9 | +1433.0 | +707.9 |
| GBPUSD | ALL_DAY | SPECTRAL_TREND_MOM | INVERT | 1.10/0.30 | 514 | 2.59 | 2.97 (51%) | 3.25 (30%) | +547.6 | +321.0 | +203.2 |
| XAGUSD | ALL_DAY | SPECTRAL_TREND_MOM | INVERT | 0.80/0.50 | 417 | 2.70 | 3.08 (50%) | 3.06 (30%) | +254.0 | +142.6 | +84.6 |
| EURUSD | ASIA | HURST_TREND_MOM | INVERT | 1.00/0.50 | 1033 | 2.12 | 2.47 (49%) | 2.14 (27%) | +565.0 | +325.0 | +158.7 |
| USDJPY | ALL_DAY | SPECTRAL_TREND_MOM | INVERT | 1.20/0.30 | 442 | 2.05 | 2.30 (49%) | 1.87 (29%) | +380.8 | +217.9 | +96.7 |
| EURJPY | NY | HURST_TREND_MOM | INVERT | 1.00/0.30 | 1259 | 2.44 | 2.65 (48%) | 2.36 (27%) | +1165.2 | +613.2 | +297.2 |
| XAUUSD | ASIA | HURST_TREND_MOM | INVERT | 1.00/0.40 | 1082 | 2.72 | 2.91 (45%) | 2.55 (25%) | +913.4 | +443.0 | +213.3 |
| GBPJPY | NY | GARCH_Z_FADE | NORMAL | 1.20/0.50 | 585 | 1.47 | 1.65 (53%) | 2.10 (19%) | +182.1 | +124.3 | +64.0 |
| XAGUSD | ALL_DAY | HURST_TREND_MOM | INVERT | 1.00/0.40 | 1653 | 2.98 | 3.12 (50%) | 3.07 (27%) | +1532.2 | +794.1 | +430.6 |
| GBPUSD | ASIA | KALMAN_INNOV_EXPAND | INVERT | 1.10/0.40 | 1366 | 1.91 | 2.05 (49%) | 2.11 (20%) | +818.5 | +448.5 | +193.8 |
| EURJPY | LONDON_NY | SPECTRAL_TREND_MOM | INVERT | 1.20/0.50 | 267 | 1.82 | 1.94 (50%) | 2.00 (30%) | +128.8 | +71.5 | +44.7 |
| AUDUSD | ASIA | KALMAN_INNOV_EXPAND | INVERT | 1.00/0.30 | 1614 | 2.24 | 2.36 (49%) | 2.30 (22%) | +1376.7 | +723.4 | +314.5 |
| GBPUSD | ALL_DAY | HURST_TREND_MOM | INVERT | 1.20/0.30 | 1779 | 2.72 | 2.84 (50%) | 2.63 (26%) | +2099.7 | +1093.0 | +522.6 |
| GBPJPY | ALL_DAY | KALMAN_INNOV_EXPAND | INVERT | 1.10/0.30 | 2047 | 2.30 | 2.40 (51%) | 2.61 (21%) | +1895.6 | +1033.7 | +468.1 |
| XAUUSD | NY | GARCH_Z_FADE | NORMAL | 1.00/0.40 | 1006 | 2.65 | 2.75 (54%) | 2.94 (17%) | +829.8 | +461.7 | +152.0 |
| GBPUSD | ASIA | OLS_SLOPE_STRONG | INVERT | 1.40/0.60 | 751 | 2.30 | 2.39 (50%) | 2.08 (25%) | +510.9 | +263.5 | +116.0 |
| GBPJPY | ASIA | OLS_SLOPE_STRONG | INVERT | 1.30/0.30 | 1072 | 2.66 | 2.74 (51%) | 2.99 (27%) | +1332.7 | +688.1 | +411.0 |
| XAGUSD | NY | GARCH_Z_FADE | NORMAL | 1.10/0.30 | 997 | 3.89 | 3.95 (52%) | 4.65 (17%) | +1473.4 | +773.5 | +274.2 |
| AUDUSD | LONDON | HURST_TREND_MOM | INVERT | 1.00/0.30 | 1134 | 2.22 | 2.27 (46%) | 2.21 (24%) | +950.9 | +451.5 | +229.4 |
| GBPAUD | NY | GARCH_Z_FADE | NORMAL | 1.10/0.90 | 634 | 1.34 | 1.38 (46%) | 1.25 (20%) | +91.9 | +47.1 | +14.3 |
| XAUUSD | LONDON | OLS_SLOPE_STRONG | INVERT | 1.50/0.80 | 1276 | 1.81 | 1.84 (50%) | 2.10 (24%) | +502.4 | +263.1 | +154.8 |
| GBPAUD | ALL_DAY | KALMAN_INNOV_EXPAND | INVERT | 1.20/0.30 | 1986 | 2.76 | 2.78 (50%) | 2.63 (23%) | +2371.3 | +1183.2 | +517.8 |
| AUDUSD | LONDON_NY | OLS_SLOPE_STRONG | INVERT | 1.20/0.40 | 1819 | 2.17 | 2.18 (50%) | 2.28 (24%) | +1355.9 | +685.5 | +345.7 |
| EURJPY | ALL_DAY | KALMAN_INNOV_EXPAND | INVERT | 1.10/0.30 | 1991 | 2.01 | 2.02 (50%) | 2.04 (23%) | +1564.3 | +790.2 | +364.5 |
| AUDUSD | LONDON_NY | GARCH_Z_FADE | NORMAL | 1.00/0.40 | 911 | 1.53 | 1.53 (51%) | 1.64 (18%) | +331.0 | +170.0 | +70.2 |
| EURUSD | LONDON | OLS_SLOPE_STRONG | INVERT | 1.20/0.30 | 1562 | 2.94 | 2.94 (51%) | 3.22 (25%) | +1987.9 | +1000.2 | +533.9 |
| EURUSD | ASIA | KALMAN_INNOV_EXPAND | INVERT | 1.10/0.40 | 1337 | 1.96 | 1.96 (51%) | 1.76 (19%) | +838.7 | +426.2 | +135.2 |
| EURUSD | LONDON_NY | GARCH_Z_FADE | NORMAL | 1.10/0.30 | 1245 | 2.16 | 2.14 (51%) | 2.03 (17%) | +1077.6 | +536.3 | +165.6 |
| GBPJPY | ASIA | HURST_TREND_MOM | INVERT | 1.20/0.40 | 1157 | 2.26 | 2.22 (50%) | 2.46 (27%) | +914.9 | +440.8 | +271.3 |
| EURJPY | NY | OLS_SLOPE_STRONG | INVERT | 1.20/0.40 | 1504 | 2.51 | 2.44 (50%) | 2.59 (25%) | +1294.1 | +633.8 | +341.7 |
| USDJPY | ALL_DAY | HURST_TREND_MOM | INVERT | 1.00/0.30 | 1867 | 2.16 | 2.08 (47%) | 1.80 (26%) | +1533.2 | +682.4 | +302.8 |
| USDJPY | LONDON | OLS_SLOPE_STRONG | INVERT | 1.10/0.30 | 1320 | 2.33 | 2.23 (50%) | 1.96 (23%) | +1256.4 | +602.8 | +236.0 |
| GBPAUD | ALL_DAY | HURST_TREND_MOM | INVERT | 1.00/0.30 | 1720 | 2.73 | 2.60 (49%) | 2.64 (27%) | +1802.8 | +837.5 | +479.4 |
| XAUUSD | ALL_DAY | SPECTRAL_TREND_MOM | INVERT | 1.00/0.30 | 473 | 2.95 | 2.69 (49%) | 2.51 (28%) | +534.8 | +240.6 | +125.0 |
| GBPAUD | NY | OLS_SLOPE_STRONG | INVERT | 1.00/0.30 | 1442 | 3.08 | 2.82 (50%) | 2.68 (24%) | +1664.5 | +765.1 | +358.2 |
