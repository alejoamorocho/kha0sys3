"""Math-FADE discovery pipeline — M15 only.

FADE mechanics applied to MATH-indicator extremes (not ORB).

Per setup at bar T:
- Entry: LIMIT at close[T] in fade direction (opposite of extreme).
- Wait window: next 5 bars (75 min on M15). If not filled -> cancel.
- Direction guard: if the setup indicator's magnitude grows in the same
  direction as the original extreme during the wait, cancel immediately.
- On fill: TP at entry -/+ tp_atr_mult*ATR, SL at entry +/- sl_atr_mult*ATR.
- Session time-stop.
- Dedup: 1 trade per (symbol, setup_type, date).

Phases:
    A = setup screen at default TP=0.5/SL=2.5 ATR
    B = R:R grid on Phase-A survivors (TP x SL = 16 combos)
    C = WF + MC + decay robustness

Usage:
    python -m src.engine.run_math_fade --phase {a,b,c,all}
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from pathlib import Path
import polars as pl

from src.domain.constants import (
    INDICATOR_UNIVERSE, INDICATOR_SESSIONS,
    FRICTION_FX, FRICTION_INDEX, INDEX_SYMBOLS,
    WF_IS_MONTHS, WF_OOS_MONTHS,
)
from src.engine.run_math_discovery import _load_and_enrich_math
from src.engine.run_indicator_discovery import _filter_by_session
from src.engine.indicator_validation import (
    compute_metrics, walk_forward_wr, monte_carlo_ruin, decay_slope_ratio,
)

REPORTS_DIR = Path("reports")
TF = "M15"

SETUP_TYPES = (
    "KALMAN_PEAK_FADE",
    "ZSCORE_EXTREME_FADE",
    "OLS_EXTREME_FADE",
    "CURVATURE_PEAK_FADE",
    "GARCH_Z_FADE",
    "AREA_EXTREME_FADE",
)

# Phase A gates
PA_DEFAULT_TP = 0.5
PA_DEFAULT_SL = 2.5
PA_MIN_TRADES_PER_YEAR = 15
PA_MIN_WR = 0.80

# Phase B grid + gates
PB_TP_GRID = (0.3, 0.5, 0.75, 1.0)
PB_SL_GRID = (1.5, 2.0, 2.5, 3.0)
PB_MIN_TRADES_PER_YEAR = 15
PB_MIN_WR = 0.80
PB_MIN_PF = 1.20
PB_MIN_EXPECTANCY = 0.05

# Phase C gates
PC_MIN_WF_RATIO = 0.80
PC_MAX_MC_RUIN = 0.02
PC_MIN_DECAY = 0.60

WAIT_BARS = 5  # 75 min on M15


def _friction_for(symbol: str) -> float:
    return FRICTION_INDEX if symbol in INDEX_SYMBOLS else FRICTION_FX


def _session_end_hour(session: str) -> int:
    return INDICATOR_SESSIONS[session][1]


# ── Setup detection ──────────────────────────────────────────────────────

@dataclass(frozen=True)
class BacktestConfig:
    tp_atr_mult: float
    sl_atr_mult: float
    session_end_hour_utc: int
    friction_r: float


def detect_setups(bars: pl.DataFrame, setup_type: str) -> pl.DataFrame:
    """Return a DataFrame with columns: time, close, direction, atr_14,
    indicator_value (signed magnitude used for direction guard).

    Detection at bar T: the setup fires when bar T-1 was the extreme peak
    and bar T shows the first bar of decay. The fade direction opposes the
    extreme's sign.
    """
    if len(bars) == 0:
        return _empty_setups()

    df = bars
    if setup_type == "KALMAN_PEAK_FADE":
        ind = pl.col("kalman_innovation")
        abs_ind = ind.abs()
        std = ind.rolling_std(window_size=50)
        # peak at T-1: |innov[T-1]| >= max(|innov[T-3..T-1]|) and > 1.5*std
        prev_abs = abs_ind.shift(1)
        peak_cond = (
            (prev_abs >= abs_ind.shift(2))
            & (prev_abs >= abs_ind.shift(3))
            & (prev_abs > 1.5 * std.shift(1))
        )
        decay_cond = abs_ind < prev_abs
        direction = pl.when(ind.shift(1) > 0).then(pl.lit("SHORT")).otherwise(pl.lit("LONG"))
        fire = peak_cond & decay_cond & ind.shift(1).is_not_null()
        ind_signed = ind.shift(1)

    elif setup_type == "ZSCORE_EXTREME_FADE":
        ind = pl.col("zscore_30")
        abs_ind = ind.abs()
        prev_abs = abs_ind.shift(1)
        peak_cond = prev_abs >= 2.0
        decay_cond = abs_ind < prev_abs
        direction = pl.when(ind.shift(1) > 0).then(pl.lit("SHORT")).otherwise(pl.lit("LONG"))
        fire = peak_cond & decay_cond & ind.shift(1).is_not_null()
        ind_signed = ind.shift(1)

    elif setup_type == "OLS_EXTREME_FADE":
        ind = pl.col("ols_resid_z_30")
        abs_ind = ind.abs()
        prev_abs = abs_ind.shift(1)
        peak_cond = prev_abs >= 2.0
        decay_cond = abs_ind < prev_abs
        direction = pl.when(ind.shift(1) > 0).then(pl.lit("SHORT")).otherwise(pl.lit("LONG"))
        fire = peak_cond & decay_cond & ind.shift(1).is_not_null()
        ind_signed = ind.shift(1)

    elif setup_type == "CURVATURE_PEAK_FADE":
        ind = pl.col("curvature_10")
        abs_ind = ind.abs()
        std = ind.rolling_std(window_size=50)
        prev_abs = abs_ind.shift(1)
        # local peak over last 5 bars at T-1
        peak_cond = (
            (prev_abs >= abs_ind.shift(2))
            & (prev_abs >= abs_ind.shift(3))
            & (prev_abs >= abs_ind.shift(4))
            & (prev_abs >= abs_ind.shift(5))
            & (prev_abs > 2.0 * std.shift(1))
        )
        decay_cond = abs_ind < prev_abs
        # curvature > 0 = accelerating up => fade SHORT
        direction = pl.when(ind.shift(1) > 0).then(pl.lit("SHORT")).otherwise(pl.lit("LONG"))
        fire = peak_cond & decay_cond & ind.shift(1).is_not_null()
        ind_signed = ind.shift(1)

    elif setup_type == "GARCH_Z_FADE":
        gv = pl.col("garch_vol_z_50")
        z = pl.col("zscore_30")
        fire = (gv > 2.0) & (z.abs() > 1.5) & gv.is_not_null() & z.is_not_null()
        direction = pl.when(z > 0).then(pl.lit("SHORT")).otherwise(pl.lit("LONG"))
        ind_signed = z  # direction guard tracks zscore magnitude

    elif setup_type == "AREA_EXTREME_FADE":
        ind = pl.col("meanrev_area_50")
        abs_ind = ind.abs()
        std = ind.rolling_std(window_size=100)
        prev_abs = abs_ind.shift(1)
        peak_cond = prev_abs > 2.0 * std.shift(1)
        decay_cond = abs_ind < prev_abs
        direction = pl.when(ind.shift(1) > 0).then(pl.lit("SHORT")).otherwise(pl.lit("LONG"))
        fire = peak_cond & decay_cond & ind.shift(1).is_not_null()
        ind_signed = ind.shift(1)

    else:
        raise ValueError(f"Unknown setup_type: {setup_type}")

    setups = df.with_columns([
        fire.alias("_fire"),
        direction.alias("direction"),
        ind_signed.alias("ind_signed"),
    ]).filter(pl.col("_fire") & pl.col("atr_14").is_not_null()).select([
        "time", "close", "direction", "atr_14", "ind_signed",
    ])
    return setups


def _empty_setups() -> pl.DataFrame:
    return pl.DataFrame(schema={
        "time": pl.Datetime, "close": pl.Float64, "direction": pl.Utf8,
        "atr_14": pl.Float64, "ind_signed": pl.Float64,
    })


# ── Backtester ───────────────────────────────────────────────────────────

def _guard_indicator_col(setup_type: str) -> str:
    return {
        "KALMAN_PEAK_FADE": "kalman_innovation",
        "ZSCORE_EXTREME_FADE": "zscore_30",
        "OLS_EXTREME_FADE": "ols_resid_z_30",
        "CURVATURE_PEAK_FADE": "curvature_10",
        "GARCH_Z_FADE": "zscore_30",
        "AREA_EXTREME_FADE": "meanrev_area_50",
    }[setup_type]


def run_backtest(setups: pl.DataFrame, bars: pl.DataFrame, setup_type: str,
                 cfg: BacktestConfig, symbol: str) -> pl.DataFrame:
    """Event-driven FADE backtest with LIMIT wait window + direction guard."""
    if len(setups) == 0:
        return _empty_trades()

    # Dedup: first per (date, setup_type)
    setups = setups.with_columns(pl.col("time").dt.date().alias("_date")) \
        .sort("time").unique(subset=["_date"], keep="first").drop("_date")

    bars_sorted = bars.sort("time")
    guard_col = _guard_indicator_col(setup_type)
    bar_times = bars_sorted["time"].to_list()
    bar_highs = bars_sorted["high"].to_list()
    bar_lows = bars_sorted["low"].to_list()
    bar_closes = bars_sorted["close"].to_list()
    guard_vals = bars_sorted[guard_col].to_list()
    time_to_idx = {t: i for i, t in enumerate(bar_times)}

    results = []
    for s in setups.iter_rows(named=True):
        atr = s["atr_14"]
        if atr is None or atr <= 0:
            continue
        direction = s["direction"]
        limit_price = s["close"]
        ind0 = s["ind_signed"]
        if ind0 is None:
            continue
        start_idx = time_to_idx.get(s["time"])
        if start_idx is None:
            continue

        # Direction guard: extreme grew further in original direction -> cancel
        ind0_sign = 1.0 if ind0 > 0 else -1.0
        ind0_abs = abs(ind0)

        # Wait window for fill
        fill_idx = None
        fill_price = None
        end_wait = min(start_idx + 1 + WAIT_BARS, len(bar_times))
        cancelled = False
        for i in range(start_idx + 1, end_wait):
            # Direction guard check
            gv = guard_vals[i]
            if gv is not None:
                # cancel if indicator magnitude GROWS in same sign as original extreme
                if (gv * ind0_sign) > ind0_abs:
                    cancelled = True
                    break
            hi = bar_highs[i]
            lo = bar_lows[i]
            # LIMIT fill: LONG LIMIT below entry requires lo<=limit; SHORT LIMIT above requires hi>=limit
            if direction == "LONG":
                if lo <= limit_price:
                    fill_idx = i
                    fill_price = limit_price
                    break
            else:
                if hi >= limit_price:
                    fill_idx = i
                    fill_price = limit_price
                    break
        if cancelled or fill_idx is None:
            continue

        entry = fill_price
        if direction == "LONG":
            tp = entry + cfg.tp_atr_mult * atr
            sl = entry - cfg.sl_atr_mult * atr
        else:
            tp = entry - cfg.tp_atr_mult * atr
            sl = entry + cfg.sl_atr_mult * atr

        exit_reason = None
        exit_price = None
        exit_time = None
        signal_date = s["time"].date()
        for j in range(fill_idx + 1, len(bar_times)):
            bt = bar_times[j]
            if bt.date() > signal_date or bt.hour >= cfg.session_end_hour_utc:
                exit_reason = "TIME_STOP"
                exit_price = bar_closes[j - 1]
                exit_time = bar_times[j - 1]
                break
            hi = bar_highs[j]
            lo = bar_lows[j]
            if direction == "LONG":
                if hi >= tp:
                    exit_reason, exit_price, exit_time = "TP", tp, bt
                    break
                if lo <= sl:
                    exit_reason, exit_price, exit_time = "SL", sl, bt
                    break
            else:
                if lo <= tp:
                    exit_reason, exit_price, exit_time = "TP", tp, bt
                    break
                if hi >= sl:
                    exit_reason, exit_price, exit_time = "SL", sl, bt
                    break
        else:
            exit_reason = "TIME_STOP"
            exit_price = bar_closes[-1]
            exit_time = bar_times[-1]

        risk_per_unit = cfg.sl_atr_mult * atr
        if direction == "LONG":
            pnl = exit_price - entry
        else:
            pnl = entry - exit_price
        r_gross = pnl / risk_per_unit if risk_per_unit > 0 else 0.0
        r_net = r_gross - cfg.friction_r

        results.append({
            "time": s["time"], "symbol": symbol,
            "setup_type": setup_type, "direction": direction,
            "entry_price": entry, "tp_price": tp, "sl_price": sl,
            "exit_time": exit_time, "exit_price": exit_price,
            "exit_reason": exit_reason, "r_multiple": r_net,
        })
    if not results:
        return _empty_trades()
    return pl.DataFrame(results)


def _empty_trades() -> pl.DataFrame:
    return pl.DataFrame(schema={
        "time": pl.Datetime, "symbol": pl.Utf8, "setup_type": pl.Utf8, "direction": pl.Utf8,
        "entry_price": pl.Float64, "tp_price": pl.Float64, "sl_price": pl.Float64,
        "exit_time": pl.Datetime, "exit_price": pl.Float64, "exit_reason": pl.Utf8,
        "r_multiple": pl.Float64,
    })


# ── Phase A ──────────────────────────────────────────────────────────────

def run_phase_a() -> pl.DataFrame:
    total = len(INDICATOR_UNIVERSE) * len(INDICATOR_SESSIONS) * len(SETUP_TYPES)
    print(f"[FADE-PhaseA] {total} combos "
          f"({len(INDICATOR_UNIVERSE)} assets x {len(INDICATOR_SESSIONS)} sessions x {len(SETUP_TYPES)} setups)")

    rows = []
    i = 0
    for symbol in INDICATOR_UNIVERSE:
        try:
            bars = _load_and_enrich_math(symbol)
        except FileNotFoundError:
            print(f"[FADE-PhaseA][SKIP] {symbol}: no data")
            continue
        friction = _friction_for(symbol)
        for setup_type in SETUP_TYPES:
            try:
                all_setups = detect_setups(bars, setup_type)
            except Exception as exc:
                print(f"[FADE-PhaseA][SKIP] {symbol}/{setup_type}: {exc}")
                continue
            for session in INDICATOR_SESSIONS:
                i += 1
                sigs = _filter_by_session(all_setups, session)
                if len(sigs) < 10:
                    continue
                cfg = BacktestConfig(
                    tp_atr_mult=PA_DEFAULT_TP, sl_atr_mult=PA_DEFAULT_SL,
                    session_end_hour_utc=_session_end_hour(session),
                    friction_r=friction,
                )
                trades = run_backtest(sigs, bars, setup_type, cfg, symbol)
                if len(trades) == 0:
                    continue
                m = compute_metrics(trades)
                rows.append({
                    "symbol": symbol, "tf": TF, "session": session,
                    "setup_type": setup_type,
                    "n_trades": m.n_trades, "wr": m.wr, "pf": m.profit_factor,
                    "expectancy_r": m.expectancy_r, "max_dd_r": m.max_dd_r,
                    "trades_per_year": m.trades_per_year,
                })
                if i % 50 == 0:
                    print(f"[FADE-PhaseA] {i}/{total} — {symbol}/{session}/{setup_type}")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    if not rows:
        print("[FADE-PhaseA] No results.")
        pl.DataFrame().write_parquet(REPORTS_DIR / "math_fade_phase_a.parquet")
        (REPORTS_DIR / "math_fade_phase_a.md").write_text(
            "# Math FADE Phase A\n\nNo combos produced trades.\n", encoding="utf-8")
        return pl.DataFrame()

    results = pl.DataFrame(rows)
    survivors = results.filter(
        (pl.col("trades_per_year") >= PA_MIN_TRADES_PER_YEAR)
        & (pl.col("wr") >= PA_MIN_WR)
    ).sort("expectancy_r", descending=True)

    results.write_parquet(REPORTS_DIR / "math_fade_phase_a.parquet")
    survivors.write_parquet(REPORTS_DIR / "math_fade_phase_a_survivors.parquet")
    (REPORTS_DIR / "math_fade_phase_a.md").write_text(
        _render_phase_a_md(results, survivors), encoding="utf-8")
    print(f"[FADE-PhaseA] {len(results)} evaluated, {len(survivors)} passed gates")
    return survivors


def _render_phase_a_md(results: pl.DataFrame, survivors: pl.DataFrame) -> str:
    lines = [
        "# Math FADE — Phase A Report", "",
        f"- Combos evaluated: **{len(results)}**",
        f"- Passed gates: **{len(survivors)}**",
        f"- Gates: trades/year >= {PA_MIN_TRADES_PER_YEAR}, WR >= {PA_MIN_WR}",
        f"- TP/SL: {PA_DEFAULT_TP}xATR / {PA_DEFAULT_SL}xATR",
        "",
        "## Top 30 survivors",
        "",
        "| Symbol | Session | Setup | Trades | WR | PF | Exp (R) | MaxDD (R) | Trades/yr |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for r in survivors.head(30).iter_rows(named=True):
        lines.append(
            f"| {r['symbol']} | {r['session']} | {r['setup_type']} "
            f"| {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.2f} "
            f"| {r['expectancy_r']:.3f} | {r['max_dd_r']:.1f} | {r['trades_per_year']:.1f} |"
        )
    return "\n".join(lines) + "\n"


# ── Phase B ──────────────────────────────────────────────────────────────

def run_phase_b() -> pl.DataFrame:
    surv_path = REPORTS_DIR / "math_fade_phase_a_survivors.parquet"
    if not surv_path.exists():
        raise FileNotFoundError(f"Run Phase-A first (missing {surv_path})")
    survivors = pl.read_parquet(surv_path)
    if len(survivors) == 0:
        print("[FADE-PhaseB] No Phase-A survivors.")
        pl.DataFrame().write_parquet(REPORTS_DIR / "math_fade_phase_b.parquet")
        (REPORTS_DIR / "math_fade_phase_b.md").write_text(
            "# Math FADE Phase B\n\nNo Phase-A survivors.\n", encoding="utf-8")
        return pl.DataFrame()

    rr_combos = [(tp, sl) for tp in PB_TP_GRID for sl in PB_SL_GRID]
    total = len(survivors) * len(rr_combos)
    print(f"[FADE-PhaseB] {len(survivors)} x {len(rr_combos)} = {total}")

    rows = []
    for surv in survivors.iter_rows(named=True):
        symbol, session, setup_type = surv["symbol"], surv["session"], surv["setup_type"]
        try:
            bars = _load_and_enrich_math(symbol)
        except FileNotFoundError:
            continue
        all_setups = detect_setups(bars, setup_type)
        sigs = _filter_by_session(all_setups, session)
        if len(sigs) < 10:
            continue
        friction = _friction_for(symbol)
        session_end = _session_end_hour(session)
        for tp_mult, sl_mult in rr_combos:
            cfg = BacktestConfig(
                tp_atr_mult=tp_mult, sl_atr_mult=sl_mult,
                session_end_hour_utc=session_end, friction_r=friction,
            )
            trades = run_backtest(sigs, bars, setup_type, cfg, symbol)
            if len(trades) == 0:
                continue
            m = compute_metrics(trades)
            if (m.trades_per_year < PB_MIN_TRADES_PER_YEAR
                    or m.wr < PB_MIN_WR
                    or m.profit_factor < PB_MIN_PF
                    or m.expectancy_r < PB_MIN_EXPECTANCY):
                continue
            rows.append({
                "symbol": symbol, "tf": TF, "session": session,
                "setup_type": setup_type,
                "tp_atr_mult": tp_mult, "sl_atr_mult": sl_mult,
                "n_trades": m.n_trades, "wr": m.wr, "pf": m.profit_factor,
                "expectancy_r": m.expectancy_r, "max_dd_r": m.max_dd_r,
                "trades_per_year": m.trades_per_year,
            })

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    if not rows:
        print("[FADE-PhaseB] 0 survivors passed gates.")
        pl.DataFrame().write_parquet(REPORTS_DIR / "math_fade_phase_b.parquet")
        (REPORTS_DIR / "math_fade_phase_b.md").write_text(
            "# Math FADE Phase B\n\n0 survivors passed R:R gates.\n", encoding="utf-8")
        return pl.DataFrame()

    phase_b = pl.DataFrame(rows).sort("expectancy_r", descending=True)
    phase_b.write_parquet(REPORTS_DIR / "math_fade_phase_b.parquet")
    (REPORTS_DIR / "math_fade_phase_b.md").write_text(
        _render_phase_b_md(phase_b), encoding="utf-8")
    print(f"[FADE-PhaseB] {len(phase_b)} passed R:R gates")
    return phase_b


def _render_phase_b_md(phase_b: pl.DataFrame) -> str:
    lines = [
        "# Math FADE — Phase B Report", "",
        f"- Survivors: **{len(phase_b)}**",
        f"- Gates: trades/yr>={PB_MIN_TRADES_PER_YEAR}, WR>={PB_MIN_WR}, "
        f"PF>={PB_MIN_PF}, exp>={PB_MIN_EXPECTANCY}R",
        "",
        "| Symbol | Session | Setup | TP | SL | Trades | WR | PF | Exp(R) | MaxDD(R) | T/yr |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in phase_b.iter_rows(named=True):
        lines.append(
            f"| {r['symbol']} | {r['session']} | {r['setup_type']} "
            f"| {r['tp_atr_mult']} | {r['sl_atr_mult']} "
            f"| {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.2f} "
            f"| {r['expectancy_r']:.3f} | {r['max_dd_r']:.1f} | {r['trades_per_year']:.1f} |"
        )
    return "\n".join(lines) + "\n"


# ── Phase C ──────────────────────────────────────────────────────────────

def run_phase_c() -> pl.DataFrame:
    pb_path = REPORTS_DIR / "math_fade_phase_b.parquet"
    if not pb_path.exists():
        raise FileNotFoundError(f"Run Phase-B first (missing {pb_path})")
    phase_b = pl.read_parquet(pb_path)
    if len(phase_b) == 0:
        print("[FADE-PhaseC] No Phase-B survivors.")
        _write_empty_final()
        return pl.DataFrame()

    print(f"[FADE-PhaseC] Validating {len(phase_b)} Phase-B survivors")
    final_rows = []

    for surv in phase_b.iter_rows(named=True):
        symbol = surv["symbol"]; session = surv["session"]; setup_type = surv["setup_type"]
        tp_mult = surv["tp_atr_mult"]; sl_mult = surv["sl_atr_mult"]
        try:
            bars = _load_and_enrich_math(symbol)
        except FileNotFoundError:
            continue
        all_setups = detect_setups(bars, setup_type)
        sigs = _filter_by_session(all_setups, session)
        if len(sigs) < 10:
            continue
        cfg = BacktestConfig(
            tp_atr_mult=tp_mult, sl_atr_mult=sl_mult,
            session_end_hour_utc=_session_end_hour(session),
            friction_r=_friction_for(symbol),
        )
        trades = run_backtest(sigs, bars, setup_type, cfg, symbol)
        if len(trades) < 20:
            continue
        wf = walk_forward_wr(trades, WF_IS_MONTHS, WF_OOS_MONTHS)
        mc = monte_carlo_ruin(trades, risk_pct=0.02, initial_balance=10_000)
        decay = decay_slope_ratio(trades, last_months=6)
        if wf < PC_MIN_WF_RATIO or mc > PC_MAX_MC_RUIN or decay < PC_MIN_DECAY:
            continue
        m = compute_metrics(trades)
        final_rows.append({
            "symbol": symbol, "tf": TF, "session": session,
            "setup_type": setup_type,
            "tp_atr_mult": tp_mult, "sl_atr_mult": sl_mult,
            "n_trades": m.n_trades, "wr": m.wr, "pf": m.profit_factor,
            "expectancy_r": m.expectancy_r, "max_dd_r": m.max_dd_r,
            "trades_per_year": m.trades_per_year,
            "wf_ratio": wf, "mc_ruin": mc, "decay_ratio": decay,
        })

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    if not final_rows:
        print("[FADE-PhaseC] 0 passed robustness gates.")
        _write_empty_final()
        return pl.DataFrame()

    final = pl.DataFrame(final_rows).sort("expectancy_r", descending=True)
    (REPORTS_DIR / "Math_Fade_Final.md").write_text(_render_final_md(final), encoding="utf-8")
    _export_json(final, REPORTS_DIR / "math_fade_strategies.json")
    print(f"[FADE-PhaseC] {len(final)} passed ALL gates")
    for r in final.head(10).iter_rows(named=True):
        print(f"  {r['symbol']:8s} {r['session']:9s} {r['setup_type']:22s} "
              f"TP={r['tp_atr_mult']} SL={r['sl_atr_mult']} "
              f"WR={r['wr']:.3f} PF={r['pf']:.2f} Exp={r['expectancy_r']:.3f}R")
    return final


def _render_final_md(final: pl.DataFrame) -> str:
    lines = [
        "# Math FADE — Final Strategies", "",
        f"- Passed ALL gates (WF/MC/decay): **{len(final)}**",
        f"- Gates: WF>={PC_MIN_WF_RATIO}, MC<={PC_MAX_MC_RUIN}, decay>={PC_MIN_DECAY}",
        "",
        "| Symbol | Session | Setup | TP | SL | Trades | WR | PF | Exp(R) | T/yr | WF | MC | Decay |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in final.iter_rows(named=True):
        lines.append(
            f"| {r['symbol']} | {r['session']} | {r['setup_type']} "
            f"| {r['tp_atr_mult']} | {r['sl_atr_mult']} "
            f"| {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.2f} "
            f"| {r['expectancy_r']:.3f} | {r['trades_per_year']:.1f} "
            f"| {r['wf_ratio']:.2f} | {r['mc_ruin']:.3f} | {r['decay_ratio']:.2f} |"
        )
    return "\n".join(lines) + "\n"


def _export_json(final: pl.DataFrame, path: Path) -> None:
    import json
    records = []
    for r in final.iter_rows(named=True):
        records.append({
            "symbol": r["symbol"], "tf": r["tf"], "session": r["session"],
            "setup_type": r["setup_type"],
            "tp_atr_mult": float(r["tp_atr_mult"]),
            "sl_atr_mult": float(r["sl_atr_mult"]),
            "metrics": {
                "n_trades": int(r["n_trades"]),
                "wr": float(r["wr"]),
                "pf": float(r["pf"]),
                "expectancy_r": float(r["expectancy_r"]),
                "max_dd_r": float(r["max_dd_r"]),
                "trades_per_year": float(r["trades_per_year"]),
                "wf_ratio": float(r["wf_ratio"]),
                "mc_ruin": float(r["mc_ruin"]),
                "decay_ratio": float(r["decay_ratio"]),
            },
        })
    path.write_text(json.dumps(records, indent=2), encoding="utf-8")


def _write_empty_final() -> None:
    (REPORTS_DIR / "Math_Fade_Final.md").write_text(
        "# Math FADE Final\n\nNo strategies passed all gates.\n", encoding="utf-8")
    (REPORTS_DIR / "math_fade_strategies.json").write_text("[]", encoding="utf-8")


# ── Entry point ──────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(description="Math FADE discovery pipeline (M15)")
    ap.add_argument("--phase", choices=("a", "b", "c", "all"), default="all")
    args = ap.parse_args()

    if args.phase in ("a", "all"):
        run_phase_a()
    if args.phase in ("b", "all"):
        run_phase_b()
    if args.phase in ("c", "all"):
        run_phase_c()


if __name__ == "__main__":
    main()
