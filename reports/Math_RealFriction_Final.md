# Math Rediscovery — REALISTIC FRICTION (v2)

Friction model: `friction_real.friction_r(sym, sl, median_atr) + 0.2`
(broker spread + commission converted to R, plus +0.2R live slippage).

- Phase A passers (trades/yr>=30, WR>0.50, PF>1.0, exp>0): **1958**
- Phase B validated (WF>=0.80, MC<=0.02, decay>=0.60): **987**
- Phase C portfolio (session-disjoint, max 4/sym): **35**

Grid: TP(0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0) x SL(0.75, 1.0, 1.5, 2.0, 2.5) (max combos), families = FADE (6) + MOMENTUM (6), direction = NORMAL + INVERT,
universe = 15 symbols x 5 sessions on 3y+ M15 cache.

## Aggregate metrics — portfolio

- Strategies: **35**
- Avg WR: **0.5554**
- Avg PF: **1.520**
- Avg expectancy: **0.2878R**
- Avg max DD: **18.44R**
- Avg trades/year: **149.0**

## Top 15 validated by expectancy

| # | Sym | Session | Setup | Dir | Fam | TP | SL | Fric_R | N | WR | PF | Exp(R) | DD(R) | T/yr | WF | MC | Decay |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | XAGUSD | NY | OLS_SLOPE_STRONG | INVERT | MOM | 2.0 | 0.75 | 0.228 | 1562 | 0.539 | 2.07 | 0.565 | 13.38 | 190.2 | 1.01 | 0.000 | 1.51 |
| 2 | XAGUSD | ASIA | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.228 | 917 | 0.615 | 2.23 | 0.561 | 12.72 | 111.6 | 1.00 | 0.000 | 0.73 |
| 3 | XAGUSD | LONDON_NY | OLS_SLOPE_STRONG | INVERT | MOM | 2.0 | 0.75 | 0.228 | 1856 | 0.506 | 1.91 | 0.542 | 20.40 | 226.0 | 1.00 | 0.000 | 0.92 |
| 4 | XAGUSD | ASIA | OLS_SLOPE_STRONG | INVERT | MOM | 1.25 | 0.75 | 0.228 | 917 | 0.670 | 2.38 | 0.538 | 11.05 | 111.6 | 1.00 | 0.000 | 0.72 |
| 5 | XAGUSD | NY | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.228 | 1562 | 0.607 | 2.20 | 0.538 | 10.54 | 190.2 | 1.01 | 0.000 | 1.16 |
| 6 | XAGUSD | ALL_DAY | OLS_SLOPE_STRONG | INVERT | MOM | 1.25 | 0.75 | 0.228 | 2169 | 0.664 | 2.33 | 0.535 | 9.52 | 263.8 | 1.00 | 0.000 | 0.68 |
| 7 | XAGUSD | LONDON_NY | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.228 | 1856 | 0.594 | 2.08 | 0.526 | 15.42 | 226.0 | 1.00 | 0.000 | 0.62 |
| 8 | GBPUSD | ASIA | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.311 | 751 | 0.615 | 2.06 | 0.523 | 10.11 | 91.5 | 1.02 | 0.000 | 0.78 |
| 9 | XAGUSD | ALL_DAY | OLS_SLOPE_STRONG | INVERT | MOM | 1.0 | 0.75 | 0.228 | 2169 | 0.724 | 2.40 | 0.463 | 10.07 | 263.8 | 1.00 | 0.000 | 0.66 |
| 10 | GBPUSD | ASIA | OLS_SLOPE_STRONG | INVERT | MOM | 1.25 | 0.75 | 0.311 | 751 | 0.659 | 2.05 | 0.463 | 7.69 | 91.5 | 1.02 | 0.000 | 0.98 |
| 11 | XAGUSD | LONDON_NY | OLS_SLOPE_STRONG | INVERT | MOM | 1.25 | 0.75 | 0.228 | 1856 | 0.637 | 2.06 | 0.461 | 9.36 | 226.0 | 1.00 | 0.000 | 0.73 |
| 12 | XAGUSD | NY | OLS_SLOPE_STRONG | INVERT | MOM | 1.25 | 0.75 | 0.228 | 1562 | 0.640 | 2.12 | 0.458 | 11.65 | 190.2 | 1.01 | 0.000 | 1.26 |
| 13 | XAUUSD | LONDON | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.245 | 1276 | 0.582 | 1.87 | 0.435 | 16.46 | 155.5 | 1.00 | 0.000 | 0.88 |
| 14 | XAUUSD | NY | OLS_SLOPE_STRONG | INVERT | MOM | 2.0 | 0.75 | 0.245 | 1572 | 0.501 | 1.73 | 0.428 | 25.11 | 191.4 | 1.01 | 0.000 | 0.78 |
| 15 | XAUUSD | LONDON | OLS_SLOPE_STRONG | INVERT | MOM | 2.0 | 0.75 | 0.245 | 1276 | 0.505 | 1.72 | 0.422 | 15.43 | 155.5 | 1.00 | 0.000 | 0.97 |

## Final consolidated portfolio

| # | Sym | Session | Setup | Dir | Fam | TP | SL | Fric_R | N | WR | PF | Exp(R) | DD(R) | T/yr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | XAGUSD | NY | OLS_SLOPE_STRONG | INVERT | MOM | 2.0 | 0.75 | 0.228 | 1562 | 0.539 | 2.07 | 0.565 | 13.38 | 190.2 |
| 2 | GBPUSD | ASIA | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.311 | 751 | 0.615 | 2.06 | 0.523 | 10.11 | 91.5 |
| 3 | XAUUSD | LONDON | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.245 | 1276 | 0.582 | 1.87 | 0.435 | 16.46 | 155.5 |
| 4 | EURUSD | LONDON | OLS_SLOPE_STRONG | INVERT | MOM | 2.0 | 0.75 | 0.353 | 1562 | 0.520 | 1.68 | 0.414 | 22.39 | 190.1 |
| 5 | XAGUSD | ALL_DAY | HURST_TREND_MOM | INVERT | MOM | 1.5 | 0.75 | 0.228 | 1653 | 0.554 | 1.76 | 0.412 | 19.84 | 201.1 |
| 6 | XAGUSD | ALL_DAY | SPECTRAL_TREND_MOM | INVERT | MOM | 1.5 | 0.75 | 0.228 | 417 | 0.552 | 1.75 | 0.411 | 9.28 | 51.6 |
| 7 | XAGUSD | NY | GARCH_Z_FADE | NORMAL | FADE | 1.25 | 0.75 | 0.228 | 997 | 0.614 | 1.87 | 0.396 | 11.45 | 121.5 |
| 8 | EURJPY | NY | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.364 | 1504 | 0.594 | 1.74 | 0.378 | 15.53 | 183.0 |
| 9 | XAUUSD | ASIA | HURST_TREND_MOM | INVERT | MOM | 1.5 | 0.75 | 0.245 | 1082 | 0.552 | 1.68 | 0.365 | 13.10 | 131.6 |
| 10 | GBPAUD | NY | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.299 | 1442 | 0.570 | 1.68 | 0.360 | 18.61 | 175.7 |
| 11 | GBPJPY | ASIA | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.321 | 1072 | 0.563 | 1.62 | 0.344 | 13.85 | 130.7 |
| 12 | EURUSD | ASIA | HURST_TREND_MOM | INVERT | MOM | 1.5 | 0.75 | 0.353 | 1033 | 0.573 | 1.61 | 0.339 | 17.01 | 125.7 |
| 13 | GBPUSD | ALL_DAY | HURST_TREND_MOM | INVERT | MOM | 1.5 | 0.75 | 0.311 | 1779 | 0.551 | 1.57 | 0.333 | 17.64 | 216.4 |
| 14 | XAUUSD | ALL_DAY | SPECTRAL_TREND_MOM | INVERT | MOM | 1.5 | 0.75 | 0.245 | 473 | 0.524 | 1.54 | 0.317 | 15.75 | 57.6 |
| 15 | XAUUSD | NY | GARCH_Z_FADE | NORMAL | FADE | 1.5 | 0.75 | 0.245 | 1006 | 0.521 | 1.53 | 0.304 | 11.13 | 122.7 |
| 16 | GBPAUD | ALL_DAY | KALMAN_INNOV_EXPAND | INVERT | MOM | 1.5 | 0.75 | 0.299 | 1986 | 0.535 | 1.50 | 0.297 | 26.77 | 241.6 |
| 17 | GBPJPY | ASIA | HURST_TREND_MOM | INVERT | MOM | 1.25 | 0.75 | 0.321 | 1157 | 0.608 | 1.57 | 0.289 | 15.45 | 140.8 |
| 18 | AUDUSD | LONDON_NY | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.369 | 1819 | 0.557 | 1.49 | 0.288 | 16.40 | 221.4 |
| 19 | EURJPY | LONDON_NY | SPECTRAL_TREND_MOM | INVERT | MOM | 1.5 | 0.75 | 0.364 | 267 | 0.554 | 1.46 | 0.268 | 12.45 | 32.5 |
| 20 | GBPAUD | ALL_DAY | HURST_TREND_MOM | INVERT | MOM | 1.5 | 0.75 | 0.299 | 1720 | 0.526 | 1.43 | 0.264 | 20.25 | 209.3 |
| 21 | USDJPY | LONDON | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.406 | 1320 | 0.555 | 1.41 | 0.239 | 17.31 | 160.8 |
| 22 | AUDUSD | LONDON | HURST_TREND_MOM | INVERT | MOM | 1.5 | 0.75 | 0.369 | 1134 | 0.538 | 1.39 | 0.233 | 13.92 | 138.2 |
| 23 | GBPUSD | ALL_DAY | SPECTRAL_TREND_MOM | INVERT | MOM | 1.5 | 1.0 | 0.283 | 514 | 0.605 | 1.45 | 0.224 | 15.04 | 62.6 |
| 24 | EURUSD | ASIA | KALMAN_INNOV_EXPAND | INVERT | MOM | 1.5 | 0.75 | 0.353 | 1337 | 0.542 | 1.37 | 0.223 | 30.12 | 162.7 |
| 25 | EURJPY | NY | HURST_TREND_MOM | INVERT | MOM | 1.5 | 0.75 | 0.364 | 1259 | 0.543 | 1.38 | 0.222 | 14.01 | 153.2 |
| 26 | GBPUSD | ASIA | KALMAN_INNOV_EXPAND | INVERT | MOM | 1.5 | 0.75 | 0.311 | 1366 | 0.532 | 1.37 | 0.220 | 22.10 | 166.3 |
| 27 | USDJPY | ALL_DAY | HURST_TREND_MOM | INVERT | MOM | 1.5 | 0.75 | 0.406 | 1867 | 0.544 | 1.34 | 0.214 | 30.01 | 227.2 |
| 28 | GBPAUD | NY | GARCH_Z_FADE | NORMAL | FADE | 1.25 | 0.75 | 0.299 | 634 | 0.558 | 1.32 | 0.174 | 15.23 | 77.2 |
| 29 | AUDUSD | ASIA | KALMAN_INNOV_EXPAND | INVERT | MOM | 1.5 | 0.75 | 0.369 | 1614 | 0.514 | 1.26 | 0.167 | 39.16 | 196.4 |
| 30 | GBPJPY | ALL_DAY | KALMAN_INNOV_EXPAND | INVERT | MOM | 1.25 | 0.75 | 0.321 | 2047 | 0.560 | 1.28 | 0.162 | 20.91 | 249.0 |
| 31 | USDJPY | ALL_DAY | SPECTRAL_TREND_MOM | INVERT | MOM | 1.25 | 0.75 | 0.406 | 442 | 0.581 | 1.28 | 0.157 | 25.65 | 53.9 |
| 32 | EURJPY | ALL_DAY | KALMAN_INNOV_EXPAND | INVERT | MOM | 1.5 | 0.75 | 0.364 | 1991 | 0.507 | 1.23 | 0.154 | 20.04 | 242.2 |
| 33 | EURUSD | LONDON_NY | GARCH_Z_FADE | NORMAL | FADE | 1.25 | 0.75 | 0.353 | 1245 | 0.561 | 1.26 | 0.149 | 23.40 | 151.5 |
| 34 | AUDUSD | LONDON_NY | GARCH_Z_FADE | NORMAL | FADE | 1.25 | 0.75 | 0.369 | 911 | 0.555 | 1.21 | 0.122 | 20.21 | 110.8 |
| 35 | GBPJPY | NY | GARCH_Z_FADE | NORMAL | FADE | 1.25 | 0.75 | 0.321 | 585 | 0.537 | 1.19 | 0.108 | 21.34 | 71.2 |

## Per-symbol distribution

| Sym | N | avg WR | avg PF | avg Exp(R) |
|---|---|---|---|---|
| XAUUSD | 4 | 0.545 | 1.66 | 0.355 |
| AUDUSD | 4 | 0.541 | 1.34 | 0.203 |
| EURJPY | 4 | 0.550 | 1.45 | 0.256 |
| XAGUSD | 4 | 0.565 | 1.86 | 0.446 |
| GBPAUD | 4 | 0.547 | 1.48 | 0.274 |
| EURUSD | 4 | 0.549 | 1.48 | 0.281 |
| GBPJPY | 4 | 0.567 | 1.41 | 0.226 |
| GBPUSD | 4 | 0.576 | 1.61 | 0.325 |
| USDJPY | 3 | 0.560 | 1.34 | 0.204 |
