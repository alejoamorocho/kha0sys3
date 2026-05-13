# Live Strategy Classification — K3M1-75 (5 days, May 9-13 2026)

Account demo $100,000 → $68,253 (-31.7% in 5 days)
Total trades: 94 (66 K3-97 era + 28 K3M1-75 era)
Bot stopped May 13 to prevent further bleed.

## Classification rules
- **WINNER** : n ≥ 2 trades AND wr_live ≥ 60% AND net > 0
- **NEUTRAL**: n ≥ 2 AND 40% ≤ wr_live ≤ 60%
- **LOSER**  : n ≥ 2 AND (wr_live < 40% OR net < 0)
- **TOO_FEW**: n = 1 (cannot conclude — keep ON)

## Summary

- **WINNER**: 0
- **NEUTRAL**: 5
- **LOSER**: 6
- **TOO_FEW**: 16
- **Cold (never fired)**: 48/75

## WINNERS — KEEP ON

| ID | TF | Setup | Sess | n | WR | PF live | Net USD | WR expected | PF OOS exp |
|---|---|---|---|---|---|---|---|---|---|

## NEUTRALS — OBSERVE

| ID | TF | Setup | Sess | n | WR | PF live | Net USD | WR expected | PF OOS exp |
|---|---|---|---|---|---|---|---|---|---|
| XAUUSD_M1_HURS_LONDON_NY_INV | M1 | HURST_TREND_MOM | LONDON_NY | 2 | 50% | 2.01 | $+379 | 59% | 1.75 |
| USDJPY_M15_HURS_ALL_DAY_INV | M15 | HURST_TREND_MOM | ALL_DAY | 2 | 50% | 1.65 | $+289 | 64% | 1.76 |
| GBPUSD_M1_SPEC_ALL_DAY_INV | M1 | SPECTRAL_TREND_MOM | ALL_DAY | 2 | 50% | 1.16 | $+99 | 57% | 1.70 |
| GBPJPY_M1_KAL_NY_INV | M1 | KALMAN_INNOV_EXPAND | NY | 2 | 50% | 1.18 | $+92 | 58% | 1.54 |
| USDJPY_M15_KAL_ALL_DAY_INV | M15 | KALMAN_INNOV_EXPAND | ALL_DAY | 2 | 50% | 0.85 | $-62 | 88% | 2.43 |

## LOSERS — DISABLE

| ID | TF | Setup | Sess | n | WR | Net USD | WR expected | PF OOS exp |
|---|---|---|---|---|---|---|---|---|
| GBPAUD_M1_OLS_ALL_DAY_INV | M1 | OLS_SLOPE_STRONG | ALL_DAY | 3 | 0% | $-1691 | 56% | 2.29 |
| AUDUSD_M1_SPEC_ALL_DAY_INV | M1 | SPECTRAL_TREND_MOM | ALL_DAY | 2 | 0% | $-1210 | 59% | 1.52 |
| GBPAUD_M1_HURS_ASIA_INV | M1 | HURST_TREND_MOM | ASIA | 2 | 0% | $-1167 | 59% | 1.80 |
| GBPJPY_M1_OLS_LONDON_NY_INV | M1 | OLS_SLOPE_STRONG | LONDON_NY | 2 | 0% | $-1121 | 59% | 1.78 |
| GBPUSD_M15_OLS_LONDON_NY_INV | M15 | OLS_SLOPE_STRONG | LONDON_NY | 2 | 0% | $-880 | 66% | 2.31 |
| EURUSD_M15_OLS_LONDON_INV | M15 | OLS_SLOPE_STRONG | LONDON | 2 | 0% | $-868 | 69% | 2.47 |

## TOO_FEW (1 trade — keep ON for more data)

| ID | TF | Setup | Sess | n | WR | Net USD |
|---|---|---|---|---|---|---|
| GBPAUD_M1_KAL_NY_INV | M1 | KALMAN_INNOV_EXPAND | NY | 1 | 0% | $-470 |
| GBPJPY_M1_HURS_NY_INV | M1 | HURST_TREND_MOM | NY | 1 | 0% | $-428 |
| XAUUSD_M1_SPEC_ALL_DAY_INV | M1 | SPECTRAL_TREND_MOM | ALL_DAY | 1 | 0% | $-415 |
| GBPAUD_H1_VEL_NY_INV | H1 | VELOCITY_ACCEL_GO | NY | 1 | 0% | $-395 |
| GBPUSD_H4_VEL_LONDON_NY_INV | H4 | VELOCITY_ACCEL_GO | LONDON_NY | 1 | 0% | $-387 |
| WTI_M15_KAL_ALL_DAY_INV | M15 | KALMAN_INNOV_EXPAND | ALL_DAY | 1 | 0% | $-384 |
| WTI_M1_HURS_LONDON_NY_INV | M1 | HURST_TREND_MOM | LONDON_NY | 1 | 0% | $-383 |
| BRENT_M15_OLS_NY_INV | M15 | OLS_SLOPE_STRONG | NY | 1 | 0% | $-382 |
| WTI_M15_OLS_NY_INV | M15 | OLS_SLOPE_STRONG | NY | 1 | 0% | $-381 |
| XAGUSD_M15_HURS_ALL_DAY_INV | M15 | HURST_TREND_MOM | ALL_DAY | 1 | 0% | $-376 |
| XAGUSD_M1_KAL_ASIA_INV | M1 | KALMAN_INNOV_EXPAND | ASIA | 1 | 0% | $-371 |
| EURJPY_M15_HURS_LONDON_NY_INV | M15 | HURST_TREND_MOM | LONDON_NY | 1 | 100% | $+279 |
| GBPUSD_M15_HURS_ASIA_INV | M15 | HURST_TREND_MOM | ASIA | 1 | 100% | $+321 |
| GBPJPY_M15_HURS_LONDON_NY_INV | M15 | HURST_TREND_MOM | LONDON_NY | 1 | 100% | $+346 |
| EURUSD_M1_KAL_NY_INV | M1 | KALMAN_INNOV_EXPAND | NY | 1 | 100% | $+529 |
| GBPUSD_M1_KAL_NY_INV | M1 | KALMAN_INNOV_EXPAND | NY | 1 | 100% | $+606 |

## By TF

| TF | strats | trades | wins | WR | Net USD |
|---|---|---|---|---|---|
| **M1** | 14 | 22 | 5 | 23% | $-5550 |
| **M15** | 11 | 15 | 5 | 33% | $-2098 |
| **H4** | 1 | 1 | 0 | 0% | $-387 |
| **H1** | 1 | 1 | 0 | 0% | $-395 |

## Strategies that have NOT fired yet (cold)

48 strategies remain untested. Don't disable — let them run when bot resumes to gather data.