"""
VPS Diagnostics — Kha0sys3
Diagnostico completo del estado del VPS. Ejecutar desde local.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deploy.vps_connection import VPSConnection

BOT_PATH = r"C:\Proyectos\kha0sys3"
SERVICES = ["Kha0sysBot3", "Kha0sysWatchdog3"]


def section(title: str):
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")


def main():
    vps = VPSConnection()

    if not vps.test_connection():
        print("ERROR: No se pudo conectar al VPS.")
        sys.exit(1)

    # 1. Info del sistema
    section("Sistema")
    result = vps.run_ps("Get-Date; $env:COMPUTERNAME; [System.Environment]::OSVersion")
    print(result["stdout"])

    # 2. Estado de servicios
    section("Servicios NSSM")
    for svc in SERVICES:
        result = vps.run_ps(f"C:\\nssm\\nssm.exe status {svc}")
        print(f"  {svc}: {result['stdout'].strip()}")

    # 3. Python
    section("Python")
    result = vps.run_ps("C:\\Python312\\python.exe --version")
    print(f"  Version: {result['stdout']}")

    # 4. MT5
    section("MetaTrader 5")
    result = vps.run_ps(
        "C:\\Python312\\python.exe -c \"import MetaTrader5 as mt5; print(f'MT5 version: {mt5.__version__}')\""
    )
    print(f"  {result['stdout']}")
    if result["stderr"]:
        print(f"  Error: {result['stderr'][:200]}")

    # 5. Estructura del proyecto
    section("Estructura del Proyecto")
    result = vps.run_ps(f"if (Test-Path '{BOT_PATH}') {{ Get-ChildItem '{BOT_PATH}' -Name }} else {{ 'NO EXISTE' }}")
    print(result["stdout"])

    # 6. Configs
    section("Archivos de Configuracion")
    configs = ["config/telegram.yaml", "config/broker.yaml", "src/execution/bot_config.json"]
    for cfg in configs:
        full_path = f"{BOT_PATH}\\{cfg}"
        result = vps.run_ps(f"Test-Path '{full_path}'")
        exists = "OK" if "True" in result["stdout"] else "FALTA"
        print(f"  {cfg}: {exists}")

    # 7. Disco
    section("Espacio en Disco")
    result = vps.run_ps("Get-PSDrive C | Select-Object Used,Free | Format-List")
    print(result["stdout"])

    # 8. Procesos Python
    section("Procesos Python Activos")
    result = vps.run_ps("Get-Process python* -ErrorAction SilentlyContinue | Select-Object Id, ProcessName, StartTime | Format-Table")
    print(result["stdout"] or "  Ninguno")

    # 9. Logs recientes
    section("Logs Bot (ultimas 15 lineas)")
    result = vps.run_ps(
        f"if (Test-Path '{BOT_PATH}\\logs\\bot_stdout.log') "
        f"{{ Get-Content '{BOT_PATH}\\logs\\bot_stdout.log' -Tail 15 }} "
        f"else {{ 'Log no encontrado' }}"
    )
    print(result["stdout"])

    # 10. Errores recientes
    section("Errores Recientes (ultimas 10 lineas)")
    result = vps.run_ps(
        f"if (Test-Path '{BOT_PATH}\\logs\\bot_stderr.log') "
        f"{{ Get-Content '{BOT_PATH}\\logs\\bot_stderr.log' -Tail 10 }} "
        f"else {{ 'Sin errores' }}"
    )
    print(result["stdout"] or "  Sin errores")

    # 11. Git status
    section("Git Status")
    result = vps.run_ps(f"cd '{BOT_PATH}'; git log --oneline -5; echo '---'; git status --short")
    print(result["stdout"])

    print(f"\n{'='*50}")
    print("  Diagnostico completo.")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
