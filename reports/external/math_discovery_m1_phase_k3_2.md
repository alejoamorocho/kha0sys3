# Phase K3-2 — TP/SL 7×7 grid on K3 combined survivors

## Summary

- Seeds refined: **189**
- Grid: TP=[0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0]
- Grid: SL=[0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0]
- Backtests: **9,261** (189 × 49 combos)
- Friction: 0.05R FX (AUDUSD, EURAUD, EURJPY, EURUSD, GBPAUD, GBPJPY, GBPUSD, USDJPY) / 0.10R non-FX
- Gate: WR>=0.6 AND PF>=1.3 AND n>=30
- Runtime: **139s (2.3 min)**

| Metric | Value |
|--------|-------|
| Strict survivors total | **818** |
| Best per seed (unique strategies) | **189** |
| Seeds with NO survivors | **0** |

## Top 30 best-per-seed by Calmar

| # | sym | tf | setup | session | inv | tp | sl | n | wr | pf | exp_R | dd_R | calmar |
|---|-----|-----|-------|---------|-----|-----|-----|---|-----|-----|-------|------|--------|
| 1 | EURUSD | H1 | KAMA_CROSS_MOM | NY | True | 1.00 | 1.00 | 67 | 0.627 | 1.958 | 0.247 | 2.4 | 0.1035 |
| 2 | WTI | M15 | SPECTRAL_TREND_MOM | ASIA | False | 0.50 | 1.00 | 66 | 0.682 | 2.272 | 0.261 | 2.6 | 0.1006 |
| 3 | AUDUSD | H1 | SPECTRAL_TREND_MOM | LONDON | False | 0.30 | 0.50 | 49 | 0.755 | 2.020 | 0.197 | 2.1 | 0.0936 |
| 4 | GBPAUD | H1 | KAMA_CROSS_MOM | ASIA | False | 1.00 | 1.50 | 41 | 0.610 | 1.970 | 0.152 | 1.7 | 0.0919 |
| 5 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | False | 0.30 | 0.50 | 118 | 0.686 | 2.718 | 0.517 | 6.2 | 0.0834 |
| 6 | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | False | 1.50 | 1.50 | 36 | 0.611 | 1.638 | 0.183 | 2.3 | 0.0782 |
| 7 | AUDUSD | M15 | KAMA_CROSS_MOM | LONDON | True | 0.30 | 0.50 | 73 | 0.658 | 1.805 | 0.265 | 4.2 | 0.0631 |
| 8 | USDJPY | H1 | SPECTRAL_TREND_MOM | LONDON_NY | False | 0.50 | 1.00 | 86 | 0.663 | 1.724 | 0.150 | 2.5 | 0.0605 |
| 9 | NATGAS | M15 | KAMA_CROSS_MOM | ASIA | True | 0.70 | 1.00 | 94 | 0.702 | 1.834 | 0.166 | 2.8 | 0.0603 |
| 10 | GBPUSD | M15 | KAMA_CROSS_MOM | ASIA | False | 0.30 | 0.50 | 123 | 0.650 | 1.727 | 0.204 | 3.7 | 0.0559 |
| 11 | NATGAS | M1 | KAMA_CROSS_MOM | ASIA | True | 1.50 | 1.00 | 1238 | 0.628 | 2.172 | 0.474 | 8.8 | 0.0539 |
| 12 | EURUSD | M15 | SPECTRAL_TREND_MOM | NY | False | 0.50 | 1.50 | 160 | 0.838 | 1.857 | 0.112 | 2.1 | 0.0535 |
| 13 | EURJPY | M15 | KAMA_CROSS_MOM | LONDON | False | 0.30 | 0.50 | 117 | 0.650 | 2.142 | 0.401 | 7.6 | 0.0528 |
| 14 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | False | 0.30 | 0.50 | 214 | 0.636 | 2.575 | 0.575 | 11.7 | 0.0489 |
| 15 | NATGAS | M1 | KAMA_CROSS_MOM | ALL_DAY | True | 1.50 | 1.00 | 1765 | 0.612 | 2.009 | 0.429 | 9.0 | 0.0477 |
| 16 | GBPJPY | H1 | SPECTRAL_TREND_MOM | LONDON_NY | False | 1.50 | 2.50 | 84 | 0.607 | 1.588 | 0.103 | 2.3 | 0.0451 |
| 17 | NATGAS | M1 | VELOCITY_ACCEL_GO | LONDON | False | 0.70 | 0.50 | 1430 | 0.611 | 1.858 | 0.367 | 8.6 | 0.0427 |
| 18 | USDJPY | M15 | SPECTRAL_TREND_MOM | ALL_DAY | False | 0.30 | 0.50 | 361 | 0.654 | 2.113 | 0.393 | 9.7 | 0.0405 |
| 19 | EURUSD | M15 | KAMA_CROSS_MOM | NY | False | 1.00 | 1.00 | 183 | 0.607 | 1.531 | 0.202 | 5.2 | 0.0384 |
| 20 | GBPUSD | H1 | SPECTRAL_TREND_MOM | LONDON_NY | False | 0.70 | 2.50 | 90 | 0.656 | 1.569 | 0.056 | 1.6 | 0.0360 |
| 21 | AUDUSD | H1 | SPECTRAL_TREND_MOM | LONDON_NY | False | 0.30 | 2.00 | 69 | 0.855 | 1.793 | 0.037 | 1.1 | 0.0337 |
| 22 | USDJPY | M1 | VELOCITY_ACCEL_GO | ASIA | False | 1.50 | 1.50 | 1614 | 0.641 | 1.616 | 0.232 | 7.1 | 0.0327 |
| 23 | USDJPY | M15 | KAMA_CROSS_MOM | ASIA | False | 1.00 | 1.50 | 134 | 0.672 | 1.359 | 0.101 | 3.2 | 0.0313 |
| 24 | NATGAS | M1 | VELOCITY_ACCEL_GO | LONDON_NY | False | 0.70 | 0.50 | 1430 | 0.611 | 1.858 | 0.367 | 11.8 | 0.0311 |
| 25 | GBPJPY | M15 | KAMA_CROSS_MOM | NY | False | 0.50 | 2.00 | 110 | 0.836 | 1.521 | 0.062 | 2.1 | 0.0303 |
| 26 | NATGAS | M1 | SPECTRAL_TREND_MOM | ASIA | True | 3.00 | 3.00 | 344 | 0.637 | 1.451 | 0.174 | 5.9 | 0.0295 |
| 27 | GBPUSD | M1 | SPECTRAL_TREND_MOM | ASIA | True | 1.00 | 1.00 | 893 | 0.619 | 1.559 | 0.222 | 7.6 | 0.0291 |
| 28 | GBPUSD | M1 | VELOCITY_ACCEL_GO | ALL_DAY | True | 1.00 | 1.00 | 1918 | 0.655 | 1.719 | 0.260 | 9.1 | 0.0287 |
| 29 | XAUUSD | H1 | KAMA_CROSS_MOM | LONDON_NY | True | 1.00 | 2.00 | 79 | 0.671 | 1.488 | 0.083 | 3.0 | 0.0278 |
| 30 | GBPUSD | M1 | SPECTRAL_TREND_MOM | ASIA | False | 1.00 | 1.00 | 843 | 0.622 | 1.567 | 0.224 | 8.5 | 0.0261 |

## Top 30 by PF

| # | sym | tf | setup | session | inv | tp | sl | n | wr | pf | exp_R | dd_R | calmar |
|---|-----|-----|-------|---------|-----|-----|-----|---|-----|-----|-------|------|--------|
| 1 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | False | 0.30 | 0.50 | 118 | 0.686 | 2.718 | 0.517 | 6.2 | 0.0834 |
| 2 | AUDUSD | H1 | SPECTRAL_TREND_MOM | LONDON | False | 0.50 | 1.00 | 49 | 0.694 | 2.638 | 0.173 | 1.8 | 0.0934 |
| 3 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | False | 0.30 | 0.50 | 214 | 0.636 | 2.575 | 0.575 | 11.7 | 0.0489 |
| 4 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | False | 0.30 | 1.00 | 118 | 0.805 | 2.428 | 0.248 | 5.2 | 0.0475 |
| 5 | WTI | M15 | SPECTRAL_TREND_MOM | ASIA | False | 0.50 | 2.00 | 66 | 0.742 | 2.329 | 0.119 | 2.0 | 0.0600 |
| 6 | WTI | M15 | SPECTRAL_TREND_MOM | ASIA | False | 0.50 | 1.00 | 66 | 0.682 | 2.272 | 0.261 | 2.6 | 0.1006 |
| 7 | AUDUSD | H1 | SPECTRAL_TREND_MOM | LONDON | False | 0.30 | 1.00 | 49 | 0.796 | 2.223 | 0.105 | 1.6 | 0.0668 |
| 8 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | False | 0.50 | 1.00 | 118 | 0.737 | 2.207 | 0.296 | 5.1 | 0.0579 |
| 9 | NATGAS | M1 | KAMA_CROSS_MOM | ASIA | True | 1.50 | 1.00 | 1238 | 0.628 | 2.172 | 0.474 | 8.8 | 0.0539 |
| 10 | EURJPY | M15 | KAMA_CROSS_MOM | LONDON | False | 0.30 | 0.50 | 117 | 0.650 | 2.142 | 0.401 | 7.6 | 0.0528 |
| 11 | GBPAUD | H1 | KAMA_CROSS_MOM | ASIA | False | 0.70 | 1.50 | 41 | 0.659 | 2.141 | 0.136 | 1.8 | 0.0747 |
| 12 | WTI | M15 | SPECTRAL_TREND_MOM | ASIA | False | 0.30 | 0.50 | 66 | 0.621 | 2.136 | 0.381 | 7.2 | 0.0532 |
| 13 | WTI | M15 | SPECTRAL_TREND_MOM | ASIA | False | 0.50 | 1.50 | 66 | 0.712 | 2.134 | 0.157 | 4.6 | 0.0341 |
| 14 | AUDUSD | H1 | SPECTRAL_TREND_MOM | LONDON | False | 0.50 | 1.50 | 49 | 0.694 | 2.133 | 0.092 | 1.4 | 0.0640 |
| 15 | USDJPY | M15 | SPECTRAL_TREND_MOM | ALL_DAY | False | 0.30 | 0.50 | 361 | 0.654 | 2.113 | 0.393 | 9.7 | 0.0405 |
| 16 | EURUSD | H1 | KAMA_CROSS_MOM | NY | True | 0.70 | 1.00 | 67 | 0.687 | 2.101 | 0.222 | 3.6 | 0.0626 |
| 17 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | False | 0.70 | 1.00 | 118 | 0.669 | 2.095 | 0.330 | 7.2 | 0.0460 |
| 18 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | False | 0.30 | 1.00 | 214 | 0.752 | 2.073 | 0.250 | 8.6 | 0.0291 |
| 19 | EURUSD | H1 | KAMA_CROSS_MOM | NY | True | 0.50 | 1.50 | 67 | 0.761 | 2.033 | 0.108 | 1.9 | 0.0582 |
| 20 | AUDUSD | H1 | SPECTRAL_TREND_MOM | LONDON | False | 0.30 | 0.50 | 49 | 0.755 | 2.020 | 0.197 | 2.1 | 0.0936 |
| 21 | NATGAS | M1 | KAMA_CROSS_MOM | ALL_DAY | True | 1.50 | 1.00 | 1765 | 0.612 | 2.009 | 0.429 | 9.0 | 0.0477 |
| 22 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | False | 0.50 | 1.00 | 214 | 0.687 | 2.006 | 0.299 | 10.8 | 0.0276 |
| 23 | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | False | 0.70 | 0.50 | 36 | 0.611 | 1.999 | 0.402 | 5.4 | 0.0744 |
| 24 | GBPAUD | H1 | KAMA_CROSS_MOM | ASIA | False | 1.00 | 1.50 | 41 | 0.610 | 1.970 | 0.152 | 1.7 | 0.0919 |
| 25 | EURUSD | H1 | KAMA_CROSS_MOM | NY | True | 1.00 | 1.00 | 67 | 0.627 | 1.958 | 0.247 | 2.4 | 0.1035 |
| 26 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | False | 0.30 | 1.50 | 118 | 0.831 | 1.953 | 0.133 | 6.5 | 0.0205 |
| 27 | WTI | M15 | SPECTRAL_TREND_MOM | ASIA | False | 0.70 | 2.00 | 66 | 0.667 | 1.948 | 0.124 | 2.4 | 0.0520 |
| 28 | NATGAS | M1 | KAMA_CROSS_MOM | ASIA | True | 1.00 | 1.00 | 1238 | 0.696 | 1.908 | 0.300 | 6.5 | 0.0461 |
| 29 | EURUSD | M15 | SPECTRAL_TREND_MOM | NY | False | 0.70 | 1.50 | 160 | 0.794 | 1.907 | 0.159 | 3.4 | 0.0469 |
| 30 | WTI | M15 | SPECTRAL_TREND_MOM | ASIA | False | 0.50 | 2.50 | 66 | 0.727 | 1.903 | 0.072 | 1.4 | 0.0499 |

## Distribution (best per seed)

| Metric | p50 | p75 | p90 | max |
|--------|-----|-----|-----|-----|
| WR | 0.616 | 0.627 | 0.655 | 0.855 |
| PF | 1.424 | 1.493 | 1.719 | 2.718 |
| Calmar | 0.0145 | 0.0190 | 0.0384 | 0.1035 |

