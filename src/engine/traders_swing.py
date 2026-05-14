"""Traders SWING — detectores D1 FX-calibrated + M1 intraday breakout scanner.

Diferencia vs traders_setups.py:
  - Thresholds calibrados a magnitudes FX/commodities (5-15%) en vez de stocks
    (20-100%).
  - Cada detector D1 produce un SETUP TABLE: filas con
    (date_signal, pivot_high, base_low, atr_d1, valid_through_date).
  - Un escaner aparte busca el primer cierre M1 > pivot_high dentro de la
    ventana valid; emite la senal en ese minuto.
  - Asi la entrada NO se queda esperando al cierre D1: cualquier ruptura
    intradia dispara, como dicen los PDFs ("se activa en el instante preciso
    en que el precio cruza la linea de tendencia").
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np
import polars as pl

from src.engine.traders_setups import (
    resample_to_daily, add_indicators, _trend_template,
)


def _empty_setup() -> pl.DataFrame:
    return pl.DataFrame(schema={
        "date_signal": pl.Date,
        "pivot_high": pl.Float64,
        "base_low": pl.Float64,
        "atr_d1": pl.Float64,
        "valid_days": pl.Int64,
        "sma10_d": pl.Float64,
        "sma20_d": pl.Float64,
        "sma50_d": pl.Float64,
    })


# ── Minervini VCP — FX calibrated ────────────────────────────────────────


def setup_minervini_vcp_fx(daily: pl.DataFrame, valid_days: int = 5) -> pl.DataFrame:
    """VCP con thresholds FX:
      - Stage 2 (trend template) requerido (mas flexible: precio>SMA50 y SMA50>SMA200, sin SMA150 strict)
      - Contracciones: c1 en [0.05, 0.25], c2<c1, c3<c2, c3<=0.05
      - Pivot = max(high) ultimas 5 D1 barras
    """
    if len(daily) < 200:
        return _empty_setup()
    df = add_indicators(daily)
    # Trend template "lite": precio > SMA50 > SMA200 (FX rara vez hace Stage 2 stock-style)
    stage2_lite = (pl.col("close") > pl.col("sma50")) & (pl.col("sma50") > pl.col("sma200"))
    c1 = (pl.col("high").rolling_max(30) - pl.col("low").rolling_min(30)) / pl.col("high").rolling_max(30)
    c2 = (pl.col("high").rolling_max(15) - pl.col("low").rolling_min(15)) / pl.col("high").rolling_max(15)
    c3 = (pl.col("high").rolling_max(5) - pl.col("low").rolling_min(5)) / pl.col("high").rolling_max(5)
    vcp_geom = (
        (c1 >= 0.04) & (c1 <= 0.25)
        & (c2 < c1) & (c2 >= 0.02)
        & (c3 < c2) & (c3 <= 0.06)
    )
    pivot = pl.col("high").rolling_max(5)
    setup_valid = stage2_lite & vcp_geom & pivot.is_not_null()
    setup = df.with_columns([
        setup_valid.alias("_v"),
        pivot.alias("_p"),
        pl.col("low").rolling_min(5).alias("_bl"),
    ]).filter(pl.col("_v"))
    if len(setup) == 0:
        return _empty_setup()
    return setup.select([
        pl.col("time").dt.date().alias("date_signal"),
        pl.col("_p").alias("pivot_high"),
        pl.col("_bl").alias("base_low"),
        pl.col("atr_14").alias("atr_d1"),
        pl.lit(valid_days, dtype=pl.Int64).alias("valid_days"),
        pl.col("sma10").alias("sma10_d"),
        pl.col("sma20").alias("sma20_d"),
        pl.col("sma50").alias("sma50_d"),
    ])


# ── Zanger FLAG — FX calibrated ──────────────────────────────────────────


def setup_zanger_flag_fx(daily: pl.DataFrame, valid_days: int = 5) -> pl.DataFrame:
    """Flag con thresholds FX:
      - Flagpole +5-20% en 15 dias
      - Flag range <= 40% del avance, 5-10 dias
      - Pivot = max(high) flag
    """
    if len(daily) < 100:
        return _empty_setup()
    df = add_indicators(daily)
    pole_lo = pl.col("low").shift(12).rolling_min(15)
    pole_hi = pl.col("high").shift(5).rolling_max(10)
    pole_gain = (pole_hi - pole_lo) / pole_lo
    flag_hi = pl.col("high").shift(1).rolling_max(7)
    flag_lo = pl.col("low").shift(1).rolling_min(7)
    flag_rng = (flag_hi - flag_lo) / flag_lo
    valid = (
        (pole_gain >= 0.05) & (pole_gain <= 0.30)
        & (flag_rng <= 0.50 * pole_gain)
        & (pl.col("close") <= flag_hi * 1.02)  # aun cerca del pivot
        & flag_hi.is_not_null()
    )
    setup = df.with_columns([
        valid.alias("_v"), flag_hi.alias("_p"), flag_lo.alias("_bl"),
    ]).filter(pl.col("_v"))
    if len(setup) == 0:
        return _empty_setup()
    return setup.select([
        pl.col("time").dt.date().alias("date_signal"),
        pl.col("_p").alias("pivot_high"),
        pl.col("_bl").alias("base_low"),
        pl.col("atr_14").alias("atr_d1"),
        pl.lit(valid_days, dtype=pl.Int64).alias("valid_days"),
        pl.col("sma10").alias("sma10_d"),
        pl.col("sma20").alias("sma20_d"),
        pl.col("sma50").alias("sma50_d"),
    ])


# ── Zanger CUP&HANDLE — FX calibrated ────────────────────────────────────


def setup_zanger_cup_handle_fx(daily: pl.DataFrame, valid_days: int = 5) -> pl.DataFrame:
    """Cup&Handle con thresholds FX:
      - Cup depth 5-20% (vs 15-40% stocks)
      - Handle range <= 12%, 5-15 dias
    """
    if len(daily) < 100:
        return _empty_setup()
    df = add_indicators(daily)
    cup_left = pl.col("high").shift(50).rolling_max(10)
    cup_low = pl.col("low").shift(15).rolling_min(40)
    cup_right = pl.col("high").shift(8).rolling_max(8)
    handle_hi = pl.col("high").shift(1).rolling_max(10)
    handle_lo = pl.col("low").shift(1).rolling_min(10)

    cup_depth = (cup_left - cup_low) / cup_left
    cup_symm = (cup_right - cup_low) / cup_left
    handle_rng = (handle_hi - handle_lo) / handle_lo
    valid = (
        (cup_depth >= 0.05) & (cup_depth <= 0.25)
        & (cup_symm >= 0.70) & (cup_symm <= 1.10)
        & (handle_rng <= 0.12)
        & (pl.col("close") <= handle_hi * 1.02)
        & handle_hi.is_not_null()
    )
    setup = df.with_columns([
        valid.alias("_v"), handle_hi.alias("_p"), handle_lo.alias("_bl"),
    ]).filter(pl.col("_v"))
    if len(setup) == 0:
        return _empty_setup()
    return setup.select([
        pl.col("time").dt.date().alias("date_signal"),
        pl.col("_p").alias("pivot_high"),
        pl.col("_bl").alias("base_low"),
        pl.col("atr_14").alias("atr_d1"),
        pl.lit(valid_days, dtype=pl.Int64).alias("valid_days"),
        pl.col("sma10").alias("sma10_d"),
        pl.col("sma20").alias("sma20_d"),
        pl.col("sma50").alias("sma50_d"),
    ])


# ── Qulla HTF — FX calibrated ────────────────────────────────────────────


def setup_qulla_htf_fx(daily: pl.DataFrame, valid_days: int = 5) -> pl.DataFrame:
    """High Tight Flag con thresholds FX:
      - Pole +8-30% en 20 dias (vs +25-100% stocks)
      - Flag pullback <= 30% del pole
      - Precio dentro de +-4% de SMA10
    """
    if len(daily) < 60:
        return _empty_setup()
    df = add_indicators(daily)
    pole_lo = pl.col("low").shift(20).rolling_min(20)
    pole_hi = pl.col("high").shift(5).rolling_max(20)
    pole_gain = (pole_hi - pole_lo) / pole_lo
    flag_hi = pl.col("high").shift(1).rolling_max(8)
    flag_lo = pl.col("low").shift(1).rolling_min(8)
    flag_pull = (flag_hi - flag_lo) / flag_hi
    dist10 = (pl.col("close") - pl.col("sma10")).abs() / pl.col("sma10")
    valid = (
        (pole_gain >= 0.08) & (pole_gain <= 0.40)
        & (flag_pull <= 0.30)
        & (dist10 <= 0.04)
        & flag_hi.is_not_null()
    )
    setup = df.with_columns([
        valid.alias("_v"), flag_hi.alias("_p"), flag_lo.alias("_bl"),
    ]).filter(pl.col("_v"))
    if len(setup) == 0:
        return _empty_setup()
    return setup.select([
        pl.col("time").dt.date().alias("date_signal"),
        pl.col("_p").alias("pivot_high"),
        pl.col("_bl").alias("base_low"),
        pl.col("atr_14").alias("atr_d1"),
        pl.lit(valid_days, dtype=pl.Int64).alias("valid_days"),
        pl.col("sma10").alias("sma10_d"),
        pl.col("sma20").alias("sma20_d"),
        pl.col("sma50").alias("sma50_d"),
    ])


# ── Qulla EP — FX calibrated ─────────────────────────────────────────────


def setup_qulla_ep_fx(daily: pl.DataFrame, valid_days: int = 3) -> pl.DataFrame:
    """Episodic Pivot con thresholds FX:
      - Gap up >= 1% (vs +4-7.5% stocks)
      - Bar range >= 1.5x ATR_20
      - Tick volume day >= 1.3x SMA20 (proxy)
    """
    if len(daily) < 30:
        return _empty_setup()
    df = add_indicators(daily)
    gap = (pl.col("open") - pl.col("close").shift(1)) / pl.col("close").shift(1)
    valid = (
        (gap >= 0.010)
        & (pl.col("bar_range") >= 1.5 * pl.col("atr_20"))
        & (pl.col("volume") >= 1.3 * pl.col("vol_sma20"))
        & (pl.col("close") > pl.col("open"))
    )
    setup = df.with_columns([
        valid.alias("_v"),
        pl.col("high").alias("_p"),
        pl.col("low").alias("_bl"),
    ]).filter(pl.col("_v"))
    if len(setup) == 0:
        return _empty_setup()
    return setup.select([
        pl.col("time").dt.date().alias("date_signal"),
        pl.col("_p").alias("pivot_high"),
        pl.col("_bl").alias("base_low"),
        pl.col("atr_14").alias("atr_d1"),
        pl.lit(valid_days, dtype=pl.Int64).alias("valid_days"),
        pl.col("sma10").alias("sma10_d"),
        pl.col("sma20").alias("sma20_d"),
        pl.col("sma50").alias("sma50_d"),
    ])


# ── Ryan ANTS — FX calibrated ────────────────────────────────────────────


def setup_ryan_ants_fx(daily: pl.DataFrame, valid_days: int = 5) -> pl.DataFrame:
    """Ants con thresholds FX:
      - Ventana 15 dias: +5-12% precio, +20% vol, >=11/15 dias alcistas
      - Base secundaria T-5..T: rango <= 5%
      - Pivot = max(high) base
    """
    if len(daily) < 80:
        return _empty_setup()
    df = add_indicators(daily)
    ret_15 = (pl.col("close").shift(5) / pl.col("close").shift(20)) - 1.0
    vol_15 = pl.col("volume").shift(5).rolling_mean(15)
    vol_prev = pl.col("volume").shift(20).rolling_mean(30)
    up_days = ((pl.col("close") > pl.col("open")).cast(pl.Int64)
               .shift(5).rolling_sum(15))
    base_hi = pl.col("high").shift(1).rolling_max(5)
    base_lo = pl.col("low").shift(1).rolling_min(5)
    base_tight = ((base_hi - base_lo) / base_hi) <= 0.05
    valid = (
        (ret_15 >= 0.05) & (ret_15 <= 0.20)
        & (vol_15 >= 1.20 * vol_prev)
        & (up_days >= 11)
        & base_tight
        & base_hi.is_not_null()
    )
    setup = df.with_columns([
        valid.alias("_v"), base_hi.alias("_p"), base_lo.alias("_bl"),
    ]).filter(pl.col("_v"))
    if len(setup) == 0:
        return _empty_setup()
    return setup.select([
        pl.col("time").dt.date().alias("date_signal"),
        pl.col("_p").alias("pivot_high"),
        pl.col("_bl").alias("base_low"),
        pl.col("atr_14").alias("atr_d1"),
        pl.lit(valid_days, dtype=pl.Int64).alias("valid_days"),
        pl.col("sma10").alias("sma10_d"),
        pl.col("sma20").alias("sma20_d"),
        pl.col("sma50").alias("sma50_d"),
    ])


SWING_DETECTORS = {
    "Minervini_VCP":   setup_minervini_vcp_fx,
    "Zanger_FLAG":     setup_zanger_flag_fx,
    "Zanger_CUP":      setup_zanger_cup_handle_fx,
    "Qulla_HTF":       setup_qulla_htf_fx,
    "Qulla_EP":        setup_qulla_ep_fx,
    "Ryan_ANTS":       setup_ryan_ants_fx,
}


# ── M1 intraday breakout scanner ─────────────────────────────────────────


def find_intraday_breakouts(
    setup_table: pl.DataFrame,
    m1_arr: np.ndarray,
    m1_times_us: np.ndarray,
    m1_close: np.ndarray,
    trader: str,
    setup_name: str,
) -> pl.DataFrame:
    """Para cada fila del setup_table (cada D1 con setup valido), busca el primer
    minuto en [date_signal+1 00:00, date_signal+valid_days 23:59) donde
    M1.close > pivot_high. Emite signal en ese minuto.

    Returns: DataFrame con columnas compatibles con backtest_signals/orb_vectorized.
    """
    if len(setup_table) == 0:
        return pl.DataFrame(schema={
            "time": pl.Datetime, "close": pl.Float64, "high": pl.Float64,
            "low": pl.Float64, "atr_14": pl.Float64, "stop_price": pl.Float64,
            "direction": pl.Utf8, "trader": pl.Utf8, "setup_name": pl.Utf8,
            "sma10": pl.Float64, "sma20": pl.Float64, "sma50": pl.Float64,
            "base_low": pl.Float64, "base_high": pl.Float64,
            "extra_days": pl.Int64,
        })

    rows = []
    day_us = 86_400 * 1_000_000
    for r in setup_table.iter_rows(named=True):
        ds = r["date_signal"]
        # date_signal es un Date (Polars). Lo convertimos a datetime UTC dia siguiente.
        start_us = int(np.datetime64(ds, 'us').astype(np.int64)) + day_us  # T+1 00:00 UTC
        end_us = start_us + int(r["valid_days"]) * day_us
        pivot = float(r["pivot_high"])
        atr = float(r["atr_d1"])
        if not (np.isfinite(pivot) and np.isfinite(atr) and pivot > 0 and atr > 0):
            continue
        i0 = int(np.searchsorted(m1_times_us, start_us, side="left"))
        i1 = int(np.searchsorted(m1_times_us, end_us, side="left"))
        if i0 >= i1:
            continue
        # Primer cierre M1 que cruza pivot (LONG breakout)
        seg = m1_close[i0:i1]
        mask = seg > pivot
        if not mask.any():
            continue
        first_off = int(np.argmax(mask))
        sig_idx = i0 + first_off
        sig_us = int(m1_times_us[sig_idx])
        # construct row
        rows.append({
            "time": np.datetime64(sig_us, 'us').astype('datetime64[ms]').astype('O'),
            "close": float(m1_arr[sig_idx, 3]),
            "high": float(m1_arr[sig_idx, 1]),
            "low": float(m1_arr[sig_idx, 2]),
            "atr_14": atr,
            "stop_price": pivot,  # el STOP fill se hace cuando high>=pivot en el wait window
            "direction": "LONG",
            "trader": trader,
            "setup_name": setup_name,
            "sma10": r.get("sma10_d"),
            "sma20": r.get("sma20_d"),
            "sma50": r.get("sma50_d"),
            "base_low": float(r["base_low"]) if r["base_low"] is not None else None,
            "base_high": pivot,
            "extra_days": 0,
        })
    if not rows:
        return pl.DataFrame(schema={
            "time": pl.Datetime, "close": pl.Float64, "high": pl.Float64,
            "low": pl.Float64, "atr_14": pl.Float64, "stop_price": pl.Float64,
            "direction": pl.Utf8, "trader": pl.Utf8, "setup_name": pl.Utf8,
            "sma10": pl.Float64, "sma20": pl.Float64, "sma50": pl.Float64,
            "base_low": pl.Float64, "base_high": pl.Float64,
            "extra_days": pl.Int64,
        })
    df = pl.DataFrame(rows)
    df = df.with_columns(pl.col("time").cast(pl.Datetime))
    return df.sort("time")
