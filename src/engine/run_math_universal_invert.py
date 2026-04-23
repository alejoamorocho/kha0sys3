"""Universal inversion test: flip direction for EVERY (asset, session, setup)
combo — both FADE and MOMENTUM families — over their full R:R grids.

Goal: find combos where the ORIGINAL direction had low WR (say <45%) but
INVERTED direction produces WR>55% + PF>=1.2. These are setups we previously
rejected that become winners when flipped.

Two inversion tracks:
  1. FADE setups (6) inverted → becomes momentum-like (STOP-style R:R)
  2. MOMENTUM setups (6) inverted → becomes fade-like (tight TP, wide SL)

For each track we sweep its OWN R:R grid (same as the original pipeline).
"""
from __future__ import annotations
from pathlib import Path
import polars as pl

from src.domain.constants import (
    INDICATOR_UNIVERSE, INDICATOR_SESSIONS, FRICTION_FX, FRICTION_INDEX, INDEX_SYMBOLS,
)
from src.engine.indicator_validation import compute_metrics
from src.engine.run_math_discovery import _load_and_enrich_math
from src.engine.run_indicator_discovery import _filter_by_session

# FADE: detect setups, then invert direction, test momentum-style R:R
from src.engine.run_math_fade import (
    detect_setups as detect_fade,
    run_backtest as run_fade_bt,
    BacktestConfig as FadeCfg,
)

# MOMENTUM: detect, invert, test fade-style R:R
from src.engine.run_math_momentum import (
    detect_setups as detect_mom,
    run_backtest as run_mom_bt,
    BacktestConfig as MomCfg,
)

REPORTS_DIR = Path("reports")

FADE_SETUPS = ("KALMAN_PEAK_FADE", "ZSCORE_EXTREME_FADE", "OLS_EXTREME_FADE",
               "CURVATURE_PEAK_FADE", "GARCH_Z_FADE", "AREA_EXTREME_FADE")
MOM_SETUPS = ("VELOCITY_ACCEL_GO", "KAMA_CROSS_MOM", "OLS_SLOPE_STRONG",
              "HURST_TREND_MOM", "KALMAN_INNOV_EXPAND", "SPECTRAL_TREND_MOM")

# When inverting FADE → test momentum-style R:R (wide TP, tight SL)
FADE_INV_TP = (2.0, 2.5, 3.0, 4.0, 5.0, 6.0)
FADE_INV_SL = (0.5, 0.75, 1.0, 1.5)

# When inverting MOMENTUM → test fade-style R:R (tight TP, wide SL)
MOM_INV_TP = (0.3, 0.5, 0.75, 1.0)
MOM_INV_SL = (1.5, 2.0, 2.5, 3.0)


def _flip(signals: pl.DataFrame) -> pl.DataFrame:
    if len(signals) == 0:
        return signals
    return signals.with_columns([
        pl.when(pl.col("direction") == "LONG")
        .then(pl.lit("SHORT"))
        .otherwise(pl.lit("LONG"))
        .alias("direction")
    ])


def _friction(sym: str) -> float:
    return FRICTION_INDEX if sym in INDEX_SYMBOLS else FRICTION_FX


def sweep_family(setups_list, detector, runner, cfg_cls, tp_grid, sl_grid, family_label):
    rows = []
    total = len(INDICATOR_UNIVERSE) * len(INDICATOR_SESSIONS) * len(setups_list)
    done = 0
    for sym in INDICATOR_UNIVERSE:
        try:
            bars = _load_and_enrich_math(sym)
        except FileNotFoundError:
            continue
        for setup in setups_list:
            try:
                raw = detector(bars, setup)
            except Exception:
                continue
            for ses in INDICATOR_SESSIONS:
                done += 1
                sigs = _filter_by_session(raw, ses)
                if len(sigs) < 30:
                    continue
                sigs_inv = _flip(sigs)
                fric = _friction(sym)
                se = INDICATOR_SESSIONS[ses][1]
                for tp in tp_grid:
                    for sl in sl_grid:
                        cfg = cfg_cls(tp_atr_mult=tp, sl_atr_mult=sl,
                                      session_end_hour_utc=se, friction_r=fric)
                        trades = runner(sigs_inv, bars, setup, cfg, sym)
                        if len(trades) < 30:
                            continue
                        m = compute_metrics(trades)
                        if m.trades_per_year < 15:
                            continue
                        rows.append({
                            "family": family_label,
                            "symbol": sym, "session": ses, "setup_type": setup,
                            "tp_atr_mult": tp, "sl_atr_mult": sl,
                            "n_trades": m.n_trades, "wr": m.wr, "pf": m.profit_factor,
                            "expectancy_r": m.expectancy_r, "max_dd_r": m.max_dd_r,
                            "trades_per_year": m.trades_per_year,
                        })
            if done % 10 == 0:
                print(f"[{family_label}-INV] {done}/{total}", flush=True)
    return rows


def main():
    print("=== INVERT ALL FADE setups + test momentum R:R ===")
    fade_rows = sweep_family(FADE_SETUPS, detect_fade, run_fade_bt, FadeCfg,
                             FADE_INV_TP, FADE_INV_SL, "FADE_INV")
    print(f"  fade-inv combos (>=15 trades/yr): {len(fade_rows)}")

    print("\n=== INVERT ALL MOMENTUM setups + test fade R:R ===")
    mom_rows = sweep_family(MOM_SETUPS, detect_mom, run_mom_bt, MomCfg,
                            MOM_INV_TP, MOM_INV_SL, "MOM_INV")
    print(f"  mom-inv combos (>=15 trades/yr): {len(mom_rows)}")

    all_rows = fade_rows + mom_rows
    if not all_rows:
        print("no combos produced trades")
        return
    df = pl.DataFrame(all_rows)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    df.write_parquet(REPORTS_DIR / "math_universal_invert.parquet")

    print(f"\n=== SUMMARY ===")
    print(f"Total combos evaluated: {len(df)}")
    print(f"PF>=1.2 AND WR>=0.55: {len(df.filter((pl.col('pf')>=1.2)&(pl.col('wr')>=0.55)))}")
    print(f"PF>=1.2 AND exp>=0.05R: {len(df.filter((pl.col('pf')>=1.2)&(pl.col('expectancy_r')>=0.05)))}")
    print(f"PF>=1.3 AND exp>=0.10R: {len(df.filter((pl.col('pf')>=1.3)&(pl.col('expectancy_r')>=0.10)))}")
    print(f"PF>=1.5 AND exp>=0.15R: {len(df.filter((pl.col('pf')>=1.5)&(pl.col('expectancy_r')>=0.15)))}")

    for fam in ("FADE_INV", "MOM_INV"):
        sub = df.filter(pl.col("family") == fam)
        print(f"\n--- Top 10 {fam} by expectancy ---")
        pl.Config.set_tbl_rows(10); pl.Config.set_tbl_width_chars(220)
        top = sub.filter(pl.col("pf") >= 1.2).sort("expectancy_r", descending=True).head(10)
        if len(top) == 0:
            top = sub.sort("expectancy_r", descending=True).head(10)
        print(top)


if __name__ == "__main__":
    main()
