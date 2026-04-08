# Reporte de Estrategia: AUDUSD London 45m FADE_UP

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | AUDUSD |
| Sesion | London (07:00 UTC) |
| Duracion OR | 45 minutos |
| Arquetipo | FADE_UP |
| Direccion | UP |
| TP Multiplier | 1.0x OR |

### Logica de Ejecucion

Entrada CONTRA la rotura alcista. Cuando el precio rompe el OR, se entra en direccion opuesta apostando a que es un falso rompimiento. TP a 1x OR width (el extremo opuesto). SL a 1x OR width en la direccion del breakout. R:R = 1:1.

## Resultados del Backtest

### Metricas Principales

| Metrica | Valor | Umbral |
| --- | --- | --- |
| Win Rate | `61.53%` | >= 65% [FAIL] |
| Trades/Ano | `119.8` | >= 20 [PASS] |
| Profit Factor | `1.60` | > 1.0 [PASS] |
| Total Trades | `980` | - |
| Net R | `226.00R` | - |
| R Promedio/Trade | `0.231R` | - |
| Max Drawdown | `-10.00R` | - |
| Sharpe (anualizado) | `3.760` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 120 | 78 | `65.0%` | `36.0R` |
| 2019 | 112 | 58 | `51.8%` | `4.0R` |
| 2020 | 126 | 75 | `59.5%` | `24.0R` |
| 2021 | 118 | 70 | `59.3%` | `22.0R` |
| 2022 | 135 | 82 | `60.7%` | `29.0R` |
| 2023 | 109 | 74 | `67.9%` | `39.0R` |
| 2024 | 119 | 74 | `62.2%` | `29.0R` |
| 2025 | 117 | 75 | `64.1%` | `33.0R` |
| 2026 | 24 | 17 | `70.8%` | `10.0R` |

**Mejor ano:** 2023 | **Peor ano:** 2019

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: WR=61.5% < 65%. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
