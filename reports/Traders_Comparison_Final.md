# Comparativa Final — PDF-strict vs Grid-uniform vs K3M1-75

Backtest 2018-2026 (8 años), 14 símbolos. Tres variantes evaluadas:

| Variante | Reglas |
|---|---|
| **Grid-uniform** | Mi grid: `sl_atr ∈ {0.5,1,1.5}×ATR`, `partial_R ∈ {2,3}`, max_hours 4-8h (ORB) / 15-30d (swing), trail variable |
| **PDF-strict** | Reglas EXACTAS del PDF: Minervini 7.5%/SMA10, Zanger 8%/+15%/SMA20/2d, Qulla 1×ATR+30%d3+20%d5+SMA50, Ryan 7%/+22%/SMA50, ORB Range Low+30%d3+20%d5+SMA50/max 10d |
| **K3M1-75** | Sistema live actual (math fade momentum) |

## Resumen ejecutivo

| Variante | Estrategias positivas | Avg PF | Avg PF OOS | sum_R total |
|---|---|---|---|---|
| Grid-uniform Qulla ORB | 12/14 | 2.47 | 2.34 | +17,040R |
| Grid-uniform Swing | 7 | 1.71 | 2.12 | +769R |
| **Grid-uniform total** | **19** | – | **2.3** | **+17,809R** |
| PDF-strict Qulla ORB | 11/14 (PF 1.1-1.5) | 1.20 | 1.30 | +3,005R |
| PDF-strict Swing winners (PF≥1.5) | 3 | 1.92 | 3.69 | +366R |
| **PDF-strict total** | **3 viables + 11 marginales** | – | – | **+3,371R** |
| K3M1-75 live | 75 | 2.86 | 2.88 | (proxy +20,000R) |

**Verdict**: **Grid-uniform supera a PDF-strict en 5× en sum_R total**. Los PDFs están calibrados para STOCKS que se mueven en %; FX/commodities tienen otro perfil de volatilidad/whipsaw donde ATR-based stops y horizons más cortos funcionan mejor.

---

## 1. Side-by-side por (symbol, trader_setup)

### 1a. Qulla ORB — comparación directa

| Símbolo | Grid PF | Grid OOS | Grid n | Grid WR | | PDF PF | PDF OOS | PDF n | PDF WR | Delta sum_R |
|---|---|---|---|---|---|---|---|---|---|---|
| XAUUSD | **2.70** | **2.96** | 1442 | 51% | | 1.55 | 1.53 | 1442 | 15% | grid +678R |
| WTI | **2.79** | **2.24** | 1639 | 51% | | 1.24 | 1.29 | 1540 | 21% | grid +1517R |
| NASDAQ100 | **2.33** | **2.05** | 1758 | 54% | | 1.17 | 1.21 | 1758 | 15% | grid +1702R |
| EURUSD | **2.41** | **2.64** | 1691 | 51% | | 1.13 | 1.10 | 1493 | 15% | grid +1462R |
| BRENT | **2.72** | **2.34** | 1543 | 52% | | 1.38 | 1.41 | 1601 | 13% | grid +981R |
| GBPJPY | **2.75** | **2.64** | 1454 | 56% | | 1.42 | 1.23 | 1454 | 19% | grid +939R |
| GBPUSD | **2.67** | **2.43** | 1603 | 60% | | 1.29 | 1.12 | 1463 | 16% | grid +1029R |
| USDJPY | **2.28** | 1.62 | 1569 | 51% | | 1.45 | 1.49 | 1437 | 18% | grid +758R |
| AUDUSD | **2.26** | **2.58** | 1574 | 50% | | 0.85 | 0.59 | 1465 | 12% | grid +1689R |
| GBPAUD | **2.38** | **2.67** | 1452 | 57% | | 1.27 | 1.29 | 1452 | 16% | grid +743R |
| EURJPY | **2.08** | 2.09 | 1633 | 56% | | 1.16 | 1.13 | 1501 | 17% | grid +862R |
| XAGUSD | **2.28** | 2.22 | 1419 | 55% | | 1.55 | 1.60 | 1419 | 24% | grid +316R |
| SP500 | – | – | – | – | | 0.86 | 0.80 | 1723 | 15% | (-419R PDF) |
| NATGAS | – | – | – | – | | 0.41 | 0.40 | 1299 | 18% | (-1939R PDF) |

**Patrón claro**: Grid-uniform Qulla ORB **gana en TODOS los 12 símbolos**, ~$1000R promedio por símbolo. Razones:
- **SL 0.5×ATR (tight) vs Range Low (~4-8% wide)**: la pérdida promedio en PDF es 4-8× más grande, requiere WR mucho mayor que no se logra.
- **Max 4-8h vs 10 días**: el edge del ORB es **intradía** (momentum del breakout fresco). Mantener 10 días expone a whipsaws y mean-reversion.
- **WR colapsa de 50-60% (grid) a 13-24% (PDF)**: con Range Low SL el trade tiene que recorrer mucho para llegar a TP1, raro en FX.

### 1b. Swing setups — comparación directa

| Símbolo | Setup | Grid PF | Grid OOS | | PDF PF | PDF OOS | Winner |
|---|---|---|---|---|---|---|---|
| XAUUSD | **Minervini_VCP** | 1.79 | 2.30 | | **2.24** | **6.83** ⭐ | **PDF gana** |
| XAGUSD | **Qulla_HTF** | 1.96 | 1.84 | | **2.30** | **2.08** | **PDF gana** (FUERTE clean) |
| XAUUSD | Qulla_HTF | 1.72 | 2.64 | | 1.51 | 2.15 | grid gana |
| XAGUSD | Minervini_VCP | 1.47 | 1.80 | | 1.24 | 2.35 | grid gana |
| BRENT | Minervini_VCP | 1.57 | 1.96 | | 0.92 | 0.83 | grid gana |
| WTI | Qulla_HTF | – | – | | 1.22 | 1.57 | PDF marginal |
| BRENT | Qulla_HTF | – | – | | 1.13 | 1.59 | PDF marginal |
| NATGAS | Minervini_VCP | 1.58 | – | | 1.09 | – | grid gana |

**3 ganadores PDF-strict claros**:
1. ⭐ **XAUUSD Minervini_VCP** (PF 2.24 IS, **PF OOS 6.83**) — el SL 7.5% + parciales 2R/4R + trail SMA10 captura las tendencias largas del oro mejor que cualquier ATR
2. ⭐ **XAGUSD Qulla_HTF** (PF 2.30 IS, OOS 2.08) — **FUERTE clean** (sin flags) — única estrategia clasificada FUERTE pura del experimento entero
3. **XAUUSD Qulla_HTF** (PF 1.51 IS, OOS 2.15) — coherente IS/OOS

### 1c. Setups PDF que NO funcionan en FX

| Setup | n syms positivos | Avg PF | Diagnóstico |
|---|---|---|---|
| **Zanger_FLAG** | **0/14** | **0.07** | Disaster total. 8% SL muy laxo + 50%@+15% target casi imposible en FX. WR ~0 en todos. |
| Ryan_ANTS | 1/14 (XAUUSD 16 trades) | 0.41 | Casi no dispara (umbrales FX-calibrados pero PDF strict exit con SL 7% mata trades) |
| Zanger_CUP | 0/14 (no signals) | – | Cup&Handle stock pattern no se forma en FX |
| Qulla_EP | 0/14 (no signals) | – | Gap >+1% no existe en FX 24/7 |

---

## 2. Análisis cualitativo: ¿por qué grid > PDF en FX?

1. **% fijos no escalan a FX**: 7-8% SL en stocks ≈ 3-4× ATR diario. En FX 8% es 8-15× ATR — un "cinturón de seguridad" tan ancho que solo se activa en cisne negro, pero la pérdida cuando se activa es masiva.

2. **Target +15% from entry (Zanger)**: stocks momentum pueden subir +15% en días. En FX EURUSD subir +15% son ~150 días en tendencia. PDF rule no hits.

3. **Range Low SL (Qulla ORB)**: el rango de apertura en M1 puede ser muy ancho (gap nocturno + primeros 30 min volatiles). Range Low promedio 4-8% bajo entry → risk muy grande, exp_R por trade colapsa.

4. **10-day hold (Qulla ORB PDF)**: el ORB captura momentum **intradía** (4-8h donde el flujo institucional se concentra). Mantener 10 días expone a mean-reversion natural — el edge desaparece.

5. **Trail SMA10/20 (Minervini/Zanger)**: en FX, SMA10/20 son muy reactivas — se activan en pullbacks normales, cortando ganadoras antes de tiempo. SMA50 funciona mejor.

---

## 3. Donde el PDF SÍ gana: metales con tendencia secular

XAUUSD y XAGUSD presentan **tendencias seculares multi-mensuales** que los PDFs (diseñados para growth stocks tendenciales) capturan mejor que mis grid genéricos:

- XAUUSD Minervini_VCP PDF: 7.5% SL es amplio pero el oro hace movimientos de +20-40% sin pullback significativo → 2R/4R partials capturan el premium completo, SMA10 trail aguanta.
- XAGUSD Qulla_HTF PDF: 1×ATR_D1 SL + holds hasta 40 días + SMA50 trail captura las "banderas altas" características del rally 2020-2024 plata.

**Insight**: los PDFs **están bien diseñados para activos con tendencias estructurales fuertes**, no para FX ranging. Donde el activo SÍ tiene perfil "growth stock" (metales), las reglas PDF se sostienen.

---

## 4. Decisión recomendada

### Portfolio FX/commodities/indices candidato

| Sistema | Estrategias | Filosofía | Sizing recomendado |
|---|---|---|---|
| **K3M1-75 (live actual)** | 75 fade-momentum | INVERT | 0.5% × ~5 strats simultáneas = 2.5% sym exposure |
| **Grid Qulla ORB** | top 6: WTI/XAUUSD/BRENT/NASDAQ100/EURUSD/GBPJPY | LONG ORB intradía | 0.1-0.15% × 6 = 0.9% expected |
| **PDF-strict swing** | 3 winners: XAUUSD-VCP, XAGUSD-HTF, XAUUSD-HTF | LONG swing 30-60d | 0.2% × 3 = 0.6% |

Total exposure: **~4% account** distribuido en 3 filosofías independientes (fade math, breakout intradía, swing trend-following stocks-style).

Las 3 son **direccionalmente opuestas** entre sí (K3M1-75 fadea, ORB compra el breakout, swing aguanta tendencia larga) → drawdowns rotados en el tiempo.

### Próximos pasos sugeridos

1. **Paper-deploy las 3 swing PDF winners** durante 2-3 meses con 0.05% sizing — validar slippage real, especialmente el fill del STOP en break del pivot diario.
2. **Deploy las top 6 ORB grid-uniform** después del paper period — son las que mejor performance OOS demostraron.
3. **No tocar K3M1-75 live** — sigue siendo el sistema dominante (PF 2.88 OOS, 75 strats diversificadas).
4. **NO desplegar Zanger ni Ryan ANTS**: PDF strict los demuestra inviables en FX, y los grid uniformes apenas marginales.

---

## 5. Archivos

- [reports/Traders_PDF_Strict.md](reports/Traders_PDF_Strict.md) — detalle PDF-strict
- [reports/Qulla_ORB_Robustness.md](reports/Qulla_ORB_Robustness.md) — detalle grid Qulla ORB
- [reports/Traders_Swing_Robustness.md](reports/Traders_Swing_Robustness.md) — detalle grid swing
- [reports/traders_pdf_strict.parquet](reports/traders_pdf_strict.parquet) — fuente de verdad PDF
- [reports/qulla_orb_robustness.parquet](reports/qulla_orb_robustness.parquet) — fuente grid ORB
- [reports/traders_swing_robustness.parquet](reports/traders_swing_robustness.parquet) — fuente grid swing
- [scripts/run_traders_pdf_strict.py](scripts/run_traders_pdf_strict.py) — runner PDF-strict
- [scripts/run_qulla_orb_grid.py](scripts/run_qulla_orb_grid.py) — runner grid ORB
- [scripts/run_traders_swing_grid.py](scripts/run_traders_swing_grid.py) — runner grid swing
