# Reporte de Estrategia: WTI NY Main 45m FADE_UP

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | WTI |
| Sesion | NY Main (13:00 UTC) |
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
| Win Rate | `63.44%` | >= 65% [FAIL] |
| Trades/Ano | `98.8` | >= 20 [PASS] |
| Profit Factor | `1.74` | > 1.0 [PASS] |
| Total Trades | `807` | - |
| Net R | `217.00R` | - |
| R Promedio/Trade | `0.269R` | - |
| Max Drawdown | `-13.00R` | - |
| Sharpe (anualizado) | `4.429` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 105 | 58 | `55.2%` | `11.0R` |
| 2019 | 100 | 59 | `59.0%` | `18.0R` |
| 2020 | 99 | 58 | `58.6%` | `17.0R` |
| 2021 | 94 | 63 | `67.0%` | `32.0R` |
| 2022 | 85 | 61 | `71.8%` | `37.0R` |
| 2023 | 98 | 71 | `72.4%` | `44.0R` |
| 2024 | 114 | 71 | `62.3%` | `28.0R` |
| 2025 | 89 | 58 | `65.2%` | `27.0R` |
| 2026 | 23 | 13 | `56.5%` | `3.0R` |

**Mejor ano:** 2023 | **Peor ano:** 2026

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: WR=63.4% < 65%. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
