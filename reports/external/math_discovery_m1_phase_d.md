# MATH Discovery Phase D — Salidas alternativas

- Strategies tested: 8
- Variants per strategy: 3 (V1 baseline, V2 opposite_only, V3 opposite+tpsl)
- Total runs: 24

## Best variant per strategy

| sym | tf | setup | session | invert | best | tp | sl | n | wr | pf | exp_R | dd_R | calmar |
|-----|-----|-------|---------|--------|------|-----|-----|---|-----|-----|-------|------|--------|
| EURUSD | H1 | KAMA_CROSS_MOM | NY | True | V3_opposite_with_tpsl | 1.75 | 1.05 | 67 | 0.522 | 1.432 | 0.154 | 4.9 | 0.031 |
| USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | False | V1_baseline | 0.75 | 0.55 | 118 | 0.508 | 1.581 | 0.335 | 11.0 | 0.030 |
| NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | False | V3_opposite_with_tpsl | 1.50 | 0.80 | 36 | 0.528 | 1.182 | 0.104 | 4.2 | 0.025 |
| USDJPY | M15 | KAMA_CROSS_MOM | ASIA | False | V1_baseline | 1.50 | 0.80 | 134 | 0.500 | 1.241 | 0.141 | 11.6 | 0.012 |
| USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | False | V2_opposite_only | 0.50 | 0.55 | 214 | 0.444 | 1.323 | 0.413 | 42.7 | 0.010 |
| EURUSD | M15 | KAMA_CROSS_MOM | NY | False | V3_opposite_with_tpsl | 1.25 | 0.80 | 183 | 0.519 | 1.115 | 0.068 | 16.6 | 0.004 |
| XAUUSD | M15 | SPECTRAL_TREND_MOM | NY | False | V1_baseline | 0.75 | 0.55 | 203 | 0.522 | 1.036 | 0.021 | 21.1 | 0.001 |
| XAUUSD | M15 | VELOCITY_ACCEL_GO | NY | False | V1_baseline | 0.75 | 0.55 | 1551 | 0.502 | 1.000 | 0.000 | 69.1 | 0.000 |

## All runs (all 3 variants per strategy)

| variant | sym | tf | setup | session | n | wr | pf | exp_R | calmar |
|---------|-----|-----|-------|---------|---|-----|-----|-------|--------|
| V1_baseline | EURUSD | H1 | KAMA_CROSS_MOM | NY | 67 | 0.522 | 1.432 | 0.154 | 0.026 |
| V2_opposite_only | EURUSD | H1 | KAMA_CROSS_MOM | NY | 67 | 0.463 | 1.152 | 0.071 | 0.009 |
| V3_opposite_with_tpsl | EURUSD | H1 | KAMA_CROSS_MOM | NY | 67 | 0.522 | 1.432 | 0.154 | 0.031 |
| V1_baseline | EURUSD | M15 | KAMA_CROSS_MOM | NY | 183 | 0.519 | 1.115 | 0.068 | 0.004 |
| V2_opposite_only | EURUSD | M15 | KAMA_CROSS_MOM | NY | 183 | 0.432 | 0.752 | -0.433 | -0.005 |
| V3_opposite_with_tpsl | EURUSD | M15 | KAMA_CROSS_MOM | NY | 183 | 0.519 | 1.115 | 0.068 | 0.004 |
| V1_baseline | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | 36 | 0.528 | 1.182 | 0.104 | 0.017 |
| V2_opposite_only | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | 36 | 0.500 | 0.787 | -0.286 | -0.027 |
| V3_opposite_with_tpsl | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | 36 | 0.528 | 1.182 | 0.104 | 0.025 |
| V1_baseline | USDJPY | M15 | KAMA_CROSS_MOM | ASIA | 134 | 0.500 | 1.241 | 0.141 | 0.012 |
| V2_opposite_only | USDJPY | M15 | KAMA_CROSS_MOM | ASIA | 134 | 0.537 | 1.290 | 0.348 | 0.012 |
| V3_opposite_with_tpsl | USDJPY | M15 | KAMA_CROSS_MOM | ASIA | 134 | 0.500 | 1.241 | 0.141 | 0.011 |
| V1_baseline | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | 118 | 0.508 | 1.581 | 0.335 | 0.030 |
| V2_opposite_only | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | 118 | 0.424 | 1.498 | 0.445 | 0.018 |
| V3_opposite_with_tpsl | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | 118 | 0.466 | 1.520 | 0.275 | 0.016 |
| V1_baseline | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | 214 | 0.551 | 1.594 | 0.324 | 0.009 |
| V2_opposite_only | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | 214 | 0.444 | 1.323 | 0.413 | 0.010 |
| V3_opposite_with_tpsl | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | 214 | 0.509 | 1.573 | 0.302 | 0.009 |
| V1_baseline | XAUUSD | M15 | SPECTRAL_TREND_MOM | NY | 203 | 0.522 | 1.036 | 0.021 | 0.001 |
| V2_opposite_only | XAUUSD | M15 | SPECTRAL_TREND_MOM | NY | 203 | 0.443 | 0.656 | -0.469 | -0.004 |
| V3_opposite_with_tpsl | XAUUSD | M15 | SPECTRAL_TREND_MOM | NY | 203 | 0.498 | 0.901 | -0.055 | -0.002 |
| V1_baseline | XAUUSD | M15 | VELOCITY_ACCEL_GO | NY | 1551 | 0.502 | 1.000 | 0.000 | 0.000 |
| V2_opposite_only | XAUUSD | M15 | VELOCITY_ACCEL_GO | NY | 1551 | 0.384 | 0.400 | -1.102 | -0.001 |
| V3_opposite_with_tpsl | XAUUSD | M15 | VELOCITY_ACCEL_GO | NY | 1551 | 0.473 | 0.936 | -0.039 | -0.000 |