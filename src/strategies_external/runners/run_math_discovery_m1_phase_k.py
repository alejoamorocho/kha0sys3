"""MATH Discovery Phase K — re-run Phase B (M15/H1/H4) and Phase F (M1 entries)
with realistic Vantage friction: 0.05R FX / 0.10R non-FX (halved from 0.10/0.20).

Phase B: 1800 combos × 14 (7 TP/SL × 2 invert) = 25,200 backtests
Phase F: 4 × 12 × 5 × 7 × 2 = 3,360 backtests
Filter gate: WR >= 0.60 AND PF >= 1.30 AND n_trades >= 30

Usage:
    python -u -m src.strategies_external.runners.run_math_discovery_m1_phase_k
"""
from __future__ import annotations

import time
from pathlib import Path

import polars as pl

# ── Import base module and monkey-patch friction BEFORE any runs ────────────────
import src.strategies_external.runners.run_math_discovery_m1 as _mod

# Override friction: realistic Vantage values (halved from original 0.30/0.40).
_FX_SET = {"EURUSD", "USDJPY", "GBPAUD"}


def _friction_for(sym: str) -> float:
    """Realistic Vantage friction: 0.05R FX / 0.10R non-FX."""
    return 0.05 if sym in _FX_SET else 0.10


# Patch the module-level function so both Phase B and Phase F use new friction.
_mod._friction_for = _friction_for

# ── Phase K gates (stricter than Phase A/B default) ────────────────────────────
PK_MIN_TRADES = 30
PK_MIN_WR = 0.60
PK_MIN_PF = 1.30

REPORTS_DIR = Path("reports/external")

# ── Report paths ───────────────────────────────────────────────────────────────
PHASE_B_OUTPUT = "reports/external/math_discovery_m1_phase_b_lowfric.md"
PHASE_F_OUTPUT = "reports/external/math_discovery_m1_phase_f_lowfric.md"
COMBINED_OUTPUT = "reports/external/math_discovery_m1_phase_k_combined.md"


def _apply_strict_gate(df: pl.DataFrame) -> pl.DataFrame:
    """Filter to Phase K strict gate: WR >= 0.60 AND PF >= 1.30 AND n_trades >= 30."""
    if df.is_empty():
        return df
    return df.filter(
        (pl.col("wr") >= PK_MIN_WR)
        & (pl.col("pf") >= PK_MIN_PF)
        & (pl.col("n_trades") >= PK_MIN_TRADES)
    )


def _distribution_stats(df: pl.DataFrame, label: str) -> list[str]:
    """Return markdown lines with p50/p75/p90/max of WR and PF."""
    if df.is_empty():
        return [f"**{label}**: no data"]
    wr = df["wr"].to_list()
    pf = df["pf"].to_list()
    wr_sorted = sorted(wr)
    pf_sorted = sorted(pf)
    n = len(wr_sorted)

    def pct(lst: list[float], p: float) -> float:
        idx = min(int(p * n), n - 1)
        return round(lst[idx], 4)

    lines = [
        f"**{label}** (n={n})",
        f"  - WR: p50={pct(wr_sorted, 0.50):.3f}  p75={pct(wr_sorted, 0.75):.3f}  "
        f"p90={pct(wr_sorted, 0.90):.3f}  max={max(wr_sorted):.3f}",
        f"  - PF: p50={pct(pf_sorted, 0.50):.3f}  p75={pct(pf_sorted, 0.75):.3f}  "
        f"p90={pct(pf_sorted, 0.90):.3f}  max={max(pf_sorted):.3f}",
    ]
    return lines


def _closest_to_gate(df: pl.DataFrame) -> pl.DataFrame:
    """For each (sym, tf, setup_type, session, invert): row with highest PF × WR."""
    if df.is_empty():
        return df
    return (
        df.with_columns(
            (pl.col("pf") * pl.col("wr")).alias("_score")
        )
        .sort("_score", descending=True)
        .group_by(["symbol", "tf", "setup_type", "session", "invert"])
        .agg(pl.all().first())
        .drop("_score")
        .sort("calmar", descending=True)
    )


def _write_combined_report(
    df_b: pl.DataFrame,
    df_f: pl.DataFrame,
    b_total_backtests: int,
    f_total_backtests: int,
    b_runtime: float,
    f_runtime: float,
) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # Phase K survivors (strict gate applied to raw survivors from B and F)
    strict_b = _apply_strict_gate(df_b)
    strict_f = _apply_strict_gate(df_f)

    # Combined
    combined_parts = []
    if not strict_b.is_empty():
        combined_parts.append(strict_b.with_columns(pl.lit("B").alias("phase")))
    if not strict_f.is_empty():
        combined_parts.append(strict_f.with_columns(pl.lit("F").alias("phase")))

    if combined_parts:
        combined = pl.concat(combined_parts, how="diagonal").sort("calmar", descending=True)
    else:
        combined = pl.DataFrame()

    lines = [
        "# MATH Discovery Phase K — Realistic Vantage Friction (0.05 FX / 0.10 non-FX)",
        "",
        "## Summary",
        "",
        f"| Phase | Backtests | Raw Survivors (WR>=0.50 PF>=1.0) | Strict Survivors (WR>=0.60 PF>=1.30) | Runtime |",
        f"|-------|-----------|-----------------------------------|---------------------------------------|---------|",
        f"| B (M15/H1/H4) | {b_total_backtests} | {len(df_b)} | {len(strict_b)} | {b_runtime:.0f}s ({b_runtime/60:.1f} min) |",
        f"| F (M1 entries) | {f_total_backtests} | {len(df_f)} | {len(strict_f)} | {f_runtime:.0f}s ({f_runtime/60:.1f} min) |",
        f"| **TOTAL** | **{b_total_backtests + f_total_backtests}** | **{len(df_b) + len(df_f)}** | **{len(combined)}** | **{(b_runtime+f_runtime)/60:.1f} min** |",
        "",
        f"Gates (strict): WR >= {PK_MIN_WR}, PF >= {PK_MIN_PF}, n_trades >= {PK_MIN_TRADES}",
        "",
    ]

    # --- Phase B section ---
    lines += [
        "## Phase B Re-run (M15/H1/H4 × TP/SL grid)",
        "",
        f"- Total backtests: **{b_total_backtests}**",
        f"- Raw survivors (Phase A gate WR>=0.50 PF>=1.0): **{len(df_b)}**",
        f"- Strict survivors (Phase K gate): **{len(strict_b)}**",
        "",
    ]
    if not strict_b.is_empty():
        lines += [
            "### Top 20 Phase B strict survivors (by Calmar)",
            "",
            "| # | sym | tf | setup | session | inv | tp | sl | n | wr | pf | exp_R | dd_R | calmar |",
            "|---|-----|-----|-------|---------|-----|-----|-----|---|-----|-----|-------|------|--------|",
        ]
        for rank, r in enumerate(strict_b.head(20).iter_rows(named=True), 1):
            kind = "FADE" if r.get("is_fade") else "MOM"
            lines.append(
                f"| {rank} | {r['symbol']} | {r['tf']} | {r['setup_type']} | {r['session']} "
                f"| {r['invert']} | {r['tp_mult']:.2f} | {r['sl_mult']:.2f} | "
                f"{r['n_trades']} | {r['wr']:.3f} | {r['pf']:.3f} | "
                f"{r['expectancy_r']:.3f} | {r['max_dd_r']:.1f} | {r['calmar']:.4f} |"
            )
        lines.append("")
    elif not df_b.is_empty():
        lines += [
            "No Phase B strict survivors. Top 10 raw (closest to gate):",
            "",
            "| # | sym | tf | setup | session | inv | tp | sl | n | wr | pf | exp_R | calmar |",
            "|---|-----|-----|-------|---------|-----|-----|-----|---|-----|-----|-------|--------|",
        ]
        closest = _closest_to_gate(df_b).head(10)
        for rank, r in enumerate(closest.iter_rows(named=True), 1):
            lines.append(
                f"| {rank} | {r['symbol']} | {r['tf']} | {r['setup_type']} | {r['session']} "
                f"| {r['invert']} | {r['tp_mult']:.2f} | {r['sl_mult']:.2f} | "
                f"{r['n_trades']} | {r['wr']:.3f} | {r['pf']:.3f} | "
                f"{r['expectancy_r']:.3f} | {r['calmar']:.4f} |"
            )
        lines.append("")
    else:
        lines.append("No Phase B survivors at all.\n")

    # Distribution stats for Phase B raw survivors
    if not df_b.is_empty():
        lines += ["### Phase B Distribution (raw survivors)", ""] + _distribution_stats(df_b, "Phase B raw") + [""]

    # --- Phase F section ---
    lines += [
        "## Phase F Re-run (M1 entries)",
        "",
        f"- Total backtests: **{f_total_backtests}**",
        f"- Raw survivors (Phase A gate WR>=0.50 PF>=1.0): **{len(df_f)}**",
        f"- Strict survivors (Phase K gate): **{len(strict_f)}**",
        "",
    ]
    if not strict_f.is_empty():
        lines += [
            "### Top 20 Phase F strict survivors (by Calmar)",
            "",
            "| # | sym | setup | session | inv | tp | sl | n | wr | pf | exp_R | dd_R | calmar |",
            "|---|-----|-------|---------|-----|-----|-----|---|-----|-----|-------|------|--------|",
        ]
        for rank, r in enumerate(strict_f.head(20).iter_rows(named=True), 1):
            lines.append(
                f"| {rank} | {r['symbol']} | {r['setup_type']} | {r['session']} "
                f"| {r['invert']} | {r['tp_mult']:.2f} | {r['sl_mult']:.2f} | "
                f"{r['n_trades']} | {r['wr']:.3f} | {r['pf']:.3f} | "
                f"{r['expectancy_r']:.3f} | {r['max_dd_r']:.1f} | {r['calmar']:.4f} |"
            )
        lines.append("")
    elif not df_f.is_empty():
        lines += [
            "No Phase F strict survivors. Top 10 raw (closest to gate):",
            "",
            "| # | sym | setup | session | inv | tp | sl | n | wr | pf | exp_R | calmar |",
            "|---|-----|-------|---------|-----|-----|-----|---|-----|-----|-------|--------|",
        ]
        closest = _closest_to_gate(df_f).head(10)
        for rank, r in enumerate(closest.iter_rows(named=True), 1):
            lines.append(
                f"| {rank} | {r['symbol']} | {r['setup_type']} | {r['session']} "
                f"| {r['invert']} | {r['tp_mult']:.2f} | {r['sl_mult']:.2f} | "
                f"{r['n_trades']} | {r['wr']:.3f} | {r['pf']:.3f} | "
                f"{r['expectancy_r']:.3f} | {r['calmar']:.4f} |"
            )
        lines.append("")
    else:
        lines.append("No Phase F survivors at all.\n")

    # Distribution stats for Phase F raw survivors
    if not df_f.is_empty():
        lines += ["### Phase F Distribution (raw survivors)", ""] + _distribution_stats(df_f, "Phase F raw") + [""]

    # --- Combined strict survivors ---
    lines += [
        "## COMBINED Strict Survivors (WR>=0.60 AND PF>=1.30 AND n>=30)",
        "",
    ]
    if not combined.is_empty():
        lines += [
            f"Total: **{len(combined)}** survivors across Phase B + F",
            "",
            "### Top 30 by Calmar",
            "",
            "| # | phase | sym | tf | setup | session | inv | tp | sl | n | wr | pf | exp_R | dd_R | calmar |",
            "|---|-------|-----|-----|-------|---------|-----|-----|-----|---|-----|-----|-------|------|--------|",
        ]
        for rank, r in enumerate(combined.head(30).iter_rows(named=True), 1):
            lines.append(
                f"| {rank} | {r.get('phase', '?')} | {r['symbol']} | {r['tf']} "
                f"| {r['setup_type']} | {r['session']} "
                f"| {r['invert']} | {r['tp_mult']:.2f} | {r['sl_mult']:.2f} | "
                f"{r['n_trades']} | {r['wr']:.3f} | {r['pf']:.3f} | "
                f"{r['expectancy_r']:.3f} | {r['max_dd_r']:.1f} | {r['calmar']:.4f} |"
            )
        lines.append("")

        # Per-setup distribution
        lines += ["### Combined distribution", ""] + _distribution_stats(combined, "Combined strict") + [""]
    else:
        lines += [
            "**0 strict survivors** across both phases.",
            "",
            "### Closest-to-gate candidates (by phase)",
            "",
        ]
        if not df_b.is_empty():
            lines += ["**Phase B (best per key):**", ""]
            closest_b = _closest_to_gate(df_b).head(15)
            lines += [
                "| sym | tf | setup | session | inv | tp | sl | n | wr | pf | calmar |",
                "|-----|-----|-------|---------|-----|-----|-----|---|-----|-----|--------|",
            ]
            for r in closest_b.iter_rows(named=True):
                lines.append(
                    f"| {r['symbol']} | {r['tf']} | {r['setup_type']} | {r['session']} "
                    f"| {r['invert']} | {r['tp_mult']:.2f} | {r['sl_mult']:.2f} | "
                    f"{r['n_trades']} | {r['wr']:.3f} | {r['pf']:.3f} | {r['calmar']:.4f} |"
                )
            lines.append("")
        if not df_f.is_empty():
            lines += ["**Phase F (best per key):**", ""]
            closest_f = _closest_to_gate(df_f).head(15)
            lines += [
                "| sym | setup | session | inv | tp | sl | n | wr | pf | calmar |",
                "|-----|-------|---------|-----|-----|-----|---|-----|-----|--------|",
            ]
            for r in closest_f.iter_rows(named=True):
                lines.append(
                    f"| {r['symbol']} | {r['setup_type']} | {r['session']} "
                    f"| {r['invert']} | {r['tp_mult']:.2f} | {r['sl_mult']:.2f} | "
                    f"{r['n_trades']} | {r['wr']:.3f} | {r['pf']:.3f} | {r['calmar']:.4f} |"
                )
            lines.append("")

    out_path = Path(COMBINED_OUTPUT)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n[PhaseK] Combined report written to {out_path}", flush=True)

    # Persist combined parquet for downstream analysis
    if not combined.is_empty():
        pq_path = REPORTS_DIR / "math_discovery_m1_phase_k_combined.parquet"
        combined.write_parquet(pq_path)
        print(f"[PhaseK] Parquet saved to {pq_path}", flush=True)


def run() -> None:
    """Run Phase K: B + F with low friction, strict gate, combined report."""
    t_start = time.time()

    print("=" * 70, flush=True)
    print("[PhaseK] MATH Discovery Phase K — Low Friction (0.05/0.10)", flush=True)
    print(f"[PhaseK] Friction override: FX={_friction_for('EURUSD')} non-FX={_friction_for('XAUUSD')}", flush=True)
    print("=" * 70, flush=True)

    # --- Sanity test ---
    # Before full sweep: verify friction override is live by checking one combo
    # USDJPY M1 VELOCITY_ACCEL_GO ASIA TP=2.0 SL=1.0 INV=False
    # Phase F old friction for USDJPY: 0.30 (FX base 0.10 + 0.20 slippage)
    # Phase K new friction for USDJPY: 0.05 (FX, halved)
    # Expected: PF should improve from ~1.41 to ~1.50+
    print("\n[PhaseK][SANITY] Testing USDJPY friction override...", flush=True)
    try:
        from src.strategies_external.strategies.math_discovery import (
            _load_and_enrich_math_tf,
            _filter_by_session,
            _empty_trades,
            run_setup_backtest_m1,
            precompute_m1_arrays,
        )
        from src.strategies_external.data_loader import load_m1
        from src.engine.run_math_momentum import detect_setups as mom_detect
        from src.engine.indicator_validation import compute_metrics

        m1 = load_m1("USDJPY")
        if m1 is not None:
            m1_arrays = precompute_m1_arrays(m1)
            bars = _load_and_enrich_math_tf("USDJPY", "M1")
            all_setups = mom_detect(bars, "VELOCITY_ACCEL_GO")
            from src.domain.constants import INDICATOR_SESSIONS
            ses_setups = _filter_by_session(all_setups, "ASIA")
            friction_new = _friction_for("USDJPY")  # should be 0.05
            trades_new = run_setup_backtest_m1(
                setups=ses_setups, bars_signal_tf=bars, m1_df=None,
                setup_type="VELOCITY_ACCEL_GO", is_fade=False,
                tp_atr_mult=2.0, sl_atr_mult=1.0,
                session_end_hour_utc=INDICATOR_SESSIONS["ASIA"][1],
                friction_r=friction_new, symbol="USDJPY", signal_tf="M1",
                m1_arrays=m1_arrays, invert_direction=False,
            )
            m_new = compute_metrics(trades_new)
            print(
                f"[PhaseK][SANITY] USDJPY VELOCITY_ACCEL_GO ASIA TP=2.0 SL=1.0: "
                f"friction={friction_new} WR={m_new.wr:.3f} PF={m_new.profit_factor:.3f} "
                f"expR={m_new.expectancy_r:.3f}",
                flush=True,
            )
            print(
                "[PhaseK][SANITY] Old friction was 0.30 (0.10+0.20slippage). "
                f"New = {friction_new}. PF expected to rise from ~1.41 toward ~1.50+",
                flush=True,
            )
        else:
            print("[PhaseK][SANITY] SKIP: USDJPY M1 data not available", flush=True)
    except Exception as e:
        print(f"[PhaseK][SANITY] ERROR: {e}", flush=True)

    # --- Phase B ---
    print("\n" + "=" * 70, flush=True)
    print("[PhaseK] Starting Phase B re-run (M15/H1/H4)...", flush=True)
    t_b = time.time()
    df_b = _mod.run_discovery_phase_b(output_path=PHASE_B_OUTPUT)
    b_runtime = time.time() - t_b

    # Count backtests from the module run (approximation from total)
    n_grid = len(_mod.PHASE_B_GRID)
    from src.domain.constants import INDICATOR_SESSIONS as _SESSIONS
    from src.strategies_external.strategies.math_discovery import (
        MOMENTUM_SETUP_TYPES, FADE_SETUP_TYPES,
    )
    b_total = (
        len(_mod.M1_AVAILABLE) * len(_mod.TFS)
        * (len(MOMENTUM_SETUP_TYPES) + len(FADE_SETUP_TYPES))
        * len(_SESSIONS)
        * n_grid * 2
    )
    print(f"[PhaseK] Phase B done: {len(df_b)} raw survivors in {b_runtime:.0f}s", flush=True)

    # --- Phase F ---
    print("\n" + "=" * 70, flush=True)
    print("[PhaseK] Starting Phase F re-run (M1 entries)...", flush=True)
    t_f = time.time()
    df_f = _mod.run_discovery_phase_f(output_path=PHASE_F_OUTPUT)
    f_runtime = time.time() - t_f
    f_total = 4 * len(MOMENTUM_SETUP_TYPES + FADE_SETUP_TYPES) * 5 * n_grid * 2
    print(f"[PhaseK] Phase F done: {len(df_f)} raw survivors in {f_runtime:.0f}s", flush=True)

    # --- Combined report ---
    print("\n[PhaseK] Writing combined report...", flush=True)
    _write_combined_report(
        df_b=df_b,
        df_f=df_f,
        b_total_backtests=b_total,
        f_total_backtests=f_total,
        b_runtime=b_runtime,
        f_runtime=f_runtime,
    )

    total_elapsed = time.time() - t_start
    print(f"\n[PhaseK] ALL DONE in {total_elapsed:.0f}s ({total_elapsed/60:.1f} min)", flush=True)

    # Final print summary
    strict_b = _apply_strict_gate(df_b)
    strict_f = _apply_strict_gate(df_f)
    total_strict = len(strict_b) + len(strict_f)
    print(f"[PhaseK] Strict survivors (WR>={PK_MIN_WR} PF>={PK_MIN_PF}): "
          f"B={len(strict_b)} + F={len(strict_f)} = {total_strict}", flush=True)
    print(f"[PhaseK] Reports: {PHASE_B_OUTPUT}, {PHASE_F_OUTPUT}, {COMBINED_OUTPUT}", flush=True)


if __name__ == "__main__":
    run()
