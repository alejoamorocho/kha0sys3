"""Inna Rosputnia Doble Suelo cualificado.

Detector + filtros (precio > SMA18, ruptura neckline, consolidacion 3-5 barras
con rango < 1xATR(14)). Trigger: ruptura del high de la consolidacion + 1 tick.
"""

from datetime import timedelta

import polars as pl

from src.strategies_external.common.signal import Signal
from src.strategies_external.strategies.base import Strategy
from src.strategies_external.strategies.swings import find_swings


_TICK = 0.01


class DoubleBottomStrategy(Strategy):
    name = "double_bottom"

    def __init__(
        self,
        tolerance: float = 0.02,
        min_separation: int = 15,
        max_separation: int = 80,
        consol_min_bars: int = 3,
        consol_max_atr_mult: float = 1.0,
        sma_window: int = 18,
        atr_window: int = 14,
    ):
        self.tolerance = tolerance
        self.min_separation = min_separation
        self.max_separation = max_separation
        self.consol_min_bars = consol_min_bars
        self.consol_max_atr_mult = consol_max_atr_mult
        self.sma_window = sma_window
        self.atr_window = atr_window

    def generate_signals(self, df: pl.DataFrame, symbol: str) -> list[Signal]:
        # Need enough bars to compute SMA/ATR + at least min_separation for a W pattern
        min_bars = max(self.sma_window, self.atr_window) + self.min_separation + 5
        if df.is_empty() or df.shape[0] < min_bars:
            return []

        enriched = (
            df.with_columns(
                pl.col("close").rolling_mean(self.sma_window).alias("sma"),
                pl.max_horizontal(
                    pl.col("high") - pl.col("low"),
                    (pl.col("high") - pl.col("close").shift(1)).abs(),
                    (pl.col("low") - pl.col("close").shift(1)).abs(),
                ).alias("tr"),
            )
            .with_columns(pl.col("tr").rolling_mean(self.atr_window).alias("atr"))
        )
        rows = enriched.to_dicts()

        swing_lows, swing_highs = find_swings(df, prominence_factor=0.5,
                                               min_distance=self.consol_min_bars)
        signals: list[Signal] = []

        for L2_idx, L2 in swing_lows:
            for L1_idx, L1 in swing_lows:
                if L1_idx >= L2_idx:
                    continue
                if not (self.min_separation <= L2_idx - L1_idx <= self.max_separation):
                    continue
                if L2 <= 0 or abs(L1 - L2) / L2 > self.tolerance:
                    continue
                # neckline = max high entre L1 y L2
                neckline = max(rows[i]["high"] for i in range(L1_idx, L2_idx + 1))
                altura = neckline - L2
                if altura <= 0:
                    continue
                # buscar ruptura + consolidacion post-neckline
                for trigger_idx in range(L2_idx + self.consol_min_bars, len(rows)):
                    cur = rows[trigger_idx]
                    if cur.get("sma") is None or cur["close"] <= cur["sma"]:
                        continue
                    if cur["close"] <= neckline:
                        continue
                    # consolidacion de ultimas N barras antes de trigger
                    consol_start = max(0, trigger_idx - self.consol_min_bars + 1)
                    consol_high = max(rows[i]["high"] for i in range(consol_start, trigger_idx + 1))
                    consol_low = min(rows[i]["low"] for i in range(consol_start, trigger_idx + 1))
                    rango = consol_high - consol_low
                    atr_cur = cur.get("atr") or 0.0
                    if atr_cur == 0 or rango > self.consol_max_atr_mult * atr_cur:
                        continue
                    if min(rows[i]["low"] for i in range(consol_start, trigger_idx + 1)) <= neckline:
                        continue
                    # all filters passed; emit signal
                    entry_price = consol_high + _TICK
                    setup_ts = cur["time"]
                    valid_until = setup_ts + timedelta(days=20)
                    anchors = {
                        "L1": L1, "L2": L2, "neckline": neckline,
                        "altura_patron": altura, "sma18": cur["sma"],
                        "atr14": atr_cur, "consol_low": consol_low,
                    }
                    signals.append(Signal(
                        symbol=symbol, strategy=self.name, side="long",
                        setup_ts=setup_ts, entry_type="stop",
                        entry_price=entry_price,
                        valid_until=valid_until,
                        stop=0.0, tp1=None, tp2=None,
                        timestop_bars=20,
                        indicator_anchors=anchors,
                    ))
                    break  # one signal per (L1, L2) pair
        return signals
