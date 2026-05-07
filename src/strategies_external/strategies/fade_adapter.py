"""FADE adapter: reads bot_config.json + asset_config.json + M15 data,
produces Signal objects compatible with strategies_external backtester.
"""
import json
from datetime import timedelta
from pathlib import Path

import polars as pl

from src.application.calculators import DataEnricher
from src.domain.constants import MT5_TO_INTERNAL
from src.strategies_external.common.signal import Signal
from src.strategies_external.strategies.base import Strategy


# Symbols that have M1 data available in data/M1/
_M1_AVAILABLE = frozenset({
    "XAUUSD", "XAGUSD", "SP500", "NASDAQ100",
    "EURUSD", "USDJPY", "GBPAUD",
    "WTI", "BRENT", "NATGAS",
})


def load_fade_portfolio(
    bot_config_path: str = "src/execution/bot_config.json",
    enabled_only: bool = True,
    symbols_filter: "frozenset[str] | None" = _M1_AVAILABLE,
) -> list[dict]:
    """Carga estrategias FADE filtradas por enabled + symbols overlap M1.

    Convention: entries without an 'enabled' key are treated as enabled=True
    (they were added before the key was introduced). Entries with
    enabled=False are disabled.
    """
    with open(bot_config_path) as f:
        cfg = json.load(f)
    portfolio = cfg["portfolio"]
    out = []
    for s in portfolio:
        if enabled_only and s.get("enabled", True) is False:
            continue
        sym_internal = MT5_TO_INTERNAL.get(s["sym"], s["sym"])
        if symbols_filter is not None and sym_internal not in symbols_filter:
            continue
        out.append({**s, "sym_internal": sym_internal})
    return out


class FADEAdapter(Strategy):
    """Adapter that reads bot_config.json FADE strategies and generates Signals."""

    name = "fade"

    def __init__(
        self,
        asset_config_path: str = "src/infrastructure/config/asset_config.json",
    ):
        with open(asset_config_path) as f:
            self.asset_config = json.load(f)

    def generate_signals_for_strategy(
        self,
        df_m15: pl.DataFrame,
        symbol: str,
        strategy_cfg: dict,
    ) -> list[Signal]:
        """Genera signals historicos para una FADE strategy concreta.

        Args:
            df_m15: M15 OHLCV DataFrame for the symbol.
            symbol: internal symbol name (e.g. "EURUSD", "WTI").
            strategy_cfg: dict from bot_config.json with keys:
                edge, magic_time, duration, tp_mult, sl_mult, session.
        """
        cfg = self.asset_config.get(symbol)
        if not cfg:
            return []

        df_enriched = DataEnricher.enrich_with_daily_context(
            df_m15, cfg["pd_start"], cfg["pd_end"]
        )
        df_or = DataEnricher.enrich_with_opening_range(
            df_enriched,
            strategy_cfg["magic_time"],
            strategy_cfg["duration"],
        )

        # Detect first post-OR bar per trade_date (the bar where OR closes).
        # group_by does not guarantee order; sort ensures setup_ts == first post-OR bar.
        post_or_all = df_or.filter(pl.col("is_post_or") == True).sort("time")

        if post_or_all.is_empty():
            return []

        post_or_first = (
            post_or_all
            .group_by("trade_date")
            .agg(
                pl.col("time").first().alias("setup_ts"),
                pl.col("or_high").first().alias("or_high"),
                pl.col("or_low").first().alias("or_low"),
                pl.col("or_atr_ratio").first().alias("or_atr_ratio"),
            )
            # ATR filter (same as bot live: 0.1 <= or/atr <= 0.8)
            .filter(pl.col("or_atr_ratio").is_between(0.1, 0.8))
            .sort("trade_date")
        )

        if post_or_first.is_empty():
            return []

        edge = strategy_cfg["edge"]  # FADE_UP / FADE_DOWN
        tp_mult = strategy_cfg["tp_mult"]
        sl_mult = strategy_cfg["sl_mult"]

        signals: list[Signal] = []
        for row in post_or_first.iter_rows(named=True):
            or_high = row["or_high"]
            or_low = row["or_low"]
            or_width = or_high - or_low
            if or_width <= 0:
                continue
            setup_ts = row["setup_ts"]
            # Valid window: 6 hours after setup is reasonable.
            # FADE patterns mostly resolve within session; bot live uses session-end timestop.
            valid_until = setup_ts + timedelta(hours=6)

            anchors = {
                "tp_mult": tp_mult,
                "sl_mult": sl_mult,
                "or_high": or_high,
                "or_low": or_low,
                "or_width": or_width,
                "magic_time": _hhmm_to_minutes(strategy_cfg["magic_time"]),
                "duration": float(strategy_cfg["duration"]),
            }

            if edge == "FADE_UP":
                # SELL_LIMIT at OR_HIGH: price touches high and reverses.
                # Direction guard: cancel if OR_LOW breaches first (trend down).
                signals.append(Signal(
                    symbol=symbol,
                    strategy=self.name,
                    side="short",
                    setup_ts=setup_ts,
                    entry_type="limit",
                    entry_price=or_high,
                    valid_until=valid_until,
                    stop=0.0,   # filled by ExitManager
                    tp1=None,
                    tp2=None,
                    indicator_anchors=anchors,
                    cancel_on_opposite_breach=or_low,
                ))
            elif edge == "FADE_DOWN":
                # BUY_LIMIT at OR_LOW: price touches low and reverses.
                # Direction guard: cancel if OR_HIGH breaches first (trend up).
                signals.append(Signal(
                    symbol=symbol,
                    strategy=self.name,
                    side="long",
                    setup_ts=setup_ts,
                    entry_type="limit",
                    entry_price=or_low,
                    valid_until=valid_until,
                    stop=0.0,   # filled by ExitManager
                    tp1=None,
                    tp2=None,
                    indicator_anchors=anchors,
                    cancel_on_opposite_breach=or_high,
                ))

        return signals

    def generate_signals(self, df: pl.DataFrame, symbol: str) -> list[Signal]:
        """Strategy ABC compatibility: generates signals using default FADE_UP @ 07:00, 60min OR.

        Real use: call generate_signals_for_strategy with explicit cfg from bot_config.
        """
        return self.generate_signals_for_strategy(
            df,
            symbol,
            {
                "edge": "FADE_UP",
                "magic_time": "07:00",
                "duration": 60,
                "sl_mult": 2.5,
                "tp_mult": 0.5,
                "session": "London",
            },
        )


def _hhmm_to_minutes(hhmm: str) -> int:
    """Convert 'HH:MM' to total minutes from midnight."""
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)
