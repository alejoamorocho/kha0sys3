# Reporte de Estrategia: GBPAUD London 60m FADE_UP

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | GBPAUD |
| Sesion | London (07:00 UTC) |
| Duracion OR | 60 minutos |
| Arquetipo | FADE_UP |
| Direccion | UP |
| TP Multiplier | 1.0x OR |

### Logica de Ejecucion

Entrada CONTRA la rotura alcista. Cuando el precio rompe el OR, se entra en direccion opuesta apostando a que es un falso rompimiento. TP a 1x OR width (el extremo opuesto). SL a 1x OR width en la direccion del breakout. R:R = 1:1.

## Resultados del Backtest

### Metricas Principales

| Metrica | Valor | Umbral |
| --- | --- | --- |
| Win Rate | `58.21%` | >= 65% [FAIL] |
| Trades/Ano | `114.8` | >= 20 [PASS] |
| Profit Factor | `1.39` | > 1.0 [PASS] |
| Total Trades | `938` | - |
| Net R | `154.00R` | - |
| R Promedio/Trade | `0.164R` | - |
| Max Drawdown | `-13.00R` | - |
| Sharpe (anualizado) | `2.641` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 119 | 65 | `54.6%` | `11.0R` |
| 2019 | 109 | 62 | `56.9%` | `15.0R` |
| 2020 | 105 | 61 | `58.1%` | `17.0R` |
| 2021 | 118 | 72 | `61.0%` | `26.0R` |
| 2022 | 114 | 72 | `63.2%` | `30.0R` |
| 2023 | 114 | 69 | `60.5%` | `24.0R` |
| 2024 | 118 | 65 | `55.1%` | `12.0R` |
| 2025 | 114 | 65 | `57.0%` | `16.0R` |
| 2026 | 27 | 15 | `55.6%` | `3.0R` |

**Mejor ano:** 2022 | **Peor ano:** 2026

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: WR=58.2% < 65%. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
