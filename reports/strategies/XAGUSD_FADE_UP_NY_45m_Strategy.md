# Reporte de Estrategia: XAGUSD NY 45m FADE_UP

**Status:** `[APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | XAGUSD |
| Sesion | NY (13:30 UTC) |
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
| Win Rate | `67.34%` | >= 65% [PASS] |
| Trades/Ano | `60.6` | >= 20 [PASS] |
| Profit Factor | `2.06` | > 1.0 [PASS] |
| Total Trades | `493` | - |
| Net R | `171.00R` | - |
| R Promedio/Trade | `0.347R` | - |
| Max Drawdown | `-6.00R` | - |
| Sharpe (anualizado) | `5.865` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 71 | 50 | `70.4%` | `29.0R` |
| 2019 | 62 | 35 | `56.5%` | `8.0R` |
| 2020 | 68 | 53 | `77.9%` | `38.0R` |
| 2021 | 50 | 37 | `74.0%` | `24.0R` |
| 2022 | 55 | 31 | `56.4%` | `7.0R` |
| 2023 | 44 | 34 | `77.3%` | `24.0R` |
| 2024 | 52 | 35 | `67.3%` | `18.0R` |
| 2025 | 73 | 45 | `61.6%` | `17.0R` |
| 2026 | 18 | 12 | `66.7%` | `6.0R` |

**Mejor ano:** 2020 | **Peor ano:** 2026

## Veredicto del Equipo Quant

> **ESTRATEGIA APROBADA.** WR=67.3%, PF=2.06, 61 trades/ano. Edge consistente y explotable.

---
*Generado por KHA0SYS3 Strategy Pipeline*
