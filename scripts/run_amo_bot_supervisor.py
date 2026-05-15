"""AMO8 supervisor — entry point for NSSM service.

Usage:
    py -3.12 scripts/run_amo_bot_supervisor.py --dry-run
    py -3.12 scripts/run_amo_bot_supervisor.py --live

Mirrors scripts/run_math_bot_supervisor.py pattern. Catches uncaught
exceptions and restarts the engine after a short delay so a transient
MT5 disconnect does not require external supervision beyond NSSM.
"""
from __future__ import annotations

import argparse
import sys
import time
import traceback
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src.execution.live_amo_trader import AmoTraderEngine


RESTART_DELAY_SEC = 30


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="src/execution/bot_config_amo8.json")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--live", action="store_true")
    args = p.parse_args()

    dry = bool(args.dry_run)
    print(f"[AMO8 SUPERVISOR] starting (dry_run={dry})")
    while True:
        try:
            engine = AmoTraderEngine(config_path=args.config, dry_run=dry)
            engine.start()
            print("[AMO8 SUPERVISOR] engine.start() returned (stop signal); exiting")
            return
        except KeyboardInterrupt:
            print("[AMO8 SUPERVISOR] KeyboardInterrupt, exiting cleanly")
            return
        except Exception:
            print("[AMO8 SUPERVISOR] uncaught exception:")
            traceback.print_exc()
            print(f"[AMO8 SUPERVISOR] restarting in {RESTART_DELAY_SEC}s ...")
            time.sleep(RESTART_DELAY_SEC)


if __name__ == "__main__":
    main()
