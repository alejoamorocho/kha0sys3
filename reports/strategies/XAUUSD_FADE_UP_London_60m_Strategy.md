# Reporte de Estrategia: XAUUSD London 60m FADE_UP

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | XAUUSD |
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
| Win Rate | `56.89%` | >= 65% [FAIL] |
| Trades/Ano | `119.8` | >= 20 [PASS] |
| Profit Factor | `1.32` | > 1.0 [PASS] |
| Total Trades | `979` | - |
| Net R | `135.00R` | - |
| R Promedio/Trade | `0.138R` | - |
| Max Drawdown | `-11.00R` | - |
| Sharpe (anualizado) | `2.209` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 106 | 53 | `50.0%` | `0.0R` |
| 2019 | 118 | 68 | `57.6%` | `18.0R` |
| 2020 | 130 | 71 | `54.6%` | `12.0R` |
| 2021 | 105 | 61 | `58.1%` | `17.0R` |
| 2022 | 121 | 72 | `59.5%` | `23.0R` |
| 2023 | 117 | 68 | `58.1%` | `19.0R` |
| 2024 | 125 | 73 | `58.4%` | `21.0R` |
| 2025 | 135 | 73 | `54.1%` | `11.0R` |
| 2026 | 22 | 18 | `81.8%` | `14.0R` |

**Mejor ano:** 2022 | **Peor ano:** 2018

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: WR=56.9% < 65%. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
