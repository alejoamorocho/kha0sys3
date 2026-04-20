# Indicator-Based Edge Discovery — Design Spec

**Date:** 2026-04-20
**Status:** Approved, pending implementation plan
**Scope:** Research only (no live trading changes)

## Goal

Descubrir estrategias con edge estadístico basadas en indicadores técnicos clásicos
(RSI, MACD, Bollinger Bands, Fractal, ADX), independientes del Opening Range. Mínimo
100 trades/año, WR ≥ 80%, validadas con walk-forward, Monte Carlo y análisis de decay.

Entregable: reporte + JSON export con estrategias candidatas. **No se modifica el bot
live en esta fase.**

## Decisiones de diseño (brainstorming)

| # | Pregunta | Decisión |
|---|----------|----------|
| 1 | Uso de indicadores | Arquetipos nuevos independientes de ORB |
| 2 | Timeframe | Scanner sobre M15 + H1 (scanner elige por estrategia) |
| 3 | Universo | 15 activos originales (incluye XAGUSD/SP500) |
| 4 | Familias de señales | Reversión + Momentum + confluencia 0-2 filtros |
| 5 | Salida TP/SL | Grid ATR por estrategia (igual metodología que FADE R:R) |
| 6 | ATR period + tiempo | ATR(14) + time-stop a cierre de sesión nativa |
| 7 | Filtro de sesión | Grid {Asia, London, NY, London+NY, 24h} |
| 8 | Gates validación | trades/año≥100, WR≥80%, Exp>0.1R, PF≥1.3, MaxDD≤20R, WF OOS≥0.85×IS, MC ruina<1%, decay slope≥0.7×global |
| 9 | Ventana datos | Todo el histórico + walk-forward rolling (6m IS / 2m OOS) |
| 10 | Control combinatorio | Pipeline 2 fases (discovery rápido → optimización sobre survivors) |

## Arquitectura

```
CSV (M15+H1) → DataEnricher extendido (RSI, MACD, BB, Fractal, ADX)
   ↓
SignalGenerator: 10 señales primarias × 4 filtros de confluencia
   ↓
Phase-1 Scanner: R:R fijo (2×ATR / 1×ATR), sin confluencia
   → filtra por gates laxos
   ↓
Phase-2 Optimizer: 11 combos confluencia × 20 combos R:R ATR
   → aplica gates estrictos (WR≥80% + WF + MC + decay)
   ↓
ReportGenerator: Markdown + JSON export
```

**Principios:**
- Zero cambios en `domain/` excepto añadir constantes de indicadores.
- Reusa `TrackerEngine` y `StatisticalEngine` sin modificación.
- Nuevo archetype `INDICATOR` coexiste con FADE/MOMENTUM/SHAKEOUT.
- Salida no-ORB usa time-stop a cierre de sesión nativa del activo.
- Todo Polars vectorizado, sin loops fila-a-fila.

## Componentes

### 1. `src/application/indicators.py` (nuevo)

Cálculo vectorizado con Polars. Parámetros fijos (no se optimizan en esta fase).

| Indicador | Columnas output | Parámetros |
|-----------|-----------------|------------|
| RSI | `rsi_14` | period=14 |
| MACD | `macd`, `macd_signal`, `macd_hist` | 12/26/9 |
| Bollinger Bands | `bb_upper`, `bb_middle`, `bb_lower`, `bb_pct` | period=20, std=2.0 |
| Fractal | `fractal_high`, `fractal_low` (bool) | window=5 |
| ADX | `adx_14`, `plus_di`, `minus_di` | period=14 |

ATR(14) ya existe en `calculators.py`, se reusa.

Cache intermedio en `data/enriched/{symbol}_{tf}.parquet` para que Phase-1 y Phase-2 no recalculen.

### 2. `src/application/signal_generator.py` (nuevo)

Emite DataFrame: `timestamp, symbol, direction, signal_type, indicator_state`.

**10 señales primarias:**

Reversión:
1. `RSI_OB_REV` — RSI cruza 70↓ → SHORT; 30↑ → LONG
2. `BB_TOUCH_REV` — toque `bb_upper` → SHORT; `bb_lower` → LONG
3. `FRACTAL_REV` — `fractal_high` → SHORT; `fractal_low` → LONG
4. `MACD_DIVERGENCE` — precio HH + MACD LH → SHORT; LL + HL → LONG
5. `BB_RSI_CONFLUENCE` — toque BB + RSI extremo (señal conjunta)

Momentum:
6. `MACD_CROSS` — MACD cruza signal al alza/baja
7. `ADX_BREAKOUT` — ADX cruza 25 + DI dominante
8. `BB_BREAKOUT` — cierre fuera de banda
9. `RSI_50_CROSS` — RSI cruza 50
10. `FRACTAL_TREND` — fractal en dirección de ADX>20

**4 filtros de confluencia:** `RSI_ZONE`, `ADX_REGIME`, `BB_POSITION`, `MACD_ALIGN`.

Phase-2 prueba 0-2 filtros = C(4,0)+C(4,1)+C(4,2) = **11 combos**.

### 3. Arquetipo INDICATOR en `strategy_backtester.py` (edit)

- **Entrada:** LIMIT al cierre de barra de señal (MARKET como alternativa a decidir en plan).
- **TP:** entry ± tp_mult × ATR(14) medido en barra de entrada.
- **SL:** entry ∓ sl_mult × ATR(14).
- **Time-stop:** cierre de sesión nativa del activo.
- **Dedup:** 1 trade por (symbol, signal_type, session) por día.

### 4. `src/engine/run_indicator_discovery.py` (nuevo)

**Fase 1 — Discovery rápido**
- Espacio: 15 activos × 2 TFs × 5 sesiones × 10 señales = **1.500 combos**
- Setup: TP=2×ATR, SL=1×ATR, sin confluencia
- Gates laxos: trades/año≥100, WR≥60%, PF≥1.2, Exp>0
- Output: `reports/indicator_discovery_phase1.md` + `survivors.parquet`
- Runtime estimado: 10-20 min

**Fase 2 — Optimización**
- Por survivor: 11 confluencias × 20 R:R ATR = **220 trials**
- R:R grid: TP∈{1, 1.5, 2, 2.5, 3}×ATR × SL∈{0.75, 1, 1.5, 2}×ATR
- Gates estrictos (completos, ver tabla decisiones #8)
- Runtime estimado: 1-4h (depende de # survivors)

### 5. Reporting

**`reports/Indicator_Discovery_Final.md`:**
1. Resumen ejecutivo (# combos, survivors, aprobados)
2. Tabla top-N por activo + señal con todas las métricas
3. Heatmap (activo × familia señal): edge R/trade
4. Equity curves OOS de top-10

**`reports/indicator_strategies.json`:** compatible con formato `bot_config.json`.
Campos: symbol, tf, session, archetype=INDICATOR, signal_type, filters,
tp_mult, sl_mult, atr_period=14.

## Scope explícito (YAGNI)

**En scope:**
- Cálculo de indicadores, generador de señales, backtester INDICATOR, pipeline 2 fases, reporte, JSON export, tests unitarios.

**Fuera de scope (fases futuras):**
- Modificar `live_trader.py` / `order_manager.py`.
- Activar arquetipo INDICATOR en el bot live.
- Optimización de parámetros de indicadores (RSI period, MACD settings, etc.).
- Optuna / búsqueda bayesiana sobre el grid completo.
- ATR adaptativo por ADX.

## Estructura de archivos

```
src/application/indicators.py               [nuevo]
src/application/signal_generator.py         [nuevo]
src/engine/run_indicator_discovery.py       [nuevo]
src/engine/strategy_backtester.py           [edit: +INDICATOR archetype]
src/domain/constants.py                     [edit: +params indicadores]
tests/test_indicators.py                    [nuevo]
tests/test_signal_generator.py              [nuevo]
reports/Indicator_Discovery_Final.md        [output]
reports/indicator_strategies.json           [output]
data/enriched/*.parquet                     [cache intermedio]
```

## Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|-----------|
| Overfitting con WR≥80% | Walk-forward rolling + MC + decay (gates estrictos) |
| Explosión combinatoria | Pipeline 2 fases con gates laxos en Phase-1 |
| Sesgo look-ahead en fractal | Fractal(5) solo se marca después de 2 barras de confirmación |
| Survivorship bias XAGUSD/SP500 | Incluidos en universo, scanner decide |
| Cambio de régimen invalida edge | Decay slope gate filtra estrategias degradando |

## Criterios de éxito

- Al menos **5-10 estrategias** pasan todos los gates (incluye WR≥80%).
- Estrategias cubren ≥5 activos distintos (no concentradas en uno solo).
- Edge OOS no se degrada >15% vs IS.
- Reporte reproducible (seed fijo en MC, ventanas WF deterministas).

## Next steps

Tras aprobación del spec → invocar `writing-plans` para plan de implementación detallado paso a paso.
