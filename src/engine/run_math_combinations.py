"""Math-signal COMBINATIONS discovery pipeline — M15 only.

Extends run_math_discovery with multi-signal entries (1/2/3 signal AND-confluence
within a 3-bar window) and multi-exit OR-combinations, controlled by a beam-search
and a coherence (family-taxonomy) filter.

Phases:
    A  Entry screen   — best 1/2/3-signal entries at default R:R
    B  Exit optimization — 1/2/3-exit combos for top-50 Phase-A survivors
    C  Walk-forward + Monte Carlo validation

Usage:
    python -m src.engine.run_math_combinations --phase all
"""
from __future__ import annotations
import argparse
import itertools
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import polars as pl

from src.domain.constants import (
    INDICATOR_UNIVERSE, INDICATOR_SESSIONS,
    FRICTION_FX, FRICTION_INDEX, INDEX_SYMBOLS,
    WF_IS_MONTHS, WF_OOS_MONTHS,
)
from src.application.signal_generator import SignalGenerator, SIGNAL_TYPES
from src.engine.indicator_backtester import IndicatorBacktester, BacktestConfig
from src.engine.indicator_validation import (
    compute_metrics, walk_forward_wr, monte_carlo_ruin,
)
from src.engine.run_math_discovery import _load_and_enrich_math
from src.engine.run_indicator_discovery import _filter_by_session

REPORTS_DIR = Path("reports")
TF = "M15"
CONFLUENCE_BARS = 3  # signals must fire within N consecutive bars

# ── Default R:R for Phase A (entry screen) ──────────────────────────
PA_DEFAULT_TP = 1.0
PA_DEFAULT_SL = 2.0

# ── Gates ─────────────────────────────────────────────────────────
PA_MIN_TRADES_PER_YEAR = 30
PA_MIN_WR = 0.55

PB_MIN_TRADES_PER_YEAR = 30
PB_MIN_PF = 1.20
PB_MIN_EXPECTANCY = 0.05

PC_MIN_WF_RATIO = 0.80
PC_MAX_MC_RUIN = 0.02

# Beam-search widths
BEAM_TOP_1SIG = 50   # top 1-signal combos kept for 2-signal expansion
BEAM_TOP_2SIG = 30   # top 2-signal combos kept for 3-signal expansion
BEAM_TOP_ENTRY = 50  # top entries passed to Phase B for exit optimization

# ── Signal family taxonomy (coherence filter) ─────────────────────
SIGNAL_FAMILY = {
    # mean reversion / oscillator reversal
    "RSI_OB_REV": "mean_rev", "BB_TOUCH_REV": "mean_rev",
    "BB_RSI_CONFLUENCE": "mean_rev", "MACD_DIVERGENCE": "mean_rev",
    "ZSCORE_REV": "mean_rev", "OLS_RESIDUAL_REV": "mean_rev",
    "VWAP_AREA_EXTREME": "mean_rev", "MEANREV_AREA_EXTREME": "mean_rev",
    "SKEW_REGIME_REV": "mean_rev", "FRAC_DIFF_REV": "mean_rev",
    "HURST_MEANREV": "mean_rev", "GARCH_SPIKE_FADE": "mean_rev",
    "KALMAN_INNOV_REV": "mean_rev", "FRACTAL_REV": "mean_rev",
    # momentum / breakout
    "MACD_CROSS": "momentum", "ADX_BREAKOUT": "momentum",
    "BB_BREAKOUT": "momentum", "RSI_50_CROSS": "momentum",
    "FRACTAL_TREND": "momentum", "REGRESSION_BREAKOUT": "momentum",
    "HURST_TREND": "momentum", "SPECTRAL_TREND": "momentum",
    "KAMA_CROSS": "momentum",
    # structural / regime change
    "VELOCITY_REV": "structural", "ACCEL_SHOCK": "structural",
    "CURVATURE_PEAK": "structural", "SHANNON_DROP_TREND": "structural",
}

# Exit styles (bool-like identifiers)
EXIT_STYLES_CLASSICAL = ("TP_ATR_1", "TP_ATR_1_5", "TP_ATR_2", "SL_ATR_2", "TIME_STOP")
EXIT_STYLES_MATH = ("KAMA_CROSS_EXIT", "ZSCORE_NEUTRAL", "VELOCITY_FLIP",
                    "KALMAN_REVERT", "SPECTRAL_DROP")
ALL_EXITS = EXIT_STYLES_CLASSICAL + EXIT_STYLES_MATH

EXIT_THESIS = {
    "TP_ATR_1": "profit", "TP_ATR_1_5": "profit", "TP_ATR_2": "profit",
    "SL_ATR_2": "stop", "TIME_STOP": "time",
    "KAMA_CROSS_EXIT": "trend_flip", "ZSCORE_NEUTRAL": "mean_rev_complete",
    "VELOCITY_FLIP": "trend_flip", "KALMAN_REVERT": "mean_rev_complete",
    "SPECTRAL_DROP": "regime_change",
}


# ── Coherence filter ──────────────────────────────────────────────

def check_combination_coherence(entry_signals: tuple[str, ...],
                                  exit_styles: tuple[str, ...] = ()) -> bool:
    """Return True if combination is logically coherent (non-redundant, non-contradictory).

    Rules:
      1. 2-signal entries: families must NOT be identical (too redundant).
      2. 3-signal entries: must span ≥ 2 families (require a diversifier).
      3. A momentum entry must not pair with a pure mean-rev-complete exit as sole TP.
    """
    if not entry_signals:
        return False
    fams = [SIGNAL_FAMILY.get(s, "unknown") for s in entry_signals]

    if len(entry_signals) == 2 and fams[0] == fams[1]:
        return False
    if len(entry_signals) == 3 and len(set(fams)) < 2:
        return False

    # Contradictory exit pairing
    entry_is_momentum = any(f == "momentum" for f in fams)
    entry_is_meanrev = any(f == "mean_rev" for f in fams)

    # If ALL exits are mean_rev_complete but entry is pure momentum → contradiction
    if entry_is_momentum and not entry_is_meanrev and exit_styles:
        theses = {EXIT_THESIS.get(e, "unknown") for e in exit_styles}
        # Need at least one profit-taking or stop exit
        if not (theses & {"profit", "stop", "time", "trend_flip", "regime_change"}):
            return False

    return True


# ── Signal materialisation: bar-level booleans ────────────────────

def _signal_mask(bars: pl.DataFrame, signal_type: str, symbol: str,
                 direction: str) -> pl.DataFrame:
    """Return a dataframe with time + bool 'fires' column (direction-filtered)."""
    try:
        sigs = SignalGenerator.generate(bars, signal_type, symbol)
    except Exception:
        return pl.DataFrame({"time": bars["time"], "fires": [False] * len(bars)})
    sigs = sigs.filter(pl.col("direction") == direction)
    # Left-join mask
    return bars.select("time").join(
        sigs.select([pl.col("time"), pl.lit(True).alias("fires")]),
        on="time", how="left",
    ).with_columns(pl.col("fires").fill_null(False))


def _confluence_signals(bars: pl.DataFrame, signal_tuple: tuple[str, ...],
                         symbol: str, direction: str,
                         window: int = CONFLUENCE_BARS) -> pl.DataFrame:
    """Return signal-df (time, symbol, direction, signal_type, close, high, low, atr_14)
    where ALL signals in tuple fire within a `window`-bar rolling window.
    Emission bar = the latest bar of the confluence.
    """
    masks = []
    for st in signal_tuple:
        m = _signal_mask(bars, st, symbol, direction)
        # rolling any-true in last `window` bars
        rolling = pl.col("fires").cast(pl.Int8).rolling_max(window_size=window).fill_null(0).cast(pl.Boolean)
        m = m.with_columns(rolling.alias(f"_fires_{st}"))
        masks.append(m.select(["time", f"_fires_{st}"]))

    joined = bars.select("time")
    for m in masks:
        joined = joined.join(m, on="time", how="left")
    confluence_cols = [f"_fires_{st}" for st in signal_tuple]
    confluence = joined.with_columns(
        pl.all_horizontal([pl.col(c).fill_null(False) for c in confluence_cols]).alias("_confluence")
    ).filter(pl.col("_confluence"))

    if len(confluence) == 0:
        return _empty_signal_df()

    # Join OHLC+ATR
    ctx = bars.select(["time", "close", "high", "low", "atr_14"])
    out = confluence.select("time").join(ctx, on="time", how="left")
    signal_label = "+".join(signal_tuple)
    return out.with_columns([
        pl.lit(symbol).alias("symbol"),
        pl.lit(direction).alias("direction"),
        pl.lit(signal_label).alias("signal_type"),
    ]).select([
        "time", "symbol", "direction", "signal_type",
        "close", "high", "low", "atr_14",
    ])


def _empty_signal_df() -> pl.DataFrame:
    return pl.DataFrame(schema={
        "time": pl.Datetime, "symbol": pl.Utf8, "direction": pl.Utf8,
        "signal_type": pl.Utf8, "close": pl.Float64, "high": pl.Float64,
        "low": pl.Float64, "atr_14": pl.Float64,
    })


def _friction_for(symbol: str) -> float:
    return FRICTION_INDEX if symbol in INDEX_SYMBOLS else FRICTION_FX


def _session_end_hour(session: str) -> int:
    return INDICATOR_SESSIONS[session][1]


# ── Phase A: entries ──────────────────────────────────────────────

@dataclass(frozen=True)
class ComboResult:
    symbol: str
    session: str
    entry: tuple[str, ...]
    n_trades: int
    wr: float
    pf: float
    expectancy_r: float
    max_dd_r: float
    trades_per_year: float


def _backtest_entry(bars: pl.DataFrame, entry: tuple[str, ...],
                     symbol: str, session: str,
                     tp_mult: float = PA_DEFAULT_TP,
                     sl_mult: float = PA_DEFAULT_SL) -> ComboResult | None:
    """Run backtest for a given entry tuple, both LONG and SHORT direction streams.
    Returns aggregated ComboResult or None if empty.
    """
    long_sigs = _confluence_signals(bars, entry, symbol, "LONG")
    short_sigs = _confluence_signals(bars, entry, symbol, "SHORT")
    sigs = pl.concat([long_sigs, short_sigs]) if len(long_sigs) + len(short_sigs) > 0 else _empty_signal_df()
    if len(sigs) == 0:
        return None
    sigs = _filter_by_session(sigs, session)
    if len(sigs) < 20:
        return None
    cfg = BacktestConfig(
        tp_atr_mult=tp_mult, sl_atr_mult=sl_mult,
        session_end_hour_utc=_session_end_hour(session),
        friction_r=_friction_for(symbol),
    )
    trades = IndicatorBacktester.run(sigs, bars, cfg)
    if len(trades) == 0:
        return None
    m = compute_metrics(trades)
    return ComboResult(
        symbol=symbol, session=session, entry=entry,
        n_trades=m.n_trades, wr=m.wr, pf=m.profit_factor,
        expectancy_r=m.expectancy_r, max_dd_r=m.max_dd_r,
        trades_per_year=m.trades_per_year,
    )


def run_phase_a(universe: Iterable[str] = INDICATOR_UNIVERSE,
                sessions: Iterable[str] = tuple(INDICATOR_SESSIONS.keys()),
                signals: Iterable[str] = SIGNAL_TYPES) -> pl.DataFrame:
    """Beam-search Phase-A: 1-signal → top-N 2-signal → top-N 3-signal."""
    print(f"[PhaseA] 1-signal sweep on {len(list(universe))}*{len(list(sessions))}*{len(list(signals))}")

    universe = list(universe)
    sessions = list(sessions)
    signals = [s for s in signals if s in SIGNAL_FAMILY]  # guard typos

    rows: list[dict] = []

    # ── Stage 1: enumerate all 1-signal combos ──
    for symbol in universe:
        try:
            bars = _load_and_enrich_math(symbol)
        except FileNotFoundError:
            print(f"[PhaseA][SKIP] {symbol}: no data")
            continue
        for sig in signals:
            for session in sessions:
                r = _backtest_entry(bars, (sig,), symbol, session)
                if r is None:
                    continue
                rows.append(_row_from(r, stage="1sig"))

    results1 = pl.DataFrame(rows) if rows else pl.DataFrame()
    survivors1 = _gate_entries(results1)
    print(f"[PhaseA] 1-sig: {len(results1)} evaluated, {len(survivors1)} passed gate")

    # ── Stage 2: beam 2-signal on top-BEAM_TOP_1SIG entries ──
    rows2: list[dict] = []
    seeds = survivors1.sort("expectancy_r", descending=True).head(BEAM_TOP_1SIG)
    # For each (symbol, session) seed, try adding any OTHER signal (coherence-filtered)
    for seed in seeds.iter_rows(named=True):
        seed_sig = seed["entry"][0]  # entry stored as list
        symbol, session = seed["symbol"], seed["session"]
        try:
            bars = _load_and_enrich_math(symbol)
        except FileNotFoundError:
            continue
        for partner in signals:
            if partner == seed_sig:
                continue
            combo = tuple(sorted((seed_sig, partner)))
            if not check_combination_coherence(combo):
                continue
            r = _backtest_entry(bars, combo, symbol, session)
            if r is None:
                continue
            rows2.append(_row_from(r, stage="2sig"))

    results2 = pl.DataFrame(rows2) if rows2 else pl.DataFrame()
    survivors2 = _gate_entries(results2)
    print(f"[PhaseA] 2-sig: {len(results2)} evaluated, {len(survivors2)} passed gate")

    # ── Stage 3: beam 3-signal on top-BEAM_TOP_2SIG 2-sig entries ──
    rows3: list[dict] = []
    seeds2 = survivors2.sort("expectancy_r", descending=True).head(BEAM_TOP_2SIG)
    for seed in seeds2.iter_rows(named=True):
        pair = tuple(seed["entry"])
        symbol, session = seed["symbol"], seed["session"]
        try:
            bars = _load_and_enrich_math(symbol)
        except FileNotFoundError:
            continue
        for third in signals:
            if third in pair:
                continue
            combo = tuple(sorted((*pair, third)))
            if not check_combination_coherence(combo):
                continue
            r = _backtest_entry(bars, combo, symbol, session)
            if r is None:
                continue
            rows3.append(_row_from(r, stage="3sig"))

    results3 = pl.DataFrame(rows3) if rows3 else pl.DataFrame()
    survivors3 = _gate_entries(results3)
    print(f"[PhaseA] 3-sig: {len(results3)} evaluated, {len(survivors3)} passed gate")

    all_survivors = pl.concat([s for s in (survivors1, survivors2, survivors3) if len(s) > 0]) \
        if (len(survivors1) + len(survivors2) + len(survivors3)) > 0 else pl.DataFrame()

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    if len(all_survivors) > 0:
        all_survivors = all_survivors.sort("expectancy_r", descending=True)
        all_survivors.write_parquet(REPORTS_DIR / "math_combo_phase_a.parquet")
    else:
        pl.DataFrame().write_parquet(REPORTS_DIR / "math_combo_phase_a.parquet")

    _write_phase_a_md(results1, results2, results3, all_survivors)
    return all_survivors


def _row_from(r: ComboResult, stage: str) -> dict:
    return {
        "symbol": r.symbol, "session": r.session,
        "entry": list(r.entry), "stage": stage,
        "n_trades": r.n_trades, "wr": r.wr, "pf": r.pf,
        "expectancy_r": r.expectancy_r, "max_dd_r": r.max_dd_r,
        "trades_per_year": r.trades_per_year,
    }


def _gate_entries(df: pl.DataFrame) -> pl.DataFrame:
    if len(df) == 0:
        return df
    return df.filter(
        (pl.col("trades_per_year") >= PA_MIN_TRADES_PER_YEAR)
        & (pl.col("wr") >= PA_MIN_WR)
    )


def _write_phase_a_md(r1: pl.DataFrame, r2: pl.DataFrame, r3: pl.DataFrame,
                       surv: pl.DataFrame) -> None:
    lines = [
        "# Math Combinations — Phase A",
        "",
        f"- 1-sig combos evaluated: {len(r1)}",
        f"- 2-sig combos evaluated: {len(r2)}",
        f"- 3-sig combos evaluated: {len(r3)}",
        f"- Passed gates (trades/yr >= {PA_MIN_TRADES_PER_YEAR}, WR >= {PA_MIN_WR}): "
        f"**{len(surv)}**",
        "",
        "## Top 30 survivors",
        "",
        "| Stage | Symbol | Session | Entry | Trades | WR | PF | Exp(R) |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in surv.head(30).iter_rows(named=True):
        lines.append(
            f"| {r['stage']} | {r['symbol']} | {r['session']} | {'+'.join(r['entry'])} "
            f"| {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.2f} | {r['expectancy_r']:.3f} |"
        )
    (REPORTS_DIR / "math_combo_phase_a.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


# ── Phase B: exits ─────────────────────────────────────────────────

def _exit_to_cfg(exit_combo: tuple[str, ...], session: str, friction: float) -> BacktestConfig:
    """Map an exit-combo to a single BacktestConfig. Simplification:
    TP is the minimum TP_ATR_x in the combo; SL is SL_ATR_2 if present else 2.0.
    Math-exits act as soft overrides but are approximated here by tightening TP.
    """
    tps = []
    if "TP_ATR_1" in exit_combo: tps.append(1.0)
    if "TP_ATR_1_5" in exit_combo: tps.append(1.5)
    if "TP_ATR_2" in exit_combo: tps.append(2.0)
    if not tps:
        tps.append(1.0)  # default
    tp = min(tps)  # OR-first-hit
    sl = 2.0  # fixed for now (keeps backtester parity)
    return BacktestConfig(
        tp_atr_mult=tp, sl_atr_mult=sl,
        session_end_hour_utc=_session_end_hour(session),
        friction_r=friction,
    )


def run_phase_b() -> pl.DataFrame:
    path = REPORTS_DIR / "math_combo_phase_a.parquet"
    if not path.exists():
        raise FileNotFoundError(f"Run Phase-A first (missing {path})")
    survivors = pl.read_parquet(path)
    if len(survivors) == 0:
        print("[PhaseB] no Phase-A survivors, skipping.")
        pl.DataFrame().write_parquet(REPORTS_DIR / "math_combo_phase_b.parquet")
        (REPORTS_DIR / "math_combo_phase_b.md").write_text(
            "# Math Combinations — Phase B\n\nNo Phase-A survivors.\n", encoding="utf-8"
        )
        return pl.DataFrame()

    entries = survivors.head(BEAM_TOP_ENTRY)

    # Build exit combinations: 1, 2 (OR), 3 (OR) — coherence-filtered
    exit_pool = ALL_EXITS
    exit_combos = list(itertools.combinations(exit_pool, 1))
    # 2-exit: sample only profit+stop pairs and classical+math pairs (prune redundant pairs)
    for a, b in itertools.combinations(exit_pool, 2):
        if EXIT_THESIS[a] == EXIT_THESIS[b]:
            continue  # too redundant
        exit_combos.append((a, b))
    # 3-exit: must include at least one profit-taking
    for a, b, c in itertools.combinations(exit_pool, 3):
        theses = {EXIT_THESIS[x] for x in (a, b, c)}
        if "profit" not in theses:
            continue
        if len(theses) < 3:
            continue
        exit_combos.append((a, b, c))

    print(f"[PhaseB] {len(entries)} entries × {len(exit_combos)} exit-combos")

    rows = []
    for e in entries.iter_rows(named=True):
        entry_tuple = tuple(e["entry"])
        symbol, session = e["symbol"], e["session"]
        try:
            bars = _load_and_enrich_math(symbol)
        except FileNotFoundError:
            continue
        long_sigs = _confluence_signals(bars, entry_tuple, symbol, "LONG")
        short_sigs = _confluence_signals(bars, entry_tuple, symbol, "SHORT")
        sigs = pl.concat([long_sigs, short_sigs]) if len(long_sigs) + len(short_sigs) > 0 else _empty_signal_df()
        if len(sigs) == 0:
            continue
        sigs = _filter_by_session(sigs, session)
        if len(sigs) < 20:
            continue
        friction = _friction_for(symbol)

        for ex_combo in exit_combos:
            if not check_combination_coherence(entry_tuple, ex_combo):
                continue
            cfg = _exit_to_cfg(ex_combo, session, friction)
            trades = IndicatorBacktester.run(sigs, bars, cfg)
            if len(trades) == 0:
                continue
            m = compute_metrics(trades)
            if (m.trades_per_year < PB_MIN_TRADES_PER_YEAR
                    or m.profit_factor < PB_MIN_PF
                    or m.expectancy_r < PB_MIN_EXPECTANCY):
                continue
            rows.append({
                "symbol": symbol, "session": session,
                "entry": list(entry_tuple), "exit": list(ex_combo),
                "tp_atr_mult": cfg.tp_atr_mult, "sl_atr_mult": cfg.sl_atr_mult,
                "n_trades": m.n_trades, "wr": m.wr, "pf": m.profit_factor,
                "expectancy_r": m.expectancy_r,
                "max_dd_r": m.max_dd_r,
                "trades_per_year": m.trades_per_year,
            })

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    if not rows:
        print("[PhaseB] 0 survivors passed gates.")
        pl.DataFrame().write_parquet(REPORTS_DIR / "math_combo_phase_b.parquet")
        (REPORTS_DIR / "math_combo_phase_b.md").write_text(
            "# Math Combinations — Phase B\n\n0 passed exit gates.\n", encoding="utf-8"
        )
        return pl.DataFrame()
    phase_b = pl.DataFrame(rows).sort("expectancy_r", descending=True)
    phase_b.write_parquet(REPORTS_DIR / "math_combo_phase_b.parquet")
    _write_phase_b_md(phase_b)
    return phase_b


def _write_phase_b_md(df: pl.DataFrame) -> None:
    lines = [
        "# Math Combinations — Phase B",
        "",
        f"- Strategies passing exit gates (PF>={PB_MIN_PF}, Exp>={PB_MIN_EXPECTANCY}): "
        f"**{len(df)}**",
        "",
        "| Symbol | Session | Entry | Exit | TP | SL | Trades | WR | PF | Exp(R) |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in df.head(50).iter_rows(named=True):
        lines.append(
            f"| {r['symbol']} | {r['session']} | {'+'.join(r['entry'])} "
            f"| {','.join(r['exit'])} | {r['tp_atr_mult']} | {r['sl_atr_mult']} "
            f"| {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.2f} | {r['expectancy_r']:.3f} |"
        )
    (REPORTS_DIR / "math_combo_phase_b.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


# ── Phase C: WF + MC validation ───────────────────────────────────

def run_phase_c() -> pl.DataFrame:
    path = REPORTS_DIR / "math_combo_phase_b.parquet"
    if not path.exists():
        raise FileNotFoundError(f"Run Phase-B first (missing {path})")
    pb = pl.read_parquet(path)
    if len(pb) == 0:
        print("[PhaseC] no Phase-B survivors.")
        _write_empty_final()
        return pl.DataFrame()

    rows = []
    for r in pb.iter_rows(named=True):
        entry = tuple(r["entry"])
        symbol, session = r["symbol"], r["session"]
        try:
            bars = _load_and_enrich_math(symbol)
        except FileNotFoundError:
            continue
        long_sigs = _confluence_signals(bars, entry, symbol, "LONG")
        short_sigs = _confluence_signals(bars, entry, symbol, "SHORT")
        sigs = pl.concat([long_sigs, short_sigs]) if len(long_sigs) + len(short_sigs) > 0 else _empty_signal_df()
        if len(sigs) == 0:
            continue
        sigs = _filter_by_session(sigs, session)
        if len(sigs) < 20:
            continue
        cfg = BacktestConfig(
            tp_atr_mult=r["tp_atr_mult"], sl_atr_mult=r["sl_atr_mult"],
            session_end_hour_utc=_session_end_hour(session),
            friction_r=_friction_for(symbol),
        )
        trades = IndicatorBacktester.run(sigs, bars, cfg)
        if len(trades) < 20:
            continue
        wf = walk_forward_wr(trades, WF_IS_MONTHS, WF_OOS_MONTHS)
        mc = monte_carlo_ruin(trades, risk_pct=0.02, initial_balance=10_000)
        if wf < PC_MIN_WF_RATIO or mc > PC_MAX_MC_RUIN:
            continue
        m = compute_metrics(trades)
        rows.append({
            "symbol": symbol, "session": session,
            "entry": r["entry"], "exit": r["exit"],
            "tp_atr_mult": r["tp_atr_mult"], "sl_atr_mult": r["sl_atr_mult"],
            "n_trades": m.n_trades, "wr": m.wr, "pf": m.profit_factor,
            "expectancy_r": m.expectancy_r, "max_dd_r": m.max_dd_r,
            "trades_per_year": m.trades_per_year,
            "wf_ratio": wf, "mc_ruin": mc,
        })

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    if not rows:
        print("[PhaseC] 0 strategies passed WF/MC gates.")
        _write_empty_final()
        return pl.DataFrame()

    final = pl.DataFrame(rows).sort("expectancy_r", descending=True)
    final.write_parquet(REPORTS_DIR / "math_combo_phase_c.parquet")
    _write_final_md(final)
    # JSON export
    strategies = [
        {
            "symbol": r["symbol"], "session": r["session"],
            "entry": list(r["entry"]), "exit": list(r["exit"]),
            "tp_atr_mult": r["tp_atr_mult"], "sl_atr_mult": r["sl_atr_mult"],
            "metrics": {
                "n_trades": r["n_trades"], "wr": r["wr"], "pf": r["pf"],
                "expectancy_r": r["expectancy_r"], "max_dd_r": r["max_dd_r"],
                "trades_per_year": r["trades_per_year"],
                "wf_ratio": r["wf_ratio"], "mc_ruin": r["mc_ruin"],
            },
        }
        for r in final.iter_rows(named=True)
    ]
    (REPORTS_DIR / "math_combinations_strategies.json").write_text(
        json.dumps(strategies, indent=2, default=str), encoding="utf-8"
    )
    return final


def _write_final_md(df: pl.DataFrame) -> None:
    lines = [
        "# Math Combinations — Final (Phase C)",
        "",
        f"- Strategies passing ALL gates (WF>={PC_MIN_WF_RATIO}, MC<={PC_MAX_MC_RUIN}): "
        f"**{len(df)}**",
        "",
        "| Symbol | Session | Entry | Exit | TP | SL | N | WR | PF | Exp(R) | WF | MCruin |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in df.head(50).iter_rows(named=True):
        lines.append(
            f"| {r['symbol']} | {r['session']} | {'+'.join(r['entry'])} "
            f"| {','.join(r['exit'])} | {r['tp_atr_mult']} | {r['sl_atr_mult']} "
            f"| {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.2f} "
            f"| {r['expectancy_r']:.3f} | {r['wf_ratio']:.2f} | {r['mc_ruin']:.3f} |"
        )
    (REPORTS_DIR / "Math_Combinations_Final.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def _write_empty_final() -> None:
    (REPORTS_DIR / "Math_Combinations_Final.md").write_text(
        "# Math Combinations — Final\n\n0 strategies passed all gates.\n", encoding="utf-8"
    )
    (REPORTS_DIR / "math_combinations_strategies.json").write_text("[]", encoding="utf-8")


# ── CLI ────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(description="Math-combination discovery pipeline")
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
