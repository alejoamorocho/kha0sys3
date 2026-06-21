# Informe — Estrategias positivas en vivo medidas en PIPS

**Fecha:** 2026-06-20 · **Ventana:** post-purga profit-only (desde 2026-06-09 20:00 UTC, ~11 días)
**Cuenta:** Vantage DEMO 25246666 · Balance $380,897 · **Solo trades cerrados**

## Por qué pips y no dólares

El bot **MATH (magic 1338) está sobredimensionado ~10–30×** vs AMO8/ORB (opera 100 lotes en FX,
500 en SP500, donde debería ir 7–8 y ~13). Eso infla artificialmente su P&L en dólares y **hace
imposible comparar edge entre estrategias por saldo**. Los **pips** (movimiento de precio normalizado
por el pip-size del símbolo, ponderado por volumen en cierres parciales) eliminan el tamaño de posición.
El **PF y el WR son las métricas comparables reales**; los pips netos solo son comparables *dentro del
mismo activo* (un pip de NAS100 ≠ un pip de GBPUSD).

## Ranking por pips netos (10 estrategias con pips > 0)

| # | Bot | Símbolo | Estrategia | n | WR | PF | Pips netos | Pips/op | $ ref |
|---|-----|---------|-----------|---|----|----|-----------|---------|-------|
| 1 | AMO8 | NAS100 | OR_·FBD·081 | 7 | 86% | **7.60** | +19,552 | +2,793 | +$1,115 |
| 2 | AMO8 | SP500 | OR_·FBD·018 | 6 | 83% | **9.09** | +6,006 | +1,001 | +$1,145 |
| 3 | AMO8 | XAUUSD | OR_·FBD·046 | 5 | 60% | **5.27** | +4,325 | +865 | +$477 |
| 4 | AMO8 | SP500 | OR_·FBU·066 | 7 | 57% | 1.67 | +2,202 | +315 | +$268 |
| 5 | AMO8 | XAUUSD | OR_·FBU·112 | 7 | 57% | 1.17 | +341 | +49 | +$329 |
| 6 | MATH | XAUUSD | M1·KALMAN·LDN | 8 | 62% | 1.18 | +137 | +17 | +$3,043 |
| 7 | ORB | GBPJPY | 07h30m | 3 | 100% | INF | +64.4 | +21.5 | +$1,122 |
| 8 | AMO8 | XAGUSD | OR_·FBU·033 | 1 | 100% | INF | +22.0 | +22.0 | +$286 |
| 9 | MATH | GBPUSD | M15·HURST·ASIA | 3 | 100% | INF | +9.8 | +3.3 | +$4,823 |
| 10 | MATH | GBPJPY | M1·HURST·ALLDAY | 7 | 57% | 1.27 | +2.5 | +0.4 | −$1,795 |

> El #1 y #2 dominan en pips solo porque el pip de índice (0.01) es una unidad pequeña: +19,552 pips de
> NAS100 = ~195 puntos de índice. Por eso **no rankees por pips entre activos distintos**.

## Ranking por edge real (PF), filtrando n ≥ 5

Este es el orden que importa para decidir capital — PF y WR no dependen del tamaño:

| # | Estrategia | n | WR | PF | Pips/op | Veredicto |
|---|-----------|---|----|----|---------|-----------|
| 1 | AMO8 · SP500 · OR_·FBD·018 | 6 | 83% | **9.09** | +1,001 | Edge fuerte |
| 2 | AMO8 · NAS100 · OR_·FBD·081 | 7 | 86% | **7.60** | +2,793 | Edge fuerte |
| 3 | AMO8 · XAUUSD · OR_·FBD·046 | 5 | 60% | **5.27** | +865 | Edge fuerte |
| 4 | AMO8 · SP500 · OR_·FBU·066 | 7 | 57% | 1.67 | +315 | Edge moderado |
| 5 | MATH · GBPJPY · M1·HURST·ALLDAY | 7 | 57% | 1.27 | +0.4 | Marginal (− en $) |
| 6 | MATH · XAUUSD · M1·KALMAN·LDN | 8 | 62% | 1.18 | +17 | Marginal |
| 7 | AMO8 · XAUUSD · OR_·FBU·112 | 7 | 57% | 1.17 | +49 | Marginal |

**Provisionales (n < 5, muestra insuficiente):** ORB GBPJPY 07h30 (PF INF, n3), MATH GBPUSD HURST ASIA
(PF INF, n3), AMO8 XAGUSD FBU·033 (n1). Buenos indicios pero aún sin confirmar.

## Conclusiones

1. **El edge real vive en AMO8 false-break (FBD/FBU) sobre índices y oro.** SP500·018, NAS100·081 y
   XAUUSD·046 tienen PF 5–9 con WR 60–86% — son las que de verdad están ganando.
2. **Los "ganadores" de MATH eran un espejismo del sobredimensionamiento.** KALMAN·LDN se veía +$3,043 y
   HURST·ASIA +$4,823, pero en pips son apenas +137 y +9.8 (PF ~1.18). El edge es mínimo; los dólares solo
   reflejaban lotes enormes en los aciertos. MATH GBPJPY·HURST·ALLDAY es el caso extremo: **positivo en
   pips (+2.5) pero −$1,795 en dólares**, porque sus pérdidas iban sobredimensionadas.
3. **Implicación:** el sobredimensionamiento de MATH no solo amplifica pérdidas — también disfraza de
   "ganadoras" a estrategias sin edge. Corregir el sizing es prerequisito para evaluar MATH con justicia.

## Nota técnica — pip-size usado (1 pip =)

FX 5 dígitos (GBPUSD/AUDUSD/GBPAUD): 0.0001 · JPY (GBPJPY/EURJPY/USDJPY): 0.01 ·
Oro/Plata/Índices/Petróleo (XAUUSD/XAGUSD/NAS100/SP500/UKOUSD/USOUSD/NG): 0.01
Fuente: `scripts/_report_pips_postpurge.py` (corre en VPS sobre `history_deals_get`).
