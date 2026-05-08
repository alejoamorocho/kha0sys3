# Phase K2 — TP/SL grid amplio sobre Phase K survivors

## Summary

- Unique seeds refined: **53**
- Backtests run: **2597** (53 seeds x 49 TP/SL combos)
- Grid: TP = [0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0]
- Grid: SL = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0]
- Friction: 0.05R FX (EURUSD/USDJPY/GBPAUD) / 0.10R non-FX
- Gate: WR >= 0.6 AND PF >= 1.3 AND n >= 30
- Runtime: **42s (0.7 min)**

| Metric | Value |
|--------|-------|
| Strict survivors total | **296** |
| Best per seed (unique strategies) | **53** |
| Seeds with NO survivors | **0** |

## Top 30 best-per-seed by Calmar

| # | sym | tf | setup | session | inv | tp | sl | n | wr | pf | exp_R | dd_R | calmar |
|---|-----|-----|-------|---------|-----|-----|-----|---|-----|-----|-------|------|--------|
| 1 | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | False | 0.70 | 1.00 | 36 | 0.722 | 1.897 | 0.215 | 2.2 | 0.0978 |
| 2 | GBPAUD | H1 | KAMA_CROSS_MOM | ASIA | False | 0.70 | 1.00 | 41 | 0.659 | 1.857 | 0.177 | 2.0 | 0.0891 |
| 3 | WTI | M15 | SPECTRAL_TREND_MOM | ASIA | False | 0.50 | 1.50 | 66 | 0.712 | 2.134 | 0.157 | 1.8 | 0.0863 |
| 4 | EURUSD | H1 | KAMA_CROSS_MOM | NY | True | 1.50 | 2.00 | 67 | 0.612 | 1.669 | 0.118 | 1.5 | 0.0772 |
| 5 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | False | 0.70 | 1.00 | 118 | 0.669 | 2.095 | 0.330 | 4.4 | 0.0759 |
| 6 | USDJPY | H1 | SPECTRAL_TREND_MOM | LONDON_NY | False | 0.50 | 1.00 | 86 | 0.663 | 1.724 | 0.150 | 2.1 | 0.0709 |
| 7 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | False | 0.30 | 0.50 | 214 | 0.636 | 2.575 | 0.575 | 10.6 | 0.0540 |
| 8 | EURUSD | M15 | SPECTRAL_TREND_MOM | NY | False | 0.70 | 1.50 | 160 | 0.794 | 1.907 | 0.159 | 3.0 | 0.0535 |
| 9 | NATGAS | M15 | KAMA_CROSS_MOM | ASIA | True | 1.00 | 1.00 | 94 | 0.617 | 1.626 | 0.176 | 4.2 | 0.0417 |
| 10 | XAUUSD | H1 | KAMA_CROSS_MOM | LONDON_NY | True | 1.00 | 2.00 | 79 | 0.671 | 1.488 | 0.083 | 2.2 | 0.0377 |
| 11 | USDJPY | M15 | SPECTRAL_TREND_MOM | ALL_DAY | False | 0.30 | 0.50 | 361 | 0.654 | 2.113 | 0.393 | 10.6 | 0.0369 |
| 12 | USDJPY | M15 | KAMA_CROSS_MOM | ASIA | False | 1.00 | 1.00 | 134 | 0.627 | 1.575 | 0.200 | 6.8 | 0.0292 |
| 13 | EURUSD | M1 | HURST_TREND_MOM | ASIA | False | 1.00 | 1.00 | 1490 | 0.634 | 1.569 | 0.218 | 7.6 | 0.0286 |
| 14 | USDJPY | M1 | VELOCITY_ACCEL_GO | ASIA | False | 1.50 | 1.50 | 1614 | 0.641 | 1.616 | 0.232 | 8.6 | 0.0270 |
| 15 | EURUSD | M15 | KAMA_CROSS_MOM | NY | False | 1.00 | 1.00 | 183 | 0.607 | 1.531 | 0.202 | 7.6 | 0.0264 |
| 16 | EURUSD | M1 | KALMAN_INNOV_EXPAND | ALL_DAY | True | 1.00 | 1.00 | 1888 | 0.644 | 1.637 | 0.238 | 10.7 | 0.0223 |
| 17 | EURUSD | M1 | VELOCITY_ACCEL_GO | ALL_DAY | True | 1.50 | 1.50 | 1861 | 0.641 | 1.616 | 0.232 | 10.8 | 0.0216 |
| 18 | USDJPY | M1 | SPECTRAL_TREND_MOM | ASIA | False | 2.00 | 2.00 | 852 | 0.603 | 1.390 | 0.160 | 8.0 | 0.0199 |
| 19 | EURUSD | M1 | VELOCITY_ACCEL_GO | ASIA | False | 1.50 | 1.50 | 1604 | 0.634 | 1.568 | 0.218 | 11.1 | 0.0196 |
| 20 | USDJPY | M1 | VELOCITY_ACCEL_GO | LONDON_NY | False | 1.50 | 1.50 | 1586 | 0.618 | 1.463 | 0.186 | 9.7 | 0.0191 |
| 21 | USDJPY | M1 | VELOCITY_ACCEL_GO | ALL_DAY | True | 1.50 | 1.50 | 1821 | 0.616 | 1.452 | 0.182 | 9.8 | 0.0186 |
| 22 | EURUSD | M1 | VELOCITY_ACCEL_GO | ALL_DAY | False | 1.00 | 1.00 | 1803 | 0.607 | 1.398 | 0.164 | 8.9 | 0.0183 |
| 23 | EURUSD | M1 | KALMAN_INNOV_EXPAND | ASIA | True | 1.00 | 1.00 | 1547 | 0.622 | 1.492 | 0.195 | 11.3 | 0.0173 |
| 24 | EURUSD | M1 | HURST_TREND_MOM | ALL_DAY | False | 1.00 | 1.00 | 1676 | 0.619 | 1.467 | 0.187 | 10.9 | 0.0172 |
| 25 | USDJPY | M15 | SPECTRAL_TREND_MOM | NY | True | 1.00 | 2.00 | 145 | 0.669 | 1.365 | 0.077 | 4.5 | 0.0169 |
| 26 | EURUSD | M1 | KALMAN_INNOV_EXPAND | LONDON_NY | True | 1.00 | 1.00 | 1581 | 0.614 | 1.436 | 0.177 | 10.4 | 0.0169 |
| 27 | EURUSD | M1 | KALMAN_INNOV_EXPAND | ASIA | False | 1.50 | 1.50 | 1564 | 0.616 | 1.450 | 0.181 | 11.2 | 0.0162 |
| 28 | USDJPY | M1 | KALMAN_INNOV_EXPAND | ASIA | False | 1.50 | 1.50 | 1565 | 0.621 | 1.482 | 0.192 | 11.9 | 0.0160 |
| 29 | EURUSD | M1 | VELOCITY_ACCEL_GO | LONDON_NY | True | 1.50 | 1.50 | 1573 | 0.608 | 1.402 | 0.166 | 10.3 | 0.0160 |
| 30 | GBPAUD | M15 | SPECTRAL_TREND_MOM | LONDON_NY | False | 1.00 | 2.00 | 161 | 0.683 | 1.305 | 0.076 | 4.8 | 0.0159 |

## Top 30 by absolute PF

| # | sym | tf | setup | session | inv | tp | sl | n | wr | pf | exp_R | dd_R | calmar |
|---|-----|-----|-------|---------|-----|-----|-----|---|-----|-----|-------|------|--------|
| 1 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | False | 0.30 | 0.50 | 118 | 0.686 | 2.718 | 0.517 | 7.0 | 0.0735 |
| 2 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | False | 0.30 | 0.50 | 214 | 0.636 | 2.575 | 0.575 | 10.6 | 0.0540 |
| 3 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | False | 0.30 | 1.00 | 118 | 0.805 | 2.428 | 0.248 | 4.3 | 0.0582 |
| 4 | WTI | M15 | SPECTRAL_TREND_MOM | ASIA | False | 0.50 | 2.00 | 66 | 0.742 | 2.329 | 0.119 | 2.1 | 0.0558 |
| 5 | WTI | M15 | SPECTRAL_TREND_MOM | ASIA | False | 0.50 | 1.00 | 66 | 0.682 | 2.272 | 0.261 | 3.6 | 0.0721 |
| 6 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | False | 0.50 | 1.00 | 118 | 0.737 | 2.207 | 0.296 | 4.4 | 0.0679 |
| 7 | GBPAUD | H1 | KAMA_CROSS_MOM | ASIA | False | 0.70 | 1.50 | 41 | 0.659 | 2.141 | 0.136 | 1.6 | 0.0826 |
| 8 | WTI | M15 | SPECTRAL_TREND_MOM | ASIA | False | 0.30 | 0.50 | 66 | 0.621 | 2.136 | 0.381 | 8.4 | 0.0456 |
| 9 | WTI | M15 | SPECTRAL_TREND_MOM | ASIA | False | 0.50 | 1.50 | 66 | 0.712 | 2.134 | 0.157 | 1.8 | 0.0863 |
| 10 | USDJPY | M15 | SPECTRAL_TREND_MOM | ALL_DAY | False | 0.30 | 0.50 | 361 | 0.654 | 2.113 | 0.393 | 10.6 | 0.0369 |
| 11 | EURUSD | H1 | KAMA_CROSS_MOM | NY | True | 0.70 | 1.00 | 67 | 0.687 | 2.101 | 0.222 | 3.9 | 0.0562 |
| 12 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | False | 0.70 | 1.00 | 118 | 0.669 | 2.095 | 0.330 | 4.4 | 0.0759 |
| 13 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | False | 0.30 | 1.00 | 214 | 0.752 | 2.073 | 0.250 | 8.6 | 0.0290 |
| 14 | EURUSD | H1 | KAMA_CROSS_MOM | NY | True | 0.50 | 1.50 | 67 | 0.761 | 2.033 | 0.108 | 2.8 | 0.0389 |
| 15 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | False | 0.50 | 1.00 | 214 | 0.687 | 2.006 | 0.299 | 9.8 | 0.0306 |
| 16 | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | False | 0.70 | 0.50 | 36 | 0.611 | 1.999 | 0.402 | 4.4 | 0.0914 |
| 17 | GBPAUD | H1 | KAMA_CROSS_MOM | ASIA | False | 1.00 | 1.50 | 41 | 0.610 | 1.970 | 0.152 | 2.0 | 0.0757 |
| 18 | EURUSD | H1 | KAMA_CROSS_MOM | NY | True | 1.00 | 1.00 | 67 | 0.627 | 1.958 | 0.247 | 3.8 | 0.0651 |
| 19 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | False | 0.30 | 1.50 | 118 | 0.831 | 1.953 | 0.133 | 6.6 | 0.0202 |
| 20 | WTI | M15 | SPECTRAL_TREND_MOM | ASIA | False | 0.70 | 2.00 | 66 | 0.667 | 1.948 | 0.124 | 3.3 | 0.0373 |
| 21 | EURUSD | M15 | SPECTRAL_TREND_MOM | NY | False | 0.70 | 1.50 | 160 | 0.794 | 1.907 | 0.159 | 3.0 | 0.0535 |
| 22 | WTI | M15 | SPECTRAL_TREND_MOM | ASIA | False | 0.50 | 2.50 | 66 | 0.727 | 1.903 | 0.072 | 1.5 | 0.0477 |
| 23 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | False | 0.70 | 1.00 | 214 | 0.626 | 1.901 | 0.322 | 14.2 | 0.0226 |
| 24 | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | False | 0.70 | 1.00 | 36 | 0.722 | 1.897 | 0.215 | 2.2 | 0.0978 |
| 25 | EURUSD | H1 | KAMA_CROSS_MOM | NY | True | 0.50 | 1.00 | 67 | 0.716 | 1.869 | 0.148 | 3.0 | 0.0499 |
| 26 | GBPAUD | H1 | KAMA_CROSS_MOM | ASIA | False | 0.70 | 1.00 | 41 | 0.659 | 1.857 | 0.177 | 2.0 | 0.0891 |
| 27 | EURUSD | M15 | SPECTRAL_TREND_MOM | NY | False | 0.50 | 1.50 | 160 | 0.838 | 1.857 | 0.112 | 2.6 | 0.0435 |
| 28 | EURUSD | H1 | KAMA_CROSS_MOM | NY | True | 0.70 | 2.00 | 67 | 0.716 | 1.852 | 0.094 | 1.3 | 0.0735 |
| 29 | EURUSD | H1 | KAMA_CROSS_MOM | NY | True | 0.70 | 1.50 | 67 | 0.716 | 1.836 | 0.127 | 2.5 | 0.0498 |
| 30 | GBPAUD | H1 | KAMA_CROSS_MOM | ASIA | False | 0.70 | 2.00 | 41 | 0.659 | 1.835 | 0.083 | 1.6 | 0.0509 |

## Per-seed comparison: Phase K original vs K2 best

| sym | tf | setup | session | inv | K_tp | K_sl | K_wr | K_pf | K_calmar | K2_tp | K2_sl | K2_wr | K2_pf | K2_calmar | delta_calmar |
|-----|-----|-------|---------|-----|------|------|------|------|----------|-------|-------|-------|-------|-----------|-------------|
| EURUSD | H1 | KAMA_CROSS_MOM | NY | True | 1.00 | 1.00 | 0.627 | 1.958 | 0.0714 | 1.50 | 2.00 | 0.612 | 1.669 | 0.0772 | +0.0059 |
| EURUSD | M1 | HURST_TREND_MOM | ALL_DAY | True | 1.00 | 1.00 | 0.619 | 1.472 | 0.0143 | 1.50 | 1.50 | 0.608 | 1.406 | 0.0151 | +0.0007 |
| EURUSD | M1 | HURST_TREND_MOM | ALL_DAY | False | 1.00 | 1.00 | 0.619 | 1.467 | 0.0210 | 1.00 | 1.00 | 0.619 | 1.467 | 0.0172 | -0.0039 |
| EURUSD | M1 | HURST_TREND_MOM | ASIA | False | 1.00 | 1.00 | 0.634 | 1.569 | 0.0250 | 1.00 | 1.00 | 0.634 | 1.569 | 0.0286 | +0.0036 |
| EURUSD | M1 | HURST_TREND_MOM | NY | True | 1.00 | 1.00 | 0.612 | 1.424 | 0.0146 | 1.00 | 1.00 | 0.612 | 1.424 | 0.0149 | +0.0003 |
| EURUSD | M1 | KALMAN_INNOV_EXPAND | ALL_DAY | False | 1.00 | 1.00 | 0.605 | 1.387 | 0.0113 | 1.00 | 1.00 | 0.605 | 1.387 | 0.0085 | -0.0028 |
| EURUSD | M1 | KALMAN_INNOV_EXPAND | ALL_DAY | True | 1.00 | 1.00 | 0.644 | 1.637 | 0.0184 | 1.00 | 1.00 | 0.644 | 1.637 | 0.0223 | +0.0039 |
| EURUSD | M1 | KALMAN_INNOV_EXPAND | ASIA | False | 1.00 | 1.00 | 0.621 | 1.486 | 0.0111 | 1.50 | 1.50 | 0.616 | 1.450 | 0.0162 | +0.0051 |
| EURUSD | M1 | KALMAN_INNOV_EXPAND | ASIA | True | 1.00 | 1.00 | 0.622 | 1.492 | 0.0146 | 1.00 | 1.00 | 0.622 | 1.492 | 0.0173 | +0.0027 |
| EURUSD | M1 | KALMAN_INNOV_EXPAND | LONDON | True | 1.00 | 1.00 | 0.614 | 1.436 | 0.0142 | 1.00 | 1.00 | 0.614 | 1.436 | 0.0149 | +0.0008 |
| EURUSD | M1 | KALMAN_INNOV_EXPAND | LONDON_NY | True | 1.00 | 1.00 | 0.614 | 1.436 | 0.0160 | 1.00 | 1.00 | 0.614 | 1.436 | 0.0169 | +0.0009 |
| EURUSD | M1 | KALMAN_INNOV_EXPAND | NY | True | 1.00 | 1.00 | 0.612 | 1.425 | 0.0123 | 1.00 | 1.00 | 0.612 | 1.425 | 0.0145 | +0.0022 |
| EURUSD | M1 | KAMA_CROSS_MOM | ALL_DAY | True | 1.00 | 1.00 | 0.610 | 1.424 | 0.0153 | 1.00 | 1.00 | 0.610 | 1.424 | 0.0131 | -0.0022 |
| EURUSD | M1 | KAMA_CROSS_MOM | ASIA | True | 1.00 | 1.00 | 0.603 | 1.373 | 0.0091 | 1.00 | 1.00 | 0.603 | 1.373 | 0.0098 | +0.0007 |
| EURUSD | M1 | OLS_SLOPE_STRONG | ALL_DAY | True | 1.00 | 1.00 | 0.609 | 1.409 | 0.0097 | 2.00 | 2.00 | 0.603 | 1.379 | 0.0109 | +0.0012 |
| EURUSD | M1 | SPECTRAL_TREND_MOM | LONDON | True | 1.00 | 1.00 | 0.601 | 1.370 | 0.0096 | 1.00 | 1.00 | 0.601 | 1.370 | 0.0090 | -0.0006 |
| EURUSD | M1 | VELOCITY_ACCEL_GO | ALL_DAY | False | 1.00 | 1.00 | 0.607 | 1.398 | 0.0128 | 1.00 | 1.00 | 0.607 | 1.398 | 0.0183 | +0.0056 |
| EURUSD | M1 | VELOCITY_ACCEL_GO | ALL_DAY | True | 1.00 | 1.00 | 0.643 | 1.631 | 0.0174 | 1.50 | 1.50 | 0.641 | 1.616 | 0.0216 | +0.0041 |
| EURUSD | M1 | VELOCITY_ACCEL_GO | ASIA | True | 1.00 | 1.00 | 0.618 | 1.461 | 0.0108 | 1.50 | 1.50 | 0.613 | 1.433 | 0.0151 | +0.0043 |
| EURUSD | M1 | VELOCITY_ACCEL_GO | ASIA | False | 1.00 | 1.00 | 0.627 | 1.518 | 0.0206 | 1.50 | 1.50 | 0.634 | 1.568 | 0.0196 | -0.0011 |
| EURUSD | M1 | VELOCITY_ACCEL_GO | LONDON | True | 1.00 | 1.00 | 0.614 | 1.440 | 0.0115 | 1.50 | 1.50 | 0.608 | 1.402 | 0.0147 | +0.0032 |
| EURUSD | M1 | VELOCITY_ACCEL_GO | LONDON_NY | True | 1.00 | 1.00 | 0.614 | 1.440 | 0.0138 | 1.50 | 1.50 | 0.608 | 1.402 | 0.0160 | +0.0022 |
| EURUSD | M15 | KAMA_CROSS_MOM | NY | False | 1.00 | 1.00 | 0.607 | 1.531 | 0.0447 | 1.00 | 1.00 | 0.607 | 1.531 | 0.0264 | -0.0184 |
| EURUSD | M15 | SPECTRAL_TREND_MOM | NY | False | 1.00 | 2.00 | 0.738 | 1.604 | 0.0316 | 0.70 | 1.50 | 0.794 | 1.907 | 0.0535 | +0.0219 |
| GBPAUD | H1 | KAMA_CROSS_MOM | ASIA | False | 1.00 | 1.00 | 0.610 | 1.827 | 0.0985 | 0.70 | 1.00 | 0.659 | 1.857 | 0.0891 | -0.0095 |
| GBPAUD | M15 | SPECTRAL_TREND_MOM | LONDON_NY | False | 1.00 | 2.00 | 0.683 | 1.305 | 0.0151 | 1.00 | 2.00 | 0.683 | 1.305 | 0.0159 | +0.0008 |
| NASDAQ100 | M1 | KAMA_CROSS_MOM | LONDON | False | 1.00 | 1.00 | 0.614 | 1.315 | 0.0095 | 1.00 | 1.00 | 0.614 | 1.315 | 0.0082 | -0.0013 |
| NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | False | 0.70 | 0.50 | 0.611 | 1.999 | 0.1218 | 0.70 | 1.00 | 0.722 | 1.897 | 0.0978 | -0.0240 |
| NATGAS | M15 | KAMA_CROSS_MOM | ASIA | True | 1.00 | 1.00 | 0.617 | 1.626 | 0.0354 | 1.00 | 1.00 | 0.617 | 1.626 | 0.0417 | +0.0063 |
| USDJPY | H1 | SPECTRAL_TREND_MOM | LONDON_NY | False | 0.50 | 2.50 | 0.721 | 1.354 | 0.0121 | 0.50 | 1.00 | 0.663 | 1.724 | 0.0709 | +0.0587 |
| USDJPY | M1 | HURST_TREND_MOM | ALL_DAY | True | 1.00 | 1.00 | 0.602 | 1.371 | 0.0097 | 1.00 | 1.00 | 0.602 | 1.371 | 0.0114 | +0.0016 |
| USDJPY | M1 | HURST_TREND_MOM | ASIA | False | 1.00 | 1.00 | 0.609 | 1.412 | 0.0142 | 1.00 | 1.00 | 0.609 | 1.412 | 0.0144 | +0.0002 |
| USDJPY | M1 | KALMAN_INNOV_EXPAND | ALL_DAY | True | 1.00 | 1.00 | 0.607 | 1.399 | 0.0103 | 2.00 | 2.00 | 0.608 | 1.403 | 0.0149 | +0.0046 |
| USDJPY | M1 | KALMAN_INNOV_EXPAND | ASIA | False | 1.00 | 1.00 | 0.603 | 1.375 | 0.0139 | 1.50 | 1.50 | 0.621 | 1.482 | 0.0160 | +0.0021 |
| USDJPY | M1 | SPECTRAL_TREND_MOM | ASIA | False | 1.00 | 1.00 | 0.601 | 1.372 | 0.0111 | 2.00 | 2.00 | 0.603 | 1.390 | 0.0199 | +0.0088 |
| USDJPY | M1 | VELOCITY_ACCEL_GO | ALL_DAY | True | 1.00 | 1.00 | 0.601 | 1.361 | 0.0080 | 1.50 | 1.50 | 0.616 | 1.452 | 0.0186 | +0.0106 |
| USDJPY | M1 | VELOCITY_ACCEL_GO | ALL_DAY | False | 1.00 | 1.00 | 0.622 | 1.492 | 0.0164 | 1.00 | 1.00 | 0.622 | 1.492 | 0.0158 | -0.0006 |
| USDJPY | M1 | VELOCITY_ACCEL_GO | ASIA | False | 1.00 | 1.00 | 0.650 | 1.680 | 0.0202 | 1.50 | 1.50 | 0.641 | 1.616 | 0.0270 | +0.0068 |
| USDJPY | M1 | VELOCITY_ACCEL_GO | LONDON | False | 1.00 | 1.00 | 0.611 | 1.421 | 0.0129 | 1.00 | 1.00 | 0.611 | 1.421 | 0.0146 | +0.0018 |
| USDJPY | M1 | VELOCITY_ACCEL_GO | LONDON_NY | False | 1.00 | 1.00 | 0.611 | 1.421 | 0.0153 | 1.50 | 1.50 | 0.618 | 1.463 | 0.0191 | +0.0038 |
| USDJPY | M1 | VELOCITY_ACCEL_GO | NY | False | 1.00 | 1.00 | 0.601 | 1.362 | 0.0090 | 1.00 | 1.00 | 0.601 | 1.362 | 0.0090 | -0.0000 |
| USDJPY | M15 | KAMA_CROSS_MOM | ASIA | False | 1.00 | 1.00 | 0.627 | 1.575 | 0.0547 | 1.00 | 1.00 | 0.627 | 1.575 | 0.0292 | -0.0255 |
| USDJPY | M15 | SPECTRAL_TREND_MOM | ALL_DAY | False | 1.00 | 2.00 | 0.701 | 1.434 | 0.0128 | 0.30 | 0.50 | 0.654 | 2.113 | 0.0369 | +0.0241 |
| USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | False | 0.50 | 2.50 | 0.814 | 1.704 | 0.0238 | 0.70 | 1.00 | 0.669 | 2.095 | 0.0759 | +0.0521 |
| USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | False | 0.50 | 2.50 | 0.799 | 1.650 | 0.0169 | 0.30 | 0.50 | 0.636 | 2.575 | 0.0540 | +0.0371 |
| USDJPY | M15 | SPECTRAL_TREND_MOM | NY | True | 1.00 | 2.00 | 0.669 | 1.365 | 0.0204 | 1.00 | 2.00 | 0.669 | 1.365 | 0.0169 | -0.0034 |
| WTI | M15 | SPECTRAL_TREND_MOM | ASIA | False | 0.50 | 2.50 | 0.727 | 1.903 | 0.0296 | 0.50 | 1.50 | 0.712 | 2.134 | 0.0863 | +0.0568 |
| XAUUSD | H1 | KAMA_CROSS_MOM | ALL_DAY | True | 1.00 | 2.00 | 0.673 | 1.315 | 0.0146 | 1.00 | 2.00 | 0.673 | 1.315 | 0.0129 | -0.0017 |
| XAUUSD | H1 | KAMA_CROSS_MOM | LONDON_NY | True | 1.00 | 2.00 | 0.671 | 1.488 | 0.0318 | 1.00 | 2.00 | 0.671 | 1.488 | 0.0377 | +0.0059 |
| XAUUSD | M1 | KALMAN_INNOV_EXPAND | LONDON | True | 1.00 | 1.00 | 0.614 | 1.302 | 0.0092 | 1.00 | 1.00 | 0.614 | 1.302 | 0.0091 | -0.0001 |
| XAUUSD | M1 | KALMAN_INNOV_EXPAND | LONDON_NY | True | 1.00 | 1.00 | 0.614 | 1.302 | 0.0091 | 1.00 | 1.00 | 0.614 | 1.302 | 0.0099 | +0.0008 |
| XAUUSD | M1 | VELOCITY_ACCEL_GO | ASIA | False | 1.00 | 1.00 | 0.615 | 1.306 | 0.0095 | 1.00 | 1.00 | 0.615 | 1.306 | 0.0103 | +0.0008 |
| XAUUSD | M1 | VELOCITY_ACCEL_GO | NY | False | 1.00 | 1.00 | 0.616 | 1.312 | 0.0085 | 1.00 | 1.00 | 0.616 | 1.312 | 0.0065 | -0.0020 |

## Distribution (best per seed)

| Metric | p50 | p75 | p90 | max |
|--------|-----|-----|-----|-----|
| WR | 0.616 | 0.641 | 0.671 | 0.794 |
| PF | 1.436 | 1.575 | 1.897 | 2.575 |
| Calmar | 0.0162 | 0.0270 | 0.0709 | 0.0978 |

