# Reporte de Estrategia: EURJPY Tokyo 60m FADE_DOWN

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | EURJPY |
| Sesion | Tokyo (00:00 UTC) |
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
| Win Rate | `60.50%` | >= 65% [FAIL] |
| Trades/Ano | `121.8` | >= 20 [PASS] |
| Profit Factor | `1.53` | > 1.0 [PASS] |
| Total Trades | `995` | - |
| Net R | `209.00R` | - |
| R Promedio/Trade | `0.210R` | - |
| Max Drawdown | `-11.00R` | - |
| Sharpe (anualizado) | `3.409` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 110 | 65 | `59.1%` | `20.0R` |
| 2019 | 122 | 65 | `53.3%` | `8.0R` |
| 2020 | 128 | 82 | `64.1%` | `36.0R` |
| 2021 | 121 | 70 | `57.9%` | `19.0R` |
| 2022 | 120 | 72 | `60.0%` | `24.0R` |
| 2023 | 127 | 80 | `63.0%` | `33.0R` |
| 2024 | 122 | 79 | `64.8%` | `36.0R` |
| 2025 | 124 | 78 | `62.9%` | `32.0R` |
| 2026 | 21 | 11 | `52.4%` | `1.0R` |

**Mejor ano:** 2020 | **Peor ano:** 2026

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: WR=60.5% < 65%. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
