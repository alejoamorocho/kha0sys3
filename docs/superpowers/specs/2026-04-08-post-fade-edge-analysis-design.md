# Post-Fade Edge Analysis & Feature Relationship Study

**Fecha:** 2026-04-08
**Objetivo:** Extender el pipeline de análisis de edges para descubrir patrones post-false-breakout y relaciones entre features (RSI, posición OR vs PD, ATR) que generen ventajas operables por activo.

---

## 1. Post-Fade Tracker (Extensión de `TrackerEngine`)

### Problema
El tracker actual detecta false breakouts (rompe OR → SL hit antes de TP) pero no mide qué sucede después. La hipótesis es que muchos false breakouts son "shakeouts" donde el precio barre stops y luego arranca en la dirección original.

### Nuevas columnas en `stats_df`

**Para False Breakout UP** (rompe OR high, baja a OR low):
- `post_fade_up_max_continuation_down` — máxima extensión bajista después de tocar OR low (múltiplos de OR width)
- `post_fade_up_max_reversal_up` — máxima extensión alcista después de tocar OR low (shakeout/re-breakout)
- `post_fade_up_time_to_reversal` — minutos desde SL hit hasta que precio vuelve a superar OR high (null si no lo hace)
- `post_fade_up_reached_Nx_down` — flags para 1x, 1.5x, 2x extensión bajista post-fade
- `post_fade_up_reached_Nx_up` — flags para 1x, 1.5x, 2x extensión alcista post-fade (re-breakout)

**Simétrico para False Breakout DOWN** (rompe OR low, sube a OR high):
- `post_fade_down_max_continuation_up` — extensión alcista post-fade
- `post_fade_down_max_reversal_down` — extensión bajista post-fade (shakeout inverso)
- Mismos flags de extensión y timing

### Mecánica de cálculo
1. Identificar días con false breakout UP: `time_sl_up` no null AND (`time_tp_up` null OR `time_sl_up < time_tp_up`)
2. Filtrar velas posteriores a `time_sl_up`, dentro de la ventana activa 8h
3. Medir `high - or_high` (reversal UP) y `or_low - low` (continuation DOWN) desde el punto de SL hit
4. Calcular máximos y normalizar por `or_width`
5. Para timing del re-breakout: primer vela post-SL donde `high > or_high`

---

## 2. RSI y Feature Enrichment (Extensión de `DataEnricher`)

### RSI(14) M15
- Cálculo Wilder estándar: EMA de ganancias y pérdidas sobre 14 velas M15
- Captura: `rsi_at_or_close` — valor RSI en la última vela del período OR
- Sin look-ahead: RSI calculado sobre velas previas e incluyendo la vela actual

### RSI(14) Diario
- RSI sobre cierre diario, shift(1) para usar el del día anterior → `rsi_daily_14`

### Posición del OR respecto a niveles PD
- `or_position_vs_pd` — categórico:
  - `ABOVE_PD_HIGH`: or_open > pd_high
  - `BELOW_PD_LOW`: or_open < pd_low
  - `INSIDE_PD_RANGE`: pd_low ≤ or_open ≤ pd_high (subdividido por close y mid)
- `or_open_vs_pd_close` — distancia normalizada: `(or_open - pd_close) / atr_14`
- `or_open_vs_pd_mid` — distancia normalizada: `(or_open - pd_mid) / atr_14`
- `or_high_vs_pd_high` — `(or_high - pd_high) / atr_14`
- `or_low_vs_pd_low` — `(or_low - pd_low) / atr_14`

### ATR como predictor
- `atr_change` — `(atr_14_hoy - atr_14_ayer) / atr_14_ayer` (requiere shift de ATR del día anterior)
- `atr_percentile` — percentil del ATR actual vs rolling 50 días

---

## 3. Nuevos Edges en `StatisticalEngine`

### A. Post-Fade Edges

Para cada dirección de false breakout:
- **P(shakeout & re-breakout)** — % donde después de tocar SL, el precio vuelve a superar el OR boundary original y extiende ≥1x OR
- **P(continuation post-fade)** — % donde continúa en dirección contraria ≥1x, 1.5x, 2x OR
- **Extensión media/mediana post-fade** — en múltiplos de OR width, para reversal y continuation
- **Tiempo medio al re-breakout** — minutos desde SL hit hasta re-cruce de OR boundary

### B. Feature-Conditional Edges

Segmentar datos por cada feature y recalcular todos los edges core:

| Segmento | Filtro |
|---|---|
| RSI Oversold al OR | `rsi_at_or_close < 30` |
| RSI Overbought al OR | `rsi_at_or_close > 70` |
| RSI Neutro | `30 ≤ rsi_at_or_close ≤ 70` |
| OR dentro del rango PD | `or_position = INSIDE_PD_RANGE` |
| OR encima de PD High | `or_position = ABOVE_PD_HIGH` |
| OR debajo de PD Low | `or_position = BELOW_PD_LOW` |
| ATR creciente | `atr_change > 0.1` |
| ATR decreciente | `atr_change < -0.1` |
| ATR Q1 (baja vol histórica) | `atr_percentile < 25` |
| ATR Q4 (alta vol histórica) | `atr_percentile > 75` |

Para cada segmento: n_days, p_break_up/down, extensions (1x, 1.5x, 2x), false_breaks, post_fade_shakeout, touches_pd.
**Filtro de significancia:** solo segmentos con n ≥ 20 días.

### C. Timing de Targets

- Minutos promedio/mediana para alcanzar 1x, 1.5x, 2x OR en cada dirección
- Minutos promedio del primer breakout al SL hit (para false breaks)
- Distribución P80: ¿en cuánto tiempo se alcanza el 80% de los TP?
- Tiempo medio del re-breakout post-fade

---

## 4. Reportes (Extensión de `ReportGenerator` y `QuantTeam`)

### Nuevas secciones por permutación en `{SYMBOL}_Edge.md`:

#### 4.1 "Anatomia Post-False Breakout" (después de la sección actual de trampas)
- Número de false breakouts analizados por dirección
- Probabilidad de shakeout & re-breakout con extensión media
- Probabilidad de continuación post-fade con extensión media
- Tiempo medio al re-breakout

#### 4.2 "Edge por Contexto de Features" (tabla resumen)
Tabla con columnas: Contexto | N | Break UP | Ext 1.5x UP | False BK UP | Shakeout UP | Magnet PD_Close
Solo filas con n ≥ 20. Marcador en valores ≥ 60%.

#### 4.3 "Velocidad de Ejecucion" (timing)
Tabla: Target | Tiempo Medio | Mediana | P80 alcanzado en

#### 4.4 Nuevos arquetipos en QuantTeam Debate
- **`EDGE SHAKEOUT-REVERSAL`** — P(shakeout & re-breakout) ≥ 60%. Sugerencia: orden límite en lado contrario del OR post primer rompimiento.
- **`EDGE RSI-CONDITIONAL`** — filtro RSI eleva edge base por encima del 60%.
- **`EDGE CONTEXT-BOOST`** — contexto (inside PD, ATR Q1, etc.) mejora edge existente ≥ 10pp vs baseline.

El QuantTeam compara cada edge condicional vs baseline y solo reporta mejoras ≥ 10 puntos porcentuales.

---

## 5. Archivos a modificar

| Archivo | Cambio |
|---|---|
| `src/application/calculators.py` | Agregar RSI M15, RSI diario, posición OR vs PD, ATR change/percentile |
| `src/application/trackers.py` | Agregar tracking post-fade (extensiones y timing después de SL hit) |
| `src/application/statistics.py` | Agregar post-fade edges, feature-conditional edges, timing stats |
| `src/application/quant_team.py` | Agregar arquetipos SHAKEOUT-REVERSAL, RSI-CONDITIONAL, CONTEXT-BOOST |
| `src/engine/report_generator.py` | Agregar secciones de anatomía post-fade, features condicionales, timing |

No se crean archivos nuevos. Todo se extiende orgánicamente.

---

## 6. Restricciones

- Sin look-ahead bias: RSI y ATR siempre calculados sobre datos disponibles al momento
- Normalización por ATR para comparabilidad entre activos
- Mínimo 20 días por segmento para reportar
- Pipeline Polars vectorizado (sin loops por fila)
- Compatible con el backtester y portfolio compounder existentes (no romper columnas actuales)
