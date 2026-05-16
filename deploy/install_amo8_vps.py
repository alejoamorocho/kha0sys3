"""One-shot installer for Kha0sysAmo8 service on the VPS.

Idempotent: re-running on an existing service updates its parameters and
restarts. Default mode is --dry-run for safety; switch to --live after
validating Telegram + log output.

Usage:
    py -3.12 deploy/install_amo8_vps.py [--mode dry|live] [--start | --no-start]

Steps performed (via WinRM):
    1. git pull on VPS to sync AMO8 source files
    2. mkdir log + state directories
    3. nssm install/edit Kha0sysAmo8 with all parameters
    4. nssm start (optional)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import os

from deploy.vps_connection import VPSConnection


SERVICE = "Kha0sysAmo8"
BOT_PATH = r"C:\Proyectos\kha0sys3"
PYTHON_EXE = r"C:\Python312\python.exe"
LOG_DIR = r"C:\ProgramData\Kha0sysAmo8\logs"
STATE_DIR = r"C:\ProgramData\Kha0sysAmo8\state"
NSSM = r"C:\nssm\nssm.exe"  # adjust if NSSM is elsewhere


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["dry", "live"], default="dry",
                   help="Service startup mode (default: dry)")
    p.add_argument("--no-start", action="store_true",
                   help="Do not start the service after install")
    args = p.parse_args()

    vps = VPSConnection()
    if not vps.test_connection():
        print("ERROR: cannot reach VPS")
        sys.exit(1)

    # 1) Resolve NSSM path (try a few common locations)
    print("[install] resolving nssm.exe location ...")
    resolve_nssm = (
        "$candidates = @('C:\\nssm\\nssm.exe','C:\\nssm\\win64\\nssm.exe',"
        "'C:\\ProgramData\\nssm\\nssm.exe','C:\\Program Files\\nssm\\nssm.exe',"
        "(Get-Command nssm.exe -ErrorAction SilentlyContinue).Source); "
        "foreach ($c in $candidates) { if ($c -and (Test-Path $c)) { "
        "Write-Output $c; break } }"
    )
    r = vps.run_ps(resolve_nssm)
    nssm_path = (r.get("stdout") or "").strip().splitlines()
    nssm_path = nssm_path[0] if nssm_path else NSSM
    if not nssm_path:
        print("ERROR: nssm.exe not found on VPS. Install nssm first.")
        sys.exit(1)
    print(f"[install] nssm = {nssm_path}")

    # 2) git pull (idempotent)
    print("[install] git pull on VPS ...")
    r = vps.run_ps(f"cd '{BOT_PATH}'; git pull --ff-only 2>&1 | Select-Object -Last 5")
    print(r.get("stdout", "").strip())

    # 3) Create log + state directories
    print("[install] creating log + state dirs ...")
    vps.run_ps(f"New-Item -ItemType Directory -Force -Path '{LOG_DIR}' | Out-Null; "
               f"New-Item -ItemType Directory -Force -Path '{STATE_DIR}' | Out-Null")

    # 4) Check if service exists
    print(f"[install] checking if {SERVICE} exists ...")
    r = vps.run_ps(f"Get-Service {SERVICE} -ErrorAction SilentlyContinue | "
                   f"Select-Object -ExpandProperty Status")
    exists = bool((r.get("stdout") or "").strip())
    print(f"[install] service exists: {exists}")

    mode_flag = "--live" if args.mode == "live" else "--dry-run"
    app_params = f"-u {BOT_PATH}\\scripts\\run_amo_bot_supervisor.py {mode_flag}"

    # 5) Stop service if running (so we can edit params)
    if exists:
        print(f"[install] stopping {SERVICE} ...")
        vps.run_ps(f"& '{nssm_path}' stop {SERVICE}")

    # 6) Install or edit service
    if not exists:
        print(f"[install] installing {SERVICE} ...")
        vps.run_ps(f"& '{nssm_path}' install {SERVICE} '{PYTHON_EXE}' '{app_params}'")
    else:
        print(f"[install] editing {SERVICE} parameters ...")

    # Set all attributes (works for both new and existing)
    settings = {
        "Application": PYTHON_EXE,
        "AppParameters": app_params,
        "AppDirectory": BOT_PATH,
        "DisplayName": "Kha0sys3 AMO8 ORB Trader (magic 8338)",
        "Description": "ORB false-break fade portfolio. Parallel to Kha0sysMathBot.",
        "AppStdout": f"{LOG_DIR}\\amo8.log",
        "AppStderr": f"{LOG_DIR}\\amo8.err.log",
        "AppRotateFiles": "1",
        "AppRotateOnline": "1",
        "AppRotateBytes": "52428800",  # 50 MB
        "Start": "SERVICE_AUTO_START",
    }
    for key, val in settings.items():
        cmd = f"& '{nssm_path}' set {SERVICE} {key} '{val}'"
        vps.run_ps(cmd)

    # ObjectName: must run as Administrator (NOT LocalSystem) so it can
    # see the MT5 terminal launched by Administrator. Reuse VPS_PASS for
    # the Administrator password (same credentials used for WinRM).
    admin_pass = os.environ.get("VPS_PASS")
    if not admin_pass:
        print("[install] WARNING: VPS_PASS not set; service may not be able to "
              "start under Administrator. Set the env var or configure ObjectName "
              "manually with: nssm set Kha0sysAmo8 ObjectName .\\Administrator <pass>")
    else:
        # NSSM accepts: nssm set <svc> ObjectName "<user>" "<password>"
        escaped_pass = admin_pass.replace("'", "''")
        cmd = f"& '{nssm_path}' set {SERVICE} ObjectName '.\\Administrator' '{escaped_pass}'"
        vps.run_ps(cmd)
        print("[install] ObjectName set to .\\Administrator")

    vps.run_ps(f"& '{nssm_path}' set {SERVICE} AppExit Default Restart")

    # 7) Start (if not --no-start)
    if not args.no_start:
        print(f"[install] starting {SERVICE} in {args.mode.upper()} mode ...")
        r = vps.run_ps(f"& '{nssm_path}' start {SERVICE}")
        print(r.get("stdout", "").strip() or "(no stdout)")
        if r.get("stderr"):
            print(f"STDERR: {r['stderr'][:500]}")

    # 8) Verify
    print(f"[install] final status:")
    r = vps.run_ps(
        f"Get-Service {SERVICE} | Select-Object Name, Status, StartType | "
        f"Format-Table -AutoSize | Out-String; "
        f"Write-Output 'Latest stdout:'; "
        f"if (Test-Path '{LOG_DIR}\\amo8.log') {{ Get-Content '{LOG_DIR}\\amo8.log' -Tail 5 }}"
    )
    print(r.get("stdout", "").strip())

    print(f"\n[install] DONE. Tail logs with:")
    print(f"  Get-Content '{LOG_DIR}\\amo8.log' -Wait")
    print(f"\nWhen ready to switch DRY→LIVE, re-run:")
    print(f"  py -3.12 deploy/install_amo8_vps.py --mode live")


if __name__ == "__main__":
    main()
