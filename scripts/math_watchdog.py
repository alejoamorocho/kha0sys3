"""
Math Watchdog - Kha0sys3 MATH parallel runner
Monitors Kha0sysMathBot service + logs/math_bot_heartbeat freshness.
Restarts the service when heartbeat is stale. Mirrors scripts/watchdog.py
but scoped to the MATH bot only (magic 1338). Independent from FADE.
"""

import sys
import os
import time
import subprocess
from datetime import datetime, timezone

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
os.chdir(PROJECT_ROOT)

from src.monitoring.telegram_notifier import TelegramNotifier

CHECK_INTERVAL = 300        # 5 minutes between checks
HEARTBEAT_MAX_AGE = 120     # 2 minutes
SERVICE_NAME = "Kha0sysMathBot"
HEARTBEAT_FILE = os.path.join(PROJECT_ROOT, "logs", "math_bot_heartbeat")


def check_service_running() -> bool:
    try:
        result = subprocess.run(
            ["C:\\nssm\\nssm.exe", "status", SERVICE_NAME],
            capture_output=True, timeout=10,
        )
        raw = result.stdout
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
    try:
        if not os.path.exists(HEARTBEAT_FILE):
            return False
        mtime = os.path.getmtime(HEARTBEAT_FILE)
        age = time.time() - mtime
        return age < HEARTBEAT_MAX_AGE
    except Exception:
        return False


def restart_service():
    print(f"[MathWatchdog] Restarting {SERVICE_NAME}...")
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

    print(f"[MathWatchdog] Started - monitoring {SERVICE_NAME}")
    print(f"[MathWatchdog] Heartbeat file: {HEARTBEAT_FILE}")

    while True:
        try:
            service_ok = check_service_running()
            heartbeat_ok = check_heartbeat_fresh()
            now_str = datetime.now(timezone.utc).strftime("%H:%M")

            if not service_ok:
                consecutive_failures += 1
                print(f"[MathWatchdog] [{now_str}] Service NOT running "
                      f"(fail #{consecutive_failures})")
                if consecutive_failures >= 2:
                    telegram.notify_error(
                        f"[MATH] Service {SERVICE_NAME} down. Restarting...",
                        "MathWatchdog",
                    )
                    restart_service()
                    time.sleep(30)
                    if check_service_running():
                        consecutive_failures = 0
                        print(f"[MathWatchdog] [{now_str}] Restart OK")
                    else:
                        telegram.notify_error(
                            f"[MATH] Restart of {SERVICE_NAME} FAILED.",
                            "MathWatchdog",
                        )
            elif not heartbeat_ok:
                consecutive_failures += 1
                print(f"[MathWatchdog] [{now_str}] Heartbeat stale "
                      f"(fail #{consecutive_failures})")
                if consecutive_failures >= 3:
                    telegram.notify_error(
                        f"[MATH] Bot no heartbeat "
                        f">{HEARTBEAT_MAX_AGE * consecutive_failures}s. Restarting...",
                        "MathWatchdog",
                    )
                    restart_service()
                    consecutive_failures = 0
            else:
                if consecutive_failures > 0:
                    print(f"[MathWatchdog] [{now_str}] Recovered")
                consecutive_failures = 0

        except Exception as e:
            print(f"[MathWatchdog] Error: {e}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[MathWatchdog] Stopped.")
