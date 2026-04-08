# Reporte de Estrategia: USDJPY Tokyo 30m FADE_UP

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | USDJPY |
| Sesion | Tokyo (00:00 UTC) |
| Duracion OR | 30 minutos |
| Arquetipo | FADE_UP |
| Direccion | UP |
| TP Multiplier | 1.0x OR |

### Logica de Ejecucion

Entrada CONTRA la rotura alcista. Cuando el precio rompe el OR, se entra en direccion opuesta apostando a que es un falso rompimiento. TP a 1x OR width (el extremo opuesto). SL a 1x OR width en la direccion del breakout. R:R = 1:1.

## Resultados del Backtest

### Metricas Principales

| Metrica | Valor | Umbral |
| --- | --- | --- |
| Win Rate | `58.50%` | >= 65% [FAIL] |
| Trades/Ano | `123.8` | >= 20 [PASS] |
| Profit Factor | `1.41` | > 1.0 [PASS] |
| Total Trades | `1012` | - |
| Net R | `172.00R` | - |
| R Promedio/Trade | `0.170R` | - |
| Max Drawdown | `-10.00R` | - |
| Sharpe (anualizado) | `2.737` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 126 | 69 | `54.8%` | `12.0R` |
| 2019 | 122 | 74 | `60.7%` | `26.0R` |
| 2020 | 127 | 84 | `66.1%` | `41.0R` |
| 2021 | 128 | 67 | `52.3%` | `6.0R` |
| 2022 | 127 | 71 | `55.9%` | `15.0R` |
| 2023 | 112 | 69 | `61.6%` | `26.0R` |
| 2024 | 116 | 69 | `59.5%` | `22.0R` |
| 2025 | 129 | 76 | `58.9%` | `23.0R` |
| 2026 | 25 | 13 | `52.0%` | `1.0R` |

**Mejor ano:** 2020 | **Peor ano:** 2026

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: WR=58.5% < 65%. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
