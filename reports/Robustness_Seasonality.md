# Robustness — Seasonality 3-Regime Optuna Portfolio

Tested on 9 strategies with optimised TP/SL.
Realistic Vantage friction + 0.2R slippage. MC=10000.

## Classification distribution

- **FUERTE**: 2
- **ACEPTABLE**: 1
- **DEBIL**: 2
- **MUERTA**: 4

## Aggregate (keepable = FUERTE + ACEPTABLE)

- N: 3
- Avg PF IS:  1.43
- Avg PF OOS: 1.96
- Avg MC ruin: 0.43%
- Sum net R: 783.4

## Per-strategy results

| Sym | UTC | Dir | Reg | TP/SL | RR | n | WR | PF | PF OOS | DegWR% | Ruin% | P5 | Decay | Label | Flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GBPAUD | 20:30 | SHORT | HIGH_WR | 1.10/1.20 | 0.92 | 2129 | 0.771 | 1.74 | 2.93 | -22.8 | 0.0 | +458.6 | MEJORANDO | **FUERTE** | - |
| GBPJPY | 20:30 | SHORT | HIGH_RR | 1.00/1.10 | 0.91 | 2130 | 0.735 | 1.36 | 1.72 | -12.5 | 0.2 | +258.2 | MEJORANDO | **FUERTE** | - |
| XAUUSD | 21:45 | LONG | BALANCED | 2.00/1.80 | 1.11 | 718 | 0.621 | 1.20 | 1.23 | -1.8 | 1.1 | +66.5 | ESTABLE | **ACEPTABLE** | - |
| XAGUSD | 21:30 | SHORT | BALANCED | 0.60/0.50 | 1.20 | 718 | 0.635 | 1.34 | 0.95 | +23.3 | 0.1 | +111.5 | DEGRADANDO | **DEBIL** | WF deg WR>15%,PF OOS<1,decay- |
| XAGUSD | 21:45 | LONG | HIGH_RR | 1.30/0.70 | 1.86 | 718 | 0.500 | 1.32 | 0.88 | +33.8 | 2.8 | +142.6 | DEGRADANDO | **DEBIL** | WF deg WR>15%,PF OOS<1,decay- |
| GBPJPY | 20:45 | SHORT | HIGH_RR | 1.10/0.80 | 1.38 | 2130 | 0.581 | 1.12 | 1.79 | -45.1 | 56.4 | +143.1 | MEJORANDO | **MUERTA** | ruin>5% |
| XAGUSD | 20:30 | SHORT | BALANCED | 0.80/0.60 | 1.33 | 2052 | 0.555 | 1.11 | 0.95 | +13.0 | 60.0 | +123.6 | DEGRADANDO | **MUERTA** | ruin>5%,PF OOS<1,decay- |
| GBPAUD | 20:45 | SHORT | HIGH_RR | 1.30/0.80 | 1.62 | 2129 | 0.502 | 1.04 | 1.66 | -59.7 | 99.1 | +51.0 | MEJORANDO | **MUERTA** | ruin>5% |
| EURJPY | 20:30 | SHORT | HIGH_RR | 1.20/1.00 | 1.20 | 2130 | 0.609 | 1.03 | 1.48 | -31.2 | 94.3 | +35.5 | MEJORANDO | **MUERTA** | ruin>5% |
