"""Source reader/keeper (NSSM service Kha0sysCopierSrc).

Holds ONE persistent session-0 MetaBuy/TMFinancials connection (never shutdowns,
so the terminal stays up and positions stay synced) and writes the current GOLD
positions to a file every second. The copier reads that file — so the copier
never connects to the source terminal and there is NO per-tick churn (the churn
caused ~110s ticks and a watchdog restart loop).

Creds from .env (MT5_*2). Symbols hard-scoped to gold (XAUUSD.f).
"""
import json
import os
import sys
import time
from datetime import datetime, timezone
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
GOLD = {"XAUUSD.f"}
POLL_SEC = 1


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
    try:
        SRC_FILE.parent.mkdir(parents=True, exist_ok=True)
        tmp = SRC_FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps({
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "positions": positions,
        }), encoding="utf-8")
        tmp.replace(SRC_FILE)  # atomic — the copier never sees a half-written file
    except Exception as e:
        log(f"write error: {e}")


def main() -> None:
    load_env()
    login = int(os.environ["MT5_LOGIN2"])
    password = os.environ["MT5_PASSWORD2"]
    server = os.environ["MT5_SERVER2"]
    log(f"=== source keeper/reader START (login {login} @ {server}) ===")
    healthy_before = False
    while True:
        ti = mt5.terminal_info() if mt5 else None
        ai = mt5.account_info() if mt5 else None
        healthy = bool(ti and ti.connected and ai and int(ai.login) == login)
        if not healthy:
            # Clear any half/stuck state, then a CLEAN fresh login (a clean-slate
            # initialize is what works; thrashing a half-launched terminal fails).
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
                time.sleep(8)   # back off so we don't thrash a launching terminal
                continue
        elif not healthy_before:
            log(f"source healthy (login {ai.login}, connected) — writing positions")
        healthy_before = healthy

        if healthy:
            positions = mt5.positions_get()
            if positions is not None:
                gold = [
                    {"ticket": p.ticket, "symbol": p.symbol, "type": int(p.type),
                     "sl": float(p.sl), "tp": float(p.tp), "volume": float(p.volume)}
                    for p in positions if p.symbol in GOLD
                ]
                _write(gold)
        time.sleep(POLL_SEC)


if __name__ == "__main__":
    main()
