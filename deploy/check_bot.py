"""
Check Bot — Kha0sys3
Verifica el estado del bot en el VPS. Ejecutar desde local.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deploy.vps_connection import VPSConnection

BOT_PATH = r"C:\Proyectos\kha0sys3"
SERVICES = ["Kha0sysBot3", "Kha0sysWatchdog3"]


def main():
    vps = VPSConnection()

    if not vps.test_connection():
        print("ERROR: No se pudo conectar al VPS.")
        sys.exit(1)

    print("=== Estado de Servicios ===")
    for svc in SERVICES:
        result = vps.run_ps(f"C:\\nssm\\nssm.exe status {svc}")
        status = result["stdout"].strip() or "DESCONOCIDO"
        print(f"  {svc}: {status}")

    print("\n=== Ultimas lineas del log ===")
    result = vps.run_ps(
        f"if (Test-Path '{BOT_PATH}\\logs\\bot_stdout.log') "
        f"{{ Get-Content '{BOT_PATH}\\logs\\bot_stdout.log' -Tail 20 }} "
        f"else {{ 'Log no encontrado' }}"
    )
    print(result["stdout"])

    print("\n=== Errores recientes ===")
    result = vps.run_ps(
        f"if (Test-Path '{BOT_PATH}\\logs\\bot_stderr.log') "
        f"{{ Get-Content '{BOT_PATH}\\logs\\bot_stderr.log' -Tail 10 }} "
        f"else {{ 'Sin errores' }}"
    )
    print(result["stdout"] or "Sin errores")


if __name__ == "__main__":
    main()
