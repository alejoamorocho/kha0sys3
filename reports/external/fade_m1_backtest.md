# FADE M1 Backtest — bot live strategies
Generated: 2026-05-07T13:35:29.784406Z

## Per-strategy comparison (live vs M1/M15 backtest)

| sym | edge | magic | dur | tp | sl | tracking_tf | live_wr | bt_n | bt_wr | bt_pf | bt_dd_R | bt_calmar |
|-----|------|-------|-----|-----|-----|------------|---------|------|-------|-------|---------|----------|
| USOUSD | FADE_UP | 13:00 | 45 | 0.75 | 2.5 | M1 | 0.889 | 1534 | 0.531 | 0.098 | 417.3 | -0.999 | DRIFT=35.84%
| UKOUSD | FADE_DOWN | 07:00 | 60 | 0.5 | 2.5 | M1 | 0.923 | 1450 | 0.000 | 0.000 | 369.8 | -1.000 | DRIFT=92.30%
| USOUSD | FADE_UP | 13:00 | 60 | 0.75 | 2.5 | M1 | 0.892 | 1445 | 0.486 | 0.094 | 390.5 | -0.999 | DRIFT=40.62%
| UKOUSD | FADE_DOWN | 07:00 | 45 | 0.5 | 2.5 | M1 | 0.926 | 1355 | 0.000 | 0.000 | 339.2 | -1.001 | DRIFT=92.60%
| USOUSD | FADE_UP | 13:00 | 30 | 0.5 | 2.5 | M1 | 0.929 | 1598 | 0.000 | 0.000 | 422.8 | -1.000 | DRIFT=92.90%
| UKOUSD | FADE_DOWN | 07:00 | 30 | 0.5 | 2.5 | M1 | 0.924 | 1113 | 0.000 | 0.000 | 283.7 | -1.004 | DRIFT=92.40%

## Aggregate (all enabled FADE strategies)
- n_strategies: 6
- n_trades: 8495
- win_rate: 0.178
- profit_factor: 0.037
- expectancy_R: -0.262
- max_dd_R: 2224.351
- calmar: -1.000
- total_R: -2224.047

## Drift analysis (|live_wr - bt_wr| > 10pp)

| sym | edge | live_wr | bt_wr | diff |
|-----|------|---------|-------|------|
| USOUSD | FADE_UP | 0.889 | 0.531 | +0.358 |
| UKOUSD | FADE_DOWN | 0.923 | 0.000 | +0.923 |
| USOUSD | FADE_UP | 0.892 | 0.486 | +0.406 |
| UKOUSD | FADE_DOWN | 0.926 | 0.000 | +0.926 |
| USOUSD | FADE_UP | 0.929 | 0.000 | +0.929 |
| UKOUSD | FADE_DOWN | 0.924 | 0.000 | +0.924 |