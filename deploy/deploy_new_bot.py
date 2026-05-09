"""
Deploy Kha0sys3 — Script de despliegue completo
Ejecutar desde tu PC local. Conecta al VPS, elimina el bot viejo, clona el nuevo repo,
instala dependencias y registra servicios NSSM.

Uso:
    python deploy/deploy_new_bot.py
"""

import sys
import os
import time

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _REPO_ROOT)
from deploy.vps_connection import VPSConnection

# --- Configuracion ---
OLD_BOT_PATH = r"C:\Proyectos\Kha0sys"
NEW_BOT_PATH = r"C:\Proyectos\kha0sys3"
REPO_URL = "https://github.com/alejoamorocho/kha0sys3.git"

OLD_SERVICES = ["Kha0sysBot", "Kha0sysWatchdog"]
NEW_SERVICES = {
    "Kha0sysBot3": {
        "exe": r"C:\Python312\python.exe",
        "args": f"-u {NEW_BOT_PATH}\\scripts\\run_bot_supervisor.py",
        "workdir": NEW_BOT_PATH,
        "stdout": f"{NEW_BOT_PATH}\\logs\\bot_stdout.log",
        "stderr": f"{NEW_BOT_PATH}\\logs\\bot_stderr.log",
        "restart_delay": 10000,
    },
    "Kha0sysWatchdog3": {
        "exe": r"C:\Python312\python.exe",
        "args": f"-u {NEW_BOT_PATH}\\scripts\\watchdog.py",
        "workdir": NEW_BOT_PATH,
        "stdout": f"{NEW_BOT_PATH}\\logs\\watchdog_stdout.log",
        "stderr": f"{NEW_BOT_PATH}\\logs\\watchdog_stderr.log",
        "restart_delay": 5000,
    },
}


def step(msg: str):
    print(f"\n{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}")


def run_and_print(vps: VPSConnection, script: str, label: str = "") -> dict:
    result = vps.run_ps(script)
    if label:
        print(f"[{label}]")
    if result["stdout"]:
        print(f"  stdout: {result['stdout'][:500]}")
    if result["stderr"]:
        print(f"  stderr: {result['stderr'][:500]}")
    return result


def main():
    vps = VPSConnection()

    # --- 1. Test conexion ---
    step("1. Verificando conexion al VPS")
    if not vps.test_connection():
        print("ERROR: No se pudo conectar al VPS. Abortando.")
        sys.exit(1)
    print("Conexion exitosa.")

    # --- 2. Parar servicios viejos ---
    step("2. Deteniendo servicios del bot viejo")
    for svc in OLD_SERVICES:
        run_and_print(vps, f"C:\\nssm\\nssm.exe stop {svc}", f"Stop {svc}")
        time.sleep(2)

    # --- 3. Eliminar servicios viejos de NSSM ---
    step("3. Eliminando registros NSSM del bot viejo")
    for svc in OLD_SERVICES:
        run_and_print(vps, f"C:\\nssm\\nssm.exe remove {svc} confirm", f"Remove {svc}")

    # --- 4. Eliminar tarea programada vieja ---
    step("4. Eliminando tarea programada vieja")
    run_and_print(
        vps,
        "Unregister-ScheduledTask -TaskName 'Kha0sysWeeklyRestart' -Confirm:$false -ErrorAction SilentlyContinue",
        "Remove ScheduledTask",
    )

    # --- 5. Eliminar directorio del bot viejo ---
    step("5. Eliminando directorio del bot viejo")
    run_and_print(
        vps,
        f"if (Test-Path '{OLD_BOT_PATH}') {{ Remove-Item -Path '{OLD_BOT_PATH}' -Recurse -Force; 'Eliminado' }} else {{ 'No existia' }}",
        "Delete old bot",
    )

    # --- 6. Clonar nuevo repo ---
    step("6. Clonando nuevo repositorio desde GitHub")
    # Verificar si ya existe
    check = vps.run_ps(f"Test-Path '{NEW_BOT_PATH}'")
    if "True" in check["stdout"]:
        print("Directorio ya existe. Haciendo git pull...")
        run_and_print(
            vps,
            f"cd '{NEW_BOT_PATH}'; git pull origin main",
            "Git pull",
        )
    else:
        run_and_print(
            vps,
            f"cd C:\\Proyectos; git clone {REPO_URL}",
            "Git clone",
        )

    # --- 7. Crear directorios necesarios ---
    step("7. Creando directorios necesarios")
    dirs_to_create = [
        f"{NEW_BOT_PATH}\\logs",
        f"{NEW_BOT_PATH}\\config",
        f"{NEW_BOT_PATH}\\data\\live_state",
    ]
    for d in dirs_to_create:
        run_and_print(
            vps,
            f"if (-not (Test-Path '{d}')) {{ New-Item -ItemType Directory -Path '{d}' -Force | Out-Null; 'Creado: {d}' }} else {{ 'Existe: {d}' }}",
            f"Dir {d.split(chr(92))[-1]}",
        )

    # --- 8. Crear configs ---
    step("8. Creando archivos de configuracion")

    # Lee configs locales (gitignored) y los sube tal cual al VPS.
    # Si los archivos no existen, aborta antes de tocar el VPS.
    local_telegram = os.path.join(_REPO_ROOT, "config", "telegram.yaml")
    local_broker = os.path.join(_REPO_ROOT, "config", "broker.yaml")
    for f in (local_telegram, local_broker):
        if not os.path.exists(f):
            raise SystemExit(
                f"deploy_new_bot: falta {f}. Crea los configs locales antes "
                f"de desplegar (ver .env.example y config/*.yaml)."
            )
    with open(local_telegram, "r", encoding="utf-8") as f:
        telegram_yaml = f.read()
    vps.upload_file(telegram_yaml, f"{NEW_BOT_PATH}\\config\\telegram.yaml")
    print("  telegram.yaml subido desde config/ local")

    with open(local_broker, "r", encoding="utf-8") as f:
        broker_yaml = f.read()
    vps.upload_file(broker_yaml, f"{NEW_BOT_PATH}\\config\\broker.yaml")
    print("  broker.yaml subido desde config/ local")

    # --- 9. Instalar dependencias ---
    step("9. Instalando dependencias Python")
    packages = (
        "MetaTrader5 polars pyarrow duckdb numpy scipy scikit-learn "
        "hmmlearn filterpy riskfolio-lib optuna python-telegram-bot "
        "streamlit plotly pyyaml psutil requests pywinrm"
    )
    run_and_print(
        vps,
        f"C:\\Python312\\python.exe -m pip install --upgrade {packages}",
        "pip install",
    )

    # --- 10. Registrar nuevos servicios NSSM ---
    step("10. Registrando nuevos servicios NSSM")
    for svc_name, cfg in NEW_SERVICES.items():
        # Primero intentar remover por si ya existe
        vps.run_ps(f"C:\\nssm\\nssm.exe stop {svc_name} 2>$null")
        vps.run_ps(f"C:\\nssm\\nssm.exe remove {svc_name} confirm 2>$null")
        time.sleep(1)

        # Registrar
        run_and_print(
            vps,
            f'C:\\nssm\\nssm.exe install {svc_name} "{cfg["exe"]}" "{cfg["args"]}"',
            f"Install {svc_name}",
        )

        # Configurar parametros
        nssm_sets = [
            f'C:\\nssm\\nssm.exe set {svc_name} AppDirectory "{cfg["workdir"]}"',
            f'C:\\nssm\\nssm.exe set {svc_name} AppStdout "{cfg["stdout"]}"',
            f'C:\\nssm\\nssm.exe set {svc_name} AppStderr "{cfg["stderr"]}"',
            f'C:\\nssm\\nssm.exe set {svc_name} AppRestartDelay {cfg["restart_delay"]}',
            f"C:\\nssm\\nssm.exe set {svc_name} AppRotateFiles 1",
            f"C:\\nssm\\nssm.exe set {svc_name} AppRotateBytes 10485760",
        ]
        for cmd in nssm_sets:
            vps.run_ps(cmd)
        print(f"  {svc_name} configurado")

    # --- 11. Crear tarea de reinicio semanal ---
    step("11. Creando tarea de reinicio semanal")
    restart_script = (
        f"C:\\nssm\\nssm.exe stop Kha0sysBot3; "
        f"C:\\nssm\\nssm.exe stop Kha0sysWatchdog3; "
        f"Start-Sleep -Seconds 5; "
        f"C:\\nssm\\nssm.exe start Kha0sysBot3; "
        f"C:\\nssm\\nssm.exe start Kha0sysWatchdog3"
    )
    scheduled_task_ps = (
        f"$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument '-Command \"{restart_script}\"';"
        f"$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At '20:00';"
        f"Register-ScheduledTask -TaskName 'Kha0sys3WeeklyRestart' -Action $action -Trigger $trigger "
        f"-User 'Administrator' -Password '{VPSConnection.VPS_PASS}' -RunLevel Highest -Force"
    )
    run_and_print(vps, scheduled_task_ps, "ScheduledTask")

    # --- 12. Iniciar servicios ---
    step("12. Iniciando servicios")
    for svc_name in NEW_SERVICES:
        run_and_print(vps, f"C:\\nssm\\nssm.exe start {svc_name}", f"Start {svc_name}")
        time.sleep(3)

    # --- 13. Verificacion final ---
    step("13. Verificacion final")
    time.sleep(10)  # Dar tiempo a que arranque

    for svc_name in NEW_SERVICES:
        run_and_print(vps, f"C:\\nssm\\nssm.exe status {svc_name}", f"Status {svc_name}")

    run_and_print(
        vps,
        f"if (Test-Path '{NEW_BOT_PATH}\\logs\\bot_stdout.log') {{ Get-Content '{NEW_BOT_PATH}\\logs\\bot_stdout.log' -Tail 10 }} else {{ 'Log aun no creado' }}",
        "Recent logs",
    )

    print("\n" + "=" * 60)
    print("  DEPLOY COMPLETADO")
    print("=" * 60)
    print(f"  Bot nuevo: {NEW_BOT_PATH}")
    print(f"  Servicios: {', '.join(NEW_SERVICES.keys())}")
    print(f"  Repo: {REPO_URL}")
    print("=" * 60)


if __name__ == "__main__":
    main()
