# Reporte de Estrategia: VIX NY Cash 60m FADE_DOWN | color_position_vs_pd, op==, valBETWEEN_LOW_AND_CLOSE, labelBtwLowClose

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | VIX |
| Sesion | NY Cash (13:30 UTC) |
| Duracion OR | 60 minutos |
| Arquetipo | FADE_DOWN |
| Direccion | DOWN |
| TP Multiplier | 1.0x OR |
| Filtro Contextual | `BtwLowClose` |

### Logica de Ejecucion

Entrada CONTRA la rotura bajista. Cuando el precio rompe el OR, se entra en direccion opuesta apostando a que es un falso rompimiento. TP a 1x OR width (el extremo opuesto). SL a 1x OR width en la direccion del breakout. R:R = 1:1.

**Filtro activo:** Solo opera cuando `or_position_vs_pd == BETWEEN_LOW_AND_CLOSE`

## Resultados del Backtest

### Metricas Principales

| Metrica | Valor | Umbral |
| --- | --- | --- |
| Win Rate | `73.02%` | >= 65% [PASS] |
| Trades/Ano | `19.5` | >= 20 [FAIL] |
| Profit Factor | `2.71` | > 1.0 [PASS] |
| Total Trades | `63` | - |
| Net R | `29.00R` | - |
| R Promedio/Trade | `0.460R` | - |
| Max Drawdown | `-2.00R` | - |
| Sharpe (anualizado) | `8.166` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2022 | 1 | 0 | `0.0%` | `-1.0R` |
| 2023 | 19 | 13 | `68.4%` | `7.0R` |
| 2024 | 21 | 16 | `76.2%` | `11.0R` |
| 2025 | 15 | 12 | `80.0%` | `9.0R` |
| 2026 | 7 | 5 | `71.4%` | `3.0R` |

**Mejor ano:** 2024 | **Peor ano:** 2022

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: Trades/ano=19 < 20. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
