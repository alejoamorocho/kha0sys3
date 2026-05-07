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
    # 2 invert modes × n_grid per combo
    total = total_combos * n_grid * 2
    print(f"[PhaseB] Starting grid sweep: {total_combos} combos × {n_grid} (TP,SL) × 2 invert = {total} backtests", flush=True)

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
                            # 2 invert modes inside the inner loop -> count both
                            backtest_count += 2
                            if backtest_count % 2000 == 0:
                                elapsed = time.time() - t0
                                pct = 100 * backtest_count / total
                                print(f"[PhaseB] {backtest_count}/{total} ({pct:.0f}%) — {elapsed:.0f}s", flush=True)
                            # Plan 4: probar tanto NORMAL como INVERT (bot live MATH usa INVERT).
                            for invert in (False, True):
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
                                if (m_dict["n_trades"] >= PA_MIN_TRADES
                                        and m_dict["wr"] >= PA_MIN_WR
                                        and m_dict["pf"] >= PA_MIN_PF):
                                    rows.append({
                                        "symbol": sym, "tf": tf,
                                        "setup_type": setup_type, "session": session,
                                        "is_fade": is_fade,
                                        "invert": invert,
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


def _load_phase_b_survivors() -> pl.DataFrame:
    path = REPORTS_DIR / "math_discovery_m1_phase_b.parquet"
    if not path.exists():
        raise FileNotFoundError(f"Phase B parquet not found: {path}")
    return pl.read_parquet(path)


def run_discovery_phase_c(
    output_path: str = "reports/external/math_discovery_m1_phase_c.md",
) -> pl.DataFrame:
    """Phase C: grid fino TP/SL sobre los supervivientes de Phase B.

    Para cada superviviente: grid 12x12 = 144 combos (TP, SL) en step 0.25.
    Reporta el mejor (tp, sl) por estrategia y todas las combinaciones que
    siguen pasando los gates.
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    survivors = _load_phase_b_survivors()
    if survivors.is_empty():
        print("[PhaseC] No Phase B survivors to refine.", flush=True)
        return pl.DataFrame()

    # Grid finer than Phase B
    tp_values = [round(0.5 + i * 0.25, 2) for i in range(11)]   # 0.5..3.0
    sl_values = [round(0.3 + i * 0.25, 2) for i in range(11)]   # 0.3..2.8
    n_grid = sum(1 for tp in tp_values for sl in sl_values)
    total = len(survivors) * n_grid
    print(f"[PhaseC] Refining {len(survivors)} survivors × {n_grid} grid = {total} backtests", flush=True)

    from src.engine.run_math_momentum import detect_setups as mom_detect
    from src.engine.run_math_fade import detect_setups as fade_detect

    rows = []
    backtest_count = 0
    t0 = time.time()

    # Cache per (sym, tf): bars + m1_arrays + setups
    bars_cache: dict[tuple[str, str], pl.DataFrame] = {}
    m1_cache: dict[str, dict] = {}
    setups_cache: dict[tuple[str, str, str, bool], pl.DataFrame] = {}

    for surv in survivors.iter_rows(named=True):
        sym = surv["symbol"]
        tf = surv["tf"]
        setup_type = surv["setup_type"]
        session = surv["session"]
        is_fade = surv["is_fade"]
        invert = bool(surv.get("invert", False))

        # Cache m1 per symbol
        if sym not in m1_cache:
            m1 = load_m1(sym)
            if m1 is None:
                continue
            m1_cache[sym] = precompute_m1_arrays(m1)
        m1_arrays = m1_cache[sym]

        # Cache bars per (sym, tf)
        bk = (sym, tf)
        if bk not in bars_cache:
            bars_cache[bk] = _load_and_enrich_math_tf(sym, tf)
        bars = bars_cache[bk]

        # Cache setups per (sym, tf, setup_type, is_fade)
        sk = (sym, tf, setup_type, is_fade)
        if sk not in setups_cache:
            detect_fn = fade_detect if is_fade else mom_detect
            try:
                setups_cache[sk] = detect_fn(bars, setup_type)
            except Exception as e:
                print(f"[PhaseC][SKIP] {sym}/{tf}/{setup_type}: {e}", flush=True)
                setups_cache[sk] = pl.DataFrame()
        all_setups = setups_cache[sk]
        if all_setups.is_empty():
            continue
        ses_setups = _filter_by_session(all_setups, session)
        if len(ses_setups) < 30:
            continue

        friction = _friction_for(sym)
        for tp in tp_values:
            for sl in sl_values:
                if tp <= 0 or sl <= 0:
                    continue
                backtest_count += 1
                if backtest_count % 200 == 0:
                    elapsed = time.time() - t0
                    pct = 100 * backtest_count / total
                    print(f"[PhaseC] {backtest_count}/{total} ({pct:.0f}%) — {elapsed:.0f}s", flush=True)
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
                if (m_dict["n_trades"] >= PA_MIN_TRADES
                        and m_dict["wr"] >= PA_MIN_WR
                        and m_dict["pf"] >= PA_MIN_PF):
                    rows.append({
                        "symbol": sym, "tf": tf,
                        "setup_type": setup_type, "session": session,
                        "is_fade": is_fade, "invert": invert,
                        "tp_mult": tp, "sl_mult": sl,
                        **m_dict,
                    })

    elapsed = time.time() - t0
    print(f"\n[PhaseC] Sweep complete in {elapsed:.0f}s", flush=True)
    print(f"[PhaseC] {backtest_count} backtests, {len(rows)} survivors", flush=True)

    if not rows:
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text("# Phase C\n- Survivors: 0\n", encoding="utf-8")
        return pl.DataFrame()

    df = pl.DataFrame(rows).sort("calmar", descending=True)
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Best (tp, sl) per (sym, tf, setup_type, session, invert)
    best_per_strat = (
        df.sort("calmar", descending=True)
        .group_by(["symbol", "tf", "setup_type", "session", "invert"])
        .agg([
            pl.col("tp_mult").first().alias("tp_mult"),
            pl.col("sl_mult").first().alias("sl_mult"),
            pl.col("n_trades").first().alias("n_trades"),
            pl.col("wr").first().alias("wr"),
            pl.col("pf").first().alias("pf"),
            pl.col("expectancy_r").first().alias("expectancy_r"),
            pl.col("max_dd_r").first().alias("max_dd_r"),
            pl.col("calmar").first().alias("calmar"),
        ])
        .sort("calmar", descending=True)
    )

    lines = [
        "# MATH Discovery Phase C — fine TP/SL grid on Phase B survivors",
        "",
        f"- Phase B survivors refined: **{len(survivors)}**",
        f"- Backtests run: **{backtest_count}**",
        f"- Phase-C survivors (gates: n>=30 wr>=0.5 pf>=1): **{len(df)}**",
        f"- Best (tp, sl) per strategy: **{len(best_per_strat)}**",
        f"- Runtime: {elapsed:.0f}s",
        "",
        "## Best (tp, sl) per strategy",
        "",
        "| sym | tf | setup | session | invert | tp | sl | n | wr | pf | exp_R | dd_R | calmar |",
        "|-----|-----|-------|---------|--------|-----|-----|---|-----|-----|-------|------|--------|",
    ]
    for r in best_per_strat.iter_rows(named=True):
        lines.append(
            f"| {r['symbol']} | {r['tf']} | {r['setup_type']} | {r['session']} | "
            f"{r['invert']} | {r['tp_mult']:.2f} | {r['sl_mult']:.2f} | {r['n_trades']} | "
            f"{r['wr']:.3f} | {r['pf']:.3f} | {r['expectancy_r']:.3f} | "
            f"{r['max_dd_r']:.1f} | {r['calmar']:.3f} |"
        )
    out_path.write_text("\n".join(lines), encoding="utf-8")
    df.write_parquet(REPORTS_DIR / "math_discovery_m1_phase_c.parquet")
    best_per_strat.write_parquet(REPORTS_DIR / "math_discovery_m1_phase_c_best.parquet")

    print(f"\n[PhaseC] Top 5 by Calmar (best per strategy):", flush=True)
    for r in best_per_strat.head(5).iter_rows(named=True):
        print(f"  {r['symbol']:10s} {r['tf']:4s} {r['setup_type']:25s} "
              f"{r['session']:10s} INV={r['invert']}  "
              f"TP={r['tp_mult']:.2f} SL={r['sl_mult']:.2f}  "
              f"n={r['n_trades']:4d} WR={r['wr']:.3f} PF={r['pf']:.2f} "
              f"Calmar={r['calmar']:.4f}", flush=True)

    return df


def run_discovery_phase_d(
    output_path: str = "reports/external/math_discovery_m1_phase_d.md",
) -> pl.DataFrame:
    """Phase D: salidas alternativas — exit en señal opuesta.

    Para cada estrategia con su mejor (tp, sl) de Phase C, probar:
      V1 (baseline): TP/SL fijos
      V2: exit cuando aparece próxima señal opuesta (mismo setup, dir invertida)
      V3: exit en señal opuesta + TP/SL como cap de protección
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    best_path = REPORTS_DIR / "math_discovery_m1_phase_c_best.parquet"
    if not best_path.exists():
        print("[PhaseD] Phase C best not found; run Phase C first.", flush=True)
        return pl.DataFrame()
    best = pl.read_parquet(best_path)
    if best.is_empty():
        print("[PhaseD] No Phase C survivors.", flush=True)
        return pl.DataFrame()
    print(f"[PhaseD] {len(best)} strategies × 3 variants = {len(best)*3} backtests", flush=True)

    from src.engine.run_math_momentum import detect_setups as mom_detect
    from src.engine.run_math_fade import detect_setups as fade_detect

    rows = []
    t0 = time.time()
    m1_cache: dict[str, dict] = {}
    bars_cache: dict[tuple[str, str], pl.DataFrame] = {}
    setups_cache: dict[tuple[str, str, str, bool], pl.DataFrame] = {}

    for s in best.iter_rows(named=True):
        sym, tf, setup, ses = s["symbol"], s["tf"], s["setup_type"], s["session"]
        is_fade = s.get("is_fade", False)
        invert = bool(s["invert"])
        tp, sl = s["tp_mult"], s["sl_mult"]

        if sym not in m1_cache:
            m1 = load_m1(sym)
            if m1 is None:
                continue
            m1_cache[sym] = precompute_m1_arrays(m1)
        m1_arrays = m1_cache[sym]
        bk = (sym, tf)
        if bk not in bars_cache:
            bars_cache[bk] = _load_and_enrich_math_tf(sym, tf)
        bars = bars_cache[bk]
        sk = (sym, tf, setup, is_fade)
        if sk not in setups_cache:
            detect_fn = fade_detect if is_fade else mom_detect
            setups_cache[sk] = detect_fn(bars, setup)
        all_setups = setups_cache[sk]
        ses_setups = _filter_by_session(all_setups, ses)
        if len(ses_setups) < 30:
            continue
        friction = _friction_for(sym)
        end_h = _session_end_hour(ses)

        # V1 baseline
        try:
            t_v1 = run_setup_backtest_m1(
                setups=ses_setups, bars_signal_tf=bars, m1_df=None,
                setup_type=setup, is_fade=is_fade,
                tp_atr_mult=tp, sl_atr_mult=sl,
                session_end_hour_utc=end_h, friction_r=friction,
                symbol=sym, signal_tf=tf, m1_arrays=m1_arrays,
                invert_direction=invert,
            )
            m1_metrics = compute_phase_a_metrics(t_v1)
            rows.append({"variant": "V1_baseline", "symbol": sym, "tf": tf,
                         "setup_type": setup, "session": ses, "invert": invert,
                         "tp_mult": tp, "sl_mult": sl, **m1_metrics})
        except Exception as e:
            print(f"[PhaseD][V1 ERR] {sym}/{tf}/{setup}: {e}", flush=True)

        # V2 + V3 require exit on opposite signal: pre-compute opposite signal times.
        # Opposite signals = the same setup with direction OPPOSITE to what we trade.
        # Recall: invert=True means our trade direction is OPPOSITE of detector's direction.
        # So our LONG = detector SHORT; our SHORT = detector LONG. Opposite-of-our-trade
        # signals are detector signals matching our same trade direction (since they
        # would invert again to the OPPOSITE). i.e. detector's same-direction signals.
        # Complicated. Implement plainly:
        # opposite_for_long_trade = detector signals that lead to short trades
        # opposite_for_short_trade = detector signals that lead to long trades
        # Under invert: detector LONG → our SHORT; detector SHORT → our LONG.
        #   so for our LONG trade (open from detector SHORT), opposite signal arrives
        #   as the next detector LONG (our next SHORT trade).
        # Without invert: detector LONG → our LONG; opposite = next detector SHORT.

        # Build opposite_ts_long / opposite_ts_short sorted lists of timestamps.
        det_dir_col = ses_setups["direction"].to_list()
        det_time_col = ses_setups["time"].to_list()
        if invert:
            # our_trade_direction = INVERT(det_dir)
            our_dirs = ["SHORT" if d == "LONG" else "LONG" for d in det_dir_col]
        else:
            our_dirs = list(det_dir_col)
        # opposite_for_long_trade = times of "SHORT" our_trades
        opp_for_long = [det_time_col[i] for i, d in enumerate(our_dirs) if d == "SHORT"]
        opp_for_short = [det_time_col[i] for i, d in enumerate(our_dirs) if d == "LONG"]

        # V2 / V3: re-implement a lighter loop here that uses our_dirs as both entries
        # and exits on opposite. To keep this manageable, we delegate to a helper.
        # For now, run V1-like trades but cap exit when next opposite-our signal arrives.
        try:
            t_v2 = _run_with_opposite_exit(
                setups=ses_setups, m1_arrays=m1_arrays,
                setup_type=setup, is_fade=is_fade,
                tp_atr_mult=tp, sl_atr_mult=sl,
                session_end_hour_utc=end_h, friction_r=friction,
                symbol=sym, signal_tf=tf, invert=invert,
                opp_long_ts=sorted(opp_for_long),
                opp_short_ts=sorted(opp_for_short),
                use_tp_sl_protection=False,
            )
            mm = compute_phase_a_metrics(t_v2)
            rows.append({"variant": "V2_opposite_only", "symbol": sym, "tf": tf,
                         "setup_type": setup, "session": ses, "invert": invert,
                         "tp_mult": tp, "sl_mult": sl, **mm})
        except Exception as e:
            print(f"[PhaseD][V2 ERR] {sym}/{tf}/{setup}: {e}", flush=True)

        try:
            t_v3 = _run_with_opposite_exit(
                setups=ses_setups, m1_arrays=m1_arrays,
                setup_type=setup, is_fade=is_fade,
                tp_atr_mult=tp, sl_atr_mult=sl,
                session_end_hour_utc=end_h, friction_r=friction,
                symbol=sym, signal_tf=tf, invert=invert,
                opp_long_ts=sorted(opp_for_long),
                opp_short_ts=sorted(opp_for_short),
                use_tp_sl_protection=True,
            )
            mm = compute_phase_a_metrics(t_v3)
            rows.append({"variant": "V3_opposite_with_tpsl", "symbol": sym, "tf": tf,
                         "setup_type": setup, "session": ses, "invert": invert,
                         "tp_mult": tp, "sl_mult": sl, **mm})
        except Exception as e:
            print(f"[PhaseD][V3 ERR] {sym}/{tf}/{setup}: {e}", flush=True)

    elapsed = time.time() - t0
    print(f"\n[PhaseD] complete in {elapsed:.0f}s — {len(rows)} variant runs", flush=True)

    df = pl.DataFrame(rows)
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if df.is_empty():
        out_path.write_text("# Phase D\n- No runs.\n", encoding="utf-8")
        return df

    # Per strategy: pick best variant by calmar
    best_variant = (
        df.sort("calmar", descending=True)
        .group_by(["symbol", "tf", "setup_type", "session", "invert"])
        .agg([
            pl.col("variant").first().alias("best_variant"),
            pl.col("tp_mult").first().alias("tp_mult"),
            pl.col("sl_mult").first().alias("sl_mult"),
            pl.col("n_trades").first().alias("n_trades"),
            pl.col("wr").first().alias("wr"),
            pl.col("pf").first().alias("pf"),
            pl.col("expectancy_r").first().alias("expectancy_r"),
            pl.col("max_dd_r").first().alias("max_dd_r"),
            pl.col("calmar").first().alias("calmar"),
        ])
        .sort("calmar", descending=True)
    )

    lines = [
        "# MATH Discovery Phase D — Salidas alternativas",
        "",
        f"- Strategies tested: {len(best)}",
        f"- Variants per strategy: 3 (V1 baseline, V2 opposite_only, V3 opposite+tpsl)",
        f"- Total runs: {len(df)}",
        "",
        "## Best variant per strategy",
        "",
        "| sym | tf | setup | session | invert | best | tp | sl | n | wr | pf | exp_R | dd_R | calmar |",
        "|-----|-----|-------|---------|--------|------|-----|-----|---|-----|-----|-------|------|--------|",
    ]
    for r in best_variant.iter_rows(named=True):
        lines.append(
            f"| {r['symbol']} | {r['tf']} | {r['setup_type']} | {r['session']} | "
            f"{r['invert']} | {r['best_variant']} | "
            f"{r['tp_mult']:.2f} | {r['sl_mult']:.2f} | {r['n_trades']} | "
            f"{r['wr']:.3f} | {r['pf']:.3f} | {r['expectancy_r']:.3f} | "
            f"{r['max_dd_r']:.1f} | {r['calmar']:.3f} |"
        )
    lines.append("")
    lines.append("## All runs (all 3 variants per strategy)")
    lines.append("")
    lines.append("| variant | sym | tf | setup | session | n | wr | pf | exp_R | calmar |")
    lines.append("|---------|-----|-----|-------|---------|---|-----|-----|-------|--------|")
    df_sorted = df.sort(["symbol", "tf", "setup_type", "session", "variant"])
    for r in df_sorted.iter_rows(named=True):
        lines.append(
            f"| {r['variant']} | {r['symbol']} | {r['tf']} | {r['setup_type']} | "
            f"{r['session']} | {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.3f} | "
            f"{r['expectancy_r']:.3f} | {r['calmar']:.3f} |"
        )
    out_path.write_text("\n".join(lines), encoding="utf-8")
    df.write_parquet(REPORTS_DIR / "math_discovery_m1_phase_d.parquet")
    best_variant.write_parquet(REPORTS_DIR / "math_discovery_m1_phase_d_best.parquet")

    return df


def _run_with_opposite_exit(
    setups, m1_arrays, setup_type, is_fade, tp_atr_mult, sl_atr_mult,
    session_end_hour_utc, friction_r, symbol, signal_tf, invert,
    opp_long_ts, opp_short_ts, use_tp_sl_protection,
):
    """Like run_setup_backtest_m1 but adds exit on next opposite-direction signal.

    If use_tp_sl_protection=False, ONLY exit reasons are: SIGNAL_OPP, TIME_STOP, end-of-data.
    If True: also TP/SL hits before SIGNAL_OPP.
    """
    import bisect
    from datetime import timedelta
    if len(setups) == 0:
        return _empty_trades()

    tf_minutes = _TF_MINUTES.get(signal_tf, 15)
    wait_m1_bars = WAIT_BARS * tf_minutes

    # Apply invert + dedup like base function
    if invert:
        setups = setups.with_columns(
            pl.when(pl.col("direction") == "LONG").then(pl.lit("SHORT"))
              .otherwise(pl.lit("LONG")).alias("direction")
        )
        if "stop_price" in setups.columns and "atr_14" in setups.columns and "close" in setups.columns:
            setups = setups.with_columns(
                pl.when(pl.col("direction") == "LONG")
                  .then(pl.col("close") + 0.5 * pl.col("atr_14"))
                  .otherwise(pl.col("close") - 0.5 * pl.col("atr_14"))
                  .alias("stop_price")
            )

    setups = (
        setups.with_columns(pl.col("time").dt.date().alias("_date"))
        .sort("time")
        .unique(subset=["_date"], keep="first")
        .drop("_date")
    )

    m1_times = m1_arrays["times"]
    m1_highs = m1_arrays["highs"]
    m1_lows = m1_arrays["lows"]
    m1_closes = m1_arrays["closes"]

    results = []
    for s in setups.iter_rows(named=True):
        atr = s.get("atr_14")
        if atr is None or atr <= 0:
            continue
        direction = s.get("direction")
        if direction is None:
            continue
        if is_fade:
            order_price = s.get("close")
        else:
            order_price = s.get("stop_price") if "stop_price" in setups.columns else s.get("close")
        if order_price is None:
            continue

        setup_time = s["time"]
        bar_close_time = setup_time + timedelta(minutes=tf_minutes)
        start_idx = bisect.bisect_right(m1_times, bar_close_time)
        if start_idx >= len(m1_times):
            continue
        end_wait = min(start_idx + wait_m1_bars, len(m1_times))

        # find fill
        fill_idx = None
        for i in range(start_idx, end_wait):
            hi, lo = m1_highs[i], m1_lows[i]
            if hi is None or lo is None:
                continue
            if is_fade:
                if direction == "LONG" and lo <= order_price:
                    fill_idx = i; break
                if direction == "SHORT" and hi >= order_price:
                    fill_idx = i; break
            else:
                if direction == "LONG" and hi >= order_price:
                    fill_idx = i; break
                if direction == "SHORT" and lo <= order_price:
                    fill_idx = i; break
        if fill_idx is None:
            continue

        entry = order_price
        if direction == "LONG":
            tp = entry + tp_atr_mult * atr
            sl = entry - sl_atr_mult * atr
        else:
            tp = entry - tp_atr_mult * atr
            sl = entry + sl_atr_mult * atr

        # Find opposite-direction signal time AFTER fill_time
        fill_time = m1_times[fill_idx]
        opp_list = opp_short_ts if direction == "LONG" else opp_long_ts
        idx_opp = bisect.bisect_right(opp_list, fill_time)
        opp_signal_ts = opp_list[idx_opp] if idx_opp < len(opp_list) else None

        exit_reason = None; exit_price = None; exit_time = None
        signal_date = setup_time.date()

        for j in range(fill_idx + 1, len(m1_times)):
            bt = m1_times[j]
            if bt.date() > signal_date or bt.hour >= session_end_hour_utc:
                exit_reason = "TIME_STOP"; prev = j - 1
                exit_price = m1_closes[prev] if prev >= 0 else entry
                exit_time = m1_times[prev] if prev >= 0 else bt; break
            if opp_signal_ts is not None and bt >= opp_signal_ts:
                exit_reason = "SIGNAL_OPP"; exit_price = m1_closes[j]; exit_time = bt; break
            if use_tp_sl_protection:
                hi, lo = m1_highs[j], m1_lows[j]
                if hi is None or lo is None:
                    continue
                if direction == "LONG":
                    if hi >= tp: exit_reason="TP"; exit_price=tp; exit_time=bt; break
                    if lo <= sl: exit_reason="SL"; exit_price=sl; exit_time=bt; break
                else:
                    if lo <= tp: exit_reason="TP"; exit_price=tp; exit_time=bt; break
                    if hi >= sl: exit_reason="SL"; exit_price=sl; exit_time=bt; break
        else:
            exit_reason = "TIME_STOP"
            exit_price = m1_closes[-1]; exit_time = m1_times[-1]

        if exit_price is None:
            continue
        risk_per_unit = sl_atr_mult * atr
        pnl = (exit_price - entry) if direction == "LONG" else (entry - exit_price)
        r_gross = pnl / risk_per_unit if risk_per_unit > 0 else 0.0
        r_net = r_gross - friction_r
        results.append({
            "time": setup_time, "symbol": symbol, "setup_type": setup_type,
            "direction": direction, "entry_price": entry, "tp_price": tp, "sl_price": sl,
            "exit_time": exit_time, "exit_price": exit_price, "exit_reason": exit_reason,
            "r_multiple": r_net,
        })

    if not results:
        return _empty_trades()
    return pl.DataFrame(results)


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
    p = phase.lower()
    if p == "a":
        df = run_discovery_phase_a()
    elif p == "b":
        df = run_discovery_phase_b()
    elif p == "c":
        df = run_discovery_phase_c()
    elif p == "d":
        df = run_discovery_phase_d()
    else:
        raise SystemExit(f"unknown phase: {phase}")
    # Avoid polars table unicode chars failing on Windows cp1252.
    print(f"\nTotal rows: {len(df)}", flush=True)
    print(f"\n{len(df)} survivors")
    if not df.is_empty():
        print(df.head(20))
