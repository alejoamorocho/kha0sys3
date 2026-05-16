# MATH Purge Summary (2026-05-16)

**Window:** last 7 days  
**Deals observed:** 291  
**Strategies before:** 63  
**Strategies after:** 51  
**Removed:** 12  

## Strategy-level kills (all symbols of this strategy)

| tf | setup | session | reason |
|---|---|---|---|
| M1 | HURST_TREND_MOM | ALL_DAY | strategy: n>=10, sum net < -$1500 |
| M1 | OLS_SLOPE_STRONG | ALL_DAY | strategy: n>=10, sum net < -$1500 |
| M1 | VELOCITY_ACCEL_GO | ALL_DAY | strategy: n>=10, sum net < -$1500 |
| M1 | KALMAN_INNOV_EXPAND | NY | strategy: n>=10, sum net < -$1500 |

## Pair-level kills

| tf | setup | session | symbol | reason |
|---|---|---|---|---|
| M1 | HURST_TREND_MOM | ASIA | EURUSD+ | pair: n=2, 0% WR, net=$-1106 |
| M1 | VELOCITY_ACCEL_GO | ASIA | USDJPY+ | pair: n=2, 0% WR, net=$-1154 |
| M1 | KALMAN_INNOV_EXPAND | ASIA | USDJPY+ | pair: n=2, 0% WR, net=$-1154 |
| M1 | SPECTRAL_TREND_MOM | ALL_DAY | XAUUSD+ | pair: n=3, PF=0.00, net=$-1277 |
| M1 | OLS_SLOPE_STRONG | LONDON | GBPJPY+ | pair: n=2, 0% WR, net=$-1121 |
| M15 | OLS_SLOPE_STRONG | LONDON | EURUSD+ | pair: n=2, 0% WR, net=$-868 |
| M15 | HURST_TREND_MOM | ALL_DAY | XAGUSD | pair: n=3, PF=0.57, net=$-377 |
| M1 | SPECTRAL_TREND_MOM | ALL_DAY | GBPUSD+ | pair: n=4, PF=0.59, net=$-1179 |
| H1 | VELOCITY_ACCEL_GO | NY | GBPAUD+ | pair: n=2, 0% WR, net=$-903 |
| M1 | SPECTRAL_TREND_MOM | ALL_DAY | AUDUSD+ | pair: n=2, 0% WR, net=$-1210 |
| M1 | HURST_TREND_MOM | ASIA | GBPAUD+ | pair: n=2, 0% WR, net=$-1167 |
| M1 | HURST_TREND_MOM | NY | GBPJPY+ | pair: n=2, 0% WR, net=$-1189 |
| M15 | KALMAN_INNOV_EXPAND | LONDON | XAUUSD+ | pair: n=3, PF=0.40, net=$-510 |
| M15 | HURST_TREND_MOM | ASIA | AUDUSD+ | pair: n=2, 0% WR, net=$-975 |
| M15 | HURST_TREND_MOM | NY | UKOUSD | pair: n=2, 0% WR, net=$-990 |

## Surviving distribution (n=51)

- **By symbol:** {'XAGUSD': 8, 'XAUUSD+': 8, 'UKOUSD': 7, 'USOUSD': 7, 'GBPUSD+': 6, 'GBPJPY+': 4, 'AUDUSD+': 1, 'EURJPY+': 2, 'EURUSD+': 4, 'USDJPY+': 3, 'GBPAUD+': 1}
- **By TF:** {'H1': 12, 'M15': 24, 'H4': 8, 'M1': 7}
- **By setup:** {'KALMAN_INNOV_EXPAND': 15, 'SPECTRAL_TREND_MOM': 7, 'HURST_TREND_MOM': 14, 'VELOCITY_ACCEL_GO': 15}
- **By session:** {'NY': 18, 'ALL_DAY': 10, 'ASIA': 7, 'LONDON_NY': 12, 'LONDON': 4}

## Removed strategy IDs

- `XAGUSD_M15_HURS_ALL_DAY_INV` (pair: pair: n=3, PF=0.57, net=$-377)
- `BRENT_M15_HURS_NY_INV` (pair: pair: n=2, 0% WR, net=$-990)
- `AUDUSD_M15_HURS_ASIA_INV` (pair: pair: n=2, 0% WR, net=$-975)
- `XAUUSD_M1_SPEC_ALL_DAY_INV` (pair: pair: n=3, PF=0.00, net=$-1277)
- `GBPAUD_M1_KAL_NY_INV` (strategy: strategy: n>=10, sum net < -$1500)
- `BRENT_M1_KAL_NY_INV` (strategy: strategy: n>=10, sum net < -$1500)
- `GBPUSD_M1_KAL_NY_INV` (strategy: strategy: n>=10, sum net < -$1500)
- `GBPJPY_M1_HURS_NY_INV` (pair: pair: n=2, 0% WR, net=$-1189)
- `GBPAUD_H1_VEL_NY_INV` (pair: pair: n=2, 0% WR, net=$-903)
- `GBPJPY_M1_KAL_NY_INV` (strategy: strategy: n>=10, sum net < -$1500)
- `GBPUSD_M1_SPEC_ALL_DAY_INV` (pair: pair: n=4, PF=0.59, net=$-1179)
- `EURUSD_M1_KAL_NY_INV` (strategy: strategy: n>=10, sum net < -$1500)
