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
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import polars as pl

from src.execution.mt5_client import MT5Client
from src.execution.math_order_manager import MathOrderManager
from src.execution.risk_manager import DynamicRiskAllocator, BalanceTieredRiskAllocator
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

    POLL_INTERVAL = 10                  # seconds between loop iterations
    HEARTBEAT_INTERVAL = 900            # 15 min
    M15_SECONDS = 15 * 60
    RECONNECT_CHECK_INTERVAL = 60       # secs — ensure_connected cadence
    SL_GUARDIAN_INTERVAL = 10           # secs
    HEALTH_CHECK_INTERVAL = 300         # 5 min
    SWEEP_STALE_INTERVAL = 3600         # 1 hour

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

        # Risk allocator: prefer balance-tiered if present in config, else flat.
        rs = cfg.get("risk_scaling", {})
        min_wr = float(rs.get("min_wr", MATH_WR_MIN))
        max_wr = float(rs.get("max_wr", MATH_WR_MAX))
        if "tiers" in rs:
            self.risk = BalanceTieredRiskAllocator(
                tiers=rs["tiers"], min_wr=min_wr, max_wr=max_wr,
            )
            print(f"[MATH] Risk: balance-tiered {len(rs['tiers'])} tiers, WR range {min_wr:.2f}-{max_wr:.2f}")
        else:
            self.risk = DynamicRiskAllocator(
                min_risk=float(rs.get("min_risk", MATH_RISK_MIN_PCT)),
                max_risk=float(rs.get("max_risk", MATH_RISK_MAX_PCT)),
                min_wr=min_wr, max_wr=max_wr,
            )

        self.om = MathOrderManager(
            client=self.client, magic=MAGIC_NUMBER_MATH,
            dry_run=dry_run, telegram=self.telegram,
            risk_allocator=self.risk,
        )

        self._start_time: Optional[float] = None
        self._last_heartbeat: float = 0.0
        self._last_m15_processed: Optional[datetime] = None
        self._last_reconnect_check: float = 0.0
        self._last_sl_check: float = 0.0
        self._last_health_check: float = 0.0
        self._last_sweep: float = 0.0

        # Thread-safe pause flag (for /math_stop /math_resume)
        self._paused = False
        self._pause_lock = threading.Lock()

        # Health monitor (optional — tolerate missing deps in dev)
        self._health = None
        try:
            from src.monitoring.system_health import SystemHealthMonitor
            self._health = SystemHealthMonitor()
        except Exception as e:
            print(f"[MATH] SystemHealthMonitor init skipped: {e}")

    # ------- pause API -------
    def pause(self):
        with self._pause_lock:
            self._paused = True
        self._tg("engine PAUSED (no new placements)")

    def resume(self):
        with self._pause_lock:
            self._paused = False
        self._tg("engine RESUMED")

    def is_paused(self) -> bool:
        with self._pause_lock:
            return self._paused

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

    @staticmethod
    def _is_h1_close(now: datetime, tol_sec: int = 30) -> bool:
        """True within `tol_sec` after an H1 boundary (HH:00)."""
        sec_offset = now.minute * 60 + now.second
        return sec_offset <= tol_sec

    @staticmethod
    def _is_h4_close(now: datetime, tol_sec: int = 30) -> bool:
        """True within `tol_sec` after an H4 boundary (00,04,08,12,16,20 broker hour)."""
        if now.hour % 4 != 0:
            return False
        sec_offset = now.minute * 60 + now.second
        return sec_offset <= tol_sec

    @staticmethod
    def _bar_key_for_tf(now: datetime, tf: str) -> datetime:
        """Returns the truncated time stamping the most recent bar boundary."""
        if tf == "M15":
            return now.replace(second=0, microsecond=0,
                               minute=(now.minute // 15) * 15)
        if tf == "H1":
            return now.replace(second=0, microsecond=0, minute=0)
        if tf == "H4":
            return now.replace(second=0, microsecond=0, minute=0,
                               hour=(now.hour // 4) * 4)
        return now.replace(second=0, microsecond=0)

    def _is_tf_close(self, now: datetime, tf: str, tol_sec: int = 30) -> bool:
        if tf == "M15":
            return self._is_m15_close(now, tol_sec)
        if tf == "H1":
            return self._is_h1_close(now, tol_sec)
        if tf == "H4":
            return self._is_h4_close(now, tol_sec)
        return False

    def _compute_server_offset(self) -> int:
        """Detect MT5 server time vs real UTC offset in seconds.

        MT5 returns bar/tick timestamps as epoch seconds interpreted in server
        local time (not real UTC). Vantage server is EEST (UTC+3) most of the
        year. If we naively convert with timezone.utc we get +3h skew which
        breaks session-hour filters.
        """
        if mt5 is None:
            return 0
        try:
            t = mt5.symbol_info_tick("EURUSD+")
            if t is None:
                return 0
            # time.time() is real UTC epoch; t.time is server "as-UTC" epoch
            import time as _t
            offset = int(t.time) - int(_t.time())
            # Round to nearest hour (MT5 servers are whole-hour offsets)
            hours = round(offset / 3600)
            return hours * 3600
        except Exception as e:
            print(f"[MATH] server offset detect failed: {e}")
            return 0

    def _fetch_bars(self, broker_sym: str, tf: str = "M15",
                    count: int = MATH_BARS_LOOKBACK) -> Optional[pl.DataFrame]:
        if mt5 is None:
            return None
        try:
            tf_const = {
                "M15": mt5.TIMEFRAME_M15,
                "H1":  mt5.TIMEFRAME_H1,
                "H4":  mt5.TIMEFRAME_H4,
            }.get(tf, mt5.TIMEFRAME_M15)
            rates = mt5.copy_rates_from_pos(broker_sym, tf_const, 0, count)
            if rates is None or len(rates) == 0:
                return None
            # IMPORTANT: do NOT subtract server offset.
            # The backtest cache (CSV) stores broker server time as if UTC.
            # Sessions in bot_config_math.json are configured in BROKER hours
            # (matching backtest semantics: ASIA=0-7 broker = real UTC 21-04).
            # Live MT5 also returns broker-time-as-Unix-ts; treating it as UTC
            # keeps live==backtest alignment exact.
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

    def _session_active_now(self, session: str) -> bool:
        """True if the setup's session is open AT THE BROKER's current hour.

        Critical: backtest interprets sessions in BROKER server time (the CSV
        cache stores broker-time-as-UTC). Live must check 'is broker hour in
        session window?', NOT real UTC hour. For Vantage EEST, broker hour =
        real UTC hour + 3.
        """
        real_utc_h = datetime.now(timezone.utc).hour
        offset_h = getattr(self, "_server_offset_sec", 0) // 3600
        broker_h = (real_utc_h + offset_h) % 24
        start_h, end_h = INDICATOR_SESSIONS[session]
        return start_h <= broker_h < end_h

    def _process_setup(self, s: dict):
        sym = s["sym"]
        sess = s["session"]
        tf = s.get("tf", "M15")
        # Hard guard: only process during the setup's session window (real UTC)
        if not self._session_active_now(sess):
            return
        bars = self._fetch_bars(sym, tf=tf)
        if bars is None or len(bars) < 100:
            return
        bars = self._enrich(bars)
        scoped = _filter_by_session(bars, sess)
        if len(scoped) == 0:
            return
        # Order: guard → virtual sim (DRY only) → detect_and_place on newest.
        try:
            self.om.tick_pending(s, scoped)
        except Exception as e:
            print(f"[MATH] tick_pending {sym}/{s['setup_type']}: {e}")
        try:
            self.om.tick_virtual(s, scoped)
        except Exception as e:
            print(f"[MATH] tick_virtual {sym}/{s['setup_type']}: {e}")
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

        # Account snapshot
        bal = eq = free = 0.0
        n_pos = 0
        pnl_d = 0.0
        if mt5 is not None:
            try:
                a = mt5.account_info()
                if a is not None:
                    bal = float(a.balance); eq = float(a.equity); free = float(a.margin_free)
                positions = mt5.positions_get() or []
                math_pos = [p for p in positions if p.magic == MAGIC_NUMBER_MATH]
                n_pos = len(math_pos)
                pnl_d = sum(float(p.profit) for p in math_pos)
            except Exception:
                pass

        from collections import Counter as _Cnt
        tf_dist = _Cnt(s.get("tf", "M15") for s in self.setups)
        tf_line = " ".join(f"{k}:{v}" for k, v in tf_dist.most_common())
        msg = (
            f"HEARTBEAT\n"
            f"Uptime:   {uptime_h:.1f}h\n"
            f"Setups:   {len(self.setups)} ({tf_line})\n"
            f"Pending:  {len(self.om._pending)}\n"
            f"Open pos: {n_pos} (floating P&L ${pnl_d:+.2f})\n"
            f"Balance:  ${bal:.2f}\n"
            f"Equity:   ${eq:.2f}\n"
            f"Free:     ${free:.2f}"
        )
        if self.dry_run:
            trades = self.om.read_dry_trades()
            today = self.om._today_utc()
            todays = [t for t in trades if (t.get("exit_time") or "").startswith(today)]
            msg += (
                f"\nDRY today: n={len(todays)} "
                f"netR={sum(t.get('r_multiple', 0.0) for t in todays):+.2f}"
            )
        self._tg(msg)

    def _maybe_emit_daily_report(self):
        """Fire the DRY daily report at 23:55 UTC (once per day)."""
        if not self.dry_run:
            return
        utc = self._utc_now()
        if not (utc.hour == 23 and utc.minute >= 55):
            return
        key = utc.strftime("%Y-%m-%d")
        if getattr(self, "_last_report_day", None) == key:
            return
        try:
            self.om.emit_daily_report()
            self._last_report_day = key
        except Exception as e:
            print(f"[MATH] daily report error: {e}")

    def run(self):
        """Main loop. Polls every POLL_INTERVAL; acts on M15 boundaries."""
        if not self.client.connect():
            print("[MATH] MT5 connect failed.")
            self._tg("ENGINE FATAL\nMT5 connect failed\nEngine exiting")
            return

        self._start_time = time.time()
        self._last_heartbeat = self._start_time

        # Detect MT5 server-time offset (CRITICAL for session filters to work)
        self._server_offset_sec = self._compute_server_offset()
        off_h = self._server_offset_sec / 3600
        print(f"[MATH] MT5 server offset vs real UTC: {off_h:+.0f}h "
              f"(bars in broker time = backtest cache; sessions in broker hour)")
        if abs(off_h) >= 1:
            # Warn if offset is non-zero so operator knows sessions are now corrected
            pass

        n = len(self.setups)
        syms = sorted({s["sym"] for s in self.setups})

        # Startup Telegram — account snapshot + setup labels
        try:
            acct = None
            if mt5 is not None:
                acct = mt5.account_info()
            bal = float(getattr(acct, "balance", 0.0)) if acct else 0.0
            eq = float(getattr(acct, "equity", 0.0)) if acct else 0.0
            mg = float(getattr(acct, "margin_free", 0.0)) if acct else 0.0
            # Symbol summary compact
            from collections import Counter
            sym_counter = Counter(s["sym"] for s in self.setups)
            setup_counter = Counter(s["setup_type"] for s in self.setups)
            dir_counter = Counter(s.get("direction_mode", "INVERT") for s in self.setups)
            tf_counter = Counter(s.get("tf", "M15") for s in self.setups)
            syms_line = ", ".join(f"{k}({v})" for k, v in sym_counter.most_common())
            setups_line = ", ".join(f"{k}({v})" for k, v in setup_counter.most_common())
            dirs_line = ", ".join(f"{k}({v})" for k, v in dir_counter.most_common())
            tfs_line = ", ".join(f"{k}({v})" for k, v in tf_counter.most_common())
            avg_wr = (sum(s.get("expected_wr", 0) for s in self.setups) / max(n, 1))

            mode = "LIVE" if not self.dry_run else "DRY_RUN"
            off_h = self._server_offset_sec / 3600
            self._tg(
                f"ENGINE STARTED ({mode}) - ELITE WR>=65%\n"
                f"Magic:      {MAGIC_NUMBER_MATH}\n"
                f"Setups:     {n}\n"
                f"Timeframes: {tfs_line}\n"
                f"Avg WR:     {avg_wr:.1%}\n"
                f"Symbols:    {len(sym_counter)} -> {syms_line}\n"
                f"Setup mix:  {setups_line}\n"
                f"Direction:  {dirs_line}\n"
                f"MT5 offset: {off_h:+.0f}h (server -> real UTC)\n"
                f"Risk:       balance-tiered 1-15% / 1-8% / 0.5-5% / 0.3-3%\n"
                f"Balance:    ${bal:.2f}\n"
                f"Equity:     ${eq:.2f}\n"
                f"Free:       ${mg:.2f}"
            )
        except Exception as e:
            print(f"[MATH] startup TG error: {e}")
            self._tg(
                f"ENGINE STARTED (fallback)\n"
                f"Magic:   {MAGIC_NUMBER_MATH}\n"
                f"Setups:  {n}\n"
                f"Symbols: {len(syms)}\n"
                f"Dry run: {self.dry_run}"
            )

        print(f"[MATH] Engine started ({n} setups, dry_run={self.dry_run})")

        try:
            while True:
                now = self._utc_now()
                nowt = time.time()

                # Ensure MT5 connected (every RECONNECT_CHECK_INTERVAL)
                if nowt - self._last_reconnect_check >= self.RECONNECT_CHECK_INTERVAL:
                    self._last_reconnect_check = nowt
                    try:
                        if not self.client.ensure_connected():
                            self._tg("MT5 RECONNECT FAILED\nSkipping this pass")
                            time.sleep(self.POLL_INTERVAL)
                            continue
                    except Exception as e:
                        print(f"[MATH] ensure_connected err: {e}")

                # SL Guardian every 10s
                if nowt - self._last_sl_check >= self.SL_GUARDIAN_INTERVAL:
                    self._last_sl_check = nowt
                    try:
                        self.om.check_sl_guardian()
                    except Exception as e:
                        print(f"[MATH] SLG error: {e}")

                # LIVE event detection (fills + closes) — every poll in LIVE
                if not self.dry_run:
                    try:
                        self.om.detect_live_events()
                    except Exception as e:
                        print(f"[MATH] detect_live_events err: {e}")

                # Hourly stale sweep
                if nowt - self._last_sweep >= self.SWEEP_STALE_INTERVAL:
                    self._last_sweep = nowt
                    try:
                        self.om.sweep_stale()
                    except Exception as e:
                        print(f"[MATH] sweep_stale error: {e}")

                # Health monitor
                if (self._health is not None
                        and nowt - self._last_health_check >= self.HEALTH_CHECK_INTERVAL):
                    self._last_health_check = nowt
                    try:
                        alerts = self._health.get_critical_alerts()
                        if alerts:
                            self._tg("HEALTH ALERT\n" + "\n".join(alerts))
                    except Exception as e:
                        print(f"[MATH] health check err: {e}")

                # No forced session-end cleanup — let TP/SL/expiration play
                # exactly as in backtest. The only session enforcement is
                # at PLACEMENT (via _session_active_now in _process_setup).

                # Multi-TF dispatch: process each TF only at its own bar close.
                # Setups grouped by tf field (M15/H1/H4); each TF has its own
                # last-processed bar key so we never double-process.
                if not hasattr(self, "_last_tf_processed"):
                    self._last_tf_processed = {}
                if self.is_paused():
                    pass
                else:
                    for tf in ("M15", "H1", "H4"):
                        if not self._is_tf_close(now, tf):
                            continue
                        bar_key = self._bar_key_for_tf(now, tf)
                        if self._last_tf_processed.get(tf) == bar_key:
                            continue
                        self._last_tf_processed[tf] = bar_key
                        self.om.reset_daily_if_needed()
                        tf_setups = [s for s in self.setups if s.get("tf", "M15") == tf]
                        if not tf_setups:
                            continue
                        print(f"[MATH] {tf} close — processing {len(tf_setups)} setups")
                        for s in tf_setups:
                            try:
                                self._process_setup(s)
                            except Exception as e:
                                print(f"[MATH] process {s.get('sym')}/{tf}: {e}")
                        self.om.sweep_expired()

                self._heartbeat()
                self._maybe_emit_daily_report()

                Path("logs").mkdir(exist_ok=True)
                Path("logs/math_bot_heartbeat").touch()

                time.sleep(self.POLL_INTERVAL)

        except KeyboardInterrupt:
            self._tg("ENGINE STOPPED\nReason: KeyboardInterrupt")
            print("[MATH] Stopped.")
        finally:
            try:
                self.client.disconnect()
            except Exception:
                pass


if __name__ == "__main__":
    MathTraderEngine(dry_run=True).run()
