"""Test the 'invert the fade' hypothesis.

For each Math FADE Phase-A survivor (WR>=0.80 at TP=0.5/SL=2.5 but likely
negative expectancy due to asymmetric R:R), flip the entry direction and
sweep a momentum-style R:R grid (wide TP, tight SL). Report combos with
PF>=1.2 on full history.

Math: WR fade = 0.85 -> WR inverse = 0.15. PF>=1.2 needs TP/SL >= 4.72.
"""
from __future__ import annotations
from pathlib import Path
import polars as pl

from src.domain.constants import (
    INDICATOR_SESSIONS, FRICTION_FX, FRICTION_INDEX, INDEX_SYMBOLS,
)
from src.engine.indicator_validation import compute_metrics
from src.engine.run_math_discovery import _load_and_enrich_math
from src.engine.run_indicator_discovery import _filter_by_session
from src.engine.run_math_fade import detect_setups, run_backtest, BacktestConfig

REPORTS_DIR = Path("reports")
TP_GRID = (2.5, 3.0, 4.0, 5.0, 6.0, 7.5)
SL_GRID = (0.5, 0.75, 1.0, 1.5)


def _flip(signals: pl.DataFrame) -> pl.DataFrame:
    if len(signals) == 0:
        return signals
    return signals.with_columns([
        pl.when(pl.col("direction") == "LONG")
        .then(pl.lit("SHORT"))
        .otherwise(pl.lit("LONG"))
        .alias("direction")
    ])


def main():
    surv_path = REPORTS_DIR / "math_fade_phase_a_survivors.parquet"
    if not surv_path.exists():
        raise FileNotFoundError(surv_path)
    survivors = pl.read_parquet(surv_path)
    print(f"[Invert] {len(survivors)} Phase-A FADE survivors, flipping direction")
    print(f"[Invert] grid: TP {TP_GRID} x SL {SL_GRID} = {len(TP_GRID)*len(SL_GRID)} combos")

    rows = []
    for i, s in enumerate(survivors.iter_rows(named=True)):
        if i % 20 == 0:
            print(f"[Invert] {i}/{len(survivors)}", flush=True)
        sym, ses, setup = s["symbol"], s["session"], s["setup_type"]
        try:
            bars = _load_and_enrich_math(sym)
        except FileNotFoundError:
            continue
        try:
            sigs = detect_setups(bars, setup)
        except Exception:
            continue
        sigs = _filter_by_session(sigs, ses)
        if len(sigs) < 30:
            continue
        sigs_inv = _flip(sigs)
        fric = FRICTION_INDEX if sym in INDEX_SYMBOLS else FRICTION_FX
        session_end = INDICATOR_SESSIONS[ses][1]
        for tp in TP_GRID:
            for sl in SL_GRID:
                cfg = BacktestConfig(
                    tp_atr_mult=tp, sl_atr_mult=sl,
                    session_end_hour_utc=session_end,
                    friction_r=fric,
                )
                trades = run_backtest(sigs_inv, bars, setup, cfg, sym)
                if len(trades) < 30:
                    continue
                m = compute_metrics(trades)
                if m.trades_per_year < 15:
                    continue
                rows.append({
                    "symbol": sym, "session": ses, "setup_type": setup,
                    "tp_atr_mult": tp, "sl_atr_mult": sl,
                    "n_trades": m.n_trades, "wr": m.wr, "pf": m.profit_factor,
                    "expectancy_r": m.expectancy_r, "max_dd_r": m.max_dd_r,
                    "trades_per_year": m.trades_per_year,
                })

    if not rows:
        print("[Invert] no combos produced trades")
        return
    df = pl.DataFrame(rows)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    df.write_parquet(REPORTS_DIR / "math_fade_invert.parquet")
    print(f"\nTotal combos: {len(df)}")
    print(f"PF>=1.2: {len(df.filter(pl.col('pf')>=1.2))}")
    print(f"PF>=1.2 AND exp>=0.05R: {len(df.filter((pl.col('pf')>=1.2)&(pl.col('expectancy_r')>=0.05)))}")
    print(f"PF>=1.3 AND exp>=0.10R: {len(df.filter((pl.col('pf')>=1.3)&(pl.col('expectancy_r')>=0.10)))}")
    print()
    pl.Config.set_tbl_rows(15); pl.Config.set_tbl_width_chars(220)
    print("Top 15 by expectancy:")
    print(df.sort("expectancy_r", descending=True).head(15))


if __name__ == "__main__":
    main()
