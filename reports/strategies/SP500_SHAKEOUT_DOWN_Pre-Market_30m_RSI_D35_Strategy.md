# Reporte de Estrategia: SP500 Pre-Market 30m SHAKEOUT_DOWN | colrsi_daily_14, op<, val35, labelRSI_D<35

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | SP500 |
| Sesion | Pre-Market (12:00 UTC) |
| Duracion OR | 30 minutos |
| Arquetipo | SHAKEOUT_DOWN |
| Direccion | DOWN |
| TP Multiplier | 1.0x OR |
| Filtro Contextual | `RSI_D<35` |

### Logica de Ejecucion

Re-entrada CORTA despues de un falso rompimiento. Espera a que el breakout falle (SL hit), luego re-entra en la direccion original del breakout apostando a que el mercado barre stops y luego continua. TP a 1x OR extension. R:R = 1:1.

**Filtro activo:** Solo opera cuando `rsi_daily_14 < 35`

## Resultados del Backtest

### Metricas Principales

| Metrica | Valor | Umbral |
| --- | --- | --- |
| Win Rate | `80.00%` | >= 65% [PASS] |
| Trades/Ano | `3.7` | >= 20 [FAIL] |
| Profit Factor | `4.00` | > 1.0 [PASS] |
| Total Trades | `30` | - |
| Net R | `18.00R` | - |
| R Promedio/Trade | `0.600R` | - |
| Max Drawdown | `-1.00R` | - |
| Sharpe (anualizado) | `11.706` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 5 | 5 | `100.0%` | `5.0R` |
| 2019 | 1 | 0 | `0.0%` | `-1.0R` |
| 2020 | 3 | 2 | `66.7%` | `1.0R` |
| 2021 | 1 | 1 | `100.0%` | `1.0R` |
| 2022 | 8 | 5 | `62.5%` | `2.0R` |
| 2023 | 5 | 4 | `80.0%` | `3.0R` |
| 2025 | 6 | 6 | `100.0%` | `6.0R` |
| 2026 | 1 | 1 | `100.0%` | `1.0R` |

**Mejor ano:** 2025 | **Peor ano:** 2019

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: Trades/ano=4 < 20. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
