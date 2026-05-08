# MATH Discovery Phase K3-F — M1 entries over 15 symbols

- Symbols: EURUSD, USDJPY, GBPAUD, GBPUSD, AUDUSD, GBPJPY, EURJPY, XAUUSD, XAGUSD, WTI, BRENT, NATGAS, SP500, NASDAQ100, EURAUD
- Friction: 0.05R FX (8 syms) / 0.10R non-FX
- Total backtests: **12,600**
- Raw survivors (WR>=0.5 PF>=1.0): **2802**
- Strict survivors (WR>=0.6 PF>=1.3 n>=30): **199**
- Runtime: 5902s (98.4 min)

## Top 20 strict survivors (by Calmar)

| # | sym | setup | session | inv | tp | sl | n | wr | pf | exp_R | dd_R | calmar |
|---|-----|-------|---------|-----|-----|-----|---|-----|-----|-------|------|--------|
| 1 | NATGAS | KAMA_CROSS_MOM | ASIA | True | 1.50 | 1.00 | 1238 | 0.628 | 2.172 | 0.474 | 6.8 | 0.0698 |
| 2 | NATGAS | SPECTRAL_TREND_MOM | ASIA | True | 1.00 | 1.00 | 344 | 0.660 | 1.637 | 0.235 | 4.8 | 0.0490 |
| 3 | NATGAS | KAMA_CROSS_MOM | ASIA | True | 1.00 | 1.00 | 1238 | 0.696 | 1.908 | 0.300 | 7.2 | 0.0416 |
| 4 | NATGAS | KAMA_CROSS_MOM | ALL_DAY | True | 1.00 | 1.00 | 1765 | 0.688 | 1.819 | 0.279 | 7.2 | 0.0388 |
| 5 | GBPUSD | VELOCITY_ACCEL_GO | ALL_DAY | True | 1.00 | 1.00 | 1918 | 0.655 | 1.719 | 0.260 | 7.8 | 0.0333 |
| 6 | GBPUSD | SPECTRAL_TREND_MOM | ASIA | True | 1.00 | 1.00 | 893 | 0.619 | 1.559 | 0.222 | 6.7 | 0.0331 |
| 7 | NATGAS | KAMA_CROSS_MOM | ALL_DAY | True | 1.50 | 1.00 | 1765 | 0.612 | 2.009 | 0.429 | 13.6 | 0.0316 |
| 8 | NATGAS | KAMA_CROSS_MOM | ASIA | True | 0.70 | 0.50 | 1238 | 0.612 | 1.900 | 0.382 | 12.3 | 0.0310 |
| 9 | NATGAS | KAMA_CROSS_MOM | ALL_DAY | True | 0.70 | 0.50 | 1765 | 0.607 | 1.838 | 0.362 | 12.2 | 0.0297 |
| 10 | NATGAS | KAMA_CROSS_MOM | LONDON_NY | True | 1.00 | 1.00 | 1314 | 0.666 | 1.634 | 0.233 | 8.1 | 0.0287 |
| 11 | USDJPY | VELOCITY_ACCEL_GO | ASIA | False | 1.00 | 1.00 | 1614 | 0.650 | 1.680 | 0.250 | 8.8 | 0.0284 |
| 12 | NATGAS | KAMA_CROSS_MOM | LONDON | True | 1.00 | 1.00 | 1037 | 0.672 | 1.680 | 0.244 | 8.9 | 0.0274 |
| 13 | NATGAS | VELOCITY_ACCEL_GO | LONDON | False | 0.70 | 0.50 | 1430 | 0.611 | 1.858 | 0.367 | 14.3 | 0.0257 |
| 14 | NATGAS | VELOCITY_ACCEL_GO | LONDON_NY | False | 0.70 | 0.50 | 1430 | 0.611 | 1.858 | 0.367 | 14.3 | 0.0257 |
| 15 | EURUSD | HURST_TREND_MOM | ASIA | False | 1.00 | 1.00 | 1490 | 0.634 | 1.569 | 0.218 | 9.6 | 0.0228 |
| 16 | AUDUSD | KAMA_CROSS_MOM | ALL_DAY | True | 1.00 | 1.00 | 1705 | 0.626 | 1.518 | 0.203 | 9.2 | 0.0221 |
| 17 | GBPJPY | KAMA_CROSS_MOM | LONDON | True | 1.00 | 1.00 | 715 | 0.622 | 1.522 | 0.206 | 9.5 | 0.0219 |
| 18 | AUDUSD | KAMA_CROSS_MOM | NY | True | 1.00 | 1.00 | 743 | 0.635 | 1.583 | 0.222 | 10.3 | 0.0215 |
| 19 | GBPJPY | SPECTRAL_TREND_MOM | LONDON | True | 1.00 | 1.00 | 703 | 0.620 | 1.508 | 0.201 | 9.5 | 0.0211 |
| 20 | GBPUSD | SPECTRAL_TREND_MOM | ASIA | False | 1.00 | 1.00 | 843 | 0.622 | 1.567 | 0.224 | 10.7 | 0.0209 |

## Distribution (raw survivors)

**K3-F raw** (n=2802)
  - WR: p50=0.578  p75=0.677  p90=0.715  max=0.790
  - PF: p50=1.244  p75=1.388  p90=1.508  max=2.172

