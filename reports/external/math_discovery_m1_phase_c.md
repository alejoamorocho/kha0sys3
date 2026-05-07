# MATH Discovery Phase C — fine TP/SL grid on Phase B survivors

- Phase B survivors refined: **12**
- Backtests run: **1452**
- Phase-C survivors (gates: n>=30 wr>=0.5 pf>=1): **66**
- Best (tp, sl) per strategy: **8**
- Runtime: 8s

## Best (tp, sl) per strategy

| sym | tf | setup | session | invert | tp | sl | n | wr | pf | exp_R | dd_R | calmar |
|-----|-----|-------|---------|--------|-----|-----|---|-----|-----|-------|------|--------|
| EURUSD | H1 | KAMA_CROSS_MOM | NY | True | 1.75 | 1.05 | 67 | 0.522 | 1.432 | 0.154 | 3.9 | 0.040 |
| USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | False | 0.75 | 0.55 | 118 | 0.508 | 1.581 | 0.335 | 12.6 | 0.027 |
| NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | False | 1.50 | 0.80 | 36 | 0.528 | 1.182 | 0.104 | 5.6 | 0.019 |
| USDJPY | M15 | KAMA_CROSS_MOM | ASIA | False | 1.50 | 0.80 | 134 | 0.500 | 1.241 | 0.141 | 10.8 | 0.013 |
| USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | False | 0.50 | 0.55 | 214 | 0.551 | 1.594 | 0.324 | 34.2 | 0.009 |
| EURUSD | M15 | KAMA_CROSS_MOM | NY | False | 1.25 | 0.80 | 183 | 0.519 | 1.115 | 0.068 | 12.7 | 0.005 |
| XAUUSD | M15 | SPECTRAL_TREND_MOM | NY | False | 0.75 | 0.55 | 203 | 0.522 | 1.036 | 0.021 | 20.5 | 0.001 |
| XAUUSD | M15 | VELOCITY_ACCEL_GO | NY | False | 0.75 | 0.55 | 1551 | 0.502 | 1.000 | 0.000 | 60.1 | 0.000 |