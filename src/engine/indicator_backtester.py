"""Event-driven backtester for INDICATOR-archetype signals.

Each signal becomes a LIMIT at the signal bar's close price. TP = entry ± tp_atr_mult*ATR,
SL = entry ∓ sl_atr_mult*ATR. Trades time-stop at session_end_hour_utc.
Dedup: at most one trade per (symbol, signal_type, trade_date).
"""
from __future__ import annotations
from dataclasses import dataclass
import polars as pl


@dataclass(frozen=True)
class BacktestConfig:
    tp_atr_mult: float
    sl_atr_mult: float
    session_end_hour_utc: int
    friction_r: float


class IndicatorBacktester:

    @staticmethod
    def run(signals: pl.DataFrame, bars: pl.DataFrame, cfg: BacktestConfig) -> pl.DataFrame:
        """Return trade-level DataFrame: time, symbol, signal_type, direction,
        entry_price, tp_price, sl_price, exit_time, exit_price, exit_reason, r_multiple."""
        if len(signals) == 0:
            return _empty_trades()

        # Dedup: keep first per (symbol, signal_type, trade_date)
        deduped = signals.with_columns([
            pl.col("time").dt.date().alias("_date")
        ]).sort("time").unique(
            subset=["symbol", "signal_type", "_date"], keep="first"
        ).drop("_date")

        # Build bars index for fast lookup
        bars_sorted = bars.sort("time")
        bar_times = bars_sorted["time"].to_list()
        bar_highs = bars_sorted["high"].to_list()
        bar_lows = bars_sorted["low"].to_list()
        bar_closes = bars_sorted["close"].to_list()

        # Build dict time -> idx
        time_to_idx = {t: i for i, t in enumerate(bar_times)}

        results = []
        for sig in deduped.iter_rows(named=True):
            if sig["atr_14"] is None:
                continue
            entry = sig["close"]
            atr = sig["atr_14"]
            direction = sig["direction"]
            if direction == "LONG":
                tp = entry + cfg.tp_atr_mult * atr
                sl = entry - cfg.sl_atr_mult * atr
            else:
                tp = entry - cfg.tp_atr_mult * atr
                sl = entry + cfg.sl_atr_mult * atr

            # Scan bars forward from signal bar + 1 until session_end or TP/SL hit
            start_idx = time_to_idx.get(sig["time"])
            if start_idx is None:
                continue
            exit_reason = None
            exit_price = None
            exit_time = None
            signal_date = sig["time"].date()
            for i in range(start_idx + 1, len(bar_times)):
                bt = bar_times[i]
                # Stop at session end on same trading day
                if bt.date() > signal_date or bt.hour >= cfg.session_end_hour_utc:
                    exit_reason = "TIME_STOP"
                    exit_price = bar_closes[i - 1]
                    exit_time = bar_times[i - 1]
                    break
                hi = bar_highs[i]
                lo = bar_lows[i]
                if direction == "LONG":
                    if hi >= tp:
                        exit_reason, exit_price, exit_time = "TP", tp, bt
                        break
                    if lo <= sl:
                        exit_reason, exit_price, exit_time = "SL", sl, bt
                        break
                else:
                    if lo <= tp:
                        exit_reason, exit_price, exit_time = "TP", tp, bt
                        break
                    if hi >= sl:
                        exit_reason, exit_price, exit_time = "SL", sl, bt
                        break
            else:
                # Reached end of bars without hitting anything
                exit_reason = "TIME_STOP"
                exit_price = bar_closes[-1]
                exit_time = bar_times[-1]

            # R-multiple
            risk_per_unit = cfg.sl_atr_mult * atr
            if direction == "LONG":
                pnl = exit_price - entry
            else:
                pnl = entry - exit_price
            r_gross = pnl / risk_per_unit if risk_per_unit > 0 else 0.0
            r_net = r_gross - cfg.friction_r

            results.append({
                "time": sig["time"], "symbol": sig["symbol"],
                "signal_type": sig["signal_type"], "direction": direction,
                "entry_price": entry, "tp_price": tp, "sl_price": sl,
                "exit_time": exit_time, "exit_price": exit_price,
                "exit_reason": exit_reason, "r_multiple": r_net,
            })
        if not results:
            return _empty_trades()
        return pl.DataFrame(results)


def _empty_trades() -> pl.DataFrame:
    return pl.DataFrame(schema={
        "time": pl.Datetime, "symbol": pl.Utf8, "signal_type": pl.Utf8, "direction": pl.Utf8,
        "entry_price": pl.Float64, "tp_price": pl.Float64, "sl_price": pl.Float64,
        "exit_time": pl.Datetime, "exit_price": pl.Float64, "exit_reason": pl.Utf8,
        "r_multiple": pl.Float64,
    })
