# Reporte de Estrategia: SP500 Pre-Market 15m SHAKEOUT_UP | colatr_change, op>, val0.1, labelATR+10%

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | SP500 |
| Sesion | Pre-Market (12:00 UTC) |
| Duracion OR | 15 minutos |
| Arquetipo | SHAKEOUT_UP |
| Direccion | UP |
| TP Multiplier | 1.0x OR |
| Filtro Contextual | `ATR+10%` |

### Logica de Ejecucion

Re-entrada LARGA despues de un falso rompimiento. Espera a que el breakout falle (SL hit), luego re-entra en la direccion original del breakout apostando a que el mercado barre stops y luego continua. TP a 1x OR extension. R:R = 1:1.

**Filtro activo:** Solo opera cuando `atr_change > 0.1`

## Resultados del Backtest

### Metricas Principales

| Metrica | Valor | Umbral |
| --- | --- | --- |
| Win Rate | `82.35%` | >= 65% [PASS] |
| Trades/Ano | `4.3` | >= 20 [FAIL] |
| Profit Factor | `4.67` | > 1.0 [PASS] |
| Total Trades | `34` | - |
| Net R | `22.00R` | - |
| R Promedio/Trade | `0.647R` | - |
| Max Drawdown | `-1.00R` | - |
| Sharpe (anualizado) | `13.273` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 3 | 3 | `100.0%` | `3.0R` |
| 2019 | 3 | 3 | `100.0%` | `3.0R` |
| 2020 | 8 | 6 | `75.0%` | `4.0R` |
| 2021 | 5 | 5 | `100.0%` | `5.0R` |
| 2022 | 4 | 3 | `75.0%` | `2.0R` |
| 2023 | 4 | 3 | `75.0%` | `2.0R` |
| 2024 | 4 | 3 | `75.0%` | `2.0R` |
| 2025 | 2 | 2 | `100.0%` | `2.0R` |
| 2026 | 1 | 0 | `0.0%` | `-1.0R` |

**Mejor ano:** 2021 | **Peor ano:** 2026

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: Trades/ano=4 < 20. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
