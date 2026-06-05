# Pivot Fade — Análisis de Gestión (R:R)

**Setups simulados:** 93,818 · SL=1R (siguiente nivel pivot) · fricción 0.3R · SL-first

WR = alcanza TP (rr·R favorable) antes del SL (1R adverso). Expectancy neta de fricción. R:R≥1 respetado.

## Por setup (todos los símbolos/horas)


### R1_D_DOWN_SHORT  (n=14,287)

| R:R | WR | expectancy_R | PF |
|---|---|---|---|
| 1:0.5 | 35% | -0.583 | 0.34 |
| 1:1.0 | 24% | -0.509 | 0.45 |
| 1:1.5 | 16% | -0.493 | 0.45 |
| 1:2.0 | 12% | -0.498 | 0.43 |
| 1:3.0 | 7% | -0.516 | 0.38 |

### R1_D_UP_SHORT  (n=15,349)

| R:R | WR | expectancy_R | PF |
|---|---|---|---|
| 1:0.5 | 34% | -0.637 | 0.31 |
| 1:1.0 | 24% | -0.556 | 0.42 |
| 1:1.5 | 18% | -0.524 | 0.46 |
| 1:2.0 | 13% | -0.517 | 0.46 |
| 1:3.0 | 8% | -0.542 | 0.40 |

### PP_D_DOWN_SHORT  (n=24,309)

| R:R | WR | expectancy_R | PF |
|---|---|---|---|
| 1:0.5 | 36% | -0.584 | 0.35 |
| 1:1.0 | 26% | -0.496 | 0.49 |
| 1:1.5 | 19% | -0.468 | 0.51 |
| 1:2.0 | 14% | -0.473 | 0.48 |
| 1:3.0 | 7% | -0.516 | 0.39 |

### R2_D_UP_SHORT  (n=7,890)

| R:R | WR | expectancy_R | PF |
|---|---|---|---|
| 1:0.5 | 30% | -0.691 | 0.26 |
| 1:1.0 | 21% | -0.621 | 0.35 |
| 1:1.5 | 16% | -0.588 | 0.39 |
| 1:2.0 | 13% | -0.571 | 0.41 |
| 1:3.0 | 9% | -0.565 | 0.41 |

### PP_D_UP_SHORT  (n=24,422)

| R:R | WR | expectancy_R | PF |
|---|---|---|---|
| 1:0.5 | 37% | -0.559 | 0.38 |
| 1:1.0 | 26% | -0.474 | 0.50 |
| 1:1.5 | 18% | -0.451 | 0.52 |
| 1:2.0 | 13% | -0.462 | 0.48 |
| 1:3.0 | 7% | -0.507 | 0.37 |

### S2_D_DOWN_LONG  (n=7,561)

| R:R | WR | expectancy_R | PF |
|---|---|---|---|
| 1:0.5 | 31% | -0.331 | 0.48 |
| 1:1.0 | 17% | -0.302 | 0.48 |
| 1:1.5 | 11% | -0.304 | 0.44 |
| 1:2.0 | 7% | -0.323 | 0.38 |
| 1:3.0 | 3% | -0.366 | 0.24 |

## Mejor horario por setup (R:R 1:1)

| setup | mejor hora UTC | n | WR | exp_R |
|---|---|---|---|---|

## EDGE ESTRELLA S2_D_DOWN_LONG · por símbolo (R:R 1:1)

| símbolo | n | WR | exp_R | PF |
|---|---|---|---|---|
| AUDUSD | 544 | 15% | -0.290 | 0.45 |
| BRENT | 375 | 3% | -0.266 | 0.13 |
| EURJPY | 542 | 18% | -0.244 | 0.57 |
| EURUSD | 578 | 18% | -0.299 | 0.52 |
| GBPAUD | 496 | 15% | -0.248 | 0.50 |
| GBPJPY | 524 | 18% | -0.253 | 0.56 |
| GBPUSD | 576 | 20% | -0.258 | 0.61 |
| NASDAQ100 | 587 | 22% | -0.315 | 0.57 |
| NATGAS | 541 | 17% | -0.330 | 0.46 |
| SP500 | 580 | 18% | -0.336 | 0.48 |
| USDJPY | 535 | 17% | -0.281 | 0.51 |
| WTI | 570 | 16% | -0.380 | 0.41 |
| XAGUSD | 565 | 17% | -0.350 | 0.44 |
| XAUUSD | 548 | 17% | -0.358 | 0.43 |

## Notas

- 1R = distancia entry→siguiente nivel pivot en dirección de ruptura (SL ahí).

- SL-first en empates. 'neither' (ni TP ni SL ese día) = -0.2R timeout.

- Fricción 0.3R/trade. R:R≥1 = tu mínimo.

---

## VEREDICTO FINAL — el edge NO es operable

**Hallazgo clave:** MFE ≈ MAE en TODOS los setups (movimiento simétrico).

| setup | MFE p50 | MAE p50 | simetría |
|---|---|---|---|
| PP_D_UP_SHORT | 0.87R | 0.88R | idéntico |
| R1_D_UP_SHORT | 1.05R | 1.08R | idéntico |
| R1_D_DOWN_SHORT | 0.90R | 0.92R | idéntico |
| PP_D_DOWN_SHORT | 0.92R | 0.94R | idéntico |
| R2_D_UP_SHORT | 1.15R | 1.26R | idéntico |
| S2_D_DOWN_LONG | 0.38R | 0.39R | idéntico |

**Conclusión:** El "edge direccional" del 70% (estudio de transición) era un
artefacto de medir qué nivel toca primero con el CLOSE. El recorrido REAL del
precio (MFE/MAE con mechas) es **simétrico** — se mueve igual a favor y en
contra. Con fricción 0.3R, NINGUNA combinación de SL/TP con R:R≥1 da
expectancy positivo. El mejor caso de cada setup es exp ≈ -0.5R.

**Por qué falla:**
- El SL se ejecuta con la mecha (high/low toca el nivel), no con el close.
- Las mechas intradía tocan el SL antes de que el TP se alcance.
- Los pivots clásicos NO predicen movimiento favorable NETO en estos activos.

**Recomendación:** descartar pivot points clásicos como fuente de edge
direccional para trading sistemático. El estudio fue riguroso (14 activos,
daily+weekly, 2018-2026, 93,818 setups simulados) y el resultado es robusto.
