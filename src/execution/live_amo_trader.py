"""Live AMO8 Trader Engine — Kha0sys3 parallel ORB runner.

Magic 8338. Lives ALONGSIDE the MATH bot (magic 1338) on the same VPS,
account, and Telegram — but in an isolated process and file footprint.

Responsibilities:
  - Load the AMO8 portfolio from bot_config_amo8.json (V1: 75 configs,
    modes ATR + OR_FIXED only).
  - Build a "schedule" indexed by (broker_sym, magic_time, or_duration).
    Each entry holds the list of strategies that share that OR window.
  - Every 30 seconds:
      * For each (sym, magic_time, or_duration) currently in its post-OR
        active window (max 8h after OR close), fetch the last few M1 bars
        for that symbol and run pattern detection on the latest closed M1.
      * If a pattern fires AND a strategy in that slot matches AND no
        dedup conflict for today → AmoOrderManager.place_market().
  - Heartbeat to Telegram every 15 minutes prefixed "[AMO8]".
  - Sweep max-hold every 60s.
  - DRY_RUN default: never sends real orders.

NEVER reads/writes MATH (1338) state — every MT5 query filters by
magic=MAGIC_NUMBER_AMO8.
"""
from __future__ import annotations

import bisect
import json
import threading
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import numpy as np
import polars as pl

from src.application.calculators import DataEnricher
from src.application.orb_edge_metrics import mfe_mae_walk  # noqa: F401 (used in tests)
from src.application.orb_patterns import (
    add_state_columns,
    detect_events_for_day,
)
from src.application.orb_utils import to_us_utc  # noqa: F401
from src.execution.amo_order_manager import (
    AmoOrderManager,
    MAGIC_NUMBER_AMO8,
)
from src.execution.mt5_client import MT5Client

try:
    import MetaTrader5 as mt5  # type: ignore
except Exception:  # pragma: no cover
    mt5 = None  # type: ignore


# Build a pattern-id parser locally (same logic as build_bot_config_amo8.py)
_EVENTS = [
    "FALSE_BREAK_UP", "FALSE_BREAK_DOWN",
    "BREAK_UP", "BREAK_DOWN",
    "MITIG_PD_MID", "MITIG_PD_CLOSE",
    "REENTRY_PD_OR_HIGH", "REENTRY_PD_OR_LOW",
]


class AmoTraderEngine:
    """Live engine that fires AMO8 ORB strategies."""

    POLL_INTERVAL = 30                    # secs between detection passes
    HEARTBEAT_INTERVAL = 15 * 60          # 15 min
    SWEEP_INTERVAL = 60                   # 60s — max-hold check
    M1_LOOKBACK_BARS = 600                # ~10h M1 — covers any 8h post-OR window
    M15_LOOKBACK_BARS = 800               # for OR computation (PD context)
    POST_OR_ACTIVE_HOURS = 8              # listen window after OR close

    def __init__(self, config_path: str = "src/execution/bot_config_amo8.json",
                 dry_run: bool = True):
        cfg_path = Path(config_path)
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)

        self.cfg = cfg
        self.portfolio = cfg["portfolio"]
        self.risk_per_trade = float(cfg.get("risk_per_trade", 0.001))
        self.dry_run = dry_run

        # Build schedule: { (broker_sym, magic_time, or_duration_min): [strategies] }
        self.schedule: dict[tuple, list[dict]] = {}
        for s in self.portfolio:
            k = (s["broker_sym"], s["magic_time"], int(s["or_duration_min"]))
            self.schedule.setdefault(k, []).append(s)

        # Strategies grouped by symbol for fast M1/M15 fetch dedup
        self.symbols: set[str] = {s["broker_sym"] for s in self.portfolio}

        # MT5 client + order manager + telegram
        self.client = MT5Client(attach_only=True)
        self.telegram = None
        try:
            from src.monitoring.telegram_notifier import TelegramNotifier
            self.telegram = TelegramNotifier()
        except Exception as e:
            print(f"[AMO8] Telegram init skipped: {e}")
        self.orders = AmoOrderManager(dry_run=self.dry_run, telegram=self.telegram)

        # Cooldown: don't reprocess the same OR-window/bar within POLL_INTERVAL
        # key=(broker_sym, magic_time, or_duration_min, m1_bar_ts_iso)
        self._processed: dict[tuple, bool] = {}
        # Last heartbeat / sweep timestamps
        self._last_heartbeat = 0.0
        self._last_sweep = 0.0
        self._stop = False

    # ───────────────────────── Lifecycle ─────────────────────────

    def start(self) -> None:
        print(f"[AMO8] ENGINE STARTED  magic={MAGIC_NUMBER_AMO8}  "
              f"dry_run={self.dry_run}  configs={len(self.portfolio)}  "
              f"symbols={len(self.symbols)}  unique_slots={len(self.schedule)}")
        if self.telegram is not None:
            try:
                self.telegram._send(
                    f"[AMO8] ENGINE STARTED\n"
                    f"magic: {MAGIC_NUMBER_AMO8}\n"
                    f"dry_run: {self.dry_run}\n"
                    f"configs: {len(self.portfolio)}\n"
                    f"unique slots: {len(self.schedule)}\n"
                    f"avg PF expected: "
                    f"{self.cfg['_metrics_aggregate']['avg_pf_weighted']}\n"
                    f"sum trades/yr expected: "
                    f"{self.cfg['_metrics_aggregate']['sum_trades_per_year']}"
                )
            except Exception:
                pass

        # Ensure MT5 connection
        if mt5 is not None:
            ok = self.client.ensure_connected()
            if not ok:
                print("[AMO8] MT5 connection failed; running DRY without ticks")

        # Main loop
        while not self._stop:
            try:
                self._tick()
            except KeyboardInterrupt:
                self._stop = True
                break
            except Exception as e:
                print(f"[AMO8] tick error: {e}")
            time.sleep(self.POLL_INTERVAL)

    def stop(self) -> None:
        self._stop = True

    # ───────────────────────── Main tick ─────────────────────────

    def _tick(self) -> None:
        now = datetime.now(timezone.utc)

        # Heartbeat
        if (time.time() - self._last_heartbeat) > self.HEARTBEAT_INTERVAL:
            self._emit_heartbeat(now)
            self._last_heartbeat = time.time()

        # Periodic max-hold sweep + partial-exit tick for DOC/SWING positions
        if (time.time() - self._last_sweep) > self.SWEEP_INTERVAL:
            closed = self.orders.sweep_max_hold()
            if closed > 0:
                print(f"[AMO8] sweep closed {closed} positions over max_hold")
            self._partial_exit_tick(now)
            self._last_sweep = time.time()

        # Active slots: those whose OR closed in the last POST_OR_ACTIVE_HOURS hours
        active = self._active_slots(now)
        if not active:
            return

        # Per-symbol M1 + M15 cache for this tick (refetched each tick)
        m1_cache: dict[str, pl.DataFrame] = {}
        m15_cache: dict[str, pl.DataFrame] = {}

        for (broker_sym, magic_time, or_dur), strategies in active.items():
            m1 = m1_cache.get(broker_sym)
            if m1 is None:
                m1 = self._fetch_bars(broker_sym, "M1", self.M1_LOOKBACK_BARS)
                if m1 is None or m1.is_empty():
                    continue
                m1_cache[broker_sym] = m1
            m15 = m15_cache.get(broker_sym)
            if m15 is None:
                m15 = self._fetch_bars(broker_sym, "M15", self.M15_LOOKBACK_BARS)
                if m15 is None or m15.is_empty():
                    continue
                m15_cache[broker_sym] = m15

            self._process_slot(broker_sym, magic_time, or_dur, strategies, m1, m15, now)

    def _active_slots(self, now: datetime) -> dict[tuple, list[dict]]:
        """Return slots whose OR window has closed and we're still within
        POST_OR_ACTIVE_HOURS hours of that close."""
        out: dict[tuple, list[dict]] = {}
        for (sym, mt_str, or_dur), strats in self.schedule.items():
            or_close = self._or_close_time(now, mt_str, or_dur)
            if or_close is None:
                continue
            age_min = (now - or_close).total_seconds() / 60
            if 0 <= age_min <= self.POST_OR_ACTIVE_HOURS * 60:
                out[(sym, mt_str, or_dur)] = strats
        return out

    def _or_close_time(self, now: datetime, magic_time: str, or_dur: int) -> Optional[datetime]:
        """Compute today's OR close UTC datetime (today's date + magic_time + or_dur).

        Note: magic_time is stored in broker hours but K3M1 convention treats
        broker time as UTC for time-window alignment (see live_math_trader
        notes). So we use 'now' UTC date directly.
        """
        hh, mm = magic_time.split(":")
        or_start_today = now.replace(
            hour=int(hh), minute=int(mm), second=0, microsecond=0
        )
        # OR closes at start + duration minutes
        or_close = or_start_today + timedelta(minutes=or_dur)
        # If OR close hasn't happened yet today, we have no active window today
        if or_close > now:
            return None
        return or_close

    # ───────────────────────── Per-slot processing ─────────────────────────

    def _process_slot(
        self,
        broker_sym: str,
        magic_time: str,
        or_dur: int,
        strategies: list[dict],
        m1: pl.DataFrame,
        m15: pl.DataFrame,
        now: datetime,
    ) -> None:
        """For one (sym, magic_time, or_duration) slot, detect ORB events on
        the latest M1 bar and place orders for matching strategies."""
        # Compute OR + PD context on M15
        try:
            enriched_m15 = DataEnricher.enrich_with_daily_context(m15, "00:00", "23:59")
            enriched_or = DataEnricher.enrich_with_opening_range(
                enriched_m15, magic_time, or_dur
            )
            enriched_or = add_state_columns(enriched_or)
        except Exception as e:
            print(f"[AMO8] enrich error {broker_sym} {magic_time}/{or_dur}: {e}")
            return

        # Find today's row
        today = now.date()
        today_rows = enriched_or.filter(
            (pl.col("trade_date") == today) & (pl.col("is_post_or"))
        ).sort("time")
        if today_rows.is_empty():
            return
        row0 = today_rows.row(0, named=True)
        # Required fields
        for k in ("or_high", "or_low", "atr_14"):
            if row0.get(k) is None:
                return

        or_close_ts = row0["time"]
        or_high = float(row0["or_high"])
        or_low = float(row0["or_low"])
        or_width = or_high - or_low
        if or_width <= 0:
            return
        atr_at_setup = float(row0["atr_14"])
        if atr_at_setup <= 0:
            return

        # Build M1 slice from or_close_ts to now (today only)
        m1_sorted = m1.sort("time")
        m1_times = m1_sorted["time"].to_list()
        if not m1_times:
            return
        start_idx = bisect.bisect_right(m1_times, or_close_ts)
        # End: last M1 bar (current bar may still be forming; use closed bars)
        last_closed_ts = now.replace(second=0, microsecond=0) - timedelta(minutes=1)
        end_idx = bisect.bisect_right(m1_times, last_closed_ts)
        if end_idx <= start_idx:
            return

        # Cooldown: don't reprocess if we already saw this last bar timestamp
        cooldown_key = (broker_sym, magic_time, or_dur, m1_times[end_idx - 1].isoformat())
        if cooldown_key in self._processed:
            return
        self._processed[cooldown_key] = True
        # Trim cooldown cache to last 1000 entries
        if len(self._processed) > 1000:
            self._processed.clear()

        day_slice = {
            "times": np.array(m1_times[start_idx:end_idx], dtype="object"),
            "highs": np.asarray(
                m1_sorted["high"].to_list()[start_idx:end_idx], dtype=float
            ),
            "lows": np.asarray(
                m1_sorted["low"].to_list()[start_idx:end_idx], dtype=float
            ),
            "closes": np.asarray(
                m1_sorted["close"].to_list()[start_idx:end_idx], dtype=float
            ),
        }

        events = detect_events_for_day(
            or_close_ts=or_close_ts,
            or_high=or_high, or_low=or_low,
            pd_mid=row0.get("pd_mid"), pd_close=row0.get("pd_close"),
            pd_or_high=row0.get("pd_or_high"), pd_or_low=row0.get("pd_or_low"),
            atr_at_setup=atr_at_setup, m1=day_slice,
        )
        if not events:
            return

        # Get account balance for sizing
        balance = self._get_balance()
        if balance is None or balance <= 0:
            print("[AMO8] no balance available, skip placement")
            return

        # For each event: build pattern_id, find matching strategies, place
        or_position = row0.get("or_position_vs_pd") or "NULL"
        or_atr_bucket = row0.get("or_atr_bucket") or "NULL"
        pd_or_bucket = row0.get("pd_or_overlap_bucket") or "NULL"
        for ev in events:
            event_type = ev["event_type"]
            pattern_id = f"{event_type}_{or_position}_{or_atr_bucket}_{pd_or_bucket}"
            entry_price = float(ev["trigger_close"])
            # Match strategies on this slot with same pattern_id
            for strategy in strategies:
                if strategy["pattern_id"] != pattern_id:
                    continue
                if self.orders.has_fired_today(
                    strategy["internal_sym"], pattern_id, strategy["direction"]
                ):
                    continue
                mode = strategy["exit_rules"]["mode"]
                if mode in ("DOC", "SWING"):
                    self.orders.place_partial(
                        strategy=strategy,
                        entry_price=entry_price,
                        atr_at_setup=atr_at_setup,
                        or_width=or_width,
                        risk_per_trade=self.risk_per_trade,
                        account_balance=balance,
                    )
                else:  # ATR or OR_FIXED
                    self.orders.place_market(
                        strategy=strategy,
                        entry_price=entry_price,
                        atr_at_setup=atr_at_setup,
                        or_width=or_width,
                        risk_per_trade=self.risk_per_trade,
                        account_balance=balance,
                    )

    # ───────────────────────── MT5 helpers ─────────────────────────

    def _fetch_bars(self, broker_sym: str, tf: str, count: int) -> Optional[pl.DataFrame]:
        if mt5 is None:
            return None
        try:
            tf_const = {
                "M1": mt5.TIMEFRAME_M1,
                "M15": mt5.TIMEFRAME_M15,
                "H1": mt5.TIMEFRAME_H1,
            }[tf]
            rates = mt5.copy_rates_from_pos(broker_sym, tf_const, 0, count)
            if rates is None or len(rates) == 0:
                return None
            # broker time treated as UTC (matches K3M1 + backtest convention)
            df = pl.DataFrame({
                "time": [datetime.fromtimestamp(int(r["time"]), tz=timezone.utc)
                         for r in rates],
                "open": [float(r["open"]) for r in rates],
                "high": [float(r["high"]) for r in rates],
                "low": [float(r["low"]) for r in rates],
                "close": [float(r["close"]) for r in rates],
            }).with_columns([
                pl.col("time").dt.replace_time_zone(None),
                pl.col("time").dt.date().alias("trade_date"),
            ])
            return df
        except Exception as e:
            print(f"[AMO8] fetch bars error {broker_sym}/{tf}: {e}")
            return None

    def _partial_exit_tick(self, now: datetime) -> None:
        """Build bars_by_symbol snapshot from live MT5 ticks + last M1 close
        for every symbol that currently has a DOC/SWING partial position open,
        then delegate to AmoOrderManager.partial_exit_tick."""
        positions = getattr(self.orders, "state_positions", {})
        if not positions:
            return
        symbols_needed = {pos.broker_sym for pos in positions.values()
                          if pos.remaining_volume > 0}
        if not symbols_needed:
            return
        bars_by_symbol: dict[str, dict] = {}
        for sym in symbols_needed:
            data = self._fetch_partial_snapshot(sym)
            if data is None:
                continue
            bars_by_symbol[sym] = data
        if bars_by_symbol:
            self.orders.partial_exit_tick(bars_by_symbol)

    def _fetch_partial_snapshot(self, broker_sym: str) -> Optional[dict]:
        """Return {bid, ask, m1_high, m1_low, m1_close} for one symbol.

        Falls back gracefully if MT5 is unavailable.
        """
        if mt5 is None:
            return None
        try:
            tick = mt5.symbol_info_tick(broker_sym)
            if tick is None:
                return None
            # Last closed M1 bar (count=2 to ensure we get a fully-closed one)
            rates = mt5.copy_rates_from_pos(broker_sym, mt5.TIMEFRAME_M1, 1, 1)
            if rates is None or len(rates) == 0:
                # Fallback: use bid/ask for high/low/close
                mid = (float(tick.bid) + float(tick.ask)) / 2
                return {"bid": float(tick.bid), "ask": float(tick.ask),
                        "m1_high": float(tick.ask), "m1_low": float(tick.bid),
                        "m1_close": mid}
            r = rates[0]
            return {
                "bid": float(tick.bid),
                "ask": float(tick.ask),
                "m1_high": float(r["high"]),
                "m1_low": float(r["low"]),
                "m1_close": float(r["close"]),
            }
        except Exception as e:
            print(f"[AMO8] partial snapshot error {broker_sym}: {e}")
            return None

    def _get_balance(self) -> Optional[float]:
        if mt5 is None:
            return 10000.0  # DRY default for sizing math
        try:
            info = mt5.account_info()
            if info is None:
                return None
            return float(info.balance)
        except Exception:
            return None

    # ───────────────────────── Telegram heartbeat ─────────────────────────

    def _emit_heartbeat(self, now: datetime) -> None:
        try:
            bal = self._get_balance()
            equity = bal
            n_pos = 0
            if mt5 is not None:
                try:
                    positions = mt5.positions_get() or []
                    n_pos = sum(
                        1 for p in positions
                        if int(getattr(p, "magic", 0)) == MAGIC_NUMBER_AMO8
                    )
                    info = mt5.account_info()
                    if info is not None:
                        equity = float(info.equity)
                except Exception:
                    pass
            msg = (
                f"[AMO8] HEARTBEAT  {now.isoformat(timespec='seconds')}\n"
                f"magic: {MAGIC_NUMBER_AMO8}\n"
                f"balance: {bal}\n"
                f"equity: {equity}\n"
                f"open positions: {n_pos}\n"
                f"active slots: {len(self._active_slots(now))}/{len(self.schedule)}"
            )
            print(msg)
            if self.telegram is not None:
                self.telegram._send(msg)
        except Exception as e:
            print(f"[AMO8] heartbeat error: {e}")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="src/execution/bot_config_amo8.json")
    p.add_argument("--live", action="store_true",
                   help="Disable DRY (will send real orders)")
    args = p.parse_args()
    engine = AmoTraderEngine(config_path=args.config, dry_run=not args.live)
    engine.start()
