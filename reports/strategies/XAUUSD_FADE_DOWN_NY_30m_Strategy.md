# Reporte de Estrategia: XAUUSD NY 30m FADE_DOWN

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | XAUUSD |
| Sesion | NY (13:30 UTC) |
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
| Win Rate | `57.23%` | >= 65% [FAIL] |
| Trades/Ano | `79.6` | >= 20 [PASS] |
| Profit Factor | `1.34` | > 1.0 [PASS] |
| Total Trades | `650` | - |
| Net R | `94.00R` | - |
| R Promedio/Trade | `0.145R` | - |
| Max Drawdown | `-14.00R` | - |
| Sharpe (anualizado) | `2.318` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 84 | 49 | `58.3%` | `14.0R` |
| 2019 | 98 | 55 | `56.1%` | `12.0R` |
| 2020 | 75 | 52 | `69.3%` | `29.0R` |
| 2021 | 80 | 48 | `60.0%` | `16.0R` |
| 2022 | 75 | 37 | `49.3%` | `-1.0R` |
| 2023 | 57 | 29 | `50.9%` | `1.0R` |
| 2024 | 77 | 44 | `57.1%` | `11.0R` |
| 2025 | 83 | 46 | `55.4%` | `9.0R` |
| 2026 | 21 | 12 | `57.1%` | `3.0R` |

**Mejor ano:** 2020 | **Peor ano:** 2022

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: WR=57.2% < 65%. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
