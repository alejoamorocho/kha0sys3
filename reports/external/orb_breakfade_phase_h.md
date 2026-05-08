# ORB Break-Fade Phase H — ATR Windows + Alt Exits

- Backtests run:  1140
- Survivors:      301
- Runtime:        157s (2.6 min)
- Phase G seeds:  12
- ATR windows:    [5, 10, 14, 20, 50]
- Exit variants:  19 (['V1_baseline', 'V4_trail_0.5', 'V4_trail_1.0', 'V4_trail_1.5', 'V4_trail_2.0', 'V4_trail_2.5', 'V5_sma10', 'V5_sma20', 'V5_sma50', 'V5_sma100', 'V5_sma200', 'V6_time30', 'V6_time60', 'V6_time120', 'V6_time240', 'V6_time480', 'V7_breakback', 'V8_partial_be', 'V8b_partial_trail'])

## Top 15 survivors (sorted by Calmar)

| # | sym | magic | dur | tp | sl | atr_w | variant | n | wr | pf | exp_R | dd_R | calmar |
|---|-----|-------|-----|----|----|-------|---------|---|-----|-----|-------|------|--------|
| 1 | GBPAUD | 15:00 | 120m | 2.0 | 1.5 | 5 | V6_time240 | 1844 | 0.510 | 1.095 | 0.0408 | 29.5 | 2.551 |
| 2 | GBPAUD | 15:00 | 120m | 1.5 | 1.5 | 5 | V6_time240 | 1844 | 0.556 | 1.092 | 0.0369 | 30.0 | 2.266 |
| 3 | GBPAUD | 15:00 | 120m | 1.5 | 1.5 | 5 | V7_breakback | 1844 | 0.559 | 1.088 | 0.0367 | 30.3 | 2.234 |
| 4 | GBPAUD | 15:00 | 120m | 1.5 | 1.5 | 5 | V1_baseline | 1844 | 0.559 | 1.087 | 0.0364 | 30.9 | 2.174 |
| 5 | GBPAUD | 15:00 | 120m | 1.5 | 1.5 | 5 | V6_time480 | 1844 | 0.559 | 1.087 | 0.0364 | 30.9 | 2.174 |
| 6 | GBPAUD | 15:00 | 120m | 1.0 | 1.0 | 10 | V6_time240 | 1844 | 0.566 | 1.098 | 0.0426 | 36.4 | 2.160 |
| 7 | GBPAUD | 15:00 | 120m | 2.0 | 1.5 | 5 | V7_breakback | 1844 | 0.503 | 1.076 | 0.0352 | 30.3 | 2.143 |
| 8 | GBPAUD | 15:00 | 120m | 1.5 | 1.5 | 20 | V1_baseline | 1844 | 0.547 | 1.080 | 0.0292 | 25.4 | 2.122 |
| 9 | GBPAUD | 15:00 | 120m | 1.5 | 1.5 | 20 | V6_time480 | 1844 | 0.547 | 1.080 | 0.0292 | 25.4 | 2.122 |
| 10 | GBPAUD | 15:00 | 120m | 1.5 | 1.5 | 20 | V7_breakback | 1844 | 0.548 | 1.081 | 0.0296 | 25.7 | 2.122 |
| 11 | GBPAUD | 15:00 | 120m | 2.0 | 1.5 | 10 | V7_breakback | 1844 | 0.512 | 1.073 | 0.0297 | 27.1 | 2.017 |
| 12 | GBPAUD | 15:00 | 120m | 1.5 | 1.5 | 14 | V7_breakback | 1844 | 0.547 | 1.080 | 0.0294 | 27.0 | 2.011 |
| 13 | GBPAUD | 15:00 | 120m | 1.5 | 1.5 | 14 | V1_baseline | 1844 | 0.547 | 1.079 | 0.0291 | 26.8 | 2.000 |
| 14 | GBPAUD | 15:00 | 120m | 1.5 | 1.5 | 14 | V6_time480 | 1844 | 0.547 | 1.079 | 0.0291 | 26.8 | 2.000 |
| 15 | GBPAUD | 15:00 | 120m | 2.0 | 1.5 | 10 | V1_baseline | 1844 | 0.510 | 1.071 | 0.0291 | 27.1 | 1.983 |

## Best variant per Phase-G base strategy (12 rows, best Calmar per seed)

| sym | magic | dur | tp | sl | best_atr_w | best_variant | n | wr | pf | exp_R | dd_R | calmar |
|-----|-------|-----|----|----|------------|--------------|---|-----|-----|-------|------|--------|
| GBPAUD | 15:00 | 120m | 2.0 | 1.5 | 5 | V6_time240 | 1844 | 0.510 | 1.095 | 0.0408 | 29.5 | 2.551 |
| GBPAUD | 15:00 | 120m | 1.5 | 1.5 | 5 | V6_time240 | 1844 | 0.556 | 1.092 | 0.0369 | 30.0 | 2.266 |
| GBPAUD | 15:00 | 120m | 1.0 | 1.0 | 10 | V6_time240 | 1844 | 0.566 | 1.098 | 0.0426 | 36.4 | 2.160 |
| USDJPY | 15:00 | 120m | 1.5 | 1.5 | 5 | V7_breakback | 1743 | 0.546 | 1.053 | 0.0221 | 24.6 | 1.569 |
| GBPAUD | 15:00 | 120m | 1.0 | 1.5 | 10 | V1_baseline | 1844 | 0.640 | 1.060 | 0.0194 | 23.4 | 1.531 |
| USDJPY | 15:00 | 120m | 2.0 | 1.5 | 50 | V7_breakback | 1743 | 0.503 | 1.073 | 0.0299 | 35.5 | 1.465 |
| USDJPY | 15:00 | 120m | 1.0 | 1.0 | 20 | V7_breakback | 1743 | 0.544 | 1.037 | 0.0158 | 23.3 | 1.184 |
| GBPAUD | 15:00 | 60m | 1.0 | 1.5 | 50 | V1_baseline | 2000 | 0.651 | 1.049 | 0.0170 | 31.2 | 1.091 |
| GBPAUD | 15:00 | 60m | 1.5 | 1.5 | 50 | V7_breakback | 2000 | 0.549 | 1.040 | 0.0171 | 36.5 | 0.937 |
| GBPAUD | 15:00 | 60m | 1.0 | 1.0 | 5 | V1_baseline | 2000 | 0.554 | 1.033 | 0.0156 | 35.7 | 0.875 |
| GBPAUD | 13:30 | 120m | 1.5 | 1.5 | 10 | V6_time480 | 1836 | 0.529 | 1.020 | 0.0082 | 30.4 | 0.494 |
| USDJPY | 15:00 | 120m | 1.0 | 1.5 | 20 | V7_breakback | 1743 | 0.609 | 1.032 | 0.0097 | 35.4 | 0.479 |

## Survivors by ATR window

- ATR 5: 61 survivors
- ATR 10: 65 survivors
- ATR 14: 63 survivors
- ATR 20: 63 survivors
- ATR 50: 49 survivors

## Survivors by exit variant

- V1_baseline: 55
- V4_trail_1.5: 8
- V4_trail_2.0: 19
- V4_trail_2.5: 44
- V6_time60: 4
- V6_time120: 9
- V6_time240: 40
- V6_time480: 55
- V7_breakback: 56
- V8_partial_be: 2
- V8b_partial_trail: 9
