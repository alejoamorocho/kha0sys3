"""Phase-2: for each Phase-1 survivor, grid-search 11 confluence combos x 20 R:R ATR.
Apply strict gates (WR>=80%, WF, MC, decay). Output final report + JSON export."""
from __future__ import annotations
from itertools import combinations
from pathlib import Path
import polars as pl

from src.domain.constants import (
    INDICATOR_TP_ATR_GRID, INDICATOR_SL_ATR_GRID, INDICATOR_SESSIONS,
    PHASE2_MIN_TRADES_PER_YEAR, PHASE2_MIN_WR, PHASE2_MIN_PF, PHASE2_MIN_EXPECTANCY_R,
    PHASE2_MAX_DD_R, PHASE2_WF_OOS_RATIO, PHASE2_MC_MAX_RUIN_PCT, PHASE2_DECAY_MIN_RATIO,
    WF_IS_MONTHS, WF_OOS_MONTHS, FRICTION_FX, FRICTION_INDEX, INDEX_SYMBOLS,
)
from src.application.signal_generator import SignalGenerator
from src.engine.indicator_backtester import IndicatorBacktester, BacktestConfig
from src.engine.indicator_validation import (
    compute_metrics, walk_forward_wr, monte_carlo_ruin, decay_slope_ratio,
)
from src.engine.indicator_reporter import render_final_report, export_strategies_json
from src.engine.run_indicator_discovery import _load_and_enrich, _filter_by_session

REPORTS_DIR = Path("reports")

# Confluence filter combos: 0, 1, or 2 filters from 4 families.
# One representative state per family picked (TREND/EXTREME/UPPER/POS -- aggressive side).
FILTER_POOL = ("ADX_REGIME_TREND", "RSI_ZONE_EXTREME", "BB_POSITION_UPPER", "MACD_ALIGN_POS")


def _all_filter_combos() -> list[tuple[str, ...]]:
    combos: list[tuple[str, ...]] = [()]
    for k in (1, 2):
        combos.extend(tuple(c) for c in combinations(FILTER_POOL, k))
    return combos  # 1 + 4 + 6 = 11


def run_phase2() -> pl.DataFrame:
    survivors_path = REPORTS_DIR / "indicator_survivors_phase1.parquet"
    if not survivors_path.exists():
        raise FileNotFoundError(f"Run Phase-1 first (missing {survivors_path})")
    survivors = pl.read_parquet(survivors_path)
    print(f"[P2] optimizing {len(survivors)} Phase-1 survivors")

    filter_combos = _all_filter_combos()
    rr_combos = [(tp, sl) for tp in INDICATOR_TP_ATR_GRID for sl in INDICATOR_SL_ATR_GRID]

    final_rows = []
    for surv_idx, surv in enumerate(survivors.iter_rows(named=True)):
        symbol, tf, session, signal_type = (
            surv["symbol"], surv["tf"], surv["session"], surv["signal_type"]
        )
        try:
            bars = _load_and_enrich(symbol, tf)
        except FileNotFoundError:
            print(f"[P2][SKIP] {symbol} {tf}: no data file")
            continue
        raw_signals = SignalGenerator.generate(bars, signal_type, symbol)
        sigs_session = _filter_by_session(raw_signals, session)
        friction = FRICTION_INDEX if symbol in INDEX_SYMBOLS else FRICTION_FX
        session_end = INDICATOR_SESSIONS[session][1]

        for fcombo in filter_combos:
            filtered_sigs = SignalGenerator.apply_filters(sigs_session, bars, fcombo)
            if len(filtered_sigs) < 20:
                continue
            for tp_mult, sl_mult in rr_combos:
                cfg = BacktestConfig(
                    tp_atr_mult=tp_mult, sl_atr_mult=sl_mult,
                    session_end_hour_utc=session_end, friction_r=friction,
                )
                trades = IndicatorBacktester.run(filtered_sigs, bars, cfg)
                if len(trades) == 0:
                    continue
                m = compute_metrics(trades)
                # Cheap gates first
                if (m.trades_per_year < PHASE2_MIN_TRADES_PER_YEAR
                        or m.wr < PHASE2_MIN_WR
                        or m.profit_factor < PHASE2_MIN_PF
                        or m.expectancy_r < PHASE2_MIN_EXPECTANCY_R
                        or m.max_dd_r > PHASE2_MAX_DD_R):
                    continue
                # Expensive gates only if cheap ones pass
                wf_ratio = walk_forward_wr(trades, is_months=WF_IS_MONTHS, oos_months=WF_OOS_MONTHS)
                if wf_ratio < PHASE2_WF_OOS_RATIO:
                    continue
                mc = monte_carlo_ruin(trades, risk_pct=0.01, initial_balance=10000,
                                      n_sims=1000, n_steps=500, seed=42)
                if mc > PHASE2_MC_MAX_RUIN_PCT:
                    continue
                decay = decay_slope_ratio(trades, last_months=6)
                if decay < PHASE2_DECAY_MIN_RATIO:
                    continue
                final_rows.append({
                    "symbol": symbol, "tf": tf, "session": session,
                    "signal_type": signal_type, "filters": list(fcombo),
                    "tp_atr_mult": tp_mult, "sl_atr_mult": sl_mult,
                    "n_trades": m.n_trades, "wr": m.wr, "pf": m.profit_factor,
                    "expectancy_r": m.expectancy_r, "max_dd_r": m.max_dd_r,
                    "trades_per_year": m.trades_per_year,
                    "wf_ratio": wf_ratio, "mc_ruin": mc, "decay_ratio": decay,
                })
        if surv_idx % 10 == 0:
            print(f"[P2] {surv_idx + 1}/{len(survivors)} survivors processed")

    final = pl.DataFrame(final_rows) if final_rows else pl.DataFrame()
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    if len(final) > 0:
        final = final.sort("expectancy_r", descending=True)
    final.write_parquet(REPORTS_DIR / "indicator_final.parquet")
    (REPORTS_DIR / "Indicator_Discovery_Final.md").write_text(
        render_final_report(final), encoding="utf-8"
    )
    export_strategies_json(final, REPORTS_DIR / "indicator_strategies.json")
    print(f"[P2] {len(final)} strategies passed strict gates")
    return final
