# Reporte de Estrategia: XAGUSD London 60m FADE_DOWN

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | XAGUSD |
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
| Win Rate | `60.13%` | >= 65% [FAIL] |
| Trades/Ano | `110.2` | >= 20 [PASS] |
| Profit Factor | `1.51` | > 1.0 [PASS] |
| Total Trades | `898` | - |
| Net R | `182.00R` | - |
| R Promedio/Trade | `0.203R` | - |
| Max Drawdown | `-17.00R` | - |
| Sharpe (anualizado) | `3.284` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 106 | 54 | `50.9%` | `2.0R` |
| 2019 | 112 | 73 | `65.2%` | `34.0R` |
| 2020 | 101 | 70 | `69.3%` | `39.0R` |
| 2021 | 130 | 78 | `60.0%` | `26.0R` |
| 2022 | 118 | 67 | `56.8%` | `16.0R` |
| 2023 | 112 | 67 | `59.8%` | `22.0R` |
| 2024 | 105 | 72 | `68.6%` | `39.0R` |
| 2025 | 98 | 49 | `50.0%` | `0.0R` |
| 2026 | 16 | 10 | `62.5%` | `4.0R` |

**Mejor ano:** 2020 | **Peor ano:** 2025

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: WR=60.1% < 65%. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
