# Reporte de Estrategia: NATGAS NY 15m MOMENTUM_UP

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | NATGAS |
| Sesion | NY (13:00 UTC) |
| Duracion OR | 15 minutos |
| Arquetipo | MOMENTUM_UP |
| Direccion | UP |
| TP Multiplier | 1.5x OR |

### Logica de Ejecucion

Entrada en la rotura alcista del Opening Range. TP fijo a 1.5x OR width. SL en el extremo opuesto del OR (1R riesgo).

## Resultados del Backtest

### Metricas Principales

| Metrica | Valor | Umbral |
| --- | --- | --- |
| Win Rate | `46.28%` | >= 65% [FAIL] |
| Trades/Ano | `98.6` | >= 20 [PASS] |
| Profit Factor | `1.29` | > 1.0 [PASS] |
| Total Trades | `806` | - |
| Net R | `126.50R` | - |
| R Promedio/Trade | `0.157R` | - |
| Max Drawdown | `-28.00R` | - |
| Sharpe (anualizado) | `1.997` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 94 | 41 | `43.6%` | `8.5R` |
| 2019 | 89 | 40 | `44.9%` | `11.0R` |
| 2020 | 108 | 47 | `43.5%` | `9.5R` |
| 2021 | 101 | 56 | `55.4%` | `39.0R` |
| 2022 | 101 | 52 | `51.5%` | `29.0R` |
| 2023 | 94 | 52 | `55.3%` | `36.0R` |
| 2024 | 99 | 31 | `31.3%` | `-21.5R` |
| 2025 | 103 | 45 | `43.7%` | `9.5R` |
| 2026 | 17 | 9 | `52.9%` | `5.5R` |

**Mejor ano:** 2021 | **Peor ano:** 2024

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: WR=46.3% < 65%. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
