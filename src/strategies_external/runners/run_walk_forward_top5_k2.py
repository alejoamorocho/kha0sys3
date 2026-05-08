"""Walk-Forward IS/OOS Validation — Top 5 Phase K2 Candidates.

For each candidate, generates ALL trades over the full 8.33-year period
(2018-01 to 2026-05), then applies walk_forward_split (5 windows, 70/30)
to measure IS vs OOS stability WITHOUT re-optimization.

Usage:
    python -u -m src.strategies_external.runners.run_walk_forward_top5_k2
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
from src.engine.indicator_validation import compute_metrics

# ── Config ─────────────────────────────────────────────────────────────────────

REPORTS_DIR = Path("reports/external")
OUTPUT_MD = REPORTS_DIR / "math_discovery_m1_phase_k2_walkforward.md"

N_WINDOWS = 5
IS_PCT = 0.7

# Robustness gate thresholds
ROBUST_WR_DROP_MAX = 0.05   # 5pp
ROBUST_PF_DROP_MAX = 0.20   # 0.20 absolute

_FX_SET = {"EURUSD", "USDJPY", "GBPAUD"}

CANDIDATES: list[dict] = [
    {
        "label": "NASDAQ100 M15 KAMA_CROSS_MOM ASIA TP=0.70 SL=1.00",
        "sym": "NASDAQ100", "tf": "M15", "setup": "KAMA_CROSS_MOM",
        "ses": "ASIA", "inv": False, "is_fade": False,
        "tp": 0.70, "sl": 1.00,
    },
    {
        "label": "GBPAUD H1 KAMA_CROSS_MOM ASIA TP=0.70 SL=1.00",
        "sym": "GBPAUD", "tf": "H1", "setup": "KAMA_CROSS_MOM",
        "ses": "ASIA", "inv": False, "is_fade": False,
        "tp": 0.70, "sl": 1.00,
    },
    {
        "label": "WTI M15 SPECTRAL_TREND_MOM ASIA TP=0.50 SL=1.50",
        "sym": "WTI", "tf": "M15", "setup": "SPECTRAL_TREND_MOM",
        "ses": "ASIA", "inv": False, "is_fade": False,
        "tp": 0.50, "sl": 1.50,
    },
    {
        "label": "EURUSD H1 KAMA_CROSS_MOM NY INV=True TP=1.50 SL=2.00",
        "sym": "EURUSD", "tf": "H1", "setup": "KAMA_CROSS_MOM",
        "ses": "NY", "inv": True, "is_fade": False,
        "tp": 1.50, "sl": 2.00,
    },
    {
        "label": "USDJPY M15 SPECTRAL_TREND_MOM LONDON TP=0.70 SL=1.00",
        "sym": "USDJPY", "tf": "M15", "setup": "SPECTRAL_TREND_MOM",
        "ses": "LONDON", "inv": False, "is_fade": False,
        "tp": 0.70, "sl": 1.00,
    },
]


def _friction_for(sym: str) -> float:
    return 0.05 if sym in _FX_SET else 0.10


def _session_end_hour(session: str) -> int:
    return INDICATOR_SESSIONS[session][1]


# ── Metrics from Polars trades DataFrame ───────────────────────────────────────

# Cap used for averaging PF when inf (all-win windows) to avoid nan in drift
_INF_PF_CAP = 99.0


def _metrics_from_df(trades_df: pl.DataFrame) -> dict:
    """Compute WR, PF, expectancy from a Polars trades DataFrame.

    PF is capped at _INF_PF_CAP to avoid inf/nan in drift calculations
    while preserving that an all-win window is excellent (pf_raw=inf).
    """
    if trades_df is None or len(trades_df) == 0:
        return {"n": 0, "wr": 0.0, "pf": 0.0, "pf_raw": 0.0, "exp_r": 0.0}
    m = compute_metrics(trades_df)
    pf_raw = m.profit_factor
    pf_capped = min(pf_raw, _INF_PF_CAP) if pf_raw != float("inf") else _INF_PF_CAP
    return {
        "n": m.n_trades,
        "wr": m.wr,
        "pf": pf_capped,
        "pf_raw": pf_raw,
        "exp_r": m.expectancy_r,
    }


# ── Walk-forward split on Polars DataFrame ─────────────────────────────────────

def walk_forward_split_df(
    trades_df: pl.DataFrame,
    n_windows: int = 5,
    is_pct: float = 0.7,
) -> list[tuple[pl.DataFrame, pl.DataFrame]]:
    """Chronological walk-forward split directly on a Polars DataFrame.

    Each window is a consecutive slice of rows (sorted by time).
    Returns list of (is_df, oos_df) tuples.
    """
    if len(trades_df) < n_windows * 2:
        raise ValueError(
            f"Too few trades ({len(trades_df)}) for {n_windows} windows"
        )
    sorted_df = trades_df.sort("time")
    n = len(sorted_df)
    window_size = n // n_windows
    is_size = int(window_size * is_pct)
    oos_size = window_size - is_size

    windows = []
    for w in range(n_windows):
        start = w * window_size
        end = start + window_size if w < n_windows - 1 else n
        chunk = sorted_df.slice(start, end - start)
        is_chunk = chunk.slice(0, is_size)
        oos_chunk = chunk.slice(is_size, oos_size)
        windows.append((is_chunk, oos_chunk))
    return windows


# ── Per-candidate runner ───────────────────────────────────────────────────────

def run_candidate(cand: dict) -> dict:
    """Run full WF analysis for one candidate. Returns result dict."""
    sym = cand["sym"]
    tf = cand["tf"]
    setup = cand["setup"]
    ses = cand["ses"]
    inv = cand["inv"]
    is_fade = cand["is_fade"]
    tp = cand["tp"]
    sl = cand["sl"]
    label = cand["label"]

    print(f"\n[WF] Candidate: {label}", flush=True)
    t0 = time.time()

    # Load M1
    m1_df = load_m1(sym)
    if m1_df is None:
        print(f"[WF] ERROR: No M1 data for {sym}", flush=True)
        return {"label": label, "error": f"No M1 data for {sym}"}
    m1_arr = precompute_m1_arrays(m1_df)

    # Load enriched bars
    bars = _load_and_enrich_math_tf(sym, tf)
    print(f"[WF]   Bars loaded: {len(bars)} {tf} rows", flush=True)

    # Detect setups
    detect_fn = fade_detect if is_fade else mom_detect
    all_setups = detect_fn(bars, setup)
    ses_setups = _filter_by_session(all_setups, ses)
    print(f"[WF]   Session setups: {len(ses_setups)}", flush=True)

    if len(ses_setups) < N_WINDOWS * 2:
        msg = f"Too few setups ({len(ses_setups)}) for {N_WINDOWS} WF windows"
        print(f"[WF] SKIP: {msg}", flush=True)
        return {"label": label, "error": msg}

    friction = _friction_for(sym)
    end_h = _session_end_hour(ses)

    # Generate ALL trades over full period
    trades_df = run_setup_backtest_m1(
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
        invert_direction=inv,
    )
    print(f"[WF]   Total trades: {len(trades_df)} in {time.time()-t0:.1f}s", flush=True)

    if len(trades_df) < N_WINDOWS * 4:
        msg = f"Too few trades ({len(trades_df)}) for {N_WINDOWS} WF windows"
        print(f"[WF] SKIP: {msg}", flush=True)
        return {"label": label, "error": msg}

    # Full-period metrics
    full_metrics = _metrics_from_df(trades_df)

    # Split into 5 windows
    windows = walk_forward_split_df(trades_df, n_windows=N_WINDOWS, is_pct=IS_PCT)

    window_results = []
    for w_idx, (is_df, oos_df) in enumerate(windows, 1):
        is_m = _metrics_from_df(is_df)
        oos_m = _metrics_from_df(oos_df)
        drift_wr = oos_m["wr"] - is_m["wr"]
        # Use capped PF for drift to avoid inf - inf = nan
        drift_pf = oos_m["pf"] - is_m["pf"]
        window_results.append({
            "window": w_idx,
            "is_n": is_m["n"],
            "is_wr": is_m["wr"],
            "is_pf": is_m["pf"],
            "is_pf_raw": is_m["pf_raw"],
            "is_exp_r": is_m["exp_r"],
            "oos_n": oos_m["n"],
            "oos_wr": oos_m["wr"],
            "oos_pf": oos_m["pf"],
            "oos_pf_raw": oos_m["pf_raw"],
            "oos_exp_r": oos_m["exp_r"],
            "drift_wr": drift_wr,
            "drift_pf": drift_pf,
        })
        print(
            f"[WF]   W{w_idx}: IS n={is_m['n']} WR={is_m['wr']:.3f} PF={is_m['pf']:.2f} | "
            f"OOS n={oos_m['n']} WR={oos_m['wr']:.3f} PF={oos_m['pf']:.2f} | "
            f"dWR={drift_wr:+.3f} dPF={drift_pf:+.2f}",
            flush=True,
        )

    # Average across windows
    def _avg(key: str) -> float:
        vals = [r[key] for r in window_results]
        return sum(vals) / len(vals) if vals else 0.0

    avg_is_wr = _avg("is_wr")
    avg_oos_wr = _avg("oos_wr")
    avg_is_pf = _avg("is_pf")
    avg_oos_pf = _avg("oos_pf")
    avg_is_exp = _avg("is_exp_r")
    avg_oos_exp = _avg("oos_exp_r")
    avg_drift_wr = avg_oos_wr - avg_is_wr
    avg_drift_pf = avg_oos_pf - avg_is_pf

    is_robust = (
        abs(avg_drift_wr) <= ROBUST_WR_DROP_MAX
        and avg_drift_pf >= -ROBUST_PF_DROP_MAX
    )

    print(
        f"[WF]   AVG: IS WR={avg_is_wr:.3f} OOS WR={avg_oos_wr:.3f} dWR={avg_drift_wr:+.3f} | "
        f"IS PF={avg_is_pf:.2f} OOS PF={avg_oos_pf:.2f} dPF={avg_drift_pf:+.2f} | "
        f"Robust: {'YES' if is_robust else 'NO'}",
        flush=True,
    )

    return {
        "label": label,
        "error": None,
        "full_n": full_metrics["n"],
        "full_wr": full_metrics["wr"],
        "full_pf": full_metrics["pf"],
        "full_pf_raw": full_metrics["pf_raw"],
        "full_exp_r": full_metrics["exp_r"],
        "windows": window_results,
        "avg_is_wr": avg_is_wr,
        "avg_oos_wr": avg_oos_wr,
        "avg_is_pf": avg_is_pf,
        "avg_oos_pf": avg_oos_pf,
        "avg_is_exp": avg_is_exp,
        "avg_oos_exp": avg_oos_exp,
        "avg_drift_wr": avg_drift_wr,
        "avg_drift_pf": avg_drift_pf,
        "is_robust": is_robust,
    }


# ── Report writer ──────────────────────────────────────────────────────────────

def _write_report(results: list[dict], runtime_s: float) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Walk-Forward IS/OOS — Top 5 Phase K2",
        "",
        "## Configuration",
        "",
        f"- Windows: {N_WINDOWS} rolling non-overlapping",
        f"- Split: {int(IS_PCT*100)}% IS / {int((1-IS_PCT)*100)}% OOS per window",
        f"- No re-optimization in IS — fixed TP/SL from K2",
        f"- Friction: 0.05R FX (EURUSD/USDJPY/GBPAUD) / 0.10R non-FX (WTI/NASDAQ100)",
        f"- Robustness gate: OOS WR drop < {ROBUST_WR_DROP_MAX*100:.0f}pp AND OOS PF drop < {ROBUST_PF_DROP_MAX:.2f}",
        f"- Runtime: {runtime_s:.0f}s ({runtime_s/60:.1f} min)",
        "",
        "---",
        "",
        "## Per-candidate per-window IS vs OOS",
        "",
    ]

    for i, res in enumerate(results, 1):
        label = res["label"]
        lines.append(f"### Candidate {i}: {label}")
        lines.append("")

        if res.get("error"):
            lines.append(f"**SKIPPED:** {res['error']}")
            lines.append("")
            continue

        # Full-period summary
        full_pf_raw = res.get("full_pf_raw", res["full_pf"])
        full_pf_str = "inf" if full_pf_raw == float("inf") else f"{full_pf_raw:.2f}"
        lines.append(
            f"Full period: n={res['full_n']}, WR={res['full_wr']:.3f}, "
            f"PF={full_pf_str}, ExpR={res['full_exp_r']:.3f}"
        )
        min_oos_n = min(w["oos_n"] for w in res["windows"]) if res["windows"] else 0
        if min_oos_n < 10:
            lines.append(
                f"> **Note:** min OOS window = {min_oos_n} trades — "
                f"per-window metrics are low-count and noisy. "
                f"PF capped at {_INF_PF_CAP} for avg/drift (all-win windows shown as inf)."
            )
        lines.append("")

        # Per-window table
        lines.append(
            "| window | IS n | IS WR | IS PF | IS expR "
            "| OOS n | OOS WR | OOS PF | OOS expR | drift_WR | drift_PF |"
        )
        lines.append("|---|---|---|---|---|---|---|---|---|---|---|")

        for w in res["windows"]:
            is_pf_str = "inf" if w["is_pf_raw"] == float("inf") else f"{w['is_pf_raw']:.2f}"
            oos_pf_str = "inf" if w["oos_pf_raw"] == float("inf") else f"{w['oos_pf_raw']:.2f}"
            lines.append(
                f"| {w['window']} "
                f"| {w['is_n']} | {w['is_wr']:.3f} | {is_pf_str} | {w['is_exp_r']:.3f} "
                f"| {w['oos_n']} | {w['oos_wr']:.3f} | {oos_pf_str} | {w['oos_exp_r']:.3f} "
                f"| {w['drift_wr']:+.3f} | {w['drift_pf']:+.2f} |"
            )

        # AVG row (uses capped PF for meaningful averaging)
        lines.append(
            f"| **AVG** "
            f"| — | {res['avg_is_wr']:.3f} | {res['avg_is_pf']:.2f}* | {res['avg_is_exp']:.3f} "
            f"| — | {res['avg_oos_wr']:.3f} | {res['avg_oos_pf']:.2f}* | {res['avg_oos_exp']:.3f} "
            f"| {res['avg_drift_wr']:+.3f} | {res['avg_drift_pf']:+.2f} |"
        )
        lines.append(f"*PF capped at {_INF_PF_CAP} for avg/drift when all-win windows present.")
        lines.append("")

    lines += [
        "---",
        "",
        "## Summary table (averages across 5 windows)",
        "",
        "| candidate | avg IS WR | avg OOS WR | drift WR | avg IS PF | avg OOS PF | drift PF | OOS robust? |",
        "|---|---|---|---|---|---|---|---|",
    ]

    robust_count = 0
    for i, res in enumerate(results, 1):
        label = res["label"]
        if res.get("error"):
            lines.append(f"| {i}. {label} | SKIP | SKIP | — | SKIP | SKIP | — | — |")
            continue
        flag = "YES" if res["is_robust"] else "NO"
        if res["is_robust"]:
            robust_count += 1
        lines.append(
            f"| {i}. {label} "
            f"| {res['avg_is_wr']:.3f} | {res['avg_oos_wr']:.3f} | {res['avg_drift_wr']:+.3f} "
            f"| {res['avg_is_pf']:.2f} | {res['avg_oos_pf']:.2f} | {res['avg_drift_pf']:+.2f} "
            f"| {flag} |"
        )

    n_valid = sum(1 for r in results if not r.get("error"))
    lines += [
        "",
        "---",
        "",
        "## Robustness verdict",
        "",
        f"- **OOS robust** = OOS WR drop < {ROBUST_WR_DROP_MAX*100:.0f}pp AND OOS PF drop < {ROBUST_PF_DROP_MAX:.2f}",
        f"- Candidates evaluated: {n_valid}/5",
        f"- **Survivors that pass robustness: {robust_count}/{n_valid}**",
        "",
    ]

    # Narrative per candidate
    lines.append("### Per-candidate verdict")
    lines.append("")
    for i, res in enumerate(results, 1):
        label = res["label"]
        if res.get("error"):
            lines.append(f"- **Candidate {i}** ({label}): SKIPPED — {res['error']}")
        elif res["is_robust"]:
            lines.append(
                f"- **Candidate {i}** ({label}): PASS — "
                f"avg OOS WR={res['avg_oos_wr']:.3f} (drift {res['avg_drift_wr']:+.3f}), "
                f"avg OOS PF={res['avg_oos_pf']:.2f} (drift {res['avg_drift_pf']:+.2f})"
            )
        else:
            reasons = []
            if abs(res["avg_drift_wr"]) > ROBUST_WR_DROP_MAX:
                reasons.append(
                    f"WR instability {res['avg_drift_wr']:+.3f} (|drift| > {ROBUST_WR_DROP_MAX:.2f})"
                )
            if res["avg_drift_pf"] < -ROBUST_PF_DROP_MAX:
                reasons.append(f"PF drop {res['avg_drift_pf']:+.2f} < -{ROBUST_PF_DROP_MAX:.2f} threshold")
            if not reasons:
                reasons.append("undetermined — check per-window table")
            lines.append(
                f"- **Candidate {i}** ({label}): FAIL — {'; '.join(reasons)}"
            )
    lines.append("")

    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n[WF] Report written to {OUTPUT_MD}", flush=True)


# ── Entry point ────────────────────────────────────────────────────────────────

def run() -> None:
    t_start = time.time()
    print("=" * 70, flush=True)
    print("[WF] Walk-Forward IS/OOS — Top 5 Phase K2 Candidates", flush=True)
    print(f"[WF] Windows: {N_WINDOWS} | IS: {int(IS_PCT*100)}% | OOS: {int((1-IS_PCT)*100)}%", flush=True)
    print("=" * 70, flush=True)

    results = []
    for cand in CANDIDATES:
        res = run_candidate(cand)
        results.append(res)

    runtime_s = time.time() - t_start
    _write_report(results, runtime_s)

    # Quick terminal summary
    print("\n" + "=" * 70, flush=True)
    print("[WF] SUMMARY", flush=True)
    print("=" * 70, flush=True)
    robust_count = 0
    n_valid = 0
    for i, res in enumerate(results, 1):
        if res.get("error"):
            print(f"  C{i}: {res['label'][:50]}... SKIPPED ({res['error']})", flush=True)
            continue
        n_valid += 1
        flag = "PASS" if res["is_robust"] else "FAIL"
        if res["is_robust"]:
            robust_count += 1
        print(
            f"  C{i}: {res['label'][:50]} | "
            f"OOS WR={res['avg_oos_wr']:.3f} (d{res['avg_drift_wr']:+.3f}) "
            f"OOS PF={res['avg_oos_pf']:.2f} (d{res['avg_drift_pf']:+.2f}) "
            f"[{flag}]",
            flush=True,
        )
    print(f"\n[WF] Robust survivors: {robust_count}/{n_valid}", flush=True)
    print(f"[WF] Total runtime: {runtime_s:.0f}s ({runtime_s/60:.1f} min)", flush=True)


if __name__ == "__main__":
    run()
