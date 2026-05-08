"""ORB break-fade Phase I — exhaustive R:R grid on Phase G base seeds.

For each of the 4 unique (sym, magic_time, duration) combos from Phase G:
  - ATR windows: 5, 10, 14, 20
  - TP multipliers: 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0  (7 values)
  - SL multipliers: 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0  (7 values)
  - All 49 TP x SL combos
  - Exit mode: V1 baseline only (fastest)

Total (12 Phase G rows x 4 atr_w x 49 rr combos = but deduped to 4 unique seeds):
  4 base seeds x 4 atr_w x 49 TP/SL = 784 backtests (base signal generation cached)

STRICT filter (both required):
  WR >= 0.60
  PF >= 1.30
  n_trades >= 30

If zero survivors: report closest-to-gate per seed.

Usage:
    python -u -m src.strategies_external.runners.run_orb_breakfade_phase_i
"""
from __future__ import annotations

import math
import time
from dataclasses import replace as _replace
from pathlib import Path

import polars as pl

from src.strategies_external.common.metrics import evaluate
from src.strategies_external.common.signal import Signal
from src.strategies_external.constants import friction_for
from src.strategies_external.data_loader import load_csv, load_m1
from src.strategies_external.runners.run_orb_breakfade_phase_h import (
    _precompute_m1_arrays,
    _run_orb_with_alt_exit,
)
from src.strategies_external.strategies.orb_breakfade import ORBBreakFadeAdapter

REPORTS_DIR = Path("reports/external")

ATR_WINDOWS = (5, 10, 14, 20)
TP_GRID = (0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0)
SL_GRID = (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0)

# Strict Phase I gates
MIN_TRADES = 30
MIN_WR = 0.60
MIN_PF = 1.30
RISK_PCT = 0.005


def _attach_rr(sigs: list[Signal], tp_mult: float, sl_mult: float) -> list[Signal]:
    """Attach TP/SL (ATR multiples) to a list of base signals."""
    out: list[Signal] = []
    for s in sigs:
        atr = s.indicator_anchors["atr_14"]
        if s.side == "short":
            stop = s.entry_price + sl_mult * atr
            tp1 = s.entry_price - tp_mult * atr
        else:
            stop = s.entry_price - sl_mult * atr
            tp1 = s.entry_price + tp_mult * atr
        out.append(_replace(s, stop=stop, tp1=tp1, tp2=None))
    return out


def run_phase_i(
    output_stem: str = "reports/external/orb_breakfade_phase_i",
) -> pl.DataFrame:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    phase_g_path = REPORTS_DIR / "orb_breakfade_phase_g.parquet"
    if not phase_g_path.exists():
        raise FileNotFoundError(f"Phase G parquet not found: {phase_g_path}")

    survivors_g = pl.read_parquet(phase_g_path)
    print(f"[PhaseI] Loaded {len(survivors_g)} Phase G rows", flush=True)

    # Unique base seeds: (sym, magic_time, duration)
    unique_seeds = (
        survivors_g.select(["symbol", "magic_time", "duration"])
        .unique()
        .sort(["symbol", "magic_time", "duration"])
        .to_dicts()
    )
    n_seeds = len(unique_seeds)
    n_rr = len(TP_GRID) * len(SL_GRID)
    total_expected = n_seeds * len(ATR_WINDOWS) * n_rr
    print(
        f"[PhaseI] {n_seeds} unique seeds x {len(ATR_WINDOWS)} ATR windows x "
        f"{n_rr} TP/SL combos = {total_expected} backtests",
        flush=True,
    )
    print(
        f"[PhaseI] Strict gates: WR>={MIN_WR} AND PF>={MIN_PF} AND n>={MIN_TRADES}",
        flush=True,
    )

    adapter = ORBBreakFadeAdapter()

    # Cache M15 + M1 per symbol.
    m15_cache: dict[str, pl.DataFrame | None] = {}
    m1_cache: dict[str, pl.DataFrame | None] = {}

    # Signal cache: (sym, magic_time, duration, atr_w) -> list[Signal]
    sig_cache: dict[tuple, list[Signal]] = {}

    rows: list[dict] = []
    # Track ALL results (not just survivors) for closest-to-gate analysis
    all_results: list[dict] = []

    backtest_count = 0
    t0 = time.time()

    for seed in unique_seeds:
        sym = seed["symbol"]
        magic_time = seed["magic_time"]
        duration = seed["duration"]
        friction_r = friction_for(sym)

        # Load data once per symbol.
        if sym not in m15_cache:
            try:
                m15_cache[sym] = load_csv(sym, "M15")
            except FileNotFoundError:
                print(f"[PhaseI][SKIP] {sym} no M15 data", flush=True)
                m15_cache[sym] = None
        if sym not in m1_cache:
            m1_df = load_m1(sym)
            m1_cache[sym] = m1_df
            if m1_df is None:
                print(f"[PhaseI][SKIP] {sym} no M1 data", flush=True)

        df_m15 = m15_cache.get(sym)
        m1_df = m1_cache.get(sym)
        if df_m15 is None or m1_df is None:
            print(f"[PhaseI][SKIP] {sym} missing data — skipping seed", flush=True)
            backtest_count += len(ATR_WINDOWS) * n_rr
            continue

        m1_arrays = _precompute_m1_arrays(m1_df)

        for atr_w in ATR_WINDOWS:
            sig_key = (sym, magic_time, duration, atr_w)

            if sig_key not in sig_cache:
                try:
                    base_sigs = adapter.generate_signals_for_combo(
                        df_m15, m1_df, sym, magic_time, duration, atr_window=atr_w
                    )
                    sig_cache[sig_key] = base_sigs
                    print(
                        f"[PhaseI] {sym} {magic_time}/{duration}m atr_w={atr_w}: "
                        f"{len(base_sigs)} signals generated",
                        flush=True,
                    )
                except Exception as e:
                    print(
                        f"[PhaseI][ERR] {sym} {magic_time}/{duration} atr_w={atr_w}: {e}",
                        flush=True,
                    )
                    sig_cache[sig_key] = []

            base_sigs = sig_cache[sig_key]

            if len(base_sigs) < MIN_TRADES:
                print(
                    f"[PhaseI][SKIP] {sym} {magic_time}/{duration}m atr_w={atr_w}: "
                    f"only {len(base_sigs)} signals < {MIN_TRADES}",
                    flush=True,
                )
                backtest_count += n_rr
                continue

            for tp_mult in TP_GRID:
                for sl_mult in SL_GRID:
                    backtest_count += 1
                    if backtest_count % 100 == 0:
                        elapsed = time.time() - t0
                        pct = 100.0 * backtest_count / total_expected
                        print(
                            f"[PhaseI] {backtest_count}/{total_expected} ({pct:.0f}%) "
                            f"— {elapsed:.0f}s",
                            flush=True,
                        )

                    sigs_rr = _attach_rr(base_sigs, tp_mult, sl_mult)

                    try:
                        trades = _run_orb_with_alt_exit(
                            sigs_rr,
                            m1_arrays,
                            exit_mode="baseline",
                            friction_r=friction_r,
                        )
                    except Exception as e:
                        print(
                            f"[PhaseI][ERR] {sym} {magic_time}/{duration}m "
                            f"atr={atr_w} tp={tp_mult} sl={sl_mult}: {e}",
                            flush=True,
                        )
                        continue

                    if len(trades) == 0:
                        continue

                    m = evaluate(trades)

                    result = {
                        "symbol": sym,
                        "magic_time": magic_time,
                        "duration": duration,
                        "atr_window": atr_w,
                        "tp_mult": tp_mult,
                        "sl_mult": sl_mult,
                        "n_trades": m["n_trades"],
                        "wr": m["win_rate"],
                        "pf": m["profit_factor"],
                        "expectancy_r": m["expectancy_R"],
                        "max_dd_r": m["max_dd_R"],
                        "calmar": m.get("calmar", 0.0),
                        "total_r": m["total_R"],
                        "sharpe": m.get("sharpe", 0.0),
                    }
                    all_results.append(result)

                    if (
                        m["n_trades"] >= MIN_TRADES
                        and m["win_rate"] >= MIN_WR
                        and m["profit_factor"] >= MIN_PF
                    ):
                        rows.append(result)

    elapsed = time.time() - t0
    print(
        f"\n[PhaseI] complete in {elapsed:.0f}s ({elapsed / 60:.1f} min)"
        f" — {len(rows)} survivors / {backtest_count} backtests",
        flush=True,
    )

    df_survivors = (
        pl.DataFrame(rows).sort("calmar", descending=True)
        if rows
        else pl.DataFrame()
    )
    df_all = (
        pl.DataFrame(all_results).sort("calmar", descending=True)
        if all_results
        else pl.DataFrame()
    )

    _write_report(
        df_survivors, df_all, backtest_count, elapsed,
        output_stem, survivors_g, unique_seeds,
    )
    return df_survivors


def _write_report(
    df: pl.DataFrame,
    df_all: pl.DataFrame,
    backtest_count: int,
    elapsed: float,
    output_stem: str,
    survivors_g: pl.DataFrame,
    unique_seeds: list[dict],
) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out_md = Path(f"{output_stem}.md")

    n_survivors = len(df)

    # Save survivors parquet (even if empty, save df_all for analysis)
    if not df.is_empty():
        df.write_parquet(f"{output_stem}.parquet")
    if not df_all.is_empty():
        df_all.write_parquet(f"{output_stem}_all.parquet")

    lines = [
        "# Phase I — High-WR R:R Grid Exploration",
        "",
        f"- Backtests: {backtest_count}",
        f"- Survivors (WR>={MIN_WR} AND PF>={MIN_PF} AND n>={MIN_TRADES}): {n_survivors}",
        f"- Runtime: {elapsed:.0f}s ({elapsed / 60:.1f} min)",
        f"- ATR windows: {list(ATR_WINDOWS)}",
        f"- TP grid: {list(TP_GRID)}",
        f"- SL grid: {list(SL_GRID)}",
        f"- Total TP x SL combos: {len(TP_GRID) * len(SL_GRID)}",
        "",
    ]

    if not df.is_empty():
        # TOP 30 by Calmar
        lines += [
            "## TOP 30 by Calmar (WR>=0.60 AND PF>=1.30 survivors)",
            "",
            "| # | sym | magic | dur | atr_w | tp | sl | n | WR | PF | exp_R | dd_R | calmar |",
            "|---|-----|-------|-----|-------|----|----|---|-----|-----|-------|------|--------|",
        ]
        for rank, r in enumerate(df.sort("calmar", descending=True).head(30).iter_rows(named=True), 1):
            lines.append(
                f"| {rank} | {r['symbol']} | {r['magic_time']} | {r['duration']}m"
                f" | {r['atr_window']} | {r['tp_mult']:.2f} | {r['sl_mult']:.2f}"
                f" | {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.3f}"
                f" | {r['expectancy_r']:.4f} | {r['max_dd_r']:.1f} | {r['calmar']:.3f} |"
            )

        # TOP 30 by PF
        lines += [
            "",
            "## TOP 30 by PF (WR>=0.60 AND PF>=1.30 survivors)",
            "",
            "| # | sym | magic | dur | atr_w | tp | sl | n | WR | PF | exp_R | dd_R | calmar |",
            "|---|-----|-------|-----|-------|----|----|---|-----|-----|-------|------|--------|",
        ]
        for rank, r in enumerate(df.sort("pf", descending=True).head(30).iter_rows(named=True), 1):
            lines.append(
                f"| {rank} | {r['symbol']} | {r['magic_time']} | {r['duration']}m"
                f" | {r['atr_window']} | {r['tp_mult']:.2f} | {r['sl_mult']:.2f}"
                f" | {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.3f}"
                f" | {r['expectancy_r']:.4f} | {r['max_dd_r']:.1f} | {r['calmar']:.3f} |"
            )
    else:
        lines += [
            "## TOP 30 by Calmar",
            "",
            "No survivors met WR>=0.60 AND PF>=1.30 AND n>=30.",
            "",
            "## TOP 30 by PF",
            "",
            "No survivors met WR>=0.60 AND PF>=1.30 AND n>=30.",
            "",
        ]

    # Best per Phase-G base seed
    lines += [
        "",
        "## Best per Phase-G base seed (12 rows)",
        "",
        "Each Phase G row is (sym, magic_time, dur, tp_g, sl_g). Best qualifier found",
        "in Phase I grid for each seed's (sym, magic_time, dur) combo.",
        "",
        "| # | sym | magic | dur | tp_g | sl_g | best_i_tp | best_i_sl | best_atr_w | n | WR | PF | calmar | note |",
        "|---|-----|-------|-----|------|------|-----------|-----------|------------|---|-----|-----|--------|------|",
    ]

    for rank, g_row in enumerate(survivors_g.iter_rows(named=True), 1):
        sym = g_row["symbol"]
        magic = g_row["magic_time"]
        dur = g_row["duration"]
        tp_g = g_row["tp_atr_mult"]
        sl_g = g_row["sl_atr_mult"]

        # Find best qualifier for this seed (sym, magic, dur) in survivors
        if not df.is_empty():
            seed_survivors = df.filter(
                (pl.col("symbol") == sym)
                & (pl.col("magic_time") == magic)
                & (pl.col("duration") == dur)
            )
        else:
            seed_survivors = pl.DataFrame()

        if not seed_survivors.is_empty():
            best = seed_survivors.sort("calmar", descending=True).head(1).row(0, named=True)
            lines.append(
                f"| {rank} | {sym} | {magic} | {dur}m"
                f" | {tp_g:.1f} | {sl_g:.1f}"
                f" | {best['tp_mult']:.2f} | {best['sl_mult']:.2f} | {best['atr_window']}"
                f" | {best['n_trades']} | {best['wr']:.3f} | {best['pf']:.3f}"
                f" | {best['calmar']:.3f} | QUALIFIER |"
            )
        else:
            lines.append(
                f"| {rank} | {sym} | {magic} | {dur}m"
                f" | {tp_g:.1f} | {sl_g:.1f}"
                f" | — | — | —"
                f" | — | — | — | — | no qualifier |"
            )

    # Closest-to-gate section (informational)
    lines += [
        "",
        "## Closest-to-gate (informational, not survivors)",
        "",
        "For each unique (sym, magic_time, duration) seed, the combo with minimum",
        "Euclidean distance to (WR=0.60, PF=1.30) among ALL grid results.",
        "",
        "| sym | magic | dur | atr_w | tp | sl | n | WR | PF | dist_to_gate |",
        "|-----|-------|-----|-------|----|----|---|-----|-----|--------------|",
    ]

    if not df_all.is_empty():
        for seed in unique_seeds:
            sym = seed["symbol"]
            magic = seed["magic_time"]
            dur = seed["duration"]
            seed_all = df_all.filter(
                (pl.col("symbol") == sym)
                & (pl.col("magic_time") == magic)
                & (pl.col("duration") == dur)
            )
            if seed_all.is_empty():
                lines.append(f"| {sym} | {magic} | {dur}m | — | — | — | — | — | — | — |")
                continue

            # Compute distance = sqrt((wr-0.60)^2 + (pf-1.30)^2)
            seed_with_dist = seed_all.with_columns(
                (
                    (pl.col("wr") - MIN_WR).pow(2) + (pl.col("pf") - MIN_PF).pow(2)
                ).sqrt().alias("dist")
            ).sort("dist")

            closest = seed_with_dist.head(1).row(0, named=True)
            lines.append(
                f"| {sym} | {magic} | {dur}m"
                f" | {closest['atr_window']} | {closest['tp_mult']:.2f} | {closest['sl_mult']:.2f}"
                f" | {closest['n_trades']} | {closest['wr']:.3f} | {closest['pf']:.3f}"
                f" | {closest['dist']:.4f} |"
            )
    else:
        lines.append("No data available.")

    # Distribution summary (if no survivors)
    if df.is_empty() and not df_all.is_empty():
        lines += [
            "",
            "## Distribution of (WR, PF) across full grid",
            "",
        ]
        wrs = df_all["wr"].to_list()
        pfs = df_all["pf"].to_list()
        wrs_sorted = sorted(wrs)
        pfs_sorted = sorted(pfs)
        n = len(wrs_sorted)

        def pctile(lst, p):
            idx = int(len(lst) * p / 100)
            idx = min(idx, len(lst) - 1)
            return lst[idx]

        lines += [
            f"- Total grid results: {n}",
            f"- WR: p10={pctile(wrs_sorted,10):.3f}, p25={pctile(wrs_sorted,25):.3f}, "
            f"p50={pctile(wrs_sorted,50):.3f}, p75={pctile(wrs_sorted,75):.3f}, "
            f"p90={pctile(wrs_sorted,90):.3f}, max={max(wrs_sorted):.3f}",
            f"- PF: p10={pctile(pfs_sorted,10):.3f}, p25={pctile(pfs_sorted,25):.3f}, "
            f"p50={pctile(pfs_sorted,50):.3f}, p75={pctile(pfs_sorted,75):.3f}, "
            f"p90={pctile(pfs_sorted,90):.3f}, max={max(pfs_sorted):.3f}",
            "",
            "Rows with WR>=0.60 (regardless of PF):",
        ]
        wr60 = df_all.filter(pl.col("wr") >= MIN_WR)
        lines.append(f"  count={len(wr60)}")
        if not wr60.is_empty():
            pf_of_wr60 = sorted(wr60["pf"].to_list())
            lines.append(
                f"  PF of those: p50={pctile(pf_of_wr60,50):.3f}, "
                f"p75={pctile(pf_of_wr60,75):.3f}, p90={pctile(pf_of_wr60,90):.3f}, "
                f"max={max(pf_of_wr60):.3f}"
            )

        lines += ["", "Rows with PF>=1.30 (regardless of WR):"]
        pf130 = df_all.filter(pl.col("pf") >= MIN_PF)
        lines.append(f"  count={len(pf130)}")
        if not pf130.is_empty():
            wr_of_pf130 = sorted(pf130["wr"].to_list())
            lines.append(
                f"  WR of those: p50={pctile(wr_of_pf130,50):.3f}, "
                f"p75={pctile(wr_of_pf130,75):.3f}, p90={pctile(wr_of_pf130,90):.3f}, "
                f"max={max(wr_of_pf130):.3f}"
            )

    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[PhaseI] Report written to {out_md}", flush=True)


if __name__ == "__main__":
    import sys

    # ── Sanity test ──────────────────────────────────────────────────────────
    print(
        "[PhaseI] Sanity test: GBPAUD 15:00 120m atr_w=14 TP=0.5 SL=2.0",
        flush=True,
    )
    adapter = ORBBreakFadeAdapter()
    df_m15 = load_csv("GBPAUD", "M15")
    m1_df = load_m1("GBPAUD")

    if m1_df is not None:
        m1_arrays = _precompute_m1_arrays(m1_df)
        base_sigs = adapter.generate_signals_for_combo(
            df_m15, m1_df, "GBPAUD", "15:00", 120, atr_window=14
        )
        sigs_rr = _attach_rr(base_sigs, tp_mult=0.5, sl_mult=2.0)
        fr = friction_for("GBPAUD")
        trades = _run_orb_with_alt_exit(
            sigs_rr, m1_arrays, exit_mode="baseline", friction_r=fr
        )
        m = evaluate(trades)
        print(
            f"  Sanity: n={m['n_trades']} WR={m['win_rate']:.3f} "
            f"PF={m['profit_factor']:.3f} calmar={m['calmar']:.3f}",
            flush=True,
        )
        wr_ok = m["win_rate"] > 0.50
        n_ok = m["n_trades"] >= 30
        print(
            f"  WR > 0.50: {wr_ok}  (expected True — tight TP=0.5 vs SL=2.0)",
            flush=True,
        )
        print(f"  n >= 30: {n_ok}", flush=True)
    else:
        print("[PhaseI][WARN] No M1 data for GBPAUD — sanity test skipped", flush=True)

    print("\n[PhaseI] Starting full sweep...", flush=True)
    df_result = run_phase_i()
    print(f"\n[PhaseI] Done. Survivors: {len(df_result)}", flush=True)
