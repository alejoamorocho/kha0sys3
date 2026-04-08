# Reporte de Estrategia: EURJPY London 45m MOMENTUM_DOWN | colrsi_at_or_close, op>, val70, labelRSI>70

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | EURJPY |
| Sesion | London (07:00 UTC) |
| Duracion OR | 45 minutos |
| Arquetipo | MOMENTUM_DOWN |
| Direccion | DOWN |
| TP Multiplier | 1.5x OR |
| Filtro Contextual | `RSI>70` |

### Logica de Ejecucion

Entrada en la rotura bajista del Opening Range. TP fijo a 1.5x OR width. SL en el extremo opuesto del OR (1R riesgo).

**Filtro activo:** Solo opera cuando `rsi_at_or_close > 70`

## Resultados del Backtest

### Metricas Principales

| Metrica | Valor | Umbral |
| --- | --- | --- |
| Win Rate | `65.22%` | >= 65% [PASS] |
| Trades/Ano | `3.0` | >= 20 [FAIL] |
| Profit Factor | `2.81` | > 1.0 [PASS] |
| Total Trades | `23` | - |
| Net R | `14.50R` | - |
| R Promedio/Trade | `0.630R` | - |
| Max Drawdown | `-3.00R` | - |
| Sharpe (anualizado) | `8.220` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 4 | 4 | `100.0%` | `6.0R` |
| 2019 | 1 | 1 | `100.0%` | `1.5R` |
| 2020 | 1 | 1 | `100.0%` | `1.5R` |
| 2021 | 2 | 1 | `50.0%` | `0.5R` |
| 2022 | 4 | 2 | `50.0%` | `1.0R` |
| 2023 | 3 | 1 | `33.3%` | `-0.5R` |
| 2024 | 3 | 3 | `100.0%` | `4.5R` |
| 2025 | 4 | 2 | `50.0%` | `1.0R` |
| 2026 | 1 | 0 | `0.0%` | `-1.0R` |

**Mejor ano:** 2018 | **Peor ano:** 2026

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: Trades/ano=3 < 20. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
