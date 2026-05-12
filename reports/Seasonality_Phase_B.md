# Seasonality Phase B — TP/SL grid backtest with realistic friction

Friction = friction_real.friction_r + 0.2R slippage.
Grid: TP(0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0) x SL(0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0).
Gates: trades/yr >= 30.0, WR > 0.5, PF > 1.0, expectancy_R > 0.0.

Total survivors: **131**

Unique (sym, bucket, direction) tuples passing: **9**

## Per-symbol (best per bucket+dir)

| Symbol | N | Avg PF | Avg WR | Avg Exp(R) | Avg t/yr |
|---|---|---|---|---|---|
| XAGUSD | 3 | 1.24 | 0.538 | +0.137 | 142 |
| GBPJPY | 2 | 1.23 | 0.643 | +0.088 | 259 |
| GBPAUD | 2 | 1.36 | 0.630 | +0.143 | 259 |
| XAUUSD | 1 | 1.22 | 0.517 | +0.133 | 88 |
| EURJPY | 1 | 1.03 | 0.595 | +0.015 | 259 |

## Top 25 (sym, bucket, dir) by PF

| # | Sym | UTC | Dir | TP/SL | RR | n | WR | PF | Exp(R) | DD(R) | t/yr |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | GBPJPY | 20:45 | SHORT | 1.25/0.75 | 1.67 | 2130 | 0.522 | 1.11 | +0.070 | 323.7 | 259 |
| 2 | XAGUSD | 21:45 | LONG | 1.25/0.75 | 1.67 | 718 | 0.526 | 1.30 | +0.176 | 66.4 | 88 |
| 3 | GBPJPY | 20:30 | SHORT | 1.00/1.25 | 0.80 | 2130 | 0.765 | 1.35 | +0.105 | 27.3 | 259 |
| 4 | EURJPY | 20:30 | SHORT | 1.25/1.00 | 1.25 | 2130 | 0.595 | 1.03 | +0.015 | 213.8 | 259 |
| 5 | GBPAUD | 20:30 | SHORT | 1.25/1.00 | 1.25 | 2129 | 0.690 | 1.70 | +0.277 | 53.5 | 259 |
| 6 | GBPAUD | 20:45 | SHORT | 1.25/1.00 | 1.25 | 2129 | 0.570 | 1.02 | +0.009 | 330.8 | 259 |
| 7 | XAGUSD | 20:30 | SHORT | 0.75/0.50 | 1.50 | 2052 | 0.522 | 1.11 | +0.063 | 134.9 | 250 |
| 8 | XAUUSD | 21:45 | LONG | 1.25/0.75 | 1.67 | 718 | 0.517 | 1.22 | +0.133 | 23.8 | 88 |
| 9 | XAGUSD | 21:30 | SHORT | 0.75/0.50 | 1.50 | 718 | 0.565 | 1.32 | +0.172 | 42.4 | 88 |
