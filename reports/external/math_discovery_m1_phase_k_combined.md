# MATH Discovery Phase K — Realistic Vantage Friction (0.05 FX / 0.10 non-FX)

## Summary

| Phase | Backtests | Raw Survivors (WR>=0.50 PF>=1.0) | Strict Survivors (WR>=0.60 PF>=1.30) | Runtime |
|-------|-----------|-----------------------------------|---------------------------------------|---------|
| B (M15/H1/H4) | 25200 | 519 | 27 | 378s (6.3 min) |
| F (M1 entries) | 3360 | 780 | 41 | 62s (1.0 min) |
| **TOTAL** | **28560** | **1299** | **68** | **7.3 min** |

Gates (strict): WR >= 0.6, PF >= 1.3, n_trades >= 30

## Phase B Re-run (M15/H1/H4 × TP/SL grid)

- Total backtests: **25200**
- Raw survivors (Phase A gate WR>=0.50 PF>=1.0): **519**
- Strict survivors (Phase K gate): **27**

### Top 20 Phase B strict survivors (by Calmar)

| # | sym | tf | setup | session | inv | tp | sl | n | wr | pf | exp_R | dd_R | calmar |
|---|-----|-----|-------|---------|-----|-----|-----|---|-----|-----|-------|------|--------|
| 1 | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | False | 0.70 | 0.50 | 36 | 0.611 | 1.999 | 0.402 | 3.3 | 0.1218 |
| 2 | GBPAUD | H1 | KAMA_CROSS_MOM | ASIA | False | 1.00 | 1.00 | 41 | 0.610 | 1.827 | 0.207 | 2.1 | 0.0985 |
| 3 | GBPAUD | H1 | KAMA_CROSS_MOM | ASIA | False | 1.00 | 2.00 | 41 | 0.610 | 1.665 | 0.090 | 1.0 | 0.0854 |
| 4 | EURUSD | H1 | KAMA_CROSS_MOM | NY | True | 1.00 | 1.00 | 67 | 0.627 | 1.958 | 0.247 | 3.5 | 0.0714 |
| 5 | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | False | 1.00 | 1.00 | 36 | 0.639 | 1.757 | 0.241 | 4.3 | 0.0555 |
| 6 | USDJPY | M15 | KAMA_CROSS_MOM | ASIA | False | 1.00 | 1.00 | 134 | 0.627 | 1.575 | 0.200 | 3.7 | 0.0547 |
| 7 | EURUSD | H1 | KAMA_CROSS_MOM | NY | True | 1.50 | 2.50 | 67 | 0.612 | 1.658 | 0.091 | 1.8 | 0.0520 |
| 8 | EURUSD | M15 | KAMA_CROSS_MOM | NY | False | 1.00 | 1.00 | 183 | 0.607 | 1.531 | 0.202 | 4.5 | 0.0447 |
| 9 | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | False | 1.50 | 2.50 | 36 | 0.611 | 1.361 | 0.072 | 1.8 | 0.0405 |
| 10 | EURUSD | H1 | KAMA_CROSS_MOM | NY | True | 1.00 | 2.00 | 67 | 0.642 | 1.583 | 0.090 | 2.4 | 0.0380 |
| 11 | NATGAS | M15 | KAMA_CROSS_MOM | ASIA | True | 1.00 | 1.00 | 94 | 0.617 | 1.626 | 0.176 | 5.0 | 0.0354 |
| 12 | XAUUSD | H1 | KAMA_CROSS_MOM | LONDON_NY | True | 1.00 | 2.00 | 79 | 0.671 | 1.488 | 0.083 | 2.6 | 0.0318 |
| 13 | EURUSD | M15 | SPECTRAL_TREND_MOM | NY | False | 1.00 | 2.00 | 160 | 0.738 | 1.604 | 0.123 | 3.9 | 0.0316 |
| 14 | EURUSD | H1 | KAMA_CROSS_MOM | NY | True | 0.50 | 2.50 | 67 | 0.761 | 1.722 | 0.047 | 1.5 | 0.0307 |
| 15 | WTI | M15 | SPECTRAL_TREND_MOM | ASIA | False | 0.50 | 2.50 | 66 | 0.727 | 1.903 | 0.072 | 2.4 | 0.0296 |
| 16 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | False | 0.50 | 2.50 | 118 | 0.814 | 1.704 | 0.085 | 3.6 | 0.0238 |
| 17 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | False | 1.00 | 2.00 | 118 | 0.644 | 1.428 | 0.113 | 5.3 | 0.0213 |
| 18 | USDJPY | M15 | SPECTRAL_TREND_MOM | NY | True | 1.00 | 2.00 | 145 | 0.669 | 1.365 | 0.077 | 3.8 | 0.0204 |
| 19 | USDJPY | M15 | KAMA_CROSS_MOM | ASIA | False | 1.50 | 2.50 | 134 | 0.657 | 1.463 | 0.102 | 5.2 | 0.0197 |
| 20 | EURUSD | M15 | SPECTRAL_TREND_MOM | NY | False | 0.50 | 2.50 | 160 | 0.869 | 1.603 | 0.050 | 2.7 | 0.0187 |

### Phase B Distribution (raw survivors)

**Phase B raw** (n=519)
  - WR: p50=0.539  p75=0.599  p90=0.669  max=0.869
  - PF: p50=1.110  p75=1.294  p90=1.546  max=2.443

## Phase F Re-run (M1 entries)

- Total backtests: **3360**
- Raw survivors (Phase A gate WR>=0.50 PF>=1.0): **780**
- Strict survivors (Phase K gate): **41**

### Top 20 Phase F strict survivors (by Calmar)

| # | sym | setup | session | inv | tp | sl | n | wr | pf | exp_R | dd_R | calmar |
|---|-----|-------|---------|-----|-----|-----|---|-----|-----|-------|------|--------|
| 1 | EURUSD | HURST_TREND_MOM | ASIA | False | 1.00 | 1.00 | 1490 | 0.634 | 1.569 | 0.218 | 8.8 | 0.0250 |
| 2 | EURUSD | HURST_TREND_MOM | ALL_DAY | False | 1.00 | 1.00 | 1676 | 0.619 | 1.467 | 0.187 | 8.9 | 0.0210 |
| 3 | EURUSD | VELOCITY_ACCEL_GO | ASIA | False | 1.00 | 1.00 | 1604 | 0.627 | 1.518 | 0.203 | 9.9 | 0.0206 |
| 4 | USDJPY | VELOCITY_ACCEL_GO | ASIA | False | 1.00 | 1.00 | 1614 | 0.650 | 1.680 | 0.250 | 12.3 | 0.0202 |
| 5 | EURUSD | KALMAN_INNOV_EXPAND | ALL_DAY | True | 1.00 | 1.00 | 1888 | 0.644 | 1.637 | 0.238 | 13.0 | 0.0184 |
| 6 | EURUSD | VELOCITY_ACCEL_GO | ALL_DAY | True | 1.00 | 1.00 | 1861 | 0.643 | 1.631 | 0.236 | 13.6 | 0.0174 |
| 7 | USDJPY | VELOCITY_ACCEL_GO | ALL_DAY | False | 1.00 | 1.00 | 1833 | 0.622 | 1.492 | 0.195 | 11.9 | 0.0164 |
| 8 | EURUSD | KALMAN_INNOV_EXPAND | LONDON_NY | True | 1.00 | 1.00 | 1581 | 0.614 | 1.436 | 0.177 | 11.0 | 0.0160 |
| 9 | EURUSD | KAMA_CROSS_MOM | ALL_DAY | True | 1.00 | 1.00 | 1702 | 0.610 | 1.424 | 0.174 | 11.4 | 0.0153 |
| 10 | USDJPY | VELOCITY_ACCEL_GO | LONDON_NY | False | 1.00 | 1.00 | 1586 | 0.611 | 1.421 | 0.172 | 11.3 | 0.0153 |
| 11 | EURUSD | HURST_TREND_MOM | NY | True | 1.00 | 1.00 | 1529 | 0.612 | 1.424 | 0.173 | 11.9 | 0.0146 |
| 12 | EURUSD | KALMAN_INNOV_EXPAND | ASIA | True | 1.00 | 1.00 | 1547 | 0.622 | 1.492 | 0.195 | 13.4 | 0.0146 |
| 13 | EURUSD | HURST_TREND_MOM | ALL_DAY | True | 1.00 | 1.00 | 1831 | 0.619 | 1.472 | 0.189 | 13.2 | 0.0143 |
| 14 | USDJPY | HURST_TREND_MOM | ASIA | False | 1.00 | 1.00 | 1483 | 0.609 | 1.412 | 0.169 | 11.9 | 0.0142 |
| 15 | EURUSD | KALMAN_INNOV_EXPAND | LONDON | True | 1.00 | 1.00 | 1581 | 0.614 | 1.436 | 0.177 | 12.5 | 0.0142 |
| 16 | USDJPY | KALMAN_INNOV_EXPAND | ASIA | False | 1.00 | 1.00 | 1565 | 0.603 | 1.375 | 0.156 | 11.2 | 0.0139 |
| 17 | EURUSD | VELOCITY_ACCEL_GO | LONDON_NY | True | 1.00 | 1.00 | 1573 | 0.614 | 1.440 | 0.178 | 13.0 | 0.0138 |
| 18 | USDJPY | VELOCITY_ACCEL_GO | LONDON | False | 1.00 | 1.00 | 1586 | 0.611 | 1.421 | 0.172 | 13.4 | 0.0129 |
| 19 | EURUSD | VELOCITY_ACCEL_GO | ALL_DAY | False | 1.00 | 1.00 | 1803 | 0.607 | 1.398 | 0.164 | 12.8 | 0.0128 |
| 20 | EURUSD | KALMAN_INNOV_EXPAND | NY | True | 1.00 | 1.00 | 1573 | 0.612 | 1.425 | 0.173 | 14.1 | 0.0123 |

### Phase F Distribution (raw survivors)

**Phase F raw** (n=780)
  - WR: p50=0.574  p75=0.673  p90=0.711  max=0.760
  - PF: p50=1.245  p75=1.388  p90=1.489  max=2.004

## COMBINED Strict Survivors (WR>=0.60 AND PF>=1.30 AND n>=30)

Total: **68** survivors across Phase B + F

### Top 30 by Calmar

| # | phase | sym | tf | setup | session | inv | tp | sl | n | wr | pf | exp_R | dd_R | calmar |
|---|-------|-----|-----|-------|---------|-----|-----|-----|---|-----|-----|-------|------|--------|
| 1 | B | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | False | 0.70 | 0.50 | 36 | 0.611 | 1.999 | 0.402 | 3.3 | 0.1218 |
| 2 | B | GBPAUD | H1 | KAMA_CROSS_MOM | ASIA | False | 1.00 | 1.00 | 41 | 0.610 | 1.827 | 0.207 | 2.1 | 0.0985 |
| 3 | B | GBPAUD | H1 | KAMA_CROSS_MOM | ASIA | False | 1.00 | 2.00 | 41 | 0.610 | 1.665 | 0.090 | 1.0 | 0.0854 |
| 4 | B | EURUSD | H1 | KAMA_CROSS_MOM | NY | True | 1.00 | 1.00 | 67 | 0.627 | 1.958 | 0.247 | 3.5 | 0.0714 |
| 5 | B | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | False | 1.00 | 1.00 | 36 | 0.639 | 1.757 | 0.241 | 4.3 | 0.0555 |
| 6 | B | USDJPY | M15 | KAMA_CROSS_MOM | ASIA | False | 1.00 | 1.00 | 134 | 0.627 | 1.575 | 0.200 | 3.7 | 0.0547 |
| 7 | B | EURUSD | H1 | KAMA_CROSS_MOM | NY | True | 1.50 | 2.50 | 67 | 0.612 | 1.658 | 0.091 | 1.8 | 0.0520 |
| 8 | B | EURUSD | M15 | KAMA_CROSS_MOM | NY | False | 1.00 | 1.00 | 183 | 0.607 | 1.531 | 0.202 | 4.5 | 0.0447 |
| 9 | B | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | False | 1.50 | 2.50 | 36 | 0.611 | 1.361 | 0.072 | 1.8 | 0.0405 |
| 10 | B | EURUSD | H1 | KAMA_CROSS_MOM | NY | True | 1.00 | 2.00 | 67 | 0.642 | 1.583 | 0.090 | 2.4 | 0.0380 |
| 11 | B | NATGAS | M15 | KAMA_CROSS_MOM | ASIA | True | 1.00 | 1.00 | 94 | 0.617 | 1.626 | 0.176 | 5.0 | 0.0354 |
| 12 | B | XAUUSD | H1 | KAMA_CROSS_MOM | LONDON_NY | True | 1.00 | 2.00 | 79 | 0.671 | 1.488 | 0.083 | 2.6 | 0.0318 |
| 13 | B | EURUSD | M15 | SPECTRAL_TREND_MOM | NY | False | 1.00 | 2.00 | 160 | 0.738 | 1.604 | 0.123 | 3.9 | 0.0316 |
| 14 | B | EURUSD | H1 | KAMA_CROSS_MOM | NY | True | 0.50 | 2.50 | 67 | 0.761 | 1.722 | 0.047 | 1.5 | 0.0307 |
| 15 | B | WTI | M15 | SPECTRAL_TREND_MOM | ASIA | False | 0.50 | 2.50 | 66 | 0.727 | 1.903 | 0.072 | 2.4 | 0.0296 |
| 16 | F | EURUSD | M1 | HURST_TREND_MOM | ASIA | False | 1.00 | 1.00 | 1490 | 0.634 | 1.569 | 0.218 | 8.8 | 0.0250 |
| 17 | B | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | False | 0.50 | 2.50 | 118 | 0.814 | 1.704 | 0.085 | 3.6 | 0.0238 |
| 18 | B | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | False | 1.00 | 2.00 | 118 | 0.644 | 1.428 | 0.113 | 5.3 | 0.0213 |
| 19 | F | EURUSD | M1 | HURST_TREND_MOM | ALL_DAY | False | 1.00 | 1.00 | 1676 | 0.619 | 1.467 | 0.187 | 8.9 | 0.0210 |
| 20 | F | EURUSD | M1 | VELOCITY_ACCEL_GO | ASIA | False | 1.00 | 1.00 | 1604 | 0.627 | 1.518 | 0.203 | 9.9 | 0.0206 |
| 21 | B | USDJPY | M15 | SPECTRAL_TREND_MOM | NY | True | 1.00 | 2.00 | 145 | 0.669 | 1.365 | 0.077 | 3.8 | 0.0204 |
| 22 | F | USDJPY | M1 | VELOCITY_ACCEL_GO | ASIA | False | 1.00 | 1.00 | 1614 | 0.650 | 1.680 | 0.250 | 12.3 | 0.0202 |
| 23 | B | USDJPY | M15 | KAMA_CROSS_MOM | ASIA | False | 1.50 | 2.50 | 134 | 0.657 | 1.463 | 0.102 | 5.2 | 0.0197 |
| 24 | B | EURUSD | M15 | SPECTRAL_TREND_MOM | NY | False | 0.50 | 2.50 | 160 | 0.869 | 1.603 | 0.050 | 2.7 | 0.0187 |
| 25 | F | EURUSD | M1 | KALMAN_INNOV_EXPAND | ALL_DAY | True | 1.00 | 1.00 | 1888 | 0.644 | 1.637 | 0.238 | 13.0 | 0.0184 |
| 26 | F | EURUSD | M1 | VELOCITY_ACCEL_GO | ALL_DAY | True | 1.00 | 1.00 | 1861 | 0.643 | 1.631 | 0.236 | 13.6 | 0.0174 |
| 27 | B | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | False | 0.50 | 2.50 | 214 | 0.799 | 1.650 | 0.093 | 5.5 | 0.0169 |
| 28 | F | USDJPY | M1 | VELOCITY_ACCEL_GO | ALL_DAY | False | 1.00 | 1.00 | 1833 | 0.622 | 1.492 | 0.195 | 11.9 | 0.0164 |
| 29 | F | EURUSD | M1 | KALMAN_INNOV_EXPAND | LONDON_NY | True | 1.00 | 1.00 | 1581 | 0.614 | 1.436 | 0.177 | 11.0 | 0.0160 |
| 30 | F | EURUSD | M1 | KAMA_CROSS_MOM | ALL_DAY | True | 1.00 | 1.00 | 1702 | 0.610 | 1.424 | 0.174 | 11.4 | 0.0153 |

### Combined distribution

**Combined strict** (n=68)
  - WR: p50=0.619  p75=0.669  p90=0.738  max=0.869
  - PF: p50=1.436  p75=1.583  p90=1.704  max=1.999

