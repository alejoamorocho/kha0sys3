# MATH Discovery Phase K3-B — M15/H1/H4 over 14 symbols

- Symbols: EURUSD, USDJPY, GBPAUD, GBPUSD, AUDUSD, GBPJPY, EURJPY, XAUUSD, XAGUSD, WTI, BRENT, NATGAS, SP500, NASDAQ100
- Friction: 0.05R FX (8 syms) / 0.10R non-FX
- Total backtests: **35,280**
- Raw survivors (WR>=0.5 PF>=1.0): **874**
- Strict survivors (WR>=0.6 PF>=1.3 n>=30): **37**
- Runtime: 432s (7.2 min)

## Top 20 strict survivors (by Calmar)

| # | sym | tf | setup | session | inv | tp | sl | n | wr | pf | exp_R | dd_R | calmar |
|---|-----|-----|-------|---------|-----|-----|-----|---|-----|-----|-------|------|--------|
| 1 | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | False | 0.70 | 0.50 | 36 | 0.611 | 1.999 | 0.402 | 3.3 | 0.1218 |
| 2 | EURUSD | H1 | KAMA_CROSS_MOM | NY | True | 1.00 | 1.00 | 67 | 0.627 | 1.958 | 0.247 | 2.5 | 0.0988 |
| 3 | GBPAUD | H1 | KAMA_CROSS_MOM | ASIA | False | 1.00 | 1.00 | 41 | 0.610 | 1.827 | 0.207 | 3.2 | 0.0657 |
| 4 | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | False | 1.00 | 1.00 | 36 | 0.639 | 1.757 | 0.241 | 4.1 | 0.0586 |
| 5 | GBPUSD | M15 | KAMA_CROSS_MOM | ASIA | False | 1.00 | 1.00 | 123 | 0.610 | 1.735 | 0.216 | 4.4 | 0.0488 |
| 6 | GBPJPY | M15 | KAMA_CROSS_MOM | NY | False | 0.50 | 2.50 | 110 | 0.864 | 1.766 | 0.061 | 1.4 | 0.0452 |
| 7 | USDJPY | M15 | KAMA_CROSS_MOM | ASIA | False | 1.00 | 1.00 | 134 | 0.627 | 1.575 | 0.200 | 4.5 | 0.0445 |
| 8 | NATGAS | M15 | KAMA_CROSS_MOM | ASIA | True | 1.00 | 1.00 | 94 | 0.617 | 1.626 | 0.176 | 4.0 | 0.0437 |
| 9 | EURUSD | H1 | KAMA_CROSS_MOM | NY | True | 1.50 | 2.50 | 67 | 0.612 | 1.658 | 0.091 | 2.2 | 0.0411 |
| 10 | GBPJPY | H1 | SPECTRAL_TREND_MOM | LONDON_NY | False | 1.50 | 2.50 | 84 | 0.607 | 1.588 | 0.103 | 2.8 | 0.0372 |
| 11 | GBPAUD | H1 | KAMA_CROSS_MOM | ASIA | False | 1.00 | 2.00 | 41 | 0.610 | 1.665 | 0.090 | 2.5 | 0.0358 |
| 12 | AUDUSD | H1 | SPECTRAL_TREND_MOM | LONDON | False | 0.50 | 2.50 | 49 | 0.673 | 1.568 | 0.033 | 0.9 | 0.0347 |
| 13 | WTI | M15 | SPECTRAL_TREND_MOM | ASIA | False | 0.50 | 2.50 | 66 | 0.727 | 1.903 | 0.072 | 2.1 | 0.0343 |
| 14 | XAUUSD | H1 | KAMA_CROSS_MOM | LONDON_NY | True | 1.00 | 2.00 | 79 | 0.671 | 1.488 | 0.083 | 2.5 | 0.0335 |
| 15 | GBPUSD | M15 | KAMA_CROSS_MOM | ASIA | False | 1.00 | 2.00 | 123 | 0.642 | 1.427 | 0.080 | 2.6 | 0.0311 |
| 16 | USDJPY | M15 | KAMA_CROSS_MOM | ASIA | False | 1.50 | 2.50 | 134 | 0.657 | 1.463 | 0.102 | 3.4 | 0.0298 |
| 17 | EURUSD | M15 | SPECTRAL_TREND_MOM | NY | False | 1.00 | 2.00 | 160 | 0.738 | 1.604 | 0.123 | 4.3 | 0.0283 |
| 18 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | False | 0.50 | 2.50 | 118 | 0.814 | 1.704 | 0.085 | 3.0 | 0.0283 |
| 19 | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | False | 1.50 | 2.50 | 36 | 0.611 | 1.361 | 0.072 | 2.7 | 0.0266 |
| 20 | EURUSD | H1 | KAMA_CROSS_MOM | NY | True | 0.50 | 2.50 | 67 | 0.761 | 1.722 | 0.047 | 1.8 | 0.0261 |

## Distribution (raw survivors)

**K3-B raw** (n=874)
  - WR: p50=0.541  p75=0.623  p90=0.679  max=0.869
  - PF: p50=1.093  p75=1.231  p90=1.470  max=2.443

