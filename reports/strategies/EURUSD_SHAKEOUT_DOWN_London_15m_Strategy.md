# Reporte de Estrategia: EURUSD London 15m SHAKEOUT_DOWN

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | EURUSD |
| Sesion | London (07:00 UTC) |
| Duracion OR | 15 minutos |
| Arquetipo | SHAKEOUT_DOWN |
| Direccion | DOWN |
| TP Multiplier | 1.0x OR |

### Logica de Ejecucion

Re-entrada CORTA despues de un falso rompimiento. Espera a que el breakout falle (SL hit), luego re-entra en la direccion original del breakout apostando a que el mercado barre stops y luego continua. TP a 1x OR extension. R:R = 1:1.

## Resultados del Backtest

### Metricas Principales

| Metrica | Valor | Umbral |
| --- | --- | --- |
| Win Rate | `50.98%` | >= 65% [FAIL] |
| Trades/Ano | `50.4` | >= 20 [PASS] |
| Profit Factor | `1.04` | > 1.0 [PASS] |
| Total Trades | `410` | - |
| Net R | `8.00R` | - |
| R Promedio/Trade | `0.020R` | - |
| Max Drawdown | `-19.00R` | - |
| Sharpe (anualizado) | `0.309` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 58 | 24 | `41.4%` | `-10.0R` |
| 2019 | 48 | 28 | `58.3%` | `8.0R` |
| 2020 | 60 | 35 | `58.3%` | `10.0R` |
| 2021 | 59 | 25 | `42.4%` | `-9.0R` |
| 2022 | 44 | 29 | `65.9%` | `14.0R` |
| 2023 | 44 | 17 | `38.6%` | `-10.0R` |
| 2024 | 40 | 21 | `52.5%` | `2.0R` |
| 2025 | 49 | 24 | `49.0%` | `-1.0R` |
| 2026 | 8 | 6 | `75.0%` | `4.0R` |

**Mejor ano:** 2022 | **Peor ano:** 2018

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: WR=51.0% < 65%. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
