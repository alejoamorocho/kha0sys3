# Strategies External — Backtest Research Module

**Fecha:** 2026-05-06
**Autor:** Alejo Amorocho (con asistencia Claude Opus 4.7)
**Estado:** Diseño aprobado — pendiente de plan de implementación
**Source de las estrategias:** `outputs/estrategias_detalladas_testeables.md` v1.0 (2026-05-04)

## 1. Objetivo

Investigar y backtestear cinco estrategias externas al stack actual KHA0SYS3 (FADE/MATH/SHAKEOUT) sobre los datos del proyecto para decidir cuáles merecen pasar a forward demo y eventual integración live como bot independiente.

**Estrategias a evaluar:**

| # | Nombre | TF señal | Activos elegidos |
|---|--------|---------|-------------------|
| 2 | Rosputnia SMA-18 | Daily | XAUUSD, XAGUSD, WTI, BRENT, NATGAS |
| 3 | Rosputnia Doble Suelo | Daily + H4 | XAUUSD, XAGUSD, SP500, NASDAQ100, WTI |
| 4 | Larry Williams OOPS | Daily | SP500, NASDAQ100 |
| 5 | Pau Perdices Fib pullback | M5 (ctx H1/H4) | XAUUSD, XAGUSD |
| 6 | InsiderWeek COT-1 | Daily + COT semanal | SP500, NASDAQ100, WTI, BRENT, NATGAS, XAUUSD, XAGUSD |

**Estrategia descartada:** #1 Denisenko Volume Profile / Order Flow — requiere datos L2/footprint propietarios fuera del alcance.

**Out of scope (por ahora):**

- Cualquier integración con el bot live (`src/execution/`).
- Cualquier modificación a `src/domain/`, `bot_config.json`, `bot_config_math.json`.
- Forward demo, paper trading, conexión MT5.
- Promoción a archetype del bot live (eso será una decisión post-resultados).

## 2. Principios de diseño

1. **Aislamiento del bot live.** Todo el código nuevo vive en `src/strategies_external/` y `src/strategies_external/runners/`. No tocamos `src/execution/`, `src/engine/`, `src/domain/` ni los configs del bot.
2. **Polars vectorizado.** El módulo procesa señales daily pero hace seguimiento intra-bar sobre M1 (cuando esté disponible) o el TF más fino que exista. Polars es obligatorio para mantener tiempos de backtest aceptables (un walk-forward sobre 8 años × 5 estrategias × 7 activos × M1 sin polars sería inviable).
3. **Comparabilidad con el sistema actual.** Las métricas reportadas y los costes (friction 0.1R FX / 0.2R commodities-índices, riesgo 0.5%/trade) son los mismos que ya usa `src/engine/run_portfolio_backtest_rr.py`. Eso permite comparar las estrategias externas con las 108 FADE y las 34 MATH en condiciones equivalentes.
4. **Gestión de salida explorada, no asumida.** El documento fuente describe gestiones heterogéneas y no validadas. Para cada estrategia probamos tres modos de salida (`doc`, `atr`, `indicator`) y reportamos cuál gana. Sin esto, las métricas serían un artefacto de la gestión copy-paste del documento.
5. **Reproducibilidad.** Cada run guarda configuración + seed + commit hash. Los reportes incluyen los parámetros usados.

## 3. Arquitectura

### 3.1 Layout de archivos

```
src/strategies_external/
├── __init__.py
├── constants.py                 # Constantes locales del módulo
├── data_loader.py               # CSV → polars; aggregate_to_daily, aggregate_to_4h
├── exit_managers.py             # DocExitManager, ATRExitManager, IndicatorExitManager
├── common/
│   ├── __init__.py
│   ├── trade.py                 # Dataclass Trade
│   ├── signal.py                # Dataclass Signal (output de estrategia)
│   ├── backtester.py            # Loop genérico daily-signal + M1-tracking
│   ├── metrics.py               # WR, PF, expectancy_R, DD, CAGR, Sharpe, Calmar...
│   ├── walk_forward.py          # Rolling 5 ventanas 70/30
│   └── monte_carlo.py           # Bootstrap 10k de trades
├── strategies/
│   ├── __init__.py
│   ├── base.py                  # Strategy ABC: generate_signals(df) -> list[Signal]
│   ├── oops.py                  # #4
│   ├── sma18.py                 # #2
│   ├── double_bottom.py         # #3
│   ├── perdices_fib.py          # #5 (versión H1 hasta llegar M5)
│   └── cot1.py                  # #6
├── data_sources/
│   ├── __init__.py
│   ├── cot_downloader.py        # Descarga COT semanal de cftc.gov
│   └── seasonality.py           # Estacionalidad histórica por (mes, día)
└── runners/
    ├── __init__.py
    ├── run_oops.py
    ├── run_sma18.py
    ├── run_double_bottom.py
    ├── run_perdices.py
    ├── run_cot1.py
    └── run_all.py               # Orquestador + reporte comparativo
```

Reportes:

```
reports/external/
├── <strategy>_backtest.md
├── <strategy>_trades.parquet
├── <strategy>_equity.parquet
├── <strategy>_walkforward.md
├── <strategy>_montecarlo.md
└── all_external_comparison.md
```

### 3.2 Flujo end-to-end

```
data/SYMBOL_TF.csv (M15/H1/H4)              data/cot/{year}.parquet
data/M5/SYMBOL.csv  (cuando llegue)         (descargado por cot_downloader)
data/M1/SYMBOL.csv  (cuando llegue)
        │                                            │
        ▼                                            ▼
data_loader.load_csv(symbol, tf)            data_sources.cot/seasonality
        │                                            │
        ├── aggregate_to_daily(df_h1)                │
        │                                            │
        ▼                                            │
strategy.generate_signals(df_daily, cot, seasonality) → list[Signal]
        │
        ▼
exit_manager.attach_levels(signals, df_daily) → Signal con stop/tp1/tp2 según modo
        │
        ▼
backtester.run(signals, df_tracking_tf) → list[Trade]
        │   (df_tracking_tf = M1 si existe, sino M5, sino M15)
        │
        ▼
metrics.evaluate(trades) → métricas
walk_forward.run(...) → métricas IS/OOS por ventana
monte_carlo.run(...) → ruina, DD quantiles
        │
        ▼
report_writer → reports/external/*.md + *.parquet
```

### 3.3 Componentes compartidos

#### `data_loader.py`

```python
def load_csv(symbol: str, tf: str) -> pl.DataFrame:
    """Carga data/{symbol}_{tf}_*.csv como polars con timestamp tipado."""

def load_m1(symbol: str) -> pl.DataFrame | None:
    """Carga data/M1/{symbol}.csv si existe, None si no."""

def load_m5(symbol: str) -> pl.DataFrame | None:
    """Carga data/M5/{symbol}.csv si existe, None si no."""

def aggregate_to_daily(df: pl.DataFrame) -> pl.DataFrame:
    """Resamplea a daily desde H1 (preferido) o desde el TF más fino disponible.
    OHLC: first/max/min/last. Volume: sum. Index: fecha (start-of-day broker time).
    """

def best_tracking_tf(symbol: str) -> tuple[str, pl.DataFrame]:
    """Devuelve (tf_label, df) eligiendo M1 > M5 > M15."""
```

#### `common/signal.py`

```python
@dataclass(frozen=True)
class Signal:
    symbol: str
    strategy: str
    side: Literal["long", "short"]
    setup_ts: pl.Datetime          # bar de la barra que disparó la señal (daily)
    entry_type: Literal["market", "stop", "limit"]
    entry_price: float
    valid_until: pl.Datetime       # cuándo expira si no se llena (default: fin del próximo daily)
    stop: float
    tp1: float | None
    tp2: float | None
    tp1_size_pct: float = 0.5      # cuánto cierra en TP1
    timestop_bars: int | None = None  # en barras del tracking_tf
    indicator_anchors: dict[str, float] = field(default_factory=dict)
    # ej. {"sma18": 1234.5, "neckline": 1250.1}; usado por IndicatorExitManager
```

#### `common/trade.py`

```python
@dataclass(frozen=True)
class Trade:
    symbol: str
    strategy: str
    exit_mode: Literal["doc", "atr", "indicator"]
    side: Literal["long", "short"]
    entry_ts: pl.Datetime
    entry: float
    stop: float
    tp1: float | None
    tp2: float | None
    exit_ts: pl.Datetime
    exit: float
    exit_reason: Literal["tp1", "tp2", "stop", "timestop", "signal_inverso", "eod"]
    R: float                      # |entry - stop|
    pnl_R: float                  # PnL en múltiplos de R, después de friction
    pnl_pct: float                # PnL en % del capital asumiendo riesgo 0.5%
    bars_in_trade: int
```

#### `common/backtester.py`

Loop genérico. Pseudocódigo:

```
for signal in signals:
    df_track = tracking_df.filter(ts >= signal.setup_ts.next_bar() & ts <= signal.valid_until + max_holding)
    estado = "esperando_fill"
    for bar in df_track.iter_rows():
        if estado == "esperando_fill":
            if cumple condición de fill (stop/limit/market):
                fill_price = ajustar por slippage (1 tick adverso futuros, 0.5pip FX)
                estado = "abierto"; continuar
            elif bar.ts > signal.valid_until:
                break  # expirado, sin trade
        elif estado == "abierto":
            # Resolución intra-bar conservadora: si la barra toca stop y tp en la misma vela, gana stop.
            if toca stop → cerrar stop (Trade.exit_reason="stop")
            elif toca tp2 → cerrar tp2
            elif toca tp1 y no se ha tomado parcial → marcar parcial, mover stop a BE si exit_manager lo dicta
            elif señal_inversa (en estrategias que la usan como salida) → cerrar
            elif timestop alcanzado → cerrar
            elif eod (estrategias intradía como #4 OOPS modo conservador) → cerrar
        ...
    aplicar friction 0.1R/0.2R según asset_class
    crear Trade
```

Friction y position sizing copiados de `src/domain/constants.py`:

```python
FRICTION_R_FOREX = 0.1
FRICTION_R_COMMODITY_INDEX = 0.2
RISK_PER_TRADE_PCT = 0.005  # 0.5% (parametrizable por runner)
```

#### `common/metrics.py`

Devuelve dict con: `n_trades, win_rate, profit_factor, expectancy_R, avg_win_R, avg_loss_R, max_dd_R, max_dd_pct, cagr_pct, sharpe, sortino, calmar, time_in_market_pct, R_distribution_quantiles`.

#### `common/walk_forward.py`

5 ventanas rolling, split 70% IS / 30% OOS por ventana. Reporta tabla IS vs OOS, y banderazo "consistente" si OOS PF > 1.0 y OOS WR no se desploma >30% vs IS.

#### `common/monte_carlo.py`

Bootstrap de 10k secuencias re-ordenando los trades observados; reporta `prob_ruin (DD < -50%)`, `dd_q5/q50/q95`, `final_equity_q5/q50/q95`. Usa el mismo enfoque que `src/engine/run_robustness_test.py`.

### 3.4 ExitManagers

Tres implementaciones, todas con la misma firma:

```python
class ExitManager(ABC):
    name: ClassVar[Literal["doc", "atr", "indicator"]]
    @abstractmethod
    def attach_levels(self, signal_raw: SignalRaw, df: pl.DataFrame) -> Signal: ...
```

Donde `SignalRaw` es lo que la estrategia produce sin gestión (ts, side, entry_price, indicator_anchors).

#### `DocExitManager`

Aplica las reglas de salida tal como las describe el documento por estrategia. Es la **referencia base** para no perder de vista lo que dice la fuente.

| Estrategia | Stop | TP1 | TP2 | Time stop |
|------------|------|-----|-----|-----------|
| OOPS | Extremo del día (long: low, short: high) | 2R o EOD | — | EOD |
| SMA-18 | 2 cierres consecutivos contra SMA18 | dejar correr | dejar correr | — |
| Doble Suelo | Low de consolidación | Fib 100% | Fib 161.8% | 20 barras |
| Perdices | Swing low (long) | Swing high anterior | Ext Fib 127.2% / 161.8% | 4 horas |
| COT-1 | Otro lado del patrón + 0.5×ATR | 1.5R | 3R | 5 días |

#### `ATRExitManager(sl_mult, tp1_mult, tp2_mult, atr_window=14)`

Estandariza: stop = entry ± sl_mult × ATR, TP1 = entry ± tp1_mult × ATR, TP2 = entry ± tp2_mult × ATR. Sweep en runner: `sl_mult ∈ {1.0, 1.5, 2.0, 2.5}`, `tp1_mult ∈ {1.0, 1.5, 2.0}`, `tp2_mult ∈ {2.0, 3.0, 4.0}` con restricción `tp1 < tp2`.

#### `IndicatorExitManager`

Ancla stops/TPs a indicadores estructurales de la propia estrategia, leyendo `signal.indicator_anchors`:

| Estrategia | Stop ancla | TP1 ancla | TP2 ancla |
|------------|------------|-----------|-----------|
| OOPS | Extremo del día (mismo doc) | Mid-rango de la barra previa | Cierre rango previo + 1×rango |
| SMA-18 | SMA18 - 0.5×ATR (long) | SMA18 + 2×ATR | SMA18 + 4×ATR |
| Doble Suelo | L2 - 0.25×altura patrón | Neckline + 1×altura | Neckline + 1.618×altura |
| Perdices | Swing low - 2 pips | Swing high reciente | Ext Fib 161.8% del swing |
| COT-1 | Low/high reciente 5d - 0.5×ATR | Media histórica estacional 5d | Media histórica estacional 10d |

Los anchors los rellena la estrategia al crear la señal. Si una ancla falta para un trade, el manager hace fallback a ATR equivalente y registra el caso para diagnóstico.

#### Cómo se eligen los modos en el reporte

Cada runner corre las 3 variantes y la reporta en una tabla comparativa. La estrategia "winner" es la que maximiza `Calmar OOS` con `prob_ruin ≤ 1%` y `n_trades ≥ 30` por activo.

## 4. Especificación por estrategia

### 4.1 #4 OOPS (Larry Williams)

**Activos:** SP500, NASDAQ100. **TF señal:** daily Vantage (agregado desde H1). **Tracking TF:** M1 si existe, M5 fallback, M15 fallback.

**Caveat declarado:** el documento sugiere "open RTH 09:30 NY" pero los CSVs son broker Vantage 24h. La señal usa el daily Vantage. Cuando llegue M1 de Dukascopy puedo recortar a RTH NY como variante adicional.

**Reglas:**

- Long: `open[t] < low[t-1]` y durante el día `high[t] > low[t-1]`. Buy stop a `low[t-1] + 1 tick` válido sólo durante el día t.
- Short simétrico.

**Anchors para Indicator/ATR:** prev_high, prev_low, prev_range, today_open, ATR14.

**Sweep:** ninguno en la entrada (regla determinista). Solo sweep en exits.

### 4.2 #2 SMA-18

**Activos:** XAUUSD, XAGUSD, WTI, BRENT, NATGAS. **TF señal:** daily. **Tracking TF:** M1>M5>M15.

**Reglas:**

- Long: `low[t-1] > SMA18[t-1]` ∧ `low[t-2] > SMA18[t-2]` ∧ ninguna de las dos es inside-day. Buy stop a `max(high[t-1], high[t-2]) + 1 tick`.
- Short simétrico.

**Anchors:** SMA18, ATR14.

**Sweep entrada:** `SMA_window ∈ {14, 18, 22}` (±20% según el documento). **Pirámide:** off en V1; flag para futuro.

### 4.3 #3 Doble Suelo cualificado

**Activos:** XAUUSD, XAGUSD, SP500, NASDAQ100, WTI. **TF señal:** daily y H4 como variantes. **Tracking TF:** M1>M5>M15.

**Reglas:**

- Detector de swings con `scipy.signal.find_peaks` parametrizado: `prominence ≥ 0.5×ATR(14)`, `distance ≥ 5 barras`.
- Identificar L2 = mínimo más reciente. Buscar L1 dentro de [L2-80, L2-15] barras tal que `|L1 - L2| / L2 ≤ tolerancia`.
- Neckline = max(high) entre L1 y L2.
- Filtro 1: `close > SMA18` al momento del trigger.
- Filtro 2: ruptura del neckline con cierre por encima.
- Filtro 3: consolidación de 3-5 barras con rango total < 1×ATR(14) sobre el neckline.
- Trigger: buy stop a `max(high) de la consolidación + 1 tick`.

**Anchors:** L1, L2, neckline, altura_patron = neckline - L2, SMA18, ATR14.

**Sweep entrada:** `tolerancia ∈ {0.015, 0.02, 0.025}`, `consol_min_bars ∈ {3, 5}`, `consol_max_atr_mult ∈ {1.0, 1.5}`.

**Riesgo conocido:** la formalización de swings con find_peaks puede diferir de cómo lo marcaría un humano. Se documenta la discrepancia mostrando los patrones detectados sobre 20 ejemplos visuales.

### 4.4 #5 Pau Perdices Fib *(versión H1 placeholder hasta llegar M5)*

**Activos:** XAUUSD, XAGUSD. **TF señal V1:** H1. **TF señal V2 (cuando llegue M5):** M5. **Tracking TF:** M1>M5>M15.

**Reglas:**

- Contexto en H4: `EMA50 > EMA200` ∧ pendiente EMA50 positiva (regresión lineal sobre 10 barras H4 con coeficiente > 0) ∧ estructura HH/HL detectada con `find_peaks` sobre las últimas 50 barras H4 (mínimo 2 highs y 2 lows en la dirección).
- En el TF señal, identificar último impulso (swing low → swing high de las últimas 50 barras del TF señal).
- Entrada zona Fib 38.2-50% del impulso ∧ `RSI(14) < 40` girando al alza (último valor > anterior) ∧ vela alcista de confirmación (`close > open` y `close > prev_close`).
- Short simétrico.

**Anchors:** swing_high, swing_low, fib_382, fib_50, fib_127, fib_1618, RSI14.

**Sweep entrada:** `RSI_threshold ∈ {35, 40, 45}`, `fib_zone_lower ∈ {0.382, 0.5}`, `fib_zone_upper ∈ {0.5, 0.618}`.

**Plan de upgrade a M5:** cuando llegue `data/M5/XAUUSD.csv` y `data/M5/XAGUSD.csv`, sustituir TF de señal en el runner. La lógica no cambia.

### 4.5 #6 InsiderWeek COT-1 *(esperando M1 de índices Dukascopy)*

**Activos:** SP500, NASDAQ100, WTI, BRENT, NATGAS, XAUUSD, XAGUSD. **TF señal:** daily. **Tracking TF:** M1>M5>M15.

**Mapeo activo CFD ↔ contrato CFTC para COT:**

| CFD Vantage | Futuros CFTC | COT report |
|-------------|--------------|-------------|
| XAUUSD | GC (COMEX Gold) | Disaggregated COT, Producer/Merchant net |
| XAGUSD | SI (COMEX Silver) | Disaggregated, Producer/Merchant net |
| WTI | CL (NYMEX Crude) | Disaggregated, Producer/Merchant net |
| BRENT | BZ (ICE Brent Last Day) | Disaggregated si disponible; **fallback Legacy COT Commercials net** si CFTC no publica Disaggregated para BZ |
| NATGAS | NG (NYMEX NatGas) | Disaggregated, Producer/Merchant net |
| SP500 | ES (CME E-mini) | Financial COT, Asset Manager net |
| NASDAQ100 | NQ (CME E-mini) | Financial COT, Asset Manager net |

> **Nota:** para índices financieros, "Commercials" no aplica directamente — usamos Asset Manager net como proxy del smart money institucional.

**Reglas:**

1. Cada viernes ~15:30 CET: descargar último COT, calcular `COT Index Commercials (26w)`. Aplicar **lag de 3 días** (la publicación del viernes reporta posiciones del martes anterior).
2. Sesgo semanal: `cot_index > 80` → bias long; `< 20` → bias short.
3. Filtro estacional: retorno medio histórico (15 años, mismo día del año) en la dirección del bias > umbral.
4. Trigger price action diario **en la dirección del bias**:
   - Pin bar: `|close - open| / (high - low) < 0.3` ∧ wick en dirección contraria al cierre del trade > 50% del rango total. Para long: long lower wick (`min(open,close) - low`) > 0.5×(high-low). Para short: long upper wick simétrica.
   - Inside-day breakout: barra t es inside-day respecto a t-1, y barra t+1 rompe el high (long) / low (short) de t en la dirección del bias.
   - Doble suelo/techo en daily reusando detector de la §4.3.

**Anchors:** ATR14, swing_low_5d, swing_high_5d, season_mean_return_5d.

**Sweep:** `cot_window ∈ {26, 52}`, `cot_threshold ∈ {(70,30), (80,20), (85,15)}`, `seasonal_min_threshold ∈ {0%, 0.5%, 1%}`.

#### Descarga del COT

`data_sources/cot_downloader.py`:

```python
def download_cot(year: int) -> pl.DataFrame:
    """Descarga deacot{YY}.zip de cftc.gov, parsea, guarda en data/cot/{year}.parquet."""

def cot_index(net_positions: pl.Series, window: int) -> pl.Series:
    """COT Index = 100 * (net - rolling_min) / (rolling_max - rolling_min)"""
```

#### Estacionalidad

`data_sources/seasonality.py`:

```python
def seasonal_mean_return(df_daily: pl.DataFrame, window_days: int) -> pl.DataFrame:
    """Retorno medio histórico por (mes, día) sobre los últimos N años, excluyendo el año actual."""
```

## 5. Validación

Para cada estrategia × cada modo de exit:

1. **Backtest full** (2018-01-01 → today, datos disponibles).
2. **Walk-forward**: 5 ventanas, 70/30. Reporta tabla IS/OOS con `WR, PF, Sharpe, max_DD_R`.
3. **Sweep ±20%** sobre parámetros principales documentados arriba.
4. **Monte Carlo** 10k bootstrap → prob_ruin (DD<-50%), dd quantiles, final equity quantiles.
5. **Per-asset breakdown**: tabla con métricas por símbolo. Estrategia se reporta por activo, no agregada.
6. **Régimen breakdown**: split por volatilidad (ATR percentile) y por tendencia (close vs SMA200) para diagnóstico.

### Criterios Go / No-Go (semáforo)

| Métrica | Verde | Amarillo | Rojo |
|---------|-------|----------|------|
| PF OOS (walk-forward) | ≥ 1.5 | 1.2-1.5 | < 1.2 |
| Win rate consistencia IS vs OOS | drop < 15% | 15-30% | > 30% |
| MC prob_ruin | ≤ 1% | 1-5% | > 5% |
| n_trades_OOS por activo | ≥ 30 | 15-30 | < 15 |
| Max DD R | ≤ 8R | 8-15R | > 15R |
| Calmar | ≥ 1.0 | 0.5-1.0 | < 0.5 |

Sólo activos en verde pasan a la lista candidata para forward demo.

## 6. Reportes

Por estrategia:

- `<strategy>_backtest.md`: cabecera con run config + commit hash + tabla métricas full + breakdown por activo + breakdown por modo exit.
- `<strategy>_trades.parquet`: todos los Trade del best-mode.
- `<strategy>_equity.parquet`: equity curve por activo.
- `<strategy>_walkforward.md`: tabla IS/OOS por ventana.
- `<strategy>_montecarlo.md`: histograma + quantiles + prob_ruin.

Reporte final: `all_external_comparison.md` con tabla cruzada de las 5 estrategias × modos exit, ranking por Calmar OOS y semáforo Go/No-Go.

## 7. Plan de implementación (alto nivel)

| Fase | Bloque | Bloqueado por |
|------|--------|---------------|
| F1 | Infra: data_loader, Trade, Signal, backtester, metrics, exit_managers, walk_forward, monte_carlo | — |
| F2 | OOPS — strategy + runner + reporte | F1 |
| F3 | SMA-18 — strategy + runner + reporte | F1 |
| F4 | Doble Suelo — strategy + runner + reporte | F1 |
| F5 | Perdices Fib (H1) — strategy + runner + reporte | F1 |
| F6 | COT downloader + estacionalidad | F1 |
| F7 | COT-1 — strategy + runner + reporte | F1, F6 |
| F8 | run_all + reporte comparativo | F2-F7 |
| F9 | Switch Perdices a M5 cuando lleguen datos | M5 entregado por usuario |
| F10 | Variante OOPS RTH NY cuando llegue M1 índices | M1 entregado por usuario |

El plan detallado paso-a-paso lo genera la skill `superpowers:writing-plans` después de aprobar este spec.

## 8. Decisiones explícitas y trade-offs

| Decisión | Alternativa rechazada | Motivo |
|----------|----------------------|---------|
| Polars en lugar de pandas | Pandas (lo que usa el documento fuente) | M1 tracking sobre 8 años × 7 activos × 5 estrategias × 3 modos × 5 ventanas WF — pandas sería minutos a horas por run; polars segundos. |
| Daily signal + M1 tracking | Daily signal + daily tracking (resolución intra-bar) | Resolución conservadora intra-bar daily (worst case stop) sesga métricas en estrategias con TP cercano. M1 da fills realistas. |
| 3 ExitManagers comparados | Sólo modo doc | El documento mismo reconoce que la gestión es heterogénea y poco probada; comparar es la única forma de saber qué gestión vale para qué setup. |
| Pirámide off en SMA-18 V1 | Pirámide on | Añade superficie de bug en V1; queda como flag. Si la estrategia pasa los Go/No-Go, V2 prueba pirámide. |
| `find_peaks` para detector swings #3 | Detector ad-hoc / criterio humano | `scipy.signal.find_peaks` con `prominence` y `distance` es reproducible. La diferencia visual con un humano se documenta con muestras. |
| COT Asset Manager net para índices | Commercials net (no aplica a índices financieros bien) | Para SP500/NASDAQ los Commercials son hedgers institucionales del cash; el smart money speculativo está en Asset Manager. Misma lógica del COT clásico, signo invertido si fuera necesario. |
| Riesgo 0.5%/trade fijo en V1 | Variable | Mantiene comparabilidad con FADE (0.5%) y MATH (0.5%). Si una estrategia justifica más, se ajusta en V2. |
| 2018 → today | 2010 → today | Los CSVs disponibles arrancan en 2018-01-01. Documentamos como limitación. |
| Sin promoción a live en este spec | Diseño live-ready | YAGNI. Live integration tiene su propio diseño cuando una estrategia pase los Go/No-Go. |

## 9. Riesgos del spec

1. **Pureza del daily Vantage para OOPS:** broker time ≠ NY RTH. Mitigación: variante RTH cuando llegue M1.
2. **Detector de swings #3 puede no replicar bien lo "humano":** mitigación documental (20 ejemplos visuales) + sweep de prominence/distance.
3. **COT lag mal aplicado puede dar look-ahead bias.** Mitigación: test unitario explícito sobre el desfase de 3 días + validación con ejemplo histórico conocido.
4. **Dependencia de scipy** para find_peaks. Si el proyecto evita scipy, alternativa: implementación propia de swing detection sobre polars (más trabajo).
5. **Datos M5 / M1 pendientes** del usuario: F9, F10, y la variante M5 de #5 dependen de eso. F1-F8 no se bloquean.

## 10. Checklist de aceptación del spec

- [x] Scope: 5 estrategias bien delimitadas, 1 descartada con motivo.
- [x] Arquitectura: layout claro, separado del bot live.
- [x] Polars confirmado.
- [x] Daily signal + M1 tracking confirmado, con fallback documentado.
- [x] 3 ExitManagers definidos con anclas concretas por estrategia.
- [x] Métricas y validación alineadas con el sistema actual (Walk-forward, MC, sweep).
- [x] Reportes en formato comparable a los existentes (`reports/`).
- [x] Periodo 2018 → today.
- [x] Datos pendientes (M5, M1) listados como dependencias de fase.
- [x] Decisiones técnicas justificadas con alternativa rechazada.
- [x] Riesgos del spec listados.
