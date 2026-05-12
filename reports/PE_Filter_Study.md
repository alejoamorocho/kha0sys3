# PE Filter Study

Gate the 35 math strategies on permutation-entropy at entry (`pe_at_entry <= gate`).

## Aggregate

- Strategies tested: **35**
- Strategies improved (PF lift > 0): **20** (57%)
- Avg PF lift (best per strategy): **+0.017**
- Avg retention (best gate):       **99%**

Score = PF_filtered * sqrt(retention) (penalizes retention loss).

## Best filter per strategy

| Symbol | Session | Setup | Dir | m | W | Gate | Base PF -> Filt PF | dPF | Retention | Filt n | Filt WR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| XAGUSD | NY | GARCH_Z_FADE | NORMAL | 4 | 50 | 0.958 | 3.89 -> 4.13 | +0.24 | 90% | 900 | 0.610 |
| XAGUSD | ALL_DAY | SPECTRAL_TREND_MOM | INVERT | 5 | 50 | 0.800 | 2.70 -> 2.75 | +0.05 | 100% | 415 | 0.713 |
| GBPUSD | ALL_DAY | SPECTRAL_TREND_MOM | INVERT | 5 | 50 | 0.800 | 2.59 -> 2.62 | +0.03 | 99% | 511 | 0.550 |
| GBPAUD | ALL_DAY | HURST_TREND_MOM | INVERT | 5 | 50 | 0.800 | 2.73 -> 2.76 | +0.03 | 99% | 1708 | 0.583 |
| XAGUSD | NY | OLS_SLOPE_STRONG | INVERT | 5 | 50 | 0.800 | 4.37 -> 4.40 | +0.03 | 99% | 1553 | 0.609 |
| XAUUSD | ALL_DAY | SPECTRAL_TREND_MOM | INVERT | 5 | 50 | 0.800 | 2.95 -> 2.98 | +0.03 | 100% | 471 | 0.567 |
| USDJPY | ALL_DAY | HURST_TREND_MOM | INVERT | 5 | 200 | 0.950 | 2.16 -> 2.18 | +0.03 | 99% | 1846 | 0.590 |
| AUDUSD | LONDON | HURST_TREND_MOM | INVERT | 5 | 200 | 0.950 | 2.22 -> 2.24 | +0.02 | 99% | 1121 | 0.571 |
| USDJPY | ALL_DAY | SPECTRAL_TREND_MOM | INVERT | 5 | 50 | 0.800 | 2.05 -> 2.07 | +0.02 | 100% | 440 | 0.518 |
| EURUSD | LONDON | OLS_SLOPE_STRONG | INVERT | 5 | 200 | 0.950 | 2.94 -> 2.96 | +0.02 | 99% | 1544 | 0.584 |
| EURJPY | LONDON_NY | SPECTRAL_TREND_MOM | INVERT | 5 | 100 | 0.950 | 1.82 -> 1.84 | +0.02 | 100% | 266 | 0.579 |
| GBPUSD | ASIA | OLS_SLOPE_STRONG | INVERT | 5 | 200 | 0.950 | 2.30 -> 2.31 | +0.02 | 99% | 744 | 0.612 |
| AUDUSD | LONDON_NY | OLS_SLOPE_STRONG | INVERT | 5 | 100 | 0.900 | 2.17 -> 2.18 | +0.01 | 99% | 1808 | 0.575 |
| GBPAUD | NY | GARCH_Z_FADE | NORMAL | 5 | 100 | 0.900 | 1.34 -> 1.35 | +0.01 | 100% | 632 | 0.636 |
| AUDUSD | LONDON_NY | GARCH_Z_FADE | NORMAL | 5 | 50 | 0.800 | 1.53 -> 1.54 | +0.01 | 100% | 908 | 0.540 |
| AUDUSD | ASIA | KALMAN_INNOV_EXPAND | INVERT | 5 | 50 | 0.800 | 2.24 -> 2.25 | +0.01 | 99% | 1601 | 0.576 |
| EURUSD | LONDON_NY | GARCH_Z_FADE | NORMAL | 5 | 50 | 0.800 | 2.16 -> 2.17 | +0.01 | 100% | 1239 | 0.525 |
| GBPUSD | ASIA | KALMAN_INNOV_EXPAND | INVERT | 5 | 100 | 0.900 | 1.91 -> 1.92 | +0.01 | 100% | 1362 | 0.563 |
| GBPJPY | NY | GARCH_Z_FADE | NORMAL | 5 | 100 | 0.900 | 1.47 -> 1.48 | +0.01 | 100% | 584 | 0.507 |
| USDJPY | LONDON | OLS_SLOPE_STRONG | INVERT | 5 | 100 | 0.900 | 2.33 -> 2.33 | +0.00 | 100% | 1319 | 0.578 |
| XAUUSD | LONDON | OLS_SLOPE_STRONG | INVERT | 5 | 50 | 0.900 | 1.81 -> 1.81 | +0.00 | 100% | 1276 | 0.590 |
| XAGUSD | ALL_DAY | HURST_TREND_MOM | INVERT | 3 | 200 | nan | 2.98 -> 2.98 | +0.00 | 100% | 1653 | 0.627 |
| EURJPY | NY | OLS_SLOPE_STRONG | INVERT | 3 | 200 | nan | 2.51 -> 2.51 | +0.00 | 100% | 1504 | 0.608 |
| XAUUSD | ASIA | HURST_TREND_MOM | INVERT | 3 | 100 | nan | 2.72 -> 2.72 | +0.00 | 100% | 1082 | 0.614 |
| GBPAUD | NY | OLS_SLOPE_STRONG | INVERT | 3 | 200 | nan | 3.08 -> 3.08 | +0.00 | 100% | 1442 | 0.610 |
| GBPJPY | ASIA | OLS_SLOPE_STRONG | INVERT | 5 | 50 | 0.900 | 2.66 -> 2.66 | +0.00 | 100% | 1072 | 0.531 |
| EURUSD | ASIA | HURST_TREND_MOM | INVERT | 3 | 200 | nan | 2.12 -> 2.12 | +0.00 | 100% | 1033 | 0.665 |
| GBPUSD | ALL_DAY | HURST_TREND_MOM | INVERT | 3 | 100 | nan | 2.72 -> 2.72 | +0.00 | 100% | 1779 | 0.535 |
| XAUUSD | NY | GARCH_Z_FADE | NORMAL | 5 | 50 | 0.900 | 2.65 -> 2.65 | +0.00 | 100% | 1006 | 0.603 |
| GBPAUD | ALL_DAY | KALMAN_INNOV_EXPAND | INVERT | 3 | 100 | nan | 2.76 -> 2.76 | +0.00 | 100% | 1986 | 0.531 |
| GBPJPY | ASIA | HURST_TREND_MOM | INVERT | 3 | 200 | nan | 2.26 -> 2.26 | +0.00 | 100% | 1157 | 0.563 |
| EURUSD | ASIA | KALMAN_INNOV_EXPAND | INVERT | 3 | 200 | nan | 1.96 -> 1.96 | +0.00 | 100% | 1337 | 0.583 |
| EURJPY | NY | HURST_TREND_MOM | INVERT | 3 | 100 | nan | 2.44 -> 2.44 | +0.00 | 100% | 1259 | 0.596 |
| GBPJPY | ALL_DAY | KALMAN_INNOV_EXPAND | INVERT | 3 | 50 | nan | 2.30 -> 2.30 | +0.00 | 100% | 2047 | 0.525 |
| EURJPY | ALL_DAY | KALMAN_INNOV_EXPAND | INVERT | 3 | 50 | nan | 2.01 -> 2.01 | +0.00 | 100% | 1991 | 0.515 |

## (m, W) selection histogram

| m | W | n_strategies |
|---|---|---|
| 5 | 50 | 12 |
| 3 | 200 | 6 |
| 5 | 100 | 6 |
| 3 | 100 | 4 |
| 5 | 200 | 4 |
| 3 | 50 | 2 |
| 4 | 50 | 1 |
