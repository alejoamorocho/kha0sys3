"""
Bot Supervisor — Kha0sys3
Entry point para NSSM. Supervisa y reinicia el LiveTraderEngine ante crashes.
Envia notificaciones Telegram de cada evento critico.
"""

import sys
import os
import time
import traceback
from datetime import datetime, timezone

# Asegurar que el proyecto este en sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
os.chdir(PROJECT_ROOT)

from src.execution.live_trader import LiveTraderEngine
from src.monitoring.telegram_notifier import TelegramNotifier

MAX_RESTARTS = 5
RESTART_COOLDOWN = 30  # segundos entre reintentos
RESTART_RESET_WINDOW = 3600  # resetear contador tras 1h estable


def main():
    telegram = TelegramNotifier()
    restart_count = 0
    last_restart_time = time.time()

    print(f"[Supervisor] Kha0sys3 Supervisor iniciado — {datetime.now(timezone.utc)}")
    telegram.notify_heartbeat(0, 0)

    while restart_count < MAX_RESTARTS:
        try:
            now = time.time()
            if now - last_restart_time > RESTART_RESET_WINDOW:
                restart_count = 0

            print(f"[Supervisor] Lanzando LiveTraderEngine (intento {restart_count + 1})")
            bot = LiveTraderEngine()
            bot.run()

            print("[Supervisor] Bot finalizo normalmente.")
            break

        except KeyboardInterrupt:
            print("[Supervisor] Interrupcion manual detectada.")
            telegram.notify_bot_stopped("KeyboardInterrupt via Supervisor")
            break

        except Exception as e:
            restart_count += 1
            last_restart_time = time.time()
            error_msg = f"{type(e).__name__}: {e}"
            tb = traceback.format_exc()

            print(f"[Supervisor] Crash #{restart_count}: {error_msg}")
            print(tb)

            telegram.notify_error(
                f"Crash #{restart_count}/{MAX_RESTARTS}: {error_msg}",
                "Supervisor",
            )

            if restart_count < MAX_RESTARTS:
                print(f"[Supervisor] Reiniciando en {RESTART_COOLDOWN}s...")
                time.sleep(RESTART_COOLDOWN)

    if restart_count >= MAX_RESTARTS:
        msg = f"Maximo de reinicios ({MAX_RESTARTS}) alcanzado. Supervisor detenido."
        print(f"[Supervisor] {msg}")
        telegram.notify_error(msg, "Supervisor")
        sys.exit(1)


if __name__ == "__main__":
    main()
