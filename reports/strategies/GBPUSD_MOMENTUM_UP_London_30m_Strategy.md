# Reporte de Estrategia: GBPUSD London 30m MOMENTUM_UP

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | GBPUSD |
| Sesion | London (07:00 UTC) |
| Duracion OR | 30 minutos |
| Arquetipo | MOMENTUM_UP |
| Direccion | UP |
| TP Multiplier | 1.5x OR |

### Logica de Ejecucion

Entrada en la rotura alcista del Opening Range. TP fijo a 1.5x OR width. SL en el extremo opuesto del OR (1R riesgo).

## Resultados del Backtest

### Metricas Principales

| Metrica | Valor | Umbral |
| --- | --- | --- |
| Win Rate | `45.29%` | >= 65% [FAIL] |
| Trades/Ano | `112.9` | >= 20 [PASS] |
| Profit Factor | `1.24` | > 1.0 [PASS] |
| Total Trades | `923` | - |
| Net R | `122.00R` | - |
| R Promedio/Trade | `0.132R` | - |
| Max Drawdown | `-26.50R` | - |
| Sharpe (anualizado) | `1.685` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 104 | 54 | `51.9%` | `31.0R` |
| 2019 | 96 | 50 | `52.1%` | `29.0R` |
| 2020 | 112 | 50 | `44.6%` | `13.0R` |
| 2021 | 120 | 48 | `40.0%` | `0.0R` |
| 2022 | 121 | 54 | `44.6%` | `14.0R` |
| 2023 | 117 | 44 | `37.6%` | `-7.0R` |
| 2024 | 114 | 54 | `47.4%` | `21.0R` |
| 2025 | 114 | 54 | `47.4%` | `21.0R` |
| 2026 | 25 | 10 | `40.0%` | `0.0R` |

**Mejor ano:** 2018 | **Peor ano:** 2023

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: WR=45.3% < 65%. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
