# Reporte de Estrategia: USDJPY Tokyo 30m MOMENTUM_DOWN

**Status:** `[NO APROBADA]`

## Definicion de la Estrategia

| Parametro | Valor |
| --- | --- |
| Activo | USDJPY |
| Sesion | Tokyo (00:00 UTC) |
| Duracion OR | 30 minutos |
| Arquetipo | MOMENTUM_DOWN |
| Direccion | DOWN |
| TP Multiplier | 1.5x OR |

### Logica de Ejecucion

Entrada en la rotura bajista del Opening Range. TP fijo a 1.5x OR width. SL en el extremo opuesto del OR (1R riesgo).

## Resultados del Backtest

### Metricas Principales

| Metrica | Valor | Umbral |
| --- | --- | --- |
| Win Rate | `45.35%` | >= 65% [FAIL] |
| Trades/Ano | `105.1` | >= 20 [PASS] |
| Profit Factor | `1.24` | > 1.0 [PASS] |
| Total Trades | `860` | - |
| Net R | `115.00R` | - |
| R Promedio/Trade | `0.134R` | - |
| Max Drawdown | `-18.50R` | - |
| Sharpe (anualizado) | `1.705` | - |

### Desglose Anual

| Ano | Trades | Wins | WR | Net R |
| --- | --- | --- | --- | --- |
| 2018 | 101 | 44 | `43.6%` | `9.0R` |
| 2019 | 102 | 40 | `39.2%` | `-2.0R` |
| 2020 | 104 | 60 | `57.7%` | `46.0R` |
| 2021 | 101 | 47 | `46.5%` | `16.5R` |
| 2022 | 89 | 39 | `43.8%` | `8.5R` |
| 2023 | 121 | 55 | `45.5%` | `16.5R` |
| 2024 | 102 | 42 | `41.2%` | `3.0R` |
| 2025 | 111 | 51 | `45.9%` | `16.5R` |
| 2026 | 29 | 12 | `41.4%` | `1.0R` |

**Mejor ano:** 2020 | **Peor ano:** 2019

## Veredicto del Equipo Quant

> **ESTRATEGIA NO APROBADA.** Falla en: WR=45.3% < 65%. Se documenta para referencia pero no se recomienda para operacion.

---
*Generado por KHA0SYS3 Strategy Pipeline*
