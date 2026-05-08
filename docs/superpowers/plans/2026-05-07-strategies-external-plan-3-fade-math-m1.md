# Plan 3 — Re-evaluar bot FADE/MATH con M1 polars

**Goal:** evaluar las estrategias del bot live (FADE en `bot_config.json` y MATH en `bot_config_math.json`) con tracking M1 polars vectorizado, sobre los activos para los que tenemos M1 (XAUUSD, XAGUSD, SP500, NASDAQ100, EURUSD, USDJPY, GBPAUD). Comparar contra las métricas esperadas/live para detectar drift backtest-vs-live.

**Tech stack:** reusa la infra de `src/strategies_external/` (Plan 1+2+2.5 mergeada). Importa lectura de `src/application/calculators.py` (DataEnricher).

**Out of scope:**
- NO modificar `src/execution/`, `src/domain/`, `bot_config*.json`.
- NO promoción a live; solo research.

---

## Activos overlap (M1 disponible)

| Symbol | M1 disp | en bot FADE | en bot MATH |
|--------|--------|-------------|-------------|
| XAUUSD | ✅ | ✅ (algunas) | ✅ (3) |
| XAGUSD | ✅ | ✅ | ✅ (10) |
| SP500 | ✅ | maybe (depend cfg) | ❌ |
| NASDAQ100 | ✅ | maybe | ❌ |
| EURUSD | ✅ | ✅ | ✅ (2) |
| USDJPY | ✅ | ✅ | ✅ (3) |
| GBPAUD | ✅ | ✅ | ✅ (3) |
| AUDUSD | ❌ M1 | — en config | ✅ (3) |
| EURJPY | ❌ M1 | — en config | ✅ (3) |
| GBPJPY | ❌ M1 | — en config | ✅ (6) |
| GBPUSD | ❌ M1 | — en config | — |

Filtramos a los 7 con M1 disponible.

---

## Bloques

### Bloque A — FADE adapter + runner

**A1: FADEStrategy adapter**
- File: `src/strategies_external/strategies/fade_adapter.py`
- Lee `bot_config.json`, filtra por enabled=True y sym ∈ overlap.
- Por cada strategy: agrupa por (sym, magic_time, duration). Reusa `DataEnricher.enrich_with_opening_range` y filtros del backtester actual.
- Emite Signal objects con setup_ts = post-OR-close, entry_type="limit", entry_price = OR_HIGH (FADE_UP) o OR_LOW (FADE_DOWN), valid_until = setup + duration*5 minutos (más allá no tiene sentido), indicator_anchors con tp_mult, sl_mult, OR_WIDTH, OR_HIGH, OR_LOW.

**A2: FADEExitManager** (en `exit_managers.py`):
- DocExitManager._fade(s): stop = entry ± sl_mult*OR_WIDTH, tp1 = entry ± tp_mult*OR_WIDTH (sentido del FADE).
- Direction guard: si OR_LOW se rompe primero (FADE_UP), cancelar (Signal expira sin fill).
- IndicatorExitManager._fade: idéntico al doc en V1.

**A3: run_fade runner**
- `src/strategies_external/runners/run_fade.py`
- Itera bot_config, agrupa por combo, genera signals, procesa con M1 tracking.
- Compara métricas (n, wr, pf, expectancy, dd_R, calmar) contra `expected_*` (si están en config) para detectar drift.

### Bloque B — MATH adapter + runner

**B1: MATHStrategy adapter**
- File: `src/strategies_external/strategies/math_adapter.py`
- Lee `bot_config_math.json`. Por cada entry (setup_type, atr_period, sl_atr_mult, tp_atr_mult, regime, direction_mode, session, sym, tf).
- Setup_type: KALMAN_INNOV_EXPAND, OLS_SLOPE_STRONG, HURST_TREND_MOM, SPECTRAL_TREND_MOM, GARCH_Z_FADE.
- direction_mode = INVERT → flipped: signal contraria al setup natural.
- TF = M15/H1/H4. Multi-TF dispatch.

**B2: MATHExitManager**:
- DocExitManager._math(s): stop = entry ± sl_atr_mult*ATR, tp1 = entry ± tp_atr_mult*ATR.
- 5-bar wait: entry NO se llena hasta 5 bars después del setup_ts (cancela si breakea contra antes).

**B3: run_math runner**
- `src/strategies_external/runners/run_math.py`
- Itera bot_config_math, agrupa por (setup_type, sym, tf), genera signals, procesa con M1 tracking.
- Compara contra expected_pf, expected_wr de cada entry.

### Bloque C — Comparativo

**C1: run_bot_live_comparison.py**
- Corre A3 + B3, compila tabla comparativa: live expected vs M1 backtest.
- Output: `reports/external/bot_live_m1_comparison.md`

---

## Implementación pragmática (auto mode)

Dado el alcance grande, voy a **empezar solo con FADE** (Bloque A) y reportar resultados antes de MATH. Si FADE muestra drift significativo, MATH se vuelve más urgente. Si FADE coincide razonablemente con live, MATH puede esperar.

Bloque A entregable: standalone `python -m src.strategies_external.runners.run_fade` produciendo `reports/external/fade_m1_backtest.md` con métricas por strategy (live vs M1 backtest).
