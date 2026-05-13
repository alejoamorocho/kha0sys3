# Live Strategy Analysis — MT5 deal history (60 days)

Pulled at 2026-05-13T15:21:27.886879+00:00
Account: login=25246666 balance=$68252.62 USD
Window: 2026-03-14T15:21:27.886879+00:00 → 2026-05-13T15:21:27.886879+00:00

## Summary
- Total closed trades: **94**
- Total wins: **28** (29.8%)
- Total net P&L: **$-22629.08**
- Open positions now: 0
- Distinct strategies that fired trades: 62
- Of those, in current K3M1-75 config: 17
- K3M1-75 strategies that have NOT fired yet: 58/75

## Por TF (signal timeframe)

| TF | n strats | n trades | wins | WR | Net USD |
|---|---|---|---|---|---|
| **M1** | 48 | 76 | 23 | 30.3% | $-19285.12 |
| **M15** | 12 | 16 | 5 | 31.2% | $-2561.75 |
| **H1** | 1 | 1 | 0 | 0.0% | $-395.01 |
| **H4** | 1 | 1 | 0 | 0.0% | $-387.20 |

## Por setup

| Setup | n strats | n trades | WR | Net USD |
|---|---|---|---|---|
| HURST | 17 | 26 | 38.5% | $-4081.62 |
| KALMAN | 16 | 23 | 47.8% | $-1641.97 |
| OLS | 11 | 20 | 15.0% | $-7770.48 |
| VELOCITY | 11 | 16 | 18.8% | $-5425.25 |
| SPECTRAL | 4 | 6 | 16.7% | $-2094.13 |
| KAMA | 3 | 3 | 0.0% | $-1615.63 |

## Per-strategy detail (ranked by trades)

| Symbol | TF | Setup | Sess | In cfg | Robust | n | WR | PF | Net USD | Expected PF OOS |
|---|---|---|---|---|---|---|---|---|---|---|
| GBPAUD+ | M1 | OLS | ALLDAY | ✓ | ACEPTABLE | 3 | 0.0% | 0.00 | $-1691.21 | 2.29 |
| EURUSD+ | M1 | HURST | ASIA | ✗ (legacy) | ? | 2 | 0.0% | 0.00 | $-1106.36 | - |
| EURAUD+ | M1 | HURST | ALLDA | ✗ (legacy) | ? | 2 | 50.0% | 0.68 | $-178.35 | - |
| GBPAUD+ | M1 | HURST | ALLDA | ✗ (legacy) | ? | 2 | 50.0% | 0.72 | $-147.55 | - |
| AUDUSD+ | M1 | HURST | ALLDA | ✗ (legacy) | ? | 2 | 0.0% | 0.00 | $-1138.95 | - |
| EURAUD+ | M1 | OLS | ALLDAY | ✗ (legacy) | ? | 2 | 50.0% | 0.49 | $-305.38 | - |
| GBPJPY+ | M1 | KALMAN | ALLD | ✗ (legacy) | ? | 2 | 50.0% | 0.75 | $-121.97 | - |
| AUDUSD+ | M1 | VELOCITY | AL | ✗ (legacy) | ? | 2 | 50.0% | 0.63 | $-209.10 | - |
| GBPUSD+ | M1 | VELOCITY | AL | ✗ (legacy) | ? | 2 | 0.0% | 0.00 | $-1216.23 | - |
| USDJPY+ | M1 | VELOCITY | AS | ✗ (legacy) | ? | 2 | 0.0% | 0.00 | $-1154.39 | - |
| USDJPY+ | M1 | KALMAN | ASIA | ✗ (legacy) | ? | 2 | 0.0% | 0.00 | $-1153.61 | - |
| USDJPY+ | M1 | HURST | ASIA | ✗ (legacy) | ? | 2 | 50.0% | 0.45 | $-353.06 | - |
| EURJPY+ | M1 | HURST | ALLDA | ✗ (legacy) | ? | 2 | 50.0% | 0.63 | $-201.37 | - |
| GBPJPY+ | M1 | VELOCITY | AL | ✗ (legacy) | ? | 2 | 50.0% | 0.92 | $-38.06 | - |
| AUDUSD+ | M1 | KALMAN | ALLD | ✗ (legacy) | ? | 2 | 100.0% | inf | $+574.60 | - |
| GBPUSD+ | M1 | KALMAN | ALLD | ✗ (legacy) | ? | 2 | 100.0% | inf | $+548.88 | - |
| EURUSD+ | M1 | OLS | ALLDAY | ✗ (legacy) | ? | 2 | 0.0% | 0.00 | $-1066.41 | - |
| EURAUD+ | M1 | KALMAN | ALLD | ✗ (legacy) | ? | 2 | 50.0% | 0.59 | $-234.61 | - |
| AUDUSD+ | M1 | OLS | ALLDAY | ✗ (legacy) | ? | 2 | 0.0% | 0.00 | $-1205.74 | - |
| GBPUSD+ | M1 | OLS | ALLDAY | ✗ (legacy) | ? | 2 | 50.0% | 0.64 | $-203.15 | - |
| SP500 | M1 | VELOCITY | AL | ✗ (legacy) | ? | 2 | 50.0% | 1.02 | $+6.87 | - |
| GBPUSD+ | M15 | OLS | LDNNY | ✓ | FUERTE | 2 | 0.0% | 0.00 | $-879.80 | 2.31 |
| EURUSD+ | M15 | OLS | LDN | ✓ | FUERTE | 2 | 0.0% | 0.00 | $-868.22 | 2.47 |
| GBPJPY+ | M1 | OLS | LDNNY | ✓ | FUERTE | 2 | 0.0% | 0.00 | $-1120.53 | 1.78 |
| XAUUSD+ | M1 | HURST | LDNNY | ✓ | ACEPTABLE | 2 | 50.0% | 2.01 | $+379.18 | 1.75 |
| USDJPY+ | M15 | KALMAN | ALL | ✗ (legacy) | ? | 2 | 50.0% | 0.85 | $-61.87 | - |
| USDJPY+ | M15 | HURST | ALLD | ✗ (legacy) | ? | 2 | 50.0% | 1.65 | $+288.68 | - |
| GBPUSD+ | M1 | SPECTRAL | AL | ✗ (legacy) | ? | 2 | 50.0% | 1.16 | $+98.94 | - |
| GBPJPY+ | M1 | KALMAN | NY | ✓ | FUERTE | 2 | 50.0% | 1.18 | $+91.98 | 1.54 |
| AUDUSD+ | M1 | SPECTRAL | AL | ✗ (legacy) | ? | 2 | 0.0% | 0.00 | $-1210.08 | - |
| GBPAUD+ | M1 | HURST | ASIA | ✓ | FUERTE | 2 | 0.0% | 0.00 | $-1166.56 | 1.80 |
| GBPUSD+ | M1 | HURST | ALLDA | ✗ (legacy) | ? | 1 | 0.0% | 0.00 | $-583.17 | - |
| XAUUSD+ | M1 | VELOCITY | AS | ✗ (legacy) | ? | 1 | 0.0% | 0.00 | $-492.96 | - |
| GBPAUD+ | M1 | KAMA | ASIA | ✗ (legacy) | ? | 1 | 0.0% | 0.00 | $-590.20 | - |
| GBPAUD+ | M1 | KALMAN | ALLD | ✗ (legacy) | ? | 1 | 0.0% | 0.00 | $-533.44 | - |
| EURUSD+ | M1 | KALMAN | ALLD | ✗ (legacy) | ? | 1 | 0.0% | 0.00 | $-658.46 | - |
| USDJPY+ | M1 | SPECTRAL | AS | ✗ (legacy) | ? | 1 | 0.0% | 0.00 | $-568.09 | - |
| GBPJPY+ | M1 | HURST | ALLDA | ✗ (legacy) | ? | 1 | 100.0% | inf | $+367.50 | - |
| XAUUSD+ | M1 | KALMAN | LDN | ✗ (legacy) | ? | 1 | 100.0% | inf | $+449.28 | - |
| USOUSD | M1 | VELOCITY | LD | ✗ (legacy) | ? | 1 | 0.0% | 0.00 | $-455.40 | - |
| GBPJPY+ | M15 | KAMA | NY | ✗ (legacy) | ? | 1 | 0.0% | 0.00 | $-463.53 | - |
| EURJPY+ | M1 | OLS | NY | ✗ (legacy) | ? | 1 | 100.0% | inf | $+332.98 | - |
| USOUSD | M1 | KALMAN | NY | ✗ (legacy) | ? | 1 | 0.0% | 0.00 | $-453.44 | - |
| AUDUSD+ | M1 | KAMA | NY | ✗ (legacy) | ? | 1 | 0.0% | 0.00 | $-561.90 | - |
| GBPAUD+ | M1 | VELOCITY | AL | ✗ (legacy) | ? | 1 | 0.0% | 0.00 | $-540.44 | - |
| EURAUD+ | M1 | VELOCITY | AL | ✗ (legacy) | ? | 1 | 0.0% | 0.00 | $-543.33 | - |
| XAUUSD+ | M1 | SPECTRAL | AL | ✗ (legacy) | ? | 1 | 0.0% | 0.00 | $-414.90 | - |
| GBPJPY+ | M15 | HURST | LDNN | ✗ (legacy) | ? | 1 | 100.0% | inf | $+346.26 | - |
| XAGUSD | M15 | HURST | ALLD | ✗ (legacy) | ? | 1 | 0.0% | 0.00 | $-376.25 | - |
| USOUSD | M15 | KALMAN | ALL | ✗ (legacy) | ? | 1 | 0.0% | 0.00 | $-384.03 | - |
| USOUSD | M1 | HURST | LDNNY | ✓ | ACEPTABLE | 1 | 0.0% | 0.00 | $-383.46 | 1.69 |
| GBPUSD+ | H4 | VELOCITY | LD | ✗ (legacy) | ? | 1 | 0.0% | 0.00 | $-387.20 | - |
| USOUSD | M15 | OLS | NY | ✓ | FUERTE | 1 | 0.0% | 0.00 | $-380.88 | 4.64 |
| UKOUSD | M15 | OLS | NY | ✓ | FUERTE | 1 | 0.0% | 0.00 | $-382.14 | 4.54 |
| GBPAUD+ | H1 | VELOCITY | NY | ✓ | FUERTE | 1 | 0.0% | 0.00 | $-395.01 | 1.57 |
| GBPUSD+ | M1 | KALMAN | NY | ✓ | FUERTE | 1 | 100.0% | inf | $+606.08 | 1.67 |
| EURUSD+ | M1 | KALMAN | NY | ✓ | ACEPTABLE | 1 | 100.0% | inf | $+529.34 | 1.45 |
| XAGUSD | M1 | KALMAN | ASIA | ✓ | FUERTE | 1 | 0.0% | 0.00 | $-371.00 | 1.87 |
| GBPUSD+ | M15 | HURST | ASIA | ✓ | FUERTE | 1 | 100.0% | inf | $+320.88 | 3.66 |
| EURJPY+ | M15 | HURST | LDNN | ✗ (legacy) | ? | 1 | 100.0% | inf | $+279.15 | - |
| GBPAUD+ | M1 | KALMAN | NY | ✓ | FUERTE | 1 | 0.0% | 0.00 | $-469.70 | 1.79 |
| GBPJPY+ | M1 | HURST | NY | ✓ | FUERTE | 1 | 0.0% | 0.00 | $-428.19 | 1.67 |

## K3M1-75 strategies WITHOUT live activity (cold)

These haven't fired since deploy — either session not active yet, or signal condition hasn't met.

| ID | Symbol | TF | Setup | Sess | Robust | Expected tpy |
|---|---|---|---|---|---|---|
| AUDUSD_M15_KAL_LONDON_INV | AUDUSD+ | M15 | KALMAN_INNOV_EXPAND | LONDON | FUERTE | 181 |
| AUDUSD_M15_HURS_ASIA_INV | AUDUSD+ | M15 | HURST_TREND_MOM | ASIA | FUERTE | 156 |
| AUDUSD_M1_SPEC_ALL_DAY_INV | AUDUSD+ | M1 | SPECTRAL_TREND_MOM | ALL_DAY | ACEPTABLE | 229 |
| EURJPY_M15_KAL_ASIA_INV | EURJPY+ | M15 | KALMAN_INNOV_EXPAND | ASIA | FUERTE | 188 |
| EURJPY_M15_HURS_LONDON_NY_INV | EURJPY+ | M15 | HURST_TREND_MOM | LONDON_NY | FUERTE | 180 |
| EURUSD_M15_KAL_NY_INV | EURUSD+ | M15 | KALMAN_INNOV_EXPAND | NY | FUERTE | 200 |
| EURUSD_M15_HURS_ASIA_INV | EURUSD+ | M15 | HURST_TREND_MOM | ASIA | FUERTE | 124 |
| EURUSD_M15_SPEC_ALL_DAY_INV | EURUSD+ | M15 | SPECTRAL_TREND_MOM | ALL_DAY | ACEPTABLE | 55 |
| EURUSD_H4_VEL_LONDON_NY_INV | EURUSD+ | H4 | VELOCITY_ACCEL_GO | LONDON_NY | ACEPTABLE | 72 |
| GBPAUD_H4_VEL_LONDON_INV | GBPAUD+ | H4 | VELOCITY_ACCEL_GO | LONDON | ACEPTABLE | 32 |
| GBPJPY_M15_OLS_LONDON_INV | GBPJPY+ | M15 | OLS_SLOPE_STRONG | LONDON | FUERTE | 191 |
| GBPJPY_M15_KAL_NY_INV | GBPJPY+ | M15 | KALMAN_INNOV_EXPAND | NY | FUERTE | 189 |
| GBPJPY_M15_HURS_LONDON_NY_INV | GBPJPY+ | M15 | HURST_TREND_MOM | LONDON_NY | FUERTE | 186 |
| GBPJPY_H4_VEL_LONDON_INV | GBPJPY+ | H4 | VELOCITY_ACCEL_GO | LONDON | ACEPTABLE | 33 |
| GBPJPY_H1_VEL_NY_INV | GBPJPY+ | H1 | VELOCITY_ACCEL_GO | NY | ACEPTABLE | 110 |
| GBPUSD_M15_KAL_ASIA_INV | GBPUSD+ | M15 | KALMAN_INNOV_EXPAND | ASIA | FUERTE | 163 |
| GBPUSD_M15_SPEC_ALL_DAY_INV | GBPUSD+ | M15 | SPECTRAL_TREND_MOM | ALL_DAY | FUERTE | 62 |
| GBPUSD_H4_VEL_LONDON_NY_INV | GBPUSD+ | H4 | VELOCITY_ACCEL_GO | LONDON_NY | FUERTE | 71 |
| GBPUSD_M1_HURS_NY_INV | GBPUSD+ | M1 | HURST_TREND_MOM | NY | FUERTE | 228 |
| GBPUSD_M1_SPEC_ALL_DAY_INV | GBPUSD+ | M1 | SPECTRAL_TREND_MOM | ALL_DAY | ACEPTABLE | 232 |
| GBPUSD_H1_VEL_NY_INV | GBPUSD+ | H1 | VELOCITY_ACCEL_GO | NY | ACEPTABLE | 118 |
| BRENT_H1_HURS_NY_INV | UKOUSD | H1 | HURST_TREND_MOM | NY | FUERTE | 69 |
| BRENT_M15_KAL_ALL_DAY_INV | UKOUSD | M15 | KALMAN_INNOV_EXPAND | ALL_DAY | FUERTE | 227 |
| BRENT_H1_KAL_NY_INV | UKOUSD | H1 | KALMAN_INNOV_EXPAND | NY | FUERTE | 113 |
| BRENT_M15_HURS_NY_INV | UKOUSD | M15 | HURST_TREND_MOM | NY | FUERTE | 149 |
| BRENT_M1_SPEC_ALL_DAY_INV | UKOUSD | M1 | SPECTRAL_TREND_MOM | ALL_DAY | FUERTE | 208 |
| BRENT_M1_HURS_NY_INV | UKOUSD | M1 | HURST_TREND_MOM | NY | FUERTE | 226 |
| BRENT_H1_VEL_NY_INV | UKOUSD | H1 | VELOCITY_ACCEL_GO | NY | FUERTE | 97 |
| BRENT_M1_KAL_NY_INV | UKOUSD | M1 | KALMAN_INNOV_EXPAND | NY | FUERTE | 218 |
| BRENT_H4_VEL_NY_INV | UKOUSD | H4 | VELOCITY_ACCEL_GO | NY | ACEPTABLE | 61 |
| USDJPY_M15_KAL_ALL_DAY_INV | USDJPY+ | M15 | KALMAN_INNOV_EXPAND | ALL_DAY | FUERTE | 244 |
| USDJPY_M15_SPEC_ALL_DAY_INV | USDJPY+ | M15 | SPECTRAL_TREND_MOM | ALL_DAY | FUERTE | 53 |
| USDJPY_M15_HURS_ALL_DAY_INV | USDJPY+ | M15 | HURST_TREND_MOM | ALL_DAY | FUERTE | 224 |
| USDJPY_M15_OLS_LONDON_NY_INV | USDJPY+ | M15 | OLS_SLOPE_STRONG | LONDON_NY | ACEPTABLE | 220 |
| WTI_M15_KAL_ALL_DAY_INV | USOUSD | M15 | KALMAN_INNOV_EXPAND | ALL_DAY | FUERTE | 238 |
| WTI_H1_KAL_NY_INV | USOUSD | H1 | KALMAN_INNOV_EXPAND | NY | FUERTE | 119 |
| WTI_M15_HURS_LONDON_NY_INV | USOUSD | M15 | HURST_TREND_MOM | LONDON_NY | FUERTE | 192 |
| WTI_M15_SPEC_LONDON_NY_INV | USOUSD | M15 | SPECTRAL_TREND_MOM | LONDON_NY | FUERTE | 56 |
| WTI_H4_VEL_NY_INV | USOUSD | H4 | VELOCITY_ACCEL_GO | NY | FUERTE | 60 |
| WTI_H1_VEL_LONDON_NY_INV | USOUSD | H1 | VELOCITY_ACCEL_GO | LONDON_NY | ACEPTABLE | 120 |
| XAGUSD_H1_OLS_ASIA_INV | XAGUSD | H1 | OLS_SLOPE_STRONG | ASIA | FUERTE | 88 |
| XAGUSD_M15_HURS_ALL_DAY_INV | XAGUSD | M15 | HURST_TREND_MOM | ALL_DAY | FUERTE | 198 |
| XAGUSD_H1_KAL_NY_INV | XAGUSD | H1 | KALMAN_INNOV_EXPAND | NY | FUERTE | 111 |
| XAGUSD_M15_SPEC_ALL_DAY_INV | XAGUSD | M15 | SPECTRAL_TREND_MOM | ALL_DAY | FUERTE | 51 |
| XAGUSD_M15_KAL_ASIA_INV | XAGUSD | M15 | KALMAN_INNOV_EXPAND | ASIA | FUERTE | 169 |
| XAGUSD_M1_HURS_ASIA_INV | XAGUSD | M1 | HURST_TREND_MOM | ASIA | FUERTE | 222 |
| XAGUSD_H4_VEL_NY_INV | XAGUSD | H4 | VELOCITY_ACCEL_GO | NY | FUERTE | 61 |
| XAGUSD_M15_VEL_LONDON_INV | XAGUSD | M15 | VELOCITY_ACCEL_GO | LONDON | FUERTE | 188 |
| XAGUSD_H1_VEL_NY_INV | XAGUSD | H1 | VELOCITY_ACCEL_GO | NY | ACEPTABLE | 99 |
| XAUUSD_M15_OLS_NY_INV | XAUUSD+ | M15 | OLS_SLOPE_STRONG | NY | FUERTE | 188 |
| XAUUSD_M15_KAL_LONDON_NY_INV | XAUUSD+ | M15 | KALMAN_INNOV_EXPAND | LONDON_NY | FUERTE | 215 |
| XAUUSD_M15_HURS_LONDON_NY_INV | XAUUSD+ | M15 | HURST_TREND_MOM | LONDON_NY | FUERTE | 180 |
| XAUUSD_H1_HURS_NY_INV | XAUUSD+ | H1 | HURST_TREND_MOM | NY | FUERTE | 76 |
| XAUUSD_H1_KAL_NY_INV | XAUUSD+ | H1 | KALMAN_INNOV_EXPAND | NY | FUERTE | 109 |
| XAUUSD_M15_SPEC_ALL_DAY_INV | XAUUSD+ | M15 | SPECTRAL_TREND_MOM | ALL_DAY | FUERTE | 57 |
| XAUUSD_H4_VEL_LONDON_NY_INV | XAUUSD+ | H4 | VELOCITY_ACCEL_GO | LONDON_NY | FUERTE | 73 |
| XAUUSD_M1_SPEC_ALL_DAY_INV | XAUUSD+ | M1 | SPECTRAL_TREND_MOM | ALL_DAY | FUERTE | 230 |
| XAUUSD_H1_VEL_NY_INV | XAUUSD+ | H1 | VELOCITY_ACCEL_GO | NY | FUERTE | 101 |