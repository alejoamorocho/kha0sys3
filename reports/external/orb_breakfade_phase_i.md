# Phase I — High-WR R:R Grid Exploration

- Backtests: 784
- Survivors (WR>=0.6 AND PF>=1.3 AND n>=30): 0
- Runtime: 40s (0.7 min)
- ATR windows: [5, 10, 14, 20]
- TP grid: [0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0]
- SL grid: [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0]
- Total TP x SL combos: 49

## TOP 30 by Calmar

No survivors met WR>=0.60 AND PF>=1.30 AND n>=30.

## TOP 30 by PF

No survivors met WR>=0.60 AND PF>=1.30 AND n>=30.


## Best per Phase-G base seed (12 rows)

Each Phase G row is (sym, magic_time, dur, tp_g, sl_g). Best qualifier found
in Phase I grid for each seed's (sym, magic_time, dur) combo.

| # | sym | magic | dur | tp_g | sl_g | best_i_tp | best_i_sl | best_atr_w | n | WR | PF | calmar | note |
|---|-----|-------|-----|------|------|-----------|-----------|------------|---|-----|-----|--------|------|
| 1 | GBPAUD | 15:00 | 120m | 1.5 | 1.5 | — | — | — | — | — | — | — | no qualifier |
| 2 | GBPAUD | 15:00 | 120m | 2.0 | 1.5 | — | — | — | — | — | — | — | no qualifier |
| 3 | GBPAUD | 15:00 | 120m | 1.0 | 1.0 | — | — | — | — | — | — | — | no qualifier |
| 4 | GBPAUD | 15:00 | 120m | 1.0 | 1.5 | — | — | — | — | — | — | — | no qualifier |
| 5 | USDJPY | 15:00 | 120m | 1.0 | 1.0 | — | — | — | — | — | — | — | no qualifier |
| 6 | USDJPY | 15:00 | 120m | 1.5 | 1.5 | — | — | — | — | — | — | — | no qualifier |
| 7 | USDJPY | 15:00 | 120m | 2.0 | 1.5 | — | — | — | — | — | — | — | no qualifier |
| 8 | USDJPY | 15:00 | 120m | 1.0 | 1.5 | — | — | — | — | — | — | — | no qualifier |
| 9 | GBPAUD | 15:00 | 60m | 1.5 | 1.5 | — | — | — | — | — | — | — | no qualifier |
| 10 | GBPAUD | 15:00 | 60m | 1.0 | 1.5 | — | — | — | — | — | — | — | no qualifier |
| 11 | GBPAUD | 15:00 | 60m | 1.0 | 1.0 | — | — | — | — | — | — | — | no qualifier |
| 12 | GBPAUD | 13:30 | 120m | 1.5 | 1.5 | — | — | — | — | — | — | — | no qualifier |

## Closest-to-gate (informational, not survivors)

For each unique (sym, magic_time, duration) seed, the combo with minimum
Euclidean distance to (WR=0.60, PF=1.30) among ALL grid results.

| sym | magic | dur | atr_w | tp | sl | n | WR | PF | dist_to_gate |
|-----|-------|-----|-------|----|----|---|-----|-----|--------------|
| GBPAUD | 13:30 | 120m | 5 | 1.50 | 1.00 | 1836 | 0.467 | 1.089 | 0.2492 |
| GBPAUD | 15:00 | 60m | 14 | 0.50 | 0.50 | 2000 | 0.569 | 1.084 | 0.2178 |
| GBPAUD | 15:00 | 120m | 20 | 0.70 | 1.00 | 1844 | 0.655 | 1.107 | 0.2008 |
| USDJPY | 15:00 | 120m | 5 | 1.50 | 1.50 | 1743 | 0.545 | 1.051 | 0.2548 |

## Distribution of (WR, PF) across full grid

- Total grid results: 784
- WR: p10=0.384, p25=0.476, p50=0.559, p75=0.738, p90=0.822, max=0.902
- PF: p10=0.433, p25=0.741, p50=0.900, p75=0.999, p90=1.051, max=1.161

Rows with WR>=0.60 (regardless of PF):
  count=358
  PF of those: p50=0.794, p75=0.919, p90=0.985, max=1.107

Rows with PF>=1.30 (regardless of WR):
  count=0
