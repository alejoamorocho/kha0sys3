# Portfolio Alpha Simulation Report (Walk-Forward OOS)

> Resultados Out-of-Sample con walk-forward validation, Monte Carlo, corrección FDR y análisis de decay.
> Deduplicación: máx 1 trade/día/símbolo. MAGNET_CLOSE filtra pd_close dentro del OR.

## Dashboard de Gestión de Riesgo
| Métrica | Valor | Descripción |
|:---|:---|:---|
| **PnL Total Neto (OOS)** | `3314.90 R` | Resultado Out-of-Sample después de fricción. |
| **Win Rate Global** | `66.38%` | Probabilidad de acierto OOS. |
| **Profit Factor** | `2.35` | Ganancia Bruta / Pérdida Bruta. |
| **Expectativa (R)** | `0.507 R` | Media por trade OOS. |
| **Máximo Drawdown** | `-18.20 R` | Mayor caída desde pico de equidad. |
| **Total Trades (OOS)** | `6543` | Trades ejecutados fuera de muestra. |

## Walk-Forward Validation
**Edges robustos:** 88/106 (sobrevivieron >= 60% de los folds)

| Fold | Train hasta | Test | Setups | Trades OOS | PnL OOS | WR OOS |
|:---|:---|:---|:---|:---|:---|:---|
| 1 | 2022-02-11 | 2022-02-11 -> 2022-12-07 | 94 | 1336 | `688.4 R` | `66.1%` |
| 2 | 2022-12-08 | 2022-12-08 -> 2023-10-03 | 97 | 1423 | `689.4 R` | `66.1%` |
| 3 | 2023-10-04 | 2023-10-04 -> 2024-07-30 | 88 | 1229 | `707.9 R` | `69.2%` |
| 4 | 2024-07-31 | 2024-07-31 -> 2025-05-26 | 90 | 1251 | `575.6 R` | `64.7%` |
| 5 | 2025-05-27 | 2025-05-27 -> 2026-03-22 | 91 | 1304 | `653.6 R` | `65.9%` |

## Monte Carlo Simulation (10,000 permutaciones)
| Métrica | P5 (Pesimista) | P50 (Mediana) | P95 (Optimista) |
|:---|:---|:---|:---|
| **PnL Final** | `3156.4 R` | `3315.2 R` | `3468.8 R` |
| **Max Drawdown** | `-14.2 R` | `-10.5 R` | `-8.5 R` |

**Probabilidad de ruina (PnL < 0):** `0.0%`

## Corrección por Multiple Testing (Benjamini-Hochberg FDR)
**Setups testeados:** 28 | **Significativos post-FDR (alpha=0.05):** 16

| Setup | WR Observado | p-value | p-adj (FDR) | Significativo |
|:---|:---|:---|:---|:---|
| NASDAQ100_Pre-Market_TREND_UP | `73.0%` | `0.0000` | `0.0000` | Si |
| WTI_London Initial_TREND_UP | `73.2%` | `0.0000` | `0.0000` | Si |
| GBPJPY_Tokyo_TREND_UP | `71.6%` | `0.0000` | `0.0000` | Si |
| EURJPY_Tokyo_TREND_UP | `71.9%` | `0.0000` | `0.0000` | Si |
| USDJPY_Tokyo_TREND_UP | `73.1%` | `0.0000` | `0.0000` | Si |
| XAUUSD_London_TREND_UP | `73.0%` | `0.0000` | `0.0000` | Si |
| SP500_Pre-Market_TREND_UP | `76.8%` | `0.0000` | `0.0000` | Si |
| GBPUSD_London_TREND_UP | `68.3%` | `0.0000` | `0.0000` | Si |
| EURUSD_London_TREND_UP | `69.3%` | `0.0000` | `0.0000` | Si |
| BRENT_London_TREND_UP | `70.1%` | `0.0000` | `0.0000` | Si |
| GBPAUD_London_TREND_UP | `69.3%` | `0.0000` | `0.0000` | Si |
| AUDUSD_London_TREND_UP | `67.2%` | `0.0000` | `0.0000` | Si |
| XAGUSD_London_TREND_UP | `64.9%` | `0.0000` | `0.0000` | Si |
| XAGUSD_London_TREND_DW | `70.5%` | `0.0000` | `0.0001` | Si |
| EURJPY_Tokyo_TREND_DW | `89.5%` | `0.0004` | `0.0007` | Si |
| GBPAUD_London_TREND_DW | `87.5%` | `0.0021` | `0.0037` | Si |
| USDJPY_Tokyo_TREND_DW | `63.6%` | `0.2744` | `0.4520` | No |
| GBPJPY_Tokyo_TREND_DW | `58.8%` | `0.3145` | `0.4893` | No |
| EURUSD_London_MAGNET_CLOSE | `54.0%` | `0.6349` | `0.9356` | No |
| WTI_London Initial_MAGNET_CLOSE | `50.0%` | `0.7617` | `1.0000` | No |
| VIX_NY Cash_MAGNET_CLOSE | `45.3%` | `0.9776` | `1.0000` | No |
| GBPAUD_London_MAGNET_CLOSE | `38.5%` | `0.9873` | `1.0000` | No |
| XAUUSD_London_MAGNET_CLOSE | `43.6%` | `0.9967` | `1.0000` | No |
| SP500_Pre-Market_MAGNET_CLOSE | `42.1%` | `0.9978` | `1.0000` | No |
| GBPUSD_London_MAGNET_CLOSE | `42.9%` | `0.9985` | `1.0000` | No |
| NASDAQ100_Pre-Market_MAGNET_CLOSE | `38.8%` | `0.9999` | `1.0000` | No |
| XAGUSD_London_MAGNET_CLOSE | `33.3%` | `0.9999` | `1.0000` | No |
| BRENT_London_MAGNET_CLOSE | `39.0%` | `1.0000` | `1.0000` | No |

## Análisis de Decay del Edge
| Período | Trades | WR | PnL (R) | Expectativa | Trend |
|:---|:---|:---|:---|:---|:---|
| 2022-02-11 -> 2023-02-11 | 1635 | `65.8%` | `815.4 R` | `0.499 R` | **ESTABLE** |
| 2023-02-11 -> 2024-02-11 | 1657 | `67.4%` | `865.9 R` | `0.523 R` | **ESTABLE** |
| 2024-02-11 -> 2025-02-10 | 1518 | `67.1%` | `792.5 R` | `0.522 R` | **ESTABLE** |
| 2025-02-10 -> 2026-02-10 | 1589 | `65.1%` | `765.3 R` | `0.482 R` | **ESTABLE** |
| 2026-02-10 -> 2026-03-20 | 144 | `67.4%` | `75.8 R` | `0.526 R` | **ESTABLE** |

**Decay score:** `1.30` (1.0 = perfectamente estable, <0.5 = degradación severa)

## Desglose por Alpha Generator (OOS)
| Instrumento | Sesión | Edge | W / L | Win Rate | PF | Net PnL (R) |
|:---|:---|:---|:---|:---|:---|:---|
| **WTI** | London Initial | `TREND_UP` | 342 / 125 | `73.2%` | `3.48` | **341.3** |
| **EURJPY** | Tokyo | `TREND_UP` | 336 / 131 | `71.9%` | `3.26` | **326.3** |
| **GBPJPY** | Tokyo | `TREND_UP` | 326 / 129 | `71.6%` | `3.22` | **314.5** |
| **XAUUSD** | London | `TREND_UP` | 316 / 117 | `73.0%` | `3.44` | **313.7** |
| **USDJPY** | Tokyo | `TREND_UP` | 307 / 113 | `73.1%` | `3.46` | **305.5** |
| **GBPUSD** | London | `TREND_UP` | 297 / 138 | `68.3%` | `2.74` | **264.0** |
| **EURUSD** | London | `TREND_UP` | 269 / 119 | `69.3%` | `2.88` | **245.7** |
| **GBPAUD** | London | `TREND_UP` | 266 / 118 | `69.3%` | `2.87` | **242.6** |
| **NASDAQ100** | Pre-Market | `TREND_UP` | 281 / 104 | `73.0%` | `2.93` | **240.5** |
| **SP500** | Pre-Market | `TREND_UP` | 252 / 76 | `76.8%` | `3.59` | **236.4** |
| **BRENT** | London | `TREND_UP` | 249 / 106 | `70.1%` | `2.99` | **232.0** |
| **AUDUSD** | London | `TREND_UP` | 254 / 124 | `67.2%` | `2.61` | **219.2** |
| **XAGUSD** | London | `TREND_UP` | 246 / 133 | `64.9%` | `2.35` | **198.1** |
| **XAGUSD** | London | `TREND_DW` | 67 / 28 | `70.5%` | `3.05` | **63.0** |
| **EURJPY** | Tokyo | `TREND_DW` | 17 / 2 | `89.5%` | `10.82` | **21.6** |
| **GBPAUD** | London | `TREND_DW` | 14 / 2 | `87.5%` | `8.91` | **17.4** |
| **GBPJPY** | Tokyo | `TREND_DW` | 10 / 7 | `58.8%` | `1.82` | **6.3** |
| **EURJPY** | London | `TREND_UP` | 5 / 1 | `83.3%` | `6.36` | **5.9** |
| **USDJPY** | Tokyo | `TREND_DW` | 7 / 4 | `63.6%` | `2.23` | **5.4** |
| **USDJPY** | Tokyo | `MAGNET_CLOSE` | 2 / 0 | `100.0%` | `99.90` | **1.8** |
| **GBPJPY** | Tokyo | `MAGNET_CLOSE` | 1 / 0 | `100.0%` | `99.90` | **0.9** |

## Curva de Equidad Agregada OOS (Unidades R)
```text
Trades 000000 |      0.90 R | 
Trades 000163 |    107.90 R | ##
Trades 000326 |    201.70 R | ####
Trades 000489 |    283.30 R | ######
Trades 000652 |    355.70 R | ########
Trades 000815 |    438.70 R | ##########
Trades 000978 |    515.30 R | ############
Trades 001141 |    594.80 R | ##############
Trades 001304 |    666.40 R | ################
Trades 001467 |    740.70 R | #################
Trades 001630 |    812.50 R | ###################
Trades 001793 |    886.90 R | #####################
Trades 001956 |    957.90 R | #######################
Trades 002119 |   1046.50 R | #########################
Trades 002282 |   1137.50 R | ###########################
Trades 002445 |   1205.70 R | #############################
Trades 002608 |   1291.60 R | ###############################
Trades 002771 |   1395.80 R | #################################
Trades 002934 |   1510.60 R | ####################################
Trades 003097 |   1579.30 R | ######################################
Trades 003260 |   1665.10 R | ########################################
Trades 003423 |   1766.70 R | ##########################################
Trades 003586 |   1844.40 R | ############################################
Trades 003749 |   1917.80 R | ##############################################
Trades 003912 |   2047.80 R | #################################################
Trades 004075 |   2112.30 R | ##################################################
Trades 004238 |   2168.10 R | ####################################################
Trades 004401 |   2267.80 R | ######################################################
Trades 004564 |   2360.30 R | ########################################################
Trades 004727 |   2425.20 R | ##########################################################
Trades 004890 |   2517.70 R | ############################################################
Trades 005053 |   2592.90 R | ##############################################################
Trades 005216 |   2656.20 R | ################################################################
Trades 005379 |   2745.60 R | ##################################################################
Trades 005542 |   2789.30 R | ###################################################################
Trades 005705 |   2866.30 R | #####################################################################
Trades 005868 |   2962.50 R | #######################################################################
Trades 006031 |   3016.00 R | ########################################################################
Trades 006194 |   3137.60 R | ###########################################################################
Trades 006357 |   3223.30 R | #############################################################################
Trades 006520 |   3302.50 R | ###############################################################################
```

---
### Lógica de Protección de Capital y Gestión
> Cada operación simulada respeta la siguiente arquitectura de riesgo:

1. **Costo de Fricción (-0.1R)**: Penalización automática por spreads y comisiones.
2. **Hardware Stop Loss (1.1R)**: Stop en extremo opuesto del OR. Pérdida = -1.1R.
3. **Asimetría TREND (1.4R Neto)**: TP a 1.5R, neto +1.4R tras fricción.
4. **Imán MAGNET (0.9R Neto)**: Dirección dada por posición de pd_close vs OR. Neto +0.9R.
5. **Filtro ATR (0.1-0.8)**: No opera si volatilidad fuera de rango.
6. **Deduplicación**: Máx 1 trade/día/símbolo.
7. **Walk-Forward**: Edges descubiertos en train, validados en test (OOS).
8. **FDR**: Solo setups estadísticamente significativos tras corrección.
