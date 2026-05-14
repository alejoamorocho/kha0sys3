"""ORB Phase C: robustness validation.

Steps:
  1. Dedup Phase B survivors to best management per (sym, magic_time,
     or_duration, pattern_id, direction) by score = pf * log(trades_per_year).
  2. Realistic filter: WR in (0.55, 0.90), PF in (1.5, 10), expectancy >= 0.1,
     trades/yr >= 30.
  3. Robustness on per-trade R series:
       - MC 10k bootstrap (ruin DD >= 30R)
       - Walk-forward 50/50 (PF IS vs OOS)
       - Decay (annual WR slope)
  4. Classify FUERTE/ACEPTABLE/DEBIL/MUERTA via k3m1_robustness.classify
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import polars as pl

from src.application.orb_utils import REPORTS_DIR
from src.engine.k3m1_robustness import mc_ruin, walk_forward, decay, classify


REALISTIC_FILTER = {
    "wr_min": 0.55, "wr_max": 0.90,
    "pf_min": 1.5, "pf_max": 10.0,
    "expectancy_min": 0.1,
    "tpy_min": 30,
}


def dedup_best_per_slot(phase_b: pl.DataFrame) -> pl.DataFrame:
    if phase_b.is_empty():
        return phase_b
    scored = phase_b.with_columns(
        (pl.col("pf") * np.log(pl.col("trades_per_year").cast(pl.Float64))).alias("dedup_score")
    )
    slot_cols = ["symbol", "magic_time", "or_duration_min", "pattern_id", "direction"]
    ranked = scored.with_columns(
        pl.col("dedup_score").rank(method="dense", descending=True).over(slot_cols).alias("_rk")
    )
    return ranked.filter(pl.col("_rk") == 1).drop(["_rk", "dedup_score"])


def realistic_filter(df: pl.DataFrame) -> pl.DataFrame:
    if df.is_empty():
        return df
    f = REALISTIC_FILTER
    return df.filter(
        (pl.col("win_rate") >= f["wr_min"]) & (pl.col("win_rate") <= f["wr_max"])
        & (pl.col("pf") >= f["pf_min"]) & (pl.col("pf") <= f["pf_max"])
        & (pl.col("expectancy_r") >= f["expectancy_min"])
        & (pl.col("trades_per_year") >= f["tpy_min"])
    )


def _trade_series_for(combo_id: str, trades: pl.DataFrame) -> pl.DataFrame:
    return trades.filter(pl.col("combo_id") == combo_id)


def run_phase_c(
    phase_b_path=None,
    trades_path=None,
    out_path=None,
) -> pl.DataFrame:
    base = Path(REPORTS_DIR)
    phase_b_path = Path(phase_b_path or base / "orb_phase_b.parquet")
    trades_path = Path(trades_path or base / "orb_phase_b_trades.parquet")
    out_path = Path(out_path or base / "orb_robustness.parquet")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not phase_b_path.exists() or not trades_path.exists():
        pl.DataFrame().write_parquet(out_path)
        return pl.DataFrame()

    phase_b = pl.read_parquet(phase_b_path)
    trades = pl.read_parquet(trades_path)

    deduped = dedup_best_per_slot(phase_b)
    realistic = realistic_filter(deduped)

    rows: list[dict] = []
    for slot in realistic.iter_rows(named=True):
        trade_df = _trade_series_for(slot["combo_id"], trades)
        if trade_df.is_empty():
            continue
        r = trade_df["realized_r"].to_numpy()
        net_r = float(r.sum())
        pf = slot["pf"]
        mc = mc_ruin(r)
        renamed = trade_df.with_columns(pl.col("realized_r").alias("r"))
        wf = walk_forward(renamed)
        dec = decay(renamed)
        klass, reason = classify(mc, wf, dec, net_r, pf)
        rows.append({
            **slot,
            "mc_ruin": mc["ruin_prob"],
            "wf_pf_is": (wf or {}).get("pf_is"),
            "wf_pf_oos": (wf or {}).get("pf_oos"),
            "decay_wr_slope": (dec or {}).get("wr_slope"),
            "classification": klass,
            "classification_reason": reason,
        })
    out = pl.DataFrame(rows) if rows else pl.DataFrame()
    out.write_parquet(out_path)
    return out


if __name__ == "__main__":
    df = run_phase_c()
    print(f"Phase C: {len(df)} robustness-evaluated strategies")
