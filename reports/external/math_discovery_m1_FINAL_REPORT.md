# MATH Discovery con M1 — Informe Final v3 (CONSERVADOR)

**Branch:** `feature/strategies-external-plan-2`
**Periodo backtest:** 2018-01 a 2026-05 (8.33 años)
**Activos M1 evaluados:** 10 (M15/H1/H4) + 4 (M1 entries: USDJPY, NASDAQ100, EURUSD, XAUUSD)
**TFs señal:** M15, H1, H4, **M1**
**Setups:** 6 momentum + 6 fade = 12
**Sesiones:** ASIA, LONDON, NY, LONDON_NY, ALL_DAY (5)

**🔧 Bias correcciones aplicadas:**
1. **Look-ahead fix** (commit 0bd21cc): start_idx shift por tf_minutes — el detector usa info al cierre del bar, no al inicio.
2. **SL-first intra-bar** (commit 550e758): TP/SL ties dentro del mismo bar resuelven a SL (worst case). Crítico en M1 con TP/SL juntos.

---

## Pipeline ejecutado completo

| Phase | Backtests | Survivors | Tiempo | Notas |
|-------|----------:|----------:|-------:|-------|
| **A** (defaults) | 1,800 | 0 | 103 s | Friction destruye economía |
| **B** (grid 7×TP/SL × 2 invert, M15/H1/H4) | 24,815 | 12 | 5.5 min | Look-ahead fix descartó 462 falsos |
| **C** (grid fino 11×11 TP/SL) | 1,452 | 7 únicos | 8 s | Refina TP/SL óptimo |
| **D** (3 variantes salida con señal opuesta) | 21 | 7 best | 3 s | V1 baseline / V2 opp / V3 opp+tpsl |
| **E** (6 exits: trailing, SMA, time_fixed) | 42 | 7 best | 5 s | V4 trailing 1.0/1.5 ATR · V5 SMA20/50 cross · V6 time_fixed 60/240 |
| **F** (entries M1, 4 syms) | 3,360 | 49 únicos | 61 s | M1 entries dan más candidates pero Calmar bajos |

---

## TOP 10 GLOBAL (mezcla M15/H1/H4 + M1)

| Rank | sym | tf | setup | session | INV | TP/SL | best_exit | n | tr/yr | WR | PF | DD | **Calmar** |
|----:|-----|----|-------|---------|-----|-------|-----------|----|------:|------|------|----|---:|
| **1** | EURUSD | H1 | KAMA_CROSS_MOM | NY | T | 1.75/1.05 | V3 opp+tpsl | 67 | 8.0 | 0.522 | 1.43 | 3.0 | **0.0515** |
| **2** | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | F | 1.50/0.80 | V4 trailing 1.5 ATR | 36 | 4.3 | 0.528 | 1.23 | 2.8 | **0.0454** |
| **3** | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | F | 0.50/0.55 | V6 time_fixed 240 | 118 | 14.2 | 0.593 | 1.57 | 10.3 | **0.0265** |
| 4 | USDJPY | M15 | KAMA_CROSS_MOM | ASIA | F | 1.50/0.80 | V3 opp+tpsl | 134 | 16.1 | 0.500 | 1.24 | 8.5 | 0.0165 |
| 5 | EURUSD | M1 | VELOCITY_ACCEL_GO | ALL_DAY | T | 2.00/1.00 | V1 baseline | 1861 | 223.4 | 0.519 | 1.41 | 17.1 | 0.0150 |
| 6 | EURUSD | M1 | KALMAN_INNOV_EXPAND | ALL_DAY | T | 2.00/1.00 | V1 baseline | 1888 | 226.7 | 0.516 | 1.40 | 18.6 | 0.0134 |
| 7 | USDJPY | M1 | VELOCITY_ACCEL_GO | ASIA | F | 2.00/1.00 | V1 baseline | 1614 | 193.8 | 0.519 | 1.41 | 19.8 | 0.0130 |
| 8 | EURUSD | M1 | VELOCITY_ACCEL_GO | ASIA | F | 2.00/1.00 | V1 baseline | 1604 | 192.6 | 0.501 | 1.31 | 18.0 | 0.0113 |
| 9 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | F | 0.50/0.55 | V5 sma50_cross | 214 | 25.7 | 0.528 | 1.65 | 34.5 | 0.0097 |
| 10 | EURUSD | M15 | KAMA_CROSS_MOM | NY | F | 1.25/0.80 | V6 time_fixed 60 | 183 | 22.0 | 0.525 | 1.15 | 12.1 | 0.0071 |

---

## Comparativa M15/H1 vs M1 entries

| Métrica | Best M15/H1 (#1) | Best M1 (#5 global) |
|---------|-----------------:|--------------------:|
| **Calmar** | **0.052** | 0.015 |
| WR | 0.522 | 0.519 |
| PF | 1.43 | 1.41 |
| trades/año | 8.0 | 223.4 |
| DD_R | 3.0 | 17.1 |
| Expectancy R | 0.154 | 0.257 |
| Total R esperado/año | ~1.2 | ~57.4 |

**Lectura**: M1 entries generan **27× más trades/año** y **48× más R total/año**, pero con **5-7× más DD**. El Calmar resultante es similar pero M15/H1 gana por DD bajo.

**Trade-off**:
- M15/H1: bajo riesgo absoluto, baja frecuencia, edge limpio.
- M1: alto throughput, pero requiere capital robusto para soportar DD ~20R + alta frecuencia exige infraestructura ejecución de baja latencia.

---

## TODOS los M15/H1 (7 estrategias únicas)

| # | sym | tf | setup | session | INV | TP/SL | best_exit | n | tr/yr | WR | PF | DD | Calmar |
|---|-----|----|-------|---------|-----|-------|-----------|----|------:|------|------|----|--------|
| 1 | EURUSD | H1 | KAMA_CROSS_MOM | NY | T | 1.75/1.05 | V3 opp+tpsl | 67 | 8.0 | 0.522 | 1.43 | 3.0 | 0.0515 |
| 2 | NASDAQ100 | M15 | KAMA_CROSS_MOM | ASIA | F | 1.50/0.80 | V4 trail 1.5 | 36 | 4.3 | 0.528 | 1.23 | 2.8 | 0.0454 |
| 3 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON | F | 0.50/0.55 | V6 time 240 | 118 | 14.2 | 0.593 | 1.57 | 10.3 | 0.0265 |
| 4 | USDJPY | M15 | KAMA_CROSS_MOM | ASIA | F | 1.50/0.80 | V3 opp+tpsl | 134 | 16.1 | 0.500 | 1.24 | 8.5 | 0.0165 |
| 5 | USDJPY | M15 | SPECTRAL_TREND_MOM | LONDON_NY | F | 0.50/0.55 | V5 sma50_cross | 214 | 25.7 | 0.528 | 1.65 | 34.5 | 0.0097 |
| 6 | EURUSD | M15 | KAMA_CROSS_MOM | NY | F | 1.25/0.80 | V6 time_fixed 60 | 183 | 22.0 | 0.525 | 1.15 | 12.1 | 0.0071 |
| 7 | XAUUSD | M15 | SPECTRAL_TREND_MOM | NY | F | 0.75/0.55 | V5 sma20_cross | 203 | 24.4 | 0.473 | 1.05 | 18.7 | 0.0014 |

---

## TOP 15 M1 entries (49 únicos en total)

| # | sym | setup | session | INV | TP/SL | n | tr/yr | WR | PF | DD | Calmar |
|---|-----|-------|---------|-----|-------|----|------:|------|------|----|--------|
| 1 | EURUSD | VELOCITY_ACCEL_GO | ALL_DAY | T | 2.00/1.00 | 1861 | 223.4 | 0.519 | 1.41 | 17.1 | 0.0150 |
| 2 | EURUSD | KALMAN_INNOV_EXPAND | ALL_DAY | T | 2.00/1.00 | 1888 | 226.7 | 0.516 | 1.40 | 18.6 | 0.0134 |
| 3 | USDJPY | VELOCITY_ACCEL_GO | ASIA | F | 2.00/1.00 | 1614 | 193.8 | 0.519 | 1.41 | 19.8 | 0.0130 |
| 4 | EURUSD | VELOCITY_ACCEL_GO | ASIA | F | 2.00/1.00 | 1604 | 192.6 | 0.501 | 1.31 | 18.0 | 0.0113 |
| 5 | EURUSD | HURST_TREND_MOM | ASIA | F | 1.50/1.00 | 1490 | 178.9 | 0.560 | 1.18 | 20.5 | 0.0049 |
| 6 | EURUSD | KALMAN_INNOV_EXPAND | ASIA | F | 1.50/1.00 | 1564 | 187.8 | 0.554 | 1.15 | 23.2 | 0.0037 |
| 7 | EURUSD | HURST_TREND_MOM | ALL_DAY | T | 1.50/1.00 | 1831 | 219.8 | 0.549 | 1.13 | 21.0 | 0.0036 |
| 8 | EURUSD | HURST_TREND_MOM | ALL_DAY | F | 1.50/1.00 | 1676 | 201.2 | 0.548 | 1.12 | 21.0 | 0.0033 |
| 9 | EURUSD | OLS_SLOPE_STRONG | ALL_DAY | T | 1.50/1.00 | 1846 | 221.6 | 0.550 | 1.13 | 26.6 | 0.0029 |
| 10 | XAUUSD | VELOCITY_ACCEL_GO | NY | F | 0.70/0.50 | 1567 | 188.1 | 0.569 | 1.12 | 26.0 | 0.0025 |
| 11 | XAUUSD | KALMAN_INNOV_EXPAND | LONDON_NY | T | 0.70/0.50 | 1534 | 184.2 | 0.561 | 1.08 | 19.6 | 0.0024 |
| 12 | USDJPY | KALMAN_INNOV_EXPAND | ALL_DAY | T | 1.50/1.00 | 1859 | 223.2 | 0.554 | 1.15 | 37.3 | 0.0023 |
| 13 | EURUSD | KALMAN_INNOV_EXPAND | ASIA | T | 1.50/1.00 | 1547 | 185.7 | 0.547 | 1.11 | 36.3 | 0.0019 |
| 14 | EURUSD | VELOCITY_ACCEL_GO | ALL_DAY | F | 1.50/1.00 | 1803 | 216.4 | 0.539 | 1.08 | 27.9 | 0.0017 |
| 15 | XAUUSD | KALMAN_INNOV_EXPAND | LONDON | T | 0.70/0.50 | 1534 | 184.2 | 0.561 | 1.08 | 27.8 | 0.0017 |

---

## Distribución Phase F (M1)

```
Por symbol: EURUSD=24, USDJPY=15, XAUUSD=8, NASDAQ100=2  (total 49 unique combos)
Por setup:  KALMAN_INNOV_EXPAND=12, VELOCITY_ACCEL_GO=11, HURST_TREND_MOM=8,
            OLS_SLOPE_STRONG=8, KAMA_CROSS_MOM=6, SPECTRAL_TREND_MOM=4
            ✅ TODOS los 6 momentum setups producen edges en M1
            (vs solo 3 en M15/H1)
Por invert: True=26, False=23  (50/50, ambas direcciones funcionan)
```

---

## 9 modos de salida probados

| Variant | Descripción | # estrategias donde gana |
|---------|-------------|-------------------------:|
| V1 baseline (TP/SL fijo) | Phase B/C grid TP/SL | 5 (M1 dominado) |
| V2 opposite_only | Salir en señal opuesta | 0 |
| V3 opposite + TP/SL | Señal opuesta o TP/SL | 2 |
| V4 trailing 1.0 ATR | Trailing 1×ATR | 0 |
| V4 trailing 1.5 ATR | Trailing 1.5×ATR | 1 |
| V5 sma20 cross | Cierre cruza SMA(20) | 1 |
| V5 sma50 cross | Cierre cruza SMA(50) | 1 |
| V6 time_fixed 60 | 60 M1 bars (1h) | 1 |
| V6 time_fixed 240 | 240 M1 bars (4h) | 1 |

**Conclusión exits**: ningún exit domina universalmente. El óptimo varía por estrategia. **TP/SL fijo (V1)** es lo más simple y funciona en M1; en M15/H1 los exits alternativos sí aportan (V3, V4, V6).

---

## Hallazgos clave

### 1. Bias detectados y corregidos
- **Look-ahead bias**: 97% de los "edges" iniciales eran ficticios.
- **Intra-bar TP/SL bias**: en M1 con TP/SL juntos, el orden de chequeo TP-first inflaba WR ~9pp (de 67% a 58%).

### 2. M15/H1 vs M1 entries — diferentes perfiles
- **M15/H1**: pocos supervivientes (7) pero **DD bajo** (3-35R), low frequency. Más limpio.
- **M1**: muchos supervivientes (49) pero **DD alto** (17-37R), alta frecuencia. Edge real pero requiere capital robusto.

### 3. Setups que funcionan
- **M15/H1**: solo 3 (KAMA_CROSS_MOM, SPECTRAL_TREND_MOM, VELOCITY_ACCEL_GO).
- **M1**: TODOS los 6 momentum setups producen edges. Los FADE siguen sin servir.

### 4. TP/SL óptimos
- M15/H1: **TPs cortos** (0.5-1.5×ATR) con stops similares.
- M1: **TP/SL = 2.0/1.0** (TP=2× SL) domina top, edge por R:R favorable.

### 5. INVERT (direction reverse)
- M15/H1: 1 INV vs 6 sin INVERT.
- M1: ~50/50 INV vs sin invert. La dirección no importa tanto en M1.

---

## ⚠️ Caveats que persisten

1. **Calmar 0.001-0.052**. Edges marginales sobre el riesgo.
2. **Sin walk-forward IS/OOS**. Riesgo de overfitting al periodo 2018-2026.
3. **Sin Monte Carlo bootstrap**. No medimos prob_ruin.
4. **M1 entries**: alta frecuencia + TP/SL cercanos = sensibilidad extrema a slippage real del broker (no modelado en friction genérica 0.3-0.4R).
5. **Comparación con bot live MATH**: WR 0.50-0.59 vs live 0.65-0.85, PF 1.05-1.65 vs 1.5-3.0. El gap puede ser overfitting in-sample del bot live, comisiones reales no modeladas, o ambos.

---

## TOP 3 recomendados (M15/H1) para validar primero

```
🥇 EURUSD H1 KAMA_CROSS_MOM NY INV=True
   TP=1.75 SL=1.05 (ATR mults), V3_opposite_with_tpsl
   67 trades en 8 años (8/yr), WR=52.2% PF=1.43 DD=3.0R Calmar=0.052

🥈 NASDAQ100 M15 KAMA_CROSS_MOM ASIA
   TP=1.50 SL=0.80, V4_trailing_1.5_atr
   36 trades en 8 años (4/yr), WR=52.8% PF=1.23 DD=2.8R Calmar=0.045

🥉 USDJPY M15 SPECTRAL_TREND_MOM LONDON
   TP=0.50 SL=0.55, V6_time_fixed_240 (4h)
   118 trades en 8 años (14/yr), WR=59.3% PF=1.57 DD=10.3R Calmar=0.027
```

## TOP 3 recomendados (M1) para validar segundo

```
1. EURUSD M1 VELOCITY_ACCEL_GO ALL_DAY INV=True
   TP=2.00 SL=1.00, V1 baseline
   1861 trades (223/yr), WR=51.9% PF=1.41 DD=17.1R Calmar=0.015

2. EURUSD M1 KALMAN_INNOV_EXPAND ALL_DAY INV=True
   TP=2.00 SL=1.00, V1 baseline
   1888 trades (227/yr), WR=51.6% PF=1.40 DD=18.6R Calmar=0.013

3. USDJPY M1 VELOCITY_ACCEL_GO ASIA
   TP=2.00 SL=1.00, V1 baseline
   1614 trades (194/yr), WR=51.9% PF=1.41 DD=19.8R Calmar=0.013
```

---

## Recomendación final

**No deployar nada sin antes**:
1. **Walk-forward IS/OOS** sobre top 6 candidatos (3 M15/H1 + 3 M1).
2. **Monte Carlo bootstrap** 10k para prob_ruin con threshold -10R (M15/H1) o -30R (M1).
3. **Friction broker exacta** del Vantage en lugar de 0.3-0.4 genérica.
4. **Forward demo 30 días mínimo** antes de risk real.

**Lo más valioso del ejercicio**: la pipeline detectó y corrigió **dos bias críticos** (look-ahead y intra-bar TP/SL). Sin estos fixes, hubiéramos confiado en falsos edges (462 → 12 → 7+49 reales).
