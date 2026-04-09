# Comparación: LIMIT (FADE) vs STOP (MOMENTUM) vs MIXTO

> Balance inicial: $20,000 | Riesgo dinámico 1-6%
> Dedup: 1 trade/día/símbolo | TP: 1.5R

## Resultado Principal

| Métrica | A: FADE (LIMIT) | B: MOMENTUM (STOP) | C: MIXTO |
|:---|:---|:---|:---|
| **Balance Final** | `$637,641.76` | `$-638,978.82` | `$776,754.12` |
| **Ganancia $** | `$617,641.76` | `$-658,978.82` | `$756,754.12` |
| **Total Trades** | `18,192` | `17,383` | `18,037` |
| **Wins** | `11,167` | `7,203` | `10,985` |
| **Win Rate** | `61.4%` | `41.4%` | `60.9%` |
| **Profit Factor** | `1.22` | `0.85` | `1.26` |
| **Net R** | `1724.5R` | `-1680.7R` | `2095.6R` |
| **Max Drawdown** | `-20.9%` | `-2580.2%` | `-9.9%` |

## Rendimiento Anual Comparado

| Año | FADE WR | FADE PnL$ | MOM WR | MOM PnL$ | MIX WR | MIX PnL$ |
|:---|:---|:---|:---|:---|:---|:---|
| **2018** | `60.0%` | `$51,989` | `42.9%` | `$-47,894` | `60.7%` | `$87,858` |
| **2019** | `59.4%` | `$43,862` | `43.4%` | `$-36,948` | `58.8%` | `$55,563` |
| **2020** | `61.7%` | `$75,695` | `40.9%` | `$-83,767` | `60.0%` | `$73,816` |
| **2021** | `61.2%` | `$75,479` | `41.7%` | `$-76,873` | `60.9%` | `$94,279` |
| **2022** | `60.4%` | `$61,029` | `42.3%` | `$-68,129` | `60.5%` | `$87,964` |
| **2023** | `64.9%` | `$131,108` | `37.9%` | `$-149,254` | `64.5%` | `$149,697` |
| **2024** | `61.1%` | `$69,960` | `41.9%` | `$-74,406` | `60.4%` | `$82,797` |
| **2025** | `61.8%` | `$85,984` | `41.1%` | `$-91,872` | `61.4%` | `$105,009` |
| **2026** | `63.0%` | `$22,536` | `38.9%` | `$-29,835` | `60.3%` | `$19,772` |

## Comparación por Estrategia: FADE vs MOMENTUM

| Estrategia | FADE Trades | FADE WR | FADE Net R | MOM Trades | MOM WR | MOM Net R | Mejor |
|:---|:---|:---|:---|:---|:---|:---|:---|
| XAGUSD|London|FADE_UP|60m|BASE | 1022 | `62.2%` | `147.8` | 1022 | `37.6%` | `-164.2` | **FADE** |
| XAGUSD|London|FADE_UP|45m|BASE | 1033 | `62.1%` | `147.7` | 1033 | `37.9%` | `-158.8` | **FADE** |
| EURUSD|London|FADE_UP|60m|BASE | 952 | `62.3%` | `138.8` | 952 | `37.2%` | `-162.2` | **FADE** |
| WTI|NY Main|FADE_UP|45m|BASE | 807 | `63.4%` | `55.6` | 807 | `36.3%` | `-235.9` | **FADE** |
| EURUSD|London|FADE_UP|60m|GapSmall | 893 | `62.4%` | `131.7` | 893 | `37.1%` | `-154.8` | **FADE** |
| EURUSD|London|FADE_UP|45m|BASE | 978 | `61.6%` | `128.2` | 978 | `38.1%` | `-143.3` | **FADE** |
| AUDUSD|London|FADE_UP|45m|BASE | 980 | `61.5%` | `128.0` | 980 | `38.3%` | `-140.5` | **FADE** |
| XAGUSD|NY|FADE_UP|45m|BASE | 493 | `67.3%` | `121.7` | 493 | `32.3%` | `-144.8` | **FADE** |
| WTI|NY Main|FADE_UP|60m|BASE | 689 | `64.2%` | `57.2` | 689 | `35.8%` | `-209.3` | **FADE** |
| AUDUSD|London|FADE_UP|60m|BASE | 941 | `61.6%` | `124.9` | 941 | `38.0%` | `-140.1` | **FADE** |
| XAGUSD|London|FADE_UP|60m|GapSmall | 894 | `61.7%` | `120.6` | 894 | `38.0%` | `-133.4` | **FADE** |
| AUDUSD|London|FADE_UP|30m|BASE | 971 | `61.2%` | `119.9` | 971 | `38.5%` | `-133.1` | **FADE** |
| EURUSD|London|FADE_UP|45m|GapSmall | 909 | `61.5%` | `118.1` | 909 | `38.2%` | `-132.4` | **FADE** |
| BRENT|NY|FADE_UP|45m|BASE | 779 | `62.5%` | `39.2` | 779 | `37.4%` | `-207.3` | **FADE** |
| EURJPY|London|FADE_UP|45m|BASE | 968 | `61.1%` | `117.2` | 968 | `38.7%` | `-127.3` | **FADE** |
| SP500|NY Cash|FADE_UP|45m|GapSmall | 573 | `64.9%` | `56.4` | 573 | `35.1%` | `-185.1` | **FADE** |
| XAGUSD|NY|FADE_UP|60m|BASE | 387 | `69.3%` | `110.3` | 387 | `30.5%` | `-130.7` | **FADE** |
| WTI|NY Main|FADE_UP|30m|BASE | 867 | `61.6%` | `27.6` | 867 | `38.2%` | `-212.9` | **FADE** |
| XAGUSD|NY|FADE_UP|30m|BASE | 655 | `63.5%` | `111.5` | 655 | `36.2%` | `-128.0` | **FADE** |
| SP500|NY Cash|FADE_UP|45m|BASE | 673 | `63.4%` | `46.4` | 673 | `36.6%` | `-192.6` | **FADE** |
| XAGUSD|London|FADE_UP|45m|GapSmall | 902 | `61.3%` | `113.8` | 902 | `38.7%` | `-119.7` | **FADE** |
| EURJPY|London|FADE_UP|30m|BASE | 982 | `60.5%` | `107.8` | 982 | `39.2%` | `-117.7` | **FADE** |
| EURUSD|NY|FADE_UP|45m|BASE | 606 | `63.5%` | `103.4` | 606 | `36.5%` | `-114.1` | **FADE** |
| BRENT|London|FADE_UP|45m|BASE | 836 | `61.1%` | `18.8` | 836 | `38.6%` | `-195.7` | **FADE** |
| GBPJPY|Tokyo|FADE_UP|45m|BASE | 980 | `60.2%` | `102.0` | 980 | `39.5%` | `-110.5` | **FADE** |
| XAGUSD|NY|FADE_UP|45m|GapSmall | 368 | `67.9%` | `95.2` | 368 | `31.5%` | `-114.8` | **FADE** |
| EURJPY|London|FADE_UP|60m|BASE | 911 | `60.6%` | `101.9` | 911 | `39.3%` | `-107.1` | **FADE** |
| EURUSD|London|FADE_UP|45m|RSI_50-70 | 570 | `63.3%` | `95.0` | 570 | `36.1%` | `-112.0` | **FADE** |
| XAGUSD|NY|FADE_UP|30m|GapSmall | 488 | `64.5%` | `93.2` | 488 | `35.0%` | `-109.3` | **FADE** |
| BRENT|London|FADE_UP|45m|RSI_50-70 | 495 | `64.4%` | `44.0` | 495 | `35.4%` | `-156.5` | **FADE** |
| WTI|NY Main|FADE_UP|45m|GapSmall | 626 | `62.5%` | `30.8` | 626 | `37.2%` | `-168.7` | **FADE** |
| XAGUSD|London|FADE_UP|60m|RSI_50-70 | 600 | `62.7%` | `92.0` | 600 | `37.2%` | `-102.5` | **FADE** |
| BRENT|London|FADE_UP|45m|GapSmall | 760 | `61.1%` | `16.0` | 760 | `38.7%` | `-177.0` | **FADE** |
| WTI|NY Main|FADE_UP|45m|RSI_50-70 | 444 | `64.9%` | `43.2` | 444 | `34.7%` | `-147.8` | **FADE** |
| WTI|NY Main|FADE_UP|60m|GapSmall | 540 | `63.3%` | `36.0` | 540 | `36.7%` | `-153.0` | **FADE** |
| GBPUSD|NY|FADE_UP|60m|BASE | 526 | `63.5%` | `89.4` | 526 | `36.5%` | `-98.6` | **FADE** |
| EURUSD|London|FADE_UP|30m|RSI_50-70 | 557 | `62.7%` | `85.3` | 557 | `36.6%` | `-102.7` | **FADE** |
| GBPUSD|NY|FADE_DOWN|60m|BASE | 490 | `64.9%` | `97.0` | 472 | `36.4%` | `-89.2` | **FADE** |
| EURJPY|London|FADE_UP|45m|RSI_50-70 | 555 | `62.7%` | `85.5` | 555 | `36.9%` | `-98.0` | **FADE** |
| EURUSD|London|FADE_UP|60m|RSI_50-70 | 550 | `62.7%` | `85.0` | 550 | `36.9%` | `-97.5` | **FADE** |
| EURUSD|NY|FADE_UP|60m|BASE | 481 | `63.8%` | `84.9` | 481 | `36.2%` | `-94.1` | **FADE** |
| XAGUSD|NY|FADE_UP|60m|GapSmall | 286 | `69.2%` | `81.4` | 286 | `30.4%` | `-97.1` | **FADE** |
| WTI|NY Main|FADE_UP|30m|RSI_50-70 | 441 | `63.9%` | `34.8` | 441 | `35.6%` | `-136.7` | **FADE** |
| AUDUSD|London|FADE_UP|45m|RSI_50-70 | 568 | `62.0%` | `79.2` | 568 | `37.7%` | `-89.8` | **FADE** |
| WTI|NY Main|FADE_UP|60m|RSI_50-70 | 404 | `64.9%` | `39.2` | 404 | `35.1%` | `-129.8` | **FADE** |
| XAGUSD|NY|FADE_UP|30m|RSI_50-70 | 354 | `65.8%` | `76.6` | 354 | `33.9%` | `-89.4` | **FADE** |
| EURJPY|London|FADE_UP|60m|RSI_50-70 | 545 | `62.2%` | `78.5` | 545 | `37.6%` | `-87.0` | **FADE** |
| EURJPY|Tokyo|FADE_DOWN|60m|RSI_30-50 | 573 | `65.8%` | `123.7` | 471 | `41.4%` | `-30.6` | **FADE** |
| SP500|NY Cash|FADE_UP|45m|RSI_50-70 | 371 | `64.4%` | `32.8` | 371 | `35.6%` | `-115.2` | **FADE** |
| EURUSD|London|FADE_UP|60m|BtwCloseHigh | 330 | `65.5%` | `69.0` | 330 | `34.5%` | `-78.0` | **FADE** |
| EURUSD|NY|FADE_UP|45m|GapSmall | 427 | `63.0%` | `68.3` | 427 | `37.0%` | `-74.7` | **FADE** |
| USDJPY|Tokyo|FADE_UP|30m|BASE | 1012 | `58.5%` | `70.8` | 1012 | `41.2%` | `-70.7` | **FADE** |
| EURUSD|London|FADE_UP|60m|OR_Q1_Tight | 248 | `67.7%` | `63.2` | 248 | `31.5%` | `-77.8` | **FADE** |
| GBPUSD|NY|FADE_UP|60m|GapSmall | 346 | `64.5%` | `65.4` | 346 | `35.5%` | `-73.1` | **FADE** |
| XAGUSD|London|FADE_UP|30m|OR_Q4_Wide | 282 | `66.3%` | `63.8` | 282 | `33.7%` | `-72.7` | **FADE** |
| NATGAS|NY|FADE_DOWN|45m|BASE | 682 | `61.6%` | `21.6` | 638 | `40.9%` | `-113.1` | **FADE** |
| EURUSD|NY|FADE_DOWN|60m|BASE | 484 | `62.4%` | `71.6` | 467 | `38.8%` | `-61.2` | **FADE** |
| EURUSD|NY|FADE_UP|45m|RSI_50-70 | 327 | `64.5%` | `62.3` | 327 | `35.5%` | `-69.7` | **FADE** |
| EURUSD|London|FADE_UP|45m|BtwCloseHigh | 337 | `64.1%` | `61.3` | 337 | `35.9%` | `-68.2` | **FADE** |
| XAGUSD|London|FADE_UP|60m|OR_Q4_Wide | 271 | `66.1%` | `59.9` | 271 | `33.9%` | `-68.1` | **FADE** |
| EURJPY|London|FADE_UP|45m|BtwCloseHigh | 338 | `63.9%` | `60.2` | 338 | `36.1%` | `-66.8` | **FADE** |
| BRENT|London|FADE_UP|45m|OR_Q4_Wide | 250 | `66.4%` | `32.0` | 250 | `33.6%` | `-90.0` | **FADE** |
| XAGUSD|London|FADE_UP|45m|RSI_30-50 | 323 | `63.8%` | `56.7` | 323 | `36.2%` | `-62.8` | **FADE** |
| GBPAUD|London|FADE_DOWN|60m|BASE | 887 | `61.6%` | `116.3` | 771 | `43.8%` | `-3.1` | **FADE** |
| AUDUSD|London|FADE_UP|60m|RSI_30-50 | 292 | `64.4%` | `54.8` | 292 | `35.3%` | `-63.7` | **FADE** |
| XAGUSD|London|FADE_UP|15m|OR_Q4_Wide | 243 | `66.3%` | `54.7` | 243 | `33.7%` | `-62.3` | **FADE** |
| GBPAUD|London|FADE_DOWN|60m|GapSmall | 749 | `62.2%` | `108.1` | 644 | `43.5%` | `-8.4` | **FADE** |
| XAGUSD|NY|FADE_UP|45m|RSI_50-70 | 293 | `64.2%` | `53.7` | 293 | `35.5%` | `-62.3` | **FADE** |
| EURUSD|NY|FADE_UP|60m|RSI_50-70 | 268 | `64.9%` | `53.2` | 268 | `35.1%` | `-59.8` | **FADE** |
| GBPUSD|NY|FADE_DOWN|60m|GapSmall | 346 | `63.6%` | `59.4` | 333 | `37.8%` | `-51.3` | **FADE** |
| XAGUSD|London|FADE_UP|45m|OR_Q4_Wide | 265 | `64.5%` | `50.5` | 265 | `35.5%` | `-56.5` | **FADE** |
| EURUSD|NY|FADE_DOWN|60m|GapSmall | 331 | `63.7%` | `57.9` | 317 | `37.9%` | `-48.7` | **FADE** |
| WTI|London Initial|FADE_UP|45m|OR_Q4_Wide | 264 | `64.0%` | `21.2` | 264 | `36.0%` | `-79.3` | **FADE** |
| VIX|NY Cash|FADE_DOWN|45m|BASE | 234 | `67.1%` | `33.2` | 214 | `36.0%` | `-64.3` | **FADE** |
| BRENT|NY|FADE_UP|60m|RSI_50-70 | 347 | `61.7%` | `11.6` | 347 | `38.3%` | `-83.9` | **FADE** |
| GBPUSD|NY|FADE_DOWN|60m|RSI_30-50 | 253 | `64.4%` | `47.7` | 244 | `36.9%` | `-43.4` | **FADE** |
| SP500|NY Cash|FADE_DOWN|30m|GapSmall | 602 | `61.6%` | `19.6` | 531 | `42.7%` | `-69.7` | **FADE** |
| GBPAUD|London|FADE_DOWN|45m|RSI_30-50 | 564 | `63.1%` | `91.6` | 468 | `44.2%` | `2.7` | **FADE** |
| VIX|NY Cash|FADE_DOWN|45m|GapSmall | 199 | `67.8%` | `31.2` | 181 | `35.4%` | `-57.2` | **FADE** |
| NASDAQ100|NY Cash|FADE_DOWN|45m|RSI_30-50 | 309 | `64.1%` | `25.2` | 279 | `39.4%` | `-59.8` | **FADE** |
| GBPAUD|London|FADE_DOWN|45m|GapSmall | 822 | `61.7%` | `109.8` | 680 | `46.0%` | `34.5` | **FADE** |
| SP500|Pre-Market|FADE_DOWN|45m|BtwCloseHigh | 249 | `68.7%` | `43.2` | 185 | `41.1%` | `-32.0` | **FADE** |
| VIX|NY Cash|FADE_DOWN|45m|RSI_30-50 | 124 | `69.4%` | `23.2` | 115 | `33.0%` | `-43.0` | **FADE** |
| GBPJPY|London|FADE_DOWN|45m|BtwCloseHigh | 289 | `64.4%` | `54.1` | 244 | `42.2%` | `-10.9` | **FADE** |
| EURJPY|Tokyo|FADE_DOWN|60m|BtwLowClose | 318 | `63.8%` | `56.2` | 263 | `43.7%` | `-1.8` | **FADE** |
| SP500|Pre-Market|FADE_DOWN|45m|GapSmall | 644 | `63.0%` | `39.2` | 499 | `46.5%` | `-18.8` | **FADE** |
| BRENT|London|FADE_DOWN|45m|BtwLowClose | 289 | `66.1%` | `35.2` | 212 | `46.2%` | `-9.4` | **FADE** |
| SP500|Pre-Market|FADE_DOWN|60m|BtwCloseHigh | 260 | `64.6%` | `24.0` | 204 | `44.1%` | `-19.8` | **FADE** |
| BRENT|London|FADE_DOWN|45m|RSI_30-50 | 484 | `64.9%` | `47.2` | 351 | `48.4%` | `3.8` | **FADE** |
| BRENT|London|FADE_DOWN|45m|BASE | 825 | `63.0%` | `50.0` | 626 | `48.6%` | `8.8` | **FADE** |
| BRENT|London|FADE_DOWN|45m|GapSmall | 761 | `63.1%` | `46.8` | 576 | `48.6%` | `8.8` | **FADE** |
| XAGUSD|London|FADE_DOWN|30m|OR_Q4_Wide | 203 | `65.0%` | `40.7` | 156 | `45.5%` | `5.9` | **FADE** |
| BRENT|London|FADE_DOWN|60m|RSI_30-50 | 523 | `62.5%` | `26.4` | 407 | `47.7%` | `-3.4` | **FADE** |
| EURJPY|Tokyo|FADE_DOWN|60m|BASE | 995 | `60.5%` | `109.5` | 817 | `48.0%` | `81.3` | **FADE** |
| EURJPY|Tokyo|FADE_DOWN|60m|GapSmall | 995 | `60.5%` | `109.5` | 817 | `48.0%` | `81.3` | **FADE** |
| GBPJPY|Tokyo|FADE_DOWN|60m|BtwCloseHigh | 598 | `62.2%` | `86.2` | 460 | `49.1%` | `59.0` | **FADE** |
| SP500|Pre-Market|FADE_DOWN|45m|BASE | 771 | `61.6%` | `24.8` | 601 | `48.1%` | `1.3` | **FADE** |
| BRENT|London|FADE_DOWN|60m|GapSmall | 828 | `61.2%` | `20.4` | 660 | `48.3%` | `5.5` | **FADE** |
| BRENT|London|FADE_DOWN|60m|BASE | 902 | `61.0%` | `17.6` | 718 | `48.7%` | `13.4` | **FADE** |
| GBPJPY|Tokyo|FADE_DOWN|60m|BASE | 980 | `60.6%` | `110.0` | 779 | `49.6%` | `108.1` | **FADE** |
| GBPJPY|Tokyo|FADE_DOWN|60m|GapSmall | 980 | `60.6%` | `110.0` | 779 | `49.6%` | `108.1` | **FADE** |
| GBPUSD|London|FADE_DOWN|60m|BASE | 945 | `58.9%` | `74.5` | 810 | `47.8%` | `76.5` | **MOM** |
| GBPJPY|London|FADE_DOWN|45m|BASE | 888 | `59.0%` | `71.2` | 760 | `47.9%` | `74.0` | **MOM** |
| XAGUSD|London|FADE_DOWN|60m|BASE | 898 | `60.1%` | `92.2` | 719 | `49.7%` | `101.6` | **MOM** |
| XAGUSD|London|FADE_DOWN|15m|BASE | 586 | `63.0%` | `93.4` | 391 | `55.2%` | `109.9` | **MOM** |
| XAGUSD|London|FADE_DOWN|15m|GapSmall | 505 | `62.6%` | `76.5` | 337 | `55.8%` | `99.3` | **MOM** |
| BRENT|London|FADE_DOWN|30m|BASE | 673 | `61.7%` | `22.4` | 484 | `53.3%` | `64.2` | **MOM** |
| XAGUSD|London|FADE_DOWN|30m|BASE | 797 | `61.1%` | `97.3` | 571 | `54.3%` | `146.9` | **MOM** |

### Resumen: 101 estrategias mejor como FADE, 7 mejor como MOMENTUM

---
### Notas
- **FADE (LIMIT):** Entrada contra el breakout. Sell Limit en OR_HIGH, Buy Limit en OR_LOW.
  Gana cuando el precio revierte al otro lado del OR (SL del breakout original).
- **MOMENTUM (STOP):** Entrada a favor del breakout. Buy Stop en OR_HIGH, Sell Stop en OR_LOW.
  Gana cuando el precio continúa 1.5x OR width más allá del breakout.
- **MIXTO:** Selecciona el mejor tipo de orden por estrategia individual (backtest Net R).
  Nota: selección con beneficio de hindsight — en live habría que validar con walk-forward.
