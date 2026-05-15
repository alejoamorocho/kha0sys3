"""
Pull & Restart — Kha0sys3 (post K3M1-75 cleanup)
Hace git pull en el VPS y reinicia los servicios. Ejecutar desde local.

Cubre los servicios NSSM activos (FADE bot retirado):
  - Kha0sysWatchdog3 (monitoreo)
  - Kha0sysMathBot   (MATH K3M1-75, magic 1338) — preserva sus AppParameters
  - Kha0sysAmo8      (AMO8 ORB,      magic 8338) — preserva sus AppParameters
NSSM start no toca AppParameters (--live / --dry-run), así se mantiene cada
servicio en el modo que tenga.

Si Kha0sysAmo8 todavía no existe en el VPS (primer deploy), `nssm stop` /
`nssm start` simplemente reportan error y seguimos — créalo manualmente
siguiendo docs/AMO8_DEPLOY.md.
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deploy.vps_connection import VPSConnection

BOT_PATH = r"C:\Proyectos\kha0sys3"
# Kha0sysTradersBot (Tier 1 Swing 1339 + Tier 2 ORB 1340) agregado 2026-05-14.
# Kha0sysAmo8 (AMO8 ORB false-break, magic 8338) agregado 2026-05-16.
# Si un servicio no existe en VPS, nssm stop/start reporta error y continuamos.
SERVICES = ["Kha0sysWatchdog3", "Kha0sysMathBot", "Kha0sysTradersBot", "Kha0sysAmo8"]


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
