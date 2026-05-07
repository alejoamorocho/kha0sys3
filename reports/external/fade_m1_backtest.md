# FADE M1 Backtest — bot live strategies
Generated: 2026-05-07T14:40:30.392755Z

## Per-strategy comparison (live vs M1/M15 backtest)

| sym | edge | magic | dur | tp | sl | tracking_tf | live_wr | bt_n | bt_wr | bt_pf | bt_dd_R | bt_calmar |
|-----|------|-------|-----|-----|-----|------------|---------|------|-------|-------|---------|----------|
| USOUSD | FADE_UP | 13:00 | 45 | 0.75 | 2.5 | M1 | 0.889 | 240 | 0.613 | 0.212 | 55.1 | -0.991 | DRIFT=27.65%
| UKOUSD | FADE_DOWN | 07:00 | 60 | 0.5 | 2.5 | M1 | 0.923 | 265 | 0.196 | 0.000 | 60.9 | -1.000 | DRIFT=72.68%
| USOUSD | FADE_UP | 13:00 | 60 | 0.75 | 2.5 | M1 | 0.892 | 289 | 0.567 | 0.191 | 69.6 | -0.997 | DRIFT=32.45%
| UKOUSD | FADE_DOWN | 07:00 | 45 | 0.5 | 2.5 | M1 | 0.926 | 171 | 0.193 | 0.000 | 28.4 | -1.000 | DRIFT=73.30%
| USOUSD | FADE_UP | 13:00 | 30 | 0.5 | 2.5 | M1 | 0.929 | 308 | 0.188 | 0.000 | 73.0 | -1.016 | DRIFT=74.07%
| UKOUSD | FADE_DOWN | 07:00 | 30 | 0.5 | 2.5 | M1 | 0.924 | 193 | 0.161 | 0.000 | 29.9 | -1.000 | DRIFT=76.34%

## Aggregate (all enabled FADE strategies)
- n_strategies: 6
- n_trades: 1466
- win_rate: 0.331
- profit_factor: 0.089
- expectancy_R: -0.217
- max_dd_R: 317.602
- calmar: -0.999
- total_R: -317.402

## Drift analysis (|live_wr - bt_wr| > 10pp)

| sym | edge | live_wr | bt_wr | diff |
|-----|------|---------|-------|------|
| USOUSD | FADE_UP | 0.889 | 0.613 | +0.276 |
| UKOUSD | FADE_DOWN | 0.923 | 0.196 | +0.727 |
| USOUSD | FADE_UP | 0.892 | 0.567 | +0.325 |
| UKOUSD | FADE_DOWN | 0.926 | 0.193 | +0.733 |
| USOUSD | FADE_UP | 0.929 | 0.188 | +0.741 |
| UKOUSD | FADE_DOWN | 0.924 | 0.161 | +0.763 |