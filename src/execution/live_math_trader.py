"""
Live MATH Trader Engine — Kha0sys3 parallel runner
Magic 1338. Lives ALONGSIDE the FADE bot (magic 1337) on the same VPS, account,
and Telegram bot, but in an isolated process.

Responsibilities:
  - Load 17 MATH_INV_MOMENTUM strategies from bot_config_math.json
  - Every M15 bar close (HH:00, :15, :30, :45 UTC): for each strategy,
    * fetch the last ~500 M15 bars from MT5,
    * enrich with MathIndicatorEnricher,
    * slice to the session window,
    * call MathOrderManager.tick_pending (direction guard),
    * call MathOrderManager.detect_and_place (new signals on the newest bar).
  - Heartbeat to Telegram every 15 minutes, prefixed "[MATH]".
  - DRY_RUN default: never calls mt5.order_send; prints & telegrams only.

NEVER reads or writes FADE orders — every MT5 query filters by magic=1338.
"""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import polars as pl

from src.execution.mt5_client import MT5Client
from src.execution.math_order_manager import MathOrderManager
from src.execution.risk_manager import DynamicRiskAllocator
from src.domain.constants import (
    MATH_RISK_MIN_PCT, MATH_RISK_MAX_PCT, MATH_WR_MIN, MATH_WR_MAX,
)
from src.application.math_indicators import MathIndicatorEnricher
from src.domain.constants import (
    MAGIC_NUMBER_MATH, MATH_BARS_LOOKBACK, INDICATOR_SESSIONS,
)

try:
    import MetaTrader5 as mt5  # type: ignore
except Exception:  # pragma: no cover
    mt5 = None  # type: ignore


def _filter_by_session(bars: pl.DataFrame, session: str) -> pl.DataFrame:
    start_h, end_h = INDICATOR_SESSIONS[session]
    return bars.filter(
        (pl.col("time").dt.hour() >= start_h) & (pl.col("time").dt.hour() < end_h)
    )


def _add_atr(bars: pl.DataFrame, period: int = 14) -> pl.DataFrame:
    """Wilder ATR via EWM alpha=1/period (matches enriched cache pipeline)."""
    if "atr_14" in bars.columns:
        return bars
    return bars.with_columns(
        pl.max_horizontal(
            pl.col("high") - pl.col("low"),
            (pl.col("high") - pl.col("close").shift(1)).abs(),
            (pl.col("low") - pl.col("close").shift(1)).abs(),
        ).alias("_tr")
    ).with_columns(
        pl.col("_tr").ewm_mean(alpha=1 / period, adjust=False,
                                min_periods=period).alias(f"atr_{period}")
    ).drop("_tr")


class MathTraderEngine:

    POLL_INTERVAL = 60                  # seconds between loop iterations
    HEARTBEAT_INTERVAL = 900            # 15 min
    M15_SECONDS = 15 * 60

    def __init__(self, config_path: str = "src/execution/bot_config_math.json",
                 dry_run: bool = True):
        cfg_path = Path(config_path)
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)

        self.setups = cfg.get("portfolio", [])
        self.dry_run = dry_run

        self.client = MT5Client()

        # Telegram: optional, tolerate missing credentials in dev/test
        self.telegram = None
        try:
            from src.monitoring.telegram_notifier import TelegramNotifier
            self.telegram = TelegramNotifier()
        except Exception as e:
            print(f"[MATH] Telegram init skipped: {e}")

        # Math-specific risk allocator: 1% @ WR 0.57 → 15% @ WR 1.00 (linear).
        self.risk = DynamicRiskAllocator(
            min_risk=MATH_RISK_MIN_PCT, max_risk=MATH_RISK_MAX_PCT,
            min_wr=MATH_WR_MIN, max_wr=MATH_WR_MAX,
        )

        self.om = MathOrderManager(
            client=self.client, magic=MAGIC_NUMBER_MATH,
            dry_run=dry_run, telegram=self.telegram,
            risk_allocator=self.risk,
        )

        self._start_time: Optional[float] = None
        self._last_heartbeat: float = 0.0
        self._last_m15_processed: Optional[datetime] = None

    # ─── helpers ────────────────────────────────────────────────

    def _tg(self, msg: str):
        if self.telegram is None:
            return
        tag = "[MATH][DRY] " if self.dry_run else "[MATH] "
        try:
            # telegram_notifier exposes _send/_broadcast
            if hasattr(self.telegram, "_broadcast"):
                self.telegram._broadcast(tag + msg)
            elif hasattr(self.telegram, "send_sync"):
                self.telegram.send_sync(tag + msg)
        except Exception as e:
            print(f"[MATH][TG] error: {e}")

    @staticmethod
    def _utc_now() -> datetime:
        return datetime.now(timezone.utc)

    @staticmethod
    def _is_m15_close(now: datetime, tol_sec: int = 30) -> bool:
        """True within `tol_sec` after an M15 boundary (HH:00, :15, :30, :45)."""
        mins_since_hour = now.minute
        sec_offset = (mins_since_hour % 15) * 60 + now.second
        return sec_offset <= tol_sec

    def _fetch_bars(self, broker_sym: str, count: int = MATH_BARS_LOOKBACK) -> Optional[pl.DataFrame]:
        if mt5 is None:
            return None
        try:
            rates = mt5.copy_rates_from_pos(broker_sym, mt5.TIMEFRAME_M15, 0, count)
            if rates is None or len(rates) == 0:
                return None
            df = pl.DataFrame({
                "time": [datetime.fromtimestamp(int(r["time"]), tz=timezone.utc)
                         for r in rates],
                "open": [float(r["open"]) for r in rates],
                "high": [float(r["high"]) for r in rates],
                "low":  [float(r["low"])  for r in rates],
                "close":[float(r["close"])for r in rates],
            })
            return df.sort("time")
        except Exception as e:
            print(f"[MATH] fetch_bars {broker_sym}: {e}")
            return None

    def _enrich(self, bars: pl.DataFrame) -> pl.DataFrame:
        bars = _add_atr(bars, 14)
        return MathIndicatorEnricher.enrich_all_math(bars)

    # ─── main loop ──────────────────────────────────────────────

    def _process_setup(self, s: dict):
        sym = s["sym"]
        bars = self._fetch_bars(sym)
        if bars is None or len(bars) < 100:
            return
        bars = self._enrich(bars)
        sess = s["session"]
        scoped = _filter_by_session(bars, sess)
        if len(scoped) == 0:
            return
        # Direction guard first (on currently pending), then detect_and_place.
        try:
            self.om.tick_pending(s, scoped)
        except Exception as e:
            print(f"[MATH] tick_pending {sym}/{s['setup_type']}: {e}")
        try:
            self.om.detect_and_place(s, scoped)
        except Exception as e:
            print(f"[MATH] detect_and_place {sym}/{s['setup_type']}: {e}")

    def _heartbeat(self):
        now = time.time()
        if now - self._last_heartbeat < self.HEARTBEAT_INTERVAL:
            return
        self._last_heartbeat = now
        uptime_h = (now - (self._start_time or now)) / 3600.0
        self._tg(f"heartbeat uptime={uptime_h:.1f}h setups={len(self.setups)} "
                 f"pending={len(self.om._pending)}")

    def run(self):
        """Main loop. Polls every POLL_INTERVAL; acts on M15 boundaries."""
        if not self.client.connect():
            print("[MATH] MT5 connect failed.")
            self._tg("MT5 connect failed — MATH engine exiting")
            return

        self._start_time = time.time()
        self._last_heartbeat = self._start_time

        n = len(self.setups)
        syms = sorted({s["sym"] for s in self.setups})
        self._tg(
            f"MATH engine started | setups={n} symbols={len(syms)} "
            f"magic={MAGIC_NUMBER_MATH} dry_run={self.dry_run}"
        )
        print(f"[MATH] Engine started ({n} setups, dry_run={self.dry_run})")

        try:
            while True:
                now = self._utc_now()

                # Process only once per M15 bar close
                bar_key = now.replace(second=0, microsecond=0,
                                      minute=(now.minute // 15) * 15)
                if self._is_m15_close(now) and bar_key != self._last_m15_processed:
                    self._last_m15_processed = bar_key
                    self.om.reset_daily_if_needed()
                    for s in self.setups:
                        try:
                            self._process_setup(s)
                        except Exception as e:
                            print(f"[MATH] process {s.get('sym')}: {e}")
                    self.om.sweep_expired()

                self._heartbeat()

                Path("logs").mkdir(exist_ok=True)
                Path("logs/math_bot_heartbeat").touch()

                time.sleep(self.POLL_INTERVAL)

        except KeyboardInterrupt:
            self._tg("MATH engine stopped (KeyboardInterrupt)")
            print("[MATH] Stopped.")
        finally:
            try:
                self.client.disconnect()
            except Exception:
                pass


if __name__ == "__main__":
    MathTraderEngine(dry_run=True).run()
