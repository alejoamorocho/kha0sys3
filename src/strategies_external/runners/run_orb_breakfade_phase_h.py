"""ORB break-fade Phase H — ATR window sweep + alternative exit modes.

For each of the 12 Phase G survivors (loaded from reports/external/orb_breakfade_phase_g.parquet):
  - 5 ATR windows: 5, 10, 14 (default), 20, 50
  - 22 exit variants:
      V1  baseline (TP/SL ATR fixed, Phase G default)
      V4  trailing ATR: 0.5, 1.0, 1.5, 2.0, 2.5  (5 variants)
      V5  SMA cross M1: 10, 20, 50, 100, 200     (5 variants)
      V6  time fixed M1 bars: 30, 60, 120, 240, 480 (5 variants)
      V7  break-back: exit on return to opposite OR boundary (1 variant)
      V8  partial TP1+BE: 50% at TP1, move stop to BE (1 variant)
      V8b partial TP1+trail: 50% at TP1, trail 1xATR remaining (1 variant)

Total: 12 x 5 x 22 = 1320 backtests.

Phase-A gates: n_trades >= 30, WR >= 0.50, PF >= 1.0

Usage:
    python -u -m src.strategies_external.runners.run_orb_breakfade_phase_h
"""
from __future__ import annotations

import bisect
import time
from dataclasses import replace as _replace
from pathlib import Path

import polars as pl

from src.strategies_external.common.metrics import evaluate
from src.strategies_external.common.signal import Signal
from src.strategies_external.common.trade import Trade
from src.strategies_external.constants import friction_for
from src.strategies_external.data_loader import load_csv, load_m1
from src.strategies_external.strategies.orb_breakfade import ORBBreakFadeAdapter

REPORTS_DIR = Path("reports/external")

ATR_WINDOWS = (5, 10, 14, 20, 50)

# Exit variant definitions
# Each is a tuple (variant_name, kwargs for _run_orb_with_alt_exit)
_V4_TRAILS = [(f"V4_trail_{m}", {"exit_mode": "trailing_atr", "trailing_atr_mult": m})
              for m in (0.5, 1.0, 1.5, 2.0, 2.5)]
_V5_SMAS   = [(f"V5_sma{w}",    {"exit_mode": "sma_cross",    "sma_window":         w})
              for w in (10, 20, 50, 100, 200)]
_V6_TIMES  = [(f"V6_time{b}",   {"exit_mode": "time_fixed",   "time_fixed_bars":    b})
              for b in (30, 60, 120, 240, 480)]
_V7        = [("V7_breakback",  {"exit_mode": "break_back"})]
_V8        = [("V8_partial_be", {"exit_mode": "partial_tp_be"})]
_V8B       = [("V8b_partial_trail", {"exit_mode": "partial_tp_trail"})]

EXIT_VARIANTS: list[tuple[str, dict]] = (
    [("V1_baseline",         {"exit_mode": "baseline"})]
    + _V4_TRAILS
    + _V5_SMAS
    + _V6_TIMES
    + _V7
    + _V8
    + _V8B
)  # total 22

# Phase-A gates
MIN_TRADES = 30
MIN_WR     = 0.50
MIN_PF     = 1.0
RISK_PCT   = 0.005


# ── M1 arrays helper ──────────────────────────────────────────────────────────

def _precompute_m1_arrays(m1_df: pl.DataFrame) -> dict:
    """Convert M1 DataFrame to plain Python lists for fast random access."""
    m1s = m1_df.sort("time")
    return {
        "times":  m1s["time"].to_list(),
        "highs":  m1s["high"].to_list(),
        "lows":   m1s["low"].to_list(),
        "closes": m1s["close"].to_list(),
    }


# ── Core alt-exit backtester ──────────────────────────────────────────────────

def _run_orb_with_alt_exit(
    signals: list[Signal],
    m1_arrays: dict,
    exit_mode: str,
    friction_r: float,
    # V4 trailing
    trailing_atr_mult: float = 1.0,
    # V5 SMA cross
    sma_window: int = 20,
    # V6 time fixed
    time_fixed_bars: int = 240,
) -> list[Trade]:
    """Run ORB break-fade signals with alternative exit logic.

    All modes:
    - Entry: market at close of break bar (already baked into Signal.entry_price).
    - Signals already have stop/tp1 set from the outer loop (ATR fixed TP/SL).
    - SL-first conservative: intra-bar if both SL and TP touched, SL wins.
    - Session-end timestop via Signal.valid_until (23:59 of trade date).

    Exit modes:
        baseline        — TP/SL ATR fixed (Phase G V1).
        trailing_atr    — trailing stop (trailing_atr_mult x ATR from best price).
        sma_cross       — exit when M1 close crosses SMA(sma_window) against trade.
        time_fixed      — exit after time_fixed_bars M1 bars from fill.
        break_back      — exit when price returns to opposite OR boundary.
        partial_tp_be   — 50% at TP1, move stop to BE for remaining 50%.
        partial_tp_trail — 50% at TP1, trail 1xATR on remaining 50%.
    """
    if not signals:
        return []

    m1_times  = m1_arrays["times"]
    m1_highs  = m1_arrays["highs"]
    m1_lows   = m1_arrays["lows"]
    m1_closes = m1_arrays["closes"]
    n_m1      = len(m1_times)

    # Pre-compute SMA on all M1 closes for sma_cross mode.
    sma_arr: list[float | None] | None = None
    if exit_mode == "sma_cross":
        sma_arr = [None] * n_m1
        if n_m1 >= sma_window:
            running = sum(m1_closes[:sma_window])
            sma_arr[sma_window - 1] = running / sma_window
            for i in range(sma_window, n_m1):
                running += m1_closes[i] - m1_closes[i - sma_window]
                sma_arr[i] = running / sma_window

    trades: list[Trade] = []

    for sig in signals:
        atr = sig.indicator_anchors.get("atr_14", 0.0)
        or_high = sig.indicator_anchors.get("or_high")
        or_low  = sig.indicator_anchors.get("or_low")
        if atr <= 0:
            continue

        # Entry: first M1 bar strictly after setup_ts (break bar close).
        start_idx = bisect.bisect_right(m1_times, sig.setup_ts)
        if start_idx >= n_m1:
            continue

        # Entry is market at the break bar close (entry_price already set).
        entry_price = sig.entry_price
        entry_idx   = start_idx  # first bar AFTER entry confirmation

        # R denominator based on the signal's ATR-fixed stop distance.
        R = abs(entry_price - sig.stop)
        if R <= 0:
            continue

        # TP and SL caps from the signal (ATR-fixed, always serve as protection).
        tp_cap = sig.tp1
        sl_cap = sig.stop

        is_long  = sig.side == "long"
        is_short = not is_long

        # Valid until: 23:59 of trade date.
        valid_until = sig.valid_until

        # Trailing state (V4 and V8b).
        if is_long:
            best_favorable = entry_price
            trailing_stop  = sl_cap
        else:
            best_favorable = entry_price
            trailing_stop  = sl_cap

        time_fixed_end = entry_idx + time_fixed_bars

        # Partial fill tracking (V8 / V8b).
        partial_hit  = False   # True after first 50% close at TP1
        partial_pnl_r = 0.0    # R from the first half
        be_stop: float | None = None   # V8: breakeven stop after partial
        trail_stop_partial: float | None = None  # V8b: trailing stop after partial

        # Per-mode initial trailing stop for partial.
        if is_long:
            trail_stop_partial = sl_cap
        else:
            trail_stop_partial = sl_cap

        exit_reason: str | None = None
        exit_price:  float | None = None
        exit_ts = None

        for j in range(entry_idx, n_m1):
            bt = m1_times[j]

            # Session-end timestop (valid_until = 23:59 of trade date).
            if bt > valid_until:
                # Close at last known close before valid_until.
                prev = j - 1
                exit_reason = "eod"
                exit_price  = m1_closes[prev] if prev >= entry_idx else entry_price
                exit_ts     = m1_times[prev]  if prev >= entry_idx else bt
                break

            hi = m1_highs[j]
            lo = m1_lows[j]
            cl = m1_closes[j]
            if hi is None or lo is None:
                continue

            # ─── BASELINE (V1) ────────────────────────────────────────────
            if exit_mode == "baseline":
                if is_long:
                    if lo <= sl_cap:
                        exit_reason = "stop"; exit_price = sl_cap; exit_ts = bt; break
                    if tp_cap is not None and hi >= tp_cap:
                        exit_reason = "tp1"; exit_price = tp_cap; exit_ts = bt; break
                else:
                    if hi >= sl_cap:
                        exit_reason = "stop"; exit_price = sl_cap; exit_ts = bt; break
                    if tp_cap is not None and lo <= tp_cap:
                        exit_reason = "tp1"; exit_price = tp_cap; exit_ts = bt; break

            # ─── TRAILING ATR (V4) ────────────────────────────────────────
            elif exit_mode == "trailing_atr":
                # SL-first: check protective stop BEFORE trailing.
                if is_long:
                    if lo <= sl_cap:
                        exit_reason = "stop"; exit_price = sl_cap; exit_ts = bt; break
                    if tp_cap is not None and hi >= tp_cap:
                        exit_reason = "tp1"; exit_price = tp_cap; exit_ts = bt; break
                    # Update trailing.
                    if hi > best_favorable:
                        best_favorable = hi
                        new_trail = best_favorable - trailing_atr_mult * atr
                        if new_trail > trailing_stop:
                            trailing_stop = new_trail
                    if lo <= trailing_stop:
                        exit_reason = "trail"; exit_price = trailing_stop; exit_ts = bt; break
                else:
                    if hi >= sl_cap:
                        exit_reason = "stop"; exit_price = sl_cap; exit_ts = bt; break
                    if tp_cap is not None and lo <= tp_cap:
                        exit_reason = "tp1"; exit_price = tp_cap; exit_ts = bt; break
                    if lo < best_favorable or best_favorable == entry_price:
                        if best_favorable == entry_price or lo < best_favorable:
                            best_favorable = lo
                        new_trail = best_favorable + trailing_atr_mult * atr
                        if new_trail < trailing_stop:
                            trailing_stop = new_trail
                    if hi >= trailing_stop:
                        exit_reason = "trail"; exit_price = trailing_stop; exit_ts = bt; break

            # ─── SMA CROSS (V5) ───────────────────────────────────────────
            elif exit_mode == "sma_cross":
                # SL-first conservative.
                if is_long:
                    if lo <= sl_cap:
                        exit_reason = "stop"; exit_price = sl_cap; exit_ts = bt; break
                    if tp_cap is not None and hi >= tp_cap:
                        exit_reason = "tp1"; exit_price = tp_cap; exit_ts = bt; break
                else:
                    if hi >= sl_cap:
                        exit_reason = "stop"; exit_price = sl_cap; exit_ts = bt; break
                    if tp_cap is not None and lo <= tp_cap:
                        exit_reason = "tp1"; exit_price = tp_cap; exit_ts = bt; break
                if sma_arr is not None:
                    sma_val = sma_arr[j]
                    if sma_val is not None:
                        if is_long and cl < sma_val:
                            exit_reason = "sma_cross"; exit_price = cl; exit_ts = bt; break
                        elif is_short and cl > sma_val:
                            exit_reason = "sma_cross"; exit_price = cl; exit_ts = bt; break

            # ─── TIME FIXED (V6) ──────────────────────────────────────────
            elif exit_mode == "time_fixed":
                # SL-first conservative.
                if is_long:
                    if lo <= sl_cap:
                        exit_reason = "stop"; exit_price = sl_cap; exit_ts = bt; break
                    if tp_cap is not None and hi >= tp_cap:
                        exit_reason = "tp1"; exit_price = tp_cap; exit_ts = bt; break
                else:
                    if hi >= sl_cap:
                        exit_reason = "stop"; exit_price = sl_cap; exit_ts = bt; break
                    if tp_cap is not None and lo <= tp_cap:
                        exit_reason = "tp1"; exit_price = tp_cap; exit_ts = bt; break
                if j >= time_fixed_end:
                    exit_reason = "time_fixed"; exit_price = cl; exit_ts = bt; break

            # ─── BREAK-BACK (V7) ──────────────────────────────────────────
            elif exit_mode == "break_back":
                if or_high is None or or_low is None:
                    # Fallback to baseline if OR bounds missing.
                    if is_long:
                        if lo <= sl_cap:
                            exit_reason = "stop"; exit_price = sl_cap; exit_ts = bt; break
                        if tp_cap is not None and hi >= tp_cap:
                            exit_reason = "tp1"; exit_price = tp_cap; exit_ts = bt; break
                    else:
                        if hi >= sl_cap:
                            exit_reason = "stop"; exit_price = sl_cap; exit_ts = bt; break
                        if tp_cap is not None and lo <= tp_cap:
                            exit_reason = "tp1"; exit_price = tp_cap; exit_ts = bt; break
                else:
                    # SL-first conservative.
                    if is_long:
                        if lo <= sl_cap:
                            exit_reason = "stop"; exit_price = sl_cap; exit_ts = bt; break
                        if tp_cap is not None and hi >= tp_cap:
                            exit_reason = "tp1"; exit_price = tp_cap; exit_ts = bt; break
                        # SHORT entered at break_up → exit when close <= or_low.
                        # LONG entered at break_down → exit when close >= or_high.
                        if cl >= or_high:
                            exit_reason = "break_back"; exit_price = cl; exit_ts = bt; break
                    else:
                        if hi >= sl_cap:
                            exit_reason = "stop"; exit_price = sl_cap; exit_ts = bt; break
                        if tp_cap is not None and lo <= tp_cap:
                            exit_reason = "tp1"; exit_price = tp_cap; exit_ts = bt; break
                        if cl <= or_low:
                            exit_reason = "break_back"; exit_price = cl; exit_ts = bt; break

            # ─── PARTIAL TP1 + BE (V8) ────────────────────────────────────
            elif exit_mode == "partial_tp_be":
                if not partial_hit:
                    # First half: looking for SL or TP1.
                    # SL-first conservative.
                    if is_long:
                        if lo <= sl_cap:
                            # Both halves stopped.
                            exit_reason = "stop"
                            exit_price = sl_cap
                            exit_ts = bt
                            break
                        if tp_cap is not None and hi >= tp_cap:
                            # First half hits TP1.
                            partial_hit   = True
                            partial_pnl_r = (tp_cap - entry_price) / R
                            be_stop       = entry_price   # Move stop to BE.
                            # Continue loop for second half.
                    else:
                        if hi >= sl_cap:
                            exit_reason = "stop"; exit_price = sl_cap; exit_ts = bt; break
                        if tp_cap is not None and lo <= tp_cap:
                            partial_hit   = True
                            partial_pnl_r = (entry_price - tp_cap) / R
                            be_stop       = entry_price
                else:
                    # Second half: use BE stop. No new TP (let it run).
                    # SL-first: check BE stop first.
                    effective_sl = be_stop if be_stop is not None else sl_cap
                    if is_long:
                        if lo <= effective_sl:
                            exit_reason = "be_stop"; exit_price = effective_sl; exit_ts = bt; break
                        # No TP limit for second half (let it run to eod/valid_until).
                    else:
                        if hi >= effective_sl:
                            exit_reason = "be_stop"; exit_price = effective_sl; exit_ts = bt; break

            # ─── PARTIAL TP1 + TRAIL (V8b) ────────────────────────────────
            elif exit_mode == "partial_tp_trail":
                if not partial_hit:
                    # SL-first conservative.
                    if is_long:
                        if lo <= sl_cap:
                            exit_reason = "stop"; exit_price = sl_cap; exit_ts = bt; break
                        if tp_cap is not None and hi >= tp_cap:
                            partial_hit         = True
                            partial_pnl_r       = (tp_cap - entry_price) / R
                            trail_stop_partial  = tp_cap - 1.0 * atr   # initial trail from TP1
                            best_favorable      = tp_cap
                    else:
                        if hi >= sl_cap:
                            exit_reason = "stop"; exit_price = sl_cap; exit_ts = bt; break
                        if tp_cap is not None and lo <= tp_cap:
                            partial_hit         = True
                            partial_pnl_r       = (entry_price - tp_cap) / R
                            trail_stop_partial  = tp_cap + 1.0 * atr
                            best_favorable      = tp_cap
                else:
                    # Second half with trailing stop.
                    if is_long:
                        if lo <= (trail_stop_partial or sl_cap):
                            exit_reason = "trail"; exit_price = trail_stop_partial; exit_ts = bt; break
                        if hi > best_favorable:
                            best_favorable = hi
                            new_trail = best_favorable - 1.0 * atr
                            if trail_stop_partial is None or new_trail > trail_stop_partial:
                                trail_stop_partial = new_trail
                    else:
                        if hi >= (trail_stop_partial or sl_cap):
                            exit_reason = "trail"; exit_price = trail_stop_partial; exit_ts = bt; break
                        if lo < best_favorable:
                            best_favorable = lo
                            new_trail = best_favorable + 1.0 * atr
                            if trail_stop_partial is None or new_trail < trail_stop_partial:
                                trail_stop_partial = new_trail

        # EOD close if no exit found in loop.
        if exit_reason is None:
            last = len(m1_times) - 1
            exit_reason = "eod"
            exit_price  = m1_closes[last]
            exit_ts     = m1_times[last]

        if exit_price is None:
            continue

        # Aggregate pnl_R.
        if exit_mode in ("partial_tp_be", "partial_tp_trail") and partial_hit:
            # Two halves: first half closed at TP1, second at exit_price.
            if is_long:
                second_pnl_r = (exit_price - entry_price) / R
            else:
                second_pnl_r = (entry_price - exit_price) / R
            pnl_gross_r = 0.5 * partial_pnl_r + 0.5 * second_pnl_r
        else:
            if is_long:
                pnl_gross_r = (exit_price - entry_price) / R
            else:
                pnl_gross_r = (entry_price - exit_price) / R

        pnl_net_r = pnl_gross_r - friction_r
        pnl_pct   = pnl_net_r * RISK_PCT

        trades.append(Trade(
            symbol=sig.symbol,
            strategy=sig.strategy,
            exit_mode="atr",
            side=sig.side,
            entry_ts=sig.setup_ts,
            entry=entry_price,
            stop=sl_cap,
            tp1=tp_cap,
            tp2=None,
            exit_ts=exit_ts,
            exit=exit_price,
            exit_reason=exit_reason,  # type: ignore[arg-type]
            R=R,
            pnl_R=pnl_net_r,
            pnl_pct=pnl_pct,
            bars_in_trade=j - entry_idx + 1 if exit_reason else 0,
        ))

    return trades


# ── Main sweep ────────────────────────────────────────────────────────────────

def run_phase_h(
    output_stem: str = "reports/external/orb_breakfade_phase_h",
) -> pl.DataFrame:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    phase_g_path = REPORTS_DIR / "orb_breakfade_phase_g.parquet"
    if not phase_g_path.exists():
        raise FileNotFoundError(f"Phase G parquet not found: {phase_g_path}")

    survivors_g = pl.read_parquet(phase_g_path)
    print(f"[PhaseH] Loaded {len(survivors_g)} Phase G survivors", flush=True)

    # Unique (sym, magic_time, duration) combos — only 3 distinct here.
    unique_combos = (
        survivors_g.select(["symbol", "magic_time", "duration"])
        .unique()
        .to_dicts()
    )

    total = len(survivors_g) * len(ATR_WINDOWS) * len(EXIT_VARIANTS)
    print(
        f"[PhaseH] {len(survivors_g)} survivors x {len(ATR_WINDOWS)} ATR windows "
        f"x {len(EXIT_VARIANTS)} exits = {total} backtests",
        flush=True,
    )

    adapter = ORBBreakFadeAdapter()

    # Cache M15 + M1 per symbol.
    m15_cache: dict[str, pl.DataFrame] = {}
    m1_cache:  dict[str, pl.DataFrame] = {}

    rows: list[dict] = []
    backtest_count = 0
    t0 = time.time()

    # Outer loop: each Phase G row defines (sym, magic, dur, tp_mult, sl_mult).
    for g_row in survivors_g.iter_rows(named=True):
        sym          = g_row["symbol"]
        magic_time   = g_row["magic_time"]
        duration     = g_row["duration"]
        tp_atr_mult  = g_row["tp_atr_mult"]
        sl_atr_mult  = g_row["sl_atr_mult"]
        friction_r   = friction_for(sym)

        # Load data once per symbol.
        if sym not in m15_cache:
            try:
                m15_cache[sym] = load_csv(sym, "M15")
            except FileNotFoundError:
                print(f"[PhaseH][SKIP] {sym} no M15", flush=True)
                m15_cache[sym] = None  # type: ignore[assignment]
        if sym not in m1_cache:
            m1_df = load_m1(sym)
            m1_cache[sym] = m1_df
            if m1_df is None:
                print(f"[PhaseH][SKIP] {sym} no M1", flush=True)

        df_m15 = m15_cache.get(sym)
        m1_df  = m1_cache.get(sym)
        if df_m15 is None or m1_df is None:
            backtest_count += len(ATR_WINDOWS) * len(EXIT_VARIANTS)
            continue

        m1_arrays = _precompute_m1_arrays(m1_df)

        for atr_w in ATR_WINDOWS:
            # Generate signals with this ATR window.
            try:
                base_sigs = adapter.generate_signals_for_combo(
                    df_m15, m1_df, sym, magic_time, duration, atr_window=atr_w
                )
            except Exception as e:
                print(
                    f"[PhaseH][ERR] {sym} {magic_time}/{duration} atr_w={atr_w}: {e}",
                    flush=True,
                )
                backtest_count += len(EXIT_VARIANTS)
                continue

            if len(base_sigs) < MIN_TRADES:
                backtest_count += len(EXIT_VARIANTS)
                continue

            for variant_name, variant_kwargs in EXIT_VARIANTS:
                backtest_count += 1
                if backtest_count % 100 == 0:
                    elapsed = time.time() - t0
                    pct = 100.0 * backtest_count / total
                    print(
                        f"[PhaseH] {backtest_count}/{total} ({pct:.0f}%) — {elapsed:.0f}s",
                        flush=True,
                    )

                # Attach TP/SL from this ATR window to each signal.
                sigs_with_rr: list[Signal] = []
                for s in base_sigs:
                    atr = s.indicator_anchors["atr_14"]
                    if s.side == "short":
                        stop = s.entry_price + sl_atr_mult * atr
                        tp1  = s.entry_price - tp_atr_mult * atr
                    else:
                        stop = s.entry_price - sl_atr_mult * atr
                        tp1  = s.entry_price + tp_atr_mult * atr
                    sigs_with_rr.append(_replace(s, stop=stop, tp1=tp1, tp2=None))

                exit_mode = variant_kwargs.get("exit_mode", "baseline")
                kw = {k: v for k, v in variant_kwargs.items() if k != "exit_mode"}

                try:
                    trades = _run_orb_with_alt_exit(
                        sigs_with_rr, m1_arrays,
                        exit_mode=exit_mode,
                        friction_r=friction_r,
                        **kw,
                    )
                except Exception as e:
                    print(
                        f"[PhaseH][ERR] {sym} {magic_time}/{duration} "
                        f"atr={atr_w} {variant_name}: {e}",
                        flush=True,
                    )
                    continue

                if len(trades) == 0:
                    continue

                m = evaluate(trades)
                if (
                    m["n_trades"]       >= MIN_TRADES
                    and m["win_rate"]   >= MIN_WR
                    and m["profit_factor"] >= MIN_PF
                ):
                    rows.append({
                        "symbol":        sym,
                        "magic_time":    magic_time,
                        "duration":      duration,
                        "tp_atr_mult":   tp_atr_mult,
                        "sl_atr_mult":   sl_atr_mult,
                        "atr_window":    atr_w,
                        "exit_variant":  variant_name,
                        "n_trades":      m["n_trades"],
                        "wr":            m["win_rate"],
                        "pf":            m["profit_factor"],
                        "expectancy_r":  m["expectancy_R"],
                        "max_dd_r":      m["max_dd_R"],
                        "calmar":        m.get("calmar", 0.0),
                        "total_r":       m["total_R"],
                        "sharpe":        m.get("sharpe", 0.0),
                    })

    elapsed = time.time() - t0
    print(
        f"\n[PhaseH] complete in {elapsed:.0f}s ({elapsed / 60:.1f} min)"
        f" — {len(rows)} survivors / {backtest_count} backtests",
        flush=True,
    )

    df = (
        pl.DataFrame(rows).sort("calmar", descending=True)
        if rows
        else pl.DataFrame()
    )

    _write_report(df, backtest_count, elapsed, output_stem, survivors_g)
    return df


# ── Report writer ─────────────────────────────────────────────────────────────

def _write_report(
    df: pl.DataFrame,
    backtest_count: int,
    elapsed: float,
    output_stem: str,
    survivors_g: pl.DataFrame,
) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out_md = Path(f"{output_stem}.md")

    if df.is_empty():
        out_md.write_text(
            f"# Phase H ORB break-fade\n- backtests: {backtest_count}\n- survivors: 0\n",
            encoding="utf-8",
        )
        return

    df.write_parquet(f"{output_stem}.parquet")

    lines = [
        "# ORB Break-Fade Phase H — ATR Windows + Alt Exits",
        "",
        f"- Backtests run:  {backtest_count}",
        f"- Survivors:      {len(df)}",
        f"- Runtime:        {elapsed:.0f}s ({elapsed / 60:.1f} min)",
        f"- Phase G seeds:  {len(survivors_g)}",
        f"- ATR windows:    {list(ATR_WINDOWS)}",
        f"- Exit variants:  {len(EXIT_VARIANTS)} ({[v for v, _ in EXIT_VARIANTS]})",
        "",
        "## Top 15 survivors (sorted by Calmar)",
        "",
        "| # | sym | magic | dur | tp | sl | atr_w | variant | n | wr | pf | exp_R | dd_R | calmar |",
        "|---|-----|-------|-----|----|----|-------|---------|---|-----|-----|-------|------|--------|",
    ]
    for rank, r in enumerate(df.head(15).iter_rows(named=True), 1):
        lines.append(
            f"| {rank} | {r['symbol']} | {r['magic_time']} | {r['duration']}m "
            f"| {r['tp_atr_mult']:.1f} | {r['sl_atr_mult']:.1f} | {r['atr_window']} "
            f"| {r['exit_variant']} | {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.3f} "
            f"| {r['expectancy_r']:.4f} | {r['max_dd_r']:.1f} | {r['calmar']:.3f} |"
        )

    lines += [
        "",
        "## Best variant per Phase-G base strategy (12 rows, best Calmar per seed)",
        "",
        "| sym | magic | dur | tp | sl | best_atr_w | best_variant | n | wr | pf | exp_R | dd_R | calmar |",
        "|-----|-------|-----|----|----|------------|--------------|---|-----|-----|-------|------|--------|",
    ]
    # Best variant per Phase-G seed = best calmar per (sym, magic, dur, tp, sl).
    seed_cols = ["symbol", "magic_time", "duration", "tp_atr_mult", "sl_atr_mult"]
    best_per_seed = (
        df
        .sort("calmar", descending=True)
        .unique(subset=seed_cols, keep="first")
        .sort("calmar", descending=True)
    )
    for r in best_per_seed.iter_rows(named=True):
        lines.append(
            f"| {r['symbol']} | {r['magic_time']} | {r['duration']}m "
            f"| {r['tp_atr_mult']:.1f} | {r['sl_atr_mult']:.1f} | {r['atr_window']} "
            f"| {r['exit_variant']} | {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.3f} "
            f"| {r['expectancy_r']:.4f} | {r['max_dd_r']:.1f} | {r['calmar']:.3f} |"
        )

    # ATR window breakdown.
    lines += ["", "## Survivors by ATR window", ""]
    for atr_w in ATR_WINDOWS:
        n = len(df.filter(pl.col("atr_window") == atr_w))
        lines.append(f"- ATR {atr_w}: {n} survivors")

    # Exit variant breakdown.
    lines += ["", "## Survivors by exit variant", ""]
    for vname, _ in EXIT_VARIANTS:
        n = len(df.filter(pl.col("exit_variant") == vname))
        if n > 0:
            lines.append(f"- {vname}: {n}")

    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[PhaseH] Report written to {out_md}", flush=True)


if __name__ == "__main__":
    import sys
    # Sanity test: single combo GBPAUD 15:00 120m atr_w=14 V4_trail_1.5
    # Compare to V1_baseline to confirm divergence.
    print("[PhaseH] Sanity test: GBPAUD 15:00 120m atr_w=14 V1_baseline vs V4_trail_1.5", flush=True)
    adapter = ORBBreakFadeAdapter()
    df_m15  = load_csv("GBPAUD", "M15")
    m1_df   = load_m1("GBPAUD")
    if m1_df is not None:
        m1_arrays = _precompute_m1_arrays(m1_df)
        base_sigs = adapter.generate_signals_for_combo(df_m15, m1_df, "GBPAUD", "15:00", 120, atr_window=14)
        sigs_rr = []
        for s in base_sigs:
            atr = s.indicator_anchors["atr_14"]
            if s.side == "short":
                stop = s.entry_price + 1.5 * atr; tp1 = s.entry_price - 1.5 * atr
            else:
                stop = s.entry_price - 1.5 * atr; tp1 = s.entry_price + 1.5 * atr
            sigs_rr.append(_replace(s, stop=stop, tp1=tp1, tp2=None))
        fr = friction_for("GBPAUD")
        t_base  = _run_orb_with_alt_exit(sigs_rr, m1_arrays, exit_mode="baseline",      friction_r=fr)
        t_trail = _run_orb_with_alt_exit(sigs_rr, m1_arrays, exit_mode="trailing_atr",  friction_r=fr, trailing_atr_mult=1.5)
        mb = evaluate(t_base)
        mt = evaluate(t_trail)
        print(f"  V1 baseline:    n={mb['n_trades']} WR={mb['win_rate']:.3f} PF={mb['profit_factor']:.3f} calmar={mb['calmar']:.3f}", flush=True)
        print(f"  V4 trail 1.5x:  n={mt['n_trades']} WR={mt['win_rate']:.3f} PF={mt['profit_factor']:.3f} calmar={mt['calmar']:.3f}", flush=True)
        diverged = (mb['win_rate'] != mt['win_rate'] or mb['total_R'] != mt['total_R'])
        print(f"  Results diverge: {diverged}", flush=True)
    else:
        print("[PhaseH][WARN] No M1 data for GBPAUD — skipping sanity test", flush=True)

    print("\n[PhaseH] Starting full sweep...", flush=True)
    df = run_phase_h()
    print(f"\n[PhaseH] Done. Total survivors: {len(df)}", flush=True)
