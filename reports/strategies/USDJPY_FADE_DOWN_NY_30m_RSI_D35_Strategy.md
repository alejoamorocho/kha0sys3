# Reporte de Estrategia: USDJPY NY 30m FADE_DOWN | colrsi_daily_14, op<, val35, labelRSI_D<35

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | USDJPY |
| Sesion | NY (13:30 UTC) |
| Duracion OR | 30 minutos |
| Arquetipo | FADE_DOWN |
| Direccion | DOWN |
| TP Multiplier | 1.0x OR |
| Filtro Contextual | `RSI_D<35` |

### Logica de Ejecucion

Entrada CONTRA la rotura bajista. Cuando el precio rompe el OR, se entra en direccion opuesta apostando a que es un falso rompimiento. TP a 1x OR width (el extremo opuesto). SL a 1x OR width en la direccion del breakout. R:R = 1:1.

**Filtro activo:** Solo opera cuando `rsi_daily_14 < 35`

## Resultados del Backtest

### Metricas Principales

| Metrica | Valor | Umbral |
| --- | --- | --- |
| Win Rate | `72.46%` | >= 65% [PASS] |
| Trades/Ano | `8.6` | >= 20 [FAIL] |
| Profit Factor | `2.63` | > 1.0 [PASS] |
| Total Trades | `69` | - |
| Net R | `31.00R` | - |
| R Promedio/Trade | `0.449R` | - |
| Max Drawdown | `-4.00R` | - |
| Sharpe (anualizado) | `7.925` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 15 | 10 | `66.7%` | `5.0R` |
| 2019 | 12 | 10 | `83.3%` | `8.0R` |
| 2020 | 8 | 7 | `87.5%` | `6.0R` |
| 2021 | 2 | 2 | `100.0%` | `2.0R` |
| 2023 | 10 | 6 | `60.0%` | `2.0R` |
| 2024 | 13 | 10 | `76.9%` | `7.0R` |
| 2025 | 7 | 4 | `57.1%` | `1.0R` |
| 2026 | 2 | 1 | `50.0%` | `0.0R` |

**Mejor ano:** 2019 | **Peor ano:** 2026

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: Trades/ano=9 < 20. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
