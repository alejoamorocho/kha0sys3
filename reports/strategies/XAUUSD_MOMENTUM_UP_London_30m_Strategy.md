# Reporte de Estrategia: XAUUSD London 30m MOMENTUM_UP

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | XAUUSD |
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
| Win Rate | `45.27%` | >= 65% [FAIL] |
| Trades/Ano | `109.9` | >= 20 [PASS] |
| Profit Factor | `1.24` | > 1.0 [PASS] |
| Total Trades | `899` | - |
| Net R | `118.50R` | - |
| R Promedio/Trade | `0.132R` | - |
| Max Drawdown | `-30.50R` | - |
| Sharpe (anualizado) | `1.681` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 107 | 55 | `51.4%` | `30.5R` |
| 2019 | 114 | 55 | `48.2%` | `23.5R` |
| 2020 | 112 | 54 | `48.2%` | `23.0R` |
| 2021 | 99 | 35 | `35.4%` | `-11.5R` |
| 2022 | 119 | 48 | `40.3%` | `1.0R` |
| 2023 | 106 | 51 | `48.1%` | `21.5R` |
| 2024 | 117 | 50 | `42.7%` | `8.0R` |
| 2025 | 104 | 52 | `50.0%` | `26.0R` |
| 2026 | 21 | 7 | `33.3%` | `-3.5R` |

**Mejor ano:** 2018 | **Peor ano:** 2021

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: WR=45.3% < 65%. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
