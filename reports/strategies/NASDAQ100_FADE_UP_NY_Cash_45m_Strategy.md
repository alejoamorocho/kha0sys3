# Reporte de Estrategia: NASDAQ100 NY Cash 45m FADE_UP

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | NASDAQ100 |
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
| Win Rate | `62.01%` | >= 65% [FAIL] |
| Trades/Ano | `68.4` | >= 20 [PASS] |
| Profit Factor | `1.63` | > 1.0 [PASS] |
| Total Trades | `558` | - |
| Net R | `134.00R` | - |
| R Promedio/Trade | `0.240R` | - |
| Max Drawdown | `-9.00R` | - |
| Sharpe (anualizado) | `3.924` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 63 | 43 | `68.3%` | `23.0R` |
| 2019 | 64 | 35 | `54.7%` | `6.0R` |
| 2020 | 78 | 51 | `65.4%` | `24.0R` |
| 2021 | 62 | 38 | `61.3%` | `14.0R` |
| 2022 | 65 | 48 | `73.8%` | `31.0R` |
| 2023 | 73 | 42 | `57.5%` | `11.0R` |
| 2024 | 74 | 43 | `58.1%` | `12.0R` |
| 2025 | 59 | 38 | `64.4%` | `17.0R` |
| 2026 | 20 | 8 | `40.0%` | `-4.0R` |

**Mejor ano:** 2022 | **Peor ano:** 2026

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: WR=62.0% < 65%. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
