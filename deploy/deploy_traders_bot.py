"""Deploy Traders Bot (Tier 1 Swing + Tier 2 ORB) — Kha0sys3

Instala `Kha0sysTradersBot` NSSM service en VPS1, AL LADO de:
  - Kha0sysMathBot (K3M1-75, magic 1338) — sin tocar
  - Kha0sysWatchdog3 — sin tocar

Magics gestionados: 1339 (swing) + 1340 (ORB).

Default: --dry-run (no MT5 order_send). Cuando valides DRY telemetry, flip
manual a --live (ver footer).

Usage (desde local):
    python deploy/deploy_traders_bot.py
"""
from __future__ import annotations

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deploy.vps_connection import VPSConnection

REPO_PATH = r"C:\Proyectos\kha0sys3"
LOG_DIR = r"C:\ProgramData\Kha0sysTraders\logs"

SERVICE_NAME = "Kha0sysTradersBot"
EXE = r"C:\Python312\python.exe"
ARGS = f"-u {REPO_PATH}\\scripts\\run_traders_bot_supervisor.py --dry-run"

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
    print("[deploy-traders] VPS connection OK.")

    # 1. Refresh repo
    run(vps, f"cd '{REPO_PATH}'; git pull origin main", "git pull")

    # 2. Ensure log dir
    run(vps, f"New-Item -ItemType Directory -Path '{LOG_DIR}' -Force | Out-Null; 'ok'",
        "log dir")

    # 3. Remove any previous install (idempotent)
    run(vps, f"{NSSM} stop {SERVICE_NAME} 2>$null", f"stop {SERVICE_NAME}")
    run(vps, f"{NSSM} remove {SERVICE_NAME} confirm 2>$null", f"remove {SERVICE_NAME}")
    time.sleep(1)

    # 4. Install NSSM service — DRY_RUN by design
    run(vps, f'{NSSM} install {SERVICE_NAME} "{EXE}" "{ARGS}"', f"install {SERVICE_NAME}")
    for cmd in [
        f'{NSSM} set {SERVICE_NAME} AppDirectory "{REPO_PATH}"',
        f'{NSSM} set {SERVICE_NAME} AppStdout "{LOG_DIR}\\traders_bot.log"',
        f'{NSSM} set {SERVICE_NAME} AppStderr "{LOG_DIR}\\traders_bot_err.log"',
        f"{NSSM} set {SERVICE_NAME} AppRestartDelay 10000",
        f"{NSSM} set {SERVICE_NAME} AppRotateFiles 1",
        f"{NSSM} set {SERVICE_NAME} AppRotateBytes 10485760",
        f"{NSSM} set {SERVICE_NAME} Start SERVICE_AUTO_START",
    ]:
        run(vps, cmd)

    # 4b. CRITICAL: run as .\Administrator (mismo account que Kha0sysMathBot).
    # MT5 Python module no encuentra terminal64.exe corriendo como LocalSystem;
    # necesita el perfil de usuario donde MT5 esta instalado.
    # Password viene de VPS_PASS env var (la misma que usa WinRM).
    vps_pass = vps.VPS_PASS
    run(vps, f'{NSSM} set {SERVICE_NAME} ObjectName ".\\Administrator" "{vps_pass}"',
        f"set ObjectName {SERVICE_NAME}")

    # 5. Install requirements (por si hay nuevas deps)
    run(vps, f"cd '{REPO_PATH}'; {EXE} -m pip install -r requirements.txt --quiet 2>&1 | Select-Object -Last 3",
        "pip install")

    # 6. Start service
    run(vps, f"{NSSM} start {SERVICE_NAME}", f"start {SERVICE_NAME}")
    time.sleep(8)

    # 7. Health check
    run(vps, f"{NSSM} status {SERVICE_NAME}", f"status {SERVICE_NAME}")
    run(vps, f"if (Test-Path '{LOG_DIR}\\traders_bot.log') {{ "
             f"Get-Content '{LOG_DIR}\\traders_bot.log' -Tail 20 }} else {{ 'no log yet' }}",
        "recent traders_bot.log")
    run(vps, f"if (Test-Path '{LOG_DIR}\\traders_bot_err.log') {{ "
             f"Get-Content '{LOG_DIR}\\traders_bot_err.log' -Tail 10 }} else {{ 'no err log' }}",
        "recent traders_bot_err.log")

    print("\n" + "=" * 60)
    print("  TRADERS BOT DEPLOY COMPLETE (DRY_RUN)")
    print("=" * 60)
    print(f"  Service  : {SERVICE_NAME}")
    print(f"  Magic    : 1339 (Swing) + 1340 (ORB)")
    print(f"  Strats   : 5 Swing + 12 ORB = 17 estrategias")
    print(f"  Risk     : 0.1% per trade")
    print(f"  Logs     : {LOG_DIR}\\traders_bot.log")
    print("")
    print("  To flip to LIVE despues de validar DRY telemetry:")
    print(f"    {NSSM} stop {SERVICE_NAME}")
    print(f'    {NSSM} set {SERVICE_NAME} AppParameters '
          f'"-u {REPO_PATH}\\scripts\\run_traders_bot_supervisor.py --live"')
    print(f"    {NSSM} start {SERVICE_NAME}")
    print("=" * 60)


if __name__ == "__main__":
    main()
