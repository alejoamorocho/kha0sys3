# MATH Discovery con M1 Tracking — Informe Final

**Branch:** `feature/strategies-external-plan-2`
**Periodo backtest:** 2018-01 a 2026-05 (8 años)
**Activos M1 evaluados (10):** EURUSD, USDJPY, GBPAUD, XAUUSD, XAGUSD, WTI, BRENT, NATGAS, SP500, NASDAQ100
**TFs señal:** M15, H1, H4
**Setups:** 6 momentum + 6 fade = 12
**Sesiones:** ASIA, LONDON, NY, LONDON_NY, ALL_DAY (5)

---

## Pipeline ejecutado

| Phase | Backtests | Survivors | Tiempo | Notas |
|-------|----------:|----------:|-------:|-------|
| **A** (defaults TP/SL) | 1,800 | 0 | 103 s | Friction destruye economía con defaults del documento |
| **B** (grid 7×TP/SL × 2 invert) | 24,815 | 12 | 5.5 min | Look-ahead **fixed** descartó 462 ficticios |
| **C** (grid fino 11×11 TP/SL) | 1,452 | 66 (best/strat: 8) | 8 s | Refina TP/SL óptimo per strategy |
| **D** (3 variantes salida) | 24 | 8 (1 por strategy) | 3 s | Compara TP/SL fijo vs salida en señal opuesta |

**Look-ahead bias detectado y corregido (commit 0bd21cc):**
- **Antes**: 462 supervivientes, top WR=96.9% PF=224 Calmar=6.96
- **Después**: 12 supervivientes, top WR=51.7% PF=1.68 Calmar=0.018
- Causa: el detector evalúa la señal al **cierre del bar T**, pero el campo `time` de polars apunta al **inicio del bar T**. El backtester buscaba fill desde `time + 1 M1 bar`, usando información que en vivo no estaría disponible.
- Fix: shift `start_idx` por `tf_minutes` para empezar tracking desde el cierre real del bar.

---

## Top 8 candidatos finales (Phase D — best variant per strategy)

| # | sym | tf | setup | session | INV | best_variant | TP | SL | n | WR | PF | exp_R | DD_R | Calmar |
|---|-----|----|-------|---------|-----|--------------|----|----|----|------|------|-------|------|--------|
| 1 | **EURUSD** | H1 | KAMA_CROSS_MOM | NY | T | **V3 opp+tpsl** | 1.75 | 1.05 | 67 | 0.522 | **1.43** | 0.154 | 4.9 | **0.031** |
| 2 | **USDJPY** | M15 | SPECTRAL_TREND_MOM | LONDON | F | V1 baseline | 0.75 | 0.55 | 118 | 0.508 | **1.58** | 0.335 | 11.0 | **0.030** |
| 3 | **NASDAQ100** | M15 | KAMA_CROSS_MOM | ASIA | F | V3 opp+tpsl | 1.50 | 0.80 | 36 | 0.528 | 1.18 | 0.104 | 4.2 | 0.025 |
| 4 | USDJPY | M15 | KAMA_CROSS_MOM | ASIA | F | V1 baseline | 1.50 | 0.80 | 134 | 0.500 | 1.24 | 0.141 | 11.6 | 0.012 |
| 5 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | F | V2 opp_only | 0.50 | 0.55 | 214 | 0.444 | 1.32 | 0.413 | 42.7 | 0.010 |
| 6 | EURUSD | M15 | KAMA_CROSS_MOM | NY | F | V3 opp+tpsl | 1.25 | 0.80 | 183 | 0.519 | 1.12 | 0.068 | 16.6 | 0.004 |
| 7 | XAUUSD | M15 | SPECTRAL_TREND_MOM | NY | F | V1 baseline | 0.75 | 0.55 | 203 | 0.522 | 1.04 | 0.021 | 21.1 | 0.001 |
| 8 | XAUUSD | M15 | VELOCITY_ACCEL_GO | NY | F | V1 baseline | 0.75 | 0.55 | 1551 | 0.502 | 1.00 | 0.000 | 69.1 | 0.000 |

---

## Hallazgos importantes

### 1. La **fase B con look-ahead** fue 100% espuria
462 falsos edges con WR 91-99%. El test diagnóstico sobre el top combo (XAGUSD H4 KAMA_CROSS_MOM) reveló que el "edge" provenía de poder entrar antes del cierre del bar de detección. Tras el fix, ese mismo combo da **22 trades, WR=13.6%, PF=0.10, 19 TIME_STOP, 1 TP, 2 SL**.

### 2. **H4 desaparece completamente** post-fix
Ningún superviviente real opera en H4 — los 138 H4 "candidatos" eran 100% bias. Esto tiene sentido: un bar H4 dura 4h, y entrar a sus M1 sub-bars con conocimiento del cierre proporciona enorme ventaja artificial. M15 y H1 tienen menos "espacio" para que el bias domine.

### 3. **Salida en señal opuesta NO mejora consistentemente**
- 4 estrategias prefieren V1 baseline (TP/SL fijos)
- 3 estrategias prefieren V3 (opposite + TP/SL protección)
- 1 estrategia prefiere V2 (solo opposite)

V2 puro (sin TP/SL como cap) **empeora la mayoría** (PF cae, exp_R puede ir negativo). V3 (opposite combinado con TP/SL) es comparable o ligeramente mejor que V1 — la protección TP/SL es necesaria.

### 4. Sólo **3 setups producen edges reales**: KAMA_CROSS_MOM, SPECTRAL_TREND_MOM, VELOCITY_ACCEL_GO
Los otros 9 (HURST_TREND_MOM, OLS_SLOPE_STRONG, todos los FADE, etc.) NO produjeron ningún superviviente válido en el grid completo. Diagnóstico: friction 0.3-0.4R + asimetría TP/SL del documento + M1 expone hits SL más estrictamente.

### 5. **0 supervivientes FADE** post-fix
Ninguno de los 6 setups FADE (KALMAN_PEAK_FADE, GARCH_Z_FADE, etc.) produce edge real bajo M1 tracking + look-ahead-clean. Coherente con Plan 3 Block A que mostró que FADE bot live también drift contra M1.

---

## ⚠️ Caveats que persisten

1. **Calmar muy bajos** (0.000-0.031). Equivalente a expectancy * trades_per_year / max_DD anual. Aún post-fix, los edges son **marginales** vs el riesgo.
2. **WR 50-58%, PF 1.0-1.6**. Apenas sobre breakeven. Una ligera regresión a la media o cambio de régimen puede invertir esos números.
3. **Sin walk-forward IS/OOS**. Estos 8 son lo mejor de un grid 11×11 + 2 invert + 3 variants — hay riesgo de **overfitting al periodo 2018-2026**. Walk-forward podría reducir aún más.
4. **Sin Monte Carlo bootstrap**. No medimos prob_ruin todavía.
5. **Trade count bajo** en algunos (NASDAQ100 ASIA = 36 trades en 8 años ≈ 4.5/año). Estadísticamente débil.
6. **direction_mode INVERT en bot live** ya estaba documentado, pero el grid encontró 7 sin invert + 1 con invert dando edges marginales — ambos pueden ser ruido en regímenes específicos.

---

## Comparación con bot live MATH (`bot_config_math.json`)

El bot live reporta para sus 34 estrategias:
- WR esperado típico: 0.65-0.85
- PF esperado típico: 1.5-3.0
- Mc ruin: 0.0-2%

Nuestros top 3 (post-fix):
- WR: 0.50-0.53 (≈ −15 a −30 pp menos)
- PF: 1.18-1.58 (≈ −0.5 a −1.0 menos)

**El gap se debe (probablemente) a una combinación de**:
- Comisiones reales del broker no modeladas (usamos friction genérica 0.3-0.4R)
- Validación in-sample del bot live (las métricas live = históricas optimizadas)
- Diferencias de session boundaries / timestop entre nuestro adapter y live
- Posible overfitting del propio bot live

---

## Archivos generados

```
reports/external/
├── math_discovery_m1_phase_a.md             (0 survivors)
├── math_discovery_m1_phase_a.parquet
├── math_discovery_m1_phase_b.md             (12 real survivors)
├── math_discovery_m1_phase_b.parquet
├── math_discovery_m1_phase_c.md             (8 best per strategy)
├── math_discovery_m1_phase_c.parquet
├── math_discovery_m1_phase_c_best.parquet
├── math_discovery_m1_phase_d.md             (8 best variants)
├── math_discovery_m1_phase_d.parquet
├── math_discovery_m1_phase_d_best.parquet
└── math_discovery_m1_FINAL_REPORT.md        (este archivo)
```

---

## Recomendaciones para siguientes pasos

### Validación crítica antes de cualquier deployment
1. **Walk-forward IS/OOS** sobre los 8 candidatos: dividir 2018-2026 en 5 ventanas, entrenar TP/SL en IS, evaluar en OOS. Si calmar OOS sigue >0, el edge es robusto.
2. **Monte Carlo bootstrap** 10k simulaciones por candidato: medir prob_ruin con DD threshold = -10R.
3. **Re-correr con friction modelada exacta** del broker Vantage (en lugar de 0.3-0.4 genérico).

### Mejoras al adapter
1. Implementar **direction guard real** (cancelar si indicador de setup se debilita en wait window).
2. Implementar **session-end timestop preciso** (matchear el bot live exacto).
3. Probar **TFs intermedios** (M30, H2) si los datos lo permiten.

### Priorización de candidatos
- **Top tier (vale walk-forward)**: candidatos #1, #2, #3 (Calmar > 0.02, PF > 1.2, n > 30, DD < 12R).
- **Mid tier**: #4, #5 (PF > 1.2 pero Calmar bajo o DD alto).
- **Borderline / descartar**: #6, #7, #8 (PF ≈ 1.0, expectancy ≈ 0).

---

## Conclusión

Plan 4 entrega un **pipeline reproducible** de discovery de MATH edges con M1 tracking, y un **set de 8 candidatos marginales pero honestos** (post-fix de look-ahead bias). Ningún edge bombástico — los WR/PF están en la frontera de breakeven. **No deployar sin walk-forward + MC + ajuste de friction al broker real.**

Lo más valioso del ejercicio fue **detectar y corregir el look-ahead bias** que infló 97% de los "edges" iniciales. Ese fix también beneficia cualquier discovery futuro sobre la misma infraestructura.
