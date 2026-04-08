# Reporte de Estrategia: GBPJPY London 45m FADE_DOWN

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | GBPJPY |
| Sesion | London (07:00 UTC) |
| Duracion OR | 45 minutos |
| Arquetipo | FADE_DOWN |
| Direccion | DOWN |
| TP Multiplier | 1.0x OR |

### Logica de Ejecucion

Entrada CONTRA la rotura bajista. Cuando el precio rompe el OR, se entra en direccion opuesta apostando a que es un falso rompimiento. TP a 1x OR width (el extremo opuesto). SL a 1x OR width en la direccion del breakout. R:R = 1:1.

## Resultados del Backtest

### Metricas Principales

| Metrica | Valor | Umbral |
| --- | --- | --- |
| Win Rate | `59.01%` | >= 65% [FAIL] |
| Trades/Ano | `108.5` | >= 20 [PASS] |
| Profit Factor | `1.44` | > 1.0 [PASS] |
| Total Trades | `888` | - |
| Net R | `160.00R` | - |
| R Promedio/Trade | `0.180R` | - |
| Max Drawdown | `-10.00R` | - |
| Sharpe (anualizado) | `2.906` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 131 | 71 | `54.2%` | `11.0R` |
| 2019 | 119 | 62 | `52.1%` | `5.0R` |
| 2020 | 110 | 71 | `64.5%` | `32.0R` |
| 2021 | 106 | 61 | `57.5%` | `16.0R` |
| 2022 | 95 | 52 | `54.7%` | `9.0R` |
| 2023 | 116 | 74 | `63.8%` | `32.0R` |
| 2024 | 95 | 59 | `62.1%` | `23.0R` |
| 2025 | 95 | 61 | `64.2%` | `27.0R` |
| 2026 | 21 | 13 | `61.9%` | `5.0R` |

**Mejor ano:** 2020 | **Peor ano:** 2019

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: WR=59.0% < 65%. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
