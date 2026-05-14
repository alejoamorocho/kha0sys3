"""Supervisor para traders_live_engine.

Wraps el engine en un loop de restart con backoff. Para uso con NSSM:
  Kha0sysTradersBot:
    Application: C:\\Python312\\python.exe
    Arguments:   C:\\Proyectos\\kha0sys3\\scripts\\run_traders_bot_supervisor.py --live
    Startup dir: C:\\Proyectos\\kha0sys3

Logs van a stdout (que NSSM redirige a su archivo configurado).

Usage:
  python scripts/run_traders_bot_supervisor.py --live
  python scripts/run_traders_bot_supervisor.py --dry-run
"""
from __future__ import annotations

import argparse
import os
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.execution.traders_live_engine import TradersEngine


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    live = args.live and not args.dry_run

    attempt = 0
    while True:
        attempt += 1
        ts = datetime.now(timezone.utc).isoformat()
        print(f"[TradersBot-Supervisor] started @ {ts} mode={'LIVE' if live else 'DRY'}")
        print(f"[TradersBot-Supervisor] launching engine (attempt {attempt})")
        try:
            engine = TradersEngine(live=live)
            engine.run()
            print("[TradersBot-Supervisor] engine returned normally.")
            # Si retorno limpio (signal), salir
            break
        except KeyboardInterrupt:
            print("[TradersBot-Supervisor] KeyboardInterrupt -> exit")
            break
        except Exception as e:
            print(f"[TradersBot-Supervisor] engine CRASHED: {e}")
            traceback.print_exc()
            backoff = min(60, 5 * attempt)
            print(f"[TradersBot-Supervisor] restart in {backoff}s")
            time.sleep(backoff)


if __name__ == "__main__":
    main()
