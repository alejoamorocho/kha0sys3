# Reporte de Estrategia: SP500 NY Cash 45m FADE_UP

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | SP500 |
| Sesion | NY Cash (13:30 UTC) |
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
| Win Rate | `63.45%` | >= 65% [FAIL] |
| Trades/Ano | `82.5` | >= 20 [PASS] |
| Profit Factor | `1.74` | > 1.0 [PASS] |
| Total Trades | `673` | - |
| Net R | `181.00R` | - |
| R Promedio/Trade | `0.269R` | - |
| Max Drawdown | `-7.00R` | - |
| Sharpe (anualizado) | `4.429` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 84 | 56 | `66.7%` | `28.0R` |
| 2019 | 82 | 50 | `61.0%` | `18.0R` |
| 2020 | 94 | 61 | `64.9%` | `28.0R` |
| 2021 | 82 | 56 | `68.3%` | `30.0R` |
| 2022 | 64 | 37 | `57.8%` | `10.0R` |
| 2023 | 80 | 47 | `58.8%` | `14.0R` |
| 2024 | 86 | 56 | `65.1%` | `26.0R` |
| 2025 | 81 | 55 | `67.9%` | `29.0R` |
| 2026 | 20 | 9 | `45.0%` | `-2.0R` |

**Mejor ano:** 2021 | **Peor ano:** 2026

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: WR=63.4% < 65%. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
