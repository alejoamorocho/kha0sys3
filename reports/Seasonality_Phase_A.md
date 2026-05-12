# Seasonality Phase A — Bucket Directional t-stat Screen

Universe: 9 symbols, 96 buckets/day (15-min wide).
Gate: |t-stat| > 2.5, n_obs >= 100.
Friction NOT applied here (raw next-bar log return only).

Total survivors: **137**

## Per-symbol survivor count

| Symbol | N buckets | Avg |t| | Avg n_obs |
|---|---|---|---|
| GBPAUD | 19 | 5.63 | 2125 |
| EURJPY | 18 | 4.35 | 2133 |
| USDJPY | 18 | 4.14 | 2134 |
| GBPJPY | 18 | 4.90 | 2132 |
| EURUSD | 17 | 4.14 | 2134 |
| AUDUSD | 15 | 5.30 | 2134 |
| GBPUSD | 13 | 4.51 | 2134 |
| XAGUSD | 11 | 6.33 | 1578 |
| XAUUSD | 8 | 4.09 | 1659 |

## Top 25 by |t-stat|

| # | Sym | Hour:Min UTC | Dir | n | mean_ret | t-stat | WR raw |
|---|---|---|---|---|---|---|---|
| 1 | GBPAUD | 20:30 | SHORT | 2130 | -0.000194 | -18.38 | 0.309 |
| 2 | XAGUSD | 20:30 | SHORT | 2053 | -0.000508 | -13.80 | 0.330 |
| 3 | XAGUSD | 21:30 | SHORT | 718 | -0.000673 | -13.52 | 0.263 |
| 4 | AUDUSD | 20:30 | SHORT | 2131 | -0.000118 | -12.45 | 0.354 |
| 5 | XAGUSD | 20:45 | LONG | 2053 | +0.000609 | +11.55 | 0.641 |
| 6 | AUDUSD | 22:45 | LONG | 2135 | +0.000132 | +11.06 | 0.608 |
| 7 | USDJPY | 20:30 | SHORT | 2131 | -0.000093 | -10.62 | 0.379 |
| 8 | GBPJPY | 20:45 | SHORT | 2131 | -0.000205 | -10.60 | 0.381 |
| 9 | EURJPY | 20:30 | SHORT | 2131 | -0.000089 | -10.46 | 0.379 |
| 10 | GBPAUD | 21:15 | LONG | 2113 | +0.000096 | +9.90 | 0.590 |
| 11 | GBPJPY | 20:30 | SHORT | 2131 | -0.000107 | -9.66 | 0.380 |
| 12 | EURUSD | 20:30 | SHORT | 2131 | -0.000061 | -9.24 | 0.380 |
| 13 | GBPUSD | 20:30 | SHORT | 2131 | -0.000086 | -9.09 | 0.368 |
| 14 | USDJPY | 21:30 | SHORT | 2132 | -0.000060 | -8.29 | 0.417 |
| 15 | GBPJPY | 21:15 | LONG | 2127 | +0.000068 | +8.22 | 0.587 |
| 16 | GBPAUD | 20:45 | SHORT | 2130 | -0.000116 | -7.93 | 0.426 |
| 17 | GBPAUD | 21:30 | SHORT | 2124 | -0.000079 | -7.88 | 0.436 |
| 18 | AUDUSD | 21:30 | SHORT | 2132 | -0.000059 | -7.47 | 0.435 |
| 19 | GBPUSD | 22:45 | LONG | 2134 | +0.000061 | +7.45 | 0.573 |
| 20 | GBPUSD | 21:30 | SHORT | 2132 | -0.000049 | -7.45 | 0.441 |
| 21 | EURJPY | 20:45 | SHORT | 2131 | -0.000117 | -6.85 | 0.416 |
| 22 | XAGUSD | 22:45 | LONG | 1364 | +0.000280 | +6.80 | 0.606 |
| 23 | XAUUSD | 20:45 | LONG | 2054 | +0.000204 | +6.79 | 0.607 |
| 24 | AUDUSD | 22:30 | SHORT | 2133 | -0.000065 | -6.74 | 0.410 |
| 25 | GBPAUD | 21:00 | LONG | 2068 | +0.000069 | +6.71 | 0.557 |
