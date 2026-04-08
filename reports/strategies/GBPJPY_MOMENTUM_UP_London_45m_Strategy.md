# Reporte de Estrategia: GBPJPY London 45m MOMENTUM_UP

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | GBPJPY |
| Sesion | London (07:00 UTC) |
| Duracion OR | 45 minutos |
| Arquetipo | MOMENTUM_UP |
| Direccion | UP |
| TP Multiplier | 1.5x OR |

### Logica de Ejecucion

Entrada en la rotura alcista del Opening Range. TP fijo a 1.5x OR width. SL en el extremo opuesto del OR (1R riesgo).

## Resultados del Backtest

### Metricas Principales

| Metrica | Valor | Umbral |
| --- | --- | --- |
| Win Rate | `44.00%` | >= 65% [FAIL] |
| Trades/Ano | `118.2` | >= 20 [PASS] |
| Profit Factor | `1.18` | > 1.0 [PASS] |
| Total Trades | `966` | - |
| Net R | `96.50R` | - |
| R Promedio/Trade | `0.100R` | - |
| Max Drawdown | `-24.00R` | - |
| Sharpe (anualizado) | `1.277` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 93 | 40 | `43.0%` | `7.0R` |
| 2019 | 101 | 47 | `46.5%` | `16.5R` |
| 2020 | 123 | 48 | `39.0%` | `-3.0R` |
| 2021 | 129 | 55 | `42.6%` | `8.5R` |
| 2022 | 130 | 57 | `43.8%` | `12.5R` |
| 2023 | 108 | 46 | `42.6%` | `7.0R` |
| 2024 | 126 | 62 | `49.2%` | `29.0R` |
| 2025 | 127 | 57 | `44.9%` | `15.5R` |
| 2026 | 29 | 13 | `44.8%` | `3.5R` |

**Mejor ano:** 2024 | **Peor ano:** 2020

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: WR=44.0% < 65%. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
