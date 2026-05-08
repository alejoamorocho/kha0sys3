"""ORB break-fade discovery — sweeps (sym, magic_time, duration, tp, sl)."""
import time
from dataclasses import replace as _replace
from pathlib import Path

import polars as pl

from src.strategies_external.common.backtester import run_backtest
from src.strategies_external.common.metrics import evaluate
from src.strategies_external.data_loader import load_csv, load_m1
from src.strategies_external.strategies.orb_breakfade import ORBBreakFadeAdapter

REPORTS_DIR = Path("reports/external")
M1_AVAILABLE = (
    "EURUSD", "USDJPY", "GBPAUD", "XAUUSD", "XAGUSD",
    "WTI", "BRENT", "NATGAS", "SP500", "NASDAQ100",
)
MAGIC_TIMES = ("07:00", "09:00", "12:00", "13:30", "15:00")
DURATIONS = (30, 60, 120)
TP_VALUES = (1.0, 1.5, 2.0)
SL_VALUES = (0.5, 1.0, 1.5)

# Phase-A gates
MIN_TRADES = 30
MIN_WR = 0.50
MIN_PF = 1.0


def _friction_for(sym: str) -> float:
    from src.domain.constants import INDEX_SYMBOLS, FRICTION_FX, FRICTION_INDEX
    return (FRICTION_INDEX if sym in INDEX_SYMBOLS else FRICTION_FX) + 0.2


def run_orb_breakfade_discovery(
    output_path: str = "reports/external/orb_breakfade_phase_g.md",
) -> pl.DataFrame:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    adapter = ORBBreakFadeAdapter()
    n_total = len(M1_AVAILABLE) * len(MAGIC_TIMES) * len(DURATIONS) * len(TP_VALUES) * len(SL_VALUES)
    print(f"[PhaseG] {n_total} combos to test", flush=True)

    rows = []
    backtest_count = 0
    t0 = time.time()
    for sym in M1_AVAILABLE:
        try:
            df_m15 = load_csv(sym, "M15")
        except FileNotFoundError:
            print(f"[PhaseG][SKIP] {sym} no M15", flush=True)
            continue
        m1 = load_m1(sym)
        if m1 is None:
            print(f"[PhaseG][SKIP] {sym} no M1", flush=True)
            continue
        friction = _friction_for(sym)
        # Pre-generate signals per (magic_time, duration). TP/SL applied later.
        sig_cache = {}
        for mt in MAGIC_TIMES:
            for dur in DURATIONS:
                key = (mt, dur)
                try:
                    sig_cache[key] = adapter.generate_signals_for_combo(
                        df_m15, m1, sym, mt, dur
                    )
                except Exception as e:
                    print(f"[PhaseG][SKIP] {sym} {mt}/{dur}: {e}", flush=True)
                    sig_cache[key] = []
        # Apply TP/SL grid
        for (mt, dur), base_sigs in sig_cache.items():
            if len(base_sigs) < MIN_TRADES:
                backtest_count += len(TP_VALUES) * len(SL_VALUES)
                continue
            for tp in TP_VALUES:
                for sl in SL_VALUES:
                    backtest_count += 1
                    if backtest_count % 100 == 0:
                        elapsed = time.time() - t0
                        pct = 100 * backtest_count / n_total
                        print(
                            f"[PhaseG] {backtest_count}/{n_total} ({pct:.0f}%) "
                            f"— {elapsed:.0f}s",
                            flush=True,
                        )
                    sigs = []
                    for s in base_sigs:
                        atr = s.indicator_anchors["atr_14"]
                        if s.side == "short":
                            stop = s.entry_price + sl * atr
                            tp1 = s.entry_price - tp * atr
                        else:
                            stop = s.entry_price - sl * atr
                            tp1 = s.entry_price + tp * atr
                        sigs.append(_replace(s, stop=stop, tp1=tp1, tp2=None))
                    try:
                        trades = run_backtest(sigs, m1, exit_mode="doc", risk_pct=0.005)
                    except Exception as e:
                        print(
                            f"[PhaseG][ERR] {sym} {mt}/{dur} tp={tp} sl={sl}: {e}",
                            flush=True,
                        )
                        continue
                    if len(trades) == 0:
                        continue
                    m_eval = evaluate(trades)
                    if (
                        m_eval["n_trades"] >= MIN_TRADES
                        and m_eval["win_rate"] >= MIN_WR
                        and m_eval["profit_factor"] >= MIN_PF
                    ):
                        rows.append({
                            "symbol": sym,
                            "magic_time": mt,
                            "duration": dur,
                            "tp_atr_mult": tp,
                            "sl_atr_mult": sl,
                            "n_trades": m_eval["n_trades"],
                            "wr": m_eval["win_rate"],
                            "pf": m_eval["profit_factor"],
                            "expectancy_r": m_eval["expectancy_R"],
                            "max_dd_r": m_eval["max_dd_R"],
                            "calmar": m_eval.get("calmar", 0.0),
                            "total_r": m_eval["total_R"],
                        })

    elapsed = time.time() - t0
    print(
        f"\n[PhaseG] complete in {elapsed:.0f}s"
        f" — {len(rows)} survivors out of {backtest_count}",
        flush=True,
    )
    df = (
        pl.DataFrame(rows).sort("calmar", descending=True)
        if rows
        else pl.DataFrame()
    )
    out = Path(output_path)
    if df.is_empty():
        out.write_text(
            f"# Phase G ORB break-fade\n- backtests: {backtest_count}\n- survivors: 0\n",
            encoding="utf-8",
        )
        return df

    lines = [
        "# ORB Break-Fade Discovery (Phase G)",
        "",
        f"- Backtests: {backtest_count}",
        f"- Survivors: {len(df)}",
        f"- Runtime: {elapsed:.0f}s ({elapsed / 60:.1f} min)",
        "- Mechanics: STOP entry at OR boundary break, INVERSE direction, TP/SL in ATR multipliers",
        "",
        "## Top 50 by Calmar",
        "",
        "| sym | magic | dur | tp | sl | n | wr | pf | exp_R | dd_R | calmar |",
        "|-----|-------|----|----|----|----|------|------|-------|------|--------|",
    ]
    for r in df.head(50).iter_rows(named=True):
        lines.append(
            f"| {r['symbol']} | {r['magic_time']} | {r['duration']}m | "
            f"{r['tp_atr_mult']:.1f} | {r['sl_atr_mult']:.1f} | "
            f"{r['n_trades']} | {r['wr']:.3f} | {r['pf']:.3f} | "
            f"{r['expectancy_r']:.3f} | {r['max_dd_r']:.1f} | {r['calmar']:.3f} |"
        )
    out.write_text("\n".join(lines), encoding="utf-8")
    df.write_parquet(REPORTS_DIR / "orb_breakfade_phase_g.parquet")
    return df


if __name__ == "__main__":
    df = run_orb_breakfade_discovery()
    print(f"\nTotal rows: {len(df)}", flush=True)
