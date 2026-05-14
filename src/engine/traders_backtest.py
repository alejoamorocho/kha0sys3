"""Traders replication — backtest con gestion exacta por trader.

Walking M1 para STOP-fill + manejo de salida. La logica de exit es ESPECIFICA
por trader (Minervini / Zanger / Qulla / Ryan) segun los PDFs.

Cada trader define ExitRules:
    initial_sl_pct        SL fijo % desde entry (None si usa ATR)
    initial_sl_atr_mult   SL en multiplos de ATR
    partials              Lista de (trigger_type, trigger_value, sell_frac)
                          trigger_type: "r_multiple" | "pct_from_entry" | "days_held"
    trail_sma             Trailing stop por SMA (10/20/50). Se activa post-TP1.
    time_stop_days        Si en X dias no toca TP1, cierra remanente.
    max_hold_days         Timeout absoluto.

R-multiple final = pnl / initial_risk - friction_R.
Friction = Vantage real (friction_real.friction_r + 0.2R slippage).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timezone as _tz

import numpy as np
import polars as pl

from src.engine.friction_real import friction_r as real_friction_r, load_median_atr


def _to_us_utc(dt) -> int:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=_tz.utc)
    return int(dt.timestamp() * 1_000_000)


@dataclass(frozen=True)
class ExitRules:
    trader: str
    initial_sl_pct: float | None
    initial_sl_atr_mult: float | None
    partials: tuple  # ((trigger_type, trigger_value, sell_frac), ...)
    trail_sma: int | None   # 10, 20, 50, or None
    time_stop_days: int | None
    max_hold_days: float    # admite fraccionales (ej 0.17 = 4h)
    wait_bars_after_signal: int  # cuantas barras de signal-TF esperar fill
    use_base_low_as_sl: bool = False  # Qulla ORB PDF: SL = Range Low del signal
    trail_uses_d1_close: bool = False  # Ryan PDF: exit si D1 close < trail SMA


TRADER_RULES = {
    "Minervini": ExitRules(
        trader="Minervini",
        initial_sl_pct=0.075,
        initial_sl_atr_mult=None,
        partials=(("r_multiple", 2.0, 0.30), ("r_multiple", 4.0, 0.30)),
        trail_sma=10,
        time_stop_days=None,
        max_hold_days=60,
        wait_bars_after_signal=2,
    ),
    "Zanger_FLAG": ExitRules(
        trader="Zanger",
        initial_sl_pct=0.08,
        initial_sl_atr_mult=None,
        partials=(("pct_from_entry", 0.15, 0.50),),
        trail_sma=20,
        time_stop_days=2,  # PDF: 20min-3h intraday; en D1 aprox 1-2 dias
        max_hold_days=30,
        wait_bars_after_signal=1,
    ),
    "Zanger_CUP_HANDLE": ExitRules(
        trader="Zanger",
        initial_sl_pct=0.08,
        initial_sl_atr_mult=None,
        partials=(("pct_from_entry", 0.20, 0.50),),
        trail_sma=20,
        time_stop_days=3,
        max_hold_days=40,
        wait_bars_after_signal=1,
    ),
    "Qulla_HTF": ExitRules(
        trader="Qulla",
        initial_sl_pct=None,
        initial_sl_atr_mult=1.0,
        partials=(("days_held", 3, 0.30), ("days_held", 5, 0.20)),
        trail_sma=50,
        time_stop_days=None,
        max_hold_days=40,
        wait_bars_after_signal=1,
    ),
    "Qulla_EP": ExitRules(
        trader="Qulla",
        initial_sl_pct=None,
        initial_sl_atr_mult=1.0,
        partials=(("days_held", 3, 0.30), ("days_held", 5, 0.20)),
        trail_sma=50,
        time_stop_days=None,
        max_hold_days=40,
        wait_bars_after_signal=1,
    ),
    "Qulla_ORB": ExitRules(
        trader="Qulla",
        initial_sl_pct=None,
        initial_sl_atr_mult=1.0,
        partials=(("r_multiple", 2.0, 0.50),),
        trail_sma=None,
        time_stop_days=None,
        max_hold_days=1,  # intraday; el max_hold se interpreta en horas si signal=H1
        wait_bars_after_signal=2,
    ),
    "Ryan_ANTS": ExitRules(
        trader="Ryan",
        initial_sl_pct=0.07,
        initial_sl_atr_mult=None,
        partials=(("pct_from_entry", 0.22, 0.15), ("pct_from_entry", 0.40, 0.15)),
        trail_sma=50,
        time_stop_days=None,
        max_hold_days=80,
        wait_bars_after_signal=2,
    ),
}


def _rules_for(trader: str, setup_name: str) -> ExitRules:
    key = f"{trader}_{setup_name}"
    if key in TRADER_RULES:
        return TRADER_RULES[key]
    return TRADER_RULES[trader]


# ── Daily SMA lookup aligned to M1 ────────────────────────────────────────


def build_sma_lookup(daily: pl.DataFrame, m1_times_us: np.ndarray, sma_col: str) -> np.ndarray:
    """Para cada timestamp M1, retorna SMA del cierre del dia ANTERIOR (causal).
    Usa forward fill desde el cierre D1.
    """
    if sma_col not in daily.columns:
        return np.full(len(m1_times_us), np.nan)
    d = daily.sort("time").select(["time", sma_col]).drop_nulls()
    if len(d) == 0:
        return np.full(len(m1_times_us), np.nan)
    # Daily "time" = inicio del dia. La SMA del cierre de ese dia se conoce
    # al cierre. Para uso causal en el siguiente dia, desplazamos +1 dia.
    d_times = (d["time"].cast(pl.Int64).to_numpy() + 86_400_000_000)  # +1 dia us
    d_vals = d[sma_col].to_numpy()
    idx = np.searchsorted(d_times, m1_times_us, side="right") - 1
    idx = np.clip(idx, -1, len(d_vals) - 1)
    out = np.where(idx < 0, np.nan, d_vals[np.clip(idx, 0, len(d_vals) - 1)])
    return out


# ── Core walker ───────────────────────────────────────────────────────────


def backtest_orb_vectorized(
    signals: pl.DataFrame,
    m1_arr: np.ndarray,
    m1_times_us: np.ndarray,
    rules: ExitRules,
    symbol: str,
    signal_tf_min: int,
) -> list[dict]:
    """Fast path numpy-only para ORB intradia (sin trail, sin days_held, LONG).

    Asume: rules.trail_sma=None, partials de tipo r_multiple o pct_from_entry,
    direction LONG.
    """
    if len(signals) == 0:
        return []
    median_atr = load_median_atr(symbol) or 0.0
    sl_mult_for_friction = rules.initial_sl_atr_mult or 1.0
    friction = real_friction_r(symbol, sl_mult_for_friction, median_atr) + 0.2

    # Dedup 1/dia
    sigs = (signals.with_columns(pl.col("time").dt.date().alias("_d"))
            .sort("time").unique(subset=["_d"], keep="first").drop("_d"))
    sig_times_us = sigs["time"].cast(pl.Int64).to_numpy()
    sig_stop = sigs["stop_price"].to_numpy().astype(np.float64)
    sig_atr = sigs["atr_14"].to_numpy().astype(np.float64)

    wait_us = rules.wait_bars_after_signal * signal_tf_min * 60 * 1_000_000
    day_us = 86_400 * 1_000_000
    minute_us = 60 * 1_000_000
    max_us_offset = int(rules.max_hold_days * day_us)

    high_arr = m1_arr[:, 1]
    low_arr = m1_arr[:, 2]
    close_arr = m1_arr[:, 3]
    N = len(m1_arr)

    results = []
    for k in range(len(sig_times_us)):
        atr = sig_atr[k]
        stop_price = sig_stop[k]
        if not np.isfinite(atr) or atr <= 0 or not np.isfinite(stop_price) or stop_price <= 0:
            continue
        sig_us = int(sig_times_us[k])
        bar_end_us = sig_us + signal_tf_min * 60 * 1_000_000
        wait_start = int(np.searchsorted(m1_times_us, bar_end_us, side="left"))
        wait_end = int(np.searchsorted(m1_times_us, bar_end_us + wait_us, side="right"))
        if wait_start >= N or wait_end <= wait_start:
            continue
        # Fill = first idx in [wait_start, wait_end) where high >= stop_price
        wait_high = high_arr[wait_start:wait_end]
        hit = wait_high >= stop_price
        if not hit.any():
            continue
        fill_off = int(np.argmax(hit))
        fill_idx = wait_start + fill_off

        entry = float(stop_price)
        entry_us = int(m1_times_us[fill_idx])
        if rules.initial_sl_pct is not None:
            risk = entry * rules.initial_sl_pct
        else:
            risk = (rules.initial_sl_atr_mult or 1.0) * atr
        if risk <= 0:
            continue
        sl_level = entry - risk

        scan_start = fill_idx + 1
        scan_end = int(np.searchsorted(m1_times_us, entry_us + max_us_offset, side="right"))
        scan_end = min(scan_end, N)
        if scan_end <= scan_start:
            continue

        seg_hi = high_arr[scan_start:scan_end]
        seg_lo = low_arr[scan_start:scan_end]
        seg_cl = close_arr[scan_start:scan_end]
        L = len(seg_hi)

        # Compute first SL hit index
        sl_mask = seg_lo <= sl_level
        sl_idx = int(np.argmax(sl_mask)) if sl_mask.any() else -1

        # Build list of partial events: (idx_first_hit_or_-1, sell_frac, trigger_price)
        events = []
        for trigger_type, trigger_val, sell_frac in rules.partials:
            if trigger_type == "r_multiple":
                tp = entry + trigger_val * risk
            elif trigger_type == "pct_from_entry":
                tp = entry * (1.0 + trigger_val)
            else:
                # days_held no soportado en fast path
                continue
            mask = seg_hi >= tp
            idx = int(np.argmax(mask)) if mask.any() else -1
            if idx >= 0:
                events.append((idx, float(sell_frac), float(tp)))
        # Order events by idx
        events.sort(key=lambda x: x[0])

        remaining = 1.0
        pnl = 0.0
        exit_reason = "MAX_HOLD"
        exit_idx = L - 1

        # Process partial events in time order, stop if SL hits first
        for ev_idx, sell_frac, tp_price in events:
            if sl_idx >= 0 and sl_idx <= ev_idx:
                # SL hits before this partial
                break
            pnl += (tp_price - entry) * sell_frac
            remaining -= sell_frac
            if remaining <= 1e-9:
                exit_reason = "PARTIAL_FULL"
                exit_idx = ev_idx
                remaining = 0.0
                break

        if remaining > 0:
            if sl_idx >= 0:
                # Resto cerrado en SL
                sl_price = sl_level
                pnl += (sl_price - entry) * remaining
                exit_reason = "SL"
                exit_idx = sl_idx
                remaining = 0.0
            else:
                # MAX_HOLD: cierra a close del ultimo minuto
                last_close = float(seg_cl[-1])
                pnl += (last_close - entry) * remaining
                exit_reason = "MAX_HOLD"
                exit_idx = L - 1
                remaining = 0.0

        r = pnl / risk - friction
        exit_us = int(m1_times_us[scan_start + exit_idx]) if scan_start + exit_idx < N else entry_us
        results.append({
            "time": sigs[k, "time"],
            "direction": "LONG",
            "trader": "Qulla",
            "setup_name": "ORB",
            "entry": entry,
            "r_multiple": float(r),
            "exit_reason": exit_reason,
            "hold_minutes": int((exit_us - entry_us) // minute_us),
        })
    return results


def backtest_signals(
    signals: pl.DataFrame,
    m1_arr: np.ndarray,
    m1_times_us: np.ndarray,
    daily: pl.DataFrame,
    rules: ExitRules,
    symbol: str,
    signal_tf_min: int,
    invert: bool = False,
) -> list[dict]:
    """Walk M1: STOP fill (wait window) -> manage exit segun ExitRules.

    Args:
        signals: filas con time, close, atr_14, stop_price, sma10/20/50, base_low...
        m1_arr: Nx4 [open, high, low, close]
        m1_times_us: Nx1 timestamps en microseconds UTC
        daily: D1 OHLC + sma10/20/50 (para trailing causal)
        rules: ExitRules del trader/setup
        signal_tf_min: minutos del TF de la senal (1440 D1, 60 H1)
        invert: si True, LONG->SHORT (testea fade)

    Returns: lista de dicts con r_multiple, hold_minutes, exit_reason, etc.
    """
    if len(signals) == 0:
        return []

    median_atr = load_median_atr(symbol) or 0.0
    sl_mult_for_friction = rules.initial_sl_atr_mult or 1.0
    friction = real_friction_r(symbol, sl_mult_for_friction, median_atr) + 0.2

    sma_col = f"sma{rules.trail_sma}" if rules.trail_sma else None
    sma_lookup = build_sma_lookup(daily, m1_times_us, sma_col) if sma_col else None

    # Dedup 1/dia/setup
    signals = (
        signals.with_columns(pl.col("time").dt.date().alias("_d"))
        .sort("time")
        .unique(subset=["_d"], keep="first")
        .drop("_d")
    )

    wait_us = rules.wait_bars_after_signal * signal_tf_min * 60 * 1_000_000
    minute_us = 60 * 1_000_000
    day_us = 86_400 * 1_000_000

    results: list[dict] = []
    for s in signals.iter_rows(named=True):
        atr = s.get("atr_14") or 0.0
        if atr <= 0:
            continue
        stop_price = s.get("stop_price")
        if stop_price is None or stop_price <= 0:
            continue

        direction = s["direction"]
        if invert:
            direction = "SHORT" if direction == "LONG" else "LONG"

        sig_us = _to_us_utc(s["time"])
        bar_end_us = sig_us + signal_tf_min * 60 * 1_000_000

        # Find fill within wait window
        wait_start = int(np.searchsorted(m1_times_us, bar_end_us, side="left"))
        wait_end = int(np.searchsorted(m1_times_us, bar_end_us + wait_us, side="right"))
        if wait_start >= len(m1_arr) or wait_end <= wait_start:
            continue

        fill_idx = None
        for i in range(wait_start, min(wait_end, len(m1_arr))):
            hi, lo = m1_arr[i, 1], m1_arr[i, 2]
            if direction == "LONG":
                if hi >= stop_price:
                    fill_idx = i
                    break
            else:
                # SHORT: STOP de venta = ruptura del base_low. Pero como invertimos
                # la direccion, el "stop_price" del setup LONG es resistencia;
                # para SHORT usamos base_low como trigger.
                bl = s.get("base_low")
                trigger = bl if (bl is not None and bl > 0) else stop_price
                if lo <= trigger:
                    fill_idx = i
                    stop_price = trigger
                    break
        if fill_idx is None:
            continue

        entry = float(stop_price)
        entry_us = m1_times_us[fill_idx]

        # Initial SL — prioridad: base_low (PDF Qulla ORB) > pct > ATR
        if rules.use_base_low_as_sl:
            bl = s.get("base_low")
            if bl is None or bl <= 0 or bl >= entry:
                continue
            sl_level = float(bl)
            risk_price = entry - sl_level
        elif rules.initial_sl_pct is not None:
            risk_price = entry * rules.initial_sl_pct
            sl_level = entry - risk_price if direction == "LONG" else entry + risk_price
        else:
            risk_price = (rules.initial_sl_atr_mult or 1.0) * atr
            sl_level = entry - risk_price if direction == "LONG" else entry + risk_price
        if risk_price <= 0:
            continue

        # Walk from fill_idx+1 forward
        scan_start = fill_idx + 1
        max_us = entry_us + rules.max_hold_days * day_us
        scan_end = int(np.searchsorted(m1_times_us, max_us, side="right"))
        scan_end = min(scan_end, len(m1_arr))
        if scan_end <= scan_start:
            continue

        # Position state
        remaining = 1.0
        weighted_pnl = 0.0
        partial_taken = [False] * len(rules.partials)
        tp1_hit = False  # cualquier partial activado activa trailing
        time_stopped = False
        exit_reason = "MAX_HOLD"
        last_close_price = entry

        # Track day boundaries for "days_held" triggers
        entry_day = int(entry_us // day_us)
        # Compute current daily SMA from lookup
        for i in range(scan_start, scan_end):
            hi, lo, cl = m1_arr[i, 1], m1_arr[i, 2], m1_arr[i, 3]
            last_close_price = float(cl)
            cur_us = m1_times_us[i]
            days_held = int(cur_us // day_us) - entry_day

            # Check SL first (conservative)
            if direction == "LONG":
                if lo <= sl_level:
                    pnl = (sl_level - entry) * remaining
                    weighted_pnl += pnl
                    exit_reason = "SL" if not tp1_hit else "TRAIL"
                    remaining = 0.0
                    break
            else:
                if hi >= sl_level:
                    pnl = (entry - sl_level) * remaining
                    weighted_pnl += pnl
                    exit_reason = "SL" if not tp1_hit else "TRAIL"
                    remaining = 0.0
                    break

            # Check partials
            for pidx, (trigger_type, trigger_val, sell_frac) in enumerate(rules.partials):
                if partial_taken[pidx]:
                    continue
                triggered = False
                trigger_price = entry
                if trigger_type == "r_multiple":
                    target = entry + trigger_val * risk_price if direction == "LONG" else entry - trigger_val * risk_price
                    if direction == "LONG" and hi >= target:
                        triggered = True; trigger_price = target
                    elif direction == "SHORT" and lo <= target:
                        triggered = True; trigger_price = target
                elif trigger_type == "pct_from_entry":
                    target = entry * (1.0 + trigger_val) if direction == "LONG" else entry * (1.0 - trigger_val)
                    if direction == "LONG" and hi >= target:
                        triggered = True; trigger_price = target
                    elif direction == "SHORT" and lo <= target:
                        triggered = True; trigger_price = target
                elif trigger_type == "days_held":
                    if days_held >= int(trigger_val):
                        triggered = True; trigger_price = float(cl)
                if triggered:
                    pnl = ((trigger_price - entry) if direction == "LONG" else (entry - trigger_price)) * sell_frac
                    weighted_pnl += pnl
                    remaining -= sell_frac
                    partial_taken[pidx] = True
                    tp1_hit = True

            # Time stop (cierra TODO si despues de X dias no toco TP1)
            if rules.time_stop_days is not None and not tp1_hit and days_held >= rules.time_stop_days:
                pnl = ((float(cl) - entry) if direction == "LONG" else (entry - float(cl))) * remaining
                weighted_pnl += pnl
                exit_reason = "TIME_STOP"
                remaining = 0.0
                time_stopped = True
                break

            # Trailing stop activado solo despues de TP1
            if tp1_hit and sma_lookup is not None and remaining > 0:
                trail = sma_lookup[i] if i < len(sma_lookup) else np.nan
                if not np.isnan(trail):
                    if direction == "LONG":
                        if trail > sl_level:
                            sl_level = float(trail)
                    else:
                        if trail < sl_level:
                            sl_level = float(trail)

            if remaining <= 1e-9:
                exit_reason = "PARTIAL_FULL"
                break

        # Si no salio por SL/TIME/PARTIAL_FULL -> max hold: cierra a last_close_price
        if remaining > 0:
            pnl = ((last_close_price - entry) if direction == "LONG" else (entry - last_close_price)) * remaining
            weighted_pnl += pnl

        # R-multiple = pnl_total / risk_price (1 unidad de riesgo)
        r = weighted_pnl / risk_price - friction
        results.append({
            "time": s["time"],
            "direction": direction,
            "trader": s["trader"],
            "setup_name": s["setup_name"],
            "entry": entry,
            "r_multiple": float(r),
            "exit_reason": exit_reason,
            "hold_minutes": int((m1_times_us[min(i, len(m1_times_us)-1)] - entry_us) // minute_us),
        })
    return results
