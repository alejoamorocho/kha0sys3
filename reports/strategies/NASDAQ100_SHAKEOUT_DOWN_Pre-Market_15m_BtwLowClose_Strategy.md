# Reporte de Estrategia: NASDAQ100 Pre-Market 15m SHAKEOUT_DOWN | color_position_vs_pd, op==, valBETWEEN_LOW_AND_CLOSE, labelBtwLowClose

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | NASDAQ100 |
| Sesion | Pre-Market (12:00 UTC) |
| Duracion OR | 15 minutos |
| Arquetipo | SHAKEOUT_DOWN |
| Direccion | DOWN |
| TP Multiplier | 1.0x OR |
| Filtro Contextual | `BtwLowClose` |

### Logica de Ejecucion

Re-entrada CORTA despues de un falso rompimiento. Espera a que el breakout falle (SL hit), luego re-entra en la direccion original del breakout apostando a que el mercado barre stops y luego continua. TP a 1x OR extension. R:R = 1:1.

**Filtro activo:** Solo opera cuando `or_position_vs_pd == BETWEEN_LOW_AND_CLOSE`

## Resultados del Backtest

### Metricas Principales

| Metrica | Valor | Umbral |
| --- | --- | --- |
| Win Rate | `66.67%` | >= 65% [PASS] |
| Trades/Ano | `8.4` | >= 20 [FAIL] |
| Profit Factor | `2.00` | > 1.0 [PASS] |
| Total Trades | `66` | - |
| Net R | `22.00R` | - |
| R Promedio/Trade | `0.333R` | - |
| Max Drawdown | `-4.00R` | - |
| Sharpe (anualizado) | `5.570` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 4 | 2 | `50.0%` | `0.0R` |
| 2019 | 8 | 5 | `62.5%` | `2.0R` |
| 2020 | 11 | 6 | `54.5%` | `1.0R` |
| 2021 | 7 | 6 | `85.7%` | `5.0R` |
| 2022 | 5 | 2 | `40.0%` | `-1.0R` |
| 2023 | 11 | 9 | `81.8%` | `7.0R` |
| 2024 | 4 | 3 | `75.0%` | `2.0R` |
| 2025 | 14 | 10 | `71.4%` | `6.0R` |
| 2026 | 2 | 1 | `50.0%` | `0.0R` |

**Mejor ano:** 2023 | **Peor ano:** 2022

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: Trades/ano=8 < 20. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
