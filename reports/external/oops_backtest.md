# OOPS backtest report

**Generated:** 2026-05-06T22:41:05.673477Z
**Symbols:** SP500, NASDAQ100
**Period:** 2018-01-01..today
**Risk per trade:** 0.50%

## Comparativa modos de exit

| metric | doc | atr | indicator |
|--------|--------|--------|--------|
| n_trades | 124 | 113 | 124 |
| win_rate | 0.161 | 0.097 | 0.177 |
| profit_factor | 0.202 | 0.140 | 0.395 |
| expectancy_R | -0.732 | -0.230 | -0.532 |
| avg_win_R | 1.146 | 0.386 | 1.956 |
| avg_loss_R | -1.093 | -0.296 | -1.068 |
| max_dd_R | 89.592 | 25.911 | 64.756 |
| sharpe | -0.804 | -0.664 | -0.265 |
| sortino | -1.803 | -0.879 | -0.941 |
| calmar | -1.013 | -1.002 | -1.019 |
| total_R | -90.793 | -25.958 | -65.957 |

## Breakdown por activo (modo doc)

| symbol | n | wr | pf | exp_R | dd_R | calmar |
|--------|---|-----|-----|-------|------|--------|
| SP500 | 61 | 0.164 | 0.214 | -0.762 | 45.245 | -1.027 |
| NASDAQ100 | 63 | 0.159 | 0.189 | -0.704 | 43.140 | -1.028 |

## Walk-forward (modo doc)

| window | IS n | IS pf | IS wr | OOS n | OOS pf | OOS wr |
|--------|------|-------|-------|-------|--------|--------|
| 1 | 16 | 0.149 | 0.125 | 8 | 0.338 | 0.250 |
| 2 | 16 | 0.435 | 0.312 | 8 | 0.000 | 0.000 |
| 3 | 16 | 0.310 | 0.250 | 8 | 0.367 | 0.250 |
| 4 | 16 | 0.262 | 0.188 | 8 | 0.238 | 0.125 |
| 5 | 16 | 0.000 | 0.000 | 8 | 0.139 | 0.125 |

## Monte Carlo (modo doc, 10k bootstrap)

| metric | value |
|--------|-------|
| prob_ruin | 1.000 |
| dd_q5_R | 90.793 |
| dd_q50_R | 90.793 |
| dd_q95_R | 93.680 |
| final_q5_R | -90.793 |
| final_q50_R | -90.793 |
| final_q95_R | -90.793 |
| n_simulations | 10000 |
