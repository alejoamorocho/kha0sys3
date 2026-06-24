"""Trade copier — mirror a source MT5 account's positions onto a dest account.

Built for: TMFinancials (source, READ-ONLY, exits managed MANUALLY = source
positions carry NO SL/TP) -> Vantage (dest), GOLD ONLY.

Guarantees (hardened 2026-06-23 after adversarial audit):
- OPEN when the source opens; CLOSE when the source closes; FORCE-retry every
  cycle until each action is CONFIRMED. The dest is NEVER allowed to drift from
  the source while we can see both.
- LIVE DEST positions (tagged `COPY|<src_ticket>`) are the single source of
  truth for what is currently copied — so closed/orphaned/double mappings can't
  poison state. order ids are never stored as position tickets.
- Idempotent open: a pending marker is written BEFORE order_send, and the dest
  position is CONFIRMED by its comment before the open is considered done, so a
  missed read-back never double-opens.
- A copy that vanishes while its source is still open (manual/stop-out/backstop)
  is RE-OPENED (capped, with a loud alert) so "copy open while source open" holds.
- Fail-safe: a source READ failure NEVER closes dest copies. But it ALERTS — a
  blind copier with no SL/TP on the copies is the real danger, so silence is not
  allowed: every failure path escalates to Telegram (rate-limited).
- Path-pinned + login-validated on BOTH terminals (never acts on a wrong account).
- Optional backstop SL on the copy (config backstop_sl_usd) as a safety net for
  the case where the copier itself dies — off by default (exact mirror).

reconcile() is pure (no MT5) and unit-tested.
"""
from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import MetaTrader5 as mt5
except Exception:  # pragma: no cover - MT5 only on the trading box
    mt5 = None


def _now() -> float:
    return time.time()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class TradeCopier:
    MAX_CONNECT_RETRIES = 3
    CONFIRM_RETRIES = 6          # post-send read-back attempts to confirm a fill
    CONFIRM_SLEEP = 0.4

    def __init__(self, cfg: dict, telegram=None):
        self.src = dict(cfg["source"])
        # Source full-login creds (MT5_*2 from .env) so the copier logs into TMF
        # on its OWN session-0 terminal that actually SYNCS positions — instead
        # of a position-blind cross-session attach to the GUI in session 1.
        try:
            from src.domain.env_loader import load_env
            load_env()
        except Exception:
            pass
        if os.environ.get("MT5_PASSWORD2") and os.environ.get("MT5_SERVER2"):
            self.src["password"] = os.environ["MT5_PASSWORD2"]
            self.src["server"] = os.environ["MT5_SERVER2"]
            if os.environ.get("MT5_LOGIN2"):
                self.src["login"] = int(os.environ["MT5_LOGIN2"])
        self.dst = cfg["dest"]
        self.symbol_map: dict[str, str] = cfg["symbol_map"]
        self.fixed_lot = float(cfg["fixed_lot"])
        self.magic = int(cfg.get("magic", 5000))
        self.poll_sec = max(1, int(cfg.get("poll_sec", 2)))
        self.max_dev = int(cfg.get("max_slippage_points", 50))
        self.max_reopen = int(cfg.get("max_reopen", 2))
        self.heartbeat_min = int(cfg.get("heartbeat_min", 15))
        self.alert_repeat_min = int(cfg.get("alert_repeat_min", 5))
        self.backstop_sl_usd = cfg.get("backstop_sl_usd")  # None = no backstop
        self.dry_run = bool(cfg.get("dry_run", True))
        self.state_file = Path(cfg.get("state_file", "logs/copier_state.json"))
        self.heartbeat_file = Path(cfg.get("heartbeat_file", "logs/copier_heartbeat"))
        self.telegram = telegram
        self._stop = False
        self._alert_ts: dict[str, float] = {}
        self._consec_src_fail = 0
        self._consec_dst_fail = 0
        self._last_heartbeat = 0.0
        self._diag_ts = 0.0

    # ───────────────────────── logging / alerts ─────────────────────────
    def log(self, msg: str, tg: bool = False) -> None:
        line = f"{_now_iso()} [COPIER]{' [DRY]' if self.dry_run else ''} {msg}"
        print(line, flush=True)
        if tg and self.telegram is not None:
            try:
                self.telegram._send(f"[COPIER]{' [DRY]' if self.dry_run else ''} {msg}")
            except Exception:
                pass

    def alert(self, key: str, msg: str) -> None:
        """Telegram alert, rate-limited per key (first hit + every alert_repeat_min)."""
        last = self._alert_ts.get(key, 0.0)
        due = (_now() - last) >= self.alert_repeat_min * 60
        self.log(msg, tg=due)
        if due:
            self._alert_ts[key] = _now()

    # ───────────────── pure logic (unit-testable) ─────────────────
    @staticmethod
    def reconcile(source_positions: list[dict], dst_map: dict) -> tuple[list[dict], list[int]]:
        """Given the source positions and the LIVE dest copy map
        {src_ticket(str): dst_ticket}, decide:
          to_open  = source positions with no live copy.
          to_close = dest tickets whose source position no longer exists.
        """
        src_tickets = {str(p["ticket"]) for p in source_positions}
        to_open = [p for p in source_positions if str(p["ticket"]) not in dst_map]
        to_close = [dst for src, dst in dst_map.items() if src not in src_tickets]
        return to_open, to_close

    def map_symbol(self, src_symbol: str) -> str | None:
        return self.symbol_map.get(src_symbol)

    # ───────────────────── state persistence ─────────────────────
    def load_state(self) -> dict:
        try:
            s = json.loads(self.state_file.read_text(encoding="utf-8"))
        except Exception:
            s = {}
        s.setdefault("pending", {})       # {src_ticket: comment} in-flight opens
        s.setdefault("ever", [])          # src tickets ever copied (new vs reopen)
        s.setdefault("reopen", {})        # {src_ticket: count}
        return s

    def save_state(self, state: dict) -> None:
        try:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            self.state_file.write_text(json.dumps(state, indent=2), encoding="utf-8")
        except Exception as e:
            self.log(f"state save error: {e}")

    # ───────────────────────── MT5 I/O ─────────────────────────
    def _connect(self, node: dict) -> bool:
        if mt5 is None:
            return False
        want = int(node["login"])
        has_creds = bool(node.get("password") and node.get("server"))
        for _ in range(self.MAX_CONNECT_RETRIES):
            mt5.shutdown()
            # Attach-first: reuse a running terminal already on the right account
            # (cheap; this is how subsequent ticks hit the persistent terminal).
            if mt5.initialize(path=node["path"]):
                info = mt5.account_info()
                ti = mt5.terminal_info()
                if info and int(info.login) == want and ti and ti.connected:
                    return True
            # Not on the right account / not connected: full login. Launches a
            # dedicated session-0 terminal that actually SYNCS positions.
            if has_creds:
                if mt5.initialize(path=node["path"], login=want,
                                  password=node["password"], server=node["server"]):
                    info = mt5.account_info()
                    if info and int(info.login) == want:
                        return True
            time.sleep(0.5)
        return False

    def _diag(self, msg: str) -> None:
        """Rate-limited (~30s) diagnostic line so a live miss is visible in the log."""
        if (_now() - self._diag_ts) >= 30:
            self.log(f"DIAG {msg}")
            self._diag_ts = _now()

    def read_source(self) -> list[dict] | None:
        """Source gold positions, or None on ANY failure (caller must skip, not close)."""
        if not self._connect(self.src):
            return None
        # Wait for the broker connection to be live, then let positions sync — a
        # fresh attach can briefly report 0 positions before they load.
        for _ in range(6):
            ti = mt5.terminal_info()
            if ti and ti.connected:
                break
            time.sleep(0.3)
        positions = mt5.positions_get()
        for _ in range(3):
            if positions:
                break
            time.sleep(0.3)
            positions = mt5.positions_get()
        if positions is None:
            return None
        raw = list(positions)
        ti = mt5.terminal_info()
        self._diag(f"src: connected={getattr(ti, 'connected', None)} raw_positions={len(raw)} "
                   f"symbols={[p.symbol for p in raw][:6]} (looking for {list(self.symbol_map)})")
        return [
            {"ticket": p.ticket, "symbol": p.symbol, "type": int(p.type),
             "sl": float(p.sl), "tp": float(p.tp), "volume": float(p.volume)}
            for p in raw if p.symbol in self.symbol_map
        ]

    def read_dest_copies(self) -> dict | None:
        """Live dest map {src_ticket(str): dst_ticket} from positions tagged
        COPY|<src> with our magic. Returns None on failure (caller must skip)."""
        positions = mt5.positions_get()
        if positions is None:
            return None
        out: dict[str, int] = {}
        for p in positions:
            if p.magic != self.magic:
                continue
            c = (p.comment or "")
            if c.startswith("COPY|"):
                out[c.split("|", 1)[1]] = p.ticket
        return out

    def _filling_modes(self):
        return [mt5.ORDER_FILLING_IOC, mt5.ORDER_FILLING_FOK, mt5.ORDER_FILLING_RETURN]

    def _backstop_sl(self, symbol: str, is_buy: bool, entry: float) -> float:
        """Protective SL price for a fixed_lot position risking ~backstop_sl_usd.
        Returns 0.0 (no SL) when backstop disabled — exact mirror like the source."""
        if not self.backstop_sl_usd:
            return 0.0
        info = mt5.symbol_info(symbol)
        if not info or info.trade_tick_value <= 0 or info.trade_tick_size <= 0:
            return 0.0
        usd_per_price = (info.trade_tick_value / info.trade_tick_size) * self.fixed_lot
        if usd_per_price <= 0:
            return 0.0
        dist = float(self.backstop_sl_usd) / usd_per_price
        sl = entry - dist if is_buy else entry + dist
        return round(sl, info.digits)

    def _confirm_open(self, dst_symbol: str, comment: str) -> int | None:
        """Confirm the dest position exists by its unique comment (bounded retry).
        NEVER returns an order id — only a real position ticket."""
        for _ in range(self.CONFIRM_RETRIES):
            for p in (mt5.positions_get(symbol=dst_symbol) or []):
                if (p.comment or "") == comment and p.magic == self.magic:
                    return p.ticket
            time.sleep(self.CONFIRM_SLEEP)
        return None

    def open_on_dest(self, src_pos: dict) -> int | None:
        dst_symbol = self.map_symbol(src_pos["symbol"])
        if dst_symbol is None:
            return None
        info = mt5.symbol_info(dst_symbol)
        if info is None:
            self.alert(f"sym:{dst_symbol}", f"dest symbol {dst_symbol} not found"); return None
        if not info.visible:
            mt5.symbol_select(dst_symbol, True)
        tick = mt5.symbol_info_tick(dst_symbol)
        if tick is None:
            self.alert(f"tick:{dst_symbol}", f"no tick for {dst_symbol} — open blocked"); return None
        is_buy = src_pos["type"] == 0
        price = tick.ask if is_buy else tick.bid
        sl = src_pos["sl"] or self._backstop_sl(dst_symbol, is_buy, price)
        comment = f"COPY|{src_pos['ticket']}"
        if self.dry_run:
            self.alert(f"dryopen:{src_pos['ticket']}",
                       f"would OPEN {dst_symbol} {'BUY' if is_buy else 'SELL'} {self.fixed_lot} "
                       f"@~{price} sl={sl} tp={src_pos['tp']} [src {src_pos['ticket']}]")
            return None
        last_ret = None
        for filling in self._filling_modes():
            req = {
                "action": mt5.TRADE_ACTION_DEAL, "symbol": dst_symbol, "volume": self.fixed_lot,
                "type": mt5.ORDER_TYPE_BUY if is_buy else mt5.ORDER_TYPE_SELL,
                "price": tick.ask if is_buy else tick.bid, "sl": sl, "tp": src_pos["tp"],
                "deviation": self.max_dev, "magic": self.magic, "comment": comment,
                "type_time": mt5.ORDER_TIME_GTC, "type_filling": filling,
            }
            result = mt5.order_send(req)
            last_ret = getattr(result, "retcode", None)
            if last_ret == mt5.TRADE_RETCODE_DONE:
                dst = self._confirm_open(dst_symbol, comment)
                if dst:
                    self.log(f"OPENED {dst_symbol} {'BUY' if is_buy else 'SELL'} {self.fixed_lot} "
                             f"[src {src_pos['ticket']} -> dst {dst}]", tg=True)
                    return dst
                # Sent DONE but unconfirmed: do NOT re-send (pending marker holds);
                # next tick will confirm via the live COPY| comment.
                self.alert(f"unconf:{src_pos['ticket']}",
                           f"OPEN sent but UNCONFIRMED [src {src_pos['ticket']}] — holding pending")
                return None
            if last_ret == 10030:  # invalid filling — try the next mode
                continue
            break  # other hard reject — stop trying fillings
        self.alert(f"openfail:{src_pos['ticket']}",
                   f"OPEN FAILED {dst_symbol} [src {src_pos['ticket']}] retcode={last_ret} — will retry")
        return None

    def close_on_dest(self, dst_ticket: int) -> bool:
        positions = mt5.positions_get(ticket=dst_ticket) or []
        if not positions:
            return True  # already flat
        p = positions[0]
        if self.dry_run:
            self.alert(f"dryclose:{dst_ticket}", f"would CLOSE dst {dst_ticket} ({p.symbol} {p.volume})")
            return False
        tick = mt5.symbol_info_tick(p.symbol)
        if tick is None:
            self.alert(f"closetick:{dst_ticket}",
                       f"CLOSE BLOCKED dst {dst_ticket}: no tick for {p.symbol} — will retry")
            return False
        is_buy = p.type == 0
        req = {
            "action": mt5.TRADE_ACTION_DEAL, "symbol": p.symbol, "position": dst_ticket,
            "volume": p.volume, "type": mt5.ORDER_TYPE_SELL if is_buy else mt5.ORDER_TYPE_BUY,
            "price": tick.bid if is_buy else tick.ask, "deviation": self.max_dev,
            "magic": self.magic, "comment": "COPY-CLOSE", "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": self._filling_modes()[0],
        }
        result = mt5.order_send(req)
        if getattr(result, "retcode", None) != mt5.TRADE_RETCODE_DONE:
            self.alert(f"closefail:{dst_ticket}",
                       f"CLOSE FAILED dst {dst_ticket}: retcode={getattr(result,'retcode',None)} — will retry")
            return False
        # Verify it actually flattened (an IOC close can partial-fill yet return DONE).
        if mt5.positions_get(ticket=dst_ticket):
            self.alert(f"closepart:{dst_ticket}", f"CLOSE partial dst {dst_ticket} — will retry residual")
            return False
        self.log(f"CLOSED dst {dst_ticket}", tg=True)
        return True

    # ───────────────────────── heartbeat ─────────────────────────
    def _heartbeat(self, n_open: int) -> None:
        try:
            self.heartbeat_file.parent.mkdir(parents=True, exist_ok=True)
            self.heartbeat_file.write_text(_now_iso(), encoding="utf-8")
        except Exception:
            pass
        if (_now() - self._last_heartbeat) >= self.heartbeat_min * 60:
            self.log(f"HEARTBEAT alive — {n_open} copies open, src OK", tg=True)
            self._last_heartbeat = _now()

    # ───────────────────────── main loop ─────────────────────────
    def tick(self) -> None:
        # Heartbeat written EVERY cycle (even on the early returns below) so the
        # external watchdog only restarts a truly HUNG process — a merely-blind
        # copier (source/dest unreadable) stays up and alerts on its own.
        try:
            self.heartbeat_file.parent.mkdir(parents=True, exist_ok=True)
            self.heartbeat_file.write_text(_now_iso(), encoding="utf-8")
        except Exception:
            pass

        # 1) Source = truth for what should be open. None => blind; alert, never close.
        source_positions = self.read_source()
        if source_positions is None:
            self._consec_src_fail += 1
            self.alert("srcfail", f"SOURCE UNREADABLE x{self._consec_src_fail} — copier blind, "
                                  f"NOT closing copies. Check TMF terminal.")
            return
        self._consec_src_fail = 0

        # 2) Dest connection.
        if not self._connect(self.dst):
            self._consec_dst_fail += 1
            self.alert("dstfail", f"DEST UNREACHABLE x{self._consec_dst_fail} — cannot mirror. "
                                  f"Check Vantage terminal.")
            return
        self._consec_dst_fail = 0

        # 3) Live dest copies = single source of truth (immune to stale state).
        dst_map = self.read_dest_copies()
        if dst_map is None:
            self.alert("dstread", "DEST positions unreadable — skipping cycle")
            return

        state = self.load_state()
        pending: dict = state["pending"]
        ever: set = set(state["ever"])
        reopen: dict = state["reopen"]
        src_tickets = {str(p["ticket"]) for p in source_positions}

        # Clear pending that is now confirmed live, or whose source already closed.
        for st in list(pending.keys()):
            if st in dst_map or st not in src_tickets:
                pending.pop(st, None)

        to_open, to_close = self.reconcile(source_positions, dst_map)

        # 4) OPENS (new sources + vanished-while-source-open re-opens).
        for src_pos in to_open:
            st = str(src_pos["ticket"])
            if st in pending:
                continue  # in-flight; don't re-send
            if st in ever:  # copy vanished while source still open
                if self.backstop_sl_usd:
                    # A backstop SL is active, so a vanished copy almost certainly
                    # hit that protective stop. Re-opening would just re-arm the
                    # stop and ping-pong — so DON'T re-open; alert for manual review.
                    self.alert(f"backstophit:{st}",
                               f"copy for source {st} CLOSED (likely backstop SL) while source "
                               f"still OPEN — NOT re-opening. Manual review.")
                    continue
                n = reopen.get(st, 0) + 1
                reopen[st] = n
                if n > self.max_reopen:
                    self.alert(f"reopencap:{st}",
                               f"COPY GONE but source {st} still OPEN — re-open cap "
                               f"({self.max_reopen}) hit. MANUAL CHECK NEEDED.")
                    continue
                self.alert(f"reopen:{st}", f"copy vanished while source {st} open — re-opening (#{n})")
            pending[st] = f"COPY|{st}"
            self.save_state({"pending": pending, "ever": list(ever), "reopen": reopen})
            dst = self.open_on_dest(src_pos)
            if dst:
                ever.add(st)
                pending.pop(st, None)
                reopen.pop(st, None)

        # 5) CLOSES (source gone => force-close the copy; guarded individually).
        for dst_ticket in to_close:
            try:
                self.close_on_dest(dst_ticket)
            except Exception as e:
                self.alert(f"closeerr:{dst_ticket}", f"close error dst {dst_ticket}: {e} — will retry")

        # 6) prune ever/reopen for sources no longer open and no live copy.
        for st in list(ever):
            if st not in src_tickets and st not in dst_map:
                ever.discard(st); reopen.pop(st, None); pending.pop(st, None)

        self.save_state({"pending": pending, "ever": list(ever), "reopen": reopen})
        self._heartbeat(len(dst_map))

    def run(self) -> None:
        self.log(f"COPIER START src={self.src['broker']}({self.src['login']}) -> "
                 f"dst={self.dst['broker']}({self.dst['login']}) lot={self.fixed_lot} "
                 f"symbols={self.symbol_map} poll={self.poll_sec}s backstop_sl_usd={self.backstop_sl_usd} "
                 f"dry_run={self.dry_run}", tg=True)
        while not self._stop:
            try:
                self.tick()
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.alert("tickerr", f"tick error: {e} — continuing")
            time.sleep(self.poll_sec)

    def stop(self) -> None:
        self._stop = True
