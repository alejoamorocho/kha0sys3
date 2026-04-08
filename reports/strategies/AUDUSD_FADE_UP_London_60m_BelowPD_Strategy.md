# Reporte de Estrategia: AUDUSD London 60m FADE_UP | color_position_vs_pd, op==, valBELOW_PD_LOW, labelBelowPD

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | AUDUSD |
| Sesion | London (07:00 UTC) |
| Duracion OR | 60 minutos |
| Arquetipo | FADE_UP |
| Direccion | UP |
| TP Multiplier | 1.0x OR |
| Filtro Contextual | `BelowPD` |

### Logica de Ejecucion

Entrada CONTRA la rotura alcista. Cuando el precio rompe el OR, se entra en direccion opuesta apostando a que es un falso rompimiento. TP a 1x OR width (el extremo opuesto). SL a 1x OR width en la direccion del breakout. R:R = 1:1.

**Filtro activo:** Solo opera cuando `or_position_vs_pd == BELOW_PD_LOW`

## Resultados del Backtest

### Metricas Principales

| Metrica | Valor | Umbral |
| --- | --- | --- |
| Win Rate | `68.10%` | >= 65% [PASS] |
| Trades/Ano | `20.0` | >= 20 [FAIL] |
| Profit Factor | `2.13` | > 1.0 [PASS] |
| Total Trades | `163` | - |
| Net R | `59.00R` | - |
| R Promedio/Trade | `0.362R` | - |
| Max Drawdown | `-5.00R` | - |
| Sharpe (anualizado) | `6.145` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 25 | 17 | `68.0%` | `9.0R` |
| 2019 | 29 | 17 | `58.6%` | `5.0R` |
| 2020 | 18 | 11 | `61.1%` | `4.0R` |
| 2021 | 19 | 13 | `68.4%` | `7.0R` |
| 2022 | 20 | 14 | `70.0%` | `8.0R` |
| 2023 | 19 | 14 | `73.7%` | `9.0R` |
| 2024 | 15 | 8 | `53.3%` | `1.0R` |
| 2025 | 16 | 15 | `93.8%` | `14.0R` |
| 2026 | 2 | 2 | `100.0%` | `2.0R` |

**Mejor ano:** 2025 | **Peor ano:** 2024

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: Trades/ano=20 < 20. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
