"""
Watchdog — Kha0sys3
Monitor independiente que verifica la salud del bot de trading.
Corre como servicio NSSM separado.
"""

import sys
import os
import time
import subprocess
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
os.chdir(PROJECT_ROOT)

from src.monitoring.telegram_notifier import TelegramNotifier

CHECK_INTERVAL = 300  # 5 minutos
SERVICE_NAME = "Kha0sysBot3"


def check_service_running() -> bool:
    """Verifica si el servicio NSSM del bot esta corriendo."""
    try:
        result = subprocess.run(
            ["C:\\nssm\\nssm.exe", "status", SERVICE_NAME],
            capture_output=True, text=True, timeout=10,
        )
        return "SERVICE_RUNNING" in result.stdout
    except Exception:
        return False


def check_log_freshness(log_path: str, max_age_seconds: int = 600) -> bool:
    """Verifica que el log del bot se haya actualizado recientemente."""
    try:
        if not os.path.exists(log_path):
            return False
        mtime = os.path.getmtime(log_path)
        age = time.time() - mtime
        return age < max_age_seconds
    except Exception:
        return False


def restart_service():
    """Reinicia el servicio del bot via NSSM."""
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
    log_path = os.path.join(PROJECT_ROOT, "logs", "bot_stdout.log")
    consecutive_failures = 0

    print(f"[Watchdog] Iniciado — monitoreando {SERVICE_NAME}")

    while True:
        try:
            service_ok = check_service_running()
            log_fresh = check_log_freshness(log_path)

            if not service_ok:
                consecutive_failures += 1
                print(f"[Watchdog] Servicio NO corriendo (fallo #{consecutive_failures})")

                if consecutive_failures >= 2:
                    telegram.notify_error(
                        f"Servicio {SERVICE_NAME} caido. Reiniciando...",
                        "Watchdog",
                    )
                    restart_service()
                    time.sleep(30)

                    if check_service_running():
                        telegram.notify_heartbeat(0, 0)
                        consecutive_failures = 0
                    else:
                        telegram.notify_error(
                            f"Reinicio de {SERVICE_NAME} fallo.", "Watchdog"
                        )
            elif not log_fresh:
                consecutive_failures += 1
                if consecutive_failures >= 3:
                    telegram.notify_error(
                        "Log del bot no se actualiza hace >10min. Posible hang.",
                        "Watchdog",
                    )
                    restart_service()
                    consecutive_failures = 0
            else:
                consecutive_failures = 0

        except Exception as e:
            print(f"[Watchdog] Error: {e}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
