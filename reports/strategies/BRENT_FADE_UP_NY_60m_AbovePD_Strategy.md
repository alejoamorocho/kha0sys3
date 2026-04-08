# Reporte de Estrategia: BRENT NY 60m FADE_UP | color_position_vs_pd, op==, valABOVE_PD_HIGH, labelAbovePD

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | BRENT |
| Sesion | NY (13:00 UTC) |
| Duracion OR | 60 minutos |
| Arquetipo | FADE_UP |
| Direccion | UP |
| TP Multiplier | 1.0x OR |
| Filtro Contextual | `AbovePD` |

### Logica de Ejecucion

Entrada CONTRA la rotura alcista. Cuando el precio rompe el OR, se entra en direccion opuesta apostando a que es un falso rompimiento. TP a 1x OR width (el extremo opuesto). SL a 1x OR width en la direccion del breakout. R:R = 1:1.

**Filtro activo:** Solo opera cuando `or_position_vs_pd == ABOVE_PD_HIGH`

## Resultados del Backtest

### Metricas Principales

| Metrica | Valor | Umbral |
| --- | --- | --- |
| Win Rate | `73.83%` | >= 65% [PASS] |
| Trades/Ano | `18.6` | >= 20 [FAIL] |
| Profit Factor | `2.82` | > 1.0 [PASS] |
| Total Trades | `149` | - |
| Net R | `71.00R` | - |
| R Promedio/Trade | `0.477R` | - |
| Max Drawdown | `-3.00R` | - |
| Sharpe (anualizado) | `8.575` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 15 | 9 | `60.0%` | `3.0R` |
| 2019 | 23 | 15 | `65.2%` | `7.0R` |
| 2020 | 19 | 14 | `73.7%` | `9.0R` |
| 2021 | 17 | 15 | `88.2%` | `13.0R` |
| 2022 | 15 | 12 | `80.0%` | `9.0R` |
| 2023 | 19 | 16 | `84.2%` | `13.0R` |
| 2024 | 20 | 15 | `75.0%` | `10.0R` |
| 2025 | 12 | 7 | `58.3%` | `2.0R` |
| 2026 | 9 | 7 | `77.8%` | `5.0R` |

**Mejor ano:** 2021 | **Peor ano:** 2025

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: Trades/ano=19 < 20. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
