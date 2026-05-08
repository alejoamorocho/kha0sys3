# MATH Discovery Phase B — M15+H1+H4 + M1 Tracking + TP/SL Grid

- Backtests run: **24815** (1800 combos × 7 grid points)
- Survivors: **519**
- Gates: n_trades >= 30, WR >= 0.5, PF >= 1.0
- Runtime: 378s (6.3 min)

## Top 50 by Calmar

| sym | tf | setup | session | kind | tp | sl | n | wr | pf | exp_R | dd_R | calmar |
|-----|-----|-------|---------|------|-----|-----|---|-----|-----|-------|------|--------|
| NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | MOM | 1.5 | 1.0 | 36 | 0.583 | 1.966 | 0.342 | 2.2 | 0.155 |
| USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | MOM | 0.7 | 0.5 | 118 | 0.525 | 2.406 | 0.645 | 5.0 | 0.128 |
| NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | MOM | 0.7 | 0.5 | 36 | 0.611 | 1.999 | 0.402 | 3.3 | 0.122 |
| BRENT | H1 | KAMA_CROSS_MOM | NY | MOM | 1.0 | 1.0 | 47 | 0.532 | 1.810 | 0.195 | 1.8 | 0.109 |
| GBPAUD | H1 | KAMA_CROSS_MOM | ASIA | MOM | 1.0 | 1.0 | 41 | 0.610 | 1.827 | 0.207 | 2.1 | 0.099 |
| EURUSD | H1 | KAMA_CROSS_MOM | NY | MOM | 2.0 | 1.0 | 67 | 0.567 | 2.086 | 0.345 | 3.7 | 0.094 |
| GBPAUD | H1 | KAMA_CROSS_MOM | ASIA | MOM | 2.0 | 1.0 | 41 | 0.585 | 1.996 | 0.262 | 2.9 | 0.089 |
| GBPAUD | H1 | KAMA_CROSS_MOM | ASIA | MOM | 1.0 | 2.0 | 41 | 0.610 | 1.665 | 0.090 | 1.0 | 0.085 |
| SP500 | M15 | KAMA_CROSS_MOM | ASIA | MOM | 0.7 | 0.5 | 40 | 0.575 | 1.598 | 0.265 | 3.3 | 0.080 |
| GBPAUD | H1 | KAMA_CROSS_MOM | ASIA | MOM | 1.5 | 1.0 | 41 | 0.585 | 1.936 | 0.247 | 3.2 | 0.076 |
| EURUSD | H1 | KAMA_CROSS_MOM | NY | MOM | 1.5 | 1.0 | 67 | 0.597 | 2.113 | 0.318 | 4.2 | 0.076 |
| USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | MOM | 0.7 | 0.5 | 214 | 0.500 | 2.443 | 0.725 | 9.8 | 0.074 |
| NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | MOM | 2.0 | 1.0 | 36 | 0.528 | 1.846 | 0.351 | 4.9 | 0.072 |
| EURUSD | H1 | KAMA_CROSS_MOM | NY | MOM | 1.0 | 1.0 | 67 | 0.627 | 1.958 | 0.247 | 3.5 | 0.071 |
| SP500 | M15 | SPECTRAL_TREND_MOM | ASIA | MOM | 1.5 | 1.0 | 52 | 0.519 | 1.505 | 0.203 | 3.1 | 0.066 |
| NASDAQ100 | H1 | SPECTRAL_TREND_MOM | ASIA | MOM | 0.7 | 0.5 | 49 | 0.551 | 1.753 | 0.218 | 3.3 | 0.066 |
| USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | MOM | 1.0 | 1.0 | 118 | 0.585 | 1.854 | 0.332 | 5.3 | 0.063 |
| NASDAQ100 | H4 | KAMA_CROSS_MOM | ALL_DAY | MOM | 0.7 | 0.5 | 33 | 0.515 | 1.568 | 0.203 | 3.3 | 0.062 |
| NASDAQ100 | H1 | SPECTRAL_TREND_MOM | LONDON | MOM | 0.7 | 0.5 | 39 | 0.564 | 2.359 | 0.451 | 7.4 | 0.061 |
| NASDAQ100 | H1 | SPECTRAL_TREND_MOM | LONDON | MOM | 1.0 | 1.0 | 39 | 0.590 | 1.580 | 0.159 | 2.8 | 0.057 |
| NASDAQ100 | H1 | GARCH_Z_FADE | LONDON | FADE | 0.7 | 0.5 | 31 | 0.548 | 1.481 | 0.219 | 3.9 | 0.056 |
| NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | MOM | 1.0 | 1.0 | 36 | 0.639 | 1.757 | 0.241 | 4.3 | 0.055 |
| NATGAS | M15 | KAMA_CROSS_MOM | ASIA | MOM | 0.7 | 0.5 | 94 | 0.553 | 1.480 | 0.201 | 3.6 | 0.055 |
| USDJPY | M15 | KAMA_CROSS_MOM | ASIA | MOM | 1.0 | 1.0 | 134 | 0.627 | 1.575 | 0.200 | 3.7 | 0.055 |
| USDJPY | M15 | KAMA_CROSS_MOM | ASIA | MOM | 1.5 | 1.0 | 134 | 0.575 | 1.866 | 0.343 | 6.3 | 0.054 |
| USDJPY | H1 | SPECTRAL_TREND_MOM | LONDON | MOM | 2.0 | 1.0 | 45 | 0.511 | 2.046 | 0.290 | 5.4 | 0.054 |
| EURUSD | H1 | KAMA_CROSS_MOM | NY | MOM | 1.5 | 2.5 | 67 | 0.612 | 1.658 | 0.091 | 1.8 | 0.052 |
| SP500 | H1 | KAMA_CROSS_MOM | NY | MOM | 0.7 | 0.5 | 87 | 0.517 | 1.611 | 0.268 | 5.4 | 0.050 |
| GBPAUD | H1 | KAMA_CROSS_MOM | ALL_DAY | MOM | 1.5 | 1.0 | 108 | 0.528 | 1.570 | 0.242 | 4.9 | 0.049 |
| USDJPY | M15 | KAMA_CROSS_MOM | ASIA | MOM | 0.7 | 0.5 | 134 | 0.560 | 1.565 | 0.254 | 5.3 | 0.048 |
| GBPAUD | H1 | KAMA_CROSS_MOM | ASIA | MOM | 1.5 | 2.5 | 41 | 0.561 | 1.658 | 0.080 | 1.7 | 0.048 |
| SP500 | M15 | SPECTRAL_TREND_MOM | ASIA | MOM | 2.0 | 1.0 | 52 | 0.500 | 1.509 | 0.215 | 4.5 | 0.048 |
| USDJPY | H1 | SPECTRAL_TREND_MOM | LONDON | MOM | 1.5 | 1.0 | 45 | 0.511 | 1.726 | 0.201 | 4.2 | 0.048 |
| GBPAUD | H1 | KAMA_CROSS_MOM | ALL_DAY | MOM | 2.0 | 1.0 | 107 | 0.523 | 1.662 | 0.290 | 6.3 | 0.046 |
| WTI | M15 | SPECTRAL_TREND_MOM | ASIA | MOM | 1.0 | 2.0 | 66 | 0.591 | 1.797 | 0.137 | 3.0 | 0.046 |
| EURUSD | M15 | KAMA_CROSS_MOM | NY | MOM | 1.0 | 1.0 | 183 | 0.607 | 1.531 | 0.202 | 4.5 | 0.045 |
| EURUSD | M15 | KAMA_CROSS_MOM | NY | MOM | 0.7 | 0.5 | 183 | 0.541 | 1.593 | 0.282 | 6.6 | 0.043 |
| EURUSD | M15 | SPECTRAL_TREND_MOM | NY | MOM | 0.7 | 0.5 | 160 | 0.525 | 1.456 | 0.225 | 5.4 | 0.042 |
| GBPAUD | H1 | KAMA_CROSS_MOM | LONDON_NY | MOM | 1.5 | 1.0 | 60 | 0.550 | 1.468 | 0.172 | 4.2 | 0.041 |
| NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | MOM | 1.5 | 2.5 | 36 | 0.611 | 1.361 | 0.072 | 1.8 | 0.040 |
| XAUUSD | H1 | KAMA_CROSS_MOM | NY | MOM | 1.5 | 1.0 | 60 | 0.533 | 1.333 | 0.124 | 3.2 | 0.039 |
| XAUUSD | H1 | SPECTRAL_TREND_MOM | NY | MOM | 0.7 | 0.5 | 76 | 0.513 | 1.599 | 0.224 | 5.9 | 0.038 |
| EURUSD | H1 | KAMA_CROSS_MOM | NY | MOM | 1.0 | 2.0 | 67 | 0.642 | 1.583 | 0.090 | 2.4 | 0.038 |
| GBPAUD | H1 | KAMA_CROSS_MOM | LONDON_NY | MOM | 0.7 | 0.5 | 60 | 0.533 | 1.416 | 0.186 | 4.9 | 0.038 |
| NASDAQ100 | H1 | GARCH_Z_FADE | LONDON | FADE | 1.0 | 1.0 | 31 | 0.516 | 1.419 | 0.129 | 3.6 | 0.036 |
| USDJPY | H1 | SPECTRAL_TREND_MOM | ASIA | MOM | 2.0 | 1.0 | 40 | 0.500 | 1.397 | 0.151 | 4.2 | 0.036 |
| XAUUSD | H1 | KAMA_CROSS_MOM | NY | MOM | 1.0 | 1.0 | 60 | 0.583 | 1.303 | 0.097 | 2.7 | 0.035 |
| NATGAS | M15 | KAMA_CROSS_MOM | ASIA | MOM | 1.0 | 1.0 | 94 | 0.617 | 1.626 | 0.176 | 5.0 | 0.035 |
| USDJPY | H1 | SPECTRAL_TREND_MOM | LONDON | MOM | 1.0 | 1.0 | 45 | 0.511 | 1.546 | 0.152 | 4.4 | 0.034 |
| NASDAQ100 | H1 | SPECTRAL_TREND_MOM | LONDON | MOM | 2.0 | 1.0 | 39 | 0.564 | 1.413 | 0.125 | 3.8 | 0.033 |

## Per-TF survivors

- M15: 362
- H1: 155
- H4: 2

## Per-symbol survivors

- USDJPY: 120
- EURUSD: 105
- NATGAS: 68
- GBPAUD: 59
- WTI: 42
- NASDAQ100: 38
- XAUUSD: 34
- SP500: 26
- BRENT: 21
- XAGUSD: 6