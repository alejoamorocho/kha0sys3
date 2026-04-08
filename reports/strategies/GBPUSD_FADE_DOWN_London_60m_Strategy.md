# Reporte de Estrategia: GBPUSD London 60m FADE_DOWN

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | GBPUSD |
| Sesion | London (07:00 UTC) |
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
| Win Rate | `58.94%` | >= 65% [FAIL] |
| Trades/Ano | `115.9` | >= 20 [PASS] |
| Profit Factor | `1.44` | > 1.0 [PASS] |
| Total Trades | `945` | - |
| Net R | `169.00R` | - |
| R Promedio/Trade | `0.179R` | - |
| Max Drawdown | `-9.00R` | - |
| Sharpe (anualizado) | `2.884` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 122 | 68 | `55.7%` | `14.0R` |
| 2019 | 111 | 58 | `52.3%` | `5.0R` |
| 2020 | 111 | 73 | `65.8%` | `35.0R` |
| 2021 | 119 | 69 | `58.0%` | `19.0R` |
| 2022 | 107 | 59 | `55.1%` | `11.0R` |
| 2023 | 129 | 74 | `57.4%` | `19.0R` |
| 2024 | 110 | 68 | `61.8%` | `26.0R` |
| 2025 | 110 | 69 | `62.7%` | `28.0R` |
| 2026 | 26 | 19 | `73.1%` | `12.0R` |

**Mejor ano:** 2020 | **Peor ano:** 2019

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: WR=58.9% < 65%. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
