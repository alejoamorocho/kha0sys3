# MATH Discovery con M1 Tracking — Informe Final v2

**Branch:** `feature/strategies-external-plan-2`
**Periodo backtest:** 2018-01 a 2026-05 (8.33 años)
**Activos M1 evaluados (10):** EURUSD, USDJPY, GBPAUD, XAUUSD, XAGUSD, WTI, BRENT, NATGAS, SP500, NASDAQ100
**TFs señal:** M15, H1, H4 (M1 entries → Phase F en ejecución)
**Setups:** 6 momentum + 6 fade = 12
**Sesiones:** ASIA, LONDON, NY, LONDON_NY, ALL_DAY (5)

---

## Pipeline ejecutado

| Phase | Backtests | Survivors | Tiempo | Notas |
|-------|----------:|----------:|-------:|-------|
| **A** (defaults TP/SL) | 1,800 | 0 | 103 s | Friction destruye economía con defaults del documento |
| **B** (grid 7×TP/SL × 2 invert) | 24,815 | 12 | 5.5 min | **Look-ahead fixed** descartó 462 ficticios (97%) |
| **C** (grid fino 11×11 TP/SL) | 1,452 | 8 únicos | 8 s | Refina TP/SL óptimo per strategy |
| **D** (3 variantes salida) | 24 | 8 best | 3 s | V1 baseline / V2 opposite / V3 opposite+tpsl |
| **E** (6 exits alternos) | 48 | 8 best (combined D+E) | 6 s | Trailing 1.0/1.5 ATR, SMA20/50 cross, time-fixed 60/240 |
| **F** (entries en M1) | en curso | — | ~45 min | 4 syms con M1 enrichment cacheado |

**Look-ahead bias detectado y corregido (commit 0bd21cc):**
- **Antes**: 462 supervivientes, top WR=96.9% PF=224 Calmar=6.96
- **Después**: 12 supervivientes, top WR=51.7% PF=1.68 Calmar=0.018
- Causa: detector evalúa al cierre del bar T pero `time` apunta al inicio del bar; el backtester buscaba fill desde `time + 1 M1 bar` con info no disponible en vivo.
- Fix: shift `start_idx` por `tf_minutes` para empezar tracking desde el cierre real del bar.

---

## TABLA COMPLETA — 12 supervivientes Phase B (con trades/año)

| # | sym | tf | setup | session | INV | TP | SL | n | trades/yr | WR | PF | exp_R | DD_R | Calmar |
|---|-----|----|-------|---------|-----|------|------|-----|----------:|------|------|-------|------|--------|
| 1 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | F | 0.70 | 0.50 | 118 | 14.2 | 0.517 | 1.68 | 0.395 | 22.4 | 0.0176 |
| 2 | USDJPY | M15 | KAMA_CROSS_MOM | ASIA | F | 1.50 | 1.00 | 134 | 16.1 | 0.552 | 1.18 | 0.093 | 6.2 | 0.0150 |
| 3 | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | F | 0.70 | 0.50 | 36 | 4.3 | 0.583 | 1.19 | 0.102 | 7.4 | 0.0138 |
| 4 | EURUSD | H1 | KAMA_CROSS_MOM | NY | T | 1.50 | 1.00 | 67 | 8.0 | 0.507 | 1.17 | 0.068 | 7.0 | 0.0097 |
| 5 | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | F | 2.00 | 1.00 | 36 | 4.3 | 0.500 | 1.09 | 0.051 | 6.2 | 0.0083 |
| 6 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | F | 1.00 | 1.00 | 118 | 14.2 | 0.551 | 1.17 | 0.082 | 12.9 | 0.0064 |
| 7 | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | F | 1.50 | 1.00 | 36 | 4.3 | 0.556 | 1.09 | 0.042 | 7.5 | 0.0056 |
| 8 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | F | 1.00 | 1.00 | 214 | 25.7 | 0.519 | 1.16 | 0.089 | 39.6 | 0.0022 |
| 9 | EURUSD | M15 | KAMA_CROSS_MOM | NY | F | 0.70 | 0.50 | 183 | 22.0 | 0.546 | 1.08 | 0.045 | 26.9 | 0.0017 |
| 10 | XAUUSD | M15 | SPECTRAL_TREND_MOM | NY | F | 0.70 | 0.50 | 203 | 24.4 | 0.522 | 1.05 | 0.031 | 21.1 | 0.0015 |
| 11 | XAUUSD | M15 | VELOCITY_ACCEL_GO | NY | F | 0.70 | 0.50 | 1551 | **186.2** | 0.504 | 1.06 | 0.035 | 50.9 | 0.0007 |
| 12 | USDJPY | M15 | KAMA_CROSS_MOM | ASIA | F | 0.70 | 0.50 | 134 | 16.1 | 0.537 | 1.01 | 0.004 | 9.3 | 0.0004 |

**Filas 1-3 + 6 son duplicados (mismo sym/tf/setup/session/invert pero distinto TP/SL)** → al hacer "best per strategy" en Phase C quedan 8 únicos.

---

## Top 8 — best variant per strategy (Phase C TP/SL optimal × Phase D+E exit)

Los 9 exits probados: V1 baseline (TP/SL fijo) · V2 opposite_only · V3 opposite+tpsl · V4 trailing_1.0_atr · V4 trailing_1.5_atr · V5 sma20_cross · V5 sma50_cross · V6 time_fixed_60 · V6 time_fixed_240

| # | sym | tf | setup | session | INV | TP | SL | best_variant | n | tr/yr | WR | PF | exp_R | DD | Calmar |
|---|-----|----|-------|---------|-----|------|------|-------------|----|------:|------|------|-------|----|--------|
| **1** | **USDJPY** | M15 | SPECTRAL_TREND_MOM | LONDON | F | 0.75 | 0.55 | **V6_time_fixed_60** | 118 | 14.2 | 0.508 | **1.58** | 0.335 | **7.9** | **0.0425** |
| **2** | **EURUSD** | H1 | KAMA_CROSS_MOM | NY | T | 1.75 | 1.05 | **V3_opposite_with_tpsl** | 67 | 8.0 | 0.522 | **1.43** | 0.154 | **4.9** | **0.0314** |
| **3** | **NASDAQ100** | M15 | KAMA_CROSS_MOM | ASIA | F | 1.50 | 0.80 | **V4_trailing_1.5_atr** | 36 | 4.3 | 0.528 | 1.23 | 0.127 | 4.5 | 0.0284 |
| 4 | USDJPY | M15 | KAMA_CROSS_MOM | ASIA | F | 1.50 | 0.80 | V6_time_fixed_60 | 134 | 16.1 | 0.507 | 1.24 | 0.134 | 7.5 | 0.0177 |
| 5 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | F | 0.50 | 0.55 | V2_opposite_only | 214 | 25.7 | 0.444 | 1.32 | 0.413 | 42.7 | 0.0097 |
| 6 | EURUSD | M15 | KAMA_CROSS_MOM | NY | F | 1.25 | 0.80 | V6_time_fixed_240 | 183 | 22.0 | 0.519 | 1.11 | 0.068 | 9.3 | 0.0073 |
| 7 | XAUUSD | M15 | SPECTRAL_TREND_MOM | NY | F | 0.75 | 0.55 | V5_sma20_cross | 203 | 24.4 | 0.473 | 1.05 | 0.025 | 18.3 | 0.0014 |
| 8 | XAUUSD | M15 | VELOCITY_ACCEL_GO | NY | F | 0.75 | 0.55 | V6_time_fixed_240 | 1551 | 186.2 | 0.502 | 1.00 | 0.000 | 62.5 | 0.0000 |

### Mejoras aportadas por exits alternativos (Phase E vs Phase B baseline)

| sym + setup + session | Calmar baseline | Calmar best alt | Mejor exit | Mejora |
|----------------------|----------------:|----------------:|------------|-------:|
| USDJPY M15 SPECTRAL LONDON | 0.018 | **0.042** | V6_time_fixed_60 | **+138%** |
| NASDAQ100 M15 KAMA ASIA | 0.014 | **0.028** | V4_trailing_1.5_atr | **+103%** |
| EURUSD H1 KAMA NY (INV) | 0.010 | **0.031** | V3_opposite_with_tpsl | **+218%** |
| USDJPY M15 KAMA ASIA | 0.015 | 0.018 | V6_time_fixed_60 | +20% |
| EURUSD M15 KAMA NY | 0.002 | 0.007 | V6_time_fixed_240 | +250% |

**V6_time_fixed_60** (cerrar a 60 M1 bars = 1h fija) y **V4_trailing_1.5_atr** (trailing stop 1.5×ATR) son los que más aportan. **V2_opposite_only** (puro signal opposite sin TP/SL) puede ayudar pero a costa de DD muy alto.

### Distribución de exits ganadores

```
V6_time_fixed_60   : 2 strategies  (preferido en M15 USDJPY)
V6_time_fixed_240  : 2 strategies  (preferido en M15 con DD largo)
V4_trailing_1.5_atr: 1 strategy
V3_opposite+tpsl   : 1 strategy
V2_opposite_only   : 1 strategy  (caveat: DD enorme)
V5_sma20_cross     : 1 strategy
```

---

## Trades/año — interpretación

- **Baja frecuencia (4-8 tr/yr)**: NASDAQ100 ASIA × KAMA, EURUSD H1 × KAMA NY. Pocas señales pero relativamente limpias. Ideal para position sizing alto.
- **Media (14-26 tr/yr)**: USDJPY × ASIA/LONDON/LONDON_NY, EURUSD M15 NY, XAUUSD NY × SPECTRAL. Frecuencia razonable.
- **Muy alta (186 tr/yr)**: XAUUSD VELOCITY_ACCEL_GO NY. Casi diario. Pero PF=1.00 = nada.

---

## Hallazgos importantes

### 1. Look-ahead bias destruido 97% de los "edges" iniciales
El test diagnóstico sobre el top combo Phase B (XAGUSD H4 KAMA_CROSS_MOM): WR cayó de 96.9% a 13.6% post-fix.

### 2. H4 desaparece completamente post-fix
Los 138 H4 "candidatos" pre-fix eran 100% bias.

### 3. Sólo 3 setups producen edges reales
- **KAMA_CROSS_MOM** (5 supervivientes únicos)
- **SPECTRAL_TREND_MOM** (3 supervivientes únicos)
- **VELOCITY_ACCEL_GO** (1, marginal)

Los otros 9 (HURST_TREND_MOM, OLS_SLOPE_STRONG, todos FADE, etc.) → 0.

### 4. 0 supervivientes FADE
Ninguno de los 6 setups FADE (KALMAN_PEAK_FADE, GARCH_Z_FADE, etc.) produce edge real bajo M1 tracking + look-ahead-clean.

### 5. Time-fixed exit (60-240 M1 bars) es el mejor exit alternativo
Sale en tiempo específico independiente del PnL. Mejora Calmar significativamente porque evita los trades que "se quedan" sin resolver hasta session-end.

### 6. Comparación con bot live MATH
- Bot live `bot_config_math.json`: WR esperado 0.65-0.85, PF 1.5-3.0
- Nuestros top 3 post-E: WR 0.51-0.53, PF 1.43-1.58
- **Gap probable**: comisiones reales del broker no modeladas (usamos friction genérica 0.3-0.4R), validación in-sample del bot live (curve-fit posible), diferencias session boundaries / timestop precisas.

---

## ⚠️ Caveats que persisten

1. **Calmar 0.000-0.042** — edges marginales sobre el riesgo. Top candidato 0.042 = expectancy_R × trades_year / max_DD ≈ 0.335 × 14 / 7.9.
2. **WR 50-58%, PF 1.0-1.6** — apenas sobre breakeven. Cambios de régimen pueden invertir.
3. **Sin walk-forward IS/OOS**. Hay riesgo de overfitting al periodo 2018-2026.
4. **Sin Monte Carlo bootstrap**. No medimos prob_ruin todavía.
5. **Trade count bajo** en NASDAQ100 ASIA (4.3/año). Estadísticamente débil.
6. **3 candidatos top usan invert=False**, 1 usa invert=True. Inconsistencia con bot live que usa direction_mode=INVERT por default.

---

## Phase F (entries en M1) — pendiente

En curso sobre 4 syms con histórico de supervivientes (USDJPY, NASDAQ100, EURUSD, XAUUSD). Cada M1 enrichment toma ~14 min. ETA total ~45 min. Resultado se actualizará a este informe.

---

## Recomendaciones

### Validación crítica antes de cualquier deployment
1. **Walk-forward IS/OOS** sobre los 8 candidatos: 5 ventanas, entrenar TP/SL en IS, evaluar en OOS.
2. **Monte Carlo bootstrap** 10k simulaciones por candidato: medir prob_ruin.
3. **Re-correr con friction modelada exacta** del broker Vantage en lugar de 0.3-0.4 genérica.

### Priorización de candidatos
- **Top tier (vale walk-forward)**: 1, 2, 3 (Calmar > 0.025, PF > 1.20, DD < 8R).
- **Mid tier**: 4 (Calmar 0.018, OK pero margen estrecho).
- **Borderline**: 5, 6 (DD alto o PF marginal).
- **Descartar**: 7, 8 (PF ≈ 1.0, expectancy ≈ 0).

### Mejoras al adapter
1. Implementar **direction guard real** del bot live (cancelar si indicador se debilita en wait window).
2. Probar **session-end timestop preciso** (matchear bot live exacto).
3. Probar **TFs intermedios** (M30, H2) si los datos lo permiten.

---

## Conclusión

Pipeline reproducible de discovery con **8 candidatos marginales pero honestos**. El hallazgo más valioso fue **detectar y corregir look-ahead bias** que hubiera convertido falsos edges en producción.

**Top candidato post-E**: **USDJPY M15 SPECTRAL_TREND_MOM LONDON TP=0.75/SL=0.55 V6_time_fixed_60** (PF 1.58, exp 0.335R, 14 tr/año, DD 7.9R, Calmar 0.042).

No deployar sin walk-forward + MC + friction broker exacta.
