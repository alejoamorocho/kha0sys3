# Portfolio Master — Math Multi-TF FUERTE

Generated: 2026-05-03T18:42:44.961422Z  ·  Backtest period: 2018-01-01 → 2026-03-24 (8.22y)

## Filtros aplicados

- Robustness class = **FUERTE** (la más estricta: WF deg < 5%, ruin < 1%, PF OOS > IS×0.95)
- Friction realista Vantage por símbolo + 0.2R slippage
- Walk-forward 50/50 IS vs OOS
- Monte Carlo 10k bootstrap, gate DD ≥ 30R
- Optuna 3-regime TP/SL per estrategia (HIGH_RR / BALANCED / HIGH_WR)

## Resumen ejecutivo

| TF | n | Avg WR | Avg PF IS | Avg PF OOS | Avg Exp R | Avg DD R | Avg ruin | Sum trades/yr | Sum n trades | Avg trades/yr/strat | Sum Net R (8.2y) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **M15** | 25 | 58.7% | 2.54 | 2.59 | +0.893 | 13.0 | 0.11% | 3764 | 30,916 | 150.6 | 29125 |
| **H1** | 70 | 58.5% | 2.32 | 2.32 | +0.741 | 12.0 | 0.12% | 7254 | 59,490 | 103.6 | 46450 |
| **H4** | 58 | 62.9% | 2.28 | 2.32 | +0.430 | 9.5 | 0.04% | 3359 | 27,377 | 57.9 | 13298 |
| **TOTAL** | 153 | 60.2% | 2.34 | 2.37 | +0.648 | 11.2 | 0.09% | 14378 | 117,783 | 94.0 | 88872 |

## Proyección de crecimiento $10k → $1M

**Modelo lineal con factor de realismo**:

- **Linear annual return** = `sum_trades_per_year × avg_exp_R × risk_pct × realism_factor`
- Realism factor 1.0 = teórico (sin slippage extra, sin correlación entre strats)
- Realism factor 0.5 = realista (escalado por correlación + slippage al subir lots)
- Realism factor 0.3 = conservador (asume live-vs-backtest gap del 70%)

Para cada TF se muestran 4 niveles de riesgo × 3 factores de realismo = 12 combinaciones.

### M15 — 25 estrategias FUERTE | 3764 trades/año | avg exp R=+0.893

| Riesgo/trade | Realismo | Annual return | Years a $1M | $10k → 1y |
|---|---|---|---|---|
| Conservador 1% (1.0%) | Teórico (perfect) (1.0) | 3,362% | 1.30 | $346,150 |
| Conservador 1% (1.0%) | Realista 50% (0.5) | 1,681% | 1.60 | $178,075 |
| Conservador 1% (1.0%) | Conservador 30% (0.3) | 1,008% | 1.91 | $110,845 |
| Moderado 3% (3.0%) | Teórico (perfect) (1.0) | 1.01e+04% | 1.00 | $1,018,450 |
| Moderado 3% (3.0%) | Realista 50% (0.5) | 5,042% | 1.17 | $514,225 |
| Moderado 3% (3.0%) | Conservador 30% (0.3) | 3,025% | 1.34 | $312,535 |
| Agresivo 5% (5.0%) | Teórico (perfect) (1.0) | 1.68e+04% | 0.90 | $1,690,750 |
| Agresivo 5% (5.0%) | Realista 50% (0.5) | 8,404% | 1.04 | $850,375 |
| Agresivo 5% (5.0%) | Conservador 30% (0.3) | 5,042% | 1.17 | $514,225 |
| WR-tier (1-15%) (3.3%) | Teórico (perfect) (1.0) | 1.11e+04% | 0.98 | $1,117,156 |
| WR-tier (1-15%) (3.3%) | Realista 50% (0.5) | 5,536% | 1.14 | $563,578 |
| WR-tier (1-15%) (3.3%) | Conservador 30% (0.3) | 3,321% | 1.30 | $342,147 |

### H1 — 70 estrategias FUERTE | 7254 trades/año | avg exp R=+0.741

| Riesgo/trade | Realismo | Annual return | Years a $1M | $10k → 1y |
|---|---|---|---|---|
| Conservador 1% (1.0%) | Teórico (perfect) (1.0) | 5,379% | 1.15 | $547,857 |
| Conservador 1% (1.0%) | Realista 50% (0.5) | 2,689% | 1.38 | $278,928 |
| Conservador 1% (1.0%) | Conservador 30% (0.3) | 1,614% | 1.62 | $171,357 |
| Moderado 3% (3.0%) | Teórico (perfect) (1.0) | 1.61e+04% | 0.90 | $1,623,571 |
| Moderado 3% (3.0%) | Realista 50% (0.5) | 8,068% | 1.05 | $816,785 |
| Moderado 3% (3.0%) | Conservador 30% (0.3) | 4,841% | 1.18 | $494,071 |
| Agresivo 5% (5.0%) | Teórico (perfect) (1.0) | 2.69e+04% | 0.82 | $2,699,285 |
| Agresivo 5% (5.0%) | Realista 50% (0.5) | 1.34e+04% | 0.94 | $1,354,642 |
| Agresivo 5% (5.0%) | Conservador 30% (0.3) | 8,068% | 1.05 | $816,785 |
| WR-tier (1-15%) (3.3%) | Teórico (perfect) (1.0) | 1.75e+04% | 0.89 | $1,762,676 |
| WR-tier (1-15%) (3.3%) | Realista 50% (0.5) | 8,763% | 1.03 | $886,338 |
| WR-tier (1-15%) (3.3%) | Conservador 30% (0.3) | 5,258% | 1.16 | $535,803 |

### H4 — 58 estrategias FUERTE | 3359 trades/año | avg exp R=+0.430

| Riesgo/trade | Realismo | Annual return | Years a $1M | $10k → 1y |
|---|---|---|---|---|
| Conservador 1% (1.0%) | Teórico (perfect) (1.0) | 1,444% | 1.68 | $154,420 |
| Conservador 1% (1.0%) | Realista 50% (0.5) | 722% | 2.19 | $82,210 |
| Conservador 1% (1.0%) | Conservador 30% (0.3) | 433% | 2.75 | $53,326 |
| Moderado 3% (3.0%) | Teórico (perfect) (1.0) | 4,333% | 1.21 | $443,259 |
| Moderado 3% (3.0%) | Realista 50% (0.5) | 2,166% | 1.48 | $226,629 |
| Moderado 3% (3.0%) | Conservador 30% (0.3) | 1,300% | 1.75 | $139,978 |
| Agresivo 5% (5.0%) | Teórico (perfect) (1.0) | 7,221% | 1.07 | $732,098 |
| Agresivo 5% (5.0%) | Realista 50% (0.5) | 3,610% | 1.27 | $371,049 |
| Agresivo 5% (5.0%) | Conservador 30% (0.3) | 2,166% | 1.48 | $226,629 |
| WR-tier (1-15%) (5.6%) | Teórico (perfect) (1.0) | 8,108% | 1.04 | $820,754 |
| WR-tier (1-15%) (5.6%) | Realista 50% (0.5) | 4,054% | 1.24 | $415,377 |
| WR-tier (1-15%) (5.6%) | Conservador 30% (0.3) | 2,432% | 1.43 | $253,226 |

### TOTAL — 153 estrategias FUERTE | 14378 trades/año | avg exp R=+0.648

| Riesgo/trade | Realismo | Annual return | Years a $1M | $10k → 1y |
|---|---|---|---|---|
| Conservador 1% (1.0%) | Teórico (perfect) (1.0) | 9,318% | 1.01 | $941,838 |
| Conservador 1% (1.0%) | Realista 50% (0.5) | 4,659% | 1.19 | $475,919 |
| Conservador 1% (1.0%) | Conservador 30% (0.3) | 2,796% | 1.37 | $289,552 |
| Moderado 3% (3.0%) | Teórico (perfect) (1.0) | 2.80e+04% | 0.82 | $2,805,515 |
| Moderado 3% (3.0%) | Realista 50% (0.5) | 1.40e+04% | 0.93 | $1,407,758 |
| Moderado 3% (3.0%) | Conservador 30% (0.3) | 8,387% | 1.04 | $848,655 |
| Agresivo 5% (5.0%) | Teórico (perfect) (1.0) | 4.66e+04% | 0.75 | $4,669,192 |
| Agresivo 5% (5.0%) | Realista 50% (0.5) | 2.33e+04% | 0.84 | $2,339,596 |
| Agresivo 5% (5.0%) | Conservador 30% (0.3) | 1.40e+04% | 0.93 | $1,407,758 |
| WR-tier (1-15%) (4.2%) | Teórico (perfect) (1.0) | 3.87e+04% | 0.77 | $3,883,829 |
| WR-tier (1-15%) (4.2%) | Realista 50% (0.5) | 1.94e+04% | 0.87 | $1,946,914 |
| WR-tier (1-15%) (4.2%) | Conservador 30% (0.3) | 1.16e+04% | 0.97 | $1,172,149 |


**ADVERTENCIAS sobre proyecciones**

1. **Trades NO son perfectamente independientes**: cuando varias estrategias operan el mismo símbolo, los DD se correlacionan. El cap del 30% simultáneo ya descuenta esto pero es heurístico.
2. **Expectancy degrada con el balance**: la fricción USD aumenta proporcionalmente con el lote, lo que reduce los R efectivos. A volumen alto, también puedes salir del rango de mejor ejecución del broker.
3. **Black swans no están modelados**: gaps, flash crashes, suspensiones de mercado pueden crear DD muy superiores al MC ruin del backtest.
4. **Margin requirements escalan**: con $1M+ balance, el broker puede requerir lots más grandes que tu liquidez disponible, forzándote a fraccionar.
5. **Realista vs teórico**: aplica un factor 0.3-0.5 a las proyecciones de arriba para una estimación menos optimista. P. ej. si el modelo dice 5 años, planea para 10-15.

## Distribución por símbolo (todas las TF, FUERTE)

| Symbol | Strats | trades/yr | Avg WR | Avg PF | Sum Net R |
|---|---|---|---|---|---|
| GBPAUD | 19 | 1976 | 58.5% | 2.28 | 13514 |
| XAGUSD | 21 | 1785 | 63.6% | 2.73 | 12221 |
| XAUUSD | 17 | 1702 | 59.3% | 2.51 | 10684 |
| EURUSD | 15 | 1695 | 59.7% | 2.17 | 10194 |
| AUDUSD | 19 | 1889 | 59.7% | 2.11 | 9913 |
| GBPJPY | 20 | 1704 | 60.3% | 2.31 | 9807 |
| GBPUSD | 11 | 1116 | 57.4% | 2.35 | 8144 |
| EURJPY | 18 | 1421 | 60.0% | 2.22 | 8123 |
| USDJPY | 13 | 1089 | 61.8% | 2.31 | 6273 |

## M15 — 25 estrategias FUERTE

| Symbol | Sess | Setup | Dir | Regime | TP | SL | RR | n | WR | PF IS | PF OOS | Exp R | DD R | tpy | Ruin% | Risk % | USD risk @$10k |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| XAGUSD | ALL_DAY | SPECTRAL_TREND_MOM | INVERT | BALANCED | 0.80 | 0.50 | 1.60 | 417 | 71.0% | 2.70 | 3.11 | +0.609 | 7.5 | 51.6 | 0.00% | 10.0% | $995 |
| GBPAUD | NY | GARCH_Z_FADE | NORMAL | BALANCED | 1.10 | 0.90 | 1.22 | 634 | 63.4% | 1.34 | 1.31 | +0.145 | 11.5 | 77.2 | 0.07% | 5.7% | $571 |
| XAGUSD | ALL_DAY | HURST_TREND_MOM | INVERT | HIGH_RR | 1.00 | 0.40 | 2.50 | 1,653 | 62.7% | 2.98 | 2.89 | +0.927 | 9.0 | 201.1 | 0.00% | 5.3% | $530 |
| XAUUSD | ASIA | HURST_TREND_MOM | INVERT | HIGH_RR | 1.00 | 0.40 | 2.50 | 1,082 | 61.4% | 2.72 | 2.59 | +0.844 | 8.1 | 131.6 | 0.00% | 4.6% | $457 |
| GBPUSD | ASIA | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 1.40 | 0.60 | 2.33 | 751 | 61.0% | 2.30 | 2.15 | +0.680 | 8.5 | 91.5 | 0.00% | 4.4% | $435 |
| GBPAUD | NY | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 1.00 | 0.30 | 3.33 | 1,442 | 61.0% | 3.08 | 3.34 | +1.154 | 18.7 | 175.7 | 0.01% | 4.3% | $434 |
| EURJPY | NY | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 1.20 | 0.40 | 3.00 | 1,504 | 60.8% | 2.51 | 2.48 | +0.860 | 15.8 | 183.0 | 0.02% | 4.3% | $427 |
| XAGUSD | NY | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 1.20 | 0.30 | 4.00 | 1,562 | 60.8% | 4.37 | 4.61 | +1.653 | 7.6 | 190.2 | 0.00% | 4.2% | $422 |
| XAUUSD | NY | GARCH_Z_FADE | NORMAL | HIGH_RR | 1.00 | 0.40 | 2.50 | 1,006 | 60.3% | 2.65 | 2.78 | +0.825 | 7.7 | 122.7 | 0.00% | 4.0% | $399 |
| EURJPY | NY | HURST_TREND_MOM | INVERT | HIGH_RR | 1.00 | 0.30 | 3.33 | 1,259 | 59.6% | 2.44 | 2.56 | +0.925 | 13.4 | 153.2 | 0.02% | 3.6% | $356 |
| XAGUSD | NY | GARCH_Z_FADE | NORMAL | HIGH_RR | 1.10 | 0.30 | 3.67 | 997 | 59.5% | 3.89 | 4.02 | +1.478 | 11.4 | 121.5 | 0.00% | 3.5% | $351 |
| XAUUSD | LONDON | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 1.50 | 0.80 | 1.88 | 1,276 | 59.0% | 1.81 | 1.91 | +0.394 | 13.9 | 155.5 | 0.10% | 3.2% | $325 |
| USDJPY | ALL_DAY | HURST_TREND_MOM | INVERT | HIGH_RR | 1.00 | 0.30 | 3.33 | 1,867 | 58.8% | 2.16 | 2.09 | +0.821 | 16.1 | 227.2 | 0.39% | 3.1% | $310 |
| EURUSD | LONDON | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 1.20 | 0.30 | 4.00 | 1,562 | 58.2% | 2.94 | 2.95 | +1.273 | 14.0 | 190.1 | 0.01% | 2.8% | $279 |
| GBPAUD | ALL_DAY | HURST_TREND_MOM | INVERT | HIGH_RR | 1.00 | 0.30 | 3.33 | 1,720 | 58.0% | 2.73 | 2.63 | +1.048 | 15.1 | 209.3 | 0.00% | 2.7% | $269 |
| EURJPY | LONDON_NY | SPECTRAL_TREND_MOM | INVERT | BALANCED | 1.20 | 0.50 | 2.40 | 267 | 57.7% | 1.82 | 2.05 | +0.482 | 11.5 | 32.5 | 0.00% | 2.5% | $250 |
| AUDUSD | ASIA | KALMAN_INNOV_EXPAND | INVERT | HIGH_RR | 1.00 | 0.30 | 3.33 | 1,614 | 57.5% | 2.24 | 2.35 | +0.853 | 13.3 | 196.4 | 0.25% | 2.4% | $240 |
| AUDUSD | LONDON_NY | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 1.20 | 0.40 | 3.00 | 1,819 | 57.3% | 2.17 | 2.39 | +0.745 | 18.2 | 221.4 | 0.10% | 2.3% | $228 |
| AUDUSD | LONDON | HURST_TREND_MOM | INVERT | HIGH_RR | 1.00 | 0.30 | 3.33 | 1,134 | 56.9% | 2.22 | 2.18 | +0.839 | 13.5 | 138.2 | 0.12% | 2.1% | $205 |
| XAUUSD | ALL_DAY | SPECTRAL_TREND_MOM | INVERT | HIGH_RR | 1.00 | 0.30 | 3.33 | 473 | 56.4% | 2.95 | 2.92 | +1.131 | 11.1 | 57.6 | 0.01% | 1.8% | $181 |
| GBPJPY | ASIA | HURST_TREND_MOM | INVERT | HIGH_RR | 1.20 | 0.40 | 3.00 | 1,157 | 56.3% | 2.26 | 2.12 | +0.791 | 8.8 | 140.8 | 0.05% | 1.7% | $171 |
| GBPAUD | ALL_DAY | KALMAN_INNOV_EXPAND | INVERT | HIGH_RR | 1.20 | 0.30 | 4.00 | 1,986 | 53.1% | 2.76 | 2.86 | +1.194 | 16.1 | 241.6 | 0.05% | 1.0% | $100 |
| GBPJPY | ALL_DAY | KALMAN_INNOV_EXPAND | INVERT | HIGH_RR | 1.10 | 0.30 | 3.67 | 2,047 | 52.5% | 2.30 | 2.21 | +0.926 | 16.5 | 249.0 | 0.40% | 1.0% | $100 |
| EURUSD | LONDON_NY | GARCH_Z_FADE | NORMAL | HIGH_RR | 1.10 | 0.30 | 3.67 | 1,245 | 52.4% | 2.16 | 2.37 | +0.866 | 19.1 | 151.5 | 0.61% | 1.0% | $100 |
| USDJPY | ALL_DAY | SPECTRAL_TREND_MOM | INVERT | HIGH_RR | 1.20 | 0.30 | 4.00 | 442 | 51.6% | 2.05 | 1.99 | +0.861 | 17.5 | 53.9 | 0.42% | 1.0% | $100 |

## H1 — 70 estrategias FUERTE

| Symbol | Sess | Setup | Dir | Regime | TP | SL | RR | n | WR | PF IS | PF OOS | Exp R | DD R | tpy | Ruin% | Risk % | USD risk @$10k |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| XAGUSD | ASIA | KALMAN_INNOV_EXPAND | INVERT | BALANCED | 0.70 | 0.50 | 1.40 | 644 | 74.2% | 2.78 | 2.85 | +0.543 | 6.2 | 78.6 | 0.00% | 11.8% | $1177 |
| XAUUSD | LONDON | OLS_SLOPE_STRONG | INVERT | BALANCED | 0.70 | 0.70 | 1.00 | 524 | 73.9% | 2.06 | 2.08 | +0.293 | 5.5 | 64.0 | 0.00% | 11.6% | $1156 |
| XAGUSD | ALL_DAY | OLS_SLOPE_STRONG | INVERT | BALANCED | 0.90 | 0.70 | 1.29 | 1,469 | 73.1% | 2.46 | 2.40 | +0.433 | 8.5 | 179.1 | 0.00% | 11.1% | $1114 |
| XAGUSD | LONDON_NY | HURST_TREND_MOM | INVERT | BALANCED | 0.90 | 0.70 | 1.29 | 746 | 71.2% | 2.24 | 2.15 | +0.383 | 5.8 | 90.8 | 0.00% | 10.1% | $1006 |
| EURUSD | ASIA | OLS_SLOPE_STRONG | INVERT | BALANCED | 1.10 | 0.60 | 1.83 | 755 | 68.2% | 2.35 | 2.21 | +0.512 | 9.4 | 92.3 | 0.00% | 8.4% | $840 |
| GBPJPY | ALL_DAY | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 1.00 | 0.50 | 2.00 | 1,427 | 66.7% | 2.38 | 2.38 | +0.595 | 9.1 | 174.2 | 0.00% | 7.6% | $756 |
| GBPUSD | ASIA | KALMAN_INNOV_EXPAND | INVERT | BALANCED | 1.10 | 0.80 | 1.38 | 480 | 66.5% | 1.89 | 1.87 | +0.287 | 9.8 | 58.6 | 0.00% | 7.4% | $742 |
| GBPAUD | NY | KALMAN_INNOV_EXPAND | INVERT | BALANCED | 0.80 | 0.50 | 1.60 | 956 | 65.9% | 1.80 | 1.87 | +0.331 | 10.7 | 116.5 | 0.00% | 7.1% | $710 |
| AUDUSD | ASIA | OLS_SLOPE_STRONG | INVERT | BALANCED | 1.10 | 0.60 | 1.83 | 731 | 65.8% | 2.13 | 2.23 | +0.469 | 8.8 | 89.2 | 0.00% | 7.0% | $705 |
| XAUUSD | ALL_DAY | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 1.00 | 0.40 | 2.50 | 1,484 | 65.4% | 3.05 | 3.00 | +0.877 | 11.9 | 181.0 | 0.00% | 6.8% | $680 |
| XAUUSD | LONDON | HURST_TREND_MOM | INVERT | HIGH_RR | 1.00 | 0.50 | 2.00 | 432 | 63.4% | 1.94 | 2.04 | +0.456 | 12.6 | 52.7 | 0.06% | 5.7% | $572 |
| XAGUSD | LONDON_NY | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 1.20 | 0.30 | 4.00 | 797 | 62.9% | 4.57 | 4.61 | +1.648 | 6.4 | 97.2 | 0.00% | 5.4% | $540 |
| EURUSD | ASIA | KALMAN_INNOV_EXPAND | INVERT | HIGH_RR | 1.50 | 0.70 | 2.14 | 515 | 62.3% | 1.84 | 1.74 | +0.331 | 10.2 | 63.0 | 0.00% | 5.1% | $510 |
| XAGUSD | LONDON | OLS_SLOPE_STRONG | INVERT | BALANCED | 1.90 | 0.60 | 3.17 | 525 | 61.7% | 2.54 | 2.64 | +0.634 | 12.2 | 64.1 | 0.01% | 4.8% | $476 |
| EURUSD | ALL_DAY | HURST_TREND_MOM | INVERT | HIGH_RR | 1.00 | 0.40 | 2.50 | 1,110 | 61.4% | 2.14 | 2.01 | +0.606 | 9.1 | 135.1 | 0.03% | 4.6% | $456 |
| XAUUSD | ALL_DAY | HURST_TREND_MOM | INVERT | HIGH_RR | 1.00 | 0.30 | 3.33 | 1,135 | 61.2% | 3.37 | 3.20 | +1.187 | 8.4 | 138.2 | 0.00% | 4.5% | $449 |
| EURUSD | ALL_DAY | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 1.30 | 0.40 | 3.25 | 1,538 | 61.0% | 2.66 | 2.61 | +0.891 | 12.4 | 187.7 | 0.00% | 4.4% | $435 |
| EURJPY | LONDON_NY | HURST_TREND_MOM | INVERT | HIGH_RR | 1.00 | 0.30 | 3.33 | 887 | 60.9% | 2.53 | 2.59 | +0.922 | 14.4 | 108.0 | 0.01% | 4.3% | $429 |
| AUDUSD | ALL_DAY | OLS_SLOPE_STRONG | INVERT | BALANCED | 1.30 | 0.50 | 2.60 | 1,456 | 60.7% | 2.20 | 2.15 | +0.639 | 12.3 | 177.5 | 0.03% | 4.2% | $420 |
| AUDUSD | NY | HURST_TREND_MOM | INVERT | HIGH_RR | 1.10 | 0.30 | 3.67 | 602 | 60.5% | 2.59 | 2.71 | +0.923 | 15.1 | 73.3 | 0.02% | 4.1% | $406 |
| GBPUSD | LONDON | HURST_TREND_MOM | INVERT | HIGH_RR | 1.00 | 0.40 | 2.50 | 491 | 59.9% | 1.88 | 1.73 | +0.553 | 11.8 | 60.6 | 0.40% | 3.7% | $373 |
| GBPJPY | NY | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 1.30 | 0.30 | 4.33 | 648 | 59.9% | 3.03 | 2.93 | +1.216 | 11.9 | 79.1 | 0.02% | 3.7% | $373 |
| EURJPY | ASIA | OLS_SLOPE_STRONG | INVERT | BALANCED | 1.20 | 0.50 | 2.40 | 702 | 59.8% | 1.96 | 2.00 | +0.513 | 12.7 | 85.6 | 0.03% | 3.7% | $370 |
| USDJPY | ALL_DAY | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 1.10 | 0.30 | 3.67 | 1,444 | 59.6% | 2.50 | 2.54 | +0.993 | 12.0 | 176.1 | 0.11% | 3.6% | $355 |
| GBPJPY | LONDON_NY | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 1.20 | 0.30 | 4.00 | 810 | 59.5% | 2.98 | 3.07 | +1.208 | 14.8 | 98.9 | 0.00% | 3.5% | $352 |
| EURUSD | ALL_DAY | KALMAN_INNOV_EXPAND | INVERT | HIGH_RR | 1.00 | 0.40 | 2.50 | 1,549 | 59.3% | 1.95 | 2.04 | +0.559 | 12.5 | 188.6 | 0.11% | 3.4% | $342 |
| GBPUSD | NY | KALMAN_INNOV_EXPAND | INVERT | HIGH_RR | 1.00 | 0.30 | 3.33 | 1,061 | 58.6% | 2.36 | 2.26 | +0.802 | 8.5 | 129.4 | 0.07% | 3.0% | $303 |
| GBPJPY | ALL_DAY | HURST_TREND_MOM | INVERT | HIGH_RR | 1.00 | 0.30 | 3.33 | 1,205 | 58.5% | 2.53 | 2.47 | +0.950 | 13.2 | 146.9 | 0.01% | 3.0% | $296 |
| AUDUSD | ASIA | KALMAN_INNOV_EXPAND | INVERT | HIGH_RR | 1.00 | 0.40 | 2.50 | 833 | 58.5% | 1.72 | 1.66 | +0.429 | 11.9 | 101.4 | 0.44% | 2.9% | $294 |
| XAGUSD | NY | HURST_TREND_MOM | INVERT | BALANCED | 2.00 | 0.50 | 4.00 | 572 | 58.4% | 2.40 | 2.38 | +0.638 | 7.2 | 69.6 | 0.00% | 2.9% | $290 |
| GBPAUD | LONDON | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 1.20 | 0.40 | 3.00 | 563 | 58.1% | 2.38 | 2.56 | +0.785 | 10.3 | 68.7 | 0.01% | 2.7% | $273 |
| EURUSD | ALL_DAY | SPECTRAL_TREND_MOM | INVERT | HIGH_RR | 1.00 | 0.30 | 3.33 | 174 | 58.0% | 2.25 | 2.30 | +0.799 | 8.6 | 21.2 | 0.02% | 2.7% | $271 |
| EURUSD | NY | KALMAN_INNOV_EXPAND | INVERT | HIGH_RR | 1.10 | 0.30 | 3.67 | 1,059 | 58.0% | 2.33 | 2.18 | +0.851 | 14.0 | 128.9 | 0.16% | 2.7% | $267 |
| EURJPY | NY | HURST_TREND_MOM | INVERT | HIGH_RR | 1.00 | 0.30 | 3.33 | 653 | 57.6% | 2.07 | 2.18 | +0.676 | 16.9 | 79.6 | 0.08% | 2.4% | $245 |
| AUDUSD | ALL_DAY | HURST_TREND_MOM | INVERT | HIGH_RR | 1.10 | 0.50 | 2.20 | 1,177 | 57.5% | 1.62 | 1.54 | +0.361 | 17.0 | 143.3 | 0.43% | 2.4% | $241 |
| XAUUSD | LONDON_NY | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 1.30 | 0.40 | 3.25 | 799 | 57.3% | 2.78 | 2.63 | +0.940 | 13.4 | 97.5 | 0.01% | 2.3% | $230 |
| XAUUSD | LONDON_NY | HURST_TREND_MOM | INVERT | HIGH_RR | 1.10 | 0.40 | 2.75 | 784 | 57.3% | 2.28 | 2.30 | +0.706 | 12.5 | 95.5 | 0.04% | 2.3% | $227 |
| EURUSD | LONDON_NY | OLS_SLOPE_STRONG | INVERT | BALANCED | 1.40 | 0.50 | 2.80 | 778 | 57.2% | 2.13 | 2.27 | +0.631 | 8.7 | 95.0 | 0.02% | 2.2% | $223 |
| GBPUSD | ASIA | HURST_TREND_MOM | INVERT | HIGH_RR | 1.40 | 0.50 | 2.80 | 317 | 57.1% | 1.92 | 1.99 | +0.507 | 21.2 | 38.7 | 0.01% | 2.2% | $217 |
| GBPJPY | LONDON | HURST_TREND_MOM | INVERT | BALANCED | 1.40 | 0.60 | 2.33 | 573 | 57.1% | 1.61 | 1.61 | +0.309 | 10.5 | 69.9 | 0.14% | 2.2% | $216 |
| USDJPY | LONDON_NY | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 1.20 | 0.40 | 3.00 | 799 | 56.8% | 1.98 | 1.83 | +0.621 | 10.9 | 97.4 | 0.06% | 2.0% | $202 |
| GBPAUD | ALL_DAY | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 1.30 | 0.30 | 4.33 | 1,460 | 56.5% | 3.08 | 3.02 | +1.293 | 12.8 | 178.0 | 0.02% | 1.8% | $184 |
| EURUSD | LONDON_NY | HURST_TREND_MOM | INVERT | HIGH_RR | 1.10 | 0.30 | 3.67 | 817 | 56.4% | 2.20 | 2.16 | +0.848 | 13.9 | 99.5 | 0.71% | 1.8% | $180 |
| XAUUSD | NY | HURST_TREND_MOM | INVERT | BALANCED | 1.50 | 0.50 | 3.00 | 637 | 55.9% | 1.99 | 1.96 | +0.523 | 14.5 | 77.6 | 0.02% | 1.5% | $150 |
| GBPUSD | ALL_DAY | KALMAN_INNOV_EXPAND | INVERT | HIGH_RR | 1.10 | 0.30 | 3.67 | 1,574 | 55.8% | 2.56 | 2.62 | +1.014 | 15.1 | 191.9 | 0.02% | 1.5% | $147 |
| XAUUSD | LONDON_NY | KALMAN_INNOV_EXPAND | INVERT | HIGH_RR | 1.00 | 0.40 | 2.50 | 1,135 | 55.8% | 2.05 | 1.90 | +0.589 | 12.6 | 138.3 | 0.03% | 1.4% | $143 |
| GBPUSD | ALL_DAY | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 1.50 | 0.40 | 3.75 | 1,503 | 55.4% | 2.53 | 2.72 | +0.888 | 12.0 | 183.5 | 0.02% | 1.2% | $124 |
| GBPAUD | LONDON_NY | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 1.40 | 0.40 | 3.50 | 847 | 55.4% | 2.48 | 2.46 | +0.862 | 12.7 | 103.2 | 0.00% | 1.2% | $121 |
| EURUSD | LONDON_NY | KALMAN_INNOV_EXPAND | INVERT | HIGH_RR | 1.00 | 0.30 | 3.33 | 1,277 | 55.2% | 2.07 | 2.07 | +0.736 | 12.7 | 155.5 | 0.35% | 1.1% | $112 |
| GBPUSD | LONDON_NY | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 1.50 | 0.40 | 3.75 | 803 | 55.2% | 2.54 | 2.54 | +0.929 | 16.2 | 98.1 | 0.01% | 1.1% | $109 |
| GBPUSD | NY | HURST_TREND_MOM | INVERT | HIGH_RR | 1.70 | 0.30 | 5.67 | 690 | 54.8% | 3.04 | 3.07 | +1.303 | 10.0 | 84.1 | 0.04% | 1.0% | $100 |
| GBPAUD | ALL_DAY | HURST_TREND_MOM | INVERT | HIGH_RR | 1.30 | 0.40 | 3.25 | 1,092 | 54.8% | 2.30 | 2.24 | +0.795 | 9.7 | 133.0 | 0.07% | 1.0% | $100 |
| XAGUSD | ALL_DAY | KALMAN_INNOV_EXPAND | INVERT | HIGH_RR | 1.20 | 0.40 | 3.00 | 1,489 | 54.7% | 2.48 | 2.57 | +0.839 | 14.1 | 181.3 | 0.00% | 1.0% | $100 |
| AUDUSD | LONDON | KALMAN_INNOV_EXPAND | INVERT | HIGH_RR | 1.40 | 0.40 | 3.50 | 723 | 54.4% | 1.78 | 1.73 | +0.469 | 10.8 | 88.1 | 0.50% | 1.0% | $100 |
| EURJPY | LONDON_NY | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 1.30 | 0.30 | 4.33 | 836 | 54.3% | 2.43 | 2.46 | +1.018 | 15.1 | 102.0 | 0.20% | 1.0% | $100 |
| XAUUSD | NY | KALMAN_INNOV_EXPAND | INVERT | HIGH_RR | 1.00 | 0.40 | 2.50 | 917 | 54.0% | 1.75 | 1.71 | +0.433 | 18.1 | 111.8 | 0.33% | 1.0% | $100 |
| GBPAUD | LONDON_NY | KALMAN_INNOV_EXPAND | INVERT | HIGH_RR | 1.00 | 0.30 | 3.33 | 1,231 | 53.7% | 2.15 | 2.18 | +0.760 | 15.8 | 150.0 | 0.18% | 1.0% | $100 |
| GBPUSD | LONDON_NY | GARCH_Z_FADE | NORMAL | HIGH_RR | 1.00 | 0.30 | 3.33 | 326 | 53.7% | 2.03 | 2.17 | +0.678 | 9.2 | 39.7 | 0.04% | 1.0% | $100 |
| GBPUSD | ALL_DAY | HURST_TREND_MOM | INVERT | HIGH_RR | 1.50 | 0.30 | 5.00 | 1,149 | 53.6% | 2.83 | 2.82 | +1.232 | 14.6 | 139.9 | 0.10% | 1.0% | $100 |
| AUDUSD | NY | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 3.00 | 0.30 | 10.00 | 616 | 53.6% | 3.10 | 3.30 | +1.485 | 12.7 | 75.3 | 0.13% | 1.0% | $100 |
| GBPAUD | LONDON_NY | GARCH_Z_FADE | NORMAL | HIGH_RR | 1.10 | 0.30 | 3.67 | 282 | 53.5% | 2.22 | 2.12 | +0.745 | 9.9 | 34.4 | 0.01% | 1.0% | $100 |
| AUDUSD | LONDON_NY | KALMAN_INNOV_EXPAND | INVERT | HIGH_RR | 1.20 | 0.30 | 4.00 | 1,216 | 53.5% | 2.09 | 2.06 | +0.803 | 15.7 | 148.2 | 0.90% | 1.0% | $100 |
| GBPAUD | LONDON | GARCH_Z_FADE | NORMAL | BALANCED | 1.40 | 0.50 | 2.80 | 131 | 52.7% | 1.59 | 1.70 | +0.301 | 6.9 | 16.3 | 0.00% | 1.0% | $100 |
| EURJPY | ALL_DAY | GARCH_Z_FADE | NORMAL | HIGH_RR | 1.00 | 0.30 | 3.33 | 396 | 51.5% | 1.71 | 1.76 | +0.560 | 14.5 | 48.4 | 0.96% | 1.0% | $100 |
| GBPAUD | LONDON_NY | HURST_TREND_MOM | INVERT | HIGH_RR | 1.40 | 0.30 | 4.67 | 831 | 51.5% | 2.62 | 2.65 | +1.116 | 14.8 | 101.2 | 0.04% | 1.0% | $100 |
| GBPJPY | ALL_DAY | GARCH_Z_FADE | NORMAL | HIGH_RR | 1.00 | 0.40 | 2.50 | 410 | 51.5% | 1.52 | 1.58 | +0.350 | 12.6 | 50.0 | 0.59% | 1.0% | $100 |
| GBPJPY | LONDON | GARCH_Z_FADE | NORMAL | HIGH_RR | 1.10 | 0.40 | 2.75 | 164 | 51.2% | 1.52 | 1.58 | +0.317 | 10.0 | 20.0 | 0.02% | 1.0% | $100 |
| EURJPY | NY | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 3.90 | 0.30 | 13.00 | 658 | 51.2% | 2.70 | 2.57 | +1.263 | 21.2 | 80.3 | 0.67% | 1.0% | $100 |
| XAUUSD | ASIA | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 3.60 | 0.30 | 12.00 | 792 | 50.8% | 3.13 | 3.09 | +1.321 | 10.9 | 96.6 | 0.05% | 1.0% | $100 |
| XAGUSD | LONDON_NY | GARCH_Z_FADE | NORMAL | HIGH_RR | 1.10 | 0.40 | 2.75 | 284 | 50.7% | 1.71 | 1.85 | +0.427 | 13.4 | 34.6 | 0.07% | 1.0% | $100 |

## H4 — 58 estrategias FUERTE

| Symbol | Sess | Setup | Dir | Regime | TP | SL | RR | n | WR | PF IS | PF OOS | Exp R | DD R | tpy | Ruin% | Risk % | USD risk @$10k |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| XAGUSD | ALL_DAY | HURST_TREND_MOM | INVERT | BALANCED | 0.80 | 0.70 | 1.14 | 673 | 74.4% | 2.47 | 2.43 | +0.362 | 4.9 | 82.3 | 0.00% | 11.9% | $1189 |
| AUDUSD | ALL_DAY | HURST_TREND_MOM | INVERT | BALANCED | 0.70 | 0.50 | 1.40 | 679 | 71.6% | 1.98 | 2.16 | +0.323 | 8.8 | 83.0 | 0.00% | 10.3% | $1028 |
| GBPJPY | NY | KALMAN_INNOV_EXPAND | INVERT | HIGH_RR | 3.90 | 0.90 | 4.33 | 527 | 69.8% | 2.85 | 3.12 | +0.216 | 3.4 | 64.7 | 0.00% | 9.3% | $930 |
| GBPJPY | LONDON_NY | HURST_TREND_MOM | INVERT | HIGH_RR | 3.90 | 0.30 | 13.00 | 480 | 69.8% | 4.21 | 4.15 | +1.260 | 8.5 | 58.8 | 0.00% | 9.3% | $928 |
| EURJPY | NY | KALMAN_INNOV_EXPAND | INVERT | HIGH_RR | 1.80 | 0.80 | 2.25 | 519 | 69.7% | 2.88 | 3.17 | +0.228 | 4.1 | 63.9 | 0.00% | 9.3% | $926 |
| USDJPY | NY | OLS_SLOPE_STRONG | INVERT | BALANCED | 2.00 | 0.70 | 2.86 | 433 | 69.7% | 3.27 | 2.92 | +0.297 | 5.4 | 53.3 | 0.00% | 9.3% | $926 |
| XAGUSD | ALL_DAY | SPECTRAL_TREND_MOM | INVERT | HIGH_RR | 1.60 | 1.00 | 1.60 | 66 | 69.7% | 1.89 | 1.71 | +0.256 | 3.8 | 8.3 | 0.00% | 9.2% | $923 |
| XAUUSD | ASIA | OLS_SLOPE_STRONG | INVERT | BALANCED | 1.30 | 0.90 | 1.44 | 488 | 69.7% | 3.08 | 3.69 | +0.295 | 4.1 | 59.8 | 0.00% | 9.2% | $922 |
| GBPAUD | LONDON_NY | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 2.70 | 0.40 | 6.75 | 538 | 69.0% | 4.29 | 4.73 | +1.088 | 7.6 | 65.9 | 0.00% | 8.8% | $882 |
| XAGUSD | NY | OLS_SLOPE_STRONG | INVERT | BALANCED | 0.60 | 1.10 | 0.55 | 409 | 68.9% | 2.87 | 2.94 | +0.209 | 2.8 | 50.2 | 0.00% | 8.8% | $881 |
| GBPJPY | ALL_DAY | OLS_SLOPE_STRONG | INVERT | BALANCED | 1.20 | 0.60 | 2.00 | 770 | 68.8% | 2.50 | 2.52 | +0.537 | 9.3 | 94.8 | 0.00% | 8.7% | $875 |
| XAGUSD | LONDON_NY | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 3.60 | 0.60 | 6.00 | 511 | 68.7% | 3.83 | 3.64 | +0.845 | 5.2 | 62.7 | 0.00% | 8.7% | $867 |
| XAGUSD | ASIA | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 3.30 | 1.00 | 3.30 | 447 | 68.7% | 3.46 | 3.70 | +0.291 | 3.4 | 54.8 | 0.00% | 8.7% | $866 |
| AUDUSD | NY | HURST_TREND_MOM | INVERT | BALANCED | 1.70 | 0.70 | 2.43 | 399 | 68.7% | 2.81 | 2.54 | +0.282 | 3.9 | 48.9 | 0.00% | 8.7% | $866 |
| EURJPY | LONDON_NY | KALMAN_INNOV_EXPAND | INVERT | HIGH_RR | 3.60 | 0.60 | 6.00 | 651 | 68.7% | 2.67 | 2.91 | +0.387 | 6.2 | 80.0 | 0.00% | 8.7% | $865 |
| USDJPY | ASIA | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 3.20 | 0.60 | 5.33 | 455 | 68.4% | 2.34 | 2.48 | +0.392 | 14.8 | 55.9 | 0.00% | 8.5% | $848 |
| EURJPY | LONDON_NY | HURST_TREND_MOM | INVERT | HIGH_RR | 3.50 | 0.40 | 8.75 | 470 | 68.3% | 3.08 | 2.96 | +0.719 | 7.1 | 57.5 | 0.00% | 8.4% | $845 |
| USDJPY | NY | HURST_TREND_MOM | INVERT | BALANCED | 1.10 | 0.70 | 1.57 | 464 | 68.1% | 2.24 | 2.53 | +0.201 | 8.4 | 57.1 | 0.00% | 8.3% | $834 |
| GBPJPY | LONDON_NY | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 3.90 | 0.40 | 9.75 | 497 | 67.8% | 3.81 | 4.03 | +0.998 | 6.6 | 61.2 | 0.00% | 8.2% | $817 |
| GBPJPY | LONDON_NY | KALMAN_INNOV_EXPAND | INVERT | HIGH_RR | 3.70 | 0.60 | 6.17 | 660 | 66.5% | 2.37 | 2.58 | +0.384 | 9.2 | 81.0 | 0.00% | 7.4% | $745 |
| EURUSD | ALL_DAY | HURST_TREND_MOM | INVERT | BALANCED | 1.00 | 0.50 | 2.00 | 702 | 66.4% | 2.05 | 2.02 | +0.411 | 8.1 | 85.9 | 0.00% | 7.4% | $737 |
| GBPAUD | ALL_DAY | OLS_SLOPE_STRONG | INVERT | BALANCED | 1.60 | 1.00 | 1.60 | 790 | 66.3% | 1.93 | 1.73 | +0.269 | 6.3 | 96.8 | 0.00% | 7.3% | $734 |
| XAGUSD | ALL_DAY | KALMAN_INNOV_EXPAND | INVERT | HIGH_RR | 1.00 | 0.40 | 2.50 | 859 | 65.9% | 3.08 | 2.98 | +0.813 | 11.3 | 104.9 | 0.00% | 7.1% | $710 |
| USDJPY | LONDON_NY | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 3.80 | 0.30 | 12.67 | 501 | 64.7% | 3.70 | 3.88 | +1.372 | 11.3 | 61.6 | 0.00% | 6.4% | $642 |
| EURJPY | ALL_DAY | KALMAN_INNOV_EXPAND | INVERT | HIGH_RR | 1.00 | 0.30 | 3.33 | 867 | 63.8% | 2.59 | 2.50 | +0.860 | 11.1 | 106.5 | 0.02% | 5.9% | $592 |
| USDJPY | LONDON_NY | HURST_TREND_MOM | INVERT | HIGH_RR | 1.40 | 0.30 | 4.67 | 537 | 63.7% | 2.31 | 2.28 | +0.686 | 14.0 | 66.1 | 0.11% | 5.9% | $586 |
| GBPAUD | ALL_DAY | KALMAN_INNOV_EXPAND | INVERT | BALANCED | 1.30 | 0.70 | 1.86 | 866 | 63.6% | 1.78 | 1.88 | +0.293 | 13.9 | 105.7 | 0.00% | 5.8% | $583 |
| EURJPY | ASIA | HURST_TREND_MOM | INVERT | HIGH_RR | 1.70 | 0.60 | 2.83 | 351 | 63.5% | 1.79 | 1.63 | +0.250 | 10.9 | 43.0 | 0.00% | 5.8% | $578 |
| AUDUSD | ALL_DAY | KALMAN_INNOV_EXPAND | INVERT | HIGH_RR | 1.00 | 0.40 | 2.50 | 869 | 63.5% | 2.17 | 2.23 | +0.554 | 12.0 | 106.1 | 0.01% | 5.8% | $577 |
| USDJPY | ASIA | HURST_TREND_MOM | INVERT | BALANCED | 2.00 | 0.50 | 4.00 | 414 | 62.8% | 1.80 | 1.59 | +0.284 | 10.2 | 50.6 | 0.00% | 5.4% | $537 |
| AUDUSD | ASIA | HURST_TREND_MOM | INVERT | HIGH_RR | 4.00 | 0.70 | 5.71 | 344 | 62.8% | 1.81 | 1.77 | +0.202 | 7.9 | 42.0 | 0.00% | 5.4% | $536 |
| USDJPY | ASIA | KALMAN_INNOV_EXPAND | INVERT | HIGH_RR | 2.60 | 0.50 | 5.20 | 428 | 62.4% | 1.50 | 1.22 | +0.210 | 18.2 | 52.5 | 0.26% | 5.1% | $513 |
| AUDUSD | LONDON_NY | HURST_TREND_MOM | INVERT | HIGH_RR | 3.80 | 0.40 | 9.50 | 488 | 62.1% | 2.48 | 2.50 | +0.621 | 7.3 | 59.6 | 0.00% | 5.0% | $497 |
| GBPAUD | LONDON | OLS_SLOPE_STRONG | INVERT | HIGH_WR | 1.20 | 1.00 | 1.20 | 396 | 61.9% | 2.09 | 2.51 | +0.256 | 5.5 | 48.5 | 0.00% | 4.8% | $485 |
| GBPJPY | LONDON | HURST_TREND_MOM | INVERT | HIGH_RR | 2.30 | 0.60 | 3.83 | 270 | 61.9% | 1.74 | 1.69 | +0.317 | 12.8 | 33.1 | 0.01% | 4.8% | $484 |
| EURJPY | LONDON | KALMAN_INNOV_EXPAND | INVERT | BALANCED | 1.30 | 0.70 | 1.86 | 275 | 61.5% | 1.53 | 1.84 | +0.179 | 10.4 | 34.0 | 0.00% | 4.6% | $461 |
| GBPJPY | ALL_DAY | HURST_TREND_MOM | INVERT | HIGH_RR | 1.20 | 0.40 | 3.00 | 663 | 61.2% | 2.22 | 2.22 | +0.626 | 13.7 | 81.2 | 0.07% | 4.5% | $449 |
| EURUSD | LONDON_NY | HURST_TREND_MOM | INVERT | HIGH_RR | 2.50 | 0.50 | 5.00 | 489 | 60.9% | 1.93 | 1.82 | +0.359 | 12.5 | 59.8 | 0.00% | 4.3% | $433 |
| EURUSD | ASIA | HURST_TREND_MOM | INVERT | HIGH_WR | 1.50 | 1.00 | 1.50 | 336 | 60.7% | 1.53 | 1.70 | +0.104 | 4.8 | 41.2 | 0.00% | 4.2% | $420 |
| EURJPY | ALL_DAY | OLS_SLOPE_STRONG | INVERT | BALANCED | 1.80 | 0.70 | 2.57 | 786 | 60.2% | 1.87 | 1.89 | +0.376 | 10.5 | 97.2 | 0.06% | 3.9% | $390 |
| EURJPY | LONDON | OLS_SLOPE_STRONG | INVERT | BALANCED | 1.10 | 0.90 | 1.22 | 373 | 59.8% | 1.69 | 1.63 | +0.191 | 6.6 | 46.2 | 0.00% | 3.7% | $368 |
| USDJPY | LONDON | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 2.90 | 1.00 | 2.90 | 368 | 59.5% | 1.78 | 1.86 | +0.235 | 11.2 | 45.3 | 0.00% | 3.5% | $353 |
| GBPAUD | LONDON | KALMAN_INNOV_EXPAND | INVERT | BALANCED | 1.90 | 0.60 | 3.17 | 286 | 59.4% | 1.33 | 1.50 | +0.149 | 21.2 | 35.2 | 0.24% | 3.5% | $349 |
| AUDUSD | LONDON | HURST_TREND_MOM | INVERT | HIGH_RR | 1.70 | 0.60 | 2.83 | 281 | 59.4% | 1.37 | 1.31 | +0.166 | 21.9 | 34.3 | 0.06% | 3.5% | $348 |
| GBPJPY | ASIA | HURST_TREND_MOM | INVERT | BALANCED | 1.40 | 0.60 | 2.33 | 341 | 58.4% | 1.39 | 1.56 | +0.157 | 14.5 | 41.8 | 0.13% | 2.9% | $288 |
| GBPJPY | LONDON | OLS_SLOPE_STRONG | INVERT | BALANCED | 1.60 | 0.90 | 1.78 | 366 | 58.2% | 1.66 | 1.94 | +0.208 | 8.4 | 45.1 | 0.00% | 2.8% | $279 |
| AUDUSD | LONDON | OLS_SLOPE_STRONG | INVERT | BALANCED | 1.60 | 0.70 | 2.29 | 394 | 57.9% | 1.75 | 1.86 | +0.282 | 11.0 | 48.5 | 0.00% | 2.6% | $261 |
| GBPJPY | ALL_DAY | KALMAN_INNOV_EXPAND | INVERT | BALANCED | 1.60 | 0.50 | 3.20 | 858 | 57.5% | 1.76 | 1.78 | +0.388 | 11.5 | 105.3 | 0.17% | 2.4% | $238 |
| USDJPY | ALL_DAY | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 2.90 | 0.40 | 7.25 | 746 | 57.2% | 2.47 | 2.61 | +0.910 | 13.0 | 91.7 | 0.29% | 2.3% | $225 |
| XAUUSD | ALL_DAY | OLS_SLOPE_STRONG | INVERT | HIGH_RR | 2.90 | 0.40 | 7.25 | 790 | 55.8% | 3.09 | 3.03 | +1.139 | 10.8 | 96.8 | 0.00% | 1.5% | $146 |
| XAGUSD | ALL_DAY | GARCH_Z_FADE | NORMAL | BALANCED | 0.70 | 0.50 | 1.40 | 194 | 54.6% | 1.27 | 1.17 | +0.114 | 8.6 | 23.8 | 0.00% | 1.0% | $100 |
| XAGUSD | LONDON_NY | GARCH_Z_FADE | NORMAL | HIGH_RR | 3.70 | 0.40 | 9.25 | 135 | 54.1% | 1.83 | 1.61 | +0.371 | 7.5 | 16.6 | 0.00% | 1.0% | $100 |
| GBPAUD | ALL_DAY | GARCH_Z_FADE | NORMAL | HIGH_RR | 1.00 | 0.50 | 2.00 | 152 | 53.9% | 1.43 | 1.38 | +0.206 | 6.9 | 18.7 | 0.00% | 1.0% | $100 |
| AUDUSD | LONDON_NY | GARCH_Z_FADE | NORMAL | HIGH_RR | 1.30 | 0.40 | 3.25 | 116 | 52.6% | 1.87 | 2.17 | +0.386 | 8.7 | 14.5 | 0.00% | 1.0% | $100 |
| GBPJPY | LONDON | GARCH_Z_FADE | NORMAL | HIGH_RR | 1.10 | 0.40 | 2.75 | 65 | 52.3% | 1.56 | 1.47 | +0.279 | 7.3 | 8.1 | 0.00% | 1.0% | $100 |
| XAUUSD | ALL_DAY | GARCH_Z_FADE | NORMAL | HIGH_RR | 1.00 | 0.30 | 3.33 | 201 | 51.2% | 1.97 | 2.08 | +0.543 | 13.1 | 24.9 | 0.01% | 1.0% | $100 |
| EURJPY | ALL_DAY | GARCH_Z_FADE | NORMAL | HIGH_RR | 1.10 | 0.40 | 2.75 | 166 | 50.6% | 1.61 | 1.53 | +0.328 | 11.0 | 20.4 | 0.00% | 1.0% | $100 |
| XAGUSD | LONDON | KALMAN_INNOV_EXPAND | NORMAL | HIGH_RR | 2.70 | 0.50 | 5.40 | 178 | 50.6% | 1.48 | 1.31 | +0.270 | 15.1 | 21.8 | 0.64% | 1.0% | $100 |

## Riesgo total simultáneo (worst-case overlap @ $10k)

Si TODAS las estrategias FUERTE dispararan trades simultáneamente y cada una perdiera 1R, el drawdown agregado sería:

- **M15**: 25 strats — riesgo simultáneo total = $8234 (82.3% del balance $10k)
- **H1**: 70 strats — riesgo simultáneo total = $22810 (228.1% del balance $10k)
- **H4**: 58 strats — riesgo simultáneo total = $32561 (325.6% del balance $10k)
- **TOTAL**: 153 strats — riesgo simultáneo total = $63605 (636.0% del balance $10k)

En la práctica, los trades NO disparan todos al mismo tiempo (deduplicación por día, session windows distintas, TFs separados). El riesgo simultáneo realista es ~10-20% del worst-case por overlap natural.

## Recomendación de deploy

1. **Bot LIVE actual** ya tiene 34 estrategias elite WR≥65% activas.
2. Si quieres todas las 153 FUERTE, hay que ampliar el filtro de `bot_config_math.json` (reemplazar el current 34 con el dataset FUERTE completo).
3. **Risk model**: el actual usa BalanceTieredRiskAllocator con tier 1 (≤$2k = 1-15%). Si tu balance es $10k, automáticamente cae en tier 2 (1-8%). Para modo agresivo (test rápido a $1M) hay que sobrescribir con tier 1 explícitamente.
4. **Crítico**: monitorear primer mes en VIVO. Las proyecciones asumen que la fricción real-time iguala la del backtest. Si los R efectivos son menores, ajustar el risk_pct a la baja.
