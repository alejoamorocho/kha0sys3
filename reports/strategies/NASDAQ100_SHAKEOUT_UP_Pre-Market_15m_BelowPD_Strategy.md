# Reporte de Estrategia: NASDAQ100 Pre-Market 15m SHAKEOUT_UP | color_position_vs_pd, op==, valBELOW_PD_LOW, labelBelowPD

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | NASDAQ100 |
| Sesion | Pre-Market (12:00 UTC) |
| Duracion OR | 15 minutos |
| Arquetipo | SHAKEOUT_UP |
| Direccion | UP |
| TP Multiplier | 1.0x OR |
| Filtro Contextual | `BelowPD` |

### Logica de Ejecucion

Re-entrada LARGA despues de un falso rompimiento. Espera a que el breakout falle (SL hit), luego re-entra en la direccion original del breakout apostando a que el mercado barre stops y luego continua. TP a 1x OR extension. R:R = 1:1.

**Filtro activo:** Solo opera cuando `or_position_vs_pd == BELOW_PD_LOW`

## Resultados del Backtest

### Metricas Principales

| Metrica | Valor | Umbral |
| --- | --- | --- |
| Win Rate | `68.09%` | >= 65% [PASS] |
| Trades/Ano | `5.9` | >= 20 [FAIL] |
| Profit Factor | `2.13` | > 1.0 [PASS] |
| Total Trades | `47` | - |
| Net R | `17.00R` | - |
| R Promedio/Trade | `0.362R` | - |
| Max Drawdown | `-2.00R` | - |
| Sharpe (anualizado) | `6.093` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 7 | 3 | `42.9%` | `-1.0R` |
| 2019 | 5 | 4 | `80.0%` | `3.0R` |
| 2020 | 5 | 5 | `100.0%` | `5.0R` |
| 2021 | 6 | 4 | `66.7%` | `2.0R` |
| 2022 | 5 | 3 | `60.0%` | `1.0R` |
| 2023 | 4 | 3 | `75.0%` | `2.0R` |
| 2024 | 7 | 4 | `57.1%` | `1.0R` |
| 2025 | 5 | 4 | `80.0%` | `3.0R` |
| 2026 | 3 | 2 | `66.7%` | `1.0R` |

**Mejor ano:** 2020 | **Peor ano:** 2018

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: Trades/ano=6 < 20. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
