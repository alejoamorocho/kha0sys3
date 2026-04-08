# Reporte de Estrategia: BRENT London 60m FADE_DOWN

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | BRENT |
| Sesion | London (07:00 UTC) |
| Duracion OR | 60 minutos |
| Arquetipo | FADE_DOWN |
| Direccion | DOWN |
| TP Multiplier | 1.0x OR |

### Logica de Ejecucion

Entrada CONTRA la rotura bajista. Cuando el precio rompe el OR, se entra en direccion opuesta apostando a que es un falso rompimiento. TP a 1x OR width (el extremo opuesto). SL a 1x OR width en la direccion del breakout. R:R = 1:1.

## Resultados del Backtest

### Metricas Principales

| Metrica | Valor | Umbral |
| --- | --- | --- |
| Win Rate | `60.98%` | >= 65% [FAIL] |
| Trades/Ano | `110.3` | >= 20 [PASS] |
| Profit Factor | `1.56` | > 1.0 [PASS] |
| Total Trades | `902` | - |
| Net R | `198.00R` | - |
| R Promedio/Trade | `0.220R` | - |
| Max Drawdown | `-14.00R` | - |
| Sharpe (anualizado) | `3.570` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 115 | 65 | `56.5%` | `15.0R` |
| 2019 | 99 | 65 | `65.7%` | `31.0R` |
| 2020 | 113 | 69 | `61.1%` | `25.0R` |
| 2021 | 111 | 69 | `62.2%` | `27.0R` |
| 2022 | 111 | 60 | `54.1%` | `9.0R` |
| 2023 | 112 | 70 | `62.5%` | `28.0R` |
| 2024 | 109 | 68 | `62.4%` | `27.0R` |
| 2025 | 106 | 63 | `59.4%` | `20.0R` |
| 2026 | 26 | 21 | `80.8%` | `16.0R` |

**Mejor ano:** 2019 | **Peor ano:** 2022

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: WR=61.0% < 65%. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
