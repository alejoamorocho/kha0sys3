# Reporte de Estrategia: VIX NY Cash 45m FADE_DOWN

**Status:** `[APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | VIX |
| Sesion | NY Cash (13:30 UTC) |
| Duracion OR | 45 minutos |
| Arquetipo | FADE_DOWN |
| Direccion | DOWN |
| TP Multiplier | 1.0x OR |

### Logica de Ejecucion

Entrada CONTRA la rotura bajista. Cuando el precio rompe el OR, se entra en direccion opuesta apostando a que es un falso rompimiento. TP a 1x OR width (el extremo opuesto). SL a 1x OR width en la direccion del breakout. R:R = 1:1.

## Resultados del Backtest

### Metricas Principales

| Metrica | Valor | Umbral |
| --- | --- | --- |
| Win Rate | `67.09%` | >= 65% [PASS] |
| Trades/Ano | `68.8` | >= 20 [PASS] |
| Profit Factor | `2.04` | > 1.0 [PASS] |
| Total Trades | `234` | - |
| Net R | `80.00R` | - |
| R Promedio/Trade | `0.342R` | - |
| Max Drawdown | `-6.00R` | - |
| Sharpe (anualizado) | `5.763` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2022 | 8 | 4 | `50.0%` | `0.0R` |
| 2023 | 78 | 48 | `61.5%` | `18.0R` |
| 2024 | 73 | 49 | `67.1%` | `25.0R` |
| 2025 | 61 | 47 | `77.0%` | `33.0R` |
| 2026 | 14 | 9 | `64.3%` | `4.0R` |

**Mejor ano:** 2025 | **Peor ano:** 2022

## Veredicto del Equipo Quant

> **ESTRATEGIA APROBADA.** WR=67.1%, PF=2.04, 69 trades/ano. Edge consistente y explotable.

---
*Generado por KHA0SYS3 Strategy Pipeline*
