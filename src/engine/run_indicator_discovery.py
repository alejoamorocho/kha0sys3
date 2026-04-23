"""End-to-end runner: Phase-1 discovery + Phase-2 optimization.

Phase-1 evaluates (asset × TF × session × primary signal) combos with fixed R:R
and loose gates, writes survivors to reports/indicator_survivors_phase1.parquet.

Usage:
    python -m src.engine.run_indicator_discovery --phase 1
    python -m src.engine.run_indicator_discovery --phase 2
    python -m src.engine.run_indicator_discovery --phase all
"""
from __future__ import annotations
import argparse
from pathlib import Path
import polars as pl

from src.domain.constants import (
    INDICATOR_UNIVERSE, INDICATOR_TIMEFRAMES, INDICATOR_SESSIONS,
    PHASE1_MIN_TRADES_PER_YEAR, PHASE1_MIN_WR, PHASE1_MIN_PF, PHASE1_MIN_EXPECTANCY_R,
    FRICTION_FX, FRICTION_INDEX, INDEX_SYMBOLS,
)
from src.application.indicators import IndicatorEnricher
from src.application.signal_generator import SignalGenerator, SIGNAL_TYPES
from src.engine.indicator_backtester import IndicatorBacktester, BacktestConfig
from src.engine.indicator_validation import compute_metrics

# CSVPolarsLoader actual path: src.infrastructure.data.polars_loader
from src.infrastructure.data.polars_loader import CSVPolarsLoader

DATA_DIR = "c:/Proyectos/kha0sys3/data"
ENRICHED_CACHE = Path("data/enriched")
REPORTS_DIR = Path("reports")


def _friction_for(symbol: str) -> float:
    return FRICTION_INDEX if symbol in INDEX_SYMBOLS else FRICTION_FX


def _session_end_hour(session: str) -> int:
    return INDICATOR_SESSIONS[session][1]


def _filter_by_session(signals: pl.DataFrame, session: str) -> pl.DataFrame:
    start_h, end_h = INDICATOR_SESSIONS[session]
    return signals.filter(
        (pl.col("time").dt.hour() >= start_h) & (pl.col("time").dt.hour() < end_h)
    )


def _load_and_enrich(symbol: str, tf: str) -> pl.DataFrame:
    cache_path = ENRICHED_CACHE / f"{symbol}_{tf}.parquet"
    if cache_path.exists():
        return pl.read_parquet(cache_path)
    ENRICHED_CACHE.mkdir(parents=True, exist_ok=True)
    loader = CSVPolarsLoader(DATA_DIR)
    bars = loader.load_data(symbol, tf)
    # Add ATR(14) inline using Wilder EWM (alpha=1/14) if not already present
    if "atr_14" not in bars.columns:
        bars = bars.with_columns(
            pl.max_horizontal(
                pl.col("high") - pl.col("low"),
                (pl.col("high") - pl.col("close").shift(1)).abs(),
                (pl.col("low") - pl.col("close").shift(1)).abs(),
            ).alias("_tr")
        ).with_columns(
            pl.col("_tr").ewm_mean(alpha=1 / 14, adjust=False, min_periods=14).alias("atr_14")
        ).drop("_tr")
    enriched = IndicatorEnricher.enrich_all(bars)
    enriched.write_parquet(cache_path)
    return enriched


def run_phase1() -> pl.DataFrame:
    rows = []
    total = (
        len(INDICATOR_UNIVERSE)
        * len(INDICATOR_TIMEFRAMES)
        * len(INDICATOR_SESSIONS)
        * len(SIGNAL_TYPES)
    )
    i = 0
    for symbol in INDICATOR_UNIVERSE:
        for tf in INDICATOR_TIMEFRAMES:
            try:
                bars = _load_and_enrich(symbol, tf)
            except FileNotFoundError:
                print(f"[SKIP] {symbol} {tf}: no data file")
                continue
            for signal_type in SIGNAL_TYPES:
                raw_signals = SignalGenerator.generate(bars, signal_type, symbol)
                for session in INDICATOR_SESSIONS:
                    i += 1
                    sigs = _filter_by_session(raw_signals, session)
                    if len(sigs) < 20:
                        continue
                    cfg = BacktestConfig(
                        tp_atr_mult=2.0,
                        sl_atr_mult=1.0,
                        session_end_hour_utc=_session_end_hour(session),
                        friction_r=_friction_for(symbol),
                    )
                    trades = IndicatorBacktester.run(sigs, bars, cfg)
                    if len(trades) == 0:
                        continue
                    m = compute_metrics(trades)
                    rows.append({
                        "symbol": symbol,
                        "tf": tf,
                        "session": session,
                        "signal_type": signal_type,
                        "n_trades": m.n_trades,
                        "wr": m.wr,
                        "pf": m.profit_factor,
                        "expectancy_r": m.expectancy_r,
                        "max_dd_r": m.max_dd_r,
                        "trades_per_year": m.trades_per_year,
                    })
                    if i % 100 == 0:
                        print(f"[P1] {i}/{total}")

    results = pl.DataFrame(rows) if rows else pl.DataFrame()
    if len(results) == 0:
        print("[P1] No results.")
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        results.write_parquet(REPORTS_DIR / "indicator_phase1_all.parquet")
        survivors = pl.DataFrame()
        survivors.write_parquet(REPORTS_DIR / "indicator_survivors_phase1.parquet")
        (REPORTS_DIR / "indicator_discovery_phase1.md").write_text(
            _render_p1_md(results, survivors), encoding="utf-8"
        )
        return results

    survivors = results.filter(
        (pl.col("trades_per_year") >= PHASE1_MIN_TRADES_PER_YEAR)
        & (pl.col("wr") >= PHASE1_MIN_WR)
        & (pl.col("pf") >= PHASE1_MIN_PF)
        & (pl.col("expectancy_r") >= PHASE1_MIN_EXPECTANCY_R)
    ).sort("expectancy_r", descending=True)

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    results.write_parquet(REPORTS_DIR / "indicator_phase1_all.parquet")
    survivors.write_parquet(REPORTS_DIR / "indicator_survivors_phase1.parquet")
    (REPORTS_DIR / "indicator_discovery_phase1.md").write_text(_render_p1_md(results, survivors), encoding="utf-8")
    print(f"[P1] {len(results)} combos evaluated, {len(survivors)} passed loose gates")
    return survivors


def _render_p1_md(results: pl.DataFrame, survivors: pl.DataFrame) -> str:
    lines = [
        "# Indicator Discovery — Phase 1 Report",
        "",
        f"- Combos evaluated: **{len(results)}**",
        f"- Passed loose gates: **{len(survivors)}**",
        f"- Gates: trades/year \u2265 {PHASE1_MIN_TRADES_PER_YEAR}, WR \u2265 {PHASE1_MIN_WR}, "
        f"PF \u2265 {PHASE1_MIN_PF}, expectancy \u2265 {PHASE1_MIN_EXPECTANCY_R}R",
        "",
        "## Top 30 survivors (by expectancy)",
        "",
        "| Symbol | TF | Session | Signal | Trades | WR | PF | Exp (R) | MaxDD (R) |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for r in survivors.head(30).iter_rows(named=True):
        lines.append(
            f"| {r['symbol']} | {r['tf']} | {r['session']} | {r['signal_type']} "
            f"| {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.2f} "
            f"| {r['expectancy_r']:.3f} | {r['max_dd_r']:.1f} |"
        )
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=("1", "2", "all"), default="all")
    args = ap.parse_args()
    if args.phase in ("1", "all"):
        run_phase1()
    if args.phase in ("2", "all"):
        from src.engine.run_indicator_discovery_phase2 import run_phase2
        run_phase2()


if __name__ == "__main__":
    main()
