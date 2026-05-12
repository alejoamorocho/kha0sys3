# Concurrent Open Positions Analysis

Computed from REAL backtest trade timestamps (2018-01-01 → 2026-03-24, 8.22 years).

Risk model: WR-tier scaling (WR=55% → 1%, WR=80% → 15% per trade, linear).
Balance assumed: $10,000.

## Portfolio FUERTE completo (153 strats) — 153 strategies, 117,783 trades over 8.22y

| Percentile | Positions abiertas | Total Risk % | USD @ Risk |
|---|---|---|---|
| p50 | 8 | 34.8% | $3,478 |
| p75 | 12 | 56.5% | $5,651 |
| p90 | 17 | 80.1% | $8,006 |
| p95 | 20 | 95.2% | $9,516 |
| p99 | 26 | 123.1% | $12,307 |
| p99.9 | 33 | 153.0% | $15,296 |
| **MAX (peor caso 8.2y)** | **40** | **183.2%** | **$18,317** |

Per-TF max concurrent:

| TF | Max concurrent | Max risk % |
|---|---|---|
| M15 | 10 | 32.5% |
| H1 | 26 | 104.4% |
| H4 | 25 | 146.2% |

## Portfolio ELITE LIVE (34 strats WR>=65%) — 34 strategies, 22,120 trades over 8.22y

| Percentile | Positions abiertas | Total Risk % | USD @ Risk |
|---|---|---|---|
| p50 | 2 | 18.6% | $1,857 |
| p75 | 4 | 33.6% | $3,364 |
| p90 | 6 | 48.5% | $4,853 |
| p95 | 7 | 58.7% | $5,866 |
| p99 | 9 | 78.0% | $7,804 |
| p99.9 | 12 | 103.1% | $10,307 |
| **MAX (peor caso 8.2y)** | **15** | **129.4%** | **$12,943** |

Per-TF max concurrent:

| TF | Max concurrent | Max risk % |
|---|---|---|
| M15 | 1 | 10.0% |
| H1 | 7 | 60.1% |
| H4 | 13 | 110.4% |

## Conclusión y recomendación de riesgo

El **MAX histórico** representa el peor caso de overlap durante 8.2 años. 
Si todas las posiciones perdieran 1R simultáneamente (escenario casi-imposible porque las strats operan en symbols/setups/sessions distintas), ese es tu DD pico.

El **p95** es la cota superior realista del 95% del tiempo. Usar el p95 como referencia de riesgo simultáneo es defensivo pero realista.

**Para fijar `max_risk_pct` por trade**:
1. Identifica tu DD aceptable (ej. 30% del balance).
2. Divide entre el max histórico de strats simultáneas.
3. Resultado = riesgo seguro por trade.
