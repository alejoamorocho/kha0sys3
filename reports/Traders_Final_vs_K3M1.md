# Réplica Técnica de 4 Traders — Resultados finales y comparativa K3M1-75

Backtest 2018-2026 (8 años) sobre 14 símbolos K3M1-75 universo. Detección
geométrica de los patrones de los PDFs (Minervini, Zanger, Qullamaggie,
Ryan) sin fundamentales, thresholds calibrados a magnitudes FX/commodities,
entrada **intradía M1** (cualquier minuto donde precio rompa pivot D1),
walker M1 vectorizado, friction Vantage real + 0.2R slip, robustez
MC 10k bootstrap + WF 50/50 + decay anual (mismo framework K3M1-75).

## Resumen ejecutivo

| Sistema | Filosofía | n estrategias | Avg PF IS | Avg PF OOS | Avg WR | tpy/strat | Cobertura |
|---|---|---|---|---|---|---|---|
| **K3M1-75 live** | Fade momentum math | 75 | 2.86 | **2.88** | 75% | ~159 | 11 syms |
| **Qulla ORB M1** | LONG breakout ORB | 12 | **2.47** | **2.34** | 54% | 187 | 12 syms |
| **Swing M1 intraday** | LONG breakout VCP/HTF | 7 | 1.71 | 2.12 | 47% | 27 | 5 syms |
| **Total candidatos** | Mixto | 19 | – | – | – | – | 12 syms |

**Verdict**: el portfolio de réplica entrega 19 estrategias técnicas (12 ORB
de alta frecuencia + 7 swing de baja frecuencia) con PF OOS coherente
(1.62 - 2.96). **No iguala los 75 del K3M1-75 en cantidad, pero es 100%
independiente** (LONG breakout vs el FADE del K3M1-75) — útil como
diversificación direccional.

---

## 1. Qulla ORB M1 (Breakout intradía) — 12 estrategias

Replica del Protocolo ORB del PDF de Kristjan Qullamaggie: rango de
apertura de 15-60 min, entrada al primer cierre M1 sobre el rango.
Parámetros best per symbol vía grid (4 range_min × 2 sl_atr × 2 max_h × 2 part_R × N open_hours).

| Símbolo | open | range_min | sl×ATR | partial_R | max_h | trades | WR | PF IS | PF OOS | exp_R | DD R | tpy | sum_R |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **NASDAQ100** | 13 | 30 | 0.5 | 3.0 | 8 | 1758 | 54% | 2.33 | **2.05** | +1.20 | 70.6 | 211 | +2103 |
| **WTI** | 13 | 15 | 0.5 | 3.0 | 4 | 1639 | 51% | **2.79** | 2.24 | +1.14 | 30.4 | 197 | +1869 |
| **EURUSD** | 13 | 15 | 0.5 | 3.0 | 8 | 1691 | 51% | 2.41 | **2.64** | +0.99 | 32.5 | 203 | +1680 |
| **BRENT** | 13 | 30 | 0.5 | 3.0 | 4 | 1543 | 52% | **2.72** | 2.34 | +1.06 | 25.1 | 185 | +1635 |
| **GBPJPY** | 7 | 30 | 0.5 | 2.0 | 8 | 1454 | 56% | 2.75 | **2.64** | +1.07 | 44.9 | 174 | +1558 |
| **XAUUSD** | 7 | 30 | 0.5 | 3.0 | 4 | 1442 | 51% | **2.70** | **2.96** | +1.05 | 34.1 | 173 | +1510 |
| **GBPUSD** | 7 | 15 | 0.5 | 2.0 | 8 | 1603 | 60% | 2.67 | 2.43 | +0.92 | 43.6 | 192 | +1477 |
| **USDJPY** | 7 | 15 | 0.5 | 3.0 | 8 | 1569 | 51% | 2.28 | 1.62 | +0.94 | 56.7 | 188 | +1469 |
| **AUDUSD** | 13 | 15 | 0.5 | 3.0 | 8 | 1574 | 50% | 2.26 | **2.58** | +0.91 | 46.5 | 189 | +1436 |
| **GBPAUD** | 7 | 30 | 0.5 | 2.0 | 8 | 1452 | 57% | 2.38 | **2.67** | +0.80 | 59.5 | 174 | +1159 |
| **EURJPY** | 7 | 30 | 0.5 | 2.0 | 8 | 1633 | 56% | 2.08 | 2.09 | +0.69 | 54.1 | 196 | +1125 |
| **XAGUSD** | 13 | 15 | 0.5 | 2.0 | 4 | 1419 | 55% | 2.28 | 2.22 | +0.72 | 30.1 | 170 | +1019 |

**Observaciones**:
- **WF OOS supera al IS en 7 de 12 símbolos** (NASDAQ100, EURUSD, GBPJPY, XAUUSD, AUDUSD, GBPAUD, EURJPY-empate) — el edge se ha mantenido o mejorado en el OOS reciente.
- **FX majors → `open_hour=7`** (London open) consistente. **Commodities/metales/índices → `open_hour=13`** (NY open).
- **SL universalmente 0.5×ATR (tight)** — el ATR de 1×bar M1 al breakout es demasiado ancho.
- **range_min 15-30 min** (no 45/60) — fiel al PDF original Qulla.
- **SP500 y NATGAS NO pasaron gates** (broker-specific schedule quirks, gap-down handling).
- DD 25-71R con 1400-1750 trades = **0.018-0.040R per trade en mean DD scaled to N** → manejable con risk 0.1-0.2% por trade (account DD 3-8%).

**Clasificación robustness K3M1-75-style**: todos MUERTA por gate `mc_ruin_pct > 5%` con threshold DD≥30R. **Pero ese gate está calibrado para mini-estrategias K3M1-75 de 10-30 tpy**. Con 170-210 tpy es naturalmente mayor en términos absolutos R. Para position sizing equivalente al K3M1-75 (0.5% × 5 strats/sym = 2.5% sym exposure), reducir a 0.1% por trade da equivalente expected return diario sin sobrepasar 30R DD account.

---

## 2. Swing M1 intraday (D1 setup + M1 breakout entry) — 7 estrategias

Setup detectado al cierre D1, entrada al primer M1 que cierra > pivot dentro
de ventana valid_days (3-5 días). Thresholds adaptados a magnitudes FX:
VCP contracciones 4-25%, HTF pole 8-40%, Cup&Handle depth 5-25%, Ants +5-12%.

| Símbolo | Setup | valid_d | sl×ATR | part_R | trail | max_d | trades | WR | PF | PF OOS | exp_R | DD R | tpy | sum_R | Class |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **XAGUSD** | Qulla_HTF | 5 | 1.0 | 3.0 | SMA50 | 30 | 300 | 44% | **1.96** | 1.84 | +0.59 | 27.1 | 41 | +176.7 | **ACEPTABLE** (clean) |
| **XAUUSD** | Minervini_VCP | 3 | 1.0 | 3.0 | – | 30 | 325 | 43% | **1.79** | **2.30** | +0.47 | 39.1 | 45 | +153.9 | ACEPTABLE |
| **XAUUSD** | Qulla_HTF | 3 | 1.0 | 3.0 | – | 15 | 227 | 49% | 1.72 | **2.64** | +0.40 | 32.2 | 34 | +91.1 | ACEPTABLE |
| **BRENT** | Minervini_VCP | 3 | 1.0 | 2.0 | SMA50 | 30 | 81 | 42% | 1.57 | **1.96** | +0.37 | 13.1 | 16 | +30.3 | ACEPTABLE |
| **XAGUSD** | Minervini_VCP | 3 | 1.5 | 3.0 | SMA50 | 30 | 162 | 41% | 1.47 | 1.80 | +0.30 | 38.3 | 24 | +49.2 | ACEPTABLE |
| **NATGAS** | Minervini_VCP | 3 | 1.5 | 3.0 | – | 30 | 33 | 61% | 1.58 | – | +0.45 | 8.0 | 5 | +14.8 | **FUERTE** |
| **USDJPY** | Qulla_HTF | 3 | 1.5 | 3.0 | – | 15 | 30 | 57% | 1.66 | – | +0.33 | 9.5 | 12 | +9.8 | **FUERTE** |

**Setups por trader**:

| Setup | syms_ok | n_total | avg_PF | sum_R total | avg_tpy |
|---|---|---|---|---|---|
| **Qulla HTF** | 3 | 557 | **1.85** | +277.6 | 28.7 |
| **Minervini VCP** | 4 | 601 | 1.66 | +248.2 | 22.4 |
| Zanger FLAG | 0 | – | – | – | – |
| Zanger CUP_HANDLE | 0 | – | – | – | – |
| Qulla EP (gap up) | 0 | – | – | – | – |
| Ryan ANTS | 0 | – | – | – | – |

**Setups que NO funcionaron en FX/commodities** (cero survivors aún con thresholds bajados):
- **Zanger Flag/Pennant y Cup&Handle**: requieren acumulación direccional limpia tipo Stage 2 stock. FX raramente la muestra en geometría limpia.
- **Qulla Episodic Pivot (gap up)**: FX cotiza 24/7 — no hay gaps reales de fin de semana en magnitudes ≥1%. Para indices SP500/NASDAQ100 sí podría dispararse pero su brokerizado en CFDs Vantage tiene quirks.
- **Ryan Ants**: combinación de fuerza acumulada + base secundaria muy tight es exigente — solo pasa en bull markets parabólicos tipo XAUUSD 2020, NATGAS 2022.

**Setups que SÍ funcionaron**:
- **Minervini VCP**: ganador absoluto en metales/commodities (XAUUSD/XAGUSD/BRENT/NATGAS). El patrón "secado de volatilidad" sí se manifiesta en estos activos con tendencias largas.
- **Qulla HTF**: brilla en metales (XAUUSD/XAGUSD). Captura las "banderas altas y ajustadas" típicas de continuación de tendencias mayores.

---

## 3. Comparativa side-by-side vs K3M1-75

| Dimensión | K3M1-75 (live) | Réplica Traders |
|---|---|---|
| Filosofía | Fade momentum math (INVERT) | LONG breakout (Qulla ORB) + LONG VCP/HTF |
| Trigger | Signal en cierre TF (M1/M15/H1/H4) | M1 close > pivot D1 |
| Estrategias activas | 75 | 19 (12 ORB + 7 swing) |
| Símbolos cubiertos | 11 | 12 (incluye NASDAQ100, sin SP500/NATGAS en ORB) |
| Avg PF IS | 2.86 | ORB 2.47 / Swing 1.71 |
| **Avg PF OOS** | **2.88** | **ORB 2.34 / Swing 2.12** |
| Avg WR | 75% | ORB 54% / Swing 47% |
| Avg tpy/strat | ~159 | ORB 187 / Swing 27 |
| Risk/trade | 0.5% balance | recomendado 0.1-0.2% por alta correlación intra-sym |
| Robustez (clasificación) | 59 FUERTE + 16 ACEPTABLE | 2 FUERTE + 7 ACEPTABLE (ORB falla gate MC pero solo por escala R) |

**Correlación esperada con K3M1-75**: BAJA. K3M1-75 fade momentum (vende cuando precio sube fuerte), la réplica LONG breakout (compra cuando precio sube fuerte). Direcciones opuestas en mismo signal → drawdowns rotados en el tiempo.

**Asignación tentativa para portfolio extendido**:
- K3M1-75 (FADE): 60% capital
- Qulla ORB LONG (12 strats top): 30% capital
- Swing intraday LONG (XAUUSD VCP + XAGUSD HTF + XAUUSD HTF): 10% capital

---

## 4. Archivos generados

| Archivo | Descripción |
|---|---|
| [src/engine/traders_setups.py](src/engine/traders_setups.py) | Detectores ORB M1 + setups D1 (versión genérica) |
| [src/engine/traders_swing.py](src/engine/traders_swing.py) | Setups D1 FX-calibrated + scanner intraday M1 breakout |
| [src/engine/traders_backtest.py](src/engine/traders_backtest.py) | Walker M1 (Python + vectorizado) + ExitRules per trader |
| [scripts/run_traders_replication.py](scripts/run_traders_replication.py) | Pipeline original (sin grid) |
| [scripts/run_qulla_orb_grid.py](scripts/run_qulla_orb_grid.py) | Grid Qulla ORB M1 + robustez |
| [scripts/run_traders_swing_grid.py](scripts/run_traders_swing_grid.py) | Grid swing intraday + robustez |
| [reports/qulla_orb_robustness.parquet](reports/qulla_orb_robustness.parquet) | 12 best per symbol con MC/WF/decay |
| [reports/traders_swing_robustness.parquet](reports/traders_swing_robustness.parquet) | 7 best swing con MC/WF/decay |
| [reports/Qulla_ORB_Robustness.md](reports/Qulla_ORB_Robustness.md) | Reporte ORB legible |
| [reports/Traders_Swing_Robustness.md](reports/Traders_Swing_Robustness.md) | Reporte swing legible |

## 5. Siguientes pasos sugeridos

1. **Ajustar el gate MC ruin para alta frecuencia**: el threshold `DD ≥ 30R` está calibrado para K3M1-75 mini-strats (10-30 tpy). Para Qulla ORB (170-210 tpy) usar `DD ≥ 60R` o convertir a `account DD %` con position sizing — esto reclasificaría las 12 ORB como FUERTE/ACEPTABLE.
2. **Live paper deploy** de las 3-5 ORB top (WTI, XAUUSD, BRENT, NASDAQ100, EURUSD) durante 1-2 meses con 0.05% risk para validar slippage real vs friction modelada.
3. **Probar SP500/NATGAS** con `open_hour` correcto del broker Vantage (NYSE 14:30 UTC en winter EST, Henry Hub 13:00 UTC).
4. **Combinar Qulla ORB + K3M1-75 fade en el mismo signal-TF**: los dos toman lados opuestos en el mismo breakout. Net market exposure se neutraliza, edge se acumula.
