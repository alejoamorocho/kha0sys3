# MATH Discovery Phase K3 — Expanded 15-Symbol Universe

Generated: Phase K-B (14 syms) + Phase K-F (15 syms) + Phase K3-2 (7×7 grid refinement)

## Summary

| Phase | Syms | Backtests | Raw Survivors | Strict (WR>=0.6 PF>=1.3) | Runtime |
|-------|------|-----------|---------------|----------------------------------------|---------|
| K3-B (M15/H1/H4) | 14 | 35,280 | 874 | 37 | 432s (7.2m) |
| K3-F (M1) | 15 | 12,600 | 2802 | 199 | 5902s (98.4m) |
| K3-2 (7×7 grid) | — | ~9,261 | — | 818 | 140s (2.3m) |
| **TOTAL** | — | — | — | **189 unique** | **107.9m** |

New symbols vs Phase K: GBPUSD, AUDUSD, GBPJPY, EURJPY (B+F), EURAUD (F only)
Extended FX friction (0.05R): AUDUSD, EURAUD, EURJPY, EURUSD, GBPAUD, GBPJPY, GBPUSD, USDJPY

## K3-2 Top 30 best-per-seed (by Calmar)

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

## K3-2 Distribution

**K3-2 best-per-seed** (n=189)
  - WR: p50=0.616  p75=0.627  p90=0.655  max=0.855
  - PF: p50=1.424  p75=1.493  p90=1.719  max=2.718

