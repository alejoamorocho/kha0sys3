# Reporte de Estrategia: EURJPY London 45m FADE_UP

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | EURJPY |
| Sesion | London (07:00 UTC) |
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
| Win Rate | `61.05%` | >= 65% [FAIL] |
| Trades/Ano | `118.4` | >= 20 [PASS] |
| Profit Factor | `1.57` | > 1.0 [PASS] |
| Total Trades | `968` | - |
| Net R | `214.00R` | - |
| R Promedio/Trade | `0.221R` | - |
| Max Drawdown | `-10.00R` | - |
| Sharpe (anualizado) | `3.597` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 112 | 80 | `71.4%` | `48.0R` |
| 2019 | 112 | 70 | `62.5%` | `28.0R` |
| 2020 | 112 | 68 | `60.7%` | `24.0R` |
| 2021 | 123 | 77 | `62.6%` | `31.0R` |
| 2022 | 124 | 79 | `63.7%` | `34.0R` |
| 2023 | 118 | 60 | `50.8%` | `2.0R` |
| 2024 | 122 | 74 | `60.7%` | `26.0R` |
| 2025 | 120 | 68 | `56.7%` | `16.0R` |
| 2026 | 25 | 15 | `60.0%` | `5.0R` |

**Mejor ano:** 2018 | **Peor ano:** 2023

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: WR=61.1% < 65%. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
