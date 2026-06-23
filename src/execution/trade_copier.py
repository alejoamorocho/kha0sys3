"""Trade copier — mirror a source MT5 account's positions onto a dest account.

Built for: TMFinancials (source, READ-ONLY) -> Vantage (dest), GOLD ONLY.
- Fixed lot on dest (never scales/grows). SL/TP price levels replicated.
- Path-pinned + login-validated on BOTH terminals so it can never act on the
  wrong account (a second broker on the same box).
- Crash-safe: every dest order is tagged `COPY|<source_ticket>` so state can be
  rebuilt from the dest positions even if the state file is lost.
- Fail-safe close: a source READ failure NEVER triggers dest closes (we only
  close a copy when we positively confirm the source position is gone).
- dry_run: logs intended actions without sending orders.

The reconcile() logic is pure (no MT5) so it is unit-testable.
"""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import MetaTrader5 as mt5
except Exception:  # pragma: no cover - MT5 only on the trading box
    mt5 = None


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class TradeCopier:
    MAX_CONNECT_RETRIES = 3

    def __init__(self, cfg: dict, telegram=None):
        self.src = cfg["source"]
        self.dst = cfg["dest"]
        self.symbol_map: dict[str, str] = cfg["symbol_map"]
        self.fixed_lot = float(cfg["fixed_lot"])
        self.magic = int(cfg.get("magic", 5000))
        self.poll_sec = int(cfg.get("poll_sec", 3))
        self.max_dev = int(cfg.get("max_slippage_points", 50))
        self.dry_run = bool(cfg.get("dry_run", True))
        self.state_file = Path(cfg.get("state_file", "logs/copier_state.json"))
        self.telegram = telegram
        self._stop = False
        self._connected_to: str | None = None

    # ───────────────────────── logging ─────────────────────────
    def log(self, msg: str, tg: bool = False) -> None:
        line = f"{_now_iso()} [COPIER]{' [DRY]' if self.dry_run else ''} {msg}"
        print(line, flush=True)
        if tg and self.telegram is not None:
            try:
                self.telegram._send(f"[COPIER]{' [DRY]' if self.dry_run else ''} {msg}")
            except Exception:
                pass

    # ───────────────── pure logic (unit-testable) ─────────────────
    @staticmethod
    def reconcile(source_positions: list[dict], state: dict) -> tuple[list[dict], list[int]]:
        """Decide what to open/close on the dest.

        source_positions: list of dicts each with at least 'ticket'.
        state: {source_ticket(str): dest_ticket(int)}.
        Returns (to_open, to_close):
          to_open  = source positions whose ticket is not yet copied.
          to_close = dest tickets whose source position no longer exists.
        """
        src_tickets = {str(p["ticket"]) for p in source_positions}
        to_open = [p for p in source_positions if str(p["ticket"]) not in state]
        to_close = [dst for src, dst in state.items() if src not in src_tickets]
        return to_open, to_close

    def map_symbol(self, src_symbol: str) -> str | None:
        return self.symbol_map.get(src_symbol)

    # ───────────────────── state persistence ─────────────────────
    def load_state(self) -> dict:
        try:
            return json.loads(self.state_file.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def save_state(self, state: dict) -> None:
        try:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            self.state_file.write_text(json.dumps(state, indent=2), encoding="utf-8")
        except Exception as e:
            self.log(f"state save error: {e}")

    # ───────────────────────── MT5 I/O ─────────────────────────
    def _connect(self, node: dict) -> bool:
        """Pin to node['path'] and validate account login. Returns True only if
        connected to the EXPECTED account."""
        if mt5 is None:
            return False
        for attempt in range(self.MAX_CONNECT_RETRIES):
            mt5.shutdown()
            if not mt5.initialize(path=node["path"]):
                time.sleep(1)
                continue
            info = mt5.account_info()
            if info is not None and int(info.login) == int(node["login"]):
                self._connected_to = node.get("broker", node["path"])
                return True
            time.sleep(1)
        self.log(f"connect FAILED to {node.get('broker')} (login {node['login']})")
        return False

    def read_source(self) -> list[dict] | None:
        """Read source positions for mapped symbols. Returns None on ANY failure
        (caller must NOT treat None as 'no positions' — it skips the cycle so a
        transient read error never closes dest copies)."""
        if not self._connect(self.src):
            return None
        positions = mt5.positions_get()
        if positions is None:
            return None
        return [
            {"ticket": p.ticket, "symbol": p.symbol, "type": int(p.type),
             "sl": float(p.sl), "tp": float(p.tp), "volume": float(p.volume)}
            for p in positions if p.symbol in self.symbol_map
        ]

    def recover_state_from_dest(self, state: dict) -> dict:
        """Rebuild any missing state mapping from dest positions tagged
        `COPY|<src_ticket>` — makes restarts crash-safe (no double-open)."""
        for p in (mt5.positions_get() or []):
            c = (p.comment or "")
            if c.startswith("COPY|"):
                src_ticket = c.split("|", 1)[1]
                state.setdefault(src_ticket, p.ticket)
        return state

    def _filling_mode(self, symbol: str):
        info = mt5.symbol_info(symbol)
        # Prefer the broker's declared filling; fall back to IOC then FOK.
        fm = getattr(info, "filling_mode", 0) if info else 0
        if fm & 2:  # SYMBOL_FILLING_IOC
            return mt5.ORDER_FILLING_IOC
        if fm & 1:  # SYMBOL_FILLING_FOK
            return mt5.ORDER_FILLING_FOK
        return mt5.ORDER_FILLING_RETURN

    def open_on_dest(self, src_pos: dict) -> int | None:
        """Open the copy on dest. Returns the dest position ticket, or None."""
        dst_symbol = self.map_symbol(src_pos["symbol"])
        if dst_symbol is None:
            return None
        info = mt5.symbol_info(dst_symbol)
        if info is None:
            self.log(f"dest symbol {dst_symbol} not found — skip"); return None
        if not info.visible:
            mt5.symbol_select(dst_symbol, True)
        tick = mt5.symbol_info_tick(dst_symbol)
        if tick is None:
            self.log(f"no tick for {dst_symbol} — skip"); return None
        is_buy = src_pos["type"] == 0
        price = tick.ask if is_buy else tick.bid
        comment = f"COPY|{src_pos['ticket']}"
        if self.dry_run:
            self.log(f"would OPEN {dst_symbol} {'BUY' if is_buy else 'SELL'} "
                     f"{self.fixed_lot} @~{price} sl={src_pos['sl']} tp={src_pos['tp']} "
                     f"[src {src_pos['ticket']}]", tg=True)
            return None
        req = {
            "action": mt5.TRADE_ACTION_DEAL, "symbol": dst_symbol,
            "volume": self.fixed_lot,
            "type": mt5.ORDER_TYPE_BUY if is_buy else mt5.ORDER_TYPE_SELL,
            "price": price, "sl": src_pos["sl"], "tp": src_pos["tp"],
            "deviation": self.max_dev, "magic": self.magic, "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC, "type_filling": self._filling_mode(dst_symbol),
        }
        result = mt5.order_send(req)
        if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
            self.log(f"OPEN FAILED {dst_symbol}: "
                     f"{getattr(result, 'retcode', '?')} {getattr(result, 'comment', '')}", tg=True)
            return None
        # Find the resulting dest position ticket by our unique comment.
        for p in (mt5.positions_get(symbol=dst_symbol) or []):
            if (p.comment or "") == comment:
                self.log(f"OPENED {dst_symbol} {'BUY' if is_buy else 'SELL'} {self.fixed_lot} "
                         f"[src {src_pos['ticket']} -> dst {p.ticket}]", tg=True)
                return p.ticket
        return result.order or None

    def close_on_dest(self, dst_ticket: int) -> bool:
        """Close a dest position by ticket (market)."""
        positions = mt5.positions_get(ticket=dst_ticket) or []
        if not positions:
            return True  # already gone
        p = positions[0]
        if self.dry_run:
            self.log(f"would CLOSE dst {dst_ticket} ({p.symbol} vol {p.volume})", tg=True)
            return False
        tick = mt5.symbol_info_tick(p.symbol)
        is_buy = p.type == 0
        price = tick.bid if is_buy else tick.ask
        req = {
            "action": mt5.TRADE_ACTION_DEAL, "symbol": p.symbol, "position": dst_ticket,
            "volume": p.volume,
            "type": mt5.ORDER_TYPE_SELL if is_buy else mt5.ORDER_TYPE_BUY,
            "price": price, "deviation": self.max_dev, "magic": self.magic,
            "comment": "COPY-CLOSE", "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": self._filling_mode(p.symbol),
        }
        result = mt5.order_send(req)
        ok = result is not None and result.retcode == mt5.TRADE_RETCODE_DONE
        self.log(f"{'CLOSED' if ok else 'CLOSE FAILED'} dst {dst_ticket}: "
                 f"{getattr(result, 'retcode', '?')}", tg=True)
        return ok

    # ───────────────────────── main loop ─────────────────────────
    def tick(self) -> None:
        """One reconcile cycle. Safe to call repeatedly."""
        source_positions = self.read_source()
        if source_positions is None:
            self.log("source unreadable this cycle — skipping (no closes)")
            return
        if not self._connect(self.dst):
            self.log("dest unreachable this cycle — skipping")
            return
        state = self.load_state()
        state = self.recover_state_from_dest(state)
        to_open, to_close = self.reconcile(source_positions, state)
        for src_pos in to_open:
            dst_ticket = self.open_on_dest(src_pos)
            if dst_ticket:
                state[str(src_pos["ticket"])] = dst_ticket
        for dst_ticket in to_close:
            if self.close_on_dest(dst_ticket):
                state = {k: v for k, v in state.items() if v != dst_ticket}
        self.save_state(state)

    def run(self) -> None:
        self.log(f"COPIER START  src={self.src['broker']}({self.src['login']}) "
                 f"-> dst={self.dst['broker']}({self.dst['login']})  "
                 f"lot={self.fixed_lot}  symbols={self.symbol_map}  "
                 f"dry_run={self.dry_run}", tg=True)
        while not self._stop:
            try:
                self.tick()
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.log(f"tick error: {e}")
            time.sleep(self.poll_sec)

    def stop(self) -> None:
        self._stop = True
