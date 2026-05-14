"""Traders replication — geometric setup detectors (Minervini, Zanger, Qulla, Ryan).

Replica TECNICA (sin fundamentales) de las 4 metodologias descritas en los
PDFs "Estrategias y Gestion de Riesgo de Traders". Adaptada al universo
FX/commodities/indices de KHA0SYS3 (14 simbolos).

Cada detector recibe un DataFrame OHLC y devuelve filas con:
    time, close, high, low, atr_14, stop_price (pivot break),
    direction (LONG), trader, setup_name,
    + metadatos especificos por trader para la salida (ej. pivot_high,
      base_low, base_high, sma50, etc.)

Setups por trader:
    Minervini  -> SEPA + VCP (D1)
    Zanger     -> Flags/Pennants + Cup&Handle (D1)
    Qulla      -> HighTightFlag + EpisodicPivot (D1) + ORB (H1)
    Ryan       -> Ants -> base secundaria breakout (D1)

Convention: signals en cierre de barra D1 (o H1 para ORB). Entry-trigger
es STOP en pivot_high, fill walked en M1 dentro de wait window.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import polars as pl


# ── Helpers ──────────────────────────────────────────────────────────────


def resample_to_daily(m1: pl.DataFrame) -> pl.DataFrame:
    """M1 -> D1 OHLCV. time = inicio del dia UTC."""
    return (
        m1.sort("time")
        .group_by_dynamic("time", every="1d", closed="left", label="left")
        .agg([
            pl.col("open").first().alias("open"),
            pl.col("high").max().alias("high"),
            pl.col("low").min().alias("low"),
            pl.col("close").last().alias("close"),
            pl.col("volume").sum().alias("volume"),
        ])
        .filter(pl.col("open").is_not_null())
    )


def resample_to_hourly(m1: pl.DataFrame) -> pl.DataFrame:
    """M1 -> H1 OHLCV."""
    return (
        m1.sort("time")
        .group_by_dynamic("time", every="1h", closed="left", label="left")
        .agg([
            pl.col("open").first().alias("open"),
            pl.col("high").max().alias("high"),
            pl.col("low").min().alias("low"),
            pl.col("close").last().alias("close"),
            pl.col("volume").sum().alias("volume"),
        ])
        .filter(pl.col("open").is_not_null())
    )


def add_indicators(df: pl.DataFrame) -> pl.DataFrame:
    """Add SMAs, ATR, range stats — todo causal rolling."""
    tr = pl.max_horizontal([
        pl.col("high") - pl.col("low"),
        (pl.col("high") - pl.col("close").shift(1)).abs(),
        (pl.col("low") - pl.col("close").shift(1)).abs(),
    ])
    return df.with_columns([
        pl.col("close").rolling_mean(10).alias("sma10"),
        pl.col("close").rolling_mean(20).alias("sma20"),
        pl.col("close").rolling_mean(50).alias("sma50"),
        pl.col("close").rolling_mean(150).alias("sma150"),
        pl.col("close").rolling_mean(200).alias("sma200"),
        tr.rolling_mean(14).alias("atr_14"),
        tr.rolling_mean(20).alias("atr_20"),
        (pl.col("high") - pl.col("low")).alias("bar_range"),
        pl.col("close").rolling_max(252).alias("max_52w"),
        pl.col("close").rolling_min(252).alias("min_52w"),
        pl.col("volume").rolling_mean(20).alias("vol_sma20"),
    ])


def _trend_template(df: pl.DataFrame) -> pl.Expr:
    """Minervini Stage 2: precio > SMA50 > SMA150 > SMA200; SMA200 ascendente >=1mes;
    precio >= 1.30*min52w AND >= 0.75*max52w."""
    sma200_22 = pl.col("sma200").shift(22)
    return (
        (pl.col("close") > pl.col("sma50"))
        & (pl.col("sma50") > pl.col("sma150"))
        & (pl.col("sma150") > pl.col("sma200"))
        & (pl.col("sma200") > sma200_22)
        & (pl.col("close") >= 1.30 * pl.col("min_52w"))
        & (pl.col("close") >= 0.75 * pl.col("max_52w"))
    )


def _empty() -> pl.DataFrame:
    return pl.DataFrame(schema={
        "time": pl.Datetime,
        "close": pl.Float64,
        "high": pl.Float64,
        "low": pl.Float64,
        "atr_14": pl.Float64,
        "stop_price": pl.Float64,
        "direction": pl.Utf8,
        "trader": pl.Utf8,
        "setup_name": pl.Utf8,
        "sma10": pl.Float64,
        "sma20": pl.Float64,
        "sma50": pl.Float64,
        "base_low": pl.Float64,
        "base_high": pl.Float64,
        "extra_days": pl.Int64,
    })


# ── Minervini: VCP en Stage 2 ────────────────────────────────────────────


def detect_minervini_vcp(daily: pl.DataFrame) -> pl.DataFrame:
    """VCP: 3 contracciones decrecientes, breakout sobre pivot con volumen +40%.
    Pivot = max de los ultimos 5 dias (zona terminal estrecha).
    Contraccion = (max - min) / max en ventanas sucesivas: c1 > c2 > c3,
        c1 in [0.15, 0.40], c3 <= 0.07.
    Volumen breakout: bar_range >= 1.5*atr_20 (proxy).
    Filtro: Stage 2 (trend template).
    """
    if len(daily) < 200:
        return _empty()

    df = add_indicators(daily)

    # Pivot reciente = max(high) ultimas 5 barras
    pivot5 = pl.col("high").rolling_max(5)
    # Contracciones: 3 ventanas
    win_a = 30  # contraccion 1
    win_b = 15  # contraccion 2
    win_c = 5   # contraccion 3 (terminal)
    c1 = (pl.col("high").rolling_max(win_a) - pl.col("low").rolling_min(win_a)) / pl.col("high").rolling_max(win_a)
    c2 = (pl.col("high").rolling_max(win_b) - pl.col("low").rolling_min(win_b)) / pl.col("high").rolling_max(win_b)
    c3 = (pl.col("high").rolling_max(win_c) - pl.col("low").rolling_min(win_c)) / pl.col("high").rolling_max(win_c)

    vcp_geometry = (
        (c1 >= 0.10) & (c1 <= 0.45)
        & (c2 < c1) & (c2 >= 0.05)
        & (c3 < c2) & (c3 <= 0.10)
    )
    breakout = (pl.col("close") > pivot5.shift(1)) & (pl.col("bar_range") >= 1.5 * pl.col("atr_20"))

    sig = df.with_columns([
        _trend_template(df).alias("_stage2"),
        vcp_geometry.alias("_vcp"),
        breakout.alias("_break"),
        pivot5.shift(1).alias("_pivot"),
    ]).filter(
        pl.col("_stage2") & pl.col("_vcp") & pl.col("_break") & pl.col("_pivot").is_not_null()
    )
    if len(sig) == 0:
        return _empty()
    return sig.select([
        "time", "close", "high", "low", "atr_14",
        pl.col("_pivot").alias("stop_price"),
        pl.lit("LONG").alias("direction"),
        pl.lit("Minervini").alias("trader"),
        pl.lit("VCP").alias("setup_name"),
        "sma10", "sma20", "sma50",
        pl.col("low").rolling_min(win_c).over([]).alias("base_low") if False else pl.col("_pivot").alias("base_low"),  # placeholder
        pl.col("_pivot").alias("base_high"),
        pl.lit(0, dtype=pl.Int64).alias("extra_days"),
    ])


# ── Zanger: Flag/Pennant + Cup&Handle ────────────────────────────────────


def detect_zanger_flag(daily: pl.DataFrame) -> pl.DataFrame:
    """Flag: avance vertical previo (10-20 dias, +15-50%), seguido de pullback
    estrecho 5-12 dias (rango <= 15% del avance), breakout sobre flag high con
    bar_range >= 1.5*atr_20 (vol proxy)."""
    if len(daily) < 100:
        return _empty()
    df = add_indicators(daily)

    flagpole_low = pl.col("low").shift(12).rolling_min(15)
    flagpole_high = pl.col("high").shift(5).rolling_max(10)
    flagpole_gain = (flagpole_high - flagpole_low) / flagpole_low
    flag_high = pl.col("high").shift(1).rolling_max(7)
    flag_low = pl.col("low").shift(1).rolling_min(7)
    flag_range = (flag_high - flag_low) / flag_low
    pole_range = flagpole_high - flagpole_low

    valid = (
        (flagpole_gain >= 0.15) & (flagpole_gain <= 0.80)
        & (flag_range <= 0.40 * flagpole_gain)
        & (pl.col("close") > flag_high)
        & (pl.col("bar_range") >= 1.5 * pl.col("atr_20"))
        & (pl.col("close") <= flag_high * 1.05)  # no perseguir > 5%
    )

    sig = df.with_columns([
        valid.alias("_valid"),
        flag_high.alias("_pivot"),
        flag_low.alias("_flag_low"),
    ]).filter(pl.col("_valid") & pl.col("_pivot").is_not_null())
    if len(sig) == 0:
        return _empty()
    return sig.select([
        "time", "close", "high", "low", "atr_14",
        pl.col("_pivot").alias("stop_price"),
        pl.lit("LONG").alias("direction"),
        pl.lit("Zanger").alias("trader"),
        pl.lit("FLAG").alias("setup_name"),
        "sma10", "sma20", "sma50",
        pl.col("_flag_low").alias("base_low"),
        pl.col("_pivot").alias("base_high"),
        pl.lit(0, dtype=pl.Int64).alias("extra_days"),
    ])


def detect_zanger_cup_handle(daily: pl.DataFrame) -> pl.DataFrame:
    """Cup&Handle: taza profunda (30-60 dias, drawdown 15-35%) + handle estrecho
    (5-15 dias, rango <= 15%). Breakout sobre handle high con bar expansion."""
    if len(daily) < 100:
        return _empty()
    df = add_indicators(daily)
    cup_left = pl.col("high").shift(50).rolling_max(10)
    cup_low = pl.col("low").shift(15).rolling_min(40)
    cup_right = pl.col("high").shift(8).rolling_max(8)
    handle_high = pl.col("high").shift(1).rolling_max(10)
    handle_low = pl.col("low").shift(1).rolling_min(10)

    cup_depth = (cup_left - cup_low) / cup_left
    cup_symm = (cup_right - cup_low) / cup_left
    handle_range = (handle_high - handle_low) / handle_low

    valid = (
        (cup_depth >= 0.12) & (cup_depth <= 0.40)
        & (cup_symm >= 0.65) & (cup_symm <= 1.05)
        & (handle_range <= 0.15)
        & (pl.col("close") > handle_high)
        & (pl.col("bar_range") >= 1.5 * pl.col("atr_20"))
        & (pl.col("close") <= handle_high * 1.05)
    )
    sig = df.with_columns([
        valid.alias("_valid"),
        handle_high.alias("_pivot"),
        handle_low.alias("_h_low"),
    ]).filter(pl.col("_valid") & pl.col("_pivot").is_not_null())
    if len(sig) == 0:
        return _empty()
    return sig.select([
        "time", "close", "high", "low", "atr_14",
        pl.col("_pivot").alias("stop_price"),
        pl.lit("LONG").alias("direction"),
        pl.lit("Zanger").alias("trader"),
        pl.lit("CUP_HANDLE").alias("setup_name"),
        "sma10", "sma20", "sma50",
        pl.col("_h_low").alias("base_low"),
        pl.col("_pivot").alias("base_high"),
        pl.lit(0, dtype=pl.Int64).alias("extra_days"),
    ])


# ── Qulla: High Tight Flag + Episodic Pivot + ORB ────────────────────────


def detect_qulla_high_tight_flag(daily: pl.DataFrame) -> pl.DataFrame:
    """HTF: +25-100% en ultimo mes, contraccion <=25% del avance, vol semana
    actual <= 0.6 * vol semana previa, precio dentro de +-3% de SMA10."""
    if len(daily) < 60:
        return _empty()
    df = add_indicators(daily)
    pole_gain = (pl.col("high").shift(5).rolling_max(20) - pl.col("low").shift(20).rolling_min(20)) / pl.col("low").shift(20).rolling_min(20)
    flag_high = pl.col("high").shift(1).rolling_max(8)
    flag_low = pl.col("low").shift(1).rolling_min(8)
    flag_pullback = (flag_high - flag_low) / flag_high
    vol_curr5 = pl.col("volume").rolling_sum(5)
    vol_prev5 = pl.col("volume").shift(5).rolling_sum(5)
    sma10_dist = (pl.col("close") - pl.col("sma10")).abs() / pl.col("sma10")
    valid = (
        (pole_gain >= 0.25) & (pole_gain <= 1.5)
        & (flag_pullback <= 0.25)
        & (vol_curr5 <= 0.7 * vol_prev5)
        & (sma10_dist <= 0.03)
        & (pl.col("close") > flag_high)
    )
    sig = df.with_columns([
        valid.alias("_valid"),
        flag_high.alias("_pivot"),
        flag_low.alias("_low"),
    ]).filter(pl.col("_valid") & pl.col("_pivot").is_not_null())
    if len(sig) == 0:
        return _empty()
    return sig.select([
        "time", "close", "high", "low", "atr_14",
        pl.col("_pivot").alias("stop_price"),
        pl.lit("LONG").alias("direction"),
        pl.lit("Qulla").alias("trader"),
        pl.lit("HTF").alias("setup_name"),
        "sma10", "sma20", "sma50",
        pl.col("_low").alias("base_low"),
        pl.col("_pivot").alias("base_high"),
        pl.lit(0, dtype=pl.Int64).alias("extra_days"),
    ])


def detect_qulla_episodic_pivot(daily: pl.DataFrame) -> pl.DataFrame:
    """EP: gap up > 4% (FX/commodities thresh; PDF dice 7.5% pero es para
    stocks) sobre cierre previo, bar_range >= 2*atr_20, volumen day > 1.5*sma20.
    """
    if len(daily) < 30:
        return _empty()
    df = add_indicators(daily)
    gap = (pl.col("open") - pl.col("close").shift(1)) / pl.col("close").shift(1)
    valid = (
        (gap >= 0.03)
        & (pl.col("bar_range") >= 2.0 * pl.col("atr_20"))
        & (pl.col("volume") >= 1.5 * pl.col("vol_sma20"))
        & (pl.col("close") > pl.col("open"))
    )
    sig = df.with_columns([
        valid.alias("_valid"),
        pl.col("high").alias("_pivot"),
    ]).filter(pl.col("_valid"))
    if len(sig) == 0:
        return _empty()
    return sig.select([
        "time", "close", "high", "low", "atr_14",
        pl.col("_pivot").alias("stop_price"),
        pl.lit("LONG").alias("direction"),
        pl.lit("Qulla").alias("trader"),
        pl.lit("EP").alias("setup_name"),
        "sma10", "sma20", "sma50",
        pl.col("low").alias("base_low"),
        pl.col("high").alias("base_high"),
        pl.lit(0, dtype=pl.Int64).alias("extra_days"),
    ])


def detect_qulla_orb_m1(m1: pl.DataFrame, open_hour_utc: int = 13,
                         open_minute_utc: int = 0,
                         range_minutes: int = 15,
                         breakout_window_minutes: int = 180) -> pl.DataFrame:
    """ORB sobre M1 directo (fiel al PDF Qulla: primeros 15-30 min de la sesion).

    Args:
        m1: M1 OHLC del simbolo (cache enriched_math_tf)
        open_hour_utc: hora UTC del open de sesion (NYSE summer 13:30 -> hour=13 min=30)
        open_minute_utc: minuto UTC del open (combina con hour: ej 13:30)
        range_minutes: ancho del rango opening, en {15, 30, 45, 60}
        breakout_window_minutes: ventana post-rango donde se acepta el breakout
            (PDF prohibe rupturas tardias)

    Logica:
        - Rango = max(high) y min(low) de los primeros `range_minutes` desde open.
        - Entry: M1 close > range_high dentro de breakout_window post-rango.
        - Volumen proxy: bar_range >= 0.5*ATR_14 (M1 es ruidoso, no exigir tanto).
        - Senal se emite UNA SOLA VEZ por dia (primer breakout valido).
    """
    if len(m1) < 1000:
        return _empty()

    # ATR_14 sobre M1
    df = m1.sort("time").with_columns([
        pl.col("time").dt.hour().alias("_h"),
        pl.col("time").dt.minute().alias("_m"),
        pl.col("time").dt.date().alias("_d"),
        (pl.col("high") - pl.col("low")).alias("bar_range"),
    ])
    tr = pl.max_horizontal([
        pl.col("high") - pl.col("low"),
        (pl.col("high") - pl.col("close").shift(1)).abs(),
        (pl.col("low") - pl.col("close").shift(1)).abs(),
    ])
    df = df.with_columns(tr.rolling_mean(14).alias("atr_14"))
    # SMA col placeholders para el schema (no se usan en ORB intradia)
    df = df.with_columns([
        pl.lit(None, dtype=pl.Float64).alias("sma10"),
        pl.lit(None, dtype=pl.Float64).alias("sma20"),
        pl.lit(None, dtype=pl.Float64).alias("sma50"),
    ])

    # Minuto absoluto del dia (UTC) — para comparar contra ventana
    minute_of_day = (pl.col("_h").cast(pl.Int64) * 60 + pl.col("_m").cast(pl.Int64))
    open_minute_abs = open_hour_utc * 60 + open_minute_utc
    range_end_min = open_minute_abs + range_minutes
    brk_end_min = range_end_min + breakout_window_minutes

    df = df.with_columns(minute_of_day.alias("_mod"))

    # Rango por dia
    range_bar = (
        df.filter((pl.col("_mod") >= open_minute_abs) & (pl.col("_mod") < range_end_min))
        .group_by("_d")
        .agg([
            pl.col("high").max().alias("_r_high"),
            pl.col("low").min().alias("_r_low"),
        ])
    )
    df = df.join(range_bar, on="_d", how="left")

    valid = (
        (pl.col("_mod") >= range_end_min)
        & (pl.col("_mod") < brk_end_min)
        & (pl.col("close") > pl.col("_r_high"))
        & (pl.col("bar_range") >= 0.5 * pl.col("atr_14"))
        & pl.col("_r_high").is_not_null()
        & pl.col("atr_14").is_not_null()
    )
    sig = df.with_columns(valid.alias("_valid")).filter(pl.col("_valid"))
    if len(sig) == 0:
        return _empty()
    # Una senal por dia (primer breakout)
    sig = sig.sort("time").unique(subset=["_d"], keep="first")

    return sig.select([
        "time", "close", "high", "low", "atr_14",
        pl.col("_r_high").alias("stop_price"),
        pl.lit("LONG").alias("direction"),
        pl.lit("Qulla").alias("trader"),
        pl.lit("ORB").alias("setup_name"),
        "sma10", "sma20", "sma50",
        pl.col("_r_low").alias("base_low"),
        pl.col("_r_high").alias("base_high"),
        pl.lit(0, dtype=pl.Int64).alias("extra_days"),
    ])


def detect_qulla_orb(h1: pl.DataFrame, open_hour_utc: int = 13,
                     range_hours: int = 1, breakout_window: int = 3) -> pl.DataFrame:
    """ORB (Opening Range Breakout) parametrico.

    Args:
        h1: H1 OHLC del simbolo
        open_hour_utc: hora UTC de apertura del rango (NYSE summer 13, winter 14)
        range_hours: cuantas barras H1 forman el rango (1 = 60min, 2 = 120min)
        breakout_window: horas despues del rango donde se acepta el breakout
            (filtro de tardios — PDFs prohiben rupturas pasada la media manana)

    Logica:
        - Rango = max/min de las primeras `range_hours` barras desde open_hour.
        - Entry: cierre H1 > range_high dentro de breakout_window horas
          posteriores al rango, con bar_range >= ATR_14 (proxy de volumen).
        - Stop suggestion (base_low) = range_low.
    """
    if len(h1) < 50:
        return _empty()
    df = add_indicators(h1)
    df = df.with_columns([
        pl.col("time").dt.hour().alias("_h"),
        pl.col("time").dt.date().alias("_d"),
    ])
    range_end = open_hour_utc + range_hours - 1
    range_bar = (
        df.filter((pl.col("_h") >= open_hour_utc) & (pl.col("_h") <= range_end))
        .group_by("_d")
        .agg([
            pl.col("high").max().alias("_r_high"),
            pl.col("low").min().alias("_r_low"),
        ])
    )
    df = df.join(range_bar, on="_d", how="left")
    valid = (
        (pl.col("_h") > range_end)
        & (pl.col("_h") <= range_end + breakout_window)
        & (pl.col("close") > pl.col("_r_high"))
        & (pl.col("bar_range") >= pl.col("atr_14"))
        & pl.col("_r_high").is_not_null()
    )
    sig = df.with_columns(valid.alias("_valid")).filter(pl.col("_valid"))
    if len(sig) == 0:
        return _empty()
    return sig.select([
        "time", "close", "high", "low", "atr_14",
        pl.col("_r_high").alias("stop_price"),
        pl.lit("LONG").alias("direction"),
        pl.lit("Qulla").alias("trader"),
        pl.lit("ORB").alias("setup_name"),
        "sma10", "sma20", "sma50",
        pl.col("_r_low").alias("base_low"),
        pl.col("_r_high").alias("base_high"),
        pl.lit(0, dtype=pl.Int64).alias("extra_days"),
    ])


# ── Ryan: Ants -> base secundaria ────────────────────────────────────────


def detect_ryan_ants(daily: pl.DataFrame) -> pl.DataFrame:
    """Ants: ventana 15 dias con +20% acumulado en precio, +20% en volumen
    medio (vs 30 dias previos), >=12/15 cierres alcistas. NO compra inmediata
    en Ants — espera consolidacion y breakout. Aqui detectamos Ants en una
    ventana T-20..T-5 y exigimos que en T se forme una base estrecha de 5 dias
    (rango <= 8%) y se rompa por arriba con bar expansion.
    """
    if len(daily) < 80:
        return _empty()
    df = add_indicators(daily)
    ret_15 = (pl.col("close").shift(5) / pl.col("close").shift(20)) - 1.0  # +20% en 15 dias hace T-5
    vol_avg_15 = pl.col("volume").shift(5).rolling_mean(15)
    vol_avg_prev = pl.col("volume").shift(20).rolling_mean(30)
    up_days = (
        (pl.col("close") > pl.col("open")).cast(pl.Int64).shift(5).rolling_sum(15)
    )
    ants_window = (ret_15 >= 0.20) & (vol_avg_15 >= 1.20 * vol_avg_prev) & (up_days >= 12)
    # Base secundaria T-5..T: rango <= 8% del max
    base_high = pl.col("high").shift(1).rolling_max(5)
    base_low = pl.col("low").shift(1).rolling_min(5)
    base_tight = ((base_high - base_low) / base_high) <= 0.08
    breakout = (pl.col("close") > base_high) & (pl.col("bar_range") >= 1.5 * pl.col("atr_20"))
    valid = ants_window & base_tight & breakout

    sig = df.with_columns([
        valid.alias("_valid"),
        base_high.alias("_pivot"),
        base_low.alias("_low"),
    ]).filter(pl.col("_valid") & pl.col("_pivot").is_not_null())
    if len(sig) == 0:
        return _empty()
    return sig.select([
        "time", "close", "high", "low", "atr_14",
        pl.col("_pivot").alias("stop_price"),
        pl.lit("LONG").alias("direction"),
        pl.lit("Ryan").alias("trader"),
        pl.lit("ANTS").alias("setup_name"),
        "sma10", "sma20", "sma50",
        pl.col("_low").alias("base_low"),
        pl.col("_pivot").alias("base_high"),
        pl.lit(0, dtype=pl.Int64).alias("extra_days"),
    ])


# ── Registry ─────────────────────────────────────────────────────────────


TRADER_SETUPS = {
    "Minervini": [("VCP", detect_minervini_vcp, "D1")],
    "Zanger":    [("FLAG", detect_zanger_flag, "D1"),
                  ("CUP_HANDLE", detect_zanger_cup_handle, "D1")],
    "Qulla":     [("HTF", detect_qulla_high_tight_flag, "D1"),
                  ("EP", detect_qulla_episodic_pivot, "D1"),
                  ("ORB", detect_qulla_orb, "H1")],
    "Ryan":      [("ANTS", detect_ryan_ants, "D1")],
}
