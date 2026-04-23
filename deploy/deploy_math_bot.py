"""
Deploy MATH Parallel Runner — Kha0sys3
Registers `Kha0sysMathBot` NSSM service on VPS1, ALONGSIDE the existing
`Kha0sysBot3` (FADE, magic 1337). Never touches the FADE service.

Default: --dry-run (no MT5 order_send). User flips to --live manually after
validating DRY telemetry (see README at bottom of this file).

Usage (from local machine):
    python deploy/deploy_math_bot.py
"""
from __future__ import annotations

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deploy.vps_connection import VPSConnection

REPO_PATH = r"C:\Proyectos\kha0sys3"
LOG_DIR = r"C:\ProgramData\Kha0sysMath\logs"

SERVICE_NAME = "Kha0sysMathBot"
EXE = r"C:\Python312\python.exe"
ARGS = f"-u {REPO_PATH}\\scripts\\run_math_bot_supervisor.py --dry-run"

NSSM = r"C:\nssm\nssm.exe"


def run(vps: VPSConnection, script: str, label: str = "") -> dict:
    res = vps.run_ps(script)
    if label:
        print(f"[{label}] status={res['status']}")
        if res["stdout"]:
            print(f"  stdout: {res['stdout'][:400]}")
        if res["stderr"]:
            print(f"  stderr: {res['stderr'][:400]}")
    return res


def main():
    vps = VPSConnection()
    if not vps.test_connection():
        print("ERROR: VPS unreachable. Abort.")
        sys.exit(1)
    print("[deploy-math] VPS connection OK.")

    # 1. Refresh repo (keeps FADE bot untouched — same working copy)
    run(vps, f"cd '{REPO_PATH}'; git pull origin main", "git pull")

    # 2. Ensure log dir
    run(vps, f"New-Item -ItemType Directory -Path '{LOG_DIR}' -Force | Out-Null; 'ok'",
        "log dir")

    # 3. Remove any previous install of this specific service (idempotent)
    run(vps, f"{NSSM} stop {SERVICE_NAME} 2>$null", f"stop {SERVICE_NAME}")
    run(vps, f"{NSSM} remove {SERVICE_NAME} confirm 2>$null", f"remove {SERVICE_NAME}")
    time.sleep(1)

    # 4. Install NSSM service — DRY_RUN by design
    run(vps, f'{NSSM} install {SERVICE_NAME} "{EXE}" "{ARGS}"', f"install {SERVICE_NAME}")
    for cmd in [
        f'{NSSM} set {SERVICE_NAME} AppDirectory "{REPO_PATH}"',
        f'{NSSM} set {SERVICE_NAME} AppStdout "{LOG_DIR}\\math_bot.log"',
        f'{NSSM} set {SERVICE_NAME} AppStderr "{LOG_DIR}\\math_bot_err.log"',
        f"{NSSM} set {SERVICE_NAME} AppRestartDelay 10000",
        f"{NSSM} set {SERVICE_NAME} AppRotateFiles 1",
        f"{NSSM} set {SERVICE_NAME} AppRotateBytes 10485760",
    ]:
        run(vps, cmd)

    # 5. Start service
    run(vps, f"{NSSM} start {SERVICE_NAME}", f"start {SERVICE_NAME}")
    time.sleep(5)

    # 6. Health check — DOES NOT touch Kha0sysBot3
    run(vps, f"sc query {SERVICE_NAME}", f"sc query {SERVICE_NAME}")
    run(vps, f"if (Test-Path '{LOG_DIR}\\math_bot.log') {{ "
             f"Get-Content '{LOG_DIR}\\math_bot.log' -Tail 15 }} else {{ 'no log yet' }}",
        "recent math_bot.log")

    print("\n" + "=" * 60)
    print("  MATH BOT DEPLOY COMPLETE (DRY_RUN)")
    print("=" * 60)
    print(f"  Service  : {SERVICE_NAME}")
    print(f"  Magic    : 1338 (isolated from FADE magic 1337)")
    print(f"  Logs     : {LOG_DIR}\\math_bot.log")
    print("")
    print("  To flip to LIVE once DRY telemetry is validated:")
    print(f"    {NSSM} stop {SERVICE_NAME}")
    print(f'    {NSSM} set {SERVICE_NAME} AppParameters '
          f'"-u {REPO_PATH}\\scripts\\run_math_bot_supervisor.py --live"')
    print(f"    {NSSM} start {SERVICE_NAME}")
    print("=" * 60)


if __name__ == "__main__":
    main()
