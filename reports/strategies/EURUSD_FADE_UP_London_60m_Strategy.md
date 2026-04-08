# Reporte de Estrategia: EURUSD London 60m FADE_UP

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | EURUSD |
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
| Win Rate | `62.29%` | >= 65% [FAIL] |
| Trades/Ano | `116.4` | >= 20 [PASS] |
| Profit Factor | `1.65` | > 1.0 [PASS] |
| Total Trades | `952` | - |
| Net R | `234.00R` | - |
| R Promedio/Trade | `0.246R` | - |
| Max Drawdown | `-9.00R` | - |
| Sharpe (anualizado) | `4.023` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 107 | 68 | `63.6%` | `29.0R` |
| 2019 | 116 | 72 | `62.1%` | `28.0R` |
| 2020 | 117 | 68 | `58.1%` | `19.0R` |
| 2021 | 106 | 68 | `64.2%` | `30.0R` |
| 2022 | 120 | 78 | `65.0%` | `36.0R` |
| 2023 | 126 | 87 | `69.0%` | `48.0R` |
| 2024 | 119 | 63 | `52.9%` | `7.0R` |
| 2025 | 115 | 68 | `59.1%` | `21.0R` |
| 2026 | 26 | 21 | `80.8%` | `16.0R` |

**Mejor ano:** 2023 | **Peor ano:** 2024

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: WR=62.3% < 65%. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
