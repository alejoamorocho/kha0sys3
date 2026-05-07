# MATH Discovery Phase B — M15+H1+H4 + M1 Tracking + TP/SL Grid

- Backtests run: **24815** (1800 combos × 7 grid points)
- Survivors: **12**
- Gates: n_trades >= 30, WR >= 0.5, PF >= 1.0
- Runtime: 330s (5.5 min)

## Top 50 by Calmar

| sym | tf | setup | session | kind | tp | sl | n | wr | pf | exp_R | dd_R | calmar |
|-----|-----|-------|---------|------|-----|-----|---|-----|-----|-------|------|--------|
| USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | MOM | 0.7 | 0.5 | 118 | 0.517 | 1.684 | 0.395 | 22.4 | 0.018 |
| USDJPY | M15 | KAMA_CROSS_MOM | ASIA | MOM | 1.5 | 1.0 | 134 | 0.552 | 1.183 | 0.093 | 6.2 | 0.015 |
| NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | MOM | 0.7 | 0.5 | 36 | 0.583 | 1.194 | 0.102 | 7.4 | 0.014 |
| EURUSD | H1 | KAMA_CROSS_MOM | NY | MOM | 1.5 | 1.0 | 67 | 0.507 | 1.173 | 0.068 | 7.0 | 0.010 |
| NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | MOM | 2.0 | 1.0 | 36 | 0.500 | 1.091 | 0.051 | 6.2 | 0.008 |
| USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | MOM | 1.0 | 1.0 | 118 | 0.551 | 1.165 | 0.082 | 12.9 | 0.006 |
| NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | MOM | 1.5 | 1.0 | 36 | 0.556 | 1.087 | 0.042 | 7.5 | 0.006 |
| USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | MOM | 1.0 | 1.0 | 214 | 0.519 | 1.160 | 0.089 | 39.6 | 0.002 |
| EURUSD | M15 | KAMA_CROSS_MOM | NY | MOM | 0.7 | 0.5 | 183 | 0.546 | 1.077 | 0.045 | 26.9 | 0.002 |
| XAUUSD | M15 | SPECTRAL_TREND_MOM | NY | MOM | 0.7 | 0.5 | 203 | 0.522 | 1.053 | 0.031 | 21.1 | 0.001 |
| XAUUSD | M15 | VELOCITY_ACCEL_GO | NY | MOM | 0.7 | 0.5 | 1551 | 0.504 | 1.055 | 0.035 | 50.9 | 0.001 |
| USDJPY | M15 | KAMA_CROSS_MOM | ASIA | MOM | 0.7 | 0.5 | 134 | 0.537 | 1.006 | 0.004 | 9.3 | 0.000 |

## Per-TF survivors

- M15: 11
- H1: 1

## Per-symbol survivors

- USDJPY: 5
- NASDAQ100: 3
- XAUUSD: 2
- EURUSD: 2