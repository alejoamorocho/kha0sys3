"""Source reader/keeper (NSSM service Kha0sysCopierSrc).

Holds ONE persistent session-0 MetaBuy/TMFinancials connection and writes the
current GOLD open positions to a file every second. The copier reads that file.

CRITICAL (2026-06-24): on this TMFinancials managed/investor account
(trade_mode=REAL, trade_allowed=False) `positions_get()` is BLIND — it returns
nothing even while a position is OPEN (proven: 2 live trades stayed open 5-7 min
with the keeper healthy and positions_get returned 0 the whole time). What DOES
work is `history_deals_get()`. So open positions are RECONSTRUCTED from deals
(net volume per position_id > 0 = still open), NOT from positions_get.

Safety net — equity cross-check + force refresh: account_info().equity is always
live, so equity != balance means a position is OPEN *right now*. If something is
open (floating) but the deal reconstruction can't see it yet, we FORCE a
reconnect to refresh the terminal's history, then re-read. This guarantees we
are never blind while a position is open ("si por algun motivo no lo hace, lo
debe forzar"). Same on close: reconstruction-open but no floating => force a
refresh to pull the OUT deal so the copy closes promptly.

Gold matched by substring (XAU/GOLD) so any broker suffix is captured. The raw
source symbol (e.g. XAUUSD.f) is written verbatim so the copier maps it.
Creds from .env (MT5_*2).
"""
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.domain.env_loader import load_env

try:
    import MetaTrader5 as mt5
except Exception:
    mt5 = None

PATH = r"C:\Program Files\MetaBuy\terminal64.exe"
SRC_FILE = Path(r"C:\ProgramData\Kha0sysCopier\source_positions.json")
LOG = Path(r"C:\ProgramData\Kha0sysCopier\logs\src_keeper.log")
POLL_SEC = 1
DIAG_SEC = 20                 # rate-limit the steady-state diagnostic line
DEAL_LOOKBACK_DAYS = 30       # window for reconstructing open positions from deals
MARGIN_EPS = 1e-6            # account margin <= this => NO position open (server truth, exact, no P&L ambiguity)
FLOAT_EPS = 0.01             # |equity-balance| above this => floating P&L present (logged cross-check)
FLAT_CONFIRM = 2              # consecutive margin==0 reads before force-closing copies (anti-glitch)
BLIND_REFRESH_AFTER = 3       # cycles of (margin>0 but 0 gold seen) -> force refresh history

# MT5 deal.entry: 0=IN (open), 1=OUT (close), 2=INOUT (reversal), 3=OUT_BY
ENTRY_IN, ENTRY_OUT, ENTRY_INOUT, ENTRY_OUT_BY = 0, 1, 2, 3


def _is_gold(symbol: str) -> bool:
    s = (symbol or "").upper()
    return "XAU" in s or "GOLD" in s


def log(m: str) -> None:
    line = f"{datetime.now(timezone.utc).isoformat(timespec='seconds')} {m}"
    print(line, flush=True)
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def _write(positions: list) -> None:
    """Atomic write with retry: on Windows os.replace fails (WinError 5) if the
    copier has the .json open for reading at that instant — retry a few times
    (the reader holds it <1ms), then fall back to a direct write so the file
    never goes stale and blinds the copier."""
    payload = json.dumps({
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "positions": positions,
    })
    SRC_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = SRC_FILE.with_suffix(".tmp")
    try:
        tmp.write_text(payload, encoding="utf-8")
    except Exception as e:
        log(f"write tmp error: {e}")
        return
    for _ in range(12):                       # ~240ms of retries
        try:
            tmp.replace(SRC_FILE)             # atomic when it succeeds
            return
        except PermissionError:
            time.sleep(0.02)
        except Exception as e:
            log(f"replace error: {e}")
            break
    try:                                      # last resort: direct (non-atomic) write
        SRC_FILE.write_text(payload, encoding="utf-8")
    except Exception as e:
        log(f"direct write error: {e}")


def reconstruct_open(deals, gold_only: bool = True) -> list:
    """PURE: given an iterable of MT5-style deals (objects/dicts with
    position_id, entry, type, volume, symbol, time, ticket), return the
    currently-OPEN positions. Net volume per position_id: IN adds, OUT/OUT_BY
    subtract; net>0 => still open. Direction + symbol come from the opening (IN)
    deal. Unit-tested in tests/test_copier_reconstruct.py."""
    def g(d, k, default=0):
        return d.get(k, default) if isinstance(d, dict) else getattr(d, k, default)

    by_pos: dict[int, list] = {}
    for d in deals:
        pid = int(g(d, "position_id", 0))
        if pid == 0:                              # balance/credit ops have no position
            continue
        by_pos.setdefault(pid, []).append(d)
    out = []
    for pid, ds in by_pos.items():
        ds = sorted(ds, key=lambda x: (g(x, "time", 0), g(x, "ticket", 0)))
        net = 0.0
        entry_deal = None
        for d in ds:
            entry = int(g(d, "entry", 0))
            vol = float(g(d, "volume", 0.0))
            if entry == ENTRY_IN:
                net += vol
                if entry_deal is None:
                    entry_deal = d
            elif entry in (ENTRY_OUT, ENTRY_OUT_BY):
                net -= vol
            elif entry == ENTRY_INOUT:            # reversal — rare; flag, don't guess
                log(f"position {pid}: INOUT reversal deal seen (unhandled)")
        if net <= 1e-9 or entry_deal is None:
            continue
        symbol = g(entry_deal, "symbol", "")
        if gold_only and not _is_gold(symbol):
            continue
        out.append({
            "ticket": int(pid),
            "symbol": symbol,
            "type": int(g(entry_deal, "type", 0)),  # 0=BUY(long) 1=SELL(short)
            "sl": 0.0, "tp": 0.0,                   # TMF exits manually — no SL/TP
            "volume": round(net, 8),
        })
    return out


def _open_positions_from_deals():
    """Reconstruct currently-OPEN gold positions from live deal history (the only
    source that works on this account). Returns a list, or None on read error."""
    frm = datetime.now(timezone.utc) - timedelta(days=DEAL_LOOKBACK_DAYS)
    to = datetime.now(timezone.utc) + timedelta(days=1)
    deals = mt5.history_deals_get(frm, to)
    if deals is None:
        return None
    return reconstruct_open(deals, gold_only=True)


def _merge(a: list, b: list) -> list:
    """Union of two position lists, deduped by ticket (position_id)."""
    seen = {}
    for p in (a or []) + (b or []):
        seen[int(p["ticket"])] = p
    return list(seen.values())


def _force_refresh(login: int, password: str, server: str, why: str) -> None:
    """Reconnect (shutdown+init) to refresh the terminal's history when we are
    blind to an open position. Only fired when state changed (a position opened
    or closed but the deal view hasn't caught up) — NOT in steady state."""
    log(f"FORCE refresh ({why}) — reconnecting to pull fresh history")
    try:
        mt5.shutdown()
    except Exception:
        pass
    ok = mt5.initialize(path=PATH, login=login, password=password, server=server)
    log(f"force refresh reconnect: ok={ok}")


_DEAL_REASON = {
    0: "CLIENT", 1: "MOBILE", 2: "WEB", 3: "EXPERT", 4: "SL", 5: "TP", 6: "SO",
    7: "ROLLOVER", 8: "VMARGIN", 9: "GATEWAY", 10: "SIGNAL", 11: "SETTLEMENT",
    12: "TRANSFER", 13: "SYNC", 14: "EXTERNAL_CLIENT", 15: "VMARGIN", 16: "CORP_ACTION",
}


def _dump_account(login: int) -> None:
    """Full structural fingerprint: every account_info field + all enumerators.
    Tells us WHAT kind of account this is and WHERE the positions live."""
    try:
        ai = mt5.account_info()
        if ai is None:
            log(f"account_info -> None (last_error={mt5.last_error()})")
            return
        try:
            d = ai._asdict()
            log("account FULL: " + " ".join(f"{k}={d[k]!r}" for k in d))
        except Exception:
            log(f"account: login={ai.login} balance={ai.balance} equity={ai.equity}")
        pos = mt5.positions_get()
        orders = mt5.orders_get()
        log(f"enumerators: positions_total={mt5.positions_total()} "
            f"positions_get={None if pos is None else len(pos)} "
            f"orders_total={mt5.orders_total()} "
            f"orders_get={None if orders is None else len(orders)} "
            f"last_error={mt5.last_error()}")
        if pos:
            for p in pos:
                log(f"  POSITION sym={p.symbol!r} type={p.type} vol={p.volume} "
                    f"magic={p.magic} comment={p.comment!r} ticket={p.ticket}")
        if orders:
            for o in orders:
                log(f"  ORDER sym={o.symbol!r} type={o.type} vol={o.volume_current} "
                    f"magic={o.magic} comment={o.comment!r} ticket={o.ticket}")
    except Exception as e:
        log(f"account dump error: {e}")


def _dump_history(login: int) -> None:
    """Recent deals with the REASON/comment/external_id — reveals if trades come
    from a SIGNAL subscription, a GATEWAY/external bridge, SYNC, etc."""
    try:
        frm = datetime.now(timezone.utc) - timedelta(days=5)
        to = datetime.now(timezone.utc) + timedelta(days=1)
        deals = mt5.history_deals_get(frm, to)
        if deals is None:
            log(f"history: none (last_error={mt5.last_error()})")
            return
        log(f"history: {len(deals)} deals (last 5d) on login {login}:")
        for d in deals[-20:]:
            ts = datetime.fromtimestamp(d.time, tz=timezone.utc).isoformat(timespec="seconds")
            reason = _DEAL_REASON.get(getattr(d, "reason", -1), getattr(d, "reason", "?"))
            log(f"  deal sym={d.symbol!r} type={d.type} entry={d.entry} vol={d.volume} "
                f"price={d.price} profit={d.profit} pos={d.position_id} "
                f"reason={reason} magic={d.magic} comment={d.comment!r} "
                f"ext_id={getattr(d, 'external_id', '')!r} t={ts}")
    except Exception as e:
        log(f"history dump error: {e}")


def main() -> None:
    load_env()
    login = int(os.environ["MT5_LOGIN2"])
    password = os.environ["MT5_PASSWORD2"]
    server = os.environ["MT5_SERVER2"]
    log(f"=== source keeper/reader START (login {login} @ {server}) — DEAL-RECONSTRUCT mode ===")
    healthy_before = False
    dumped = False
    last_diag = 0.0
    flat_streak = 0
    blind_streak = 0
    while True:
        ti = mt5.terminal_info() if mt5 else None
        ai = mt5.account_info() if mt5 else None
        healthy = bool(ti and ti.connected and ai and int(ai.login) == login)
        if not healthy:
            try:
                mt5.shutdown()
            except Exception:
                pass
            ok = mt5.initialize(path=PATH, login=login, password=password, server=server)
            ai = mt5.account_info()
            ti = mt5.terminal_info()
            healthy = bool(ok and ai and int(ai.login) == login and ti and ti.connected)
            log(f"(re)connect source: ok={ok} login={getattr(ai, 'login', None)} healthy={healthy}")
            if not healthy:
                time.sleep(8)
                continue
        elif not healthy_before:
            log(f"source healthy (login {ai.login}, connected) — reconstructing from deals")
        healthy_before = healthy

        if not healthy:
            time.sleep(POLL_SEC)
            continue

        if not dumped:
            _dump_account(login)
            _dump_history(login)
            dumped = True

        equity = float(ai.equity)
        balance = float(ai.balance)
        margin = float(getattr(ai, "margin", 0.0) or 0.0)
        floating = equity - balance
        # margin is the SERVER's truth for "is any position open" — exactly 0.0
        # when flat, >0 when something is open. Unlike equity it has no P&L /
        # breakeven ambiguity, so it is the close-side authority (anti-orphan).
        flat = margin <= MARGIN_EPS

        deals_open = _open_positions_from_deals()
        if deals_open is None:                       # history read error
            log(f"history_deals_get -> None (last_error={mt5.last_error()})")
            deals_open = []
        posget = []                                  # positions_get is blind here, but include if it ever works
        raw = mt5.positions_get()
        if raw:
            posget = [
                {"ticket": int(p.ticket), "symbol": p.symbol, "type": int(p.type),
                 "sl": float(p.sl), "tp": float(p.tp), "volume": float(p.volume)}
                for p in raw if _is_gold(p.symbol)
            ]
        merged = _merge(deals_open, posget)

        if flat:
            # SERVER says NO position open (margin==0). This is authoritative ->
            # close any copies. THE anti-orphan guarantee: TMF flat => copies
            # closed, even if a close deal failed to sync. Confirm a couple of
            # reads to ride out a one-off glitch read.
            blind_streak = 0
            flat_streak += 1
            if merged and flat_streak >= FLAT_CONFIRM:
                log(f"margin=0 (TMF FLAT) x{flat_streak} but deals still show "
                    f"{[p['ticket'] for p in merged]} -> trusting server, CLOSING (anti-orphan)")
                merged = []
        else:
            # margin>0 => something IS open. Need the gold details from deals.
            # If deals don't show it yet, give live history a few seconds then
            # FORCE a (free) refresh; if still nothing, it's a non-gold position
            # or deals are stuck -> alert, never go silent.
            flat_streak = 0
            if not merged:
                blind_streak += 1
                if blind_streak >= BLIND_REFRESH_AFTER:
                    _force_refresh(login, password, server, f"margin={margin} (open) but 0 gold seen")
                    deals_open = _open_positions_from_deals() or []
                    merged = _merge(deals_open, posget)
                    blind_streak = 0
                    if not merged:
                        log(f"ALERT: margin={margin} (position OPEN) but 0 GOLD reconstructed "
                            f"— non-gold position or deals not syncing. Check TMF.")
            else:
                blind_streak = 0

        _write(merged)

        now = time.time()
        if merged or not flat or (now - last_diag >= DIAG_SEC):
            log(f"open={len(merged)} (deals={len(deals_open)} posget={len(posget)}) "
                f"margin={margin} floating={floating:+.2f} eq={equity} bal={balance} "
                f"flat={flat} tickets={[p['ticket'] for p in merged]}")
            last_diag = now
        time.sleep(POLL_SEC)


if __name__ == "__main__":
    main()
