"""ORB break-fade: detect break of OR boundary, enter INVERSE direction.

Different from FADEAdapter (LIMIT at boundary): this one is STOP at boundary
(enters on break confirmation, then fades the move). TP/SL in ATR multipliers.
"""
import bisect
import json
from pathlib import Path

import polars as pl

from src.application.calculators import DataEnricher
from src.strategies_external.common.signal import Signal
from src.strategies_external.strategies.base import Strategy


class ORBBreakFadeAdapter(Strategy):
    name = "orb_breakfade"

    def __init__(
        self,
        asset_config_path: str = "src/infrastructure/config/asset_config.json",
        tick_size: float = 0.01,
    ):
        with open(asset_config_path) as f:
            self.asset_config = json.load(f)
        self.tick_size = tick_size

    def generate_signals_for_combo(
        self,
        df_m15: pl.DataFrame,   # base TF for OR computation; m15 is fine
        m1_df: pl.DataFrame,    # M1 bars to scan for the actual break
        symbol: str,
        magic_time: str,        # OR start, e.g. "07:00"
        duration: int,          # OR duration in minutes (60/90/120)
        atr_window: int = 14,
    ) -> list[Signal]:
        """For each day with valid OR, scan M1 post-OR session for first break.

        Returns a Signal with side OPPOSITE to break direction.
        """
        cfg = self.asset_config.get(symbol)
        if not cfg:
            return []
        # Use DataEnricher to get OR per day
        df_enriched = DataEnricher.enrich_with_daily_context(
            df_m15, cfg["pd_start"], cfg["pd_end"]
        )
        df_or = DataEnricher.enrich_with_opening_range(
            df_enriched, magic_time, duration,
        )

        # Per-day OR data: first post-OR bar per trade_date
        post_or_first = (
            df_or.filter(pl.col("is_post_or") == True)
            .sort("time")
            .group_by("trade_date")
            .agg([
                pl.col("time").first().alias("setup_ts"),
                pl.col("or_high").first().alias("or_high"),
                pl.col("or_low").first().alias("or_low"),
                pl.col("or_atr_ratio").first().alias("or_atr_ratio"),
            ])
            .filter(pl.col("or_atr_ratio").is_between(0.1, 0.8))
            .sort("setup_ts")
        )

        if post_or_first.is_empty() or m1_df is None or len(m1_df) == 0:
            return []

        # Pre-compute ATR(14) on M15 for use as TP/SL reference
        atr_df = (
            df_m15.with_columns(
                pl.max_horizontal(
                    pl.col("high") - pl.col("low"),
                    (pl.col("high") - pl.col("close").shift(1)).abs(),
                    (pl.col("low") - pl.col("close").shift(1)).abs(),
                ).alias("tr")
            )
            .with_columns(pl.col("tr").rolling_mean(atr_window).alias("atr_14"))
            .select(["time", "atr_14"])
        )
        # Map setup_ts -> atr_at_setup using as_of join (latest atr_14 <= setup_ts)
        post_or_with_atr = (
            post_or_first.sort("setup_ts")
            .join_asof(atr_df.sort("time"),
                       left_on="setup_ts", right_on="time",
                       strategy="backward")
            .drop("time")
            .filter(pl.col("atr_14").is_not_null())
            .filter(pl.col("atr_14") > 0)
        )
        if post_or_with_atr.is_empty():
            return []

        # M1 arrays for fast scan
        m1_sorted = m1_df.sort("time")
        m1_times = m1_sorted["time"].to_list()
        m1_highs = m1_sorted["high"].to_list()
        m1_lows = m1_sorted["low"].to_list()
        m1_closes = m1_sorted["close"].to_list()

        signals: list[Signal] = []

        # Session end for the bar of OR-start (broker time)
        # Use 23:59 of trade_date as session-end fallback. The runner will
        # apply session-end via session_end_hour_utc downstream.
        for row in post_or_with_atr.iter_rows(named=True):
            setup_ts = row["setup_ts"]
            or_high = row["or_high"]
            or_low = row["or_low"]
            atr = row["atr_14"]
            trade_date = row["trade_date"]

            if or_high is None or or_low is None or or_high <= or_low:
                continue

            # Scan M1 from setup_ts onwards within the SAME trade_date
            start_idx = bisect.bisect_right(m1_times, setup_ts)
            if start_idx >= len(m1_times):
                continue
            # End of day (broker date boundary)
            end_idx = start_idx
            while end_idx < len(m1_times) and m1_times[end_idx].date() == trade_date:
                end_idx += 1

            # Find first break: break_up = high > or_high; break_down = low < or_low
            break_dir = None
            break_idx = None
            for j in range(start_idx, end_idx):
                hi = m1_highs[j]
                lo = m1_lows[j]
                if hi is None or lo is None:
                    continue
                if hi > or_high:
                    break_dir = "UP"
                    break_idx = j
                    break
                if lo < or_low:
                    break_dir = "DOWN"
                    break_idx = j
                    break
            if break_dir is None:
                continue

            break_ts = m1_times[break_idx]
            valid_until = setup_ts.replace(hour=23, minute=59, second=0, microsecond=0)

            if break_dir == "UP":
                # INVERSE: SHORT. MARKET entry at the close of the M1 break bar.
                # This represents what a live system would see at the moment of
                # the break. Using STOP entries at or_high+tick caused look-ahead
                # bias in v1 (filled on retracement, leading to artifact WR=100%).
                entry = m1_closes[break_idx]
                signals.append(Signal(
                    symbol=symbol, strategy=self.name, side="short",
                    setup_ts=break_ts, entry_type="market",
                    entry_price=entry,
                    valid_until=valid_until,
                    stop=0.0, tp1=None, tp2=None,
                    indicator_anchors={
                        "atr_14": atr, "or_high": or_high, "or_low": or_low,
                        "or_width": or_high - or_low,
                        "magic_time_min": float(_hhmm_to_minutes(magic_time)),
                        "duration_min": float(duration),
                    },
                ))
            else:
                # INVERSE: LONG.
                # INVERSE: LONG. MARKET entry at the close of the M1 break bar.
                entry = m1_closes[break_idx]
                signals.append(Signal(
                    symbol=symbol, strategy=self.name, side="long",
                    setup_ts=break_ts, entry_type="market",
                    entry_price=entry,
                    valid_until=valid_until,
                    stop=0.0, tp1=None, tp2=None,
                    indicator_anchors={
                        "atr_14": atr, "or_high": or_high, "or_low": or_low,
                        "or_width": or_high - or_low,
                        "magic_time_min": float(_hhmm_to_minutes(magic_time)),
                        "duration_min": float(duration),
                    },
                ))
        return signals

    def generate_signals(self, df: pl.DataFrame, symbol: str) -> list[Signal]:
        return self.generate_signals_for_combo(df, df, symbol, "07:00", 60)


def _hhmm_to_minutes(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)
