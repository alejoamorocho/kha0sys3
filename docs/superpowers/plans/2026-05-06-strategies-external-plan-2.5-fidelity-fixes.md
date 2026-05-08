# Plan 2.5 — Fidelity Fixes vs `outputs/estrategias_detalladas_testeables.md`

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development.

**Goal:** Aligning the implemented exit rules and entry triggers with the **literal text** of the source document `outputs/estrategias_detalladas_testeables.md`. Auditoría detectó 7 desviaciones graves. Este plan las corrige.

**Source of truth:** `C:\Users\aamor\AppData\Local\Claude\local-agent-mode-sessions\63e99e55-64a3-418f-a7a6-04ffe8b7bccb\9916cff7-cb5b-42a1-a313-7e0dff9ce8e6\local_326b04c0-34b3-4c01-ae4f-b1151698ee98\outputs\estrategias_detalladas_testeables.md`

---

## Discrepancias auditadas

| # | Estrategia | Lo que dice el documento | Lo que implementé | Acción |
|---|-----------|--------------------------|---------------------|--------|
| D1 | OOPS | "Target conservador: cierre en EOD. Target agresivo: cierre del gap + extensión 1R" | `tp1 = entry + 2R` | Doc mode = EOD vía `valid_until`, sin `tp1` fijo |
| D2 | SMA-18 | "Aparición de la señal contraria sobre la SMA-18 (dos cierres consecutivos por debajo)" | `stop = nivel SMA-18` (intra-bar instantáneo) | Implementar `exit_on_two_closes_against` en backtester |
| D3 | Doble Suelo | "Distancia mínima entre L1 y L2: 15-30 barras" | `min_separation=15, max_separation=80` | `max_separation=30` |
| D4 | Perdices Fib | "Cerrar si tras 4 horas la posición **no avanza 1R** a favor" | `timestop_bars=240` (cierra siempre a las 4h) | `exit_after_bars_if_below_R=(240, 1.0)` (condicional) |
| D5 | COT-1 | "Cerrar tras 5 días hábiles si no hay TP1" | `timestop_bars=120` (= 2h en M1) | `valid_until = setup + 5d`, sin timestop_bars |
| D6 | COT-1 | "Pin bar / Inside-day breakout / Doble suelo intradía al diario" | Solo pin bar | Añadir inside-day breakout |
| D7 | Riesgo | OOPS=0.75%, SMA-18=1%, DB=1%, Perdices=0.5%, COT-1=1% | Hardcoded 0.5% global | `risk_pct` per-strategy en runner |

**Out of scope (queda como TODO en backlog):**
- Parcial TP1 50% + trailing a BE: requiere position splitting en backtester. Postergado.
- Pirámide SMA-18: documentado en spec. Postergado.

---

## Task layout

```
src/strategies_external/
├── common/
│   └── backtester.py            # MODIFY — añade exit_on_two_closes_against,
│                                 #         exit_after_bars_if_below_R, risk_pct,
│                                 #         signal_df parameter
├── common/signal.py             # MODIFY — campos opcionales adicionales
├── exit_managers.py             # MODIFY — fixes OOPS doc, SMA-18 doc,
│                                 #         Perdices doc, COT-1 doc
├── strategies/
│   ├── double_bottom.py         # MODIFY — max_separation 80 → 30 default
│   └── cot1.py                  # MODIFY — añade inside-day breakout
└── runners/
    ├── run_oops.py              # MODIFY — risk_pct=0.0075
    ├── run_sma18.py             # MODIFY — risk_pct=0.01, pasa signal_df
    ├── run_double_bottom.py     # MODIFY — risk_pct=0.01
    ├── run_perdices_fib.py      # MODIFY — risk_pct=0.005
    └── run_cot1.py              # MODIFY — risk_pct=0.01
```

---

## Task 1: Extender Signal con campos de salida condicional

**Files:**
- Modify: `src/strategies_external/common/signal.py`

- [ ] **Step 1**: añadir 2 campos opcionales nuevos al dataclass:

```python
@dataclass(frozen=True)
class Signal:
    ...  # existing fields
    # NEW (Plan 2.5):
    # Para SMA-18: el backtester cierra el trade si hay N cierres consecutivos
    # del df_signal (típicamente daily) que cruzan este nivel en contra del side.
    exit_on_two_closes_against: float | None = None
    exit_close_count_required: int = 2

    # Para Perdices Fib: tras N barras tracking_tf, si el pnl_R < threshold, cerrar.
    # Tupla (bars, R_threshold). None desactiva.
    exit_after_bars_if_below_R: tuple[int, float] | None = None
```

- [ ] **Step 2**: ejecutar todos los tests existentes — deben pasar (campos nuevos son opcionales).

- [ ] **Step 3**: commit `feat(strategies_external): Signal opcionales para exits condicionales`

---

## Task 2: Backtester con `risk_pct` parámetro y nuevas exit conditions

**Files:**
- Modify: `src/strategies_external/common/backtester.py`
- Modify: `tests/strategies_external/test_backtester.py`

- [ ] **Step 1**: añadir tests nuevos

```python
def test_exit_on_two_closes_against_long():
    """SMA-18 long: 2 cierres daily consecutivos bajo el nivel → salir."""
    base = datetime(2024, 1, 1, 0, 0)
    # signal df: daily bars (00:00 each day)
    signal_rows = [
        (base, 100.0, 102.0, 99.0, 101.0),   # day 0 close=101 above 100 (level)
        (base + timedelta(days=1), 101.0, 103.0, 100.0, 102.0),  # day 1 close=102 above
        (base + timedelta(days=2), 102.0, 102.5, 99.5, 99.8),    # day 2 close=99.8 below ← 1
        (base + timedelta(days=3), 99.8, 100.5, 99.0, 99.5),     # day 3 close=99.5 below ← 2 → exit
        (base + timedelta(days=4), 99.5, 101.0, 99.0, 100.5),
    ]
    signal_df = pl.DataFrame(
        {"time": [r[0] for r in signal_rows], "open": [r[1] for r in signal_rows],
         "high": [r[2] for r in signal_rows], "low": [r[3] for r in signal_rows],
         "close": [r[4] for r in signal_rows], "volume": [1000.0]*5},
        schema={"time": pl.Datetime, "open": pl.Float64, "high": pl.Float64,
                "low": pl.Float64, "close": pl.Float64, "volume": pl.Float64},
    )
    # Tracking df: M1 bars sobre los 5 días (simplificado: una bar por hora ≈ tracking)
    tracking_rows = []
    for i in range(5 * 24):
        ts = base + timedelta(hours=i)
        # precio sigue el daily close approximadamente
        day_idx = i // 24
        c = signal_rows[day_idx][4]
        tracking_rows.append((ts, c, c + 0.2, c - 0.2, c, 100.0))
    tracking_df = pl.DataFrame(
        {"time": [r[0] for r in tracking_rows], "open": [r[1] for r in tracking_rows],
         "high": [r[2] for r in tracking_rows], "low": [r[3] for r in tracking_rows],
         "close": [r[4] for r in tracking_rows], "volume": [r[5] for r in tracking_rows]},
        schema={"time": pl.Datetime, "open": pl.Float64, "high": pl.Float64,
                "low": pl.Float64, "close": pl.Float64, "volume": pl.Float64},
    )
    sig = Signal(
        symbol="XAUUSD", strategy="sma18", side="long",
        setup_ts=base + timedelta(hours=1),  # fill on day 0
        entry_type="market", entry_price=101.0,
        valid_until=base + timedelta(days=10),
        stop=80.0,  # far away, won't hit
        tp1=None, tp2=None,
        exit_on_two_closes_against=100.0,  # SMA level
        exit_close_count_required=2,
    )
    trades = run_backtest([sig], tracking_df, exit_mode="doc",
                          signal_df=signal_df, risk_pct=0.01)
    assert len(trades) == 1
    t = trades[0]
    assert t.exit_reason == "signal_inverso"
    # exit at end of day 3 (close=99.5)
    assert t.exit == pytest.approx(99.5, abs=0.5)


def test_exit_after_bars_if_below_R_perdices():
    """Si tras N bars el pnl < threshold R, cerrar; si lo supera, no."""
    base = datetime(2024, 1, 1, 0, 0)
    rows = []
    # 300 bars; price drift slightly up — never reaches 1R
    for i in range(300):
        ts = base + timedelta(minutes=i)
        c = 100.0 + i * 0.001  # very slow drift
        rows.append((ts, c, c + 0.05, c - 0.05, c, 100.0))
    df = pl.DataFrame(
        {"time": [r[0] for r in rows], "open": [r[1] for r in rows],
         "high": [r[2] for r in rows], "low": [r[3] for r in rows],
         "close": [r[4] for r in rows], "volume": [r[5] for r in rows]},
        schema={"time": pl.Datetime, "open": pl.Float64, "high": pl.Float64,
                "low": pl.Float64, "close": pl.Float64, "volume": pl.Float64},
    )
    sig = Signal(
        symbol="XAUUSD", strategy="perdices_fib", side="long",
        setup_ts=base - timedelta(minutes=1),
        entry_type="market", entry_price=100.0,
        valid_until=base + timedelta(days=1),
        stop=99.0,  # R = 1.0
        tp1=None, tp2=None,
        exit_after_bars_if_below_R=(240, 1.0),  # 240 bars, 1R threshold
    )
    trades = run_backtest([sig], df, exit_mode="doc", risk_pct=0.005)
    assert len(trades) == 1
    assert trades[0].exit_reason == "timestop"
    assert trades[0].bars_in_trade == 240


def test_risk_pct_propagates_to_pnl_pct():
    """pnl_pct usa el risk_pct del runner, no el global default."""
    base = datetime(2024, 1, 1)
    rows = [(base + timedelta(minutes=i), 100.0 + i*0.1, 100.0 + i*0.1 + 0.1,
             100.0 + i*0.1 - 0.1, 100.0 + i*0.1, 100.0) for i in range(20)]
    df = pl.DataFrame(
        {"time": [r[0] for r in rows], "open": [r[1] for r in rows],
         "high": [r[2] for r in rows], "low": [r[3] for r in rows],
         "close": [r[4] for r in rows], "volume": [r[5] for r in rows]},
        schema={"time": pl.Datetime, "open": pl.Float64, "high": pl.Float64,
                "low": pl.Float64, "close": pl.Float64, "volume": pl.Float64},
    )
    sig = Signal(
        symbol="SP500", strategy="oops", side="long",
        setup_ts=base - timedelta(minutes=1),
        entry_type="market", entry_price=100.0,
        valid_until=base + timedelta(minutes=20),
        stop=99.0, tp1=101.0, tp2=None,
    )
    # Use risk_pct=0.01 (1%) instead of default 0.005
    trades = run_backtest([sig], df, exit_mode="doc", risk_pct=0.01)
    assert len(trades) == 1
    # pnl_pct = pnl_R * 0.01 (no 0.005)
    assert trades[0].pnl_pct == pytest.approx(trades[0].pnl_R * 0.01, abs=1e-6)
```

- [ ] **Step 2**: ejecutar tests, verificar que fallan por nueva firma.

- [ ] **Step 3**: modificar `run_backtest` signature y lógica.

```python
def run_backtest(
    signals: list[Signal],
    tracking_df: pl.DataFrame,
    exit_mode: ExitMode,
    signal_df: pl.DataFrame | None = None,
    risk_pct: float = RISK_PER_TRADE_PCT_DEFAULT,
) -> list[Trade]:
    ...
```

Cambios al loop intra-bar (después del fill, dentro del `for j in range(...)`):

```python
            # NUEVO: salida por bars + R threshold
            if sig.exit_after_bars_if_below_R is not None:
                bars_threshold, r_threshold = sig.exit_after_bars_if_below_R
                if bars_in_trade >= bars_threshold:
                    # current pnl en R
                    if sig.side == "long":
                        cur_R = (close - sig.entry_price) / R
                    else:
                        cur_R = (sig.entry_price - close) / R
                    if cur_R < r_threshold:
                        exit_reason = "timestop"; exit_price = close; exit_ts = bar["time"]; break
                    # si supera el threshold, no cerrar (deja correr)

            # NUEVO: salida por 2 cierres consecutivos contra nivel
            # Aplica solo si hay signal_df y el bar coincide con un cierre del signal_df
            if (sig.exit_on_two_closes_against is not None
                    and signal_df is not None):
                # ¿es esta bar el cierre de un período del signal_df?
                # Aproximación: detectar cambio de fecha (daily close)
                if j == 0 or rows[j]["time"].date() != rows[j - 1]["time"].date():
                    # Buscar el cierre del signal_df que coincide con la fecha de bar prev
                    prev_date = rows[j - 1]["time"].date() if j > 0 else None
                    if prev_date is not None:
                        # Más simple: contar cierres del signal_df que han cruzado nivel
                        # desde fill_ts hacia atrás
                        ...
```

Esta lógica es compleja. Versión simplificada — el backtester **opera en el daily directamente cuando `exit_on_two_closes_against` está set**:

Mejor enfoque: si `signal_df` está provisto Y `exit_on_two_closes_against` está set, usar el signal_df como tracking para esa salida (no el tracking_df). Es más limpio.

Implementación pragmática:

```python
        # ... después de detectar fill ...
        # Si hay exit_on_two_closes_against, pre-calcular las fechas de exit por cierres consecutivos
        forced_close_ts = None
        forced_close_price = None
        if sig.exit_on_two_closes_against is not None and signal_df is not None:
            level = sig.exit_on_two_closes_against
            count_req = sig.exit_close_count_required
            sig_rows_after = signal_df.filter(pl.col("time") > entry_ts).sort("time").to_dicts()
            consec = 0
            for srow in sig_rows_after:
                close_val = srow["close"]
                triggered = (close_val < level) if sig.side == "long" else (close_val > level)
                if triggered:
                    consec += 1
                    if consec >= count_req:
                        forced_close_ts = srow["time"]
                        forced_close_price = close_val
                        break
                else:
                    consec = 0

        # ... loop intra-bar ...
        for j in range(first_idx, len(rows)):
            bar = rows[j]
            bars_in_trade = j - first_idx + 1
            high = bar["high"]; low = bar["low"]; close = bar["close"]

            # NUEVO: forced close por 2 cierres consecutivos
            if forced_close_ts is not None and bar["time"] >= forced_close_ts:
                exit_reason = "signal_inverso"; exit_price = forced_close_price
                exit_ts = forced_close_ts; break

            # ... resto de la lógica existente (stop, tp1, tp2, timestop, after_bars_if_below_R) ...
```

Y al final, donde se calcula `pnl_pct`:

```python
        pnl_pct = pnl_net_R * risk_pct  # NO RISK_PER_TRADE_PCT_DEFAULT
```

- [ ] **Step 4**: ejecutar tests, verificar 4 nuevos passed.

- [ ] **Step 5**: commit `feat(strategies_external): backtester risk_pct + exit_on_two_closes_against + exit_after_bars_if_below_R`

---

## Task 3: Fix DocExitManager para fidelidad al documento

**Files:**
- Modify: `src/strategies_external/exit_managers.py`
- Modify: `tests/strategies_external/test_exit_managers.py` y `test_exit_managers_extensions.py`

### D1 — OOPS doc: target = EOD (no tp1=2R)

```python
def _oops(self, s: Signal) -> Signal:
    if s.side == "long":
        stop = _require_anchor(s, "today_low")
    else:
        stop = _require_anchor(s, "today_high")
    # Doc target = EOD: el backtester cierra al close de la última barra antes
    # de valid_until cuando no hay tp/stop hit. tp1=None, tp2=None.
    return replace(s, stop=stop, tp1=None, tp2=None)
```

Test: `test_doc_exit_manager_oops_long` debe asertar `s.tp1 is None`. Actualizar test.

### D2 — SMA-18 doc: 2 cierres consecutivos contra SMA-18

```python
def _sma18(self, s: Signal) -> Signal:
    sma = _require_anchor(s, "sma18")
    atr = _require_anchor(s, "atr14")
    # Stop "hard" como protección extrema: SMA - 3*ATR (long) en caso de gap brutal
    if s.side == "long":
        hard_stop = sma - 3 * atr
    else:
        hard_stop = sma + 3 * atr
    return replace(
        s,
        stop=hard_stop,
        tp1=None, tp2=None,
        exit_on_two_closes_against=sma,  # backtester cierra cuando 2 cierres daily contra
        exit_close_count_required=2,
    )
```

Test: actualizar `test_doc_exit_manager_sma18_long` para verificar `exit_on_two_closes_against == 2025.0` y `stop = 2025 - 3*15 = 1980`.

### D4 — Perdices Fib: time stop condicional

```python
def _perdices_fib(self, s: Signal) -> Signal:
    if s.side == "long":
        stop = _require_anchor(s, "swing_low") - 0.2
        tp1 = _require_anchor(s, "swing_high")
    else:
        stop = _require_anchor(s, "swing_high") + 0.2
        tp1 = _require_anchor(s, "swing_low")
    return replace(
        s, stop=stop, tp1=tp1, tp2=None,
        timestop_bars=None,  # no fixed timestop
        exit_after_bars_if_below_R=(240, 1.0),  # 4h en M1 + condicional 1R
    )
```

Test: actualizar `test_doc_exit_manager_perdices_long` para verificar `exit_after_bars_if_below_R == (240, 1.0)` y `timestop_bars is None`.

### D5 — COT-1 doc: 5 días vía valid_until, sin timestop_bars

```python
def _cot1(self, s: Signal) -> Signal:
    atr = _require_anchor(s, "atr14")
    if s.side == "long":
        stop = _require_anchor(s, "swing_low_5d") - 0.5 * atr
        R = s.entry_price - stop
        tp1 = s.entry_price + 1.5 * R
        tp2 = s.entry_price + 3.0 * R
    else:
        stop = _require_anchor(s, "swing_high_5d") + 0.5 * atr
        R = stop - s.entry_price
        tp1 = s.entry_price - 1.5 * R
        tp2 = s.entry_price - 3.0 * R
    # NO timestop_bars (eso era el bug — se interpretaba en bars del tracking_tf, M1).
    # El doc dice "5 días hábiles": eso ya está cubierto por valid_until que la
    # estrategia setea a setup_ts + 5 days. Backtester cierra eod cuando expira.
    return replace(s, stop=stop, tp1=tp1, tp2=tp2, timestop_bars=None)
```

(El IndicatorExitManager._cot1 mismo cambio.)

Y en `src/strategies_external/strategies/cot1.py`, cambiar:

```python
            valid_until = cur_ts + timedelta(days=5)  # ya estaba
            ...
            signals.append(Signal(
                ...
                timestop_bars=None,  # antes 120 (bug)
                ...
            ))
```

- [ ] **Step 1**: actualizar tests con valores nuevos.
- [ ] **Step 2**: aplicar cambios al exit_managers.py y cot1.py.
- [ ] **Step 3**: ejecutar tests, verificar passes.
- [ ] **Step 4**: commit `fix(strategies_external): align Doc/Indicator exits con documento literal`

---

## Task 4: Doble Suelo separación 15-30

**Files:**
- Modify: `src/strategies_external/strategies/double_bottom.py`

```python
class DoubleBottomStrategy(Strategy):
    name = "double_bottom"

    def __init__(
        self,
        tolerance: float = 0.02,
        min_separation: int = 15,
        max_separation: int = 30,  # ← cambio: 80 → 30 (literal del documento)
        ...
    ):
```

Test `test_double_bottom_detects_pattern` puede fallar si su fixture tenía L1-L2 separation > 30. Verificar y ajustar fixture si necesario.

- [ ] **Step 1-5**: TDD.
- [ ] Commit: `fix(strategies_external): Doble Suelo max_separation 80 → 30`

---

## Task 5: COT-1 inside-day breakout trigger

**Files:**
- Modify: `src/strategies_external/strategies/cot1.py`
- Modify: `tests/strategies_external/test_cot1_strategy.py`

Añadir helper:

```python
def _is_inside_day_breakout(prev2, prev1, cur, side: str) -> bool:
    """prev1 es inside-day vs prev2; cur rompe extremos en dirección bias."""
    inside_day = prev1["high"] < prev2["high"] and prev1["low"] > prev2["low"]
    if not inside_day:
        return False
    if side == "long":
        return cur["high"] > prev1["high"]
    return cur["low"] < prev1["low"]
```

En `generate_signals`, dentro del loop, después del check de pin bar añadir:

```python
        if i >= 2:
            prev2 = rows[i - 2]
            prev1 = rows[i - 1]
            if applicable_cot >= self.cot_threshold_long and seasonal >= self.seasonal_threshold:
                if _is_inside_day_breakout(prev2, prev1, cur, "long"):
                    signals.append(Signal(
                        ...long signal con entry = prev1["high"] + 0.01...
                    ))
            if applicable_cot <= self.cot_threshold_short and seasonal <= -self.seasonal_threshold:
                if _is_inside_day_breakout(prev2, prev1, cur, "short"):
                    signals.append(Signal(
                        ...short signal con entry = prev1["low"] - 0.01...
                    ))
```

Test añadir `test_cot1_inside_day_breakout_signal`.

- [ ] Commit: `feat(strategies_external): COT-1 añade inside-day breakout trigger`

---

## Task 6: Runners pasan risk_pct correcto

**Files:**
- Modify: `src/strategies_external/runners/run_oops.py` → `risk_pct=0.0075`
- Modify: `src/strategies_external/runners/run_sma18.py` → `risk_pct=0.01`, además pasa `signal_df=df_daily` al backtester (necesario para SMA-18 doc)
- Modify: `src/strategies_external/runners/run_double_bottom.py` → `risk_pct=0.01`
- Modify: `src/strategies_external/runners/run_perdices_fib.py` → `risk_pct=0.005`
- Modify: `src/strategies_external/runners/run_cot1.py` → `risk_pct=0.01`

En cada runner, todas las llamadas a `run_backtest(...)` deben recibir `risk_pct=...` y, donde aplique (SMA-18), `signal_df=df_daily`.

Update también el config dict en cada runner para que el reporte refleje el risk_pct usado:
```python
config={"period": "...", "risk_pct": 0.01, "atr_grid": atr_grid}
```

- [ ] **Step 1-5**: aplicar cambios + commit por runner (5 commits).

---

## Task 7: Re-correr todos los backtests + tabla deltas

**Files:**
- Run standalone para cada strategy.
- Compilar tabla deltas en `reports/external/plan_2_5_deltas.md`.

```bash
python -m src.strategies_external.runners.run_oops
python -m src.strategies_external.runners.run_sma18
python -m src.strategies_external.runners.run_double_bottom
python -m src.strategies_external.runners.run_perdices_fib
python -m src.strategies_external.runners.run_cot1
```

Tabla de comparación:

| Strategy | Métrica | Plan 2 | Plan 2.5 | Δ |
|----------|---------|--------|----------|---|
| OOPS doc | calmar | -1.013 | (nuevo) | (delta) |
| OOPS doc | n | 124 | (nuevo) | |
| SMA-18 doc | calmar | 0.544 | (nuevo) | |
| SMA-18 doc | n | 4241 | (nuevo) | |
| ... | ... | | | |

- [ ] Commit: `chore(reports): refresh backtests with Plan 2.5 fidelity fixes + deltas`

---

## Self-review

- [ ] Cada fix corresponde a un texto literal en `outputs/estrategias_detalladas_testeables.md`.
- [ ] Tests cubren las salidas nuevas (`exit_on_two_closes_against`, `exit_after_bars_if_below_R`, `risk_pct`).
- [ ] Backtester sigue pasando los tests existentes (no regresión).
- [ ] Reportes muestran metrics nuevas y deltas vs runs anteriores.

---

## After Plan 2.5 → Plan 3 (FADE/MATH con M1)

Plan 3 sería: re-evaluar las 108 estrategias FADE + 34 MATH del bot live usando el módulo nuevo (polars + tracking M1) sobre los activos overlap (XAUUSD, XAGUSD, SP500, NASDAQ100, EURUSD, USDJPY, GBPAUD). Comparar contra las métricas actuales del bot live para detectar drift o bugs.

Eso se documenta cuando lleguemos.
