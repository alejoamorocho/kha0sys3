"""Backtester genérico: signal → fill → intra-bar tracking → Trade."""

from typing import Literal

import polars as pl

from src.strategies_external.common.signal import Signal
from src.strategies_external.common.trade import Trade
from src.strategies_external.constants import RISK_PER_TRADE_PCT_DEFAULT, friction_for


ExitMode = Literal["doc", "atr", "indicator"]


def _filter_window(df: pl.DataFrame, signal: Signal) -> pl.DataFrame:
    """Barras del tracking_tf relevantes para la señal."""
    return df.filter(
        (pl.col("time") > signal.setup_ts) & (pl.col("time") <= signal.valid_until)
    ).sort("time")


def _fill_condition(side: str, entry_type: str, price: float,
                    bar_open: float, bar_high: float, bar_low: float) -> bool:
    """¿La barra llena la orden?"""
    if entry_type == "market":
        return True
    if entry_type == "stop":
        if side == "long":
            return bar_high >= price
        return bar_low <= price
    if entry_type == "limit":
        if side == "long":
            return bar_low <= price
        return bar_high >= price
    raise ValueError(f"unknown entry_type: {entry_type}")


def run_backtest(
    signals: list[Signal],
    tracking_df: pl.DataFrame,
    exit_mode: ExitMode,
    signal_df: pl.DataFrame | None = None,
    risk_pct: float = RISK_PER_TRADE_PCT_DEFAULT,
) -> list[Trade]:
    """Ejecuta cada señal contra el DataFrame de tracking_tf.

    Resolución conservadora intra-bar: si una barra toca stop y tp en la
    misma vela, gana stop (worst case).

    Args:
        signal_df: DataFrame de la TF de señal (p.ej. daily para SMA-18).
            Necesario cuando exit_on_two_closes_against está set en la señal.
        risk_pct: Fracción de balance arriesgada por trade (para pnl_pct).
    """
    trades: list[Trade] = []
    for sig in signals:
        bars = _filter_window(tracking_df, sig)
        if bars.is_empty():
            continue

        rows = bars.to_dicts()
        filled = False
        entry_price = sig.entry_price
        entry_ts = sig.setup_ts
        first_idx = 0

        # Busca fill
        for i, bar in enumerate(rows):
            if _fill_condition(sig.side, sig.entry_type,
                               sig.entry_price, bar["open"], bar["high"], bar["low"]):
                filled = True
                entry_ts = bar["time"]
                # Slippage: 1 tick adverso. Usamos 0.05 como proxy genérico
                # para índices/commodities; FX se maneja con pip-equiv abajo.
                slip = 0.05 if sig.symbol not in {"EURUSD", "GBPUSD", "USDJPY",
                                                   "AUDUSD", "EURJPY", "GBPAUD",
                                                   "GBPJPY"} else 0.00005
                entry_price = sig.entry_price + slip if sig.side == "long" else sig.entry_price - slip
                first_idx = i
                break

        if not filled:
            continue

        # R uses the intended entry (sig.entry_price) so that slippage erodes
        # PnL but does not change the planned risk denominator. This matches
        # how the FADE/MATH live bots compute R.
        R = abs(sig.entry_price - sig.stop)
        if R == 0:
            continue

        # Pre-compute forced close via exit_on_two_closes_against (SMA-18 style).
        # Scan signal_df rows after entry_ts for N consecutive closes crossing level.
        forced_close_ts = None
        forced_close_price = None
        if sig.exit_on_two_closes_against is not None and signal_df is not None:
            level = sig.exit_on_two_closes_against
            count_req = sig.exit_close_count_required
            sig_rows_after = (
                signal_df.filter(pl.col("time") > entry_ts).sort("time").to_dicts()
            )
            consec = 0
            for srow in sig_rows_after:
                close_val = srow["close"]
                triggered = (close_val < level) if sig.side == "long" else (close_val > level)
                if triggered:
                    consec += 1
                    if consec >= count_req:
                        forced_close_ts = srow["time"]
                        forced_close_price = close_val
                        break
                else:
                    consec = 0

        exit_reason = None
        exit_price = None
        exit_ts = None
        bars_in_trade = 0

        # Tracking intra-bar
        for j in range(first_idx, len(rows)):
            bar = rows[j]
            bars_in_trade = j - first_idx + 1
            high = bar["high"]
            low = bar["low"]
            close = bar["close"]

            # NUEVO: forced close por exit_after_bars_if_below_R (Perdices Fib)
            if sig.exit_after_bars_if_below_R is not None:
                bars_threshold, r_threshold = sig.exit_after_bars_if_below_R
                if bars_in_trade >= bars_threshold:
                    if sig.side == "long":
                        cur_R = (close - sig.entry_price) / R
                    else:
                        cur_R = (sig.entry_price - close) / R
                    if cur_R < r_threshold:
                        exit_reason = "timestop"
                        exit_price = close
                        exit_ts = bar["time"]
                        break
                    # Si supera el threshold, no cerrar (deja correr)

            # NUEVO: forced close por 2 cierres consecutivos contra nivel (SMA-18)
            if forced_close_ts is not None and bar["time"] >= forced_close_ts:
                exit_reason = "signal_inverso"
                exit_price = forced_close_price
                exit_ts = forced_close_ts
                break

            if sig.side == "long":
                touches_stop = low <= sig.stop
                touches_tp1 = sig.tp1 is not None and high >= sig.tp1
                touches_tp2 = sig.tp2 is not None and high >= sig.tp2
                if touches_stop:
                    exit_reason = "stop"; exit_price = sig.stop; exit_ts = bar["time"]; break
                if touches_tp2:
                    exit_reason = "tp2"; exit_price = sig.tp2; exit_ts = bar["time"]; break
                if touches_tp1:
                    exit_reason = "tp1"; exit_price = sig.tp1; exit_ts = bar["time"]; break
            else:
                touches_stop = high >= sig.stop
                touches_tp1 = sig.tp1 is not None and low <= sig.tp1
                touches_tp2 = sig.tp2 is not None and low <= sig.tp2
                if touches_stop:
                    exit_reason = "stop"; exit_price = sig.stop; exit_ts = bar["time"]; break
                if touches_tp2:
                    exit_reason = "tp2"; exit_price = sig.tp2; exit_ts = bar["time"]; break
                if touches_tp1:
                    exit_reason = "tp1"; exit_price = sig.tp1; exit_ts = bar["time"]; break

            if sig.timestop_bars is not None and bars_in_trade >= sig.timestop_bars:
                exit_reason = "timestop"; exit_price = close; exit_ts = bar["time"]; break

        if exit_reason is None:
            # Cierre por valid_until (eod): tomamos close de la última barra
            last_bar = rows[-1]
            exit_reason = "eod"; exit_price = last_bar["close"]; exit_ts = last_bar["time"]

        # PnL bruto en R
        if sig.side == "long":
            pnl_gross_R = (exit_price - entry_price) / R
        else:
            pnl_gross_R = (entry_price - exit_price) / R

        pnl_net_R = pnl_gross_R - friction_for(sig.symbol)

        pnl_pct = pnl_net_R * risk_pct

        trades.append(Trade(
            symbol=sig.symbol,
            strategy=sig.strategy,
            exit_mode=exit_mode,
            side=sig.side,
            entry_ts=entry_ts,
            entry=entry_price,
            stop=sig.stop,
            tp1=sig.tp1,
            tp2=sig.tp2,
            exit_ts=exit_ts,
            exit=exit_price,
            exit_reason=exit_reason,
            R=R,
            pnl_R=pnl_net_R,
            pnl_pct=pnl_pct,
            bars_in_trade=bars_in_trade,
        ))

    return trades
