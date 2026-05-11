"""
Check Bot — Kha0sys3
Verifica el estado del bot en el VPS. Ejecutar desde local.

Cubre los 3 servicios NSSM activos:
  - Kha0sysBot3      (FADE bot)
  - Kha0sysWatchdog3 (monitoreo)
  - Kha0sysMathBot   (MATH bot, magic 1338, logs en C:\\ProgramData\\Kha0sysMath\\logs)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deploy.vps_connection import VPSConnection

BOT_PATH = r"C:\Proyectos\kha0sys3"
MATH_LOG_DIR = r"C:\ProgramData\Kha0sysMath\logs"

SERVICES = ["Kha0sysBot3", "Kha0sysWatchdog3", "Kha0sysMathBot"]
LOGS = {
    "Kha0sysBot3": rf"{BOT_PATH}\logs\bot_stdout.log",
    "Kha0sysWatchdog3": rf"{BOT_PATH}\logs\watchdog_stdout.log",
    "Kha0sysMathBot": rf"{MATH_LOG_DIR}\math_bot.log",
}
ERR_LOGS = {
    "Kha0sysBot3": rf"{BOT_PATH}\logs\bot_stderr.log",
    "Kha0sysWatchdog3": rf"{BOT_PATH}\logs\watchdog_stderr.log",
    "Kha0sysMathBot": rf"{MATH_LOG_DIR}\math_bot_err.log",
}


def _sanitize(s: str) -> str:
    """Strip non-cp1252-safe chars so the Windows console doesn't crash."""
    return "".join(c if (32 <= ord(c) < 127 or c in "\n\r\t") else "?" for c in s)


def _ps_tail(vps: VPSConnection, path: str, lines: int) -> str:
    res = vps.run_ps(
        f"$OutputEncoding=[Text.Encoding]::UTF8; "
        f"if (Test-Path '{path}') {{ Get-Content '{path}' -Tail {lines} "
        f"| Out-String -Width 200 }} else {{ 'no log' }}"
    )
    return _sanitize(res["stdout"])


def main():
    vps = VPSConnection()

    if not vps.test_connection():
        print("ERROR: No se pudo conectar al VPS.")
        sys.exit(1)

    print("=== HEAD repo en VPS ===")
    result = vps.run_ps(f"cd '{BOT_PATH}'; git log --oneline -1")
    print(f"  {_sanitize(result['stdout'])}")

    print("\n=== Estado de Servicios ===")
    for svc in SERVICES:
        result = vps.run_ps(f"C:\\nssm\\nssm.exe status {svc}")
        status = _sanitize(result["stdout"]).strip() or "DESCONOCIDO"
        print(f"  {svc}: {status}")

    # MATH bot health signal: scan last 200 lines for retcode 10027 vs
    # dispatch-skip. Useful answer to "is AutoTrading flag OK?".
    print("\n=== MATH bot health (heuristica desde log) ===")
    res = vps.run_ps(
        f"$OutputEncoding=[Text.Encoding]::UTF8; "
        f"if (Test-Path '{LOGS['Kha0sysMathBot']}') {{ "
        f"$t = Get-Content '{LOGS['Kha0sysMathBot']}' -Tail 200; "
        f"$rej = ($t | Select-String 'retcode=10027').Count; "
        f"$skip = ($t | Select-String 'dispatch skip: trade_allowed_false').Count; "
        f"$pl = ($t | Select-String 'ORDER PLACED').Count; "
        f"$proc = ($t | Select-String 'close . processing').Count; "
        f"$last = ($t | Select-Object -Last 1); "
        f"\"retcode10027={{$rej}} dispatch_skip={{$skip}} order_placed={{$pl}} tf_dispatches={{$proc}}`nlast: {{$last}}\""
        f"}} else {{ 'no log' }}"
    )
    print(_sanitize(res["stdout"]))

    for svc in SERVICES:
        print(f"\n=== {svc} stdout (last 15) ===")
        print(_ps_tail(vps, LOGS[svc], 15))

        print(f"\n=== {svc} stderr (last 10) ===")
        err = _ps_tail(vps, ERR_LOGS[svc], 10).strip()
        print(err or "sin errores")


if __name__ == "__main__":
    main()
