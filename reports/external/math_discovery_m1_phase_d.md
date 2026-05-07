# MATH Discovery Phase D — Salidas alternativas

- Strategies tested: 7
- Variants per strategy: 3 (V1 baseline, V2 opposite_only, V3 opposite+tpsl)
- Total runs: 21

## Best variant per strategy

| sym | tf | setup | session | invert | best | tp | sl | n | wr | pf | exp_R | dd_R | calmar |
|-----|-----|-------|---------|--------|------|-----|-----|---|-----|-----|-------|------|--------|
| EURUSD | H1 | KAMA_CROSS_MOM | NY | True | V3_opposite_with_tpsl | 1.75 | 1.05 | 67 | 0.522 | 1.432 | 0.154 | 3.0 | 0.051 |
| USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | False | V1_baseline | 0.50 | 0.55 | 118 | 0.593 | 1.570 | 0.273 | 11.7 | 0.023 |
| USDJPY | M15 | KAMA_CROSS_MOM | ASIA | False | V3_opposite_with_tpsl | 1.50 | 0.80 | 134 | 0.500 | 1.241 | 0.141 | 8.5 | 0.017 |
| NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | False | V1_baseline | 1.50 | 0.80 | 36 | 0.528 | 1.182 | 0.104 | 8.0 | 0.013 |
| USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | False | V2_opposite_only | 0.50 | 0.55 | 214 | 0.444 | 1.323 | 0.413 | 42.6 | 0.010 |
| EURUSD | M15 | KAMA_CROSS_MOM | NY | False | V1_baseline | 1.25 | 0.80 | 183 | 0.519 | 1.115 | 0.068 | 12.0 | 0.006 |
| XAUUSD | M15 | SPECTRAL_TREND_MOM | NY | False | V1_baseline | 0.75 | 0.55 | 203 | 0.522 | 1.036 | 0.021 | 19.7 | 0.001 |

## All runs (all 3 variants per strategy)

| variant | sym | tf | setup | session | n | wr | pf | exp_R | calmar |
|---------|-----|-----|-------|---------|---|-----|-----|-------|--------|
| V1_baseline | EURUSD | H1 | KAMA_CROSS_MOM | NY | 67 | 0.522 | 1.432 | 0.154 | 0.021 |
| V2_opposite_only | EURUSD | H1 | KAMA_CROSS_MOM | NY | 67 | 0.463 | 1.152 | 0.071 | 0.006 |
| V3_opposite_with_tpsl | EURUSD | H1 | KAMA_CROSS_MOM | NY | 67 | 0.522 | 1.432 | 0.154 | 0.051 |
| V1_baseline | EURUSD | M15 | KAMA_CROSS_MOM | NY | 183 | 0.519 | 1.115 | 0.068 | 0.006 |
| V2_opposite_only | EURUSD | M15 | KAMA_CROSS_MOM | NY | 183 | 0.432 | 0.752 | -0.433 | -0.004 |
| V3_opposite_with_tpsl | EURUSD | M15 | KAMA_CROSS_MOM | NY | 183 | 0.519 | 1.115 | 0.068 | 0.005 |
| V1_baseline | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | 36 | 0.528 | 1.182 | 0.104 | 0.013 |
| V2_opposite_only | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | 36 | 0.500 | 0.787 | -0.286 | -0.011 |
| V3_opposite_with_tpsl | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | 36 | 0.528 | 1.182 | 0.104 | 0.012 |
| V1_baseline | USDJPY | M15 | KAMA_CROSS_MOM | ASIA | 134 | 0.500 | 1.241 | 0.141 | 0.015 |
| V2_opposite_only | USDJPY | M15 | KAMA_CROSS_MOM | ASIA | 134 | 0.537 | 1.290 | 0.348 | 0.009 |
| V3_opposite_with_tpsl | USDJPY | M15 | KAMA_CROSS_MOM | ASIA | 134 | 0.500 | 1.241 | 0.141 | 0.017 |
| V1_baseline | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | 118 | 0.593 | 1.570 | 0.273 | 0.023 |
| V2_opposite_only | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | 118 | 0.424 | 1.498 | 0.445 | 0.013 |
| V3_opposite_with_tpsl | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | 118 | 0.542 | 1.539 | 0.247 | 0.014 |
| V1_baseline | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | 214 | 0.551 | 1.594 | 0.324 | 0.009 |
| V2_opposite_only | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | 214 | 0.444 | 1.323 | 0.413 | 0.010 |
| V3_opposite_with_tpsl | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | 214 | 0.509 | 1.573 | 0.302 | 0.009 |
| V1_baseline | XAUUSD | M15 | SPECTRAL_TREND_MOM | NY | 203 | 0.522 | 1.036 | 0.021 | 0.001 |
| V2_opposite_only | XAUUSD | M15 | SPECTRAL_TREND_MOM | NY | 203 | 0.443 | 0.656 | -0.469 | -0.003 |
| V3_opposite_with_tpsl | XAUUSD | M15 | SPECTRAL_TREND_MOM | NY | 203 | 0.498 | 0.901 | -0.055 | -0.002 |