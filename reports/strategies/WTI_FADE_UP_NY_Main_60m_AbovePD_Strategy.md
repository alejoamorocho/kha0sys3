# Reporte de Estrategia: WTI NY Main 60m FADE_UP | color_position_vs_pd, op==, valABOVE_PD_HIGH, labelAbovePD

**Status:** `[APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | WTI |
| Sesion | NY Main (13:00 UTC) |
| Duracion OR | 60 minutos |
| Arquetipo | FADE_UP |
| Direccion | UP |
| TP Multiplier | 1.0x OR |
| Filtro Contextual | `AbovePD` |

### Logica de Ejecucion

Entrada CONTRA la rotura alcista. Cuando el precio rompe el OR, se entra en direccion opuesta apostando a que es un falso rompimiento. TP a 1x OR width (el extremo opuesto). SL a 1x OR width en la direccion del breakout. R:R = 1:1.

**Filtro activo:** Solo opera cuando `or_position_vs_pd == ABOVE_PD_HIGH`

## Resultados del Backtest

### Metricas Principales

| Metrica | Valor | Umbral |
| --- | --- | --- |
| Win Rate | `70.00%` | >= 65% [PASS] |
| Trades/Ano | `22.3` | >= 20 [PASS] |
| Profit Factor | `2.33` | > 1.0 [PASS] |
| Total Trades | `180` | - |
| Net R | `72.00R` | - |
| R Promedio/Trade | `0.400R` | - |
| Max Drawdown | `-4.00R` | - |
| Sharpe (anualizado) | `6.909` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 17 | 9 | `52.9%` | `1.0R` |
| 2019 | 26 | 18 | `69.2%` | `10.0R` |
| 2020 | 22 | 14 | `63.6%` | `6.0R` |
| 2021 | 20 | 15 | `75.0%` | `10.0R` |
| 2022 | 19 | 14 | `73.7%` | `9.0R` |
| 2023 | 23 | 20 | `87.0%` | `17.0R` |
| 2024 | 28 | 17 | `60.7%` | `6.0R` |
| 2025 | 18 | 12 | `66.7%` | `6.0R` |
| 2026 | 7 | 7 | `100.0%` | `7.0R` |

**Mejor ano:** 2023 | **Peor ano:** 2018

## Veredicto del Equipo Quant

> **ESTRATEGIA APROBADA.** WR=70.0%, PF=2.33, 22 trades/ano. Edge consistente y explotable.

---
*Generado por KHA0SYS3 Strategy Pipeline*
