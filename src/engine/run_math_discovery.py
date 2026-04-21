"""Math-indicator edge discovery pipeline — M15 only.

Phase A: Raw edge screen (full history, fixed 2×ATR TP / 1×ATR SL)
Phase B: R:R management grid for Phase-A survivors
Phase C: Full robustness validation (WF / MC / decay)

Usage:
    python -m src.engine.run_math_discovery --phase a
    python -m src.engine.run_math_discovery --phase b
    python -m src.engine.run_math_discovery --phase c
    python -m src.engine.run_math_discovery --phase all   (default)
"""
from __future__ import annotations
import argparse
from pathlib import Path
import polars as pl

from src.domain.constants import (
    INDICATOR_UNIVERSE, INDICATOR_SESSIONS,
    INDICATOR_TP_ATR_GRID, INDICATOR_SL_ATR_GRID,
    FRICTION_FX, FRICTION_INDEX, INDEX_SYMBOLS,
    WF_IS_MONTHS, WF_OOS_MONTHS,
)
from src.application.math_indicators import MathIndicatorEnricher
from src.application.signal_generator import SignalGenerator

# Math signal types only (the 10 new ones)
MATH_SIGNAL_TYPES = (
    "ZSCORE_REV", "VELOCITY_REV", "ACCEL_SHOCK", "KALMAN_INNOV_REV", "OLS_RESIDUAL_REV",
    "CURVATURE_PEAK", "VWAP_AREA_EXTREME", "MEANREV_AREA_EXTREME", "REGRESSION_BREAKOUT",
    "SKEW_REGIME_REV",
)

from src.engine.indicator_backtester import IndicatorBacktester, BacktestConfig
from src.engine.indicator_validation import (
    compute_metrics, walk_forward_wr, monte_carlo_ruin, decay_slope_ratio,
)
from src.engine.indicator_reporter import render_final_report, export_strategies_json
from src.engine.run_indicator_discovery import _load_and_enrich, _filter_by_session

REPORTS_DIR = Path("reports")
MATH_CACHE = Path("data/enriched_math")

TF = "M15"

# Phase-A gates — very loose pass-through to Phase B for R:R tuning.
# Default R:R is now in user's target range (tight TP, wide SL): TP=1.0 ATR, SL=2.0 ATR.
# With that profile we expect WR>=55% baseline; gate only needs enough trades.
PA_DEFAULT_TP = 1.0
PA_DEFAULT_SL = 2.0
PA_MIN_TRADES_PER_YEAR = 30
PA_MIN_WR = 0.0    # pass-through — Phase-B R:R sweep determines WR
PA_MIN_PF = 0.0    # pass-through
PA_MIN_EXPECTANCY = -999.0  # pass-through

# Phase-B gates — user's target profile (high WR via tight TP + wide SL)
PB_MIN_TRADES_PER_YEAR = 30
PB_MIN_WR = 0.80
PB_MIN_PF = 1.20
PB_MIN_EXPECTANCY = 0.0  # implied by WR/PF combo; don't double-gate
PB_MAX_DD_R = 30.0

# Phase-B R:R grid — user-specified range: TP min 0.5, SL max 2.5
PB_TP_GRID = (0.3, 0.4, 0.5, 0.6, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5)
PB_SL_GRID = (0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5)

# Phase-C gates (strict) — decay removed (kills too much in current regime,
# not strictly statistical ruin). WF + MC are the hard gates.
PC_MIN_WF_RATIO = 0.80
PC_MAX_MC_RUIN = 0.02


def _friction_for(symbol: str) -> float:
    return FRICTION_INDEX if symbol in INDEX_SYMBOLS else FRICTION_FX


def _session_end_hour(session: str) -> int:
    return INDICATOR_SESSIONS[session][1]


def _load_and_enrich_math(symbol: str) -> pl.DataFrame:
    """Load, enrich with IndicatorEnricher + MathIndicatorEnricher. Cache to enriched_math."""
    cache_path = MATH_CACHE / f"{symbol}_{TF}.parquet"
    if cache_path.exists():
        return pl.read_parquet(cache_path)
    MATH_CACHE.mkdir(parents=True, exist_ok=True)
    bars = _load_and_enrich(symbol, TF)  # base enriched (IndicatorEnricher + ATR)
    bars = MathIndicatorEnricher.enrich_all_math(bars)
    bars.write_parquet(cache_path)
    return bars


# ─── Phase A ──────────────────────────────────────────────────────────────────

def run_phase_a() -> pl.DataFrame:
    total = len(INDICATOR_UNIVERSE) * len(INDICATOR_SESSIONS) * len(MATH_SIGNAL_TYPES)
    print(f"[PhaseA] {total} combos  ({len(INDICATOR_UNIVERSE)} assets × "
          f"{len(INDICATOR_SESSIONS)} sessions × {len(MATH_SIGNAL_TYPES)} signals)")

    rows = []
    i = 0
    for symbol in INDICATOR_UNIVERSE:
        try:
            bars = _load_and_enrich_math(symbol)
        except FileNotFoundError:
            print(f"[PhaseA][SKIP] {symbol}: no data file")
            continue
        friction = _friction_for(symbol)
        for signal_type in MATH_SIGNAL_TYPES:
            # Check required columns exist (math columns may be absent if enrich failed)
            try:
                raw_signals = SignalGenerator.generate(bars, signal_type, symbol)
            except Exception as exc:
                print(f"[PhaseA][SKIP] {symbol} {signal_type}: {exc}")
                continue
            for session in INDICATOR_SESSIONS:
                i += 1
                sigs = _filter_by_session(raw_signals, session)
                if len(sigs) < 20:
                    continue
                cfg = BacktestConfig(
                    tp_atr_mult=PA_DEFAULT_TP,
                    sl_atr_mult=PA_DEFAULT_SL,
                    session_end_hour_utc=_session_end_hour(session),
                    friction_r=friction,
                )
                trades = IndicatorBacktester.run(sigs, bars, cfg)
                if len(trades) == 0:
                    continue
                m = compute_metrics(trades)
                rows.append({
                    "symbol": symbol, "tf": TF, "session": session,
                    "signal_type": signal_type,
                    "n_trades": m.n_trades,
                    "wr": m.wr, "pf": m.profit_factor,
                    "expectancy_r": m.expectancy_r,
                    "max_dd_r": m.max_dd_r,
                    "trades_per_year": m.trades_per_year,
                })
                if i % 100 == 0:
                    print(f"[PhaseA] {i}/{total} — {symbol}/{session}/{signal_type}")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    if not rows:
        print("[PhaseA] No results.")
        pl.DataFrame().write_parquet(REPORTS_DIR / "math_phase_a.parquet")
        (REPORTS_DIR / "math_phase_a.md").write_text(
            "# Math Discovery Phase A\n\nNo combos produced trades.\n", encoding="utf-8"
        )
        return pl.DataFrame()

    results = pl.DataFrame(rows)
    survivors = results.filter(
        (pl.col("trades_per_year") >= PA_MIN_TRADES_PER_YEAR)
        & (pl.col("wr") >= PA_MIN_WR)
        & (pl.col("pf") >= PA_MIN_PF)
        & (pl.col("expectancy_r") >= PA_MIN_EXPECTANCY)
    ).sort("expectancy_r", descending=True)

    results.write_parquet(REPORTS_DIR / "math_phase_a.parquet")
    survivors.write_parquet(REPORTS_DIR / "math_phase_a_survivors.parquet")
    (REPORTS_DIR / "math_phase_a.md").write_text(_render_phase_a_md(results, survivors), encoding="utf-8")
    print(f"[PhaseA] {len(results)} combos evaluated, {len(survivors)} passed gates")
    return survivors


def _render_phase_a_md(results: pl.DataFrame, survivors: pl.DataFrame) -> str:
    lines = [
        "# Math Discovery — Phase A Report",
        "",
        f"- Combos evaluated: **{len(results)}**",
        f"- Passed loose gates: **{len(survivors)}**",
        f"- Gates: trades/year >= {PA_MIN_TRADES_PER_YEAR}, WR >= {PA_MIN_WR}, "
        f"PF >= {PA_MIN_PF}, expectancy >= {PA_MIN_EXPECTANCY}R",
        "",
        "## Top 30 survivors (by expectancy)",
        "",
        "| Symbol | Session | Signal | Trades | WR | PF | Exp (R) | MaxDD (R) |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in survivors.head(30).iter_rows(named=True):
        lines.append(
            f"| {r['symbol']} | {r['session']} | {r['signal_type']} "
            f"| {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.2f} "
            f"| {r['expectancy_r']:.3f} | {r['max_dd_r']:.1f} |"
        )
    return "\n".join(lines) + "\n"


# ─── Phase B ──────────────────────────────────────────────────────────────────

def run_phase_b() -> pl.DataFrame:
    surv_path = REPORTS_DIR / "math_phase_a_survivors.parquet"
    if not surv_path.exists():
        raise FileNotFoundError(f"Run Phase-A first (missing {surv_path})")
    survivors = pl.read_parquet(surv_path)
    if len(survivors) == 0:
        print("[PhaseB] No Phase-A survivors — skipping.")
        pl.DataFrame().write_parquet(REPORTS_DIR / "math_phase_b.parquet")
        (REPORTS_DIR / "math_phase_b.md").write_text(
            "# Math Discovery Phase B\n\nNo Phase-A survivors.\n", encoding="utf-8"
        )
        return pl.DataFrame()

    rr_combos = [(tp, sl) for tp in PB_TP_GRID for sl in PB_SL_GRID]
    total = len(survivors) * len(rr_combos)
    print(f"[PhaseB] {len(survivors)} survivors × {len(rr_combos)} R:R combos = {total}")
    print(f"[PhaseB] gate: WR>={PB_MIN_WR}, PF>={PB_MIN_PF}, trades/yr>={PB_MIN_TRADES_PER_YEAR}")

    rows = []
    for surv in survivors.iter_rows(named=True):
        symbol, session, signal_type = surv["symbol"], surv["session"], surv["signal_type"]
        try:
            bars = _load_and_enrich_math(symbol)
        except FileNotFoundError:
            continue
        try:
            raw_signals = SignalGenerator.generate(bars, signal_type, symbol)
        except Exception:
            continue
        sigs = _filter_by_session(raw_signals, session)
        if len(sigs) < 20:
            continue
        friction = _friction_for(symbol)
        session_end = _session_end_hour(session)

        for tp_mult, sl_mult in rr_combos:
            cfg = BacktestConfig(
                tp_atr_mult=tp_mult, sl_atr_mult=sl_mult,
                session_end_hour_utc=session_end, friction_r=friction,
            )
            trades = IndicatorBacktester.run(sigs, bars, cfg)
            if len(trades) == 0:
                continue
            m = compute_metrics(trades)
            if (m.trades_per_year < PB_MIN_TRADES_PER_YEAR
                    or m.wr < PB_MIN_WR
                    or m.profit_factor < PB_MIN_PF
                    or m.max_dd_r > PB_MAX_DD_R):
                continue
            rows.append({
                "symbol": symbol, "tf": TF, "session": session,
                "signal_type": signal_type,
                "tp_atr_mult": tp_mult, "sl_atr_mult": sl_mult,
                "n_trades": m.n_trades, "wr": m.wr, "pf": m.profit_factor,
                "expectancy_r": m.expectancy_r,
                "max_dd_r": m.max_dd_r,
                "trades_per_year": m.trades_per_year,
            })

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    if not rows:
        print("[PhaseB] 0 survivors passed strict gates.")
        pl.DataFrame().write_parquet(REPORTS_DIR / "math_phase_b.parquet")
        (REPORTS_DIR / "math_phase_b.md").write_text(
            "# Math Discovery Phase B\n\n0 survivors passed R:R gates.\n", encoding="utf-8"
        )
        return pl.DataFrame()

    phase_b = pl.DataFrame(rows).sort("expectancy_r", descending=True)
    phase_b.write_parquet(REPORTS_DIR / "math_phase_b.parquet")
    (REPORTS_DIR / "math_phase_b.md").write_text(_render_phase_b_md(phase_b), encoding="utf-8")
    print(f"[PhaseB] {len(phase_b)} strategies passed R:R gates")
    return phase_b


def _render_phase_b_md(phase_b: pl.DataFrame) -> str:
    lines = [
        "# Math Discovery — Phase B Report",
        "",
        f"- Strategies passing R:R gates: **{len(phase_b)}**",
        f"- Gates: trades/year >= {PB_MIN_TRADES_PER_YEAR}, WR >= {PB_MIN_WR}, "
        f"PF >= {PB_MIN_PF}, expectancy >= {PB_MIN_EXPECTANCY}R, MaxDD <= {PB_MAX_DD_R}R",
        "",
        "## All Phase-B survivors (best R:R per combo)",
        "",
        "| Symbol | Session | Signal | TP*ATR | SL*ATR | Trades | WR | PF | Exp (R) | MaxDD (R) |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in phase_b.iter_rows(named=True):
        lines.append(
            f"| {r['symbol']} | {r['session']} | {r['signal_type']} "
            f"| {r['tp_atr_mult']} | {r['sl_atr_mult']} "
            f"| {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.2f} "
            f"| {r['expectancy_r']:.3f} | {r['max_dd_r']:.1f} |"
        )
    return "\n".join(lines) + "\n"


# ─── Phase C ──────────────────────────────────────────────────────────────────

def run_phase_c() -> pl.DataFrame:
    pb_path = REPORTS_DIR / "math_phase_b.parquet"
    if not pb_path.exists():
        raise FileNotFoundError(f"Run Phase-B first (missing {pb_path})")
    phase_b = pl.read_parquet(pb_path)
    if len(phase_b) == 0:
        print("[PhaseC] No Phase-B survivors — skipping.")
        _write_empty_final()
        return pl.DataFrame()

    print(f"[PhaseC] Validating {len(phase_b)} Phase-B survivors (WF / MC / decay)")
    final_rows = []

    for surv in phase_b.iter_rows(named=True):
        symbol, session, signal_type = surv["symbol"], surv["session"], surv["signal_type"]
        tp_mult, sl_mult = surv["tp_atr_mult"], surv["sl_atr_mult"]
        try:
            bars = _load_and_enrich_math(symbol)
        except FileNotFoundError:
            continue
        try:
            raw_signals = SignalGenerator.generate(bars, signal_type, symbol)
        except Exception:
            continue
        sigs = _filter_by_session(raw_signals, session)
        if len(sigs) < 20:
            continue
        cfg = BacktestConfig(
            tp_atr_mult=tp_mult, sl_atr_mult=sl_mult,
            session_end_hour_utc=_session_end_hour(session),
            friction_r=_friction_for(symbol),
        )
        trades = IndicatorBacktester.run(sigs, bars, cfg)
        if len(trades) < 20:
            continue

        wf = walk_forward_wr(trades, WF_IS_MONTHS, WF_OOS_MONTHS)
        mc = monte_carlo_ruin(trades, risk_pct=0.02, initial_balance=10_000)
        decay = decay_slope_ratio(trades, last_months=6)  # info only

        if wf < PC_MIN_WF_RATIO or mc > PC_MAX_MC_RUIN:
            continue

        m = compute_metrics(trades)
        final_rows.append({
            "symbol": symbol, "tf": TF, "session": session,
            "signal_type": signal_type,
            "filters": [],  # no confluence filters in math pipeline
            "tp_atr_mult": tp_mult, "sl_atr_mult": sl_mult,
            "n_trades": m.n_trades, "wr": m.wr, "pf": m.profit_factor,
            "expectancy_r": m.expectancy_r,
            "max_dd_r": m.max_dd_r,
            "trades_per_year": m.trades_per_year,
            "wf_ratio": wf, "mc_ruin": mc, "decay_ratio": decay,
        })

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    if not final_rows:
        print("[PhaseC] 0 strategies passed robustness gates.")
        _write_empty_final()
        return pl.DataFrame()

    final = pl.DataFrame(final_rows).sort("expectancy_r", descending=True)
    report_text = render_final_report(final)
    (REPORTS_DIR / "Math_Discovery_Final.md").write_text(report_text, encoding="utf-8")
    export_strategies_json(final, REPORTS_DIR / "math_strategies.json")
    print(f"[PhaseC] {len(final)} strategies passed ALL gates")
    print(final.select(["symbol", "session", "signal_type", "tp_atr_mult", "sl_atr_mult",
                        "wr", "pf", "expectancy_r"]).head(10))
    return final


def _write_empty_final() -> None:
    (REPORTS_DIR / "Math_Discovery_Final.md").write_text(
        "# Math Discovery Final\n\nNo strategies passed all gates.\n", encoding="utf-8"
    )
    (REPORTS_DIR / "math_strategies.json").write_text("[]", encoding="utf-8")


# ─── Entry point ──────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(description="Math-indicator edge discovery pipeline (M15 only)")
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
