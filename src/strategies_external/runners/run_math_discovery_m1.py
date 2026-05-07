"""MATH discovery Phase A — multi-TF (M15/H1/H4) signals with M1 intra-bar tracking.

Sweeps 10 symbols × 3 TFs × 12 setup_types × 5 sessions = 1800 combos.
For each combo, runs a MOMENTUM or FADE backtest using M1 bars for fill/exit tracking.

Phase-A gates: n_trades >= 30, WR >= 0.50, PF >= 1.0

Usage:
    python -m src.strategies_external.runners.run_math_discovery_m1
"""
from __future__ import annotations

import time
from pathlib import Path

import polars as pl

from src.domain.constants import (
    INDICATOR_SESSIONS,
    FRICTION_FX, FRICTION_INDEX, INDEX_SYMBOLS,
)
from src.strategies_external.data_loader import load_m1
from src.strategies_external.strategies.math_discovery import (
    _load_and_enrich_math_tf,
    _filter_by_session,
    run_setup_backtest_m1,
    precompute_m1_arrays,
    MOMENTUM_SETUP_TYPES,
    FADE_SETUP_TYPES,
)
from src.engine.run_math_momentum import detect_setups as momentum_detect_setups
from src.engine.run_math_fade import detect_setups as fade_detect_setups
from src.engine.indicator_validation import compute_metrics

# ── Config ─────────────────────────────────────────────────────────────────────

M1_AVAILABLE = (
    "EURUSD", "USDJPY", "GBPAUD", "XAUUSD", "XAGUSD",
    "WTI", "BRENT", "NATGAS", "SP500", "NASDAQ100",
)

TFS = ("M15", "H1", "H4")

# Phase-A gates (same as run_math_fade.py / run_math_momentum.py)
PA_MIN_TRADES = 30
PA_MIN_WR = 0.50
PA_MIN_PF = 1.0

REPORTS_DIR = Path("reports/external")

# Default R:R parameters
MOMENTUM_TP = 2.0
MOMENTUM_SL = 1.0
FADE_TP = 0.5
FADE_SL = 2.5

# Phase B grid (per-combo TP/SL search). Each (tp, sl) is in ATR multiples.
# Selected to span 3 regimes: high-RR mom, balanced, high-WR fade.
PHASE_B_GRID: tuple[tuple[float, float], ...] = (
    (2.0, 1.0),  # high-RR momentum (default mom)
    (1.5, 1.0),  # mid-RR momentum
    (1.0, 1.0),  # 1:1
    (0.7, 0.5),  # tight high-WR (MATH bot default style)
    (1.0, 2.0),  # mild fade
    (0.5, 2.5),  # default fade
    (1.5, 2.5),  # ratio close to 1:1.7 fade
)


# ── Helpers ────────────────────────────────────────────────────────────────────

def _friction_for(symbol: str) -> float:
    """Total friction = base + 0.2R slippage."""
    base = FRICTION_INDEX if symbol in INDEX_SYMBOLS else FRICTION_FX
    return base + 0.2  # total 0.3 FX / 0.4 non-FX


def _session_end_hour(session: str) -> int:
    return INDICATOR_SESSIONS[session][1]


def compute_phase_a_metrics(trades: pl.DataFrame) -> dict:
    """Compute Phase-A metrics dict from trades DataFrame."""
    if len(trades) == 0:
        return {
            "n_trades": 0, "wr": 0.0, "pf": 0.0,
            "expectancy_r": 0.0, "max_dd_r": 0.0,
            "calmar": 0.0, "trades_per_year": 0.0,
        }
    m = compute_metrics(trades)
    # Calmar: expectancy / max_dd (simple proxy; avoids dividing by 0)
    calmar = m.expectancy_r / m.max_dd_r if m.max_dd_r > 0 else 0.0
    return {
        "n_trades": m.n_trades,
        "wr": m.wr,
        "pf": m.profit_factor,
        "expectancy_r": m.expectancy_r,
        "max_dd_r": m.max_dd_r,
        "calmar": calmar,
        "trades_per_year": m.trades_per_year,
    }


def _write_phase_a_report(output_path: Path, df: pl.DataFrame, total_combos: int) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    survivors = df if not df.is_empty() else pl.DataFrame()

    lines = [
        "# MATH Discovery Phase A — M15+H1+H4 Signals / M1 Tracking",
        "",
        f"- Total combos tested: **{total_combos}**",
        f"- Survivors (Phase-A gates): **{len(survivors)}**",
        f"- Gates: n_trades >= {PA_MIN_TRADES}, WR >= {PA_MIN_WR}, PF >= {PA_MIN_PF}",
        "",
    ]

    if not survivors.is_empty():
        # Per-TF breakdown
        lines += ["## Per-TF Breakdown", ""]
        for tf in TFS:
            n = len(survivors.filter(pl.col("tf") == tf))
            lines.append(f"- **{tf}**: {n} survivors")
        lines.append("")

        # Per-symbol breakdown
        lines += ["## Per-Symbol Breakdown", ""]
        for sym in M1_AVAILABLE:
            n = len(survivors.filter(pl.col("symbol") == sym))
            if n > 0:
                lines.append(f"- **{sym}**: {n} survivors")
        lines.append("")

        # Per-setup breakdown
        lines += ["## Per-Setup-Type Breakdown", ""]
        all_setups = list(MOMENTUM_SETUP_TYPES) + list(FADE_SETUP_TYPES)
        for st in all_setups:
            n = len(survivors.filter(pl.col("setup_type") == st))
            if n > 0:
                kind = "MOM" if st in MOMENTUM_SETUP_TYPES else "FADE"
                lines.append(f"- **{st}** ({kind}): {n} survivors")
        lines.append("")

        # Top 50 by calmar
        top = survivors.sort("calmar", descending=True).head(50)
        lines += [
            "## Top 50 Survivors (by Calmar = Exp/MaxDD)",
            "",
            "| # | Symbol | TF | Setup | Session | Kind | Trades | WR | PF | Exp(R) | MaxDD(R) | Calmar | T/yr |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
        ]
        for rank, r in enumerate(top.iter_rows(named=True), 1):
            kind = "MOM" if r["setup_type"] in MOMENTUM_SETUP_TYPES else "FADE"
            lines.append(
                f"| {rank} | {r['symbol']} | {r['tf']} | {r['setup_type']} | {r['session']} "
                f"| {kind} | {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.2f} "
                f"| {r['expectancy_r']:.3f} | {r['max_dd_r']:.1f} "
                f"| {r['calmar']:.4f} | {r['trades_per_year']:.1f} |"
            )
    else:
        lines.append("No survivors passed Phase-A gates.")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[PhaseA] Report written to {output_path}")


# ── Main sweep ─────────────────────────────────────────────────────────────────

def run_discovery_phase_b(
    output_path: str = "reports/external/math_discovery_m1_phase_b.md",
    tp_sl_grid: tuple[tuple[float, float], ...] = PHASE_B_GRID,
) -> pl.DataFrame:
    """Phase B: per-combo grid search over (TP, SL) in ATR multiples.

    For each (sym, tf, setup, session), tests every (tp, sl) in the grid.
    Reports survivors that pass gates: n_trades >= 30, WR >= 0.50, PF >= 1.0.
    Each survivor is keyed by (sym, tf, setup, session, tp, sl).
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    n_grid = len(tp_sl_grid)
    total_combos = (
        len(M1_AVAILABLE) * len(TFS)
        * (len(MOMENTUM_SETUP_TYPES) + len(FADE_SETUP_TYPES))
        * len(INDICATOR_SESSIONS)
    )
    total = total_combos * n_grid
    print(f"[PhaseB] Starting grid sweep: {total_combos} combos × {n_grid} (TP,SL) = {total} backtests", flush=True)

    rows = []
    combo_count = 0
    backtest_count = 0
    t0 = time.time()

    for sym in M1_AVAILABLE:
        m1 = load_m1(sym)
        if m1 is None:
            print(f"[PhaseB][SKIP] {sym}: no M1 data", flush=True)
            combo_count += len(TFS) * (len(MOMENTUM_SETUP_TYPES) + len(FADE_SETUP_TYPES)) * len(INDICATOR_SESSIONS)
            backtest_count += combo_count * n_grid
            continue
        print(f"[PhaseB] {sym}: arrays...", flush=True)
        m1_arrays = precompute_m1_arrays(m1)
        friction = _friction_for(sym)

        for tf in TFS:
            try:
                bars = _load_and_enrich_math_tf(sym, tf)
            except Exception as e:
                print(f"[PhaseB][SKIP] {sym} {tf}: {e}", flush=True)
                combo_count += (len(MOMENTUM_SETUP_TYPES) + len(FADE_SETUP_TYPES)) * len(INDICATOR_SESSIONS)
                continue

            for is_fade, setups_list in [
                (False, MOMENTUM_SETUP_TYPES),
                (True, FADE_SETUP_TYPES),
            ]:
                from src.engine.run_math_momentum import detect_setups as mom_detect
                from src.engine.run_math_fade import detect_setups as fade_detect
                detect_fn = fade_detect if is_fade else mom_detect

                for setup_type in setups_list:
                    try:
                        all_setups = detect_fn(bars, setup_type)
                    except Exception as exc:
                        print(f"[PhaseB][SKIP] {sym}/{tf}/{setup_type}: {exc}", flush=True)
                        combo_count += len(INDICATOR_SESSIONS)
                        continue

                    for session in INDICATOR_SESSIONS:
                        combo_count += 1
                        ses_setups = _filter_by_session(all_setups, session)
                        if len(ses_setups) < 30:
                            backtest_count += n_grid
                            continue

                        for tp, sl in tp_sl_grid:
                            backtest_count += 1
                            if backtest_count % 1000 == 0:
                                elapsed = time.time() - t0
                                pct = 100 * backtest_count / total
                                print(f"[PhaseB] {backtest_count}/{total} ({pct:.0f}%) — {elapsed:.0f}s", flush=True)
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
                                )
                            except Exception:
                                continue
                            m_dict = compute_phase_a_metrics(trades)
                            if (m_dict["n_trades"] >= PA_MIN_TRADES
                                    and m_dict["wr"] >= PA_MIN_WR
                                    and m_dict["pf"] >= PA_MIN_PF):
                                rows.append({
                                    "symbol": sym, "tf": tf,
                                    "setup_type": setup_type, "session": session,
                                    "is_fade": is_fade,
                                    "tp_mult": tp, "sl_mult": sl,
                                    **m_dict,
                                })

    elapsed = time.time() - t0
    print(f"\n[PhaseB] Sweep complete in {elapsed:.0f}s ({elapsed/60:.1f} min)", flush=True)
    print(f"[PhaseB] {backtest_count} backtests, {len(rows)} survivors", flush=True)

    if not rows:
        df = pl.DataFrame()
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            f"# MATH Discovery Phase B — TP/SL grid\n\n"
            f"- Total backtests: {backtest_count}\n- Survivors: 0\n",
            encoding="utf-8",
        )
        return df

    df = pl.DataFrame(rows).sort("calmar", descending=True)
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# MATH Discovery Phase B — M15+H1+H4 + M1 Tracking + TP/SL Grid",
        "",
        f"- Backtests run: **{backtest_count}** ({total_combos} combos × {n_grid} grid points)",
        f"- Survivors: **{len(df)}**",
        f"- Gates: n_trades >= {PA_MIN_TRADES}, WR >= {PA_MIN_WR}, PF >= {PA_MIN_PF}",
        f"- Runtime: {elapsed:.0f}s ({elapsed/60:.1f} min)",
        "",
        "## Top 50 by Calmar",
        "",
        "| sym | tf | setup | session | kind | tp | sl | n | wr | pf | exp_R | dd_R | calmar |",
        "|-----|-----|-------|---------|------|-----|-----|---|-----|-----|-------|------|--------|",
    ]
    for r in df.head(50).iter_rows(named=True):
        kind = "FADE" if r["is_fade"] else "MOM"
        lines.append(
            f"| {r['symbol']} | {r['tf']} | {r['setup_type']} | {r['session']} | "
            f"{kind} | {r['tp_mult']:.1f} | {r['sl_mult']:.1f} | {r['n_trades']} | "
            f"{r['wr']:.3f} | {r['pf']:.3f} | {r['expectancy_r']:.3f} | "
            f"{r['max_dd_r']:.1f} | {r['calmar']:.3f} |"
        )
    lines.append("")
    lines.append("## Per-TF survivors")
    lines.append("")
    by_tf = df.group_by("tf").agg(pl.len().alias("n")).sort("n", descending=True)
    for r in by_tf.iter_rows(named=True):
        lines.append(f"- {r['tf']}: {r['n']}")
    lines.append("")
    lines.append("## Per-symbol survivors")
    lines.append("")
    by_sym = df.group_by("symbol").agg(pl.len().alias("n")).sort("n", descending=True)
    for r in by_sym.iter_rows(named=True):
        lines.append(f"- {r['symbol']}: {r['n']}")
    out_path.write_text("\n".join(lines), encoding="utf-8")

    df.write_parquet(REPORTS_DIR / "math_discovery_m1_phase_b.parquet")

    print(f"\n[PhaseB] Top 5 survivors by Calmar:", flush=True)
    for r in df.head(5).iter_rows(named=True):
        kind = "MOM" if not r["is_fade"] else "FADE"
        print(f"  {r['symbol']:10s} {r['tf']:4s} {r['setup_type']:25s} "
              f"{r['session']:10s} {kind:4s}  TP={r['tp_mult']:.1f} SL={r['sl_mult']:.1f}  "
              f"WR={r['wr']:.3f}  PF={r['pf']:.2f}  Calmar={r['calmar']:.4f}", flush=True)

    return df


def run_discovery_phase_a(
    output_path: str = "reports/external/math_discovery_m1_phase_a.md",
) -> pl.DataFrame:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    total = len(M1_AVAILABLE) * len(TFS) * (len(MOMENTUM_SETUP_TYPES) + len(FADE_SETUP_TYPES)) * len(INDICATOR_SESSIONS)
    print(f"[PhaseA] Starting sweep: {total} combos", flush=True)
    print(f"[PhaseA] {len(M1_AVAILABLE)} symbols × {len(TFS)} TFs "
          f"× {len(MOMENTUM_SETUP_TYPES) + len(FADE_SETUP_TYPES)} setups "
          f"× {len(INDICATOR_SESSIONS)} sessions", flush=True)

    rows = []
    combo_count = 0
    t0 = time.time()

    def _progress(extra: str = "") -> None:
        pct = 100 * combo_count / total if total > 0 else 0
        elapsed = time.time() - t0
        print(f"[PhaseA] {combo_count}/{total} ({pct:.0f}%) — {elapsed:.0f}s  {extra}", flush=True)

    for sym in M1_AVAILABLE:
        # Load M1 once per symbol
        m1 = load_m1(sym)
        if m1 is None:
            print(f"[PhaseA][SKIP] {sym}: no M1 data", flush=True)
            combo_count += len(TFS) * (len(MOMENTUM_SETUP_TYPES) + len(FADE_SETUP_TYPES)) * len(INDICATOR_SESSIONS)
            continue

        # Pre-convert M1 to lists ONCE per symbol — reused across all combos
        # for this symbol (huge speedup: avoids ~180 list-conversions × 3M rows).
        print(f"[PhaseA] {sym}: M1 rows={len(m1)} — converting arrays...", flush=True)
        m1_arrays = precompute_m1_arrays(m1)
        print(f"[PhaseA] {sym}: arrays ready ({len(m1_arrays['times'])} M1 bars)", flush=True)

        friction = _friction_for(sym)

        for tf in TFS:
            try:
                bars = _load_and_enrich_math_tf(sym, tf)
            except Exception as e:
                print(f"[PhaseA][SKIP] {sym} {tf}: {e}")
                combo_count += (len(MOMENTUM_SETUP_TYPES) + len(FADE_SETUP_TYPES)) * len(INDICATOR_SESSIONS)
                continue

            print(f"[PhaseA]   {sym}/{tf}: signal bars={len(bars)}")

            # -- MOMENTUM setups --
            for setup_type in MOMENTUM_SETUP_TYPES:
                try:
                    all_setups = momentum_detect_setups(bars, setup_type)
                except Exception as exc:
                    print(f"[PhaseA][SKIP] {sym}/{tf}/{setup_type}: {exc}")
                    combo_count += len(INDICATOR_SESSIONS)
                    continue

                for session in INDICATOR_SESSIONS:
                    combo_count += 1
                    if combo_count % 100 == 0:
                        _progress(f"{sym}/{tf}/{setup_type}/{session}")
                    elif combo_count in (total // 4, total // 2, 3 * total // 4):
                        _progress("MILESTONE")

                    ses_setups = _filter_by_session(all_setups, session)
                    if len(ses_setups) < 30:
                        continue

                    try:
                        trades = run_setup_backtest_m1(
                            setups=ses_setups,
                            bars_signal_tf=bars,
                            m1_df=None,
                            setup_type=setup_type,
                            is_fade=False,
                            tp_atr_mult=MOMENTUM_TP,
                            sl_atr_mult=MOMENTUM_SL,
                            session_end_hour_utc=_session_end_hour(session),
                            friction_r=friction,
                            symbol=sym,
                            signal_tf=tf,
                            m1_arrays=m1_arrays,
                        )
                    except Exception as exc:
                        print(f"[PhaseA][ERR] {sym}/{tf}/{setup_type}/{session}: {exc}", flush=True)
                        continue

                    m_dict = compute_phase_a_metrics(trades)
                    if (m_dict["n_trades"] >= PA_MIN_TRADES
                            and m_dict["wr"] >= PA_MIN_WR
                            and m_dict["pf"] >= PA_MIN_PF):
                        rows.append({
                            "symbol": sym, "tf": tf,
                            "setup_type": setup_type, "session": session,
                            "is_fade": False, **m_dict,
                        })

            # -- FADE setups --
            for setup_type in FADE_SETUP_TYPES:
                try:
                    all_setups = fade_detect_setups(bars, setup_type)
                except Exception as exc:
                    print(f"[PhaseA][SKIP] {sym}/{tf}/{setup_type}: {exc}")
                    combo_count += len(INDICATOR_SESSIONS)
                    continue

                for session in INDICATOR_SESSIONS:
                    combo_count += 1
                    if combo_count % 100 == 0:
                        _progress(f"{sym}/{tf}/{setup_type}/{session}")
                    elif combo_count in (total // 4, total // 2, 3 * total // 4):
                        _progress("MILESTONE")

                    ses_setups = _filter_by_session(all_setups, session)
                    if len(ses_setups) < 30:
                        continue

                    try:
                        trades = run_setup_backtest_m1(
                            setups=ses_setups,
                            bars_signal_tf=bars,
                            m1_df=None,
                            setup_type=setup_type,
                            is_fade=True,
                            tp_atr_mult=FADE_TP,
                            sl_atr_mult=FADE_SL,
                            session_end_hour_utc=_session_end_hour(session),
                            friction_r=friction,
                            symbol=sym,
                            signal_tf=tf,
                            m1_arrays=m1_arrays,
                        )
                    except Exception as exc:
                        print(f"[PhaseA][ERR] {sym}/{tf}/{setup_type}/{session}: {exc}", flush=True)
                        continue

                    m_dict = compute_phase_a_metrics(trades)
                    if (m_dict["n_trades"] >= PA_MIN_TRADES
                            and m_dict["wr"] >= PA_MIN_WR
                            and m_dict["pf"] >= PA_MIN_PF):
                        rows.append({
                            "symbol": sym, "tf": tf,
                            "setup_type": setup_type, "session": session,
                            "is_fade": True, **m_dict,
                        })

    elapsed = time.time() - t0
    print(f"\n[PhaseA] Sweep complete in {elapsed:.0f}s ({elapsed/60:.1f} min)")
    print(f"[PhaseA] {combo_count} combos evaluated, {len(rows)} survivors")

    if not rows:
        df = pl.DataFrame()
        out_path = Path(output_path)
        _write_phase_a_report(out_path, df, total_combos=combo_count)
        df.write_parquet(REPORTS_DIR / "math_discovery_m1_phase_a.parquet")
        return df

    df = pl.DataFrame(rows).sort("calmar", descending=True)
    out_path = Path(output_path)
    _write_phase_a_report(out_path, df, total_combos=combo_count)
    df.write_parquet(REPORTS_DIR / "math_discovery_m1_phase_a.parquet")

    print(f"\n[PhaseA] Top 5 survivors by Calmar:")
    for r in df.head(5).iter_rows(named=True):
        kind = "MOM" if not r["is_fade"] else "FADE"
        print(f"  {r['symbol']:10s} {r['tf']:4s} {r['setup_type']:25s} "
              f"{r['session']:10s} {kind:4s}  "
              f"WR={r['wr']:.3f}  PF={r['pf']:.2f}  "
              f"Exp={r['expectancy_r']:.3f}R  Calmar={r['calmar']:.4f}")

    return df


if __name__ == "__main__":
    import sys
    phase = sys.argv[1] if len(sys.argv) > 1 else "b"
    if phase.lower() == "a":
        df = run_discovery_phase_a()
    else:
        df = run_discovery_phase_b()
    print(f"\n{len(df)} survivors")
    if not df.is_empty():
        print(df.head(20))
