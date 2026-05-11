"""
Pull & Restart — Kha0sys3
Hace git pull en el VPS y reinicia los servicios. Ejecutar desde local.

Cubre los 3 servicios NSSM activos:
  - Kha0sysBot3      (FADE bot, magic 1337)
  - Kha0sysWatchdog3 (monitoreo)
  - Kha0sysMathBot   (MATH bot, magic 1338) — preserva sus AppParameters
    actuales (--live / --dry-run) porque NSSM start no los toca.
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deploy.vps_connection import VPSConnection

BOT_PATH = r"C:\Proyectos\kha0sys3"
SERVICES = ["Kha0sysBot3", "Kha0sysWatchdog3", "Kha0sysMathBot"]


def main():
    vps = VPSConnection()

    if not vps.test_connection():
        print("ERROR: No se pudo conectar al VPS.")
        sys.exit(1)

    # 1. Parar servicios
    print("Deteniendo servicios...")
    for svc in SERVICES:
        vps.run_ps(f"C:\\nssm\\nssm.exe stop {svc}")
    time.sleep(3)

    # 2. Git pull
    print("Ejecutando git pull...")
    result = vps.run_ps(f"cd '{BOT_PATH}'; git pull origin main")
    print(f"  {result['stdout']}")
    if result["stderr"]:
        print(f"  stderr: {result['stderr']}")

    # 3. Reinstalar dependencias (por si hay nuevas)
    print("Verificando dependencias...")
    result = vps.run_ps(
        f"cd '{BOT_PATH}'; C:\\Python312\\python.exe -m pip install -r requirements.txt --quiet 2>&1 | Select-Object -Last 3"
    )
    print(f"  {result['stdout']}")

    # 4. Reiniciar servicios
    print("Reiniciando servicios...")
    for svc in SERVICES:
        vps.run_ps(f"C:\\nssm\\nssm.exe start {svc}")
        time.sleep(2)

    time.sleep(5)

    # 5. Verificar
    print("\n=== Estado ===")
    for svc in SERVICES:
        result = vps.run_ps(f"C:\\nssm\\nssm.exe status {svc}")
        print(f"  {svc}: {result['stdout'].strip()}")

    print("Pull & restart completado.")


if __name__ == "__main__":
    main()
