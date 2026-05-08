"""MATH Discovery Phase K3 — re-run Phase K-B + K-F + K2 with expanded 15-sym universe.

Phase K-B (M15/H1/H4) — 14 syms (all except EURAUD which has no M15):
    14 × 3 TFs × 12 setups × 5 sessions × 7 TP/SL × 2 invert = 35,280 backtests
    Filter: WR >= 0.60 AND PF >= 1.30 AND n >= 30

Phase K-F (M1 entries) — 15 syms (all 14 + EURAUD):
    15 × 12 setups × 5 sessions × 7 TP/SL × 2 invert = 12,600 backtests
    Filter: same gate

Phase K3-2 (refine TP/SL grid 49) on combined B+F survivors:
    seeds × 7 TP × 7 SL = 49 combos per seed
    Filter: same gate

Friction: 0.05R FX (8 symbols) / 0.10R non-FX

New symbols vs Phase K:
    Phase K had: EURUSD, USDJPY, GBPAUD + 7 non-FX = 10 syms
    Phase K3 adds: GBPUSD, AUDUSD, GBPJPY, EURJPY (B+F) and EURAUD (F only)

Usage:
    python -u -m src.strategies_external.runners.run_math_discovery_m1_phase_k3
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
    MOMENTUM_SETUP_TYPES,
    FADE_SETUP_TYPES,
)
from src.strategies_external.runners.run_math_discovery_m1 import (
    compute_phase_a_metrics,
    PHASE_B_GRID,
)
from src.engine.run_math_momentum import detect_setups as mom_detect
from src.engine.run_math_fade import detect_setups as fade_detect

# ── Symbols ────────────────────────────────────────────────────────────────────

# Extended FX set (vs Phase K which only had EURUSD/USDJPY/GBPAUD)
FX_SYMS = {"EURUSD", "USDJPY", "GBPAUD", "GBPUSD", "AUDUSD", "GBPJPY", "EURJPY", "EURAUD"}

# Phase K-B: 14 syms — all that have M15 data (EURAUD excluded, no M15)
PHASE_B_SYMS = (
    "EURUSD", "USDJPY", "GBPAUD", "GBPUSD", "AUDUSD", "GBPJPY", "EURJPY",
    "XAUUSD", "XAGUSD", "WTI", "BRENT", "NATGAS", "SP500", "NASDAQ100",
)

# Phase K-F: 15 syms — all M1 available (includes EURAUD)
PHASE_F_SYMS = (*PHASE_B_SYMS, "EURAUD")

TFS = ("M15", "H1", "H4")
SESSIONS = ("ASIA", "LONDON", "NY", "LONDON_NY", "ALL_DAY")

# ── Gates ──────────────────────────────────────────────────────────────────────
K3_MIN_TRADES = 30
K3_MIN_WR = 0.60
K3_MIN_PF = 1.30

# Phase A (raw) gate — same as base module
PA_MIN_TRADES = 30   # same value as K3_MIN_TRADES; kept separate for clarity
PA_MIN_WR = 0.50
PA_MIN_PF = 1.0

# ── TP/SL grid (7x7 for K3-2) ─────────────────────────────────────────────────
TP_GRID = [0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0]
SL_GRID = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0]

# ── Output paths ──────────────────────────────────────────────────────────────
REPORTS_DIR = Path("reports/external")
PHASE_B_OUTPUT = REPORTS_DIR / "math_discovery_m1_phase_k3_b.md"
PHASE_F_OUTPUT = REPORTS_DIR / "math_discovery_m1_phase_k3_f.md"
COMBINED_OUTPUT = REPORTS_DIR / "math_discovery_m1_phase_k3_combined.md"
K3_2_OUTPUT_MD = REPORTS_DIR / "math_discovery_m1_phase_k3_2.md"
K3_2_OUTPUT_PARQUET = REPORTS_DIR / "math_discovery_m1_phase_k3_2.parquet"
COMBINED_PARQUET = REPORTS_DIR / "math_discovery_m1_phase_k3_combined.parquet"


# ── Helpers ────────────────────────────────────────────────────────────────────

def _friction_for(sym: str) -> float:
    """Realistic Vantage friction: 0.05R FX / 0.10R non-FX."""
    return 0.05 if sym in FX_SYMS else 0.10


def _session_end_hour(session: str) -> int:
    return INDICATOR_SESSIONS[session][1]


def _apply_strict_gate(df: pl.DataFrame) -> pl.DataFrame:
    """Filter to K3 strict gate: WR >= 0.60 AND PF >= 1.30 AND n_trades >= 30."""
    if df.is_empty():
        return df
    return df.filter(
        (pl.col("wr") >= K3_MIN_WR)
        & (pl.col("pf") >= K3_MIN_PF)
        & (pl.col("n_trades") >= K3_MIN_TRADES)
    )


def _distribution_stats(df: pl.DataFrame, label: str) -> list[str]:
    """Return markdown lines with p50/p75/p90/max of WR and PF."""
    if df.is_empty():
        return [f"**{label}**: no data"]
    wr = sorted(df["wr"].to_list())
    pf = sorted(df["pf"].to_list())
    n = len(wr)

    def pct(lst: list[float], p: float) -> float:
        idx = min(int(p * n), n - 1)
        return round(lst[idx], 4)

    return [
        f"**{label}** (n={n})",
        f"  - WR: p50={pct(wr, 0.50):.3f}  p75={pct(wr, 0.75):.3f}  "
        f"p90={pct(wr, 0.90):.3f}  max={max(wr):.3f}",
        f"  - PF: p50={pct(pf, 0.50):.3f}  p75={pct(pf, 0.75):.3f}  "
        f"p90={pct(pf, 0.90):.3f}  max={max(pf):.3f}",
    ]


def _closest_to_gate(df: pl.DataFrame) -> pl.DataFrame:
    """For each (sym, tf, setup_type, session, invert): row with highest PF × WR."""
    if df.is_empty():
        return df
    return (
        df.with_columns((pl.col("pf") * pl.col("wr")).alias("_score"))
        .sort("_score", descending=True)
        .group_by(["symbol", "tf", "setup_type", "session", "invert"])
        .agg(pl.all().first())
        .drop("_score")
        .sort("calmar", descending=True)
    )


# ── Phase K3-B ─────────────────────────────────────────────────────────────────

def run_phase_k3_b() -> tuple[pl.DataFrame, int, float]:
    """Run Phase K-B over 14 syms × 3 TFs.

    Returns (df_raw_survivors, total_backtests, runtime_s).
    Raw survivors pass PA gate (WR>=0.50, PF>=1.0). Strict gate applied later.
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    n_grid = len(PHASE_B_GRID)
    all_setups_count = len(MOMENTUM_SETUP_TYPES) + len(FADE_SETUP_TYPES)
    total = len(PHASE_B_SYMS) * len(TFS) * all_setups_count * len(SESSIONS) * n_grid * 2
    print(f"[K3-B] Starting: {len(PHASE_B_SYMS)} syms × {len(TFS)} TFs × "
          f"{all_setups_count} setups × {len(SESSIONS)} sessions × {n_grid} R:R × 2 invert = "
          f"~{total:,} backtests", flush=True)

    rows: list[dict] = []
    backtest_count = 0
    t0 = time.time()

    for sym in PHASE_B_SYMS:
        m1 = load_m1(sym)
        if m1 is None:
            print(f"[K3-B][SKIP] {sym}: no M1 data", flush=True)
            continue
        m1_arrays = precompute_m1_arrays(m1)
        friction = _friction_for(sym)
        print(f"[K3-B] {sym}: friction={friction} M1_rows={len(m1):,}", flush=True)

        for tf in TFS:
            try:
                bars = _load_and_enrich_math_tf(sym, tf)
            except Exception as e:
                print(f"[K3-B][SKIP] {sym} {tf}: {e}", flush=True)
                continue

            for is_fade, setups_list in [(False, MOMENTUM_SETUP_TYPES), (True, FADE_SETUP_TYPES)]:
                detect_fn = fade_detect if is_fade else mom_detect
                for setup_type in setups_list:
                    try:
                        all_sig = detect_fn(bars, setup_type)
                    except Exception as exc:
                        print(f"[K3-B][SKIP] {sym}/{tf}/{setup_type}: {exc}", flush=True)
                        continue

                    for session in SESSIONS:
                        ses_setups = _filter_by_session(all_sig, session)
                        if len(ses_setups) < K3_MIN_TRADES:
                            backtest_count += n_grid * 2
                            continue

                        for tp, sl in PHASE_B_GRID:
                            for invert in (False, True):
                                backtest_count += 1
                                if backtest_count % 2000 == 0:
                                    elapsed = time.time() - t0
                                    pct = 100 * backtest_count / total
                                    rate = backtest_count / elapsed if elapsed > 0 else 1
                                    eta = (total - backtest_count) / rate if rate > 0 else 0
                                    print(
                                        f"[K3-B] {backtest_count:,}/{total:,} ({pct:.0f}%) "
                                        f"elapsed={elapsed:.0f}s ETA={eta:.0f}s survivors={len(rows)}",
                                        flush=True,
                                    )
                                try:
                                    trades = run_setup_backtest_m1(
                                        setups=ses_setups,
                                        bars_signal_tf=bars,
                                        m1_df=None,
                                        setup_type=setup_type,
                                        is_fade=is_fade,
                                        tp_atr_mult=tp,
                                        sl_atr_mult=sl,
                                        session_end_hour_utc=_session_end_hour(session),
                                        friction_r=friction,
                                        symbol=sym,
                                        signal_tf=tf,
                                        m1_arrays=m1_arrays,
                                        invert_direction=invert,
                                    )
                                except Exception:
                                    continue
                                m_dict = compute_phase_a_metrics(trades)
                                if (
                                    m_dict["n_trades"] >= PA_MIN_TRADES
                                    and m_dict["wr"] >= PA_MIN_WR
                                    and m_dict["pf"] >= PA_MIN_PF
                                ):
                                    rows.append({
                                        "symbol": sym, "tf": tf,
                                        "setup_type": setup_type, "session": session,
                                        "is_fade": is_fade, "invert": invert,
                                        "tp_mult": tp, "sl_mult": sl,
                                        **m_dict,
                                    })

    runtime_s = time.time() - t0
    print(
        f"\n[K3-B] Done: {backtest_count:,} backtests in {runtime_s:.0f}s ({runtime_s/60:.1f} min)",
        flush=True,
    )
    print(f"[K3-B] Raw survivors (PA gate): {len(rows)}", flush=True)

    if not rows:
        df = pl.DataFrame()
    else:
        df = pl.DataFrame(rows).sort("calmar", descending=True)

    # Write phase B report
    strict_b = _apply_strict_gate(df)
    _write_phase_b_report(df, strict_b, backtest_count, runtime_s)

    return df, backtest_count, runtime_s


def _write_phase_b_report(
    df_raw: pl.DataFrame,
    df_strict: pl.DataFrame,
    total_backtests: int,
    runtime_s: float,
) -> None:
    lines = [
        "# MATH Discovery Phase K3-B — M15/H1/H4 over 14 symbols",
        "",
        f"- Symbols: {', '.join(PHASE_B_SYMS)}",
        f"- Friction: 0.05R FX (8 syms) / 0.10R non-FX",
        f"- Total backtests: **{total_backtests:,}**",
        f"- Raw survivors (WR>={PA_MIN_WR} PF>={PA_MIN_PF}): **{len(df_raw)}**",
        f"- Strict survivors (WR>={K3_MIN_WR} PF>={K3_MIN_PF} n>={K3_MIN_TRADES}): **{len(df_strict)}**",
        f"- Runtime: {runtime_s:.0f}s ({runtime_s/60:.1f} min)",
        "",
    ]
    if not df_strict.is_empty():
        lines += [
            "## Top 20 strict survivors (by Calmar)",
            "",
            "| # | sym | tf | setup | session | inv | tp | sl | n | wr | pf | exp_R | dd_R | calmar |",
            "|---|-----|-----|-------|---------|-----|-----|-----|---|-----|-----|-------|------|--------|",
        ]
        for rank, r in enumerate(df_strict.head(20).iter_rows(named=True), 1):
            lines.append(
                f"| {rank} | {r['symbol']} | {r['tf']} | {r['setup_type']} | {r['session']} "
                f"| {r['invert']} | {r['tp_mult']:.2f} | {r['sl_mult']:.2f} | "
                f"{r['n_trades']} | {r['wr']:.3f} | {r['pf']:.3f} | "
                f"{r['expectancy_r']:.3f} | {r['max_dd_r']:.1f} | {r['calmar']:.4f} |"
            )
        lines.append("")
    elif not df_raw.is_empty():
        lines += ["No strict survivors. Top 10 raw (closest to gate):"]
        lines += [
            "| # | sym | tf | setup | session | inv | tp | sl | n | wr | pf | calmar |",
            "|---|-----|-----|-------|---------|-----|-----|-----|---|-----|-----|--------|",
        ]
        for rank, r in enumerate(_closest_to_gate(df_raw).head(10).iter_rows(named=True), 1):
            lines.append(
                f"| {rank} | {r['symbol']} | {r['tf']} | {r['setup_type']} | {r['session']} "
                f"| {r['invert']} | {r['tp_mult']:.2f} | {r['sl_mult']:.2f} | "
                f"{r['n_trades']} | {r['wr']:.3f} | {r['pf']:.3f} | {r['calmar']:.4f} |"
            )
        lines.append("")
    else:
        lines.append("No Phase B survivors at all.\n")
    if not df_raw.is_empty():
        lines += ["## Distribution (raw survivors)", ""] + _distribution_stats(df_raw, "K3-B raw") + [""]
    PHASE_B_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[K3-B] Report: {PHASE_B_OUTPUT}", flush=True)


# ── Phase K3-F ─────────────────────────────────────────────────────────────────

def run_phase_k3_f() -> tuple[pl.DataFrame, int, float]:
    """Run Phase K-F over 15 syms (M1 entries).

    Returns (df_raw_survivors, total_backtests, runtime_s).
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    n_grid = len(PHASE_B_GRID)
    all_setups_count = len(MOMENTUM_SETUP_TYPES) + len(FADE_SETUP_TYPES)
    total = len(PHASE_F_SYMS) * all_setups_count * len(SESSIONS) * n_grid * 2
    print(f"[K3-F] Starting: {len(PHASE_F_SYMS)} syms × {all_setups_count} setups × "
          f"{len(SESSIONS)} sessions × {n_grid} R:R × 2 invert = ~{total:,} backtests", flush=True)

    rows: list[dict] = []
    backtest_count = 0
    t0 = time.time()
    setups_cache: dict[tuple[str, str, bool], pl.DataFrame] = {}

    for sym in PHASE_F_SYMS:
        m1 = load_m1(sym)
        if m1 is None:
            print(f"[K3-F][SKIP] {sym}: no M1 data", flush=True)
            continue
        m1_arrays = precompute_m1_arrays(m1)
        friction = _friction_for(sym)
        print(f"[K3-F] {sym}: friction={friction} M1_rows={len(m1):,} — enriching M1...", flush=True)
        try:
            bars = _load_and_enrich_math_tf(sym, "M1")
        except Exception as e:
            print(f"[K3-F][SKIP] {sym} M1 enrich: {e}", flush=True)
            continue
        print(f"[K3-F] {sym}: M1 enriched ({time.time()-t0:.0f}s elapsed)", flush=True)

        for is_fade, setup_list in [(False, MOMENTUM_SETUP_TYPES), (True, FADE_SETUP_TYPES)]:
            detect_fn = fade_detect if is_fade else mom_detect
            for setup_type in setup_list:
                sk = (sym, setup_type, is_fade)
                if sk not in setups_cache:
                    try:
                        setups_cache[sk] = detect_fn(bars, setup_type)
                    except Exception as exc:
                        print(f"[K3-F][SKIP] {sym}/M1/{setup_type}: {exc}", flush=True)
                        setups_cache[sk] = pl.DataFrame()
                all_sig = setups_cache[sk]
                if all_sig.is_empty():
                    continue

                for session in SESSIONS:
                    ses_setups = _filter_by_session(all_sig, session)
                    if len(ses_setups) < K3_MIN_TRADES:
                        backtest_count += n_grid * 2
                        continue

                    for tp, sl in PHASE_B_GRID:
                        for invert in (False, True):
                            backtest_count += 1
                            if backtest_count % 500 == 0:
                                elapsed = time.time() - t0
                                pct = 100 * backtest_count / total
                                rate = backtest_count / elapsed if elapsed > 0 else 1
                                eta = (total - backtest_count) / rate if rate > 0 else 0
                                print(
                                    f"[K3-F] {backtest_count:,}/{total:,} ({pct:.0f}%) "
                                    f"elapsed={elapsed:.0f}s ETA={eta:.0f}s survivors={len(rows)}",
                                    flush=True,
                                )
                            try:
                                trades = run_setup_backtest_m1(
                                    setups=ses_setups,
                                    bars_signal_tf=bars,
                                    m1_df=None,
                                    setup_type=setup_type,
                                    is_fade=is_fade,
                                    tp_atr_mult=tp,
                                    sl_atr_mult=sl,
                                    session_end_hour_utc=_session_end_hour(session),
                                    friction_r=friction,
                                    symbol=sym,
                                    signal_tf="M1",
                                    m1_arrays=m1_arrays,
                                    invert_direction=invert,
                                )
                            except Exception:
                                continue
                            m_dict = compute_phase_a_metrics(trades)
                            if (
                                m_dict["n_trades"] >= PA_MIN_TRADES
                                and m_dict["wr"] >= PA_MIN_WR
                                and m_dict["pf"] >= PA_MIN_PF
                            ):
                                rows.append({
                                    "symbol": sym, "tf": "M1",
                                    "setup_type": setup_type, "session": session,
                                    "is_fade": is_fade, "invert": invert,
                                    "tp_mult": tp, "sl_mult": sl,
                                    **m_dict,
                                })

    runtime_s = time.time() - t0
    print(
        f"\n[K3-F] Done: {backtest_count:,} backtests in {runtime_s:.0f}s ({runtime_s/60:.1f} min)",
        flush=True,
    )
    print(f"[K3-F] Raw survivors (PA gate): {len(rows)}", flush=True)

    if not rows:
        df = pl.DataFrame()
    else:
        df = pl.DataFrame(rows).sort("calmar", descending=True)

    strict_f = _apply_strict_gate(df)
    _write_phase_f_report(df, strict_f, backtest_count, runtime_s)

    return df, backtest_count, runtime_s


def _write_phase_f_report(
    df_raw: pl.DataFrame,
    df_strict: pl.DataFrame,
    total_backtests: int,
    runtime_s: float,
) -> None:
    lines = [
        "# MATH Discovery Phase K3-F — M1 entries over 15 symbols",
        "",
        f"- Symbols: {', '.join(PHASE_F_SYMS)}",
        f"- Friction: 0.05R FX (8 syms) / 0.10R non-FX",
        f"- Total backtests: **{total_backtests:,}**",
        f"- Raw survivors (WR>={PA_MIN_WR} PF>={PA_MIN_PF}): **{len(df_raw)}**",
        f"- Strict survivors (WR>={K3_MIN_WR} PF>={K3_MIN_PF} n>={K3_MIN_TRADES}): **{len(df_strict)}**",
        f"- Runtime: {runtime_s:.0f}s ({runtime_s/60:.1f} min)",
        "",
    ]
    if not df_strict.is_empty():
        lines += [
            "## Top 20 strict survivors (by Calmar)",
            "",
            "| # | sym | setup | session | inv | tp | sl | n | wr | pf | exp_R | dd_R | calmar |",
            "|---|-----|-------|---------|-----|-----|-----|---|-----|-----|-------|------|--------|",
        ]
        for rank, r in enumerate(df_strict.head(20).iter_rows(named=True), 1):
            lines.append(
                f"| {rank} | {r['symbol']} | {r['setup_type']} | {r['session']} "
                f"| {r['invert']} | {r['tp_mult']:.2f} | {r['sl_mult']:.2f} | "
                f"{r['n_trades']} | {r['wr']:.3f} | {r['pf']:.3f} | "
                f"{r['expectancy_r']:.3f} | {r['max_dd_r']:.1f} | {r['calmar']:.4f} |"
            )
        lines.append("")
    elif not df_raw.is_empty():
        lines += ["No strict survivors. Top 10 raw (closest to gate):"]
        lines += [
            "| # | sym | setup | session | inv | tp | sl | n | wr | pf | calmar |",
            "|---|-----|-------|---------|-----|-----|-----|---|-----|-----|--------|",
        ]
        for rank, r in enumerate(_closest_to_gate(df_raw).head(10).iter_rows(named=True), 1):
            lines.append(
                f"| {rank} | {r['symbol']} | {r['setup_type']} | {r['session']} "
                f"| {r['invert']} | {r['tp_mult']:.2f} | {r['sl_mult']:.2f} | "
                f"{r['n_trades']} | {r['wr']:.3f} | {r['pf']:.3f} | {r['calmar']:.4f} |"
            )
        lines.append("")
    else:
        lines.append("No Phase F survivors at all.\n")
    if not df_raw.is_empty():
        lines += ["## Distribution (raw survivors)", ""] + _distribution_stats(df_raw, "K3-F raw") + [""]
    PHASE_F_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[K3-F] Report: {PHASE_F_OUTPUT}", flush=True)


# ── Phase K3-2 (7×7 grid on combined B+F survivors) ───────────────────────────

def run_phase_k3_2(combined_seeds_df: pl.DataFrame) -> pl.DataFrame:
    """Run Phase K3-2: 7×7 TP/SL grid on combined B+F survivors.

    Args:
        combined_seeds_df: combined strict survivors from K3-B + K3-F

    Returns:
        DataFrame of all K3-2 strict survivors.
    """
    if combined_seeds_df.is_empty():
        print("[K3-2] No seeds to refine — skipping.", flush=True)
        return pl.DataFrame()

    seeds = (
        combined_seeds_df
        .unique(subset=["symbol", "tf", "setup_type", "session", "is_fade", "invert"])
        .to_dicts()
    )
    n_seeds = len(seeds)
    total_backtests = n_seeds * len(TP_GRID) * len(SL_GRID)
    print(f"[K3-2] Seeds: {n_seeds} | Grid: {len(TP_GRID)}×{len(SL_GRID)}={len(TP_GRID)*len(SL_GRID)} per seed", flush=True)
    print(f"[K3-2] Total backtests: {total_backtests:,}", flush=True)
    print(f"[K3-2] TP grid: {TP_GRID}", flush=True)
    print(f"[K3-2] SL grid: {SL_GRID}", flush=True)

    m1_cache: dict[str, dict] = {}
    bars_cache: dict[tuple, pl.DataFrame] = {}
    setups_cache: dict[tuple, pl.DataFrame] = {}

    rows: list[dict] = []
    done = 0
    t0 = time.time()

    for idx, seed in enumerate(seeds, 1):
        sym: str = seed["symbol"]
        tf: str = seed["tf"]
        setup: str = seed["setup_type"]
        ses: str = seed["session"]
        is_fade: bool = bool(seed["is_fade"])
        invert: bool = bool(seed["invert"])

        # Lazy-load M1 arrays
        if sym not in m1_cache:
            m1_df = load_m1(sym)
            if m1_df is None:
                print(f"[K3-2] SKIP {sym}: no M1 data", flush=True)
                continue
            m1_cache[sym] = precompute_m1_arrays(m1_df)
        m1_arr = m1_cache[sym]

        # Lazy-load enriched bars
        bk = (sym, tf)
        if bk not in bars_cache:
            try:
                bars_cache[bk] = _load_and_enrich_math_tf(sym, tf)
            except Exception as e:
                print(f"[K3-2] SKIP {sym} {tf}: {e}", flush=True)
                continue
        bars = bars_cache[bk]

        # Lazy-load setups
        sk = (sym, tf, setup, is_fade)
        if sk not in setups_cache:
            detect_fn = fade_detect if is_fade else mom_detect
            try:
                setups_cache[sk] = detect_fn(bars, setup)
            except Exception as e:
                print(f"[K3-2] SKIP {sym}/{tf}/{setup}: {e}", flush=True)
                setups_cache[sk] = pl.DataFrame()
        all_sig = setups_cache[sk]

        ses_setups = _filter_by_session(all_sig, ses)
        if len(ses_setups) < K3_MIN_TRADES:
            print(
                f"[K3-2] SKIP seed {idx}/{n_seeds}: {sym} {tf} {setup} {ses} "
                f"inv={invert} — only {len(ses_setups)} signals",
                flush=True,
            )
            continue

        friction = _friction_for(sym)
        end_h = _session_end_hour(ses)
        seed_survivors = 0
        print(
            f"[K3-2] Seed {idx}/{n_seeds}: {sym} {tf} {setup} {ses} "
            f"is_fade={is_fade} inv={invert} friction={friction} signals={len(ses_setups)}",
            flush=True,
        )

        for tp in TP_GRID:
            for sl in SL_GRID:
                try:
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
                except Exception:
                    done += 1
                    continue
                m = compute_phase_a_metrics(trades)
                done += 1
                if (
                    m["n_trades"] >= K3_MIN_TRADES
                    and m["wr"] >= K3_MIN_WR
                    and m["pf"] >= K3_MIN_PF
                ):
                    rows.append({
                        "symbol": sym, "tf": tf,
                        "setup_type": setup, "session": ses,
                        "is_fade": is_fade, "invert": invert,
                        "tp_mult": tp, "sl_mult": sl,
                        **m,
                    })
                    seed_survivors += 1

        elapsed = time.time() - t0
        rate = done / elapsed if elapsed > 0 else 1
        eta = (total_backtests - done) / rate if rate > 0 else 0
        print(
            f"[K3-2]   -> seed survivors={seed_survivors} | total={len(rows)} | "
            f"ETA={eta:.0f}s",
            flush=True,
        )

    runtime_s = time.time() - t0
    print(f"\n[K3-2] Done: {done:,} backtests in {runtime_s:.0f}s ({runtime_s/60:.1f} min)", flush=True)
    print(f"[K3-2] Strict survivors: {len(rows)}", flush=True)

    if not rows:
        return pl.DataFrame()

    df = pl.DataFrame(rows).sort("calmar", descending=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    df.write_parquet(K3_2_OUTPUT_PARQUET)
    print(f"[K3-2] Parquet saved: {K3_2_OUTPUT_PARQUET}", flush=True)

    _write_k3_2_report(df, n_seeds, total_backtests, runtime_s)
    return df


def _write_k3_2_report(
    df: pl.DataFrame,
    n_seeds: int,
    total_backtests: int,
    runtime_s: float,
) -> None:
    if df.is_empty():
        lines = [
            "# Phase K3-2 — TP/SL 7×7 grid on K3 combined survivors",
            "",
            f"- Seeds: {n_seeds}",
            f"- Backtests: {total_backtests:,}",
            f"- Runtime: {runtime_s:.0f}s ({runtime_s/60:.1f} min)",
            "",
            "**0 strict survivors.**",
        ]
        K3_2_OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return

    best_per_seed = (
        df.sort("calmar", descending=True)
        .group_by(["symbol", "tf", "setup_type", "session", "is_fade", "invert"])
        .agg(pl.all().first())
        .sort("calmar", descending=True)
    )
    best_by_pf = df.sort("pf", descending=True)

    lines = [
        "# Phase K3-2 — TP/SL 7×7 grid on K3 combined survivors",
        "",
        "## Summary",
        "",
        f"- Seeds refined: **{n_seeds}**",
        f"- Grid: TP={TP_GRID}",
        f"- Grid: SL={SL_GRID}",
        f"- Backtests: **{total_backtests:,}** ({n_seeds} × {len(TP_GRID)*len(SL_GRID)} combos)",
        f"- Friction: 0.05R FX ({', '.join(sorted(FX_SYMS))}) / 0.10R non-FX",
        f"- Gate: WR>={K3_MIN_WR} AND PF>={K3_MIN_PF} AND n>={K3_MIN_TRADES}",
        f"- Runtime: **{runtime_s:.0f}s ({runtime_s/60:.1f} min)**",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Strict survivors total | **{len(df)}** |",
        f"| Best per seed (unique strategies) | **{len(best_per_seed)}** |",
        f"| Seeds with NO survivors | **{n_seeds - len(best_per_seed)}** |",
        "",
    ]

    # Top 30 best per seed by Calmar
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

    # Top 30 by PF
    lines += [
        "## Top 30 by PF",
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

    # Distribution
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
            "| Metric | p50 | p75 | p90 | max |",
            "|--------|-----|-----|-----|-----|",
            f"| WR | {pct(wr_list, 0.50):.3f} | {pct(wr_list, 0.75):.3f} | {pct(wr_list, 0.90):.3f} | {max(wr_list):.3f} |",
            f"| PF | {pct(pf_list, 0.50):.3f} | {pct(pf_list, 0.75):.3f} | {pct(pf_list, 0.90):.3f} | {max(pf_list):.3f} |",
            f"| Calmar | {pct(cal_list, 0.50):.4f} | {pct(cal_list, 0.75):.4f} | {pct(cal_list, 0.90):.4f} | {max(cal_list):.4f} |",
            "",
        ]

    K3_2_OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[K3-2] Report: {K3_2_OUTPUT_MD}", flush=True)


# ── Combined report ────────────────────────────────────────────────────────────

def _write_combined_report(
    df_b_raw: pl.DataFrame,
    df_f_raw: pl.DataFrame,
    df_k3_2: pl.DataFrame,
    b_total: int,
    f_total: int,
    b_runtime: float,
    f_runtime: float,
    k3_2_runtime: float,
) -> None:
    """Write the master combined report for K3."""
    strict_b = _apply_strict_gate(df_b_raw)
    strict_f = _apply_strict_gate(df_f_raw)

    # Combined strict B+F seeds (used as input for K3-2)
    parts = []
    if not strict_b.is_empty():
        parts.append(strict_b.with_columns(pl.lit("B").alias("phase")))
    if not strict_f.is_empty():
        parts.append(strict_f.with_columns(pl.lit("F").alias("phase")))
    combined_seeds = pl.concat(parts, how="diagonal_relaxed") if parts else pl.DataFrame()

    # K3-2 best per seed
    if not df_k3_2.is_empty():
        best_per_seed_k3_2 = (
            df_k3_2.sort("calmar", descending=True)
            .group_by(["symbol", "tf", "setup_type", "session", "is_fade", "invert"])
            .agg(pl.all().first())
            .sort("calmar", descending=True)
        )
    else:
        best_per_seed_k3_2 = pl.DataFrame()

    total_runtime = b_runtime + f_runtime + k3_2_runtime
    total_backtests = b_total + f_total + (
        len(combined_seeds.unique(subset=["symbol", "tf", "setup_type", "session", "is_fade", "invert"]))
        * len(TP_GRID) * len(SL_GRID)
        if not combined_seeds.is_empty() else 0
    )

    lines = [
        "# MATH Discovery Phase K3 — Expanded 15-Symbol Universe",
        "",
        f"Generated: Phase K-B (14 syms) + Phase K-F (15 syms) + Phase K3-2 (7×7 grid refinement)",
        "",
        "## Summary",
        "",
        f"| Phase | Syms | Backtests | Raw Survivors | Strict (WR>={K3_MIN_WR} PF>={K3_MIN_PF}) | Runtime |",
        f"|-------|------|-----------|---------------|----------------------------------------|---------|",
        f"| K3-B (M15/H1/H4) | {len(PHASE_B_SYMS)} | {b_total:,} | {len(df_b_raw)} | {len(strict_b)} | {b_runtime:.0f}s ({b_runtime/60:.1f}m) |",
        f"| K3-F (M1) | {len(PHASE_F_SYMS)} | {f_total:,} | {len(df_f_raw)} | {len(strict_f)} | {f_runtime:.0f}s ({f_runtime/60:.1f}m) |",
        f"| K3-2 (7×7 grid) | — | ~{len(combined_seeds.unique(subset=['symbol','tf','setup_type','session','is_fade','invert']) if not combined_seeds.is_empty() else pl.DataFrame()) * len(TP_GRID) * len(SL_GRID):,} | — | {len(df_k3_2)} | {k3_2_runtime:.0f}s ({k3_2_runtime/60:.1f}m) |",
        f"| **TOTAL** | — | — | — | **{len(best_per_seed_k3_2)} unique** | **{total_runtime/60:.1f}m** |",
        "",
        f"New symbols vs Phase K: GBPUSD, AUDUSD, GBPJPY, EURJPY (B+F), EURAUD (F only)",
        f"Extended FX friction (0.05R): {', '.join(sorted(FX_SYMS))}",
        "",
    ]

    # K3-2 top 30
    if not best_per_seed_k3_2.is_empty():
        lines += [
            "## K3-2 Top 30 best-per-seed (by Calmar)",
            "",
            "| # | sym | tf | setup | session | inv | tp | sl | n | wr | pf | exp_R | dd_R | calmar |",
            "|---|-----|-----|-------|---------|-----|-----|-----|---|-----|-----|-------|------|--------|",
        ]
        for rank, r in enumerate(best_per_seed_k3_2.head(30).iter_rows(named=True), 1):
            lines.append(
                f"| {rank} | {r['symbol']} | {r['tf']} | {r['setup_type']} | {r['session']} "
                f"| {r['invert']} | {r['tp_mult']:.2f} | {r['sl_mult']:.2f} | "
                f"{r['n_trades']} | {r['wr']:.3f} | {r['pf']:.3f} | "
                f"{r['expectancy_r']:.3f} | {r['max_dd_r']:.1f} | {r['calmar']:.4f} |"
            )
        lines.append("")
        lines += ["## K3-2 Distribution", ""] + _distribution_stats(best_per_seed_k3_2, "K3-2 best-per-seed") + [""]
    else:
        lines += [
            "**K3-2: 0 strict survivors.** Combined strict seeds from B+F were input.",
            "",
            "### Combined B+F strict survivors (seeds)",
            "",
        ]
        if not combined_seeds.is_empty():
            lines += [
                "| # | phase | sym | tf | setup | session | inv | tp | sl | n | wr | pf | calmar |",
                "|---|-------|-----|-----|-------|---------|-----|-----|-----|---|-----|-----|--------|",
            ]
            for rank, r in enumerate(combined_seeds.head(30).iter_rows(named=True), 1):
                lines.append(
                    f"| {rank} | {r.get('phase','?')} | {r['symbol']} | {r['tf']} "
                    f"| {r['setup_type']} | {r['session']} | {r['invert']} "
                    f"| {r['tp_mult']:.2f} | {r['sl_mult']:.2f} | "
                    f"{r['n_trades']} | {r['wr']:.3f} | {r['pf']:.3f} | {r['calmar']:.4f} |"
                )
            lines.append("")

    COMBINED_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[K3] Combined report: {COMBINED_OUTPUT}", flush=True)

    # Save combined parquet (K3-2 results if any, else B+F strict survivors)
    if not df_k3_2.is_empty():
        df_k3_2.write_parquet(COMBINED_PARQUET)
        print(f"[K3] Combined parquet (K3-2 results): {COMBINED_PARQUET}", flush=True)
    elif not combined_seeds.is_empty():
        combined_seeds.write_parquet(COMBINED_PARQUET)
        print(f"[K3] Combined parquet (B+F seeds): {COMBINED_PARQUET}", flush=True)


# ── Entry point ────────────────────────────────────────────────────────────────

def main() -> None:
    t_total = time.time()

    print("=" * 70, flush=True)
    print("[K3] MATH Discovery Phase K3 — Expanded 15-Symbol Universe", flush=True)
    print(f"[K3] Phase B syms ({len(PHASE_B_SYMS)}): {PHASE_B_SYMS}", flush=True)
    print(f"[K3] Phase F syms ({len(PHASE_F_SYMS)}): {PHASE_F_SYMS}", flush=True)
    print(f"[K3] FX_SYMS (0.05R): {sorted(FX_SYMS)}", flush=True)
    print(f"[K3] Gate: WR>={K3_MIN_WR} PF>={K3_MIN_PF} n>={K3_MIN_TRADES}", flush=True)
    print("=" * 70, flush=True)

    # ── Phase K3-B ────────────────────────────────────────────────────────────
    print("\n[K3] === PHASE K3-B (M15/H1/H4 × 14 syms) ===", flush=True)
    df_b_raw, b_total, b_runtime = run_phase_k3_b()

    # ── Phase K3-F ────────────────────────────────────────────────────────────
    print("\n[K3] === PHASE K3-F (M1 × 15 syms) ===", flush=True)
    df_f_raw, f_total, f_runtime = run_phase_k3_f()

    # ── Combine strict survivors as seeds for K3-2 ────────────────────────────
    strict_b = _apply_strict_gate(df_b_raw)
    strict_f = _apply_strict_gate(df_f_raw)

    print(f"\n[K3] K3-B strict survivors: {len(strict_b)}", flush=True)
    print(f"[K3] K3-F strict survivors: {len(strict_f)}", flush=True)

    parts = []
    if not strict_b.is_empty():
        parts.append(strict_b)
    if not strict_f.is_empty():
        parts.append(strict_f)
    if parts:
        combined_seeds = pl.concat(parts, how="diagonal_relaxed")
    else:
        combined_seeds = pl.DataFrame()
    print(f"[K3] Combined K3-B+K3-F strict survivors (input to K3-2): {len(combined_seeds)}", flush=True)

    # ── Phase K3-2 ────────────────────────────────────────────────────────────
    print("\n[K3] === PHASE K3-2 (7×7 TP/SL grid on combined survivors) ===", flush=True)
    t_k3_2 = time.time()
    df_k3_2 = run_phase_k3_2(combined_seeds)
    k3_2_runtime = time.time() - t_k3_2

    # ── Combined report ───────────────────────────────────────────────────────
    print("\n[K3] Writing combined report...", flush=True)
    _write_combined_report(
        df_b_raw=df_b_raw,
        df_f_raw=df_f_raw,
        df_k3_2=df_k3_2,
        b_total=b_total,
        f_total=f_total,
        b_runtime=b_runtime,
        f_runtime=f_runtime,
        k3_2_runtime=k3_2_runtime,
    )

    total_elapsed = time.time() - t_total

    # ── Final console summary ──────────────────────────────────────────────────
    print("\n" + "=" * 70, flush=True)
    print("[K3] PHASE K3 COMPLETE", flush=True)
    print(f"[K3] Total elapsed: {total_elapsed:.0f}s ({total_elapsed/60:.1f} min)", flush=True)
    print(f"[K3] K3-B: {b_total:,} backtests | {len(strict_b)} strict survivors", flush=True)
    print(f"[K3] K3-F: {f_total:,} backtests | {len(strict_f)} strict survivors", flush=True)

    if not df_k3_2.is_empty():
        best_per_seed = (
            df_k3_2.sort("calmar", descending=True)
            .group_by(["symbol", "tf", "setup_type", "session", "is_fade", "invert"])
            .agg(pl.all().first())
            .sort("calmar", descending=True)
        )
        print(
            f"[K3] K3-2: {len(df_k3_2)} strict survivors | {len(best_per_seed)} unique best-per-seed",
            flush=True,
        )
        print(f"\n[K3] Top 15 K3-2 best-per-seed by Calmar:", flush=True)
        print(
            f"{'sym':10s} {'tf':4s} {'setup':25s} {'ses':12s} {'inv':5s} "
            f"{'tp':5s} {'sl':5s} {'n':4s} {'wr':5s} {'pf':5s} {'calmar':8s}",
            flush=True,
        )
        for r in best_per_seed.head(15).iter_rows(named=True):
            print(
                f"{r['symbol']:10s} {r['tf']:4s} {r['setup_type']:25s} {r['session']:12s} "
                f"{str(r['invert']):5s} {r['tp_mult']:5.2f} {r['sl_mult']:5.2f} "
                f"{r['n_trades']:4d} {r['wr']:5.3f} {r['pf']:5.3f} {r['calmar']:8.4f}",
                flush=True,
            )
    else:
        print("[K3] K3-2: 0 strict survivors", flush=True)

    print(f"\n[K3] Reports:", flush=True)
    print(f"  {PHASE_B_OUTPUT}", flush=True)
    print(f"  {PHASE_F_OUTPUT}", flush=True)
    print(f"  {K3_2_OUTPUT_MD}", flush=True)
    print(f"  {COMBINED_OUTPUT}", flush=True)
    print("=" * 70, flush=True)


if __name__ == "__main__":
    main()
