"""Run analyze_last_week_trades on the VPS via WinRM.

Pushes scripts/analyze_last_week_trades.py to the VPS (if not already
synced via git), then executes it remotely with the VPS Python that has
MT5 connected to the live broker. Streams stdout back to local.

Usage:
    py -3.12 scripts/analyze_last_week_trades_remote.py [--days 7]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from deploy.vps_connection import VPSConnection


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--days", type=int, default=7)
    p.add_argument("--bot-path", default=r"C:\Proyectos\kha0sys3")
    p.add_argument("--python", default=r"C:\Python312\python.exe")
    args = p.parse_args()

    vps = VPSConnection()
    if not vps.test_connection():
        print("ERROR: cannot reach VPS via WinRM")
        sys.exit(1)
    print("[remote] VPS connection OK")

    # Ensure latest code is on the VPS (pull from git on VPS).
    # If the local repo has uncommitted changes, the user should push first.
    print("[remote] git pull on VPS ...")
    out = vps.run_ps(f"cd '{args.bot_path}'; git pull --ff-only 2>&1 | "
                     f"Select-Object -Last 5")
    print(out.get("stdout", ""))
    if out.get("stderr"):
        print(f"[remote] stderr: {out['stderr']}")

    # Run the analysis script
    print(f"[remote] running analyze_last_week_trades.py --days {args.days} ...")
    cmd = (
        f"cd '{args.bot_path}'; "
        f"& '{args.python}' scripts/analyze_last_week_trades.py --days {args.days} 2>&1"
    )
    result = vps.run_ps(cmd)
    print("=" * 80)
    print(result.get("stdout", ""))
    if result.get("stderr"):
        print("STDERR:")
        print(result["stderr"])
    print("=" * 80)


if __name__ == "__main__":
    main()
