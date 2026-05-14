# KHA0SYS3 — MATH Bot (K3M1-75) + Traders Replication (2026-05-14)

Tres sistemas live en paralelo, aislados por magic number y manejo de
ordenes pero compartiendo cuenta MT5:

| Sistema | Magic | n strats | Filosofia | Risk/trade |
|---|---|---|---|---|
| **K3M1-75** | **1338** | 63 | Fade math momentum (INVERT) | 0.1% |
| **Traders Swing** | **1339** | 5 | LONG VCP/HTF (PDFs Minervini/Qulla) | 0.1% |
| **Traders ORB** | **1340** | 12 | LONG opening range breakout (PDF Qulla) | 0.1% |

Total: **80 estrategias activas, 0.1% per trade uniformes**. FADE (magic 1337)
permanece retirado.

## Architecture (post-cleanup)

```
domain/              constants, models, env loader (zero deps)
application/         indicators, math_indicators, signal_generator
engine/              k3_universe_m1_mgmt (discovery)
                     k3m1_robustness (validation)
                     run_math_momentum (signal detectors + STOP backtest)
                     run_indicator_discovery (helpers)
                     indicator_validation (compute_metrics)
                     friction_real (per-symbol Vantage friction)
execution/           live_math_trader (K3M1 engine, magic 1338)
                     math_order_manager (orders + telegram events)
                     mt5_client, risk_manager
                     bot_config_math.json (63 K3M1 strategies)
                     bot_config_traders_swing.json (5 swing, magic 1339)
                     bot_config_traders_orb.json (12 ORB, magic 1340)
monitoring/          telegram_notifier, telegram_bot (interactive cmds)
                     mt5_reporter, system_health
infrastructure/      polars_loader, symbol_mapper
```

## Live deploy: K3M1-75 (2026-05-12)

| Item | Valor |
|---|---|
| Strategies | **75** (59 FUERTE + 16 ACEPTABLE) |
| Robustness | MC 10k bootstrap + walk-forward 50/50 + decay yearly |
| Timeframes | M15: 34 · M1: 19 · H1: 14 · H4: 8 |
| Setups (5) | KALMAN_INNOV_EXPAND (20) · HURST_TREND_MOM (19) · VELOCITY_ACCEL_GO (16) · OLS_SLOPE_STRONG (10) · SPECTRAL_TREND_MOM (10) |
| Symbols (11) | XAUUSD · XAGUSD · BRENT · GBPUSD · WTI · GBPJPY · EURUSD · GBPAUD · USDJPY · AUDUSD · EURJPY |
| Sessions | NY: 29 · ALL_DAY/LONDON_NY: 15 c/u · ASIA: 10 · LONDON: 6 |
| Direction | 100% INVERT (fade-of-momentum) |
| Risk | **0.1% per trade** (unificado con Traders Swing+ORB, 2026-05-14) |
| Friction model | Realistic Vantage `friction_r(sym, sl, median_atr) + 0.2R` (0.24-0.51R per trade) |
| Avg WR | 74.8% |
| Avg PF IS | 2.86 |
| **Avg PF OOS** | **2.88** (sin overfit) |
| Avg MC ruin | 0.09% |
| Sum trades/yr | 11,928 |

### Pipeline de descubrimiento

1. **Phase A** (`src/engine/k3_universe_m1_mgmt.py`): grid 14 syms × 6 setups × 4 signal TFs × 5 sessions × 2 dirs × 4 TPs × 3 SLs = 40,320 combos. Para cada uno: detect signal, STOP fill walking M1, exit walking M1 minuto-a-minuto hasta TP/SL/MAX_HOLD. SL-first conservative en intra-bar ties.
2. **Phase B** (filter): PF≥1.2, WR>50%, exp_R≥0.05, tpy gates por TF (M1≥200, M15≥50, H1≥15, H4≥5). Dedup: best per (sym, setup, signal_tf, sess, dir).
3. **Realistic filter**: WR 55-90%, PF 1.5-10, exp_r≥0.1, tpy≥30 → 175 survivors.
4. **Session dedup**: best session per (sym, tf, setup, dir) → **75 strategies**.
5. **Robustness** (`src/engine/k3m1_robustness.py`): MC 10k bootstrap (ruin DD≥30R), walk-forward 50/50 (PF IS vs OOS), decay anual (slope WR). Clasificación FUERTE / ACEPTABLE / DEBIL / MUERTA.

### Bias fixes críticos aplicados

1. **Causal indicators**: todos los indicadores (atr_14, ols_slope_30, velocity_10, kalman_innovation, hurst_rs_100, spectral_ratio_64, kama_slope_10) son rolling causales — verificado.
2. **SL-first intra-bar**: cuando TP y SL se tocan en el mismo M1 bar, asumir SL primero (conservador).
3. **UTC timezone normalization**: helper `_to_us_utc()` para naive datetimes. Crítico para máquinas dev no-UTC — sin esto Python's `.timestamp()` interpreta como local, creando look-ahead vs Polars datetime[μs] cast-to-Int64 que usa UTC.
4. **MAX_HOLD = 10× signal_tf** minutos (M1: 10min, M15: 2.5h, H1: 10h, H4: 40h). Sin truncación a session_end_hour del mismo día (eso inflaba PF artificialmente al matar pérdidas).

### Multi-TF dispatch en live

| Signal TF | Boundary fire | Lookback |
|---|---|---|
| M1 | cada minuto | 800 bars |
| M15 | :00/:15/:30/:45 | 500 bars |
| H1 | HH:00 | 500 bars |
| H4 | 0/4/8/12/16/20 broker hour | 500 bars |

El engine procesa cada TF SOLO en su bar close. Tracker `_last_tf_processed` previene doble proceso.

### Mecánica de orden

- Signal: detected at TF bar close, dedup 1/día por (sym, setup_type)
- Entry: STOP order placed at `close ± 0.5×ATR` (FLIPPED direction porque INVERT)
- Fill wait: 5 × signal_tf minutos (5 H1 = 5h, 5 H4 = 20h, etc.) o `MATH_WAIT_BARS=5`
- TP: `entry ± tp_atr_mult × ATR`
- SL: `entry ∓ sl_atr_mult × ATR`
- Direction guard: si el indicador de la señal se debilita (|guard| < 0.5×|guard@placement|), cancela pendiente
- Max hold (timeout): el broker maneja TP/SL automáticamente; en backtest 10×signal_tf min
- SL Guardian (live): re-verifica cada 10s que MT5 cerró si precio cruzó SL

## Running

| Comando | Descripción |
|---|---|
| `python scripts/run_math_bot_supervisor.py --live` | Live bot entry point (NSSM) |
| `python scripts/run_math_bot_supervisor.py --dry-run` | DRY mode (no `order_send`) |
| `python -m src.engine.k3_universe_m1_mgmt` | Re-run Phase A+B discovery |
| `python -m src.engine.k3m1_robustness` | Re-run MC+WF+decay validation on dedup 75 |
| `python scripts/build_bot_config_k3m1_75.py` | Generate `bot_config_math.json` from parquet |
| `python deploy/pull_and_restart.py` | VPS pull + service restart |
| `python deploy/check_bot.py` | VPS health check |
| `python scripts/check_broker_time.py` | Verify MT5 broker time alignment |
| `python scripts/math_watchdog.py` | Local watchdog |

## Conventions

- **Polars vectorized** (no row loops); numpy for the M1 exit walk
- **Risk**: balance-based (no `free_margin`), tier único 0.5%
- **Dedup**: 1 trade per `(symbol, setup_type)` per day
- **Direction**: 100% INVERT — math momentum signals are FADED
- **MT5 order comment**: `M|<TF>|<setup_tag>|<session_tag>` (unified via `make_order_comment`)
- **Strategy id**: `<sym>_<tf>_<setup>_<session>_<dir>` (e.g. `XAGUSD_H1_OLS_ASIA_INV`)
- **Magic numbers in `src/domain/constants.py`**
- **Secrets in `.env`**: `config/broker.yaml` and `config/telegram.yaml` are gitignored

## Telegram

Token & chat configured in `.env`. Interactive command bot scoped to magic=1338:

- `/status` · `/balance` · `/pnl` · `/positions` · `/orders` · `/health` · `/stop` · `/resume`

Structured multi-line events (no emojis):

| Event | Trigger |
|---|---|
| `ENGINE STARTED [K3M1-75]` | Bot startup: shows robustness count, TF mix, avg WR/PF IS/OOS |
| `HEARTBEAT` | Each 15 min: account snapshot, per-TF setup count |
| `ORDER PLACED [FUERTE/ACEPTABLE]` | New STOP placed: includes ID, TF, R:R, PF OOS |
| `LIVE FILL` | MT5 detected STOP→position transition |
| `LIVE CLOSE` | Position closed (TP/SL/STOPOUT/manual) + R-multiple |
| `GUARD CANCEL` | Direction guard weakened, pending cancelled |
| `SL GUARDIAN CLOSE` | Price crossed SL without broker close |
| `SESSION-END TIME-STOP` | Position outside session window |
| `STALE SWEEP` | STOP idle > 90min cancelled |
| Retcodes | 10015/10016/10022/10027/10030 with skip semantics |

## Friction model

`src/engine/friction_real.py` keeps a per-symbol Vantage snapshot
(spread_pt, tick_size, tick_value, vol_min, commission_rt_usd). Converted
to R-units via:

```
risk_usd       = sl_atr_mult × median_atr × (tick_value / tick_size) × vol_min
friction_R     = total_friction_usd / risk_usd
friction_effective = friction_R + 0.2R  (slippage budget)
```

Resulting effective friction per trade (SL=0.5×ATR):

| Symbol | Friction |
|---|---|
| XAGUSD/XAUUSD | 0.24-0.27 R |
| GBPUSD/AUDUSD/GBPAUD | 0.35-0.37 R |
| GBPJPY/EURJPY | 0.38-0.45 R |
| EURUSD/USDJPY | 0.43-0.51 R |

## VPS deploy

- Windows Server via WinRM (`deploy/vps_connection.py`)
- Services (NSSM): **Kha0sysMathBot** (live K3M1-75) + Kha0sysWatchdog3 (monitoreo)
- Logs en `C:\ProgramData\Kha0sysMath\logs\math_bot.log`
- Servidor MT5: VantageInternational-Demo, login 25246666
- Server time offset: +3h (EEST) — engine auto-corrects via `_refresh_server_offset_if_stale` cuando hay tick fresco

## Reports + artifacts

- `reports/K3M1_Dedup75_Robustness.md` — clasificación final per-estrategia
- `reports/k3m1_dedup75_robustness.parquet` — fuente de verdad para `build_bot_config_k3m1_75.py`
- `reports/k3m1_phase_a.parquet` — Phase A raw (36,816 survivors)
- `reports/k3m1_phase_b.parquet` — Phase B filtered (845 unique)
- `reports/k3m1_realistic_survivors.parquet` — 175 realistic
- `reports/k3m1_dedup_best_session.parquet` — 75 dedup pre-robustness

## Traders Replication (Tier 1 Swing + Tier 2 ORB, 2026-05-14)

Replica geometrica de los PDFs Minervini/Zanger/Qullamaggie/Ryan adaptada a
FX/commodities/indices. Backtest 2018-2026, friction Vantage real + 0.2R
slippage. **Risk unificado 0.1% per trade** alineado con K3M1-75.

### Tier 1: Traders Swing (magic 1339, 5 estrategias)

D1 setup detection + M1 intraday breakout entry + walker M1 con exit per trader.
Nomenclatura `TS_<SYM>_<SETUP>_<VARIANTE>`.

| ID | Variant | Setup exit (SL / Partials / Trail / Max) | PF IS | PF OOS |
|---|---|---|---|---|
| TS_XAGUSD_QULLAHTF_PDF | PDF-strict | 1×ATR / 30%d3 + 20%d5 / SMA50 / 40d | 2.30 | 2.08 |
| TS_XAUUSD_MINERVINI_VCP_PDF | PDF-strict | 7.5% / 25%@2R + 25%@4R / SMA10 / 60d | 2.24 | 6.83 |
| TS_XAUUSD_QULLAHTF_GRID | Grid | 1×ATR / 30%@1.5R + 30%@3R / – / 15d | 1.72 | 2.64 |
| TS_XAGUSD_MINERVINI_VCP_GRID | Grid | 1.5×ATR / 30%@1.5R + 30%@3R / SMA50 / 30d | 1.47 | 1.80 |
| TS_BRENT_MINERVINI_VCP_GRID | Grid | 1×ATR / 30%@1R + 30%@2R / SMA50 / 30d | 1.57 | 1.96 |

### Tier 2: Traders ORB (magic 1340, 12 estrategias)

Opening range breakout intradia: rango = primeros 15-30 min desde open_hour,
entrada en primer M1.close > range_high con bar_range >= 0.5×ATR_M1.
Nomenclatura `TO_<SYM>_<OH>h_<RM>m`.

| ID | open_hour UTC | range_min | sl_atr | partial_R | max_h | PF IS | PF OOS |
|---|---|---|---|---|---|---|---|
| TO_WTI_13h_15m | 13 | 15 | 0.5 | 3.0 | 4 | 2.79 | 2.24 |
| TO_GBPJPY_07h_30m | 7 | 30 | 0.5 | 2.0 | 8 | 2.75 | 2.64 |
| TO_BRENT_13h_30m | 13 | 30 | 0.5 | 3.0 | 4 | 2.72 | 2.34 |
| TO_XAUUSD_07h_30m | 7 | 30 | 0.5 | 3.0 | 4 | 2.70 | 2.96 |
| TO_GBPUSD_07h_15m | 7 | 15 | 0.5 | 2.0 | 8 | 2.67 | 2.43 |
| TO_EURUSD_13h_15m | 13 | 15 | 0.5 | 3.0 | 8 | 2.41 | 2.64 |
| TO_NASDAQ100_13h_30m | 13 | 30 | 0.5 | 3.0 | 8 | 2.33 | 2.05 |
| TO_GBPAUD_07h_30m | 7 | 30 | 0.5 | 2.0 | 8 | 2.38 | 2.67 |
| TO_XAGUSD_13h_30m | 13 | 30 | 0.5 | 2.0 | 4 | 2.28 | 2.22 |
| TO_USDJPY_07h_15m | 7 | 15 | 0.5 | 3.0 | 8 | 2.28 | 1.62 |
| TO_AUDUSD_13h_30m | 13 | 30 | 0.5 | 3.0 | 8 | 2.26 | 2.58 |
| TO_EURJPY_07h_15m | 7 | 15 | 0.5 | 2.0 | 8 | 2.08 | 2.09 |

**Convenciones FX vs commodities/indices**:
- FX major (EURUSD/GBPUSD/USDJPY/AUDUSD/GBPJPY/EURJPY/GBPAUD) → `open_hour=7` (London)
- Metales/commodities/indices (XAUUSD/XAGUSD/WTI/BRENT/NASDAQ100) → `open_hour=13` (NY)

### Source code

| Modulo | Proposito |
|---|---|
| `src/engine/traders_setups.py` | Detectores ORB M1 + setups D1 genericos |
| `src/engine/traders_swing.py` | Setups D1 FX-calibrated + scanner intraday M1 breakout |
| `src/engine/traders_backtest.py` | Walker M1 vectorizado + ExitRules por trader |
| `scripts/run_qulla_orb_grid.py` | Grid + robustez ORB |
| `scripts/run_traders_swing_grid.py` | Grid + robustez swing |
| `scripts/run_traders_pdf_strict.py` | Variante PDF-strict (reglas literales del PDF) |
| `scripts/build_bot_config_traders.py` | Genera bot_config_traders_swing.json + bot_config_traders_orb.json |

### Setups que NO se desplegaron (fallo en FX)

- **Zanger Flag/Pennant + Cup&Handle**: PF 0.07 PDF-strict, requiere acumulacion Stage 2 stock-style.
- **Qulla Episodic Pivot (gap up)**: FX 24/7 no genera gaps >=1%.
- **Ryan Ants**: solo dispara en bull markets paraboliccos. 16 trades 8 anos XAUUSD.

### Reports asociados

- `reports/Traders_Final_vs_K3M1.md` — primer comparativo
- `reports/Traders_Comparison_Final.md` — comparativo grid vs PDF-strict
- `reports/Qulla_ORB_Robustness.md` — detalle 12 ORB
- `reports/Traders_Swing_Robustness.md` — detalle 7 swing grid
- `reports/Traders_PDF_Strict.md` — detalle PDF-strict
- `reports/qulla_orb_robustness.parquet` — fuente verdad ORB
- `reports/traders_swing_robustness.parquet` — fuente verdad swing grid
- `reports/traders_pdf_strict.parquet` — fuente verdad PDF-strict
