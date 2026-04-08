# Reporte de Estrategia: GBPAUD Sydney 15m FADE_DOWN

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | GBPAUD |
| Sesion | Sydney (22:00 UTC) |
| Duracion OR | 15 minutos |
| Arquetipo | FADE_DOWN |
| Direccion | DOWN |
| TP Multiplier | 1.0x OR |

### Logica de Ejecucion

Entrada CONTRA la rotura bajista. Cuando el precio rompe el OR, se entra en direccion opuesta apostando a que es un falso rompimiento. TP a 1x OR width (el extremo opuesto). SL a 1x OR width en la direccion del breakout. R:R = 1:1.

## Resultados del Backtest

### Metricas Principales

| Metrica | Valor | Umbral |
| --- | --- | --- |
| Win Rate | `87.80%` | >= 65% [PASS] |
| Trades/Ano | `15.7` | >= 20 [FAIL] |
| Profit Factor | `7.20` | > 1.0 [PASS] |
| Total Trades | `123` | - |
| Net R | `93.00R` | - |
| R Promedio/Trade | `0.756R` | - |
| Max Drawdown | `-3.00R` | - |
| Sharpe (anualizado) | `18.265` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 8 | 8 | `100.0%` | `8.0R` |
| 2019 | 8 | 6 | `75.0%` | `4.0R` |
| 2020 | 24 | 24 | `100.0%` | `24.0R` |
| 2021 | 16 | 14 | `87.5%` | `12.0R` |
| 2022 | 20 | 19 | `95.0%` | `18.0R` |
| 2023 | 15 | 11 | `73.3%` | `7.0R` |
| 2024 | 19 | 15 | `78.9%` | `11.0R` |
| 2025 | 11 | 11 | `100.0%` | `11.0R` |
| 2026 | 2 | 0 | `0.0%` | `-2.0R` |

**Mejor ano:** 2020 | **Peor ano:** 2026

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: Trades/ano=16 < 20. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
