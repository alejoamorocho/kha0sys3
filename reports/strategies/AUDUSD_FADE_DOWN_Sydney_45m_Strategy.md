# Reporte de Estrategia: AUDUSD Sydney 45m FADE_DOWN

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | AUDUSD |
| Sesion | Sydney (22:00 UTC) |
| Duracion OR | 45 minutos |
| Arquetipo | FADE_DOWN |
| Direccion | DOWN |
| TP Multiplier | 1.0x OR |

### Logica de Ejecucion

Entrada CONTRA la rotura bajista. Cuando el precio rompe el OR, se entra en direccion opuesta apostando a que es un falso rompimiento. TP a 1x OR width (el extremo opuesto). SL a 1x OR width en la direccion del breakout. R:R = 1:1.

## Resultados del Backtest

### Metricas Principales

| Metrica | Valor | Umbral |
| --- | --- | --- |
| Win Rate | `73.58%` | >= 65% [PASS] |
| Trades/Ano | `13.2` | >= 20 [FAIL] |
| Profit Factor | `2.79` | > 1.0 [PASS] |
| Total Trades | `106` | - |
| Net R | `50.00R` | - |
| R Promedio/Trade | `0.472R` | - |
| Max Drawdown | `-3.00R` | - |
| Sharpe (anualizado) | `8.452` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 19 | 15 | `78.9%` | `11.0R` |
| 2019 | 19 | 15 | `78.9%` | `11.0R` |
| 2020 | 21 | 14 | `66.7%` | `7.0R` |
| 2021 | 12 | 8 | `66.7%` | `4.0R` |
| 2022 | 10 | 5 | `50.0%` | `0.0R` |
| 2023 | 3 | 3 | `100.0%` | `3.0R` |
| 2024 | 7 | 5 | `71.4%` | `3.0R` |
| 2025 | 12 | 11 | `91.7%` | `10.0R` |
| 2026 | 3 | 2 | `66.7%` | `1.0R` |

**Mejor ano:** 2018 | **Peor ano:** 2022

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: Trades/ano=13 < 20. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
