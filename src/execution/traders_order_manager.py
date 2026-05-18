"""Traders Order Manager — Tier 1 Swing (magic 1339) + Tier 2 ORB (magic 1340).

Maneja:
  - Colocacion de STOP orders (entry @ pivot/range_high)
  - SL y TP iniciales (TP = primer partial; el resto se gestiona dinamicamente)
  - Partials adicionales por r_multiple / pct_from_entry / days_held
  - Trailing por SMA D1 (10/20/50) post-primer-partial
  - Time-stop (Zanger 2-3d si no toca TP1)
  - Max hold (cerrar por timeout)
  - Filtrado por magic number (1339 swing / 1340 ORB)

DRY_RUN=True: no llama mt5.order_send, solo loguea.

Convenciones de comment MT5 (max 31 chars):
  Swing: "S|<setup>|<variant>|<sym>" ej. "S|HTF|PDF|XAGUSD"
  ORB:   "O|<oh>h<rm>m|<sym>" ej. "O|13h15m|WTI"
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

try:
    import MetaTrader5 as mt5  # type: ignore
except Exception:
    mt5 = None  # type: ignore

from src.domain.constants import (
    MAGIC_NUMBER_TRADERS_SWING, MAGIC_NUMBER_TRADERS_ORB,
)


_RETCODE_INVALID_PRICE = 10015
_RETCODE_INVALID_STOPS = 10016
_RETCODE_INVALID_EXPIRATION = 10022
_RETCODE_CLIENT_DISABLES_AT = 10027


def make_swing_comment(setup: str, variant: str, sym: str) -> str:
    setup_tag = {"VCP": "VCP", "HTF": "HTF", "FLAG": "FLG", "CUP": "CUP"}.get(setup, setup[:3])
    return f"S|{setup_tag}|{variant[:3]}|{sym[:8]}"[:31]


def make_orb_comment(oh: int, rm: int, sym: str) -> str:
    return f"O|{oh:02d}h{rm:02d}m|{sym[:8]}"[:31]


@dataclass
class TradersOpenPosition:
    """Posicion abierta tracked por el manager (estado interno).

    Persistido en state file para sobrevivir restarts.
    """
    ticket: int
    magic: int
    symbol: str
    sym_internal: str
    strategy_id: str        # ej. TS_XAGUSD_QULLAHTF_PDF
    setup_type: str         # VCP / HTF / ORB
    variant: str            # PDF / GRID / -
    direction: str          # LONG/SHORT (mostly LONG)
    entry_price: float
    initial_volume: float
    remaining_volume: float
    initial_sl: float
    current_sl: float
    initial_atr_or_risk: float   # ATR usado para sizing
    entry_time_us: int           # microseconds UTC
    partials_taken: list = field(default_factory=list)  # idx de partials ya tomadas
    tp1_hit: bool = False
    exit_rules: dict = field(default_factory=dict)   # config exit rules de la strategy
    last_state_check_us: int = 0

    def to_dict(self) -> dict:
        return {**self.__dict__}

    @classmethod
    def from_dict(cls, d: dict):
        return cls(**d)


@dataclass
class TradersPendingOrder:
    """STOP order pendiente."""
    ticket: int
    magic: int
    symbol: str
    sym_internal: str
    strategy_id: str
    setup_type: str
    variant: str
    direction: str
    stop_price: float
    tp_price: float
    sl_price: float
    atr_or_risk: float
    placed_us: int
    expiration_us: int
    exit_rules: dict = field(default_factory=dict)


class TradersOrderManager:
    """Order manager unificado para Swing (1339) + ORB (1340).

    Args:
        client: MT5Client conectado
        magic: MAGIC_NUMBER_TRADERS_SWING o MAGIC_NUMBER_TRADERS_ORB
        risk_pct: % de balance por trade (0.001 = 0.1%)
        dry_run: si True, no envia ordenes reales
        state_file: ruta a JSON con estado persistido
    """

    def __init__(self, client, magic: int, risk_pct: float = 0.001,
                 dry_run: bool = False, state_file: Optional[Path] = None,
                 notifier=None, internal_to_broker: Optional[dict] = None):
        self.client = client
        self.magic = magic
        self.risk_pct = risk_pct
        self.dry_run = dry_run
        self.state_file = state_file or Path("logs") / f"traders_state_magic{magic}.json"
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.open_positions: dict[int, TradersOpenPosition] = {}
        self.pending_orders: dict[int, TradersPendingOrder] = {}
        self.notifier = notifier   # TradersNotifier o None
        # mapping para enriquecer notifs: strategy_id -> {trader, setup, variant, internal_sym}
        self.strategy_meta: dict[str, dict] = {}
        # Once-per-day-per-strategy gate — matches backtest semantic. Each
        # strategy fires at most 1 entry per UTC day. After fill+close, the
        # strategy is DONE for the day even if breakout conditions persist.
        # Persisted so a service restart doesn't reset the day's firings.
        self._fired_today: dict[str, str] = {}  # strategy_id -> UTC date "YYYY-MM-DD"
        self._load_state()

    # ── Persistencia ─────────────────────────────────────────────────────

    def _load_state(self):
        if not self.state_file.exists():
            return
        try:
            with self.state_file.open("r", encoding="utf-8") as f:
                state = json.load(f)
            for d in state.get("open_positions", []):
                p = TradersOpenPosition.from_dict(d)
                self.open_positions[p.ticket] = p
            for d in state.get("pending_orders", []):
                self.pending_orders[d["ticket"]] = TradersPendingOrder(**d)
            for sid, day in (state.get("fired_today") or {}).items():
                self._fired_today[sid] = day
            # Backfill: any strategy with an open position or pending order
            # from today counts as fired today, so we don't double-place
            # after a restart.
            today = self._today_utc()
            for p in self.open_positions.values():
                if p.strategy_id and p.strategy_id not in self._fired_today:
                    # Best-effort: only mark today if the position was opened
                    # in the last 24h. Without entry_time_us we'd skip; here
                    # we have it from to_dict.
                    if hasattr(p, "entry_time_us") and p.entry_time_us:
                        opened = datetime.fromtimestamp(
                            p.entry_time_us / 1_000_000, tz=timezone.utc
                        ).date().isoformat()
                        if opened == today:
                            self._fired_today[p.strategy_id] = today
            for p in self.pending_orders.values():
                if p.strategy_id and p.strategy_id not in self._fired_today:
                    if p.placed_us:
                        placed = datetime.fromtimestamp(
                            p.placed_us / 1_000_000, tz=timezone.utc
                        ).date().isoformat()
                        if placed == today:
                            self._fired_today[p.strategy_id] = today
            print(f"[Traders mgr {self.magic}] loaded state: {len(self.open_positions)} open, "
                  f"{len(self.pending_orders)} pending")
        except Exception as e:
            print(f"[Traders mgr {self.magic}] state load WARN: {e}")

    def _save_state(self):
        state = {
            "open_positions": [p.to_dict() for p in self.open_positions.values()],
            "pending_orders": [p.__dict__ for p in self.pending_orders.values()],
            "fired_today": dict(self._fired_today),
        }
        try:
            with self.state_file.open("w", encoding="utf-8") as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(f"[Traders mgr {self.magic}] state save WARN: {e}")

    # ── Once-per-day-per-strategy gate ───────────────────────────────────
    # Keyed by COMMENT (the canonical broker-visible identifier of the
    # strategy) so orphan positions/orders in MT5 — even those placed by a
    # previous service incarnation we lost track of — count as "already
    # fired today" and prevent duplicates.

    @staticmethod
    def _today_utc() -> str:
        return datetime.now(timezone.utc).date().isoformat()

    def has_fired_today(self, strategy_id_or_comment: str) -> bool:
        """True if any order with this key (comment or strategy_id) was
        already placed today (UTC).
        """
        return self._fired_today.get(strategy_id_or_comment) == self._today_utc()

    def _mark_fired_today(self, *keys: str) -> None:
        """Mark one or more keys (strategy_id + comment) as fired today."""
        today = self._today_utc()
        for k in keys:
            if k:
                self._fired_today[k] = today
        self._save_state()

    # ── Helpers MT5 ──────────────────────────────────────────────────────

    def _calc_lots(self, balance: float, entry: float, sl: float, sym_info) -> float:
        if sl <= 0 or entry <= 0 or sym_info is None:
            return 0.0
        risk_money = balance * self.risk_pct
        price_diff = abs(entry - sl)
        if price_diff <= 0:
            return 0.0
        tick_size = getattr(sym_info, "trade_tick_size", None) or getattr(sym_info, "point", 0.00001)
        tick_value = getattr(sym_info, "trade_tick_value", None) or 1.0
        vol_step = getattr(sym_info, "volume_step", 0.01) or 0.01
        vol_min = getattr(sym_info, "volume_min", 0.01) or 0.01
        if tick_size <= 0 or tick_value <= 0:
            return 0.0
        risk_per_lot = (price_diff / tick_size) * tick_value
        if risk_per_lot <= 0:
            return 0.0
        raw_lots = risk_money / risk_per_lot
        # Snap a vol_step
        lots = max(vol_min, round(raw_lots / vol_step) * vol_step)
        return float(lots)

    # ── Placement ────────────────────────────────────────────────────────

    def has_open_or_pending(self, symbol: str, strategy_id: str) -> bool:
        """Dedup: 1 trade por (strategy_id) en cualquier momento."""
        for p in self.open_positions.values():
            if p.strategy_id == strategy_id:
                return True
        for p in self.pending_orders.values():
            if p.strategy_id == strategy_id:
                return True
        return False

    def place_stop_long(
        self, *, symbol: str, sym_internal: str, strategy_id: str,
        setup_type: str, variant: str, stop_price: float,
        sl_price: float, tp_price: float, atr_or_risk: float,
        exit_rules: dict, expiration_minutes: int = 60,
        comment: str | None = None,
    ) -> Optional[int]:
        """Coloca STOP buy. Devuelve ticket o None."""
        if self.has_open_or_pending(symbol, strategy_id):
            return None
        if mt5 is None:
            print(f"[DRY] No MT5 module available, would place {strategy_id}")
            return None
        if not self.client.ensure_connected():
            print(f"[Traders mgr {self.magic}] MT5 not connected, skip place")
            return None

        bal = self.client.get_account_balance()
        if bal is None or bal <= 0:
            print(f"[Traders mgr {self.magic}] no balance, skip")
            return None
        sym_info = self.client.get_symbol_info(symbol)
        lots = self._calc_lots(bal, stop_price, sl_price, sym_info)
        if lots <= 0:
            print(f"[Traders mgr {self.magic}] lots=0 for {strategy_id}, skip")
            return None

        now = datetime.now(timezone.utc)
        expiration = now + timedelta(minutes=expiration_minutes)
        comment = comment or strategy_id[:31]

        if self.dry_run:
            ticket = -int(now.timestamp() % 1_000_000_000)
            print(f"[DRY][{self.magic}] would BUY_STOP {symbol} lots={lots} "
                  f"@ {stop_price:.5f} SL={sl_price:.5f} TP={tp_price:.5f} "
                  f"id={strategy_id}", flush=True)
        else:
            request = {
                "action": mt5.TRADE_ACTION_PENDING,
                "symbol": symbol,
                "volume": lots,
                "type": mt5.ORDER_TYPE_BUY_STOP,
                "price": self.client.normalize_price(symbol, stop_price),
                "sl": self.client.normalize_price(symbol, sl_price),
                "tp": self.client.normalize_price(symbol, tp_price),
                "magic": self.magic,
                "comment": comment,
                "type_filling": mt5.ORDER_FILLING_IOC,
                "type_time": mt5.ORDER_TIME_SPECIFIED,
                "expiration": int(expiration.timestamp()),
            }
            result = self.client.send_order_raw(request)
            if not result or result.get("retcode") not in (10009, 10010, 10008):
                rc = result.get("retcode") if result else "no_result"
                print(f"[Traders mgr {self.magic}] place STOP FAIL "
                      f"{strategy_id} rc={rc} price={stop_price:.5f}",
                      flush=True)
                return None
            ticket = result.get("order")

        # Track pending
        placed_us = int(now.timestamp() * 1_000_000)
        exp_us = int(expiration.timestamp() * 1_000_000)
        self.pending_orders[ticket] = TradersPendingOrder(
            ticket=ticket, magic=self.magic, symbol=symbol,
            sym_internal=sym_internal, strategy_id=strategy_id,
            setup_type=setup_type, variant=variant, direction="LONG",
            stop_price=stop_price, tp_price=tp_price, sl_price=sl_price,
            atr_or_risk=atr_or_risk, placed_us=placed_us,
            expiration_us=exp_us, exit_rules=exit_rules,
        )
        # Once-per-day gate: mark BOTH the strategy_id and the comment so
        # orphan-by-comment checks also resolve.
        self._mark_fired_today(strategy_id, comment)
        # Cache meta for notifications later (fill, partial, close)
        # Extract trader from strategy_id (TS_XAU_QULLAHTF_PDF -> Qulla, TO_WTI -> Qulla)
        trader_name = self._infer_trader(strategy_id, setup_type)
        self.strategy_meta[strategy_id] = {
            "trader": trader_name,
            "setup_type": setup_type,
            "variant": variant,
            "internal_sym": sym_internal,
            "broker_sym": symbol,
        }
        self._save_state()
        # Notify
        if self.notifier and ticket > 0:
            self.notifier.order_placed(
                strategy_id=strategy_id, trader=trader_name,
                setup_type=setup_type, variant=variant, magic=self.magic,
                broker_sym=symbol, internal_sym=sym_internal,
                entry=stop_price, sl=sl_price, tp=tp_price,
                lots=lots, ticket=ticket, expiration_minutes=expiration_minutes,
            )
        elif self.notifier and self.dry_run:
            self.notifier.order_placed(
                strategy_id=f"[DRY] {strategy_id}", trader=trader_name,
                setup_type=setup_type, variant=variant, magic=self.magic,
                broker_sym=symbol, internal_sym=sym_internal,
                entry=stop_price, sl=sl_price, tp=tp_price,
                lots=lots, ticket=ticket, expiration_minutes=expiration_minutes,
            )
        return ticket

    def place_market_long(
        self, *, symbol: str, sym_internal: str, strategy_id: str,
        setup_type: str, variant: str, ref_price: float,
        sl_price: float, tp_price: float, atr_or_risk: float,
        exit_rules: dict, comment: str | None = None,
    ) -> Optional[int]:
        """Coloca MARKET BUY (TRADE_ACTION_DEAL). Devuelve ticket de la posición
        resultante, o None.

        Usado por ORB strategy donde la entrada es post-breakout (precio
        ya cruzó r_high). ref_price es el nivel de referencia teórico
        (e.g. r_high) usado solo para logging; el fill real es al ask actual.
        """
        if self.has_open_or_pending(symbol, strategy_id):
            return None
        if mt5 is None:
            print(f"[DRY] No MT5 module, would MARKET {strategy_id}", flush=True)
            return None
        if not self.client.ensure_connected():
            print(f"[Traders mgr {self.magic}] MT5 not connected, skip MARKET",
                  flush=True)
            return None

        bal = self.client.get_account_balance()
        if bal is None or bal <= 0:
            print(f"[Traders mgr {self.magic}] no balance, skip", flush=True)
            return None
        sym_info = self.client.get_symbol_info(symbol)
        lots = self._calc_lots(bal, ref_price, sl_price, sym_info)
        if lots <= 0:
            print(f"[Traders mgr {self.magic}] lots=0 for {strategy_id}, skip",
                  flush=True)
            return None

        now = datetime.now(timezone.utc)
        comment = comment or strategy_id[:31]

        if self.dry_run:
            print(f"[DRY][{self.magic}] would MARKET_BUY {symbol} lots={lots} "
                  f"ref={ref_price:.5f} SL={sl_price:.5f} TP={tp_price:.5f} "
                  f"id={strategy_id}", flush=True)
            ticket = -int(now.timestamp() % 1_000_000_000)
        else:
            tick = mt5.symbol_info_tick(symbol)
            if tick is None or tick.ask <= 0:
                print(f"[Traders mgr {self.magic}] {strategy_id}: no tick, "
                      f"skip", flush=True)
                return None
            ask = float(tick.ask)
            bid = float(tick.bid)
            spread = max(ask - bid, 0.0)
            # Enforce a SAFE minimum stop distance to avoid INVALID_STOPS
            # (10016). Vantage's freeze_level + spread on energies can be
            # larger than stops_level alone. Use the MAX of:
            #   - 2× broker stops_level × point (broker hard min × 2)
            #   - 3× spread (clear of bid-ask buffer)
            #   - 0.1% of ask (price-relative floor for thin instruments)
            point = float(getattr(sym_info, "point", 0)) if sym_info else 0
            stops_lvl_pts = float(getattr(sym_info, "trade_stops_level", 0) or 0) if sym_info else 0
            min_stop_dist = max(
                2.0 * stops_lvl_pts * point,
                3.0 * spread,
                0.001 * ask,
            )
            if min_stop_dist > 0:
                orig_sl, orig_tp = sl_price, tp_price
                if (ask - sl_price) < min_stop_dist:
                    sl_price = ask - min_stop_dist
                if (tp_price - ask) < min_stop_dist:
                    tp_price = ask + min_stop_dist
                if sl_price != orig_sl or tp_price != orig_tp:
                    print(f"[Traders mgr {self.magic}] {strategy_id}: "
                          f"min_dist={min_stop_dist:.5f} (stops_lvl*pt="
                          f"{stops_lvl_pts*point:.5f} spread={spread:.5f} "
                          f"0.1%ask={0.001*ask:.5f}) -> "
                          f"sl={sl_price:.5f} tp={tp_price:.5f}", flush=True)
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lots,
                "type": mt5.ORDER_TYPE_BUY,
                "price": self.client.normalize_price(symbol, ask),
                "sl": self.client.normalize_price(symbol, sl_price),
                "tp": self.client.normalize_price(symbol, tp_price),
                "deviation": 20,
                "magic": self.magic,
                "comment": comment,
                "type_filling": mt5.ORDER_FILLING_IOC,
                "type_time": mt5.ORDER_TIME_GTC,
            }
            result = self.client.send_order_raw(request)
            if not result or result.get("retcode") not in (10009, 10010, 10008):
                rc = result.get("retcode") if result else "no_result"
                print(f"[Traders mgr {self.magic}] place MARKET FAIL "
                      f"{strategy_id} rc={rc} ask={ask:.5f}", flush=True)
                return None
            ticket = result.get("order", -1)
            # For MARKET DEAL, the actual position ticket is in result.deal
            # or we fetch it via positions_get filtered by comment shortly
            print(f"[Traders mgr {self.magic}] place MARKET OK "
                  f"{strategy_id} fill_ref={ask:.5f} order_id={ticket}",
                  flush=True)

        # Track in pending_orders so reconcile_with_broker will pick up the
        # actual position on next tick and emit the fill notification.
        placed_us = int(now.timestamp() * 1_000_000)
        self.pending_orders[ticket] = TradersPendingOrder(
            ticket=ticket, magic=self.magic, symbol=symbol,
            sym_internal=sym_internal, strategy_id=strategy_id,
            setup_type=setup_type, variant=variant, direction="LONG",
            stop_price=ref_price, tp_price=tp_price, sl_price=sl_price,
            atr_or_risk=atr_or_risk, placed_us=placed_us,
            # No real expiration on a market deal — set far future as marker.
            expiration_us=placed_us + 24 * 3600 * 1_000_000,
            exit_rules=exit_rules,
        )
        # Once-per-day gate: mark BOTH the strategy_id and the comment so
        # orphan-by-comment checks also resolve.
        self._mark_fired_today(strategy_id, comment)
        trader_name = self._infer_trader(strategy_id, setup_type)
        self.strategy_meta[strategy_id] = {
            "trader": trader_name, "setup_type": setup_type,
            "variant": variant, "internal_sym": sym_internal,
            "broker_sym": symbol,
        }
        self._save_state()
        if self.notifier and ticket > 0:
            try:
                self.notifier.order_placed(
                    strategy_id=strategy_id, trader=trader_name,
                    setup_type=setup_type, variant=variant, magic=self.magic,
                    broker_sym=symbol, internal_sym=sym_internal,
                    entry=ref_price, sl=sl_price, tp=tp_price,
                    lots=lots, ticket=int(ticket),
                )
            except Exception as e:
                # Don't let notifier error fail the placement — order is in
                # MT5 already, we just lost the Telegram event.
                print(f"[Traders mgr {self.magic}] notifier.order_placed "
                      f"error (non-fatal): {e}", flush=True)
        return ticket

    @staticmethod
    def _infer_trader(strategy_id: str, setup_type: str) -> str:
        """De TS_<SYM>_QULLAHTF_PDF / TO_<SYM>_<...> -> trader name."""
        sid_up = strategy_id.upper()
        if "MINERVINI" in sid_up:
            return "Minervini"
        if "ZANGER" in sid_up or setup_type in ("FLAG", "CUP"):
            return "Zanger"
        if "QULLAHTF" in sid_up or "QULLA" in sid_up or setup_type in ("HTF", "EP", "ORB"):
            return "Qulla"
        if "RYAN" in sid_up or "ANTS" in sid_up:
            return "Ryan"
        return "Unknown"

    # ── Reconciliation: pending -> open on fill, cleanup closed ──────────

    def reconcile_with_broker(self):
        """Sync: detectar fills (pending -> open), cierres (open -> remove).

        Also adopts ORPHAN broker positions/orders (those in MT5 but not
        tracked by the bot) so they count toward the once-per-day gate and
        don't get duplicated on the next breakout tick.
        """
        if mt5 is None or not self.client.ensure_connected():
            return

        # 1) Pending orders del broker (filtrados por magic)
        broker_pending = {o.ticket: o for o in (mt5.orders_get(magic=self.magic) or [])}

        # 2) Posiciones abiertas
        broker_pos = {p.ticket: p for p in (mt5.positions_get() or []) if p.magic == self.magic}

        # 0) ORPHAN ADOPTION: positions/orders in broker but not in our state.
        # Mark by COMMENT (broker-visible strategy ID) so when the bot next
        # tries to place with the same comment, has_fired_today blocks it.
        today = self._today_utc()
        for p in broker_pos.values():
            if p.ticket in self.open_positions:
                continue
            comment = str(getattr(p, "comment", "")).strip()
            if comment and self._fired_today.get(comment) != today:
                opened = datetime.fromtimestamp(int(p.time), tz=timezone.utc).date().isoformat()
                if opened == today:
                    self._fired_today[comment] = today
                    print(f"[Traders mgr {self.magic}] adopted orphan POS "
                          f"{p.ticket} ({p.symbol}) cmt='{comment}' -> mark fired_today",
                          flush=True)
        for o in broker_pending.values():
            if o.ticket in self.pending_orders:
                continue
            comment = str(getattr(o, "comment", "")).strip()
            if comment and self._fired_today.get(comment) != today:
                placed = datetime.fromtimestamp(int(o.time_setup), tz=timezone.utc).date().isoformat()
                if placed == today:
                    self._fired_today[comment] = today
                    print(f"[Traders mgr {self.magic}] adopted orphan ORD "
                          f"{o.ticket} ({o.symbol}) cmt='{comment}' -> mark fired_today",
                          flush=True)

        # 3) Pendings que ya no estan en broker -> FILL o CANCEL
        for ticket, pend in list(self.pending_orders.items()):
            if ticket in broker_pending:
                continue  # sigue pendiente
            # Buscar posicion abierta con mismo comment o cercana
            matched_pos = None
            for p in broker_pos.values():
                if p.comment[:31] == strategy_comment(pend) or self._comment_matches(p.comment, pend):
                    matched_pos = p
                    break
            if matched_pos is not None and matched_pos.ticket not in self.open_positions:
                entry_us = int(matched_pos.time_msc * 1000)
                op = TradersOpenPosition(
                    ticket=matched_pos.ticket, magic=self.magic,
                    symbol=pend.symbol, sym_internal=pend.sym_internal,
                    strategy_id=pend.strategy_id, setup_type=pend.setup_type,
                    variant=pend.variant, direction=pend.direction,
                    entry_price=float(matched_pos.price_open),
                    initial_volume=float(matched_pos.volume),
                    remaining_volume=float(matched_pos.volume),
                    initial_sl=pend.sl_price, current_sl=pend.sl_price,
                    initial_atr_or_risk=pend.atr_or_risk,
                    entry_time_us=entry_us,
                    exit_rules=pend.exit_rules,
                )
                self.open_positions[matched_pos.ticket] = op
                print(f"[Traders mgr {self.magic}] FILLED {pend.strategy_id} "
                      f"@ {matched_pos.price_open}")
                if self.notifier:
                    trader = self._infer_trader(pend.strategy_id, pend.setup_type)
                    self.notifier.fill(
                        strategy_id=pend.strategy_id, trader=trader,
                        setup_type=pend.setup_type, variant=pend.variant,
                        magic=self.magic, broker_sym=pend.symbol,
                        internal_sym=pend.sym_internal,
                        entry=float(matched_pos.price_open),
                        lots=float(matched_pos.volume),
                        ticket=int(matched_pos.ticket),
                    )
            else:
                print(f"[Traders mgr {self.magic}] pending {ticket} ({pend.strategy_id}) "
                      f"expired/cancelled without fill")
            del self.pending_orders[ticket]

        # 4) Open positions que ya no estan en broker -> cerradas
        for ticket in list(self.open_positions.keys()):
            if ticket not in broker_pos:
                op = self.open_positions[ticket]
                print(f"[Traders mgr {self.magic}] CLOSED {op.strategy_id} ticket={ticket}")
                if self.notifier:
                    trader = self._infer_trader(op.strategy_id, op.setup_type)
                    # No tenemos exit price exacto del broker en este path; el reason
                    # ya se notifico desde _close_position(). Solo emite si no hay
                    # cierre programado (broker auto-cerro TP/SL).
                    self.notifier.position_closed(
                        strategy_id=op.strategy_id, trader=trader,
                        setup_type=op.setup_type, variant=op.variant,
                        magic=self.magic, broker_sym=op.symbol,
                        internal_sym=op.sym_internal,
                        reason="BROKER_CLOSE",
                        hold_minutes=None, final_r=None,
                    )
                del self.open_positions[ticket]
            else:
                # Actualizar remaining_volume si el broker tiene menos (partial parcial)
                self.open_positions[ticket].remaining_volume = float(broker_pos[ticket].volume)

        self._save_state()

    def _comment_matches(self, broker_comment: str, pend: TradersPendingOrder) -> bool:
        # match laxo por strategy_id en el comment (los primeros chars)
        return pend.strategy_id[:20] in broker_comment or broker_comment[:20] in pend.strategy_id

    # ── Active management: partials, trail, max_hold ─────────────────────

    def manage_open_positions(self, daily_sma_cache: dict | None = None):
        """Llamar cada N segundos. Maneja partials y trail por SMA D1 + max_hold.

        Args:
            daily_sma_cache: dict {symbol: {sma10, sma20, sma50}} con valores
                D1 close del DIA ANTERIOR (causal). Si None, sin trail.
        """
        if mt5 is None or not self.open_positions:
            return
        if not self.client.ensure_connected():
            return
        now_us = int(datetime.now(timezone.utc).timestamp() * 1_000_000)
        day_us = 86_400 * 1_000_000

        for ticket, op in list(self.open_positions.items()):
            tick = mt5.symbol_info_tick(op.symbol)
            if tick is None:
                continue
            bid = tick.bid
            ask = tick.ask
            cur_price = bid  # cerrar long usa bid

            risk = op.initial_atr_or_risk
            if risk <= 0:
                continue
            r_mult = (cur_price - op.entry_price) / risk

            days_held = (now_us - op.entry_time_us) // day_us
            hours_held = (now_us - op.entry_time_us) / 3_600_000_000

            rules = op.exit_rules
            partials = rules.get("partials", [])

            # Process pending partials
            for idx, partial in enumerate(partials):
                if idx in op.partials_taken:
                    continue
                trigger = partial.get("trigger")
                val = partial.get("value")
                sell_frac = partial.get("sell_frac", 0.0)
                triggered = False
                if trigger == "r_multiple":
                    if r_mult >= float(val):
                        triggered = True
                elif trigger == "pct_from_entry":
                    if cur_price >= op.entry_price * (1.0 + float(val)):
                        triggered = True
                elif trigger == "days_held":
                    if days_held >= int(val):
                        triggered = True
                if triggered:
                    self._send_partial_close(op, sell_frac,
                                              partial_idx=idx, trigger=trigger,
                                              trigger_value=val,
                                              r_mult_now=r_mult)
                    op.partials_taken.append(idx)
                    op.tp1_hit = True

            # Trailing SMA post-primer-partial
            trail_sma = rules.get("trail_sma")
            if op.tp1_hit and trail_sma and daily_sma_cache:
                sma_key = f"sma{trail_sma}"
                sma_val = (daily_sma_cache.get(op.sym_internal) or {}).get(sma_key)
                if sma_val and sma_val > op.current_sl:
                    self._update_sl(op, float(sma_val), sma_period=int(trail_sma))

            # Time-stop (Zanger)
            time_stop = rules.get("time_stop_days")
            if time_stop and not op.tp1_hit and days_held >= int(time_stop):
                print(f"[Traders mgr {self.magic}] TIME_STOP {op.strategy_id} "
                      f"days_held={days_held}")
                self._close_position(op, "TIME_STOP")
                continue

            # Max hold
            max_d = rules.get("max_hold_days")
            max_h = rules.get("max_hold_hours")
            if max_h and hours_held >= float(max_h):
                self._close_position(op, "MAX_HOLD")
                continue
            if max_d and days_held >= int(max_d):
                self._close_position(op, "MAX_HOLD")
                continue

            op.last_state_check_us = now_us
        self._save_state()

    def _send_partial_close(self, op: TradersOpenPosition, sell_frac: float,
                             partial_idx: int = 0, trigger: str = "",
                             trigger_value=None, r_mult_now: float = 0.0):
        if sell_frac <= 0 or op.remaining_volume <= 0:
            return
        close_vol = round(op.initial_volume * sell_frac, 2)
        if close_vol > op.remaining_volume:
            close_vol = op.remaining_volume
        if close_vol <= 0:
            return
        if self.dry_run:
            print(f"[DRY][{self.magic}] partial close {op.strategy_id} {close_vol} lots "
                  f"(frac={sell_frac:.2f})")
            op.remaining_volume -= close_vol
            if self.notifier:
                trader = self._infer_trader(op.strategy_id, op.setup_type)
                tick = mt5.symbol_info_tick(op.symbol) if mt5 else None
                px = tick.bid if tick else op.entry_price
                self.notifier.partial_close(
                    strategy_id=op.strategy_id, trader=trader, magic=self.magic,
                    broker_sym=op.symbol, internal_sym=op.sym_internal,
                    partial_idx=partial_idx, trigger=trigger,
                    trigger_value=trigger_value, fill_price=px,
                    closed_lots=close_vol, remaining_lots=op.remaining_volume,
                    r_multiple=r_mult_now,
                )
            return
        tick = mt5.symbol_info_tick(op.symbol)
        if tick is None:
            return
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": op.symbol,
            "volume": close_vol,
            "type": mt5.ORDER_TYPE_SELL,
            "position": op.ticket,
            "price": tick.bid,
            "magic": self.magic,
            "comment": f"P|{op.strategy_id[:24]}"[:31],
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = self.client.send_order_raw(request)
        rc = result.get("retcode") if result else None
        if rc in (10009, 10010, 10008):
            op.remaining_volume = max(0.0, op.remaining_volume - close_vol)
            print(f"[Traders mgr {self.magic}] PARTIAL CLOSE {op.strategy_id} "
                  f"{close_vol} lots, remaining={op.remaining_volume}")
            if self.notifier:
                trader = self._infer_trader(op.strategy_id, op.setup_type)
                self.notifier.partial_close(
                    strategy_id=op.strategy_id, trader=trader, magic=self.magic,
                    broker_sym=op.symbol, internal_sym=op.sym_internal,
                    partial_idx=partial_idx, trigger=trigger,
                    trigger_value=trigger_value, fill_price=float(tick.bid),
                    closed_lots=close_vol, remaining_lots=op.remaining_volume,
                    r_multiple=r_mult_now,
                )
        else:
            print(f"[Traders mgr {self.magic}] partial close FAIL rc={rc}")
            if self.notifier:
                self.notifier.order_rejected(
                    strategy_id=op.strategy_id, magic=self.magic,
                    broker_sym=op.symbol, reason=f"partial_close rc={rc}",
                )

    def _update_sl(self, op: TradersOpenPosition, new_sl: float, sma_period: int = 0):
        if new_sl <= op.current_sl:
            return
        old_sl = op.current_sl
        if self.dry_run:
            print(f"[DRY][{self.magic}] update SL {op.strategy_id} "
                  f"{old_sl:.5f} -> {new_sl:.5f}")
            op.current_sl = new_sl
            if self.notifier:
                self.notifier.trail_update(
                    strategy_id=op.strategy_id, magic=self.magic,
                    broker_sym=op.symbol, old_sl=old_sl, new_sl=new_sl,
                    sma_period=sma_period,
                )
            return
        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": op.ticket,
            "sl": self.client.normalize_price(op.symbol, new_sl),
            "tp": 0.0,
            "magic": self.magic,
        }
        result = self.client.send_order_raw(request)
        rc = result.get("retcode") if result else None
        if rc in (10009, 10010, 10008):
            op.current_sl = new_sl
            print(f"[Traders mgr {self.magic}] TRAIL SL {op.strategy_id} -> {new_sl:.5f}")
            if self.notifier:
                self.notifier.trail_update(
                    strategy_id=op.strategy_id, magic=self.magic,
                    broker_sym=op.symbol, old_sl=old_sl, new_sl=new_sl,
                    sma_period=sma_period,
                )

    def _close_position(self, op: TradersOpenPosition, reason: str):
        trader = self._infer_trader(op.strategy_id, op.setup_type)
        # Compute final R-multiple from current price
        tick = mt5.symbol_info_tick(op.symbol) if mt5 else None
        cur_price = tick.bid if tick else op.entry_price
        risk = op.initial_atr_or_risk if op.initial_atr_or_risk > 0 else 1.0
        final_r = (cur_price - op.entry_price) / risk
        hold_min = int((datetime.now(timezone.utc).timestamp() * 1_000_000
                          - op.entry_time_us) / 60_000_000)
        if self.dry_run:
            print(f"[DRY][{self.magic}] close {op.strategy_id} reason={reason}")
            if self.notifier:
                self.notifier.position_closed(
                    strategy_id=op.strategy_id, trader=trader,
                    setup_type=op.setup_type, variant=op.variant,
                    magic=self.magic, broker_sym=op.symbol,
                    internal_sym=op.sym_internal, reason=reason,
                    final_r=final_r, hold_minutes=hold_min,
                )
            return
        if tick is None:
            return
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": op.symbol,
            "volume": op.remaining_volume,
            "type": mt5.ORDER_TYPE_SELL,
            "position": op.ticket,
            "price": tick.bid,
            "magic": self.magic,
            "comment": f"X|{reason[:5]}|{op.strategy_id[:18]}"[:31],
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = self.client.send_order_raw(request)
        rc = result.get("retcode") if result else None
        print(f"[Traders mgr {self.magic}] CLOSE {op.strategy_id} reason={reason} rc={rc}")
        if self.notifier:
            self.notifier.position_closed(
                strategy_id=op.strategy_id, trader=trader,
                setup_type=op.setup_type, variant=op.variant,
                magic=self.magic, broker_sym=op.symbol,
                internal_sym=op.sym_internal, reason=reason,
                final_r=final_r, hold_minutes=hold_min,
            )


def strategy_comment(pend: TradersPendingOrder) -> str:
    return pend.strategy_id[:31]
