# Reporte de Estrategia: GBPAUD Sydney 30m FADE_DOWN

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | GBPAUD |
| Sesion | Sydney (22:00 UTC) |
| Duracion OR | 30 minutos |
| Arquetipo | FADE_DOWN |
| Direccion | DOWN |
| TP Multiplier | 1.0x OR |

### Logica de Ejecucion

Entrada CONTRA la rotura bajista. Cuando el precio rompe el OR, se entra en direccion opuesta apostando a que es un falso rompimiento. TP a 1x OR width (el extremo opuesto). SL a 1x OR width en la direccion del breakout. R:R = 1:1.

## Resultados del Backtest

### Metricas Principales

| Metrica | Valor | Umbral |
| --- | --- | --- |
| Win Rate | `91.26%` | >= 65% [PASS] |
| Trades/Ano | `12.7` | >= 20 [FAIL] |
| Profit Factor | `10.44` | > 1.0 [PASS] |
| Total Trades | `103` | - |
| Net R | `85.00R` | - |
| R Promedio/Trade | `0.825R` | - |
| Max Drawdown | `-1.00R` | - |
| Sharpe (anualizado) | `23.083` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 9 | 9 | `100.0%` | `9.0R` |
| 2019 | 7 | 6 | `85.7%` | `5.0R` |
| 2020 | 21 | 18 | `85.7%` | `15.0R` |
| 2021 | 8 | 7 | `87.5%` | `6.0R` |
| 2022 | 14 | 13 | `92.9%` | `12.0R` |
| 2023 | 12 | 11 | `91.7%` | `10.0R` |
| 2024 | 14 | 13 | `92.9%` | `12.0R` |
| 2025 | 13 | 13 | `100.0%` | `13.0R` |
| 2026 | 5 | 4 | `80.0%` | `3.0R` |

**Mejor ano:** 2020 | **Peor ano:** 2026

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: Trades/ano=13 < 20. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
