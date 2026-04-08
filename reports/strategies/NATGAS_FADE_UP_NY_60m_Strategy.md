# Reporte de Estrategia: NATGAS NY 60m FADE_UP

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | NATGAS |
| Sesion | NY (13:00 UTC) |
| Duracion OR | 60 minutos |
| Arquetipo | FADE_UP |
| Direccion | UP |
| TP Multiplier | 1.0x OR |

### Logica de Ejecucion

Entrada CONTRA la rotura alcista. Cuando el precio rompe el OR, se entra en direccion opuesta apostando a que es un falso rompimiento. TP a 1x OR width (el extremo opuesto). SL a 1x OR width en la direccion del breakout. R:R = 1:1.

## Resultados del Backtest

### Metricas Principales

| Metrica | Valor | Umbral |
| --- | --- | --- |
| Win Rate | `61.92%` | >= 65% [FAIL] |
| Trades/Ano | `66.5` | >= 20 [PASS] |
| Profit Factor | `1.63` | > 1.0 [PASS] |
| Total Trades | `541` | - |
| Net R | `129.00R` | - |
| R Promedio/Trade | `0.238R` | - |
| Max Drawdown | `-7.00R` | - |
| Sharpe (anualizado) | `3.894` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 53 | 33 | `62.3%` | `13.0R` |
| 2019 | 57 | 38 | `66.7%` | `19.0R` |
| 2020 | 73 | 45 | `61.6%` | `17.0R` |
| 2021 | 72 | 46 | `63.9%` | `20.0R` |
| 2022 | 68 | 42 | `61.8%` | `16.0R` |
| 2023 | 73 | 49 | `67.1%` | `25.0R` |
| 2024 | 61 | 34 | `55.7%` | `7.0R` |
| 2025 | 62 | 36 | `58.1%` | `10.0R` |
| 2026 | 22 | 12 | `54.5%` | `2.0R` |

**Mejor ano:** 2023 | **Peor ano:** 2026

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: WR=61.9% < 65%. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
