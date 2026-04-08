# Reporte de Estrategia: GBPJPY Tokyo 45m FADE_UP

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | GBPJPY |
| Sesion | Tokyo (00:00 UTC) |
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
| Win Rate | `60.20%` | >= 65% [FAIL] |
| Trades/Ano | `119.8` | >= 20 [PASS] |
| Profit Factor | `1.51` | > 1.0 [PASS] |
| Total Trades | `980` | - |
| Net R | `200.00R` | - |
| R Promedio/Trade | `0.204R` | - |
| Max Drawdown | `-9.00R` | - |
| Sharpe (anualizado) | `3.308` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 123 | 78 | `63.4%` | `33.0R` |
| 2019 | 113 | 74 | `65.5%` | `35.0R` |
| 2020 | 104 | 64 | `61.5%` | `24.0R` |
| 2021 | 129 | 72 | `55.8%` | `15.0R` |
| 2022 | 131 | 73 | `55.7%` | `15.0R` |
| 2023 | 112 | 69 | `61.6%` | `26.0R` |
| 2024 | 124 | 77 | `62.1%` | `30.0R` |
| 2025 | 118 | 72 | `61.0%` | `26.0R` |
| 2026 | 26 | 11 | `42.3%` | `-4.0R` |

**Mejor ano:** 2019 | **Peor ano:** 2026

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: WR=60.2% < 65%. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
