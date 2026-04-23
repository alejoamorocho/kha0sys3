"""
Math Bot Supervisor — Kha0sys3 parallel MATH runner
Entry point for NSSM service `Kha0sysMathBot`.

Keeps MathTraderEngine alive across crashes, same pattern as
scripts/run_bot_supervisor.py but slimmer. DRY_RUN default (--dry-run); flip
to --live only after DRY telemetry validation.
"""
from __future__ import annotations

import argparse
import os
import sys
import time
import traceback
from datetime import datetime, timezone

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
os.chdir(PROJECT_ROOT)

# Ensure our log directory exists (outside repo tree to survive git pulls)
LOG_DIR_DEFAULT = os.path.join(os.environ.get("ProgramData", PROJECT_ROOT),
                                "Kha0sysMath", "logs")
try:
    os.makedirs(LOG_DIR_DEFAULT, exist_ok=True)
except Exception:
    pass

from src.execution.live_math_trader import MathTraderEngine  # noqa: E402

MAX_RESTARTS = 5
RESTART_COOLDOWN = 30
RESTART_RESET_WINDOW = 3600


def parse_args():
    ap = argparse.ArgumentParser(description="Kha0sys3 MATH bot supervisor")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--dry-run", dest="dry_run", action="store_true",
                   help="Log-only mode (no MT5 order_send). DEFAULT.")
    g.add_argument("--live", dest="dry_run", action="store_false",
                   help="Enable live order placement. USER ACTION REQUIRED.")
    ap.set_defaults(dry_run=True)
    return ap.parse_args()


def main():
    args = parse_args()
    mode = "DRY_RUN" if args.dry_run else "LIVE"
    print(f"[MATH-Supervisor] started @ {datetime.now(timezone.utc)} mode={mode}")

    restart_count = 0
    last_restart_time = time.time()

    while restart_count < MAX_RESTARTS:
        try:
            now = time.time()
            if now - last_restart_time > RESTART_RESET_WINDOW:
                restart_count = 0

            print(f"[MATH-Supervisor] launching engine (attempt {restart_count + 1})")
            engine = MathTraderEngine(dry_run=args.dry_run)
            engine.run()
            print("[MATH-Supervisor] engine returned normally.")
            break

        except KeyboardInterrupt:
            print("[MATH-Supervisor] KeyboardInterrupt — exiting.")
            break

        except Exception as e:
            restart_count += 1
            last_restart_time = time.time()
            print(f"[MATH-Supervisor] crash #{restart_count}: {type(e).__name__}: {e}")
            traceback.print_exc()
            if restart_count < MAX_RESTARTS:
                print(f"[MATH-Supervisor] restart in {RESTART_COOLDOWN}s")
                time.sleep(RESTART_COOLDOWN)

    if restart_count >= MAX_RESTARTS:
        print(f"[MATH-Supervisor] max restarts ({MAX_RESTARTS}) reached — exiting.")
        sys.exit(1)


if __name__ == "__main__":
    main()
