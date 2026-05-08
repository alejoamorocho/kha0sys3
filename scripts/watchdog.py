"""
Watchdog — Kha0sys3
Monitor independiente que verifica la salud del bot de trading.
Corre como servicio NSSM separado.

Usa un archivo heartbeat (logs/bot_heartbeat) que el bot toca cada 10s.
Si el heartbeat no se actualiza en 2 minutos, el bot está hung.
"""

import sys
import os
import time
import subprocess
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
os.chdir(PROJECT_ROOT)

from src.monitoring.telegram_notifier import TelegramNotifier

CHECK_INTERVAL = 300        # 5 minutos entre chequeos
HEARTBEAT_MAX_AGE = 120     # 2 minutos — si heartbeat no se actualiza, está hung
SERVICE_NAME = "Kha0sysMathBot"
HEARTBEAT_FILE = os.path.join(PROJECT_ROOT, "logs", "math_bot_heartbeat")


def check_service_running() -> bool:
    """Verifica si el servicio NSSM del bot esta corriendo."""
    try:
        result = subprocess.run(
            ["C:\\nssm\\nssm.exe", "status", SERVICE_NAME],
            capture_output=True, timeout=10,
        )
        raw = result.stdout
        # NSSM devuelve UTF-16 LE en Windows
        for encoding in ["utf-16-le", "utf-8", "ascii"]:
            try:
                output = raw.decode(encoding, errors="ignore")
                if "SERVICE_RUNNING" in output:
                    return True
                if "SERVICE_STOPPED" in output or "SERVICE_PAUSED" in output:
                    return False
            except Exception:
                continue
        return False
    except Exception:
        return False


def check_heartbeat_fresh() -> bool:
    """Verifica que el archivo heartbeat se haya tocado recientemente."""
    try:
        if not os.path.exists(HEARTBEAT_FILE):
            return False
        mtime = os.path.getmtime(HEARTBEAT_FILE)
        age = time.time() - mtime
        return age < HEARTBEAT_MAX_AGE
    except Exception:
        return False


def restart_service():
    """Reinicia el servicio del bot via NSSM."""
    print(f"[Watchdog] Reiniciando {SERVICE_NAME}...")
    subprocess.run(
        ["C:\\nssm\\nssm.exe", "stop", SERVICE_NAME],
        capture_output=True, timeout=30,
    )
    time.sleep(5)
    subprocess.run(
        ["C:\\nssm\\nssm.exe", "start", SERVICE_NAME],
        capture_output=True, timeout=30,
    )


def main():
    telegram = TelegramNotifier()
    consecutive_failures = 0

    print(f"[Watchdog] Iniciado — monitoreando {SERVICE_NAME}")
    print(f"[Watchdog] Heartbeat file: {HEARTBEAT_FILE}")
    print(f"[Watchdog] Check interval: {CHECK_INTERVAL}s, Max heartbeat age: {HEARTBEAT_MAX_AGE}s")

    while True:
        try:
            service_ok = check_service_running()
            heartbeat_ok = check_heartbeat_fresh()

            now_str = datetime.now(timezone.utc).strftime("%H:%M")

            if not service_ok:
                consecutive_failures += 1
                print(f"[Watchdog] [{now_str}] Servicio NO corriendo (fallo #{consecutive_failures})")

                if consecutive_failures >= 2:
                    telegram.notify_error(
                        f"Servicio {SERVICE_NAME} caido. Reiniciando...",
                        "Watchdog",
                    )
                    restart_service()
                    time.sleep(30)

                    if check_service_running():
                        consecutive_failures = 0
                        print(f"[Watchdog] [{now_str}] Reinicio exitoso")
                    else:
                        telegram.notify_error(
                            f"Reinicio de {SERVICE_NAME} fallo.",
                            "Watchdog",
                        )

            elif not heartbeat_ok:
                consecutive_failures += 1
                print(f"[Watchdog] [{now_str}] Heartbeat stale (fallo #{consecutive_failures})")

                if consecutive_failures >= 3:
                    # 3 fallos * 5 min = 15 min sin heartbeat
                    telegram.notify_error(
                        f"Bot sin heartbeat hace >{HEARTBEAT_MAX_AGE * consecutive_failures}s. Reiniciando...",
                        "Watchdog",
                    )
                    restart_service()
                    consecutive_failures = 0
            else:
                if consecutive_failures > 0:
                    print(f"[Watchdog] [{now_str}] Recuperado (service OK, heartbeat OK)")
                consecutive_failures = 0

        except Exception as e:
            print(f"[Watchdog] Error: {e}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[Watchdog] Detenido por senal de parada.")
