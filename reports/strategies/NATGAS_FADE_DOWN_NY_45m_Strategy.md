# Reporte de Estrategia: NATGAS NY 45m FADE_DOWN

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | NATGAS |
| Sesion | NY (13:00 UTC) |
| Duracion OR | 45 minutos |
| Arquetipo | FADE_DOWN |
| Direccion | DOWN |
| TP Multiplier | 1.0x OR |

### Logica de Ejecucion

Entrada CONTRA la rotura bajista. Cuando el precio rompe el OR, se entra en direccion opuesta apostando a que es un falso rompimiento. TP a 1x OR width (el extremo opuesto). SL a 1x OR width en la direccion del breakout. R:R = 1:1.

## Resultados del Backtest

### Metricas Principales

| Metrica | Valor | Umbral |
| --- | --- | --- |
| Win Rate | `61.58%` | >= 65% [FAIL] |
| Trades/Ano | `83.5` | >= 20 [PASS] |
| Profit Factor | `1.60` | > 1.0 [PASS] |
| Total Trades | `682` | - |
| Net R | `158.00R` | - |
| R Promedio/Trade | `0.232R` | - |
| Max Drawdown | `-7.00R` | - |
| Sharpe (anualizado) | `3.778` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 74 | 45 | `60.8%` | `16.0R` |
| 2019 | 81 | 53 | `65.4%` | `25.0R` |
| 2020 | 82 | 46 | `56.1%` | `10.0R` |
| 2021 | 80 | 52 | `65.0%` | `24.0R` |
| 2022 | 89 | 60 | `67.4%` | `31.0R` |
| 2023 | 72 | 46 | `63.9%` | `20.0R` |
| 2024 | 87 | 47 | `54.0%` | `7.0R` |
| 2025 | 97 | 58 | `59.8%` | `19.0R` |
| 2026 | 20 | 13 | `65.0%` | `6.0R` |

**Mejor ano:** 2022 | **Peor ano:** 2026

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: WR=61.6% < 65%. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
