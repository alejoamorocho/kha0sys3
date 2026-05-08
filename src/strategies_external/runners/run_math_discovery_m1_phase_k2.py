"""MATH Discovery Phase K2 — exhaustive 7x7 TP/SL grid on 53 Phase K survivors.

For each unique base seed (symbol, tf, setup_type, session, is_fade, invert)
from the 68-row Phase K combined parquet, runs a 7x7 = 49 TP/SL grid with
realistic Vantage friction (0.05R FX / 0.10R non-FX).

Gate: WR >= 0.60 AND PF >= 1.30 AND n_trades >= 30.
Best per seed selected by Calmar.

Usage:
    python -u -m src.strategies_external.runners.run_math_discovery_m1_phase_k2
"""
from __future__ import annotations

import time
from pathlib import Path

import polars as pl

from src.domain.constants import INDICATOR_SESSIONS
from src.strategies_external.data_loader import load_m1
from src.strategies_external.strategies.math_discovery import (
    _load_and_enrich_math_tf,
    _filter_by_session,
    run_setup_backtest_m1,
    precompute_m1_arrays,
)
from src.strategies_external.runners.run_math_discovery_m1 import compute_phase_a_metrics
from src.engine.run_math_momentum import detect_setups as mom_detect
from src.engine.run_math_fade import detect_setups as fade_detect

# ── Config ─────────────────────────────────────────────────────────────────────

PHASE_K_PARQUET = Path("reports/external/math_discovery_m1_phase_k_combined.parquet")
REPORTS_DIR = Path("reports/external")
OUTPUT_MD = REPORTS_DIR / "math_discovery_m1_phase_k2.md"
OUTPUT_PARQUET = REPORTS_DIR / "math_discovery_m1_phase_k2.parquet"

# Grids
TP_GRID = [0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0]
SL_GRID = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0]

# Gate
K2_MIN_TRADES = 30
K2_MIN_WR = 0.60
K2_MIN_PF = 1.30

_FX_SET = {"EURUSD", "USDJPY", "GBPAUD"}


def _friction_for(sym: str) -> float:
    """Realistic Vantage friction: 0.05R FX / 0.10R non-FX."""
    return 0.05 if sym in _FX_SET else 0.10


def _session_end_hour(session: str) -> int:
    return INDICATOR_SESSIONS[session][1]


# ── Main sweep ─────────────────────────────────────────────────────────────────

def run_phase_k2() -> pl.DataFrame:
    """Run Phase K2 grid sweep. Returns DataFrame of all strict survivors."""
    survivors_k = pl.read_parquet(PHASE_K_PARQUET)
    seeds = (
        survivors_k
        .unique(subset=["symbol", "tf", "setup_type", "session", "is_fade", "invert"])
        .to_dicts()
    )
    n_seeds = len(seeds)
    total_backtests = n_seeds * len(TP_GRID) * len(SL_GRID)
    print(f"[K2] Unique seeds to refine: {n_seeds}", flush=True)
    print(f"[K2] Grid: {len(TP_GRID)} TP x {len(SL_GRID)} SL = {len(TP_GRID)*len(SL_GRID)} combos per seed", flush=True)
    print(f"[K2] Total backtests: {total_backtests}", flush=True)
    print(f"[K2] Friction: FX={_friction_for('EURUSD')} non-FX={_friction_for('XAUUSD')}", flush=True)
    print(f"[K2] Gate: WR>={K2_MIN_WR} PF>={K2_MIN_PF} n>={K2_MIN_TRADES}", flush=True)
    print("=" * 70, flush=True)

    # Caches keyed by (sym) / (sym, tf) / (sym, tf, setup_type, is_fade)
    m1_cache: dict[str, dict] = {}
    bars_cache: dict[tuple, pl.DataFrame] = {}
    setups_cache: dict[tuple, pl.DataFrame] = {}

    rows: list[dict] = []
    done_backtests = 0
    t_start = time.time()

    for seed_idx, seed in enumerate(seeds, 1):
        sym: str = seed["symbol"]
        tf: str = seed["tf"]
        setup: str = seed["setup_type"]
        ses: str = seed["session"]
        is_fade: bool = bool(seed["is_fade"])
        invert: bool = bool(seed["invert"])

        # ── Lazy-load M1 arrays ────────────────────────────────────────────────
        if sym not in m1_cache:
            m1_df = load_m1(sym)
            if m1_df is None:
                print(f"[K2] SKIP {sym}: M1 data not available", flush=True)
                continue
            m1_cache[sym] = precompute_m1_arrays(m1_df)
        m1_arr = m1_cache[sym]

        # ── Lazy-load enriched bars ────────────────────────────────────────────
        bk = (sym, tf)
        if bk not in bars_cache:
            bars_cache[bk] = _load_and_enrich_math_tf(sym, tf)
        bars = bars_cache[bk]

        # ── Lazy-load setups (filtered by session) ────────────────────────────
        sk = (sym, tf, setup, is_fade)
        if sk not in setups_cache:
            detect_fn = fade_detect if is_fade else mom_detect
            setups_cache[sk] = detect_fn(bars, setup)
        all_setups = setups_cache[sk]

        ses_setups = _filter_by_session(all_setups, ses)
        if len(ses_setups) < K2_MIN_TRADES:
            print(
                f"[K2] SKIP seed {seed_idx}/{n_seeds}: {sym} {tf} {setup} {ses} "
                f"inv={invert} — only {len(ses_setups)} setup signals (< {K2_MIN_TRADES})",
                flush=True,
            )
            continue

        friction = _friction_for(sym)
        end_h = _session_end_hour(ses)

        seed_survivors = 0
        print(
            f"[K2] Seed {seed_idx}/{n_seeds}: {sym} {tf} {setup} {ses} "
            f"is_fade={is_fade} inv={invert} | setups={len(ses_setups)} friction={friction}",
            flush=True,
        )

        for tp in TP_GRID:
            for sl in SL_GRID:
                trades = run_setup_backtest_m1(
                    setups=ses_setups,
                    bars_signal_tf=bars,
                    m1_df=None,
                    setup_type=setup,
                    is_fade=is_fade,
                    tp_atr_mult=tp,
                    sl_atr_mult=sl,
                    session_end_hour_utc=end_h,
                    friction_r=friction,
                    symbol=sym,
                    signal_tf=tf,
                    m1_arrays=m1_arr,
                    invert_direction=invert,
                )
                m = compute_phase_a_metrics(trades)
                done_backtests += 1

                if (
                    m["n_trades"] >= K2_MIN_TRADES
                    and m["wr"] >= K2_MIN_WR
                    and m["pf"] >= K2_MIN_PF
                ):
                    rows.append({
                        "symbol": sym,
                        "tf": tf,
                        "setup_type": setup,
                        "session": ses,
                        "is_fade": is_fade,
                        "invert": invert,
                        "tp_mult": tp,
                        "sl_mult": sl,
                        **m,
                    })
                    seed_survivors += 1

        elapsed = time.time() - t_start
        rate = done_backtests / elapsed if elapsed > 0 else 0
        remaining = (total_backtests - done_backtests) / rate if rate > 0 else 0
        print(
            f"[K2]   -> {seed_survivors} survivors | "
            f"total so far: {len(rows)} | "
            f"ETA: {remaining:.0f}s",
            flush=True,
        )

    print(f"\n[K2] Sweep done: {done_backtests} backtests in {time.time()-t_start:.0f}s", flush=True)
    print(f"[K2] Total strict survivors: {len(rows)}", flush=True)

    if not rows:
        return pl.DataFrame()

    return pl.DataFrame(rows)


# ── Report ─────────────────────────────────────────────────────────────────────

def _write_report(
    df_all: pl.DataFrame,
    survivors_k: pl.DataFrame,
    n_seeds: int,
    total_backtests: int,
    runtime_s: float,
) -> None:
    """Write Phase K2 markdown report."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    if df_all.is_empty():
        lines = [
            "# Phase K2 — TP/SL grid amplio sobre Phase K survivors",
            "",
            f"- Unique seeds refined: {n_seeds}",
            f"- Backtests: {total_backtests}",
            f"- Runtime: {runtime_s:.0f}s ({runtime_s/60:.1f} min)",
            "",
            "**0 strict survivors passed the gate.**",
            "",
        ]
        OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return

    # Best per seed (highest Calmar)
    best_per_seed = (
        df_all
        .sort("calmar", descending=True)
        .group_by(["symbol", "tf", "setup_type", "session", "is_fade", "invert"])
        .agg(pl.all().first())
        .sort("calmar", descending=True)
    )

    # Best by absolute PF
    best_by_pf = df_all.sort("pf", descending=True)

    # Per-seed comparison: Phase K original best vs K2 best
    # For Phase K, find original best row per seed
    pk_best = (
        survivors_k
        .sort("calmar", descending=True)
        .group_by(["symbol", "tf", "setup_type", "session", "is_fade", "invert"])
        .agg(pl.all().first())
    )

    lines = [
        "# Phase K2 — TP/SL grid amplio sobre Phase K survivors",
        "",
        "## Summary",
        "",
        f"- Unique seeds refined: **{n_seeds}**",
        f"- Backtests run: **{total_backtests}** ({n_seeds} seeds x {len(TP_GRID)*len(SL_GRID)} TP/SL combos)",
        f"- Grid: TP = {TP_GRID}",
        f"- Grid: SL = {SL_GRID}",
        f"- Friction: 0.05R FX (EURUSD/USDJPY/GBPAUD) / 0.10R non-FX",
        f"- Gate: WR >= {K2_MIN_WR} AND PF >= {K2_MIN_PF} AND n >= {K2_MIN_TRADES}",
        f"- Runtime: **{runtime_s:.0f}s ({runtime_s/60:.1f} min)**",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Strict survivors total | **{len(df_all)}** |",
        f"| Best per seed (unique strategies) | **{len(best_per_seed)}** |",
        f"| Seeds with NO survivors | **{n_seeds - len(best_per_seed)}** |",
        "",
    ]

    # --- Top 30 best per seed by Calmar ---
    lines += [
        "## Top 30 best-per-seed by Calmar",
        "",
        "| # | sym | tf | setup | session | inv | tp | sl | n | wr | pf | exp_R | dd_R | calmar |",
        "|---|-----|-----|-------|---------|-----|-----|-----|---|-----|-----|-------|------|--------|",
    ]
    for rank, r in enumerate(best_per_seed.head(30).iter_rows(named=True), 1):
        lines.append(
            f"| {rank} | {r['symbol']} | {r['tf']} | {r['setup_type']} | {r['session']} "
            f"| {r['invert']} | {r['tp_mult']:.2f} | {r['sl_mult']:.2f} | "
            f"{r['n_trades']} | {r['wr']:.3f} | {r['pf']:.3f} | "
            f"{r['expectancy_r']:.3f} | {r['max_dd_r']:.1f} | {r['calmar']:.4f} |"
        )
    lines.append("")

    # --- Top 30 by absolute PF ---
    lines += [
        "## Top 30 by absolute PF",
        "",
        "| # | sym | tf | setup | session | inv | tp | sl | n | wr | pf | exp_R | dd_R | calmar |",
        "|---|-----|-----|-------|---------|-----|-----|-----|---|-----|-----|-------|------|--------|",
    ]
    for rank, r in enumerate(best_by_pf.head(30).iter_rows(named=True), 1):
        lines.append(
            f"| {rank} | {r['symbol']} | {r['tf']} | {r['setup_type']} | {r['session']} "
            f"| {r['invert']} | {r['tp_mult']:.2f} | {r['sl_mult']:.2f} | "
            f"{r['n_trades']} | {r['wr']:.3f} | {r['pf']:.3f} | "
            f"{r['expectancy_r']:.3f} | {r['max_dd_r']:.1f} | {r['calmar']:.4f} |"
        )
    lines.append("")

    # --- Per-seed comparison Phase K vs K2 ---
    lines += [
        "## Per-seed comparison: Phase K original vs K2 best",
        "",
        "| sym | tf | setup | session | inv | K_tp | K_sl | K_wr | K_pf | K_calmar | K2_tp | K2_sl | K2_wr | K2_pf | K2_calmar | delta_calmar |",
        "|-----|-----|-------|---------|-----|------|------|------|------|----------|-------|-------|-------|-------|-----------|-------------|",
    ]

    # Build lookup for K2 best per seed
    k2_best_lookup: dict[tuple, dict] = {}
    for r in best_per_seed.iter_rows(named=True):
        key = (r["symbol"], r["tf"], r["setup_type"], r["session"], r["is_fade"], r["invert"])
        k2_best_lookup[key] = r

    # Iterate phase K original rows
    for r in pk_best.sort(["symbol", "tf", "setup_type", "session"]).iter_rows(named=True):
        key = (r["symbol"], r["tf"], r["setup_type"], r["session"], r["is_fade"], r["invert"])
        k2 = k2_best_lookup.get(key)
        if k2 is None:
            lines.append(
                f"| {r['symbol']} | {r['tf']} | {r['setup_type']} | {r['session']} "
                f"| {r['invert']} | {r['tp_mult']:.2f} | {r['sl_mult']:.2f} | "
                f"{r['wr']:.3f} | {r['pf']:.3f} | {r['calmar']:.4f} "
                f"| — | — | — | — | — | — |"
            )
        else:
            delta = k2["calmar"] - r["calmar"]
            delta_str = f"+{delta:.4f}" if delta >= 0 else f"{delta:.4f}"
            lines.append(
                f"| {r['symbol']} | {r['tf']} | {r['setup_type']} | {r['session']} "
                f"| {r['invert']} | {r['tp_mult']:.2f} | {r['sl_mult']:.2f} | "
                f"{r['wr']:.3f} | {r['pf']:.3f} | {r['calmar']:.4f} | "
                f"{k2['tp_mult']:.2f} | {k2['sl_mult']:.2f} | "
                f"{k2['wr']:.3f} | {k2['pf']:.3f} | {k2['calmar']:.4f} | {delta_str} |"
            )
    lines.append("")

    # --- Distribution stats ---
    if not best_per_seed.is_empty():
        wr_list = sorted(best_per_seed["wr"].to_list())
        pf_list = sorted(best_per_seed["pf"].to_list())
        cal_list = sorted(best_per_seed["calmar"].to_list())
        n = len(wr_list)

        def pct(lst: list, p: float) -> float:
            idx = min(int(p * n), n - 1)
            return lst[idx]

        lines += [
            "## Distribution (best per seed)",
            "",
            f"| Metric | p50 | p75 | p90 | max |",
            f"|--------|-----|-----|-----|-----|",
            f"| WR | {pct(wr_list, 0.50):.3f} | {pct(wr_list, 0.75):.3f} | {pct(wr_list, 0.90):.3f} | {max(wr_list):.3f} |",
            f"| PF | {pct(pf_list, 0.50):.3f} | {pct(pf_list, 0.75):.3f} | {pct(pf_list, 0.90):.3f} | {max(pf_list):.3f} |",
            f"| Calmar | {pct(cal_list, 0.50):.4f} | {pct(cal_list, 0.75):.4f} | {pct(cal_list, 0.90):.4f} | {max(cal_list):.4f} |",
            "",
        ]

    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[K2] Report written to {OUTPUT_MD}", flush=True)


# ── Entry point ────────────────────────────────────────────────────────────────

def run() -> None:
    """Main entry point for Phase K2."""
    t_start = time.time()
    print("=" * 70, flush=True)
    print("[K2] MATH Discovery Phase K2 — Exhaustive TP/SL Grid", flush=True)
    print(f"[K2] Input: {PHASE_K_PARQUET}", flush=True)
    print("=" * 70, flush=True)

    survivors_k = pl.read_parquet(PHASE_K_PARQUET)
    seeds = survivors_k.unique(
        subset=["symbol", "tf", "setup_type", "session", "is_fade", "invert"]
    )
    n_seeds = len(seeds)
    total_backtests = n_seeds * len(TP_GRID) * len(SL_GRID)

    df_all = run_phase_k2()

    runtime_s = time.time() - t_start

    if df_all.is_empty():
        print("[K2] WARNING: 0 strict survivors. Writing minimal report.", flush=True)
    else:
        # Save parquet
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        df_all.write_parquet(OUTPUT_PARQUET)
        print(f"[K2] Parquet saved: {OUTPUT_PARQUET}", flush=True)

    _write_report(
        df_all=df_all if not df_all.is_empty() else pl.DataFrame(),
        survivors_k=survivors_k,
        n_seeds=n_seeds,
        total_backtests=total_backtests,
        runtime_s=runtime_s,
    )

    print(f"\n[K2] ALL DONE in {runtime_s:.0f}s ({runtime_s/60:.1f} min)", flush=True)
    if not df_all.is_empty():
        best_per_seed = (
            df_all
            .sort("calmar", descending=True)
            .group_by(["symbol", "tf", "setup_type", "session", "is_fade", "invert"])
            .agg(pl.all().first())
        )
        print(f"[K2] Strict survivors: {len(df_all)} | Best per seed: {len(best_per_seed)}", flush=True)
        # Print top 15 for quick check
        print("\n[K2] Top 15 best-per-seed by Calmar:", flush=True)
        print(f"{'sym':10s} {'tf':4s} {'setup':25s} {'ses':12s} {'inv':5s} {'tp':5s} {'sl':5s} {'n':4s} {'wr':5s} {'pf':5s} {'calmar':8s}", flush=True)
        for r in best_per_seed.head(15).iter_rows(named=True):
            print(
                f"{r['symbol']:10s} {r['tf']:4s} {r['setup_type']:25s} {r['session']:12s} "
                f"{str(r['invert']):5s} {r['tp_mult']:5.2f} {r['sl_mult']:5.2f} "
                f"{r['n_trades']:4d} {r['wr']:5.3f} {r['pf']:5.3f} {r['calmar']:8.4f}",
                flush=True,
            )
    else:
        print("[K2] 0 strict survivors.", flush=True)


if __name__ == "__main__":
    run()
