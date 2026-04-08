# Reporte de Estrategia: EURUSD NY 60m FADE_DOWN | color_position_vs_pd, op==, valBELOW_PD_LOW, labelBelowPD

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | EURUSD |
| Sesion | NY (13:30 UTC) |
| Duracion OR | 60 minutos |
| Arquetipo | FADE_DOWN |
| Direccion | DOWN |
| TP Multiplier | 1.0x OR |
| Filtro Contextual | `BelowPD` |

### Logica de Ejecucion

Entrada CONTRA la rotura bajista. Cuando el precio rompe el OR, se entra en direccion opuesta apostando a que es un falso rompimiento. TP a 1x OR width (el extremo opuesto). SL a 1x OR width en la direccion del breakout. R:R = 1:1.

**Filtro activo:** Solo opera cuando `or_position_vs_pd == BELOW_PD_LOW`

## Resultados del Backtest

### Metricas Principales

| Metrica | Valor | Umbral |
| --- | --- | --- |
| Win Rate | `66.67%` | >= 65% [PASS] |
| Trades/Ano | `14.8` | >= 20 [FAIL] |
| Profit Factor | `2.00` | > 1.0 [PASS] |
| Total Trades | `120` | - |
| Net R | `40.00R` | - |
| R Promedio/Trade | `0.333R` | - |
| Max Drawdown | `-10.00R` | - |
| Sharpe (anualizado) | `5.589` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 16 | 9 | `56.2%` | `2.0R` |
| 2019 | 17 | 8 | `47.1%` | `-1.0R` |
| 2020 | 15 | 12 | `80.0%` | `9.0R` |
| 2021 | 10 | 6 | `60.0%` | `2.0R` |
| 2022 | 16 | 10 | `62.5%` | `4.0R` |
| 2023 | 12 | 11 | `91.7%` | `10.0R` |
| 2024 | 19 | 15 | `78.9%` | `11.0R` |
| 2025 | 13 | 8 | `61.5%` | `3.0R` |
| 2026 | 2 | 1 | `50.0%` | `0.0R` |

**Mejor ano:** 2024 | **Peor ano:** 2019

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: Trades/ano=15 < 20. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
