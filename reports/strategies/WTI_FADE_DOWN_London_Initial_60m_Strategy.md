# Reporte de Estrategia: WTI London Initial 60m FADE_DOWN

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | WTI |
| Sesion | London Initial (07:00 UTC) |
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
| Win Rate | `58.98%` | >= 65% [FAIL] |
| Trades/Ano | `113.3` | >= 20 [PASS] |
| Profit Factor | `1.44` | > 1.0 [PASS] |
| Total Trades | `924` | - |
| Net R | `166.00R` | - |
| R Promedio/Trade | `0.180R` | - |
| Max Drawdown | `-11.00R` | - |
| Sharpe (anualizado) | `2.898` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 115 | 61 | `53.0%` | `7.0R` |
| 2019 | 104 | 72 | `69.2%` | `40.0R` |
| 2020 | 110 | 63 | `57.3%` | `16.0R` |
| 2021 | 113 | 66 | `58.4%` | `19.0R` |
| 2022 | 112 | 57 | `50.9%` | `2.0R` |
| 2023 | 117 | 72 | `61.5%` | `27.0R` |
| 2024 | 117 | 71 | `60.7%` | `25.0R` |
| 2025 | 109 | 61 | `56.0%` | `13.0R` |
| 2026 | 27 | 22 | `81.5%` | `17.0R` |

**Mejor ano:** 2019 | **Peor ano:** 2022

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: WR=59.0% < 65%. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
