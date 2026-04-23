"""Validate invert candidates with WF + MC + decay on full history.

Input: reports/universal_invert_validation_input.parquet (combos that already
meet WR>=0.80, trades/yr>=30, PF>=1.0, expectancy>0).

Output: reports/Invert_Validated.md + .parquet + .json
Gates: WF ratio >= 0.80, MC ruin <= 0.02, decay >= 0.60.
"""
from __future__ import annotations
from pathlib import Path
import json
import polars as pl

from src.domain.constants import (
    INDICATOR_SESSIONS, FRICTION_FX, FRICTION_INDEX, INDEX_SYMBOLS,
    WF_IS_MONTHS, WF_OOS_MONTHS,
)
from src.engine.indicator_validation import (
    compute_metrics, walk_forward_wr, monte_carlo_ruin, decay_slope_ratio,
)
from src.engine.run_math_discovery import _load_and_enrich_math
from src.engine.run_indicator_discovery import _filter_by_session

from src.engine.run_math_fade import (
    detect_setups as detect_fade,
    run_backtest as run_fade_bt,
    BacktestConfig as FadeCfg,
)
from src.engine.run_math_momentum import (
    detect_setups as detect_mom,
    run_backtest as run_mom_bt,
    BacktestConfig as MomCfg,
)

REPORTS_DIR = Path("reports")

FADE_SETUPS = {"KALMAN_PEAK_FADE", "ZSCORE_EXTREME_FADE", "OLS_EXTREME_FADE",
               "CURVATURE_PEAK_FADE", "GARCH_Z_FADE", "AREA_EXTREME_FADE"}


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
    cands = pl.read_parquet(REPORTS_DIR / "universal_invert_validation_input.parquet")
    print(f"[Validate] {len(cands)} candidates")
    rows = []
    for i, c in enumerate(cands.iter_rows(named=True)):
        if i % 50 == 0:
            print(f"[Validate] {i}/{len(cands)}", flush=True)
        sym, ses, setup = c["symbol"], c["session"], c["setup_type"]
        tp, sl = c["tp_atr_mult"], c["sl_atr_mult"]
        family = c["family"]
        try:
            bars = _load_and_enrich_math(sym)
        except FileNotFoundError:
            continue

        # Detect setups using matching detector
        try:
            if setup in FADE_SETUPS:
                raw = detect_fade(bars, setup)
            else:
                raw = detect_mom(bars, setup)
        except Exception:
            continue
        sigs = _filter_by_session(raw, ses)
        if len(sigs) < 30:
            continue
        sigs_inv = _flip(sigs)

        fric = FRICTION_INDEX if sym in INDEX_SYMBOLS else FRICTION_FX
        se = INDICATOR_SESSIONS[ses][1]

        if family == "FADE_INV":
            cfg = FadeCfg(tp_atr_mult=tp, sl_atr_mult=sl, session_end_hour_utc=se, friction_r=fric)
            trades = run_fade_bt(sigs_inv, bars, setup, cfg, sym)
        else:
            cfg = MomCfg(tp_atr_mult=tp, sl_atr_mult=sl, session_end_hour_utc=se, friction_r=fric)
            trades = run_mom_bt(sigs_inv, bars, setup, cfg, sym)
        if len(trades) < 30:
            continue

        m = compute_metrics(trades)
        wf = walk_forward_wr(trades, WF_IS_MONTHS, WF_OOS_MONTHS)
        mc = monte_carlo_ruin(trades, risk_pct=0.02, initial_balance=10_000)
        decay = decay_slope_ratio(trades, last_months=6)

        if wf < 0.80 or mc > 0.02 or decay < 0.60:
            continue

        rows.append({
            "family": family, "symbol": sym, "session": ses, "setup_type": setup,
            "tp_atr_mult": tp, "sl_atr_mult": sl,
            "n_trades": m.n_trades, "wr": m.wr, "pf": m.profit_factor,
            "expectancy_r": m.expectancy_r, "max_dd_r": m.max_dd_r,
            "trades_per_year": m.trades_per_year,
            "wf_ratio": wf, "mc_ruin": mc, "decay_ratio": decay,
        })

    if not rows:
        print("[Validate] 0 survivors")
        return
    df = pl.DataFrame(rows).sort("expectancy_r", descending=True)
    df.write_parquet(REPORTS_DIR / "invert_validated.parquet")
    print(f"\n=== VALIDATED: {len(df)} survivors ===")

    # Breakdown
    print(f"  by family: {df['family'].value_counts().to_dict(as_series=False)}")
    print(f"  by setup: ")
    for s, n in df.group_by("setup_type").len().sort("len", descending=True).iter_rows():
        print(f"    {s}: {n}")
    print(f"  by symbol: ")
    for s, n in df.group_by("symbol").len().sort("len", descending=True).iter_rows():
        print(f"    {s}: {n}")

    # JSON export
    items = []
    for r in df.iter_rows(named=True):
        items.append({
            "family": r["family"],
            "symbol": r["symbol"], "tf": "M15", "session": r["session"],
            "setup_type": r["setup_type"], "direction_mode": "INVERTED",
            "tp_atr_mult": float(r["tp_atr_mult"]), "sl_atr_mult": float(r["sl_atr_mult"]),
            "metrics": {
                "wr": float(r["wr"]), "pf": float(r["pf"]),
                "expectancy_r": float(r["expectancy_r"]),
                "max_dd_r": float(r["max_dd_r"]),
                "trades_per_year": float(r["trades_per_year"]),
                "wf_ratio": float(r["wf_ratio"]),
                "mc_ruin": float(r["mc_ruin"]),
                "decay_ratio": float(r["decay_ratio"]),
            }
        })
    (REPORTS_DIR / "invert_validated.json").write_text(json.dumps(items, indent=2), encoding="utf-8")

    # Markdown report
    md = ["# Inverted Strategies - Validated on Full History", "",
          f"- Total validated: **{len(df)}**",
          f"- Gates: WR>=0.80, trades/yr>=30, PF>=1.0, WF>=0.80, MC<=0.02, decay>=0.60", "",
          "## Top 30 by expectancy", "",
          "| Family | Symbol | Session | Setup | TP | SL | Trades | WR | PF | Exp(R) | WF | MC | Decay | Trades/yr |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in df.head(30).iter_rows(named=True):
        md.append(
            f"| {r['family']} | {r['symbol']} | {r['session']} | {r['setup_type']} "
            f"| {r['tp_atr_mult']} | {r['sl_atr_mult']} "
            f"| {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.2f} "
            f"| {r['expectancy_r']:.3f} | {r['wf_ratio']:.2f} | {r['mc_ruin']:.3f} "
            f"| {r['decay_ratio']:.2f} | {r['trades_per_year']:.0f} |"
        )
    (REPORTS_DIR / "Invert_Validated.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
