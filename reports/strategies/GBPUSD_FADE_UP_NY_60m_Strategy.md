# Reporte de Estrategia: GBPUSD NY 60m FADE_UP

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | GBPUSD |
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
| Win Rate | `63.50%` | >= 65% [FAIL] |
| Trades/Ano | `64.3` | >= 20 [PASS] |
| Profit Factor | `1.74` | > 1.0 [PASS] |
| Total Trades | `526` | - |
| Net R | `142.00R` | - |
| R Promedio/Trade | `0.270R` | - |
| Max Drawdown | `-7.00R` | - |
| Sharpe (anualizado) | `4.447` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 62 | 41 | `66.1%` | `20.0R` |
| 2019 | 77 | 52 | `67.5%` | `27.0R` |
| 2020 | 59 | 37 | `62.7%` | `15.0R` |
| 2021 | 60 | 39 | `65.0%` | `18.0R` |
| 2022 | 68 | 46 | `67.6%` | `24.0R` |
| 2023 | 47 | 31 | `66.0%` | `15.0R` |
| 2024 | 58 | 36 | `62.1%` | `14.0R` |
| 2025 | 71 | 36 | `50.7%` | `1.0R` |
| 2026 | 24 | 16 | `66.7%` | `8.0R` |

**Mejor ano:** 2019 | **Peor ano:** 2025

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: WR=63.5% < 65%. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
