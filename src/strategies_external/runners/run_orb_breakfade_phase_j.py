"""ORB break-fade Phase J — expanded discovery over all 10 M1 symbols.

Grid:
  Symbols (10):  EURUSD, USDJPY, GBPAUD, XAUUSD, XAGUSD, WTI, BRENT, NATGAS, SP500, NASDAQ100
  magic_times (5): 07:00, 09:00, 12:00, 13:30, 15:00
  Durations (3): 30, 60, 120 (minutes)
  TP/SL grid (49 = 7x7):
    TP: 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0
    SL: 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0
  ATR window: 14 (single)
  Exit mode: V1 baseline (TP/SL fixed)

Total: 10 x 5 x 3 x 49 = 7,350 backtests

STRICT filter:
  WR >= 0.60
  PF >= 1.30
  n_trades >= 30

If 0 survivors: report closest-to-gate per (sym, magic, dur).

Usage:
    python -u -m src.strategies_external.runners.run_orb_breakfade_phase_j
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

# ── Phase J grid ─────────────────────────────────────────────────────────────
SYMS = [
    "EURUSD", "USDJPY", "GBPAUD", "XAUUSD", "XAGUSD",
    "WTI", "BRENT", "NATGAS", "SP500", "NASDAQ100",
]
MAGIC_TIMES = ["07:00", "09:00", "12:00", "13:30", "15:00"]
DURATIONS   = [30, 60, 120]
TP_GRID     = (0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0)
SL_GRID     = (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0)
ATR_WINDOW  = 14

# Strict gates
MIN_TRADES = 30
MIN_WR     = 0.60
MIN_PF     = 1.30
RISK_PCT   = 0.005


def _attach_rr(sigs: list[Signal], tp_mult: float, sl_mult: float) -> list[Signal]:
    """Attach ATR-based TP/SL to base signals."""
    out: list[Signal] = []
    for s in sigs:
        atr = s.indicator_anchors["atr_14"]
        if s.side == "short":
            stop = s.entry_price + sl_mult * atr
            tp1  = s.entry_price - tp_mult * atr
        else:
            stop = s.entry_price - sl_mult * atr
            tp1  = s.entry_price + tp_mult * atr
        out.append(_replace(s, stop=stop, tp1=tp1, tp2=None))
    return out


def run_phase_j(
    output_stem: str = "reports/external/orb_breakfade_phase_j",
) -> pl.DataFrame:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    n_rr  = len(TP_GRID) * len(SL_GRID)
    total_expected = len(SYMS) * len(MAGIC_TIMES) * len(DURATIONS) * n_rr
    print(
        f"[PhaseJ] Grid: {len(SYMS)} syms x {len(MAGIC_TIMES)} magic_times x "
        f"{len(DURATIONS)} durations x {n_rr} TP/SL = {total_expected} backtests",
        flush=True,
    )
    print(
        f"[PhaseJ] ATR window: {ATR_WINDOW}  |  "
        f"Strict gates: WR>={MIN_WR} AND PF>={MIN_PF} AND n>={MIN_TRADES}",
        flush=True,
    )

    adapter = ORBBreakFadeAdapter()

    # ── Load M15 + M1 data for each symbol ───────────────────────────────────
    m15_cache: dict[str, pl.DataFrame | None] = {}
    m1_cache:  dict[str, pl.DataFrame | None] = {}

    for sym in SYMS:
        try:
            m15_cache[sym] = load_csv(sym, "M15")
        except FileNotFoundError:
            print(f"[PhaseJ][SKIP] {sym} — no M15 data", flush=True)
            m15_cache[sym] = None
        m1_df = load_m1(sym)
        m1_cache[sym] = m1_df
        if m1_df is None:
            print(f"[PhaseJ][SKIP] {sym} — no M1 data", flush=True)
        elif m15_cache[sym] is not None:
            print(
                f"[PhaseJ][Load] {sym}: M1 {len(m1_df):,} rows, "
                f"M15 {len(m15_cache[sym]):,} rows",
                flush=True,
            )

    # ── Phase 1: Signal generation cache ─────────────────────────────────────
    print("\n[PhaseJ] === Phase 1: Signal generation cache ===", flush=True)
    sig_cache: dict[tuple, list[Signal]] = {}

    for sym in SYMS:
        df_m15 = m15_cache.get(sym)
        m1_df  = m1_cache.get(sym)
        if df_m15 is None or m1_df is None:
            for magic in MAGIC_TIMES:
                for dur in DURATIONS:
                    sig_cache[(sym, magic, dur)] = []
            continue

        for magic in MAGIC_TIMES:
            for dur in DURATIONS:
                key = (sym, magic, dur)
                try:
                    sigs = adapter.generate_signals_for_combo(
                        df_m15, m1_df, sym, magic, dur, atr_window=ATR_WINDOW
                    )
                    sig_cache[key] = sigs
                    print(
                        f"[Cache] {sym}/{magic}/{dur}m: {len(sigs)} signals",
                        flush=True,
                    )
                except Exception as e:
                    print(
                        f"[Cache][ERR] {sym}/{magic}/{dur}m: {e}",
                        flush=True,
                    )
                    sig_cache[key] = []

    # ── Phase 2: TP/SL grid sweep ─────────────────────────────────────────────
    print("\n[PhaseJ] === Phase 2: TP/SL grid sweep ===", flush=True)

    survivors:  list[dict] = []
    all_results: list[dict] = []
    backtest_count = 0
    skipped_count  = 0
    t0 = time.time()

    for sym in SYMS:
        m1_df = m1_cache.get(sym)
        if m1_df is None:
            skipped_count += len(MAGIC_TIMES) * len(DURATIONS) * n_rr
            continue
        m1_arrays  = _precompute_m1_arrays(m1_df)
        friction_r = friction_for(sym)

        for magic in MAGIC_TIMES:
            for dur in DURATIONS:
                key       = (sym, magic, dur)
                base_sigs = sig_cache.get(key, [])

                if len(base_sigs) < MIN_TRADES:
                    skipped_count += n_rr
                    continue

                for tp in TP_GRID:
                    for sl in SL_GRID:
                        backtest_count += 1
                        if backtest_count % 500 == 0:
                            elapsed_so_far = time.time() - t0
                            pct = 100.0 * backtest_count / total_expected
                            print(
                                f"[PhaseJ] {backtest_count}/{total_expected} "
                                f"({pct:.0f}%) — {elapsed_so_far:.0f}s  "
                                f"survivors={len(survivors)}",
                                flush=True,
                            )

                        sigs_rr = _attach_rr(base_sigs, tp, sl)

                        try:
                            trades = _run_orb_with_alt_exit(
                                sigs_rr,
                                m1_arrays,
                                exit_mode="baseline",
                                friction_r=friction_r,
                            )
                        except Exception as e:
                            print(
                                f"[PhaseJ][ERR] {sym} {magic}/{dur}m "
                                f"tp={tp} sl={sl}: {e}",
                                flush=True,
                            )
                            continue

                        if not trades:
                            continue

                        m = evaluate(trades)

                        result = {
                            "symbol":       sym,
                            "magic_time":   magic,
                            "duration":     dur,
                            "atr_window":   ATR_WINDOW,
                            "tp_mult":      tp,
                            "sl_mult":      sl,
                            "n_trades":     m["n_trades"],
                            "wr":           m["win_rate"],
                            "pf":           m["profit_factor"],
                            "expectancy_r": m["expectancy_R"],
                            "max_dd_r":     m["max_dd_R"],
                            "calmar":       m.get("calmar", 0.0),
                            "total_r":      m["total_R"],
                            "sharpe":       m.get("sharpe", 0.0),
                        }
                        all_results.append(result)

                        if (
                            m["n_trades"]          >= MIN_TRADES
                            and m["win_rate"]       >= MIN_WR
                            and m["profit_factor"]  >= MIN_PF
                        ):
                            survivors.append(result)

    elapsed = time.time() - t0
    print(
        f"\n[PhaseJ] complete in {elapsed:.0f}s ({elapsed / 60:.1f} min)"
        f"  backtests={backtest_count}  skipped={skipped_count}"
        f"  survivors={len(survivors)}",
        flush=True,
    )

    df_survivors = (
        pl.DataFrame(survivors).sort("calmar", descending=True)
        if survivors
        else pl.DataFrame()
    )
    df_all = (
        pl.DataFrame(all_results).sort("calmar", descending=True)
        if all_results
        else pl.DataFrame()
    )

    # Save parquets
    if not df_survivors.is_empty():
        df_survivors.write_parquet(f"{output_stem}.parquet")
        print(f"[PhaseJ] Survivors parquet: {output_stem}.parquet", flush=True)
    if not df_all.is_empty():
        df_all.write_parquet(f"{output_stem}_all.parquet")
        print(f"[PhaseJ] All-results parquet: {output_stem}_all.parquet", flush=True)

    _write_report(
        df_survivors, df_all,
        backtest_count, skipped_count, elapsed,
        output_stem, sig_cache,
    )
    return df_survivors


# ── Report writer ─────────────────────────────────────────────────────────────

def _write_report(
    df: pl.DataFrame,
    df_all: pl.DataFrame,
    backtest_count: int,
    skipped_count: int,
    elapsed: float,
    output_stem: str,
    sig_cache: dict[tuple, list],
) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out_md = Path(f"{output_stem}.md")
    n_survivors = len(df)

    lines = [
        "# Phase J — ORB Break-Fade: All-Symbol M1 Discovery",
        "",
        f"- Symbols: {SYMS}",
        f"- magic_times: {MAGIC_TIMES}",
        f"- Durations: {DURATIONS} min",
        f"- TP grid: {list(TP_GRID)}",
        f"- SL grid: {list(SL_GRID)}",
        f"- ATR window: {ATR_WINDOW}",
        f"- Total TP x SL combos per (sym, magic, dur): {len(TP_GRID) * len(SL_GRID)}",
        f"- Backtests run: {backtest_count}",
        f"- Backtests skipped (< {MIN_TRADES} signals or missing data): {skipped_count}",
        f"- Survivors (WR>={MIN_WR} AND PF>={MIN_PF} AND n>={MIN_TRADES}): {n_survivors}",
        f"- Runtime: {elapsed:.0f}s ({elapsed / 60:.1f} min)",
        "",
    ]

    # ── TOP 30 by Calmar ──────────────────────────────────────────────────────
    if not df.is_empty():
        lines += [
            "## TOP 30 by Calmar (strict survivors)",
            "",
            "| # | sym | magic | dur | tp | sl | n | WR | PF | exp_R | dd_R | calmar | total_R |",
            "|---|-----|-------|-----|----|----|---|-----|-----|-------|------|--------|---------|",
        ]
        for rank, r in enumerate(
            df.sort("calmar", descending=True).head(30).iter_rows(named=True), 1
        ):
            lines.append(
                f"| {rank} | {r['symbol']} | {r['magic_time']} | {r['duration']}m"
                f" | {r['tp_mult']:.2f} | {r['sl_mult']:.2f}"
                f" | {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.3f}"
                f" | {r['expectancy_r']:.4f} | {r['max_dd_r']:.1f}"
                f" | {r['calmar']:.3f} | {r['total_r']:.2f} |"
            )

        # ── TOP 30 by PF ──────────────────────────────────────────────────────
        lines += [
            "",
            "## TOP 30 by PF (strict survivors)",
            "",
            "| # | sym | magic | dur | tp | sl | n | WR | PF | exp_R | dd_R | calmar | total_R |",
            "|---|-----|-------|-----|----|----|---|-----|-----|-------|------|--------|---------|",
        ]
        for rank, r in enumerate(
            df.sort("pf", descending=True).head(30).iter_rows(named=True), 1
        ):
            lines.append(
                f"| {rank} | {r['symbol']} | {r['magic_time']} | {r['duration']}m"
                f" | {r['tp_mult']:.2f} | {r['sl_mult']:.2f}"
                f" | {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.3f}"
                f" | {r['expectancy_r']:.4f} | {r['max_dd_r']:.1f}"
                f" | {r['calmar']:.3f} | {r['total_r']:.2f} |"
            )
    else:
        lines += [
            "## TOP 30 by Calmar",
            "",
            "**No survivors met WR>=0.60 AND PF>=1.30 AND n>=30.**",
            "",
            "## TOP 30 by PF",
            "",
            "**No survivors met WR>=0.60 AND PF>=1.30 AND n>=30.**",
            "",
        ]

    # ── Best per (sym, magic, dur) ────────────────────────────────────────────
    lines += [
        "",
        "## Best per (sym, magic_time, duration) — up to 150 combos",
        "",
        "For each combination with >= 30 signals: best survivor (SURVIVOR) or",
        "closest-to-gate combo (WR/PF Euclidean distance). Combos with 0 results",
        "or < 30 signals are omitted.",
        "",
        "| # | sym | magic | dur | n_sigs | best_tp | best_sl | n_trades | WR | PF | calmar | note |",
        "|---|-----|-------|-----|--------|---------|---------|----------|-----|-----|--------|------|",
    ]

    if not df_all.is_empty():
        rank = 0
        for sym in SYMS:
            for magic in MAGIC_TIMES:
                for dur in DURATIONS:
                    n_sigs = len(sig_cache.get((sym, magic, dur), []))
                    if n_sigs < MIN_TRADES:
                        continue

                    combo_all = df_all.filter(
                        (pl.col("symbol") == sym)
                        & (pl.col("magic_time") == magic)
                        & (pl.col("duration") == dur)
                    )
                    if combo_all.is_empty():
                        continue

                    rank += 1

                    # Check if any survivor for this combo
                    if not df.is_empty():
                        combo_surv = df.filter(
                            (pl.col("symbol") == sym)
                            & (pl.col("magic_time") == magic)
                            & (pl.col("duration") == dur)
                        )
                    else:
                        combo_surv = pl.DataFrame()

                    if not combo_surv.is_empty():
                        best = combo_surv.sort("calmar", descending=True).head(1).row(0, named=True)
                        note = "SURVIVOR"
                    else:
                        # Closest-to-gate: minimise dist to (MIN_WR, MIN_PF)
                        # dist = sqrt( max(0, MIN_WR - wr)^2 + max(0, MIN_PF - pf)^2 )
                        with_dist = combo_all.with_columns(
                            (
                                (
                                    pl.when(pl.col("wr") < MIN_WR)
                                    .then((pl.col("wr") - MIN_WR).pow(2))
                                    .otherwise(0.0)
                                )
                                + (
                                    pl.when(pl.col("pf") < MIN_PF)
                                    .then((pl.col("pf") - MIN_PF).pow(2))
                                    .otherwise(0.0)
                                )
                            ).sqrt().alias("dist")
                        ).sort("dist")
                        best_row = with_dist.head(1).row(0, named=True)
                        dist_val = best_row.get("dist", 0.0)
                        best = best_row
                        note = f"closest(d={dist_val:.4f})"

                    lines.append(
                        f"| {rank} | {sym} | {magic} | {dur}m"
                        f" | {n_sigs}"
                        f" | {best['tp_mult']:.2f} | {best['sl_mult']:.2f}"
                        f" | {best['n_trades']} | {best['wr']:.3f} | {best['pf']:.3f}"
                        f" | {best['calmar']:.3f} | {note} |"
                    )
    else:
        lines.append(
            "No results available (all combos had < 30 signals or data missing)."
        )

    # ── Per-symbol survivor count ─────────────────────────────────────────────
    lines += [
        "",
        "## Per-symbol distribution (strict survivors)",
        "",
        "| sym | survivors | best_WR | best_PF | best_calmar |",
        "|-----|-----------|---------|---------|-------------|",
    ]
    for sym in SYMS:
        if not df.is_empty():
            sym_df = df.filter(pl.col("symbol") == sym)
        else:
            sym_df = pl.DataFrame()

        n_s = len(sym_df)
        if n_s > 0:
            best_wr  = sym_df["wr"].max()
            best_pf  = sym_df["pf"].max()
            best_cal = sym_df["calmar"].max()
            lines.append(
                f"| {sym} | {n_s} | {best_wr:.3f} | {best_pf:.3f} | {best_cal:.3f} |"
            )
        else:
            lines.append(f"| {sym} | 0 | — | — | — |")

    # ── WR / PF distribution analysis ─────────────────────────────────────────
    if not df_all.is_empty():
        wrs = sorted(df_all["wr"].to_list())
        pfs = sorted(df_all["pf"].to_list())
        n_total = len(wrs)

        def pctile(lst: list, p: int) -> float:
            idx = min(int(len(lst) * p / 100), len(lst) - 1)
            return lst[idx]

        pf_capped_max = min(max(pfs), 999.0)

        lines += [
            "",
            "## Distribution analysis (all backtests)",
            "",
            f"Total results with trades: {n_total}",
            "",
            f"- WR: p50={pctile(wrs,50):.3f}  p75={pctile(wrs,75):.3f}"
            f"  p90={pctile(wrs,90):.3f}  max={max(wrs):.3f}",
            f"- PF: p50={pctile(pfs,50):.3f}  p75={pctile(pfs,75):.3f}"
            f"  p90={pctile(pfs,90):.3f}  max={pf_capped_max:.3f}",
            "",
        ]

        wr60 = df_all.filter(pl.col("wr") >= MIN_WR)
        lines.append(f"Rows with WR>={MIN_WR}: {len(wr60)}")
        if not wr60.is_empty():
            pf_of_wr60 = sorted(wr60["pf"].to_list())
            lines.append(
                f"  PF of those: p50={pctile(pf_of_wr60,50):.3f}, "
                f"p75={pctile(pf_of_wr60,75):.3f}, p90={pctile(pf_of_wr60,90):.3f}, "
                f"max={min(max(pf_of_wr60), 999.0):.3f}"
            )

        pf130 = df_all.filter(pl.col("pf") >= MIN_PF)
        lines.append(f"\nRows with PF>={MIN_PF}: {len(pf130)}")
        if not pf130.is_empty():
            wr_of_pf130 = sorted(pf130["wr"].to_list())
            lines.append(
                f"  WR of those: p50={pctile(wr_of_pf130,50):.3f}, "
                f"p75={pctile(wr_of_pf130,75):.3f}, p90={pctile(wr_of_pf130,90):.3f}, "
                f"max={max(wr_of_pf130):.3f}"
            )

        # Closest-to-gate section — only when no strict survivors
        if df.is_empty():
            lines += [
                "",
                "## Closest-to-gate per (sym, magic, dur) — no strict survivors",
                "",
                "| sym | magic | dur | n_sigs | tp | sl | n_trades | WR | PF | dist_to_gate |",
                "|-----|-------|-----|--------|----|----|----------|-----|-----|--------------|",
            ]
            for sym in SYMS:
                for magic in MAGIC_TIMES:
                    for dur in DURATIONS:
                        n_sigs = len(sig_cache.get((sym, magic, dur), []))
                        combo = df_all.filter(
                            (pl.col("symbol") == sym)
                            & (pl.col("magic_time") == magic)
                            & (pl.col("duration") == dur)
                        )
                        if combo.is_empty():
                            continue
                        with_dist = combo.with_columns(
                            (
                                (
                                    pl.when(pl.col("wr") < MIN_WR)
                                    .then((pl.col("wr") - MIN_WR).pow(2))
                                    .otherwise(0.0)
                                )
                                + (
                                    pl.when(pl.col("pf") < MIN_PF)
                                    .then((pl.col("pf") - MIN_PF).pow(2))
                                    .otherwise(0.0)
                                )
                            ).sqrt().alias("dist")
                        ).sort("dist")
                        best = with_dist.head(1).row(0, named=True)
                        lines.append(
                            f"| {sym} | {magic} | {dur}m"
                            f" | {n_sigs}"
                            f" | {best['tp_mult']:.2f} | {best['sl_mult']:.2f}"
                            f" | {best['n_trades']} | {best['wr']:.3f} | {best['pf']:.3f}"
                            f" | {best.get('dist', 0.0):.4f} |"
                        )

    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[PhaseJ] Report written to {out_md}", flush=True)


if __name__ == "__main__":
    # ── Sanity test: SP500 09:00 60m TP=0.5 SL=2.0 atr_w=14 ─────────────────
    print(
        "[PhaseJ] Sanity test: SP500 09:00 60m TP=0.5 SL=2.0 atr_w=14",
        flush=True,
    )
    _adapter_st = ORBBreakFadeAdapter()
    try:
        _df_m15_st = load_csv("SP500", "M15")
    except FileNotFoundError:
        _df_m15_st = None
    _m1_df_st  = load_m1("SP500")

    _sanity_ok = False
    if _m1_df_st is not None and _df_m15_st is not None:
        _m1_arrays_st = _precompute_m1_arrays(_m1_df_st)
        _base_st = _adapter_st.generate_signals_for_combo(
            _df_m15_st, _m1_df_st, "SP500", "09:00", 60, atr_window=14
        )
        print(f"  Signals generated: {len(_base_st)}", flush=True)
        if _base_st:
            _sigs_st   = _attach_rr(_base_st, tp_mult=0.5, sl_mult=2.0)
            _fr_st     = friction_for("SP500")
            _trades_st = _run_orb_with_alt_exit(
                _sigs_st, _m1_arrays_st, exit_mode="baseline", friction_r=_fr_st
            )
            _m_st = evaluate(_trades_st)
            print(
                f"  Result: n={_m_st['n_trades']} WR={_m_st['win_rate']:.3f} "
                f"PF={_m_st['profit_factor']:.3f} calmar={_m_st['calmar']:.3f}",
                flush=True,
            )
            n_ok  = _m_st["n_trades"] >= 1
            wr_ok = 0.0 <= _m_st["win_rate"] <= 1.0
            _sanity_ok = n_ok and wr_ok
            print(
                f"  Sanity: {'PASS' if _sanity_ok else 'FAIL'}"
                f"  (n>={1}: {n_ok}, WR in [0,1]: {wr_ok})",
                flush=True,
            )
        else:
            print(
                "  [WARN] 0 signals for SP500 09:00 60m — sanity inconclusive",
                flush=True,
            )
    else:
        print(
            "  [WARN] Missing SP500 M1 or M15 data — sanity test skipped",
            flush=True,
        )

    print("\n[PhaseJ] Starting full sweep...\n", flush=True)
    _df_result = run_phase_j()
    print(f"\n[PhaseJ] Done. Survivors: {len(_df_result)}", flush=True)
