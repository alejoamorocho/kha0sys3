"""Traders Live Engine — Tier 1 Swing (magic 1339) + Tier 2 ORB (magic 1340).

Engine unificado que carga ambos configs y opera en paralelo. Magic separa
contabilidad pero todo corre en 1 servicio NSSM (Kha0sysTradersBot) para
simplicidad operativa.

Flujo cada 60s:
  1) ensure MT5 connected
  2) reconcile pending->open / closed (ambos managers)
  3) Swing: cada vez que cambia el dia UTC, refresh D1 cache + ejecutar
     detectores swing -> actualizar lista de setups activos.
     En cada tick, para cada setup activo: si current_price > pivot,
     place BUY_STOP @ pivot.
  4) ORB: para cada strategy, computar opening range del dia en curso.
     Despues del range_end, monitorear M1 close > range_high -> place STOP.
  5) manage_open_positions en ambos managers (partials, trail, max_hold)
  6) Persist state

Argumentos:
  --live      ejecuta order_send real
  --dry-run   solo log, no envia ordenes (default)
"""
from __future__ import annotations

import argparse
import json
import signal
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import polars as pl

try:
    import MetaTrader5 as mt5  # type: ignore
except Exception:
    mt5 = None  # type: ignore

from src.domain.constants import (
    MAGIC_NUMBER_TRADERS_SWING, MAGIC_NUMBER_TRADERS_ORB,
)
from src.execution.mt5_client import MT5Client
from src.execution.traders_order_manager import (
    TradersOrderManager, make_swing_comment, make_orb_comment,
)
from src.engine.traders_setups import add_indicators, resample_to_daily
from src.engine.traders_swing import SWING_DETECTORS
from src.infrastructure.symbol_mapper import SymbolMapper
from src.monitoring.traders_notifier import TradersNotifier

SWING_CONFIG = Path("src/execution/bot_config_traders_swing.json")
ORB_CONFIG = Path("src/execution/bot_config_traders_orb.json")
HEARTBEAT_FILE = Path("logs/traders_bot_heartbeat")
HEARTBEAT_FILE.parent.mkdir(parents=True, exist_ok=True)

POLL_SECONDS = 60
M1_BARS_LOOKBACK = 600     # 10 horas M1 (suficiente para ORB intradia)
D1_BARS_LOOKBACK = 300     # 300 dias (suficiente para SMA200 + detectores)
# Vantage broker es EEST (UTC+3) en verano / EET (UTC+2) en invierno. MT5
# retorna bar.time como epoch BROKER (sumado el offset). Mi backtest cache
# esta en UTC real, asi que en live convertimos restando el offset detectado
# del tick fresco vs UTC now.
BROKER_OFFSET_FALLBACK_H = 3


_stop = False


def _on_signal(signum, frame):
    global _stop
    print(f"\n[TradersEngine] signal {signum} -> shutdown")
    _stop = True


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _now_us() -> int:
    return int(_now_utc().timestamp() * 1_000_000)


def _load_config(p: Path) -> dict:
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


_TICK_FRESHNESS_MAX_SEC = 300  # 5 min — same convention as MATH bot


def detect_broker_offset_hours(client: MT5Client, probe_symbol: str,
                                current_offset_h: int | None = None) -> int:
    """Detecta offset broker vs UTC via tick reciente.

    Returns: horas enteras (positivo = broker adelantado vs UTC).
    Si no hay tick fresco (>5min), retorna current_offset_h o
    BROKER_OFFSET_FALLBACK_H.

    BUG FIX 2026-05-16: previa versión devolvía delta sobre tick stale, lo
    cual hacía drift -1h/hora durante fines de semana / mercados cerrados.
    Ahora se respeta el offset previo cuando el tick no es fresco.
    """
    fallback = current_offset_h if current_offset_h is not None else BROKER_OFFSET_FALLBACK_H
    if mt5 is None:
        return fallback
    # Probar múltiples símbolos para mayor robustez (igual que MATH bot)
    candidates = [probe_symbol, "EURUSD+", "XAUUSD+", "XAGUSD", "GBPUSD+", "AUDUSD+"]
    best_delta = None
    best_age = float("inf")
    now_utc_epoch = int(datetime.now(timezone.utc).timestamp())
    for sym in candidates:
        try:
            tick = mt5.symbol_info_tick(sym)
            if tick is None or tick.time == 0:
                continue
            age = abs(now_utc_epoch - int(tick.time))
            if age > _TICK_FRESHNESS_MAX_SEC:
                continue
            if age < best_age:
                best_age = age
                best_delta = (int(tick.time) - now_utc_epoch) / 3600.0
        except Exception:
            continue
    if best_delta is None:
        # No fresh tick available — keep previous offset (no drift)
        return fallback
    return int(round(best_delta))


def _fetch_m1_bars(client: MT5Client, broker_symbol: str,
                    broker_offset_h: int, n: int = M1_BARS_LOOKBACK) -> pl.DataFrame | None:
    """Fetch M1 desde MT5 y convierte timestamps a UTC real (resta offset broker)."""
    if mt5 is None or not client.ensure_connected():
        return None
    try:
        # Asegurar simbolo en Market Watch
        si = mt5.symbol_info(broker_symbol)
        if si is not None and not si.select:
            mt5.symbol_select(broker_symbol, True)
        rates = mt5.copy_rates_from_pos(broker_symbol, mt5.TIMEFRAME_M1, 0, n)
        if rates is None or len(rates) == 0:
            return None
        offset_sec = broker_offset_h * 3600
        df = pl.DataFrame({
            "time": [datetime.fromtimestamp(int(r["time"]) - offset_sec, tz=timezone.utc).replace(tzinfo=None) for r in rates],
            "open": [float(r["open"]) for r in rates],
            "high": [float(r["high"]) for r in rates],
            "low": [float(r["low"]) for r in rates],
            "close": [float(r["close"]) for r in rates],
            "volume": [float(r["tick_volume"]) for r in rates],
        }).sort("time")
        return df
    except Exception as e:
        print(f"[TradersEngine] fetch M1 {broker_symbol} FAIL: {e}")
        return None


def _fetch_d1_bars(client: MT5Client, broker_symbol: str,
                    broker_offset_h: int, n: int = D1_BARS_LOOKBACK) -> pl.DataFrame | None:
    """Fetch D1 desde MT5 y convierte timestamps a UTC real.

    NOTA: las velas D1 del broker abren a 00:00 broker = 21:00 UTC prev day.
    Tras la conversion, la "fecha" de cada bar es el dia broker - 1 si offset>0.
    Esto es OK para detectores tipo VCP/HTF (pattern-based, no session-based).
    """
    if mt5 is None or not client.ensure_connected():
        return None
    try:
        si = mt5.symbol_info(broker_symbol)
        if si is not None and not si.select:
            mt5.symbol_select(broker_symbol, True)
        rates = mt5.copy_rates_from_pos(broker_symbol, mt5.TIMEFRAME_D1, 0, n)
        if rates is None or len(rates) == 0:
            return None
        offset_sec = broker_offset_h * 3600
        df = pl.DataFrame({
            "time": [datetime.fromtimestamp(int(r["time"]) - offset_sec, tz=timezone.utc).replace(tzinfo=None) for r in rates],
            "open": [float(r["open"]) for r in rates],
            "high": [float(r["high"]) for r in rates],
            "low": [float(r["low"]) for r in rates],
            "close": [float(r["close"]) for r in rates],
            "volume": [float(r["tick_volume"]) for r in rates],
        }).sort("time")
        return df
    except Exception as e:
        print(f"[TradersEngine] fetch D1 {broker_symbol} FAIL: {e}")
        return None


# ── Swing setup cache ────────────────────────────────────────────────────


class SwingState:
    """Setups D1 activos por strategy con valid_until.

    Estructura: {strategy_id: list[dict(date_signal, pivot_high, base_low, atr_d1, valid_until)]}
    """
    def __init__(self):
        self.active_setups: dict[str, list[dict]] = {}
        self.last_refresh_date: dict[str, str] = {}    # strategy_id -> 'YYYY-MM-DD'

    def needs_refresh(self, strategy_id: str, today_str: str) -> bool:
        return self.last_refresh_date.get(strategy_id) != today_str

    def set_active(self, strategy_id: str, rows: list[dict], today_str: str):
        self.active_setups[strategy_id] = rows
        self.last_refresh_date[strategy_id] = today_str

    def prune_expired(self, strategy_id: str, today_date):
        rows = self.active_setups.get(strategy_id, [])
        kept = [r for r in rows if r["valid_until"] >= today_date]
        self.active_setups[strategy_id] = kept


# ── ORB state ────────────────────────────────────────────────────────────


class ORBState:
    """Tracking de opening range por (strategy_id, fecha)."""
    def __init__(self):
        # key = (strategy_id, date_str) -> {range_high, range_low, range_end_dt, breakout_fired}
        self.ranges: dict[tuple[str, str], dict] = {}


# ── Engine principal ────────────────────────────────────────────────────


class TradersEngine:
    def __init__(self, live: bool = False):
        self.live = live
        self.dry_run = not live
        # attach_only=True: TradersBot comparte el terminal MT5 con MathBot.
        # Solo attach a la sesion ya autenticada, NO re-login (eso fallaria).
        self.client = MT5Client(attach_only=True)
        self.swing_cfg = _load_config(SWING_CONFIG)
        self.orb_cfg = _load_config(ORB_CONFIG)
        self.swing_strategies = self.swing_cfg["portfolio"]
        self.orb_strategies = self.orb_cfg["portfolio"]
        self.risk_pct = float(self.swing_cfg.get("risk_per_trade", 0.001))
        # Notifier compartido entre ambos managers (envia a Telegram con prefijo [TRADERS])
        self.notifier = TradersNotifier(risk_percent=self.risk_pct)
        self.mgr_swing = TradersOrderManager(
            self.client, MAGIC_NUMBER_TRADERS_SWING,
            risk_pct=self.risk_pct, dry_run=self.dry_run,
            notifier=self.notifier,
        )
        self.mgr_orb = TradersOrderManager(
            self.client, MAGIC_NUMBER_TRADERS_ORB,
            risk_pct=self.risk_pct, dry_run=self.dry_run,
            notifier=self.notifier,
        )
        self.swing_state = SwingState()
        self.orb_state = ORBState()
        # daily SMA cache for trail: {sym_internal: {sma10, sma20, sma50}}
        self.daily_sma_cache: dict[str, dict] = {}
        self.mapper = SymbolMapper()
        self.broker_offset_h: int = BROKER_OFFSET_FALLBACK_H  # se refresca al arrancar

    def connect(self) -> bool:
        return self.client.connect()

    # ── Swing logic ──────────────────────────────────────────────────────

    def _refresh_swing_setups(self, sym_internal: str, today_str: str):
        """Para cada swing strategy del symbol (internal name), refresca setups."""
        strategies_for_sym = [s for s in self.swing_strategies if s["sym"] == sym_internal]
        if not strategies_for_sym:
            return
        broker_sym = self.mapper.to_mt5(sym_internal)
        d1 = _fetch_d1_bars(self.client, broker_sym, self.broker_offset_h, D1_BARS_LOOKBACK)
        if d1 is None or len(d1) < 200:
            return
        d1_enr = add_indicators(d1)
        # Update SMA cache (last D1 close's SMAs for trail)
        last = d1_enr.tail(1).to_dicts()[0] if len(d1_enr) > 0 else None
        if last:
            self.daily_sma_cache[sym_internal] = {
                "sma10": last.get("sma10"),
                "sma20": last.get("sma20"),
                "sma50": last.get("sma50"),
            }
        for strat in strategies_for_sym:
            sid = strat["id"]
            if not self.swing_state.needs_refresh(sid, today_str):
                continue
            setup_type = strat["setup_type"]
            valid_days = int(strat.get("valid_days", 5))
            # Map setup_type -> detector
            detector_key = f"{strat['trader']}_{setup_type}"
            detector = SWING_DETECTORS.get(detector_key)
            if detector is None:
                # also try Qulla_HTF / Zanger_FLAG / Zanger_CUP
                detector = SWING_DETECTORS.get(setup_type) or None
            if detector is None:
                continue
            try:
                setups = detector(d1_enr, valid_days=valid_days)
            except Exception as e:
                print(f"[TradersEngine][swing] {sid} detector FAIL: {e}")
                continue
            if len(setups) == 0:
                self.swing_state.set_active(sid, [], today_str)
                continue
            # Only keep setups whose valid window includes TODAY
            today = datetime.strptime(today_str, "%Y-%m-%d").date()
            rows = []
            for r in setups.iter_rows(named=True):
                ds = r["date_signal"]
                if hasattr(ds, "date"):
                    ds = ds.date()
                vu = ds + timedelta(days=valid_days)
                if vu < today:
                    continue
                rows.append({
                    "date_signal": ds,
                    "pivot_high": float(r["pivot_high"]),
                    "base_low": float(r["base_low"]) if r["base_low"] else 0.0,
                    "atr_d1": float(r["atr_d1"]) if r["atr_d1"] else 0.0,
                    "valid_until": vu,
                })
            previous_rows = self.swing_state.active_setups.get(sid, [])
            self.swing_state.set_active(sid, rows, today_str)
            if rows:
                print(f"[TradersEngine][swing] {sid}: {len(rows)} active setups, "
                      f"latest pivot={rows[-1]['pivot_high']:.5f}")
                # Telegram: notify only if there's a NEW setup not seen in previous_rows
                prev_dates = {r["date_signal"] for r in previous_rows}
                new_setups = [r for r in rows if r["date_signal"] not in prev_dates]
                if new_setups:
                    latest = new_setups[-1]
                    broker_sym = self.mapper.to_mt5(strat["sym"])
                    self.notifier.setup_detected(
                        strategy_id=sid, trader=strat["trader"],
                        setup_type=strat["setup_type"], variant=strat["variant"],
                        magic=MAGIC_NUMBER_TRADERS_SWING,
                        broker_sym=broker_sym, internal_sym=strat["sym"],
                        pivot=latest["pivot_high"], atr_d1=latest["atr_d1"],
                        valid_until=str(latest["valid_until"]),
                        n_active=len(rows),
                    )

    def _check_swing_breakouts(self):
        """En cada tick, para cada swing strategy: si current price > pivot, place STOP."""
        for strat in self.swing_strategies:
            sid = strat["id"]
            rows = self.swing_state.active_setups.get(sid, [])
            if not rows:
                continue
            broker_sym = self.mapper.to_mt5(strat["sym"])
            if self.mgr_swing.has_open_or_pending(broker_sym, sid):
                continue
            tick = mt5.symbol_info_tick(broker_sym) if mt5 else None
            if tick is None:
                continue
            cur_price = tick.ask
            # Use the LATEST setup (most recent pivot)
            r = rows[-1]
            pivot = r["pivot_high"]
            atr = r["atr_d1"]
            if atr <= 0 or pivot <= 0:
                continue
            # If current price is at/above pivot, breakout already happened. Skip.
            if cur_price >= pivot:
                continue
            # NEW GUARD: si el precio esta DEMASIADO lejos del pivot
            # (mas del 2*ATR_D1 abajo), el setup ya quedo invalido — el
            # mercado se alejo del area de breakout. Evita spammear STOPs
            # que nunca se llenan.
            gap = pivot - cur_price
            if gap > 2.0 * atr:
                continue
            # Compute SL/TP per exit_rules
            exit_r = strat["exit_rules"]
            sl_type = exit_r.get("initial_sl_type")
            if sl_type == "pct":
                sl = pivot * (1.0 - float(exit_r["initial_sl_pct"]))
                risk = pivot - sl
            else:
                sl_atr = float(exit_r.get("initial_sl_atr_mult") or 1.0)
                risk = sl_atr * atr
                sl = pivot - risk
            # TP1 = primer partial r_multiple o pct
            partials = exit_r.get("partials", [])
            first_partial = next(
                (p for p in partials if p.get("trigger") in ("r_multiple", "pct_from_entry")),
                None,
            )
            if first_partial is None or first_partial["trigger"] == "days_held":
                tp = pivot + 2.0 * risk
            elif first_partial["trigger"] == "r_multiple":
                tp = pivot + float(first_partial["value"]) * risk
            else:  # pct
                tp = pivot * (1.0 + float(first_partial["value"]))

            comment = make_swing_comment(strat["setup_type"], strat["variant"], strat["sym"])
            # BUG FIX 2026-05-16: previous hardcoded expiration_minutes=4h
            # killed swing STOP orders before they could fill. Swing setups
            # are D1-level — they should remain valid for valid_days
            # (default 5 = 7200 min). Cap at 7 days as a safety upper bound.
            valid_days = max(1, int(strat.get("valid_days", 5)))
            expiration_min = min(7, valid_days) * 24 * 60
            self.mgr_swing.place_stop_long(
                symbol=broker_sym, sym_internal=strat["internal_sym"],
                strategy_id=sid, setup_type=strat["setup_type"],
                variant=strat["variant"], stop_price=pivot, sl_price=sl,
                tp_price=tp, atr_or_risk=risk, exit_rules=exit_r,
                expiration_minutes=expiration_min,
                comment=comment,
            )

    # ── ORB logic ────────────────────────────────────────────────────────

    def _process_orb(self, sym_internal: str):
        broker_sym = self.mapper.to_mt5(sym_internal)
        m1 = _fetch_m1_bars(self.client, broker_sym, self.broker_offset_h, M1_BARS_LOOKBACK)
        if m1 is None or len(m1) < 60:
            return
        today_str = m1.tail(1)["time"][0].strftime("%Y-%m-%d") if len(m1) else None
        # ATR M1 14 for sizing
        last_rows = m1.tail(20)
        if len(last_rows) < 14:
            return
        # Compute simple ATR proxy: avg(bar_range) last 14
        last14 = m1.tail(14)
        atr_m1 = float((last14["high"] - last14["low"]).mean())
        if atr_m1 <= 0:
            return

        strategies_for_sym = [s for s in self.orb_strategies if s["sym"] == sym_internal]
        for strat in strategies_for_sym:
            sid = strat["id"]
            if self.mgr_orb.has_open_or_pending(broker_sym, sid):
                continue
            params = strat["orb_params"]
            oh = int(params["open_hour_utc"])
            om = int(params.get("open_minute_utc", 0))
            rm = int(params["range_minutes"])
            bw = int(params.get("breakout_window_minutes", 180))
            # Compute today's range
            range_start = m1.filter(
                (pl.col("time").dt.hour() == oh)
                & (pl.col("time").dt.minute() >= om)
                & (pl.col("time").dt.date() == m1.tail(1)["time"][0].date())
            )
            if len(range_start) < 1:
                continue
            range_end_min = oh * 60 + om + rm
            range_bars = m1.filter(
                (pl.col("time").dt.date() == m1.tail(1)["time"][0].date())
                & ((pl.col("time").dt.hour() * 60 + pl.col("time").dt.minute()) >= (oh * 60 + om))
                & ((pl.col("time").dt.hour() * 60 + pl.col("time").dt.minute()) < range_end_min)
            )
            if len(range_bars) < max(1, rm // 2):
                continue
            r_high = float(range_bars["high"].max())
            r_low = float(range_bars["low"].min())
            now_utc = _now_utc()
            now_min_of_day = now_utc.hour * 60 + now_utc.minute
            # Solo durante breakout_window post-range
            if now_min_of_day < range_end_min or now_min_of_day >= range_end_min + bw:
                continue
            last_close = float(m1.tail(1)["close"][0])
            if last_close <= r_high:
                continue
            # Place STOP @ r_high
            exit_r = strat["exit_rules"]
            sl_atr_mult = float(exit_r.get("initial_sl_atr_mult") or 0.5)
            risk = sl_atr_mult * atr_m1
            sl = r_high - risk
            partial_r = float(exit_r["partials"][0]["value"])
            tp = r_high + partial_r * risk
            comment = make_orb_comment(oh, rm, sym_internal)
            self.mgr_orb.place_stop_long(
                symbol=broker_sym, sym_internal=strat["internal_sym"],
                strategy_id=sid, setup_type="ORB", variant="GRID",
                stop_price=r_high, sl_price=sl, tp_price=tp,
                atr_or_risk=risk, exit_rules=exit_r,
                expiration_minutes=max(60, int(exit_r.get("max_hold_hours", 8) * 60)),
                comment=comment,
            )

    # ── Main loop ────────────────────────────────────────────────────────

    def run(self):
        if not self.connect():
            print("[TradersEngine] MT5 connect FAIL")
            sys.exit(1)
        # Pre-seleccionar todos los broker symbols en Market Watch
        symbols_swing = sorted(set(s["sym"] for s in self.swing_strategies))
        symbols_orb = sorted(set(s["sym"] for s in self.orb_strategies))
        all_internal_symbols = sorted(set(symbols_swing + symbols_orb))
        for sym_internal in all_internal_symbols:
            broker_sym = self.mapper.to_mt5(sym_internal)
            si = mt5.symbol_info(broker_sym) if mt5 else None
            if si is not None and not si.select:
                mt5.symbol_select(broker_sym, True)

        # Detect broker offset desde tick fresco (probe = primer broker symbol)
        if all_internal_symbols:
            probe = self.mapper.to_mt5(all_internal_symbols[0])
            self.broker_offset_h = detect_broker_offset_hours(self.client, probe)

        mode_str = "LIVE" if self.live else "DRY"
        print(f"[TradersEngine] started mode={mode_str}")
        print(f"  Swing strats: {len(self.swing_strategies)} (magic {MAGIC_NUMBER_TRADERS_SWING})")
        print(f"  ORB strats: {len(self.orb_strategies)} (magic {MAGIC_NUMBER_TRADERS_ORB})")
        print(f"  Risk/trade: {self.risk_pct*100:.2f}%")
        print(f"  Broker offset: {self.broker_offset_h:+d}h vs UTC (bars auto-corrected)")
        print(f"  Symbols (internal -> broker):")
        for s in all_internal_symbols:
            print(f"    {s:10s} -> {self.mapper.to_mt5(s)}")
        # Telegram start notification
        self.notifier.engine_started(
            mode=mode_str,
            swing_n=len(self.swing_strategies),
            orb_n=len(self.orb_strategies),
            risk_pct=self.risk_pct,
            broker_offset_h=self.broker_offset_h,
            symbols=all_internal_symbols,
        )

        last_swing_refresh_date: dict[str, str] = {}
        offset_refresh_counter = 0
        heartbeat_counter = 0  # ticks de 60s; cada 15 (15 min) emite heartbeat tg
        while not _stop:
            try:
                HEARTBEAT_FILE.write_text(_now_utc().isoformat())
                # Refresh broker_offset cada 10 loops (~10 min) por si hay DST cambio
                offset_refresh_counter += 1
                if offset_refresh_counter >= 10 and all_internal_symbols:
                    probe = self.mapper.to_mt5(all_internal_symbols[0])
                    new_off = detect_broker_offset_hours(
                        self.client, probe,
                        current_offset_h=self.broker_offset_h,
                    )
                    if new_off != self.broker_offset_h:
                        # Sanity: reject implausible offsets (must be in [-1h, +12h])
                        if -1 <= new_off <= 12:
                            print(f"[TradersEngine] broker_offset changed: "
                                  f"{self.broker_offset_h:+d}h -> {new_off:+d}h")
                            self.broker_offset_h = new_off
                        else:
                            print(f"[TradersEngine] rejecting implausible "
                                  f"offset {new_off:+d}h, keeping "
                                  f"{self.broker_offset_h:+d}h")
                    offset_refresh_counter = 0

                # 1) Reconcile
                self.mgr_swing.reconcile_with_broker()
                self.mgr_orb.reconcile_with_broker()

                # 2) Swing: refresh setups si cambio el dia UTC
                today_str = _now_utc().strftime("%Y-%m-%d")
                for sym_internal in symbols_swing:
                    if last_swing_refresh_date.get(sym_internal) != today_str:
                        self._refresh_swing_setups(sym_internal, today_str)
                        last_swing_refresh_date[sym_internal] = today_str

                # 3) Swing breakouts (cada tick)
                self._check_swing_breakouts()

                # 4) ORB (cada tick)
                for sym_internal in symbols_orb:
                    try:
                        self._process_orb(sym_internal)
                    except Exception as e:
                        print(f"[TradersEngine][orb] {sym_internal} FAIL: {e}")

                # 5) Manage open positions (partials, trail, max_hold)
                self.mgr_swing.manage_open_positions(self.daily_sma_cache)
                self.mgr_orb.manage_open_positions(None)  # ORB sin trail SMA

                # 6) Heartbeat Telegram cada 15 min
                heartbeat_counter += 1
                if heartbeat_counter >= 15:
                    heartbeat_counter = 0
                    bal = self.client.get_account_balance() or 0.0
                    acc = self.client.get_account_info()
                    eq = float(acc.equity) if acc else 0.0
                    self.notifier.heartbeat(
                        swing_open=len(self.mgr_swing.open_positions),
                        swing_pending=len(self.mgr_swing.pending_orders),
                        orb_open=len(self.mgr_orb.open_positions),
                        orb_pending=len(self.mgr_orb.pending_orders),
                        balance=bal, equity=eq,
                    )

            except Exception as e:
                print(f"[TradersEngine] loop error: {e}")
                import traceback; traceback.print_exc()
                try:
                    self.notifier.error(context="main_loop", msg=str(e))
                except Exception:
                    pass
            for _ in range(POLL_SECONDS):
                if _stop:
                    break
                time.sleep(1)
        print("[TradersEngine] stopped")
        try:
            self.notifier.engine_stopped(reason="signal")
        except Exception:
            pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    live = args.live and not args.dry_run
    signal.signal(signal.SIGINT, _on_signal)
    signal.signal(signal.SIGTERM, _on_signal)
    eng = TradersEngine(live=live)
    eng.run()


if __name__ == "__main__":
    main()
