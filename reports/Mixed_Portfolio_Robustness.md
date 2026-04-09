# Validación de Robustez — Portfolio MIXTO (101 FADE + 7 MOMENTUM)

> Balance: $20,000 | Riesgo dinámico 1-6%
> 101 FADE (LIMIT) + 7 MOMENTUM (STOP)

## Resultado del Portfolio
| Métrica | Valor |
|:---|:---|
| **Balance Final** | `$776,754.12` |
| **Ganancia** | `$756,754.12` (3784%) |
| **Trades** | `18,037` |
| **Win Rate** | `60.9%` |
| **Profit Factor** | `1.26` |
| **Net R** | `2095.6` |
| **Max Drawdown** | `-9.9%` |

## Rendimiento Anual
| Año | Trades | Wins | WR | PnL ($) | PnL (R) |
|:---|:---|:---|:---|:---|:---|
| **2018** | 2107 | 1279 | `60.7%` | `$87,858` | `256.7` |
| **2019** | 2124 | 1249 | `58.8%` | `$55,563` | `165.5` |
| **2020** | 2218 | 1330 | `60.0%` | `$73,816` | `210.4` |
| **2021** | 2158 | 1314 | `60.9%` | `$94,279` | `255.4` |
| **2022** | 2255 | 1365 | `60.5%` | `$87,964` | `245.7` |
| **2023** | 2205 | 1423 | `64.5%` | `$149,697` | `416.8` |
| **2024** | 2223 | 1343 | `60.4%` | `$82,797` | `222.9` |
| **2025** | 2253 | 1384 | `61.4%` | `$105,009` | `276.8` |
| **2026** | 494 | 298 | `60.3%` | `$19,772` | `45.4` |

## Monte Carlo — Portfolio (10,000 simulaciones)

| Percentil | Net R | PnL ($) |
|:---|:---|:---|
| **P5 (peor)** | `1869.1R` | `$652,634` |
| **P25** | `2002.8R` | `$699,309` |
| **P50 (mediana)** | `2097.2R` | `$732,262` |
| **P75** | `2188.1R` | `$764,019` |
| **P95 (mejor)** | `2319.4R` | `$809,865` |
| **Prob Ruina** | `0.0%` | |
| **Prob Profit** | `100.0%` | |
| **DD P5** | `-39.8R` | |
| **DD P50** | `-28.2R` | |

## Walk-Forward — Portfolio (3 folds rolling 60/40)

| Fold | Train Period | Test Period | WR Train | WR Test | PF Train | PF Test | Degradación |
|:---|:---|:---|:---|:---|:---|:---|:---|
| **1** | 2018-01-17 → 2022-12-23 | 2022-12-23 → 2026-03-24 | `60.2%` | `61.9%` | `1.23` | `1.31` | `0.0%` |
| **2** | 2019-09-13 → 2024-08-16 | 2024-08-16 → 2026-03-24 | `61.0%` | `61.4%` | `1.26` | `1.27` | `0.0%` |
| **Promedio** | | | | `61.6%` | | `1.29` | `0.0%` |

## Decay Analysis — Portfolio

**Decay Score: `1.17`** — **Tendencia: `MEJORANDO`**

| Período | Trades | WR | Expectativa | PnL (R) |
|:---|:---|:---|:---|:---|
| 2018-01-17 -> 2019-01-17 | 2206 | `60.9%` | `0.126R` | `278.3R` |
| 2019-01-17 -> 2020-01-17 | 2121 | `59.0%` | `0.081R` | `171.2R` |
| 2020-01-17 -> 2021-01-16 | 2206 | `59.5%` | `0.087R` | `191.1R` |
| 2021-01-16 -> 2022-01-16 | 2169 | `60.7%` | `0.114R` | `246.5R` |
| 2022-01-16 -> 2023-01-16 | 2242 | `60.6%` | `0.111R` | `249.7R` |
| 2023-01-16 -> 2024-01-16 | 2200 | `64.9%` | `0.197R` | `433.6R` |
| 2024-01-16 -> 2025-01-15 | 2225 | `59.6%` | `0.082R` | `182.9R` |
| 2025-01-15 -> 2026-01-15 | 2246 | `62.0%` | `0.134R` | `301.6R` |
| 2026-01-15 -> 2026-03-24 | 422 | `60.7%` | `0.096R` | `40.7R` |

## Las 7 Estrategias MOMENTUM (STOP)

Estas estrategias usan **SELL STOP / BUY STOP** en lugar de LIMIT:

| Estrategia | Tipo Orden | Trades | WR | WR OOS | MC Ruina | Decay |
|:---|:---|:---|:---|:---|:---|:---|
| GBPUSD|London|FADE_DOWN|60m|BASE | **STOP** | 810 | `47.8%` | `44.0%` | `1%` | `0.42` |
| GBPJPY|London|FADE_DOWN|45m|BASE | **STOP** | 760 | `47.9%` | `44.6%` | `2%` | `0.27` |
| XAGUSD|London|FADE_DOWN|60m|BASE | **STOP** | 719 | `49.7%` | `49.7%` | `0%` | `1.05` |
| XAGUSD|London|FADE_DOWN|15m|BASE | **STOP** | 391 | `55.2%` | `57.0%` | `0%` | `1.10` |
| XAGUSD|London|FADE_DOWN|15m|GapSmall | **STOP** | 337 | `55.8%` | `57.8%` | `0%` | `1.19` |
| BRENT|London|FADE_DOWN|30m|BASE | **STOP** | 484 | `53.3%` | `51.7%` | `1%` | `0.82` |
| XAGUSD|London|FADE_DOWN|30m|BASE | **STOP** | 571 | `54.3%` | `55.0%` | `0%` | `1.19` |

## Walk-Forward por Estrategia (todas, por degradación)

| Estrategia | Orden | Trades | WR IS | WR OOS | Deg | MC Ruina | Decay | Veredicto |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| XAGUSD|London|FADE_DOWN|30m|OR_Q4_Wide | LIMIT | 203 | `69.4%` | `53.4%` | `16.0%` | `0%` | `0.96` | **ALERTA** |
| EURUSD|London|FADE_UP|60m|BtwCloseHigh | LIMIT | 330 | `69.2%` | `57.2%` | `12.0%` | `0%` | `0.55` | **ALERTA** |
| XAGUSD|NY|FADE_UP|30m|RSI_50-70 | LIMIT | 354 | `67.7%` | `58.6%` | `9.1%` | `0%` | `0.50` | **ALERTA** |
| GBPUSD|NY|FADE_UP|60m|BASE | LIMIT | 526 | `65.7%` | `56.9%` | `8.8%` | `0%` | `0.62` | **ALERTA** |
| XAGUSD|London|FADE_UP|45m|RSI_30-50 | LIMIT | 323 | `66.6%` | `57.9%` | `8.7%` | `0%` | `0.57` | **ALERTA** |
| WTI|NY Main|FADE_UP|45m|RSI_50-70 | LIMIT | 444 | `68.2%` | `59.7%` | `8.5%` | `2%` | `1.33` | **ALERTA** |
| EURUSD|London|FADE_UP|45m|BtwCloseHigh | LIMIT | 337 | `66.3%` | `57.8%` | `8.5%` | `0%` | `0.33` | **ALERTA** |
| XAGUSD|London|FADE_UP|15m|OR_Q4_Wide | LIMIT | 243 | `69.0%` | `60.5%` | `8.5%` | `0%` | `1.11` | **ALERTA** |
| WTI|NY Main|FADE_UP|30m|RSI_50-70 | LIMIT | 441 | `66.3%` | `58.8%` | `7.5%` | `4%` | `0.62` | **VIGILA** |
| XAGUSD|NY|FADE_UP|60m|GapSmall | LIMIT | 286 | `71.3%` | `63.9%` | `7.4%` | `0%` | `0.42` | **VIGILA** |
| GBPUSD|NY|FADE_DOWN|60m|RSI_30-50 | LIMIT | 253 | `67.2%` | `60.1%` | `7.2%` | `0%` | `1.38` | **VIGILA** |
| GBPUSD|NY|FADE_DOWN|60m|GapSmall | LIMIT | 346 | `65.7%` | `59.0%` | `6.7%` | `0%` | `0.79` | **VIGILA** |
| EURUSD|NY|FADE_UP|45m|RSI_50-70 | LIMIT | 327 | `66.6%` | `59.9%` | `6.7%` | `0%` | `0.64` | **VIGILA** |
| EURUSD|London|FADE_UP|30m|RSI_50-70 | LIMIT | 557 | `64.1%` | `57.6%` | `6.4%` | `0%` | `1.20` | **VIGILA** |
| XAGUSD|NY|FADE_UP|60m|BASE | LIMIT | 387 | `70.3%` | `64.2%` | `6.1%` | `0%` | `0.33` | **VIGILA** |
| EURUSD|London|FADE_UP|45m|GapSmall | LIMIT | 909 | `62.8%` | `57.2%` | `5.5%` | `0%` | `0.92` | **VIGILA** |
| BRENT|London|FADE_UP|45m|RSI_50-70 | LIMIT | 495 | `65.0%` | `61.4%` | `5.1%` | `2%` | `0.64` | **VIGILA** |
| EURUSD|London|FADE_UP|45m|BASE | LIMIT | 978 | `62.6%` | `57.8%` | `4.8%` | `0%` | `0.92` | **VIGILA** |
| GBPUSD|NY|FADE_UP|60m|GapSmall | LIMIT | 346 | `65.5%` | `60.8%` | `4.7%` | `0%` | `1.10` | **VIGILA** |
| NASDAQ100|NY Cash|FADE_DOWN|45m|RSI_30-50 | LIMIT | 309 | `66.5%` | `61.8%` | `4.7%` | `7%` | `0.90` | **VIGILA** |
| GBPUSD|London|FADE_DOWN|60m|BASE | STOP | 810 | `48.5%` | `44.0%` | `4.5%` | `1%` | `0.42` | **VIGILA** |
| GBPUSD|NY|FADE_DOWN|60m|BASE | LIMIT | 490 | `66.7%` | `63.0%` | `4.4%` | `0%` | `1.17` | **VIGILA** |
| EURJPY|London|FADE_UP|45m|BASE | LIMIT | 968 | `61.6%` | `57.4%` | `4.2%` | `0%` | `0.30` | **VIGILA** |
| XAGUSD|NY|FADE_UP|45m|GapSmall | LIMIT | 368 | `69.5%` | `65.3%` | `4.2%` | `0%` | `1.10` | **VIGILA** |
| XAGUSD|NY|FADE_UP|30m|GapSmall | LIMIT | 488 | `65.4%` | `61.6%` | `3.8%` | `0%` | `0.50` | **VIGILA** |
| GBPJPY|London|FADE_DOWN|45m|BASE | STOP | 760 | `48.4%` | `44.6%` | `3.8%` | `2%` | `0.27` | **ALERTA** |
| SP500|NY Cash|FADE_DOWN|30m|GapSmall | LIMIT | 602 | `62.5%` | `59.1%` | `3.6%` | `21%` | `1.03` | **VIGILA** |
| EURUSD|London|FADE_UP|45m|RSI_50-70 | LIMIT | 570 | `64.5%` | `61.0%` | `3.5%` | `0%` | `1.23` | **VIGILA** |
| XAGUSD|London|FADE_UP|60m|OR_Q4_Wide | LIMIT | 271 | `66.7%` | `63.3%` | `3.4%` | `0%` | `0.14` | **ALERTA** |
| EURJPY|London|FADE_UP|30m|BASE | LIMIT | 982 | `60.8%` | `57.8%` | `3.0%` | `0%` | `0.73` | **VIGILA** |
| EURJPY|London|FADE_UP|45m|BtwCloseHigh | LIMIT | 338 | `62.4%` | `63.0%` | `2.8%` | `0%` | `0.67` | **OK** |
| BRENT|London|FADE_DOWN|30m|BASE | STOP | 484 | `53.6%` | `51.7%` | `2.8%` | `1%` | `0.82` | **OK** |
| EURJPY|London|FADE_UP|45m|RSI_50-70 | LIMIT | 555 | `62.3%` | `61.3%` | `2.7%` | `0%` | `0.53` | **OK** |
| XAGUSD|London|FADE_UP|45m|BASE | LIMIT | 1033 | `63.2%` | `60.7%` | `2.6%` | `0%` | `1.05` | **OK** |
| XAGUSD|NY|FADE_UP|45m|BASE | LIMIT | 493 | `67.8%` | `65.2%` | `2.5%` | `0%` | `1.03` | **OK** |
| VIX|NY Cash|FADE_DOWN|45m|RSI_30-50 | LIMIT | 124 | `69.6%` | `72.4%` | `2.5%` | `1%` | `0.80` | **OK** |
| SP500|NY Cash|FADE_UP|45m|RSI_50-70 | LIMIT | 371 | `65.1%` | `62.8%` | `2.3%` | `4%` | `0.58` | **OK** |
| EURUSD|London|FADE_UP|60m|GapSmall | LIMIT | 893 | `62.9%` | `60.7%` | `2.2%` | `0%` | `1.10` | **OK** |
| EURJPY|Tokyo|FADE_DOWN|60m|RSI_30-50 | LIMIT | 573 | `66.6%` | `65.3%` | `2.2%` | `0%` | `1.50` | **OK** |
| SP500|NY Cash|FADE_UP|45m|GapSmall | LIMIT | 573 | `65.3%` | `63.6%` | `2.2%` | `1%` | `0.43` | **OK** |
| EURJPY|London|FADE_UP|60m|RSI_50-70 | LIMIT | 545 | `62.1%` | `60.1%` | `2.1%` | `0%` | `0.40` | **OK** |
| NATGAS|NY|FADE_DOWN|45m|BASE | LIMIT | 682 | `62.3%` | `60.3%` | `2.1%` | `20%` | `1.08` | **OK** |
| BRENT|NY|FADE_UP|45m|BASE | LIMIT | 779 | `63.4%` | `62.7%` | `2.1%` | `7%` | `1.17` | **OK** |
| AUDUSD|London|FADE_UP|60m|RSI_30-50 | LIMIT | 292 | `64.9%` | `62.8%` | `2.0%` | `0%` | `0.48` | **OK** |
| BRENT|NY|FADE_UP|60m|RSI_50-70 | LIMIT | 347 | `61.3%` | `61.5%` | `2.0%` | `27%` | `1.31` | **OK** |
| XAGUSD|London|FADE_UP|45m|GapSmall | LIMIT | 902 | `61.9%` | `60.0%` | `1.9%` | `0%` | `1.20` | **OK** |
| EURJPY|London|FADE_UP|60m|BASE | LIMIT | 911 | `60.6%` | `59.7%` | `1.9%` | `0%` | `0.48` | **OK** |
| XAGUSD|NY|FADE_UP|30m|BASE | LIMIT | 655 | `63.7%` | `61.8%` | `1.9%` | `0%` | `0.97` | **OK** |
| XAGUSD|NY|FADE_UP|45m|RSI_50-70 | LIMIT | 293 | `64.3%` | `63.3%` | `1.7%` | `0%` | `0.95` | **OK** |
| XAGUSD|London|FADE_UP|30m|OR_Q4_Wide | LIMIT | 282 | `66.3%` | `66.4%` | `1.6%` | `0%` | `0.46` | **OK** |
| XAGUSD|London|FADE_DOWN|60m|BASE | STOP | 719 | `49.0%` | `49.7%` | `1.5%` | `0%` | `1.05` | **OK** |
| EURUSD|London|FADE_UP|60m|OR_Q1_Tight | LIMIT | 248 | `68.6%` | `67.2%` | `1.5%` | `0%` | `0.96` | **OK** |
| SP500|NY Cash|FADE_UP|45m|BASE | LIMIT | 673 | `63.5%` | `63.2%` | `1.4%` | `3%` | `0.83` | **OK** |
| WTI|NY Main|FADE_UP|60m|RSI_50-70 | LIMIT | 404 | `65.3%` | `67.7%` | `1.4%` | `2%` | `1.38` | **OK** |
| EURUSD|London|FADE_UP|60m|BASE | LIMIT | 952 | `62.5%` | `61.3%` | `1.2%` | `0%` | `1.17` | **OK** |
| XAGUSD|London|FADE_UP|60m|GapSmall | LIMIT | 894 | `62.1%` | `61.9%` | `1.1%` | `0%` | `1.20` | **OK** |
| XAGUSD|London|FADE_UP|60m|BASE | LIMIT | 1022 | `62.9%` | `62.5%` | `1.0%` | `0%` | `1.30` | **OK** |
| EURUSD|NY|FADE_UP|45m|BASE | LIMIT | 606 | `63.4%` | `63.2%` | `0.9%` | `0%` | `0.92` | **OK** |
| BRENT|London|FADE_DOWN|45m|BtwLowClose | LIMIT | 289 | `66.2%` | `67.4%` | `0.8%` | `2%` | `1.19` | **OK** |
| EURUSD|London|FADE_UP|60m|RSI_50-70 | LIMIT | 550 | `62.1%` | `62.7%` | `0.8%` | `0%` | `0.92` | **OK** |
| SP500|Pre-Market|FADE_DOWN|45m|BASE | LIMIT | 771 | `60.9%` | `61.7%` | `0.7%` | `18%` | `1.08` | **OK** |
| XAGUSD|London|FADE_UP|45m|OR_Q4_Wide | LIMIT | 265 | `64.2%` | `65.6%` | `0.6%` | `0%` | `0.74` | **OK** |
| USDJPY|Tokyo|FADE_UP|30m|BASE | LIMIT | 1012 | `58.4%` | `59.1%` | `0.6%` | `1%` | `0.78` | **OK** |
| XAGUSD|London|FADE_UP|60m|RSI_50-70 | LIMIT | 600 | `62.6%` | `64.0%` | `0.5%` | `0%` | `1.12` | **OK** |
| GBPJPY|Tokyo|FADE_UP|45m|BASE | LIMIT | 980 | `59.4%` | `60.7%` | `0.4%` | `0%` | `0.48` | **OK** |
| WTI|NY Main|FADE_UP|45m|GapSmall | LIMIT | 626 | `62.3%` | `64.7%` | `0.4%` | `10%` | `1.13` | **OK** |
| BRENT|London|FADE_DOWN|60m|RSI_30-50 | LIMIT | 523 | `62.1%` | `62.0%` | `0.3%` | `11%` | `1.07` | **OK** |
| WTI|NY Main|FADE_UP|30m|BASE | LIMIT | 867 | `61.4%` | `62.0%` | `0.3%` | `17%` | `1.13` | **OK** |
| EURJPY|Tokyo|FADE_DOWN|60m|BtwLowClose | LIMIT | 318 | `63.2%` | `64.2%` | `0.3%` | `0%` | `1.48` | **OK** |
| EURUSD|NY|FADE_DOWN|60m|BASE | LIMIT | 484 | `62.4%` | `65.0%` | `0.3%` | `0%` | `1.64` | **OK** |
| EURUSD|NY|FADE_UP|60m|RSI_50-70 | LIMIT | 268 | `64.1%` | `66.8%` | `0.3%` | `0%` | `1.43` | **OK** |
| SP500|Pre-Market|FADE_DOWN|45m|GapSmall | LIMIT | 644 | `62.3%` | `64.4%` | `0.2%` | `5%` | `1.48` | **OK** |
| EURJPY|Tokyo|FADE_DOWN|60m|BASE | LIMIT | 995 | `60.3%` | `62.1%` | `0.2%` | `0%` | `1.32` | **OK** |
| EURJPY|Tokyo|FADE_DOWN|60m|GapSmall | LIMIT | 995 | `60.3%` | `62.1%` | `0.2%` | `0%` | `1.32` | **OK** |
| WTI|NY Main|FADE_UP|45m|BASE | LIMIT | 807 | `63.2%` | `65.0%` | `0.1%` | `2%` | `1.20` | **OK** |
| GBPJPY|Tokyo|FADE_DOWN|60m|BASE | LIMIT | 980 | `60.4%` | `60.6%` | `0.1%` | `0%` | `0.83` | **OK** |
| GBPJPY|Tokyo|FADE_DOWN|60m|GapSmall | LIMIT | 980 | `60.4%` | `60.6%` | `0.1%` | `0%` | `0.83` | **OK** |
| BRENT|London|FADE_DOWN|45m|RSI_30-50 | LIMIT | 484 | `64.3%` | `65.0%` | `0.1%` | `1%` | `0.83` | **OK** |
| AUDUSD|London|FADE_UP|45m|BASE | LIMIT | 980 | `59.9%` | `64.7%` | `0.0%` | `0%` | `1.68` | **OK** |
| BRENT|London|FADE_DOWN|60m|BASE | LIMIT | 902 | `60.6%` | `62.3%` | `0.0%` | `28%` | `1.38` | **OK** |
| VIX|NY Cash|FADE_DOWN|45m|BASE | LIMIT | 234 | `66.1%` | `73.6%` | `0.0%` | `1%` | `1.80` | **OK** |
| SP500|Pre-Market|FADE_DOWN|45m|BtwCloseHigh | LIMIT | 249 | `67.1%` | `73.1%` | `0.0%` | `0%` | `1.31` | **OK** |
| VIX|NY Cash|FADE_DOWN|45m|GapSmall | LIMIT | 199 | `66.0%` | `75.2%` | `0.0%` | `1%` | `1.80` | **OK** |
| WTI|NY Main|FADE_UP|60m|BASE | LIMIT | 689 | `62.8%` | `68.2%` | `0.0%` | `1%` | `1.70` | **OK** |
| BRENT|London|FADE_UP|45m|OR_Q4_Wide | LIMIT | 250 | `63.0%` | `73.0%` | `0.0%` | `2%` | `1.14` | **OK** |
| BRENT|London|FADE_DOWN|45m|BASE | LIMIT | 825 | `62.4%` | `65.2%` | `0.0%` | `3%` | `1.45` | **OK** |
| BRENT|London|FADE_DOWN|45m|GapSmall | LIMIT | 761 | `62.6%` | `64.9%` | `0.0%` | `4%` | `1.18` | **OK** |
| EURUSD|NY|FADE_UP|60m|BASE | LIMIT | 481 | `62.5%` | `66.1%` | `0.0%` | `0%` | `1.25` | **OK** |
| WTI|NY Main|FADE_UP|60m|GapSmall | LIMIT | 540 | `62.3%` | `66.9%` | `0.0%` | `5%` | `1.48` | **OK** |
| GBPAUD|London|FADE_DOWN|45m|RSI_30-50 | LIMIT | 564 | `62.4%` | `64.9%` | `0.0%` | `0%` | `1.37` | **OK** |
| XAGUSD|London|FADE_DOWN|15m|BASE | STOP | 391 | `54.7%` | `57.0%` | `0.0%` | `0%` | `1.10` | **OK** |
| GBPAUD|London|FADE_DOWN|60m|GapSmall | LIMIT | 749 | `60.8%` | `67.2%` | `0.0%` | `0%` | `1.52` | **OK** |
| AUDUSD|London|FADE_UP|60m|BASE | LIMIT | 941 | `59.7%` | `66.0%` | `0.0%` | `0%` | `1.78` | **OK** |
| GBPAUD|London|FADE_DOWN|60m|BASE | LIMIT | 887 | `59.7%` | `67.7%` | `0.0%` | `0%` | `1.40` | **OK** |
| GBPAUD|London|FADE_DOWN|45m|GapSmall | LIMIT | 822 | `61.2%` | `64.7%` | `0.0%` | `0%` | `1.18` | **OK** |
| AUDUSD|London|FADE_UP|30m|BASE | LIMIT | 971 | `59.2%` | `64.4%` | `0.0%` | `0%` | `1.53` | **OK** |
| GBPJPY|London|FADE_DOWN|45m|BtwCloseHigh | LIMIT | 289 | `63.3%` | `71.7%` | `0.0%` | `0%` | `1.83` | **OK** |
| SP500|Pre-Market|FADE_DOWN|60m|BtwCloseHigh | LIMIT | 260 | `63.8%` | `67.3%` | `0.0%` | `6%` | `1.43` | **OK** |
| GBPJPY|Tokyo|FADE_DOWN|60m|BtwCloseHigh | LIMIT | 598 | `60.9%` | `62.4%` | `0.0%` | `0%` | `1.00` | **OK** |
| XAGUSD|London|FADE_DOWN|15m|GapSmall | STOP | 337 | `55.0%` | `57.8%` | `0.0%` | `0%` | `1.19` | **OK** |
| EURUSD|NY|FADE_DOWN|60m|GapSmall | LIMIT | 331 | `63.1%` | `65.0%` | `0.0%` | `0%` | `1.40` | **OK** |
| BRENT|London|FADE_DOWN|60m|GapSmall | LIMIT | 828 | `60.9%` | `62.4%` | `0.0%` | `23%` | `1.32` | **OK** |
| EURUSD|NY|FADE_UP|45m|GapSmall | LIMIT | 427 | `62.1%` | `65.8%` | `0.0%` | `0%` | `1.18` | **OK** |
| BRENT|London|FADE_UP|45m|BASE | LIMIT | 836 | `60.2%` | `62.7%` | `0.0%` | `25%` | `1.05` | **OK** |
| XAGUSD|London|FADE_DOWN|30m|BASE | STOP | 571 | `53.8%` | `55.0%` | `0.0%` | `0%` | `1.19` | **OK** |
| AUDUSD|London|FADE_UP|45m|RSI_50-70 | LIMIT | 568 | `58.8%` | `68.5%` | `0.0%` | `0%` | `1.77` | **OK** |
| WTI|London Initial|FADE_UP|45m|OR_Q4_Wide | LIMIT | 264 | `60.8%` | `72.3%` | `0.0%` | `9%` | `1.83` | **OK** |
| BRENT|London|FADE_UP|45m|GapSmall | LIMIT | 760 | `60.1%` | `62.5%` | `0.0%` | `27%` | `0.92` | **OK** |

### Resumen: 70 OK, 22 VIGILA, 10 ALERTA

---
### Configuración del Portfolio MIXTO

**101 FADE (LIMIT):** Sell Limit / Buy Limit en OR boundary.
Fadian el breakout. Ganan cuando el precio revierte.

**7 MOMENTUM (STOP):** Sell Stop / Buy Stop en OR boundary.
Siguen el breakout. Ganan cuando el precio continúa 1.5R.

| Estrategia STOP | Símbolo | Sesión | Duración | Lógica |
|:---|:---|:---|:---|:---|
| BRENT|London|FADE_DOWN|30m|BASE | BRENT | London | 30m | Breakout DOWN continúa en London → SELL STOP en OR_LOW |
| GBPJPY|London|FADE_DOWN|45m|BASE | GBPJPY | London | 45m | Breakout DOWN continúa en London → SELL STOP en OR_LOW |
| GBPUSD|London|FADE_DOWN|60m|BASE | GBPUSD | London | 60m | Breakout DOWN continúa en London → SELL STOP en OR_LOW |
| XAGUSD|London|FADE_DOWN|15m|BASE | XAGUSD | London | 15m | Breakout DOWN continúa en London → SELL STOP en OR_LOW |
| XAGUSD|London|FADE_DOWN|15m|GapSmall | XAGUSD | London | 15m | Breakout DOWN continúa en London → SELL STOP en OR_LOW |
| XAGUSD|London|FADE_DOWN|30m|BASE | XAGUSD | London | 30m | Breakout DOWN continúa en London → SELL STOP en OR_LOW |
| XAGUSD|London|FADE_DOWN|60m|BASE | XAGUSD | London | 60m | Breakout DOWN continúa en London → SELL STOP en OR_LOW |

> **Nota:** La selección FADE/MOMENTUM se hizo con hindsight sobre datos completos.
> Los resultados Walk-Forward validan si el edge se sostiene out-of-sample.
