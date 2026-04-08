# Reporte de Estrategia: VIX NY Cash 45m FADE_UP | color_position_vs_pd, op==, valBETWEEN_CLOSE_AND_HIGH, labelBtwCloseHigh

**Status:** `[APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | VIX |
| Sesion | NY Cash (13:30 UTC) |
| Duracion OR | 45 minutos |
| Arquetipo | FADE_UP |
| Direccion | UP |
| TP Multiplier | 1.0x OR |
| Filtro Contextual | `BtwCloseHigh` |

### Logica de Ejecucion

Entrada CONTRA la rotura alcista. Cuando el precio rompe el OR, se entra en direccion opuesta apostando a que es un falso rompimiento. TP a 1x OR width (el extremo opuesto). SL a 1x OR width en la direccion del breakout. R:R = 1:1.

**Filtro activo:** Solo opera cuando `or_position_vs_pd == BETWEEN_CLOSE_AND_HIGH`

## Resultados del Backtest

### Metricas Principales

| Metrica | Valor | Umbral |
| --- | --- | --- |
| Win Rate | `67.12%` | >= 65% [PASS] |
| Trades/Ano | `21.6` | >= 20 [PASS] |
| Profit Factor | `2.04` | > 1.0 [PASS] |
| Total Trades | `73` | - |
| Net R | `25.00R` | - |
| R Promedio/Trade | `0.342R` | - |
| Max Drawdown | `-3.00R` | - |
| Sharpe (anualizado) | `5.747` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2022 | 6 | 4 | `66.7%` | `2.0R` |
| 2023 | 17 | 10 | `58.8%` | `3.0R` |
| 2024 | 16 | 11 | `68.8%` | `6.0R` |
| 2025 | 26 | 19 | `73.1%` | `12.0R` |
| 2026 | 8 | 5 | `62.5%` | `2.0R` |

**Mejor ano:** 2025 | **Peor ano:** 2022

## Veredicto del Equipo Quant

> **ESTRATEGIA APROBADA.** WR=67.1%, PF=2.04, 22 trades/ano. Edge consistente y explotable.

---
*Generado por KHA0SYS3 Strategy Pipeline*
