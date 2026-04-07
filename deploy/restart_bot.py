"""
Restart Bot — Kha0sys3
Reinicia los servicios del bot en el VPS. Ejecutar desde local.
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deploy.vps_connection import VPSConnection

SERVICES = ["Kha0sysBot3", "Kha0sysWatchdog3"]


def main():
    vps = VPSConnection()

    if not vps.test_connection():
        print("ERROR: No se pudo conectar al VPS.")
        sys.exit(1)

    for svc in SERVICES:
        print(f"Deteniendo {svc}...")
        vps.run_ps(f"C:\\nssm\\nssm.exe stop {svc}")
        time.sleep(3)

    for svc in SERVICES:
        print(f"Iniciando {svc}...")
        vps.run_ps(f"C:\\nssm\\nssm.exe start {svc}")
        time.sleep(2)

    time.sleep(5)

    print("\n=== Estado post-reinicio ===")
    for svc in SERVICES:
        result = vps.run_ps(f"C:\\nssm\\nssm.exe status {svc}")
        print(f"  {svc}: {result['stdout'].strip()}")

    print("Reinicio completado.")


if __name__ == "__main__":
    main()
