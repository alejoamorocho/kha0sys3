# MATH Discovery Phase E — exits alternativos (con D combined)

- Phase C best strategies: 8
- New variants tested: 6 (trailing ATR x2, SMA cross x2, time fixed x2)
- Phase E runs: 48
- Combined runs (D + E): 72

## Best variant per strategy (across all D + E variants)

| sym | tf | setup | session | inv | best | tp | sl | n | wr | pf | exp_R | dd_R | calmar |
|-----|-----|-------|---------|-----|------|----|----|----|------|------|-------|------|--------|
| USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | False | V6_time_fixed_60 | 0.75 | 0.55 | 118 | 0.508 | 1.581 | 0.335 | 7.9 | 0.042 |
| EURUSD | H1 | KAMA_CROSS_MOM | NY | True | V3_opposite_with_tpsl | 1.75 | 1.05 | 67 | 0.522 | 1.432 | 0.154 | 4.9 | 0.031 |
| NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | False | V4_trailing_1.5_atr | 1.50 | 0.80 | 36 | 0.528 | 1.233 | 0.127 | 4.5 | 0.028 |
| USDJPY | M15 | KAMA_CROSS_MOM | ASIA | False | V6_time_fixed_60 | 1.50 | 0.80 | 134 | 0.507 | 1.243 | 0.134 | 7.5 | 0.018 |
| USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | False | V2_opposite_only | 0.50 | 0.55 | 214 | 0.444 | 1.323 | 0.413 | 42.7 | 0.010 |
| EURUSD | M15 | KAMA_CROSS_MOM | NY | False | V6_time_fixed_240 | 1.25 | 0.80 | 183 | 0.519 | 1.115 | 0.068 | 9.3 | 0.007 |
| XAUUSD | M15 | SPECTRAL_TREND_MOM | NY | False | V5_sma20_cross | 0.75 | 0.55 | 203 | 0.473 | 1.049 | 0.025 | 18.3 | 0.001 |
| XAUUSD | M15 | VELOCITY_ACCEL_GO | NY | False | V6_time_fixed_240 | 0.75 | 0.55 | 1551 | 0.502 | 1.000 | 0.000 | 62.5 | 0.000 |

## All Phase E runs

| variant | sym | tf | setup | session | n | wr | pf | exp_R | calmar |
|---------|-----|----|-------|---------|---|----|----|-------|--------|
| V4_trailing_1.0_atr | EURUSD | H1 | KAMA_CROSS_MOM | NY | 67 | 0.388 | 1.003 | 0.001 | 0.000 |
| V4_trailing_1.5_atr | EURUSD | H1 | KAMA_CROSS_MOM | NY | 67 | 0.463 | 1.199 | 0.076 | 0.011 |
| V5_sma20_cross | EURUSD | H1 | KAMA_CROSS_MOM | NY | 67 | 0.194 | 0.293 | -0.249 | -0.014 |
| V5_sma50_cross | EURUSD | H1 | KAMA_CROSS_MOM | NY | 67 | 0.179 | 0.331 | -0.227 | -0.013 |
| V6_time_fixed_240 | EURUSD | H1 | KAMA_CROSS_MOM | NY | 67 | 0.522 | 1.432 | 0.154 | 0.028 |
| V6_time_fixed_60 | EURUSD | H1 | KAMA_CROSS_MOM | NY | 67 | 0.448 | 0.877 | -0.045 | -0.006 |
| V4_trailing_1.0_atr | EURUSD | M15 | KAMA_CROSS_MOM | NY | 183 | 0.393 | 0.951 | -0.026 | -0.001 |
| V4_trailing_1.5_atr | EURUSD | M15 | KAMA_CROSS_MOM | NY | 183 | 0.497 | 1.095 | 0.055 | 0.004 |
| V5_sma20_cross | EURUSD | M15 | KAMA_CROSS_MOM | NY | 183 | 0.410 | 0.940 | -0.031 | -0.001 |
| V5_sma50_cross | EURUSD | M15 | KAMA_CROSS_MOM | NY | 183 | 0.492 | 1.091 | 0.052 | 0.004 |
| V6_time_fixed_240 | EURUSD | M15 | KAMA_CROSS_MOM | NY | 183 | 0.519 | 1.115 | 0.068 | 0.007 |
| V6_time_fixed_60 | EURUSD | M15 | KAMA_CROSS_MOM | NY | 183 | 0.525 | 1.149 | 0.086 | 0.004 |
| V4_trailing_1.0_atr | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | 36 | 0.500 | 1.132 | 0.065 | 0.012 |
| V4_trailing_1.5_atr | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | 36 | 0.528 | 1.233 | 0.127 | 0.028 |
| V5_sma20_cross | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | 36 | 0.278 | 0.605 | -0.207 | -0.019 |
| V5_sma50_cross | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | 36 | 0.389 | 1.002 | 0.001 | 0.000 |
| V6_time_fixed_240 | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | 36 | 0.528 | 1.207 | 0.118 | 0.014 |
| V6_time_fixed_60 | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | 36 | 0.472 | 1.143 | 0.074 | 0.019 |
| V4_trailing_1.0_atr | USDJPY | M15 | KAMA_CROSS_MOM | ASIA | 134 | 0.403 | 1.050 | 0.025 | 0.001 |
| V4_trailing_1.5_atr | USDJPY | M15 | KAMA_CROSS_MOM | ASIA | 134 | 0.455 | 1.114 | 0.067 | 0.006 |
| V5_sma20_cross | USDJPY | M15 | KAMA_CROSS_MOM | ASIA | 134 | 0.410 | 1.106 | 0.050 | 0.007 |
| V5_sma50_cross | USDJPY | M15 | KAMA_CROSS_MOM | ASIA | 134 | 0.440 | 1.135 | 0.075 | 0.005 |
| V6_time_fixed_240 | USDJPY | M15 | KAMA_CROSS_MOM | ASIA | 134 | 0.507 | 1.266 | 0.153 | 0.015 |
| V6_time_fixed_60 | USDJPY | M15 | KAMA_CROSS_MOM | ASIA | 134 | 0.507 | 1.243 | 0.134 | 0.018 |
| V4_trailing_1.0_atr | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | 118 | 0.500 | 1.597 | 0.337 | 0.025 |
| V4_trailing_1.5_atr | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | 118 | 0.508 | 1.581 | 0.335 | 0.020 |
| V5_sma20_cross | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | 118 | 0.449 | 1.643 | 0.332 | 0.017 |
| V5_sma50_cross | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | 118 | 0.475 | 1.576 | 0.320 | 0.015 |
| V6_time_fixed_240 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | 118 | 0.508 | 1.581 | 0.335 | 0.022 |
| V6_time_fixed_60 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | 118 | 0.508 | 1.581 | 0.335 | 0.042 |
| V4_trailing_1.0_atr | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | 214 | 0.551 | 1.594 | 0.324 | 0.008 |
| V4_trailing_1.5_atr | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | 214 | 0.551 | 1.594 | 0.324 | 0.009 |
| V5_sma20_cross | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | 214 | 0.514 | 1.619 | 0.322 | 0.010 |
| V5_sma50_cross | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | 214 | 0.528 | 1.647 | 0.335 | 0.009 |
| V6_time_fixed_240 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | 214 | 0.551 | 1.594 | 0.324 | 0.010 |
| V6_time_fixed_60 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | 214 | 0.551 | 1.596 | 0.324 | 0.009 |
| V4_trailing_1.0_atr | XAUUSD | M15 | SPECTRAL_TREND_MOM | NY | 203 | 0.498 | 0.973 | -0.015 | -0.001 |
| V4_trailing_1.5_atr | XAUUSD | M15 | SPECTRAL_TREND_MOM | NY | 203 | 0.522 | 1.036 | 0.021 | 0.001 |
| V5_sma20_cross | XAUUSD | M15 | SPECTRAL_TREND_MOM | NY | 203 | 0.473 | 1.049 | 0.025 | 0.001 |
| V5_sma50_cross | XAUUSD | M15 | SPECTRAL_TREND_MOM | NY | 203 | 0.502 | 1.030 | 0.017 | 0.001 |
| V6_time_fixed_240 | XAUUSD | M15 | SPECTRAL_TREND_MOM | NY | 203 | 0.522 | 1.036 | 0.021 | 0.001 |
| V6_time_fixed_60 | XAUUSD | M15 | SPECTRAL_TREND_MOM | NY | 203 | 0.522 | 1.035 | 0.020 | 0.001 |
| V4_trailing_1.0_atr | XAUUSD | M15 | VELOCITY_ACCEL_GO | NY | 1551 | 0.485 | 0.974 | -0.016 | -0.000 |
| V4_trailing_1.5_atr | XAUUSD | M15 | VELOCITY_ACCEL_GO | NY | 1551 | 0.502 | 1.000 | 0.000 | 0.000 |
| V5_sma20_cross | XAUUSD | M15 | VELOCITY_ACCEL_GO | NY | 1551 | 0.451 | 0.964 | -0.021 | -0.000 |
| V5_sma50_cross | XAUUSD | M15 | VELOCITY_ACCEL_GO | NY | 1551 | 0.489 | 0.981 | -0.012 | -0.000 |
| V6_time_fixed_240 | XAUUSD | M15 | VELOCITY_ACCEL_GO | NY | 1551 | 0.502 | 1.000 | 0.000 | 0.000 |
| V6_time_fixed_60 | XAUUSD | M15 | VELOCITY_ACCEL_GO | NY | 1551 | 0.502 | 1.000 | 0.000 | 0.000 |