# Portfolio Alpha Simulation Report (Walk-Forward OOS)

> Resultados Out-of-Sample con walk-forward validation, Monte Carlo, corrección FDR y análisis de decay.
> Deduplicación: máx 1 trade/día/símbolo. MAGNET_CLOSE filtra pd_close dentro del OR.

## Dashboard de Gestión de Riesgo
| Métrica | Valor | Descripción |
|:---|:---|:---|
| **PnL Total Neto (OOS)** | `3973.90 R` | Resultado Out-of-Sample después de fricción. |
| **Win Rate Global** | `70.15%` | Probabilidad de acierto OOS. |
| **Profit Factor** | `2.79` | Ganancia Bruta / Pérdida Bruta. |
| **Expectativa (R)** | `0.589 R` | Media por trade OOS. |
| **Máximo Drawdown** | `-16.40 R` | Mayor caída desde pico de equidad. |
| **Total Trades (OOS)** | `6746` | Trades ejecutados fuera de muestra. |

## Walk-Forward Validation
**Edges robustos:** 88/106 (sobrevivieron >= 60% de los folds)

| Fold | Train hasta | Test | Setups | Trades OOS | PnL OOS | WR OOS |
|:---|:---|:---|:---|:---|:---|:---|
| 1 | 2022-02-11 | 2022-02-11 -> 2022-12-07 | 94 | 1366 | `783.4 R` | `68.7%` |
| 2 | 2022-12-08 | 2022-12-08 -> 2023-10-03 | 97 | 1478 | `814.7 R` | `68.9%` |
| 3 | 2023-10-04 | 2023-10-04 -> 2024-07-30 | 88 | 1264 | `892.1 R` | `75.3%` |
| 4 | 2024-07-31 | 2024-07-31 -> 2025-05-26 | 90 | 1302 | `714.8 R` | `69.0%` |
| 5 | 2025-05-27 | 2025-05-27 -> 2026-03-22 | 91 | 1336 | `768.9 R` | `69.2%` |

## Monte Carlo Simulation (10,000 permutaciones)
| Métrica | P5 (Pesimista) | P50 (Mediana) | P95 (Optimista) |
|:---|:---|:---|:---|
| **PnL Final** | `3973.9 R` | `3973.9 R` | `3973.9 R` |
| **Max Drawdown** | `-11.9 R` | `-8.8 R` | `-7.2 R` |

**Probabilidad de ruina (PnL < 0):** `0.0%`

## Corrección por Multiple Testing (Benjamini-Hochberg FDR)
**Setups testeados:** 28 | **Significativos post-FDR (alpha=0.05):** 23

| Setup | WR Observado | p-value | p-adj (FDR) | Significativo |
|:---|:---|:---|:---|:---|
| WTI_London Initial_TREND_UP | `73.2%` | `0.0000` | `0.0000` | Si |
| USDJPY_Tokyo_TREND_UP | `73.1%` | `0.0000` | `0.0000` | Si |
| SP500_Pre-Market_TREND_UP | `76.8%` | `0.0000` | `0.0000` | Si |
| GBPJPY_Tokyo_TREND_UP | `71.6%` | `0.0000` | `0.0000` | Si |
| NASDAQ100_Pre-Market_TREND_UP | `73.0%` | `0.0000` | `0.0000` | Si |
| XAUUSD_London_TREND_UP | `73.0%` | `0.0000` | `0.0000` | Si |
| EURJPY_Tokyo_TREND_UP | `71.9%` | `0.0000` | `0.0000` | Si |
| EURUSD_London_TREND_UP | `69.3%` | `0.0000` | `0.0000` | Si |
| GBPUSD_London_TREND_UP | `68.3%` | `0.0000` | `0.0000` | Si |
| BRENT_London_TREND_UP | `70.1%` | `0.0000` | `0.0000` | Si |
| GBPAUD_London_TREND_UP | `69.3%` | `0.0000` | `0.0000` | Si |
| EURUSD_London_MAGNET_CLOSE | `73.5%` | `0.0000` | `0.0000` | Si |
| AUDUSD_London_TREND_UP | `67.2%` | `0.0000` | `0.0000` | Si |
| GBPUSD_London_MAGNET_CLOSE | `73.6%` | `0.0000` | `0.0000` | Si |
| XAGUSD_London_TREND_UP | `64.9%` | `0.0000` | `0.0000` | Si |
| BRENT_London_MAGNET_CLOSE | `67.9%` | `0.0000` | `0.0000` | Si |
| XAUUSD_London_MAGNET_CLOSE | `68.5%` | `0.0000` | `0.0000` | Si |
| XAGUSD_London_TREND_DW | `70.5%` | `0.0000` | `0.0001` | Si |
| SP500_Pre-Market_MAGNET_CLOSE | `64.7%` | `0.0003` | `0.0005` | Si |
| NASDAQ100_Pre-Market_MAGNET_CLOSE | `64.5%` | `0.0003` | `0.0005` | Si |
| EURJPY_Tokyo_TREND_DW | `89.5%` | `0.0004` | `0.0005` | Si |
| GBPAUD_London_TREND_DW | `87.5%` | `0.0021` | `0.0027` | Si |
| WTI_London Initial_MAGNET_CLOSE | `69.7%` | `0.0175` | `0.0214` | Si |
| XAGUSD_London_MAGNET_CLOSE | `58.2%` | `0.0883` | `0.1030` | No |
| VIX_NY Cash_MAGNET_CLOSE | `54.4%` | `0.1856` | `0.2078` | No |
| USDJPY_Tokyo_TREND_DW | `63.6%` | `0.2744` | `0.2955` | No |
| GBPJPY_Tokyo_TREND_DW | `58.8%` | `0.3145` | `0.3262` | No |
| GBPAUD_London_MAGNET_CLOSE | `53.5%` | `0.3804` | `0.3804` | No |

## Análisis de Decay del Edge
| Período | Trades | WR | PnL (R) | Expectativa | Trend |
|:---|:---|:---|:---|:---|:---|
| 2022-02-11 -> 2023-02-11 | 1670 | `69.4%` | `965.0 R` | `0.578 R` | **ESTABLE** |
| 2023-02-11 -> 2024-02-11 | 1725 | `70.7%` | `1028.5 R` | `0.596 R` | **ESTABLE** |
| 2024-02-11 -> 2025-02-10 | 1564 | `71.8%` | `976.1 R` | `0.624 R` | **ESTABLE** |
| 2025-02-10 -> 2026-02-10 | 1641 | `68.5%` | `910.4 R` | `0.555 R` | **ESTABLE** |
| 2026-02-10 -> 2026-03-20 | 146 | `72.6%` | `93.9 R` | `0.643 R` | **ESTABLE** |

**Decay score:** `1.03` (1.0 = perfectamente estable, <0.5 = degradación severa)

## Desglose por Alpha Generator (OOS)
| Instrumento | Sesión | Edge | W / L | Win Rate | PF | Net PnL (R) |
|:---|:---|:---|:---|:---|:---|:---|
| **WTI** | London Initial | `TREND_UP` | 342 / 125 | `73.2%` | `3.48` | **341.3** |
| **EURJPY** | Tokyo | `TREND_UP` | 336 / 131 | `71.9%` | `3.26` | **326.3** |
| **GBPJPY** | Tokyo | `TREND_UP` | 326 / 129 | `71.6%` | `3.22` | **314.5** |
| **XAUUSD** | London | `TREND_UP` | 316 / 117 | `73.0%` | `3.44` | **313.7** |
| **USDJPY** | Tokyo | `TREND_UP` | 307 / 113 | `73.1%` | `3.46` | **305.5** |
| **NASDAQ100** | Pre-Market | `TREND_UP` | 281 / 104 | `73.0%` | `3.44` | **279.0** |
| **SP500** | Pre-Market | `TREND_UP` | 252 / 76 | `76.8%` | `4.22` | **269.2** |
| **GBPUSD** | London | `TREND_UP` | 297 / 138 | `68.3%` | `2.74` | **264.0** |
| **EURUSD** | London | `TREND_UP` | 269 / 119 | `69.3%` | `2.88` | **245.7** |
| **GBPAUD** | London | `TREND_UP` | 266 / 118 | `69.3%` | `2.87` | **242.6** |
| **BRENT** | London | `TREND_UP` | 249 / 106 | `70.1%` | `2.99` | **232.0** |
| **AUDUSD** | London | `TREND_UP` | 254 / 124 | `67.2%` | `2.61` | **219.2** |
| **XAGUSD** | London | `TREND_UP` | 246 / 133 | `64.9%` | `2.35` | **198.1** |
| **EURUSD** | London | `MAGNET_CLOSE` | 169 / 61 | `73.5%` | `2.27` | **85.0** |
| **XAGUSD** | London | `TREND_DW` | 67 / 28 | `70.5%` | `3.05` | **63.0** |
| **GBPUSD** | London | `MAGNET_CLOSE` | 117 / 42 | `73.6%` | `2.28` | **59.1** |
| **BRENT** | London | `MAGNET_CLOSE` | 131 / 62 | `67.9%` | `1.73` | **49.7** |
| **XAUUSD** | London | `MAGNET_CLOSE` | 102 / 47 | `68.5%` | `1.78` | **40.1** |
| **SP500** | Pre-Market | `MAGNET_CLOSE` | 90 / 49 | `64.7%` | `1.50` | **27.1** |
| **NASDAQ100** | Pre-Market | `MAGNET_CLOSE` | 91 / 50 | `64.5%` | `1.49` | **26.9** |
| **EURJPY** | Tokyo | `TREND_DW` | 17 / 2 | `89.5%` | `10.82` | **21.6** |
| **GBPAUD** | London | `TREND_DW` | 14 / 2 | `87.5%` | `8.91` | **17.4** |
| **WTI** | London Initial | `MAGNET_CLOSE` | 23 / 10 | `69.7%` | `1.88` | **9.7** |
| **GBPJPY** | Tokyo | `TREND_DW` | 10 / 7 | `58.8%` | `1.82` | **6.3** |
| **EURJPY** | London | `TREND_UP` | 5 / 1 | `83.3%` | `6.36` | **5.9** |
| **USDJPY** | Tokyo | `TREND_DW` | 7 / 4 | `63.6%` | `2.23` | **5.4** |
| **XAGUSD** | London | `MAGNET_CLOSE` | 46 / 33 | `58.2%` | `1.14` | **5.1** |
| **GBPJPY** | London | `MAGNET_CLOSE` | 5 / 2 | `71.4%` | `2.05` | **2.3** |
| **EURJPY** | Tokyo | `MAGNET_CLOSE` | 2 / 0 | `100.0%` | `99.90` | **1.8** |
| **GBPJPY** | Tokyo | `MAGNET_CLOSE` | 1 / 0 | `100.0%` | `99.90` | **0.9** |

## Curva de Equidad Agregada OOS (Unidades R)
```text
Trades 000000 |      0.90 R | 
Trades 000168 |    127.60 R | ##
Trades 000336 |    234.80 R | ####
Trades 000504 |    337.50 R | ######
Trades 000672 |    421.20 R | ########
Trades 000840 |    506.90 R | ##########
Trades 001008 |    597.60 R | ############
Trades 001176 |    684.80 R | #############
Trades 001344 |    768.00 R | ###############
Trades 001512 |    861.20 R | #################
Trades 001680 |    969.40 R | ###################
Trades 001848 |   1052.10 R | #####################
Trades 002016 |   1139.80 R | ######################
Trades 002184 |   1227.00 R | ########################
Trades 002352 |   1320.20 R | ##########################
Trades 002520 |   1396.40 R | ############################
Trades 002688 |   1494.10 R | ##############################
Trades 002856 |   1616.30 R | ################################
Trades 003024 |   1752.00 R | ###################################
Trades 003192 |   1862.20 R | #####################################
Trades 003360 |   1973.40 R | #######################################
Trades 003528 |   2093.60 R | ##########################################
Trades 003696 |   2203.30 R | ############################################
Trades 003864 |   2304.50 R | ##############################################
Trades 004032 |   2453.70 R | #################################################
Trades 004200 |   2523.90 R | ##################################################
Trades 004368 |   2597.10 R | ####################################################
Trades 004536 |   2709.30 R | ######################################################
Trades 004704 |   2830.00 R | ########################################################
Trades 004872 |   2918.20 R | ##########################################################
Trades 005040 |   3014.40 R | ############################################################
Trades 005208 |   3104.10 R | ##############################################################
Trades 005376 |   3204.80 R | ################################################################
Trades 005544 |   3287.00 R | ##################################################################
Trades 005712 |   3347.20 R | ###################################################################
Trades 005880 |   3430.40 R | ####################################################################
Trades 006048 |   3538.60 R | #######################################################################
Trades 006216 |   3615.30 R | ########################################################################
Trades 006384 |   3743.00 R | ###########################################################################
Trades 006552 |   3854.20 R | #############################################################################
Trades 006720 |   3957.40 R | ###############################################################################
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
