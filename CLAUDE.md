# KHA0SYS3 — MATH Bot (K3M1-75)

Sole live trading system. **Magic 1338**. FADE bot (magic 1337) was retired
during the K3M1-75 cleanup; all legacy discovery / FADE engines, indicator
scanners, agent worktrees, and old portfolio backups were removed from the
repo to leave only what the live bot + its discovery pipeline need.

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
execution/           live_math_trader (engine)
                     math_order_manager (orders + telegram events)
                     mt5_client, risk_manager
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
| Risk | 0.5% fijo por trade |
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
