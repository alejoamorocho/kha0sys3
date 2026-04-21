"""V2 discovery pipeline: fast 1-year full-grid screen then full-history validation.

Phase-1 (screen):
    For every (symbol, TF, session, signal_type) x (TP, SL) combo on the LAST YEAR
    of data, compute metrics. Gate: trades >= 60 AND WR >= 0.60. No confluence
    filters at this stage — pattern must stand on its own before layering filters.

Phase-2 (validate):
    For each Phase-1 winner, re-run on FULL history. Gate: WR >= 0.85,
    trades/year >= 60, expectancy > 0, MaxDD <= 20R, WF/MC/decay strict.

Usage:
    python -m src.engine.run_indicator_discovery_v2 --phase 1
    python -m src.engine.run_indicator_discovery_v2 --phase 2
    python -m src.engine.run_indicator_discovery_v2 --phase all
"""
from __future__ import annotations
import argparse
from pathlib import Path
from datetime import timedelta
import polars as pl

from src.domain.constants import (
    INDICATOR_UNIVERSE, INDICATOR_TIMEFRAMES, INDICATOR_SESSIONS,
    INDICATOR_TP_ATR_GRID, INDICATOR_SL_ATR_GRID,
    FRICTION_FX, FRICTION_INDEX, INDEX_SYMBOLS,
    WF_IS_MONTHS, WF_OOS_MONTHS,
)
from src.application.signal_generator import SignalGenerator, SIGNAL_TYPES
from src.engine.indicator_backtester import IndicatorBacktester, BacktestConfig
from src.engine.indicator_validation import (
    compute_metrics, walk_forward_wr, monte_carlo_ruin, decay_slope_ratio,
)
from src.engine.indicator_reporter import render_final_report, export_strategies_json
from src.engine.run_indicator_discovery import _load_and_enrich, _filter_by_session

REPORTS_DIR = Path("reports")

# Phase-1 v2 gates (screen)
P1_MIN_TRADES = 60
P1_MIN_WR = 0.60

# Phase-2 v2 gates (validate)
P2_MIN_TRADES_PER_YEAR = 60
P2_MIN_WR = 0.85
P2_MIN_EXPECTANCY_R = 0.05
P2_MAX_DD_R = 20.0
P2_WF_OOS_RATIO = 0.85
P2_MC_MAX_RUIN = 0.01
P2_DECAY_MIN = 0.70

LAST_YEAR_DAYS = 365


def _friction_for(symbol: str) -> float:
    return FRICTION_INDEX if symbol in INDEX_SYMBOLS else FRICTION_FX


def _slice_last_year(df: pl.DataFrame) -> pl.DataFrame:
    if len(df) == 0:
        return df
    t_end = df["time"].max()
    cutoff = t_end - timedelta(days=LAST_YEAR_DAYS)
    return df.filter(pl.col("time") >= cutoff)


def run_phase1_v2() -> pl.DataFrame:
    """Full-grid screen on last 1 year. 60k combos."""
    rr_combos = [(tp, sl) for tp in INDICATOR_TP_ATR_GRID for sl in INDICATOR_SL_ATR_GRID]
    rows = []
    evaluated = 0
    total = (len(INDICATOR_UNIVERSE) * len(INDICATOR_TIMEFRAMES)
             * len(INDICATOR_SESSIONS) * len(SIGNAL_TYPES) * len(rr_combos))
    print(f"[P1v2] total combos to evaluate: {total}")

    for symbol in INDICATOR_UNIVERSE:
        for tf in INDICATOR_TIMEFRAMES:
            try:
                full_bars = _load_and_enrich(symbol, tf)
            except FileNotFoundError:
                print(f"[SKIP] {symbol} {tf}: no data")
                continue
            bars = _slice_last_year(full_bars)
            if len(bars) < 500:
                print(f"[SKIP] {symbol} {tf}: only {len(bars)} bars in last year")
                continue
            friction = _friction_for(symbol)

            for signal_type in SIGNAL_TYPES:
                raw_signals = SignalGenerator.generate(bars, signal_type, symbol)
                for session in INDICATOR_SESSIONS:
                    sigs = _filter_by_session(raw_signals, session)
                    if len(sigs) < P1_MIN_TRADES:
                        evaluated += len(rr_combos)
                        continue
                    session_end = INDICATOR_SESSIONS[session][1]
                    for tp_mult, sl_mult in rr_combos:
                        evaluated += 1
                        cfg = BacktestConfig(
                            tp_atr_mult=tp_mult, sl_atr_mult=sl_mult,
                            session_end_hour_utc=session_end, friction_r=friction,
                        )
                        trades = IndicatorBacktester.run(sigs, bars, cfg)
                        if len(trades) < P1_MIN_TRADES:
                            continue
                        m = compute_metrics(trades)
                        if m.wr < P1_MIN_WR:
                            continue
                        rows.append({
                            "symbol": symbol, "tf": tf, "session": session,
                            "signal_type": signal_type,
                            "tp_atr_mult": tp_mult, "sl_atr_mult": sl_mult,
                            "n_trades": m.n_trades, "wr": m.wr,
                            "pf": m.profit_factor, "expectancy_r": m.expectancy_r,
                            "max_dd_r": m.max_dd_r,
                            "trades_per_year": m.trades_per_year,
                        })
                    if evaluated % 2000 == 0:
                        print(f"[P1v2] {evaluated}/{total} ({len(rows)} survivors so far)")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    if not rows:
        print("[P1v2] 0 survivors")
        pl.DataFrame().write_parquet(REPORTS_DIR / "indicator_v2_p1_survivors.parquet")
        return pl.DataFrame()
    survivors = pl.DataFrame(rows).sort("wr", descending=True)
    survivors.write_parquet(REPORTS_DIR / "indicator_v2_p1_survivors.parquet")
    (REPORTS_DIR / "indicator_v2_phase1.md").write_text(
        _render_p1_md(survivors), encoding="utf-8",
    )
    print(f"[P1v2] {len(survivors)} combos passed screen (trades>={P1_MIN_TRADES}, WR>={P1_MIN_WR})")
    return survivors


def _render_p1_md(survivors: pl.DataFrame) -> str:
    lines = [
        "# Indicator Discovery V2 - Phase 1 Report (1-year screen)",
        "",
        f"- Survivors: **{len(survivors)}**",
        f"- Gate: trades >= {P1_MIN_TRADES} AND WR >= {P1_MIN_WR}",
        f"- Data window: last {LAST_YEAR_DAYS} days",
        "",
        "## Top 50 by WR",
        "",
        "| Symbol | TF | Session | Signal | TP x ATR | SL x ATR | Trades | WR | PF | Exp (R) |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in survivors.head(50).iter_rows(named=True):
        lines.append(
            f"| {r['symbol']} | {r['tf']} | {r['session']} | {r['signal_type']} "
            f"| {r['tp_atr_mult']} | {r['sl_atr_mult']} | {r['n_trades']} "
            f"| {r['wr']:.3f} | {r['pf']:.2f} | {r['expectancy_r']:.3f} |"
        )
    return "\n".join(lines) + "\n"


def run_phase2_v2() -> pl.DataFrame:
    """Re-run survivors on full history. Apply strict gates."""
    p1_path = REPORTS_DIR / "indicator_v2_p1_survivors.parquet"
    if not p1_path.exists():
        raise FileNotFoundError(f"Run Phase-1 v2 first ({p1_path})")
    survivors = pl.read_parquet(p1_path)
    if len(survivors) == 0:
        print("[P2v2] no Phase-1 survivors; nothing to do")
        return pl.DataFrame()
    print(f"[P2v2] validating {len(survivors)} candidates on full history")

    rows = []
    for i, s in enumerate(survivors.iter_rows(named=True)):
        if i % 50 == 0:
            print(f"[P2v2] {i}/{len(survivors)}")
        symbol, tf, session = s["symbol"], s["tf"], s["session"]
        signal_type = s["signal_type"]
        tp_mult, sl_mult = s["tp_atr_mult"], s["sl_atr_mult"]
        try:
            bars = _load_and_enrich(symbol, tf)
        except FileNotFoundError:
            continue
        raw_signals = SignalGenerator.generate(bars, signal_type, symbol)
        sigs = _filter_by_session(raw_signals, session)
        if len(sigs) < 20:
            continue
        cfg = BacktestConfig(
            tp_atr_mult=tp_mult, sl_atr_mult=sl_mult,
            session_end_hour_utc=INDICATOR_SESSIONS[session][1],
            friction_r=_friction_for(symbol),
        )
        trades = IndicatorBacktester.run(sigs, bars, cfg)
        if len(trades) == 0:
            continue
        m = compute_metrics(trades)
        if m.trades_per_year < P2_MIN_TRADES_PER_YEAR:
            continue
        if m.wr < P2_MIN_WR:
            continue
        if m.expectancy_r < P2_MIN_EXPECTANCY_R:
            continue
        if m.max_dd_r > P2_MAX_DD_R:
            continue
        wf = walk_forward_wr(trades, is_months=WF_IS_MONTHS, oos_months=WF_OOS_MONTHS)
        if wf < P2_WF_OOS_RATIO:
            continue
        mc = monte_carlo_ruin(trades, risk_pct=0.01, initial_balance=10000,
                              n_sims=1000, n_steps=500, seed=42)
        if mc > P2_MC_MAX_RUIN:
            continue
        decay = decay_slope_ratio(trades, last_months=6)
        if decay < P2_DECAY_MIN:
            continue
        rows.append({
            "symbol": symbol, "tf": tf, "session": session,
            "signal_type": signal_type, "filters": [],
            "tp_atr_mult": tp_mult, "sl_atr_mult": sl_mult,
            "n_trades": m.n_trades, "wr": m.wr, "pf": m.profit_factor,
            "expectancy_r": m.expectancy_r, "max_dd_r": m.max_dd_r,
            "trades_per_year": m.trades_per_year,
            "wf_ratio": wf, "mc_ruin": mc, "decay_ratio": decay,
        })

    final = pl.DataFrame(rows) if rows else pl.DataFrame()
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    if len(final) > 0:
        final = final.sort("expectancy_r", descending=True)
    final.write_parquet(REPORTS_DIR / "indicator_v2_final.parquet")
    (REPORTS_DIR / "Indicator_Discovery_V2_Final.md").write_text(
        render_final_report(final), encoding="utf-8",
    )
    export_strategies_json(final, REPORTS_DIR / "indicator_v2_strategies.json")
    print(f"[P2v2] {len(final)} strategies passed strict gates")
    return final


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=("1", "2", "all"), default="all")
    args = ap.parse_args()
    if args.phase in ("1", "all"):
        run_phase1_v2()
    if args.phase in ("2", "all"):
        run_phase2_v2()


if __name__ == "__main__":
    main()
