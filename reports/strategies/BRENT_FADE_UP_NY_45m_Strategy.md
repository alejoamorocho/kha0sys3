# Reporte de Estrategia: BRENT NY 45m FADE_UP

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | BRENT |
| Sesion | NY (13:00 UTC) |
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
| Win Rate | `62.52%` | >= 65% [FAIL] |
| Trades/Ano | `95.5` | >= 20 [PASS] |
| Profit Factor | `1.67` | > 1.0 [PASS] |
| Total Trades | `779` | - |
| Net R | `195.00R` | - |
| R Promedio/Trade | `0.250R` | - |
| Max Drawdown | `-11.00R` | - |
| Sharpe (anualizado) | `4.102` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 104 | 57 | `54.8%` | `10.0R` |
| 2019 | 106 | 59 | `55.7%` | `12.0R` |
| 2020 | 94 | 60 | `63.8%` | `26.0R` |
| 2021 | 87 | 62 | `71.3%` | `37.0R` |
| 2022 | 86 | 55 | `64.0%` | `24.0R` |
| 2023 | 92 | 66 | `71.7%` | `40.0R` |
| 2024 | 103 | 67 | `65.0%` | `31.0R` |
| 2025 | 83 | 48 | `57.8%` | `13.0R` |
| 2026 | 24 | 13 | `54.2%` | `2.0R` |

**Mejor ano:** 2023 | **Peor ano:** 2026

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: WR=62.5% < 65%. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
