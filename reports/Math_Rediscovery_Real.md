# Math Rediscovery — REAL Broker Friction

- Phase A passers (PF>=1.25, WR>=0.55, trades/yr>=60, exp>=0.05R): **5603**
- Phase B validated (WF>=0.80, MC<=0.02, decay>=0.60): **4554**
- Phase C portfolio (session-disjoint, caps): **22**

Grid: TP(0.3..2.0 x7) x SL(0.75..2.5 x5) = 35 combos,
families = FADE (6 setups) + MOMENTUM (6 setups),
direction = NORMAL + INVERT (tested in parallel),
universe = 15 symbols x 5 sessions on 3y+ M15 cache.

Friction: per-symbol USD per round-turn at vol_min, converted to R via
`friction_r = usd / (sl * median_atr * tick_val/tick_size * vol_min)`.

## Top 15 by Net R (Phase B validated)

| # | Sym | Session | Setup | Dir | Fam | TP | SL | Fric_R | Trd | WR | PF | Exp(R) | NetR | T/yr | WF | MC | Dec |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | XAGUSD | ALL_DAY | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.028 | 2169 | 0.616 | 3.03 | 0.789 | 1711.6 | 263.8 | 1.00 | 0.000 | 0.70 |
| 2 | XAGUSD | ALL_DAY | OLS_SLOPE_STRONG | INVERT | MOM | 1.25 | 0.75 | 0.028 | 2169 | 0.668 | 3.19 | 0.735 | 1594.9 | 263.8 | 1.00 | 0.000 | 0.76 |
| 3 | XAGUSD | ALL_DAY | OLS_SLOPE_STRONG | INVERT | MOM | 1.0 | 0.75 | 0.028 | 2169 | 0.727 | 3.41 | 0.663 | 1438.4 | 263.8 | 1.00 | 0.000 | 0.76 |
| 4 | XAGUSD | LONDON_NY | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.028 | 1856 | 0.600 | 2.79 | 0.726 | 1348.2 | 226.0 | 1.00 | 0.000 | 0.73 |
| 5 | GBPUSD | ALL_DAY | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.111 | 2198 | 0.580 | 2.32 | 0.613 | 1346.6 | 267.4 | 1.01 | 0.000 | 0.99 |
| 6 | WTI | ALL_DAY | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.064 | 2224 | 0.561 | 2.26 | 0.580 | 1289.4 | 270.7 | 1.01 | 0.000 | 0.83 |
| 7 | BRENT | ALL_DAY | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.061 | 2088 | 0.559 | 2.29 | 0.599 | 1250.3 | 254.1 | 1.00 | 0.000 | 0.81 |
| 8 | BRENT | ALL_DAY | OLS_SLOPE_STRONG | INVERT | MOM | 1.25 | 0.75 | 0.061 | 2088 | 0.625 | 2.49 | 0.593 | 1237.8 | 254.1 | 1.00 | 0.000 | 0.71 |
| 9 | WTI | ALL_DAY | OLS_SLOPE_STRONG | INVERT | MOM | 1.25 | 0.75 | 0.064 | 2224 | 0.616 | 2.38 | 0.556 | 1237.4 | 270.7 | 1.00 | 0.000 | 0.63 |
| 10 | XAGUSD | ALL_DAY | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 1.0 | 0.021 | 2169 | 0.644 | 2.59 | 0.567 | 1228.9 | 263.8 | 1.00 | 0.000 | 0.66 |
| 11 | XAGUSD | LONDON_NY | OLS_SLOPE_STRONG | INVERT | MOM | 1.25 | 0.75 | 0.028 | 1856 | 0.643 | 2.83 | 0.661 | 1227.4 | 226.0 | 1.00 | 0.000 | 0.81 |
| 12 | EURUSD | ALL_DAY | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.153 | 2181 | 0.570 | 2.13 | 0.554 | 1207.3 | 265.5 | 1.01 | 0.000 | 1.01 |
| 13 | GBPUSD | ALL_DAY | OLS_SLOPE_STRONG | INVERT | MOM | 1.25 | 0.75 | 0.111 | 2198 | 0.625 | 2.33 | 0.549 | 1206.1 | 267.4 | 1.01 | 0.000 | 1.03 |
| 14 | XAUUSD | ALL_DAY | OLS_SLOPE_STRONG | INVERT | MOM | 1.25 | 0.75 | 0.045 | 2162 | 0.607 | 2.37 | 0.557 | 1204.9 | 263.0 | 1.01 | 0.000 | 0.68 |
| 15 | GBPJPY | ALL_DAY | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.121 | 2216 | 0.560 | 2.10 | 0.542 | 1200.1 | 269.6 | 1.00 | 0.000 | 0.80 |

## Final Diversified Portfolio

| # | Sym | Session | Setup | Dir | Fam | TP | SL | WR | PF | Exp(R) | NetR | T/yr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | XAGUSD | ALL_DAY | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.616 | 3.03 | 0.789 | 1711.6 | 263.8 |
| 2 | WTI | NY | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.569 | 2.33 | 0.596 | 1053.0 | 214.9 |
| 3 | BRENT | NY | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.585 | 2.47 | 0.626 | 1029.1 | 200.0 |
| 4 | AUDUSD | LONDON_NY | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.566 | 1.98 | 0.488 | 887.3 | 221.4 |
| 5 | EURJPY | NY | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.610 | 2.34 | 0.578 | 869.2 | 183.0 |
| 6 | EURUSD | LONDON | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.590 | 2.23 | 0.556 | 868.8 | 190.1 |
| 7 | XAUUSD | LONDON | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.594 | 2.53 | 0.635 | 810.8 | 155.5 |
| 8 | GBPAUD | NY | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.580 | 2.26 | 0.560 | 808.1 | 175.7 |
| 9 | XAUUSD | ASIA | HURST_TREND_MOM | INVERT | MOM | 1.5 | 0.75 | 0.559 | 2.26 | 0.565 | 611.0 | 131.6 |
| 10 | GBPJPY | ASIA | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.569 | 2.15 | 0.544 | 583.4 | 130.7 |
| 11 | AUDUSD | ASIA | KALMAN_INNOV_EXPAND | INVERT | MOM | 1.25 | 0.75 | 0.576 | 1.75 | 0.361 | 582.6 | 196.4 |
| 12 | EURUSD | ASIA | HURST_TREND_MOM | INVERT | MOM | 1.5 | 0.75 | 0.583 | 2.14 | 0.539 | 557.0 | 125.7 |
| 13 | GBPUSD | ASIA | OLS_SLOPE_STRONG | INVERT | MOM | 1.5 | 0.75 | 0.626 | 2.73 | 0.723 | 543.1 | 91.5 |
| 14 | USDJPY | NY | HURST_TREND_MOM | INVERT | MOM | 1.5 | 0.75 | 0.559 | 1.80 | 0.406 | 539.2 | 161.6 |
| 15 | XAUUSD | NY | GARCH_Z_FADE | NORMAL | FADE | 1.25 | 0.75 | 0.584 | 2.15 | 0.486 | 488.6 | 122.7 |
| 16 | USDJPY | ASIA | KALMAN_INNOV_EXPAND | INVERT | MOM | 1.25 | 0.75 | 0.566 | 1.56 | 0.287 | 451.8 | 191.8 |
| 17 | BRENT | ASIA | HURST_TREND_MOM | INVERT | MOM | 1.25 | 0.75 | 0.636 | 2.69 | 0.604 | 445.9 | 90.0 |
| 18 | WTI | ASIA | HURST_TREND_MOM | INVERT | MOM | 1.5 | 0.75 | 0.584 | 2.35 | 0.569 | 395.6 | 84.7 |
| 19 | GBPUSD | NY | VELOCITY_ACCEL_GO | INVERT | MOM | 1.0 | 0.75 | 0.566 | 1.44 | 0.209 | 350.6 | 204.5 |
| 20 | GBPUSD | LONDON | GARCH_Z_FADE | NORMAL | FADE | 1.25 | 0.75 | 0.574 | 1.82 | 0.381 | 339.5 | 108.7 |
| 21 | GBPJPY | NY | GARCH_Z_FADE | NORMAL | FADE | 1.25 | 0.75 | 0.556 | 1.64 | 0.308 | 180.1 | 71.2 |
| 22 | EURJPY | LONDON | GARCH_Z_FADE | NORMAL | FADE | 1.0 | 0.75 | 0.607 | 1.55 | 0.247 | 163.2 | 80.6 |
