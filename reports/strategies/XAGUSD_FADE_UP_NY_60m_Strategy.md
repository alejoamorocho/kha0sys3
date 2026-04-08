# Reporte de Estrategia: XAGUSD NY 60m FADE_UP

**Status:** `[APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | XAGUSD |
| Sesion | NY (13:30 UTC) |
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
| Win Rate | `69.25%` | >= 65% [PASS] |
| Trades/Ano | `47.5` | >= 20 [PASS] |
| Profit Factor | `2.25` | > 1.0 [PASS] |
| Total Trades | `387` | - |
| Net R | `149.00R` | - |
| R Promedio/Trade | `0.385R` | - |
| Max Drawdown | `-6.00R` | - |
| Sharpe (anualizado) | `6.614` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 63 | 50 | `79.4%` | `37.0R` |
| 2019 | 46 | 29 | `63.0%` | `12.0R` |
| 2020 | 56 | 41 | `73.2%` | `26.0R` |
| 2021 | 34 | 27 | `79.4%` | `20.0R` |
| 2022 | 44 | 26 | `59.1%` | `8.0R` |
| 2023 | 34 | 26 | `76.5%` | `18.0R` |
| 2024 | 41 | 26 | `63.4%` | `11.0R` |
| 2025 | 51 | 33 | `64.7%` | `15.0R` |
| 2026 | 18 | 10 | `55.6%` | `2.0R` |

**Mejor ano:** 2018 | **Peor ano:** 2026

## Veredicto del Equipo Quant

> **ESTRATEGIA APROBADA.** WR=69.3%, PF=2.25, 48 trades/ano. Edge consistente y explotable.

---
*Generado por KHA0SYS3 Strategy Pipeline*
