"""
Math Order Manager — Kha0sys3 parallel MATH runner
Magic 1338 — isolated from FADE (magic 1337).

Responsibilities:
  - detect_and_place: given enriched M15 bars, run the setup's detector on the
    LAST bar, and if fires today with no existing pending/open for this
    (symbol, setup_type) pair today, place a STOP order in the FLIPPED direction
    (INVERTED portfolio) at close +/- 0.5 * ATR, with expiration at +5 bars.
  - tick_pending: re-evaluate the direction guard on each pending MATH order;
    cancel if the ORIGINAL setup's guard indicator weakens
    (|guard| < 0.5 * |guard_at_placement|) or flips sign.
  - has_pending_or_open_today: dedup gate.

DRY_RUN=True (default): never calls mt5.order_send / orders_get mutations —
only logs "[DRY] would place STOP ..." and broadcasts to Telegram prefixed
with "[MATH][DRY]". A parallel in-memory pending-store is used so tick_pending
and dedup behave correctly during the DRY observation window.

IMPORTANT: Every MT5 read filters by magic=MAGIC_NUMBER_MATH so this manager
never touches or observes FADE state.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import polars as pl

from src.domain.constants import (
    MAGIC_NUMBER_MATH,
    MATH_WAIT_BARS,
    MATH_STOP_ATR_OFFSET,
    MATH_GUARD_WEAKEN_THRESHOLD,
)
from src.engine.run_math_momentum import detect_setups, _guard_indicator_col

try:
    import MetaTrader5 as mt5  # type: ignore
except Exception:  # pragma: no cover - allow tests without MT5 installed
    mt5 = None  # type: ignore


# Retcodes we handle gracefully (skip, no crash)
_RETCODE_INVALID_PRICE = 10015
_RETCODE_INVALID_STOPS = 10016
_RETCODE_MARKET_CLOSED = 10018
_RETCODE_INVALID_EXPIRATION = 10022
_RETCODE_INVALID_FILL = 10030
_SPREAD_MULT_LIMIT = 2.5      # current spread vs typical
_STALE_STOP_MIN = 90          # minutes after which an idle STOP is nuked
_TICK_MAX_AGE_SEC = 120       # tick freshness gate: skip if last tick > 2 min old
                              # (weekend / market closed / feed stalled)
_STOPS_BUFFER_POINTS = 1      # extra points beyond broker's stops_level when
                              # validating that stop_price is far enough from bid/ask


# Setup-type → original direction source column (for live direction guard)
# (delegates to the already-validated mapping in run_math_momentum)


# ── Comment formatting (single source of truth for placement + sweeps) ──
# Stable, collision-free abbreviations. Keep total comment <= 31 chars
# (MT5 limit). Format: "M|<TF>|<SETUP_TAG>|<SESSION_TAG>".
SETUP_TAG = {
    "KAMA_CROSS_MOM":      "KAMA",
    "SPECTRAL_TREND_MOM":  "SPECTRAL",
    "VELOCITY_ACCEL_GO":   "VELOCITY",
    "KALMAN_INNOV_EXPAND": "KALMAN",
    "HURST_TREND_MOM":     "HURST",
    "OLS_SLOPE_STRONG":    "OLS",
    "GARCH_Z_FADE":        "GARCH",
}
SESSION_TAG = {
    "ASIA":      "ASIA",
    "LONDON":    "LDN",
    "NY":        "NY",
    "LONDON_NY": "LDNNY",
    "ALL_DAY":   "ALLDAY",
}


def make_order_comment(tf: str, setup_type: str, session: str) -> str:
    """Build the MT5 order comment used for both placement and sweep matching.

    Single source of truth: every call to mt5.order_send and every comment
    lookup (dedup, session-end cancel, SLG, time-stop) routes through this
    helper, so format drifts cannot cause silent mismatches.
    """
    setup_tag = SETUP_TAG.get(setup_type, setup_type[:8])
    session_tag = SESSION_TAG.get(session, session[:6])
    return f"M|{tf}|{setup_tag}|{session_tag}"


def _flip(direction: str) -> str:
    """Invert LONG↔SHORT (INVERTED portfolio semantics)."""
    return "SHORT" if direction == "LONG" else "LONG"


@dataclass
class PendingMathOrder:
    ticket: int                 # -1 in DRY_RUN
    symbol: str                 # broker symbol (sym)
    internal_sym: str
    setup_type: str
    session: str = ""
    original_direction: str = "LONG"     # LONG/SHORT per detector
    flipped_direction: str = "LONG"      # what we actually placed
    stop_price: float = 0.0
    tp_price: float = 0.0
    sl_price: float = 0.0
    atr: float = 0.0
    guard_value_at_placement: float = 0.0
    expiration_utc: Optional[datetime] = None
    placed_date: str = ""            # YYYY-MM-DD UTC
    dry_run: bool = True
    # Virtual-simulation fields (DRY only; ignored in LIVE)
    virt_state: str = "PENDING"      # PENDING | FILLED | CLOSED
    virt_entry_price: Optional[float] = None
    virt_entry_time: Optional[datetime] = None


class MathOrderManager:
    """Manages STOP orders for the MATH parallel runner (magic 1338)."""

    def __init__(self, client, magic: int = MAGIC_NUMBER_MATH,
                 dry_run: bool = True, telegram=None, risk_allocator=None):
        self.client = client
        self.magic = magic
        self.dry_run = dry_run
        self.telegram = telegram
        self.risk = risk_allocator  # DynamicRiskAllocator instance or None

        # In-memory pending registry (source of truth in DRY, shadow in LIVE)
        self._pending: dict[str, PendingMathOrder] = {}
        # Dedup: (symbol, setup_type) → date string
        self._fired_today: dict[tuple[str, str], str] = {}
        # DRY virtual trade log (append-only JSONL)
        self._dry_trades_path = Path("data/live_state/math_dry_trades.jsonl")
        self._dry_trades_path.parent.mkdir(parents=True, exist_ok=True)

    # ─── Telegram helpers ─────────────────────────────────────────

    def _tg(self, msg: str):
        if self.telegram is None:
            return
        tag = "[MATH][DRY] " if self.dry_run else "[MATH] "
        try:
            if hasattr(self.telegram, "send_sync"):
                self.telegram.send_sync(tag + msg)
            elif hasattr(self.telegram, "_broadcast"):
                self.telegram._broadcast(tag + msg)
        except Exception as e:
            print(f"[MATH][TG] notify error: {e}")

    # ─── Dedup (1 trade per (sym, setup_type) per day) ────────────

    @staticmethod
    def _today_utc() -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")

    def has_pending_or_open_today(self, symbol: str, setup_type: str) -> bool:
        """True if we already placed / filled a MATH order for this pair today."""
        today = self._today_utc()
        if self._fired_today.get((symbol, setup_type)) == today:
            return True
        # Also check any live pending registered for this pair today
        for p in self._pending.values():
            if (p.symbol == symbol and p.setup_type == setup_type
                    and p.placed_date == today):
                return True
        # In LIVE mode, also sweep MT5 for magic=1338 orders/positions.
        # Match on the SETUP_TAG token between the second and third pipe of
        # the comment ("M|<TF>|<SETUP_TAG>|<SESSION_TAG>") to avoid false
        # positives (e.g. KAMA token matching inside another setup).
        setup_tag = SETUP_TAG.get(setup_type, setup_type[:8])
        target_token = f"|{setup_tag}|"
        if not self.dry_run and mt5 is not None:
            try:
                orders = mt5.orders_get(symbol=symbol) or []
                for o in orders:
                    if getattr(o, "magic", 0) == self.magic \
                            and target_token in (o.comment or ""):
                        return True
                positions = mt5.positions_get(symbol=symbol) or []
                for p in positions:
                    if getattr(p, "magic", 0) == self.magic \
                            and target_token in (p.comment or ""):
                        return True
            except Exception:
                pass
        return False

    def _mark_fired(self, symbol: str, setup_type: str):
        self._fired_today[(symbol, setup_type)] = self._today_utc()

    # ─── Core placement ──────────────────────────────────────────

    def detect_and_place(self, setup_cfg: dict, bars: pl.DataFrame) -> Optional[PendingMathOrder]:
        """Run detector on `bars` (already math-enriched + session-filtered);
        if the LATEST bar fires and dedup allows, place an INVERTED STOP.

        Returns the PendingMathOrder record if placed, else None.
        """
        symbol = setup_cfg["sym"]
        internal = setup_cfg.get("internal_sym", symbol)
        setup_type = setup_cfg["setup_type"]

        if self.has_pending_or_open_today(symbol, setup_type):
            return None

        if bars is None or len(bars) == 0:
            return None

        try:
            sigs = detect_setups(bars, setup_type)
        except Exception as e:
            print(f"[MATH] detect_setups error {symbol}/{setup_type}: {e}")
            return None

        if len(sigs) == 0:
            return None

        # Only act on the most recent fired bar (last closed M15 bar)
        last_bar_time = bars["time"].max()
        latest = sigs.filter(pl.col("time") == last_bar_time)
        if len(latest) == 0:
            return None

        row = latest.row(-1, named=True)
        atr = row["atr_14"]
        if atr is None or atr <= 0:
            return None
        close = row["close"]
        orig_dir = row["direction"]
        guard_value = row["guard_value"]
        if guard_value is None:
            return None

        # Direction mode: INVERT flips (default for historical FADE_INV setups).
        # NORMAL uses the detector's direction as-is (for NORMAL-family setups
        # like GARCH_Z_FADE that already encode the trade direction correctly).
        dir_mode = setup_cfg.get("direction_mode", "INVERT")
        if dir_mode == "NORMAL":
            flipped = orig_dir
        else:
            flipped = _flip(orig_dir)

        # STOP placement = close +/- 0.5*ATR in the FLIPPED direction
        if flipped == "LONG":
            stop_price = close + MATH_STOP_ATR_OFFSET * atr
            tp_price = stop_price + setup_cfg["tp_atr_mult"] * atr
            sl_price = stop_price - setup_cfg["sl_atr_mult"] * atr
            order_type = "BUY_STOP"
        else:
            stop_price = close - MATH_STOP_ATR_OFFSET * atr
            tp_price = stop_price - setup_cfg["tp_atr_mult"] * atr
            sl_price = stop_price + setup_cfg["sl_atr_mult"] * atr
            order_type = "SELL_STOP"

        # Early price normalization to symbol digits (so logs/pending/submit match)
        digits = 5  # fallback
        if mt5 is not None:
            try:
                _si = mt5.symbol_info(symbol)
                if _si is not None:
                    digits = int(getattr(_si, "digits", 5))
            except Exception:
                pass
        stop_price = round(stop_price, digits)
        tp_price = round(tp_price, digits)
        sl_price = round(sl_price, digits)
        _fmt = f".{digits}f"

        # Pre-submit guards — silently skip when the broker would reject the
        # order anyway, to avoid log/Telegram spam during market-closed and
        # weekend-spread periods.
        if not self._is_market_tradable(symbol, order_type, stop_price):
            return None

        # Expiration: 5 M15 bars = 75 minutes
        expiration = datetime.now(timezone.utc) + timedelta(minutes=15 * MATH_WAIT_BARS)

        ticket = self._submit_stop(
            symbol=symbol, order_type=order_type, stop_price=stop_price,
            sl=sl_price, tp=tp_price, setup_type=setup_type,
            session=setup_cfg["session"], expiration=expiration,
            expected_wr=float(setup_cfg.get("expected_wr", 0.60)),
            tf=setup_cfg.get("tf", "M15"),
        )
        if ticket is None:
            return None

        pending = PendingMathOrder(
            ticket=ticket, symbol=symbol, internal_sym=internal,
            setup_type=setup_type, session=setup_cfg.get("session", ""),
            original_direction=orig_dir, flipped_direction=flipped,
            stop_price=stop_price, tp_price=tp_price, sl_price=sl_price,
            atr=atr, guard_value_at_placement=float(guard_value),
            expiration_utc=expiration, placed_date=self._today_utc(),
            dry_run=self.dry_run,
        )
        key = f"{symbol}|{setup_type}|{self._today_utc()}"
        self._pending[key] = pending
        self._mark_fired(symbol, setup_type)

        # Structured multi-line Telegram message (no emojis)
        expected_wr = float(setup_cfg.get("expected_wr", 0.60))
        risk_pct = 0.0
        if self.risk is not None:
            try:
                # Balance-tiered takes (wr, balance); classic takes (wr) only
                bal = getattr(self, "_last_balance", 0.0)
                try:
                    risk_pct = float(self.risk.get_risk_percent(expected_wr, bal))
                except TypeError:
                    risk_pct = float(self.risk.get_risk_percent(expected_wr))
            except Exception:
                pass
        tf = setup_cfg.get("tf", "M15")
        rr = setup_cfg.get("rr", 0)
        tg_msg = (
            f"ORDER PLACED\n"
            f"Symbol:    {symbol}\n"
            f"TF:        {tf}\n"
            f"Type:      {order_type}\n"
            f"Direction: {flipped} ({dir_mode})\n"
            f"Setup:     {setup_type}\n"
            f"Session:   {setup_cfg.get('session', '-')}\n"
            f"Entry:     {stop_price:{_fmt}}\n"
            f"TP:        {tp_price:{_fmt}}\n"
            f"SL:        {sl_price:{_fmt}}\n"
            f"R:R:       {rr:.2f}\n"
            f"ATR:       {atr:.5f}\n"
            f"Risk:      {risk_pct*100:.1f}% (WR={expected_wr:.2f})\n"
            f"Ticket:    {ticket if ticket != -1 else 'DRY'}"
        )
        # Console log stays compact (one line for grep)
        print(f"[MATH]{'[DRY]' if self.dry_run else ''} {order_type} {symbol} "
              f"@ {stop_price:{_fmt}} TP={tp_price:{_fmt}} SL={sl_price:{_fmt}} "
              f"setup={setup_type}/{dir_mode} risk={risk_pct*100:.1f}%")
        self._tg(tg_msg)
        return pending

    def _compute_volume(self, sym_info, entry: float, sl: float,
                        expected_wr: float) -> float:
        """Balance-based position sizing via DynamicRiskAllocator."""
        lot_min = float(getattr(sym_info, "volume_min", 0.01))
        if self.risk is None or mt5 is None:
            return lot_min  # fallback when allocator not wired

        acct = mt5.account_info()
        if acct is None or getattr(acct, "balance", 0) <= 0:
            return lot_min

        volume_step = float(getattr(sym_info, "volume_step", lot_min))
        tick_size = float(getattr(sym_info, "trade_tick_size",
                                  getattr(sym_info, "point", 0.0)))
        tick_value = float(getattr(sym_info, "trade_tick_value", 0.0))
        if tick_size <= 0 or tick_value <= 0:
            return lot_min

        lots = self.risk.calculate_lots(
            account_balance=float(acct.balance),
            entry_price=entry, sl_price=sl,
            tick_value=tick_value, tick_size=tick_size,
            volume_step=volume_step, win_rate=expected_wr,
        )
        # Cache balance for subsequent get_risk_percent display in log
        self._last_balance = float(acct.balance)
        return max(lots, lot_min)

    def _submit_stop(self, symbol: str, order_type: str, stop_price: float,
                     sl: float, tp: float, setup_type: str, session: str,
                     expiration: datetime, expected_wr: float = 0.60,
                     tf: str = "M15") -> Optional[int]:
        """Send STOP to MT5 unless DRY_RUN. Returns ticket (or -1 in DRY).

        Sizing: uses DynamicRiskAllocator (math-tuned: 1% @ WR 0.57 → 15% @ WR 1.00)
        with the setup's expected_wr to dimension lots against balance.
        """
        if self.dry_run:
            return -1

        if mt5 is None:
            print("[MATH] mt5 not available -- treating as DRY")
            return -1

        # Spread gate (hard guard)
        if not self._spread_ok(symbol):
            self._tg(
                f"SPREAD GATE BLOCK\n"
                f"Symbol:  {symbol}\n"
                f"Setup:   {setup_type}\n"
                f"Reason:  current spread > 2.5x typical (skip)"
            )
            return None

        try:
            sym_info = mt5.symbol_info(symbol)
            if sym_info is None:
                print(f"[MATH] symbol_info None for {symbol}")
                return None

            # Risk-based sizing using balance (not free_margin) and setup WR
            volume = self._compute_volume(sym_info, stop_price, sl, expected_wr)
            if volume <= 0:
                print(f"[MATH] computed volume=0 for {symbol}, skipping")
                return None

            # Risk-sizing log line (ASCII-safe for NSSM cp1252 stdout)
            try:
                risk_pct = 0.0
                if self.risk is not None:
                    risk_pct = float(self.risk.get_risk_percent(expected_wr))
                print(
                    f"[MATH] {symbol} place risk={risk_pct*100:.1f}% "
                    f"lots={volume:.2f} (WR={expected_wr:.2f})"
                )
            except Exception:
                pass

            type_map = {
                "BUY_STOP": mt5.ORDER_TYPE_BUY_STOP,
                "SELL_STOP": mt5.ORDER_TYPE_SELL_STOP,
            }

            # --- Price normalization to symbol digits ---
            digits = int(getattr(sym_info, "digits", 5))
            price_n = round(float(stop_price), digits)
            sl_n = round(float(sl), digits)
            tp_n = round(float(tp), digits)

            # --- Stops-level validation (broker minimum distance) ---
            tick = mt5.symbol_info_tick(symbol)
            point = float(getattr(sym_info, "point", 10 ** -digits))
            stops_level_pts = int(getattr(sym_info, "trade_stops_level", 0) or 0)
            min_dist = stops_level_pts * point
            buffer = max(min_dist * 1.5, 2 * point)  # 50% safety buffer, min 2 points
            if tick is not None and stops_level_pts > 0:
                ref_bid = float(tick.bid)
                ref_ask = float(tick.ask)
                if order_type == "BUY_STOP":
                    # BUY_STOP must be above ask by >= stops_level
                    if price_n - ref_ask < min_dist:
                        price_n = round(ref_ask + buffer, digits)
                        tp_n = round(price_n + (tp_n - stop_price), digits)
                        sl_n = round(price_n - (stop_price - sl_n), digits)
                        print(f"[MATH] {symbol} STOP bumped above ask by stops_level: {price_n}")
                elif order_type == "SELL_STOP":
                    # SELL_STOP must be below bid by >= stops_level
                    if ref_bid - price_n < min_dist:
                        price_n = round(ref_bid - buffer, digits)
                        tp_n = round(price_n - (stop_price - tp_n), digits)
                        sl_n = round(price_n + (sl_n - stop_price), digits)
                        print(f"[MATH] {symbol} STOP bumped below bid by stops_level: {price_n}")

            # Volume normalization to volume_step
            vstep = float(getattr(sym_info, "volume_step", 0.01))
            volume = round(round(volume / vstep) * vstep, 2)
            vmin = float(getattr(sym_info, "volume_min", 0.01))
            vmax = float(getattr(sym_info, "volume_max", 100.0))
            volume = max(vmin, min(vmax, volume))

            req = {
                "action": mt5.TRADE_ACTION_PENDING,
                "symbol": symbol,
                "volume": volume,
                "type": type_map[order_type],
                "price": price_n,
                "sl": sl_n,
                "tp": tp_n,
                "deviation": 10,
                "magic": self.magic,
                "comment": make_order_comment(tf, setup_type, session),
                # GTC + manual cancellation via sweep_stale (broker may reject
                # ORDER_TIME_SPECIFIED <24h on ECN → retcode 10022).
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_RETURN,
            }
            try:
                res = mt5.order_send(req)
            except Exception as e:
                print(f"[MATH] order_send raised: {e}")
                self._tg(f"ORDER SEND EXCEPTION\nSymbol: {symbol}\nSetup:  {setup_type}\nError:  {e}")
                return None
            if res is None:
                last_err = mt5.last_error() if hasattr(mt5, "last_error") else "?"
                print(f"[MATH] order_send None: {last_err}")
                self._tg(f"ORDER SEND NULL RESPONSE\nSymbol: {symbol}\nSetup:  {setup_type}\nError:  {last_err}")
                return None
            rc = int(getattr(res, "retcode", -1))
            done_code = getattr(mt5, "TRADE_RETCODE_DONE", 10009)
            if rc == done_code:
                return int(res.order)
            if rc == _RETCODE_INVALID_PRICE:
                # Pre-submit guard usually catches these now; if one slips
                # through (race vs tick refresh), log throttled, no Telegram.
                self._market_skip_log(
                    symbol,
                    f"broker_invalid_price p={price_n} stops={stops_level_pts}pt"
                )
                return None
            if rc == _RETCODE_INVALID_STOPS:
                self._market_skip_log(
                    symbol,
                    f"broker_invalid_stops tp={tp_n} sl={sl_n} stops={stops_level_pts}pt"
                )
                return None
            if rc == _RETCODE_INVALID_EXPIRATION:
                # Broker may still reject GTC for this account; try DAY as last resort
                print(f"[MATH] {symbol} invalid expiration (10022) -- retrying ORDER_TIME_DAY")
                req["type_time"] = mt5.ORDER_TIME_DAY
                try:
                    res2 = mt5.order_send(req)
                    if res2 is not None and int(getattr(res2, "retcode", -1)) == done_code:
                        return int(res2.order)
                    print(f"[MATH] {symbol} retry retcode={getattr(res2,'retcode','?')}")
                except Exception as e:
                    print(f"[MATH] {symbol} retry EXC: {e}")
                self._tg(f"INVALID EXPIRATION (retcode 10022)\nSymbol: {symbol}\nSetup:  {setup_type}\nRetry:  ORDER_TIME_DAY failed (skipped)")
                return None
            if rc == _RETCODE_INVALID_FILL:
                # Try alternate filling modes
                for fm_name, fm in (("FOK", getattr(mt5, "ORDER_FILLING_FOK", None)),
                                    ("IOC", getattr(mt5, "ORDER_FILLING_IOC", None))):
                    if fm is None:
                        continue
                    req["type_filling"] = fm
                    try:
                        res3 = mt5.order_send(req)
                        if res3 is not None and int(getattr(res3, "retcode", -1)) == done_code:
                            print(f"[MATH] {symbol} filled with {fm_name}")
                            return int(res3.order)
                    except Exception:
                        pass
                self._tg(f"INVALID FILL MODE (retcode 10030)\nSymbol: {symbol}\nSetup:  {setup_type}\nRetry:  FOK/IOC failed (skipped)")
                return None
            if rc == _RETCODE_MARKET_CLOSED:
                self._market_skip_log(symbol, "broker_market_closed")
                return None
            # Other non-done: loud
            print(f"[MATH] order_send retcode={rc} req={req}")
            self._tg(f"ORDER REJECT (retcode {rc})\nSymbol: {symbol}\nSetup:  {setup_type}\n(skipped)")
            return None
        except Exception as e:
            print(f"[MATH] _submit_stop error: {e}")
            self._tg(f"_submit_stop EXC {symbol} {setup_type}: {e}")
            return None

    # ------- pre-submit market guard -------

    def _is_market_tradable(self, symbol: str, order_type: str,
                            stop_price: float) -> bool:
        """Pre-submit guard for STOP placement. Returns False when the broker
        would reject the order with INVALID_PRICE/MARKET_CLOSED, so we skip
        quietly instead of generating retcode-noise during weekends or
        market-closed windows.

        Three checks:
          1. Tick freshness — last tick newer than _TICK_MAX_AGE_SEC.
            Stale tick => market closed or feed stalled => skip.
          2. trade_mode — symbol must be FULL (4). Anything else (DISABLED,
            CLOSE_ONLY, etc) => skip.
          3. Stop price vs bid/ask + stops_level — BUY_STOP must be at least
            stops_level_points + buffer above ask; SELL_STOP must be at least
            below bid. Anything inside the spread is rejected by the broker
            with retcode 10015.

        Throttled logging: prints one warning per (symbol, reason) per 5 min
        so the log stays useful instead of drowning in identical lines.
        """
        if mt5 is None:
            return True
        try:
            info = mt5.symbol_info(symbol)
            if info is None:
                return False
            tick = mt5.symbol_info_tick(symbol)
            if tick is None or int(getattr(tick, "time", 0)) == 0:
                self._market_skip_log(symbol, "no_tick")
                return False

            now_ts = int(datetime.now(timezone.utc).timestamp())
            srv_off = int(getattr(self, "_server_offset_sec", 0))
            tick_age = now_ts - (int(tick.time) - srv_off)
            if tick_age > _TICK_MAX_AGE_SEC:
                self._market_skip_log(symbol, f"stale_tick_age={tick_age}s")
                return False

            # 4 = SYMBOL_TRADE_MODE_FULL
            if int(getattr(info, "trade_mode", 4)) != 4:
                self._market_skip_log(symbol, f"trade_mode={info.trade_mode}")
                return False

            point = float(getattr(info, "point", 0.0) or 0.0)
            if point <= 0:
                return True  # cannot validate — let broker decide
            stops_pts = int(getattr(info, "trade_stops_level", 0) or 0)
            buffer = (stops_pts + _STOPS_BUFFER_POINTS) * point
            bid = float(tick.bid)
            ask = float(tick.ask)

            if order_type == "BUY_STOP":
                # Must be strictly above ask + buffer
                if stop_price < ask + buffer:
                    self._market_skip_log(
                        symbol,
                        f"buy_stop_inside_spread p={stop_price} ask={ask} "
                        f"buf={buffer:.{int(info.digits)}f}"
                    )
                    return False
            elif order_type == "SELL_STOP":
                # Must be strictly below bid - buffer
                if stop_price > bid - buffer:
                    self._market_skip_log(
                        symbol,
                        f"sell_stop_inside_spread p={stop_price} bid={bid} "
                        f"buf={buffer:.{int(info.digits)}f}"
                    )
                    return False

            return True
        except Exception as e:
            print(f"[MATH] _is_market_tradable {symbol}: {e}")
            return True  # fail-open: let broker reject if we can't tell

    def _market_skip_log(self, symbol: str, reason: str,
                          throttle_sec: int = 300) -> None:
        """Print a skip line at most once per (symbol, reason_kind) per
        throttle_sec to avoid drowning the log."""
        if not hasattr(self, "_skip_log_seen"):
            self._skip_log_seen: dict[tuple, float] = {}
        kind = reason.split(" ", 1)[0]  # collapse 'p=...' detail
        key = (symbol, kind)
        now = datetime.now(timezone.utc).timestamp()
        last = self._skip_log_seen.get(key, 0.0)
        if now - last >= throttle_sec:
            print(f"[MATH] {symbol} skip placement: {reason}")
            self._skip_log_seen[key] = now

    # ------- spread gate -------

    def _spread_ok(self, symbol: str) -> bool:
        """Block placement if current spread > _SPREAD_MULT_LIMIT * typical.

        'typical' = broker-reported spread (symbol_info.spread, points) EWMA'd
        across calls. Falls back to allowing trade when info unavailable.
        """
        if mt5 is None:
            return True
        try:
            info = mt5.symbol_info(symbol)
            if info is None:
                return True
            cur = float(getattr(info, "spread", 0.0) or 0.0)
            if cur <= 0:
                return True
            if not hasattr(self, "_typical_spread"):
                self._typical_spread: dict[str, float] = {}
            typ = self._typical_spread.get(symbol)
            if typ is None or typ <= 0:
                self._typical_spread[symbol] = cur
                return True
            # EWMA so typical drifts slowly
            self._typical_spread[symbol] = 0.9 * typ + 0.1 * cur
            ok = cur <= _SPREAD_MULT_LIMIT * typ
            if not ok:
                print(f"[MATH] spread gate {symbol}: cur={cur} typ={typ:.1f}"
                      f" (>{_SPREAD_MULT_LIMIT}x)")
            return ok
        except Exception:
            return True

    # ------- stale order sweep (hourly) -------

    def sweep_stale(self) -> int:
        """Cancel STOP orders older than _STALE_STOP_MIN minutes (magic filter).
        Returns number cancelled. LIVE only; DRY returns 0.
        """
        if self.dry_run or mt5 is None:
            return 0
        try:
            orders = mt5.orders_get() or []
        except Exception as e:
            print(f"[MATH] sweep_stale orders_get error: {e}")
            return 0
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(minutes=_STALE_STOP_MIN)
        cancelled = 0
        for o in orders:
            try:
                if getattr(o, "magic", 0) != self.magic:
                    continue
                ts = int(getattr(o, "time_setup", 0) or 0)
                if ts <= 0:
                    continue
                setup_at = datetime.fromtimestamp(ts, tz=timezone.utc)
                if setup_at >= cutoff:
                    continue
                req = {
                    "action": mt5.TRADE_ACTION_REMOVE,
                    "order": int(o.ticket),
                    "symbol": o.symbol,
                }
                res = mt5.order_send(req)
                if res is not None and getattr(res, "retcode", -1) == mt5.TRADE_RETCODE_DONE:
                    cancelled += 1
            except Exception as e:
                print(f"[MATH] sweep_stale iter error: {e}")
        if cancelled > 0:
            self._tg(f"STALE SWEEP\nCancelled: {cancelled} STOP orders\nAge limit: {_STALE_STOP_MIN} minutes")
            print(f"[MATH] sweep_stale cancelled={cancelled}")
        return cancelled

    # ------- SL Guardian (MATH-scoped) -------

    def check_sl_guardian(self) -> int:
        """Close positions (magic=1338) whose price has moved beyond SL.
        Returns number of positions closed. LIVE only.
        """
        if self.dry_run or mt5 is None:
            return 0
        try:
            positions = mt5.positions_get() or []
        except Exception as e:
            print(f"[MATH] SLGuardian positions_get error: {e}")
            return 0
        closed = 0
        for p in positions:
            try:
                if getattr(p, "magic", 0) != self.magic:
                    continue
                sl = float(getattr(p, "sl", 0.0) or 0.0)
                if sl == 0.0:
                    continue
                price = float(getattr(p, "price_current", 0.0) or 0.0)
                ptype = int(getattr(p, "type", -1))
                breached = False
                if ptype == 0 and price <= sl:       # BUY
                    breached = True
                elif ptype == 1 and price >= sl:     # SELL
                    breached = True
                if not breached:
                    continue
                # Close at market
                tick = mt5.symbol_info_tick(p.symbol)
                if tick is None:
                    continue
                close_price = tick.bid if ptype == 0 else tick.ask
                order_type = mt5.ORDER_TYPE_SELL if ptype == 0 else mt5.ORDER_TYPE_BUY
                req = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": p.symbol,
                    "volume": float(p.volume),
                    "type": order_type,
                    "position": int(p.ticket),
                    "price": float(close_price),
                    "deviation": 20,
                    "magic": self.magic,
                    "comment": "SLG_MATH",
                    "type_filling": mt5.ORDER_FILLING_IOC,
                }
                res = mt5.order_send(req)
                if res is not None and getattr(res, "retcode", -1) == mt5.TRADE_RETCODE_DONE:
                    closed += 1
                    self._tg(f"SL GUARDIAN CLOSE\nSymbol: {p.symbol}\nTicket: {p.ticket}\nReason: price crossed SL without broker close\nAction: closed at market")
                    print(f"[MATH][SLG] closed {p.symbol} ticket={p.ticket}")
            except Exception as e:
                print(f"[MATH][SLG] iter error: {e}")
        return closed

    # ─── Session-end cleanup ─────────────────────────────────────

    def session_end_cleanup(self, all_setups: list[dict]) -> tuple[int, int]:
        """Cancel pending STOPs and close open positions whose setup's session
        has ENDED (real UTC). This enforces the backtest's session_end_hour
        time-stop in live trading.

        Returns (cancelled_count, closed_count).
        """
        if self.dry_run or mt5 is None:
            return (0, 0)

        from src.domain.constants import INDICATOR_SESSIONS
        h_now = datetime.now(timezone.utc).hour

        # Build map: full comment ("M|<TF>|<SETUP_TAG>|<SESSION_TAG>") ->
        # (session, end_hour). Uses the same helper as placement to guarantee
        # an exact match against MT5 comments.
        end_h_by_comment = {}
        for s in all_setups:
            sess = s.get("session", "")
            if sess not in INDICATOR_SESSIONS:
                continue
            end_h = INDICATOR_SESSIONS[sess][1]
            tf = s.get("tf", "M15")
            comment_key = make_order_comment(tf, s["setup_type"], sess)
            end_h_by_comment[comment_key] = (sess, end_h)

        cancelled = 0
        closed = 0

        # 1) Cancel pending STOPs whose session has ended
        try:
            orders = mt5.orders_get() or []
        except Exception:
            orders = []
        for o in orders:
            if getattr(o, "magic", 0) != self.magic:
                continue
            comment = str(getattr(o, "comment", ""))
            info = end_h_by_comment.get(comment)
            if info is None:
                continue
            sess, end_h = info
            # Session has ended for this comment if h_now is at/past end_h
            # OR before session start (next day). Only cancel if outside window.
            start_h = INDICATOR_SESSIONS[sess][0]
            if start_h <= h_now < end_h:
                continue  # session still active, leave pending alive
            # Outside session: cancel
            try:
                req = {"action": mt5.TRADE_ACTION_REMOVE, "order": o.ticket}
                r = mt5.order_send(req)
                if r and getattr(r, "retcode", 0) == mt5.TRADE_RETCODE_DONE:
                    cancelled += 1
                    print(f"[MATH] session-end cancel pending {o.symbol} ticket={o.ticket} (sess={sess})")
                    self._tg(f"SESSION-END CANCEL\nSymbol: {o.symbol}\nSession: {sess} (ended)\nTicket:  {o.ticket}")
            except Exception as e:
                print(f"[MATH] session cancel err: {e}")

        # 2) Close open positions whose session has ended
        try:
            positions = mt5.positions_get() or []
        except Exception:
            positions = []
        for p in positions:
            if getattr(p, "magic", 0) != self.magic:
                continue
            comment = str(getattr(p, "comment", ""))
            info = end_h_by_comment.get(comment)
            if info is None:
                continue
            sess, end_h = info
            start_h = INDICATOR_SESSIONS[sess][0]
            if start_h <= h_now < end_h:
                continue  # still in session, leave open
            # Outside session: close at market (matches backtest TIME_STOP)
            try:
                tick = mt5.symbol_info_tick(p.symbol)
                if tick is None:
                    continue
                ptype = int(getattr(p, "type", -1))
                # opposite of position type
                close_type = mt5.ORDER_TYPE_SELL if ptype == 0 else mt5.ORDER_TYPE_BUY
                price = float(tick.bid if ptype == 0 else tick.ask)
                req = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "position": p.ticket,
                    "symbol": p.symbol,
                    "volume": float(p.volume),
                    "type": close_type,
                    "price": price,
                    "deviation": 20,
                    "magic": self.magic,
                    "comment": "M|TIME_STOP",
                    "type_filling": mt5.ORDER_FILLING_IOC,
                }
                r = mt5.order_send(req)
                if r and getattr(r, "retcode", 0) == mt5.TRADE_RETCODE_DONE:
                    closed += 1
                    print(f"[MATH] session-end close {p.symbol} ticket={p.ticket} (sess={sess})")
                    self._tg(
                        f"SESSION-END TIME-STOP\n"
                        f"Symbol:  {p.symbol}\n"
                        f"Session: {sess} (ended at H{end_h:02d}:00 UTC)\n"
                        f"Ticket:  {p.ticket}\n"
                        f"Reason:  position outside session window (matches backtest)\n"
                        f"Action:  closed at market"
                    )
            except Exception as e:
                print(f"[MATH] session close err: {e}")

        return (cancelled, closed)

    # ─── Direction guard (tick) ──────────────────────────────────

    def tick_pending(self, setup_cfg: dict, bars: pl.DataFrame) -> int:
        """Check guard indicator on the newest bar for every pending MATH order
        matching this setup. Cancel if the ORIGINAL guard weakens.
        Returns number of orders cancelled this tick.
        """
        symbol = setup_cfg["sym"]
        setup_type = setup_cfg["setup_type"]

        if bars is None or len(bars) == 0:
            return 0

        guard_col = _guard_indicator_col(setup_type)
        try:
            latest_guard = bars.sort("time")[guard_col][-1]
        except Exception:
            return 0
        if latest_guard is None:
            return 0

        cancelled = 0
        now = datetime.now(timezone.utc)

        for key in list(self._pending.keys()):
            p = self._pending[key]
            if p.symbol != symbol or p.setup_type != setup_type:
                continue

            # Expiration → drop from registry
            if now >= p.expiration_utc:
                self._pending.pop(key, None)
                continue

            g0 = p.guard_value_at_placement
            g0_sign = 1.0 if g0 > 0 else (-1.0 if g0 < 0 else 0.0)
            if g0_sign == 0:
                continue

            gv_aligned = float(latest_guard) * g0_sign
            weaken_thresh = MATH_GUARD_WEAKEN_THRESHOLD * abs(g0)
            if gv_aligned < weaken_thresh:
                # Guard weakened: cancel the pending STOP
                self._cancel(p)
                cancelled += 1
                self._pending.pop(key, None)
                self._tg(
                    f"GUARD CANCEL\n"
                    f"Symbol:  {p.symbol}\n"
                    f"Setup:   {p.setup_type}\n"
                    f"Reason:  original indicator weakened\n"
                    f"Guard@0: {g0:.5f}\n"
                    f"Guard now: {latest_guard:.5f}"
                )
        return cancelled

    # ─── DRY virtual simulation (fill + TP/SL tracking) ─────────────

    def tick_virtual(self, setup_cfg: dict, bars: pl.DataFrame) -> int:
        """DRY-only: simulate fill and TP/SL resolution on pending/filled MATH
        orders for this setup using the latest bar's high/low.

        State machine per pending:
          PENDING → FILLED when latest bar's range crosses the STOP price
                    (LONG_STOP filled if high >= stop; SHORT_STOP if low <= stop)
          FILLED  → CLOSED when TP or SL touched. Also closes at session end
                    or expiration_utc (virtual time-stop).

        On CLOSED: append a JSON line to data/live_state/math_dry_trades.jsonl
        and notify Telegram [MATH][DRY] with R-multiple.

        Returns the number of virtual closes this tick.
        """
        if not self.dry_run or bars is None or len(bars) == 0:
            return 0

        symbol = setup_cfg["sym"]
        setup_type = setup_cfg["setup_type"]

        last_row = bars.sort("time").row(-1, named=True)
        t = last_row["time"]
        hi = last_row["high"]
        lo = last_row["low"]
        closes = 0

        for key, p in list(self._pending.items()):
            if p.symbol != symbol or p.setup_type != setup_type:
                continue

            now = datetime.now(timezone.utc)

            # Virtual fill: only if still PENDING
            if p.virt_state == "PENDING":
                is_long = p.flipped_direction == "LONG"
                filled = (hi >= p.stop_price) if is_long else (lo <= p.stop_price)
                if filled:
                    p.virt_state = "FILLED"
                    p.virt_entry_price = p.stop_price
                    p.virt_entry_time = t
                    self._tg(
                        f"VIRTUAL FILL\n"
                        f"Symbol:    {p.symbol}\n"
                        f"Setup:     {p.setup_type}\n"
                        f"Direction: {p.flipped_direction}\n"
                        f"Entry:     {p.stop_price:.5f}"
                    )
                # If not filled and expired, drop without log
                elif now >= p.expiration_utc:
                    self._pending.pop(key, None)
                continue

            # FILLED → check TP / SL / time-stop on latest bar
            if p.virt_state == "FILLED":
                is_long = p.flipped_direction == "LONG"
                exit_reason = None
                exit_price = None
                # TP priority (matches backtester semantics)
                if is_long:
                    if hi >= p.tp_price:
                        exit_reason, exit_price = "TP", p.tp_price
                    elif lo <= p.sl_price:
                        exit_reason, exit_price = "SL", p.sl_price
                else:
                    if lo <= p.tp_price:
                        exit_reason, exit_price = "TP", p.tp_price
                    elif hi >= p.sl_price:
                        exit_reason, exit_price = "SL", p.sl_price

                # Session time-stop (session end hour on same day)
                if exit_reason is None:
                    from src.domain.constants import INDICATOR_SESSIONS
                    session_end_h = INDICATOR_SESSIONS.get(p.session, (0, 24))[1]
                    if t.date() > p.virt_entry_time.date() or t.hour >= session_end_h:
                        exit_reason, exit_price = "TIME_STOP", last_row["close"]

                if exit_reason is not None:
                    r = self._r_multiple(p, exit_price)
                    self._log_dry_trade(p, exit_reason, exit_price, r, t)
                    self._pending.pop(key, None)
                    closes += 1
        return closes

    def _r_multiple(self, p: PendingMathOrder, exit_price: float) -> float:
        """R = net PnL / initial risk per unit."""
        if p.virt_entry_price is None or p.atr <= 0:
            return 0.0
        is_long = p.flipped_direction == "LONG"
        pnl = (exit_price - p.virt_entry_price) if is_long else (p.virt_entry_price - exit_price)
        risk_per_unit = abs(p.virt_entry_price - p.sl_price)
        return float(pnl / risk_per_unit) if risk_per_unit > 0 else 0.0

    def _log_dry_trade(self, p: PendingMathOrder, reason: str, exit_price: float,
                       r: float, exit_time: datetime) -> None:
        rec = {
            "symbol": p.symbol, "internal_sym": p.internal_sym,
            "session": p.session, "setup_type": p.setup_type,
            "direction": p.flipped_direction,
            "entry_time": p.virt_entry_time.isoformat() if p.virt_entry_time else None,
            "entry_price": p.virt_entry_price,
            "tp_price": p.tp_price, "sl_price": p.sl_price,
            "exit_time": exit_time.isoformat() if hasattr(exit_time, "isoformat") else str(exit_time),
            "exit_price": float(exit_price),
            "exit_reason": reason,
            "r_multiple": round(r, 4),
            "atr": float(p.atr),
        }
        try:
            with self._dry_trades_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(rec) + "\n")
        except Exception as e:
            print(f"[MATH][DRY] log write error: {e}")
        self._tg(
            f"VIRTUAL CLOSE\n"
            f"Symbol:    {p.symbol}\n"
            f"Setup:     {p.setup_type}\n"
            f"Direction: {p.flipped_direction}\n"
            f"Reason:    {reason}\n"
            f"Entry:     {p.virt_entry_price:.5f}\n"
            f"Exit:      {exit_price:.5f}\n"
            f"R-mult:    {r:+.3f}"
        )

    def read_dry_trades(self) -> list[dict]:
        """Read all logged virtual trades."""
        if not self._dry_trades_path.exists():
            return []
        out = []
        with self._dry_trades_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except Exception:
                    pass
        return out

    def emit_daily_report(self) -> str:
        """Summarize virtual trades and notify Telegram. Returns the text."""
        trades = self.read_dry_trades()
        if not trades:
            msg = "DRY report: 0 virtual trades logged yet"
            self._tg(msg)
            return msg

        today = self._today_utc()
        today_trades = [t for t in trades if (t.get("exit_time") or "").startswith(today)]

        def _fmt_block(label: str, ts: list[dict]) -> str:
            if not ts:
                return f"{label}: 0 trades"
            n = len(ts)
            rs = [t["r_multiple"] for t in ts]
            wins = [r for r in rs if r > 0]
            losses = [r for r in rs if r < 0]
            wr = len(wins) / n if n else 0.0
            gross_win = sum(wins)
            gross_loss = abs(sum(losses))
            pf = (gross_win / gross_loss) if gross_loss > 0 else float("inf")
            avg_r = sum(rs) / n
            net_r = sum(rs)
            return (f"{label}: n={n} WR={wr:.0%} PF={pf:.2f} "
                    f"avgR={avg_r:+.3f} netR={net_r:+.2f}")

        msg = (
            "[MATH][DRY] VIRTUAL P&L\n"
            f"{_fmt_block('Today ' + today, today_trades)}\n"
            f"{_fmt_block('All-time', trades)}"
        )
        self._tg(msg)
        return msg

    def _cancel(self, p: PendingMathOrder) -> bool:
        if self.dry_run or p.ticket < 0:
            print(f"[MATH][DRY] would cancel STOP ticket={p.ticket} {p.symbol}")
            return True
        if mt5 is None:
            return False
        try:
            req = {
                "action": mt5.TRADE_ACTION_REMOVE,
                "order": p.ticket,
                "symbol": p.symbol,
            }
            res = mt5.order_send(req)
            return bool(res and res.retcode == mt5.TRADE_RETCODE_DONE)
        except Exception as e:
            print(f"[MATH] cancel error: {e}")
            return False

    # ─── Housekeeping ────────────────────────────────────────────

    def sweep_expired(self) -> int:
        """Remove pending records whose expiration has passed (LIVE broker
        auto-expires the real order via ORDER_TIME_SPECIFIED)."""
        now = datetime.now(timezone.utc)
        dropped = 0
        for key in list(self._pending.keys()):
            if now >= self._pending[key].expiration_utc:
                self._pending.pop(key, None)
                dropped += 1
        return dropped

    def reset_daily_if_needed(self):
        """Clear dedup map when UTC date rolls over."""
        today = self._today_utc()
        # drop stale entries
        for k, v in list(self._fired_today.items()):
            if v != today:
                self._fired_today.pop(k, None)

    # ─── LIVE event detection (fills + closes) ───────────────────

    def detect_live_events(self) -> tuple[int, int]:
        """LIVE only: detect new fills and closes for magic=MAGIC_NUMBER_MATH.
        Sends Telegram notifications:
          - LIVE FILL: when a previously-pending order is now an open position
          - LIVE CLOSE: when a previously-open position is gone (TP/SL/manual)
        Returns (n_fills, n_closes).
        """
        if self.dry_run or mt5 is None:
            return (0, 0)

        # Track previous tickets across calls
        prev_open = getattr(self, "_prev_open_tickets", {})
        prev_pending = getattr(self, "_prev_pending_tickets", set())

        try:
            cur_pos = mt5.positions_get() or []
            cur_orders = mt5.orders_get() or []
        except Exception as e:
            print(f"[MATH] detect_live_events MT5 err: {e}")
            return (0, 0)

        cur_pos = [p for p in cur_pos if getattr(p, "magic", 0) == self.magic]
        cur_orders = [o for o in cur_orders if getattr(o, "magic", 0) == self.magic]
        cur_open = {p.ticket: p for p in cur_pos}
        cur_pending = {o.ticket for o in cur_orders}

        n_fills = 0
        n_closes = 0

        # FILLS: pending tickets that became positions (could be different ticket
        # IDs across pending→position in MT5; use symbol+comment as fallback)
        for tkt, p in cur_open.items():
            if tkt in prev_open:
                continue
            # New position
            n_fills += 1
            entry = float(getattr(p, "price_open", 0.0))
            sl = float(getattr(p, "sl", 0.0))
            tp = float(getattr(p, "tp", 0.0))
            vol = float(getattr(p, "volume", 0.0))
            ptype = "BUY" if getattr(p, "type", 0) == 0 else "SELL"
            self._tg(
                f"LIVE FILL\n"
                f"Symbol:    {p.symbol}\n"
                f"Comment:   {p.comment}\n"
                f"Direction: {ptype}\n"
                f"Volume:    {vol}\n"
                f"Entry:     {entry:.5f}\n"
                f"SL:        {sl:.5f}\n"
                f"TP:        {tp:.5f}\n"
                f"Ticket:    {tkt}"
            )

        # CLOSES: tickets that were open last tick but no longer open now
        for tkt, prev_p in prev_open.items():
            if tkt in cur_open:
                continue
            n_closes += 1
            # Try to fetch the closing deal for R-multiple
            r_mult = None
            close_price = None
            close_reason = "unknown"
            try:
                end = datetime.now(timezone.utc)
                start = end - timedelta(hours=24)
                deals = mt5.history_deals_get(start, end, position=tkt) or []
                # closing deal is the one with entry=DEAL_ENTRY_OUT
                for d in deals:
                    if getattr(d, "entry", 0) == 1:  # DEAL_ENTRY_OUT
                        close_price = float(d.price)
                        cmt = (d.comment or "").lower()
                        if "tp" in cmt:
                            close_reason = "TP"
                        elif "sl" in cmt:
                            close_reason = "SL"
                        elif "so" in cmt or "stopout" in cmt:
                            close_reason = "STOPOUT"
                        else:
                            close_reason = "manual/other"
                        # R-multiple from entry+sl on prev_p
                        entry = float(getattr(prev_p, "price_open", 0.0))
                        sl = float(getattr(prev_p, "sl", 0.0))
                        risk_unit = abs(entry - sl) if sl > 0 else 0.0
                        if risk_unit > 0:
                            ptype = getattr(prev_p, "type", 0)
                            pnl = (close_price - entry) if ptype == 0 else (entry - close_price)
                            r_mult = pnl / risk_unit
                        break
            except Exception as e:
                print(f"[MATH] history_deals err for {tkt}: {e}")

            r_line = f"R-mult:    {r_mult:+.3f}\n" if r_mult is not None else ""
            cp_line = f"Close:     {close_price:.5f}\n" if close_price is not None else ""
            self._tg(
                f"LIVE CLOSE\n"
                f"Symbol:    {prev_p.symbol}\n"
                f"Comment:   {prev_p.comment}\n"
                f"Reason:    {close_reason}\n"
                f"Entry:     {float(prev_p.price_open):.5f}\n"
                f"{cp_line}"
                f"{r_line}"
                f"Ticket:    {tkt}"
            )

        self._prev_open_tickets = cur_open
        self._prev_pending_tickets = cur_pending
        return (n_fills, n_closes)
