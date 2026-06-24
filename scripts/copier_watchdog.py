"""Copier liveness watchdog (NSSM service Kha0sysCopierWatchdog).

Watches the copier's heartbeat file. If it goes stale (the copier process is
HUNG or dead), it ALERTS Telegram and restarts Kha0sysCopier. Critical because
TMFinancials copies carry NO SL/TP — a frozen copier means an open Vantage
position with no exit and no monitoring.
"""
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

HEARTBEAT = Path(r"C:\ProgramData\Kha0sysCopier\copier_heartbeat")
LOG = Path(r"C:\ProgramData\Kha0sysCopier\logs\watchdog.log")
SERVICE = "Kha0sysCopier"
MAX_STALE_SEC = 90      # heartbeat older than this => the copier is hung/dead
CHECK_SEC = 30


def log(m: str) -> None:
    line = f"{datetime.now(timezone.utc).isoformat(timespec='seconds')} {m}"
    print(line, flush=True)
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def telegram(msg: str) -> None:
    try:
        from src.monitoring.telegram_notifier import TelegramNotifier
        TelegramNotifier()._send(f"[COPIER-WD] {msg}")
    except Exception as e:
        log(f"telegram err: {e}")


def heartbeat_age() -> float | None:
    """Seconds since the copier's last heartbeat, or None if unreadable."""
    try:
        ts = datetime.fromisoformat(HEARTBEAT.read_text(encoding="utf-8").strip())
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - ts).total_seconds()
    except Exception:
        return None


def restart_copier() -> None:
    try:
        subprocess.run(["powershell", "-NoProfile", "-Command",
                        f"Restart-Service {SERVICE} -Force"], timeout=90)
    except Exception as e:
        log(f"restart err: {e}")


def kill_session1_metabuy() -> int:
    """Kill any MetaBuy terminal NOT in session 0. A session-1 MetaBuy (e.g. the
    user reopening the GUI) would make the session-0 copier read positions
    cross-session and go blind. Keep TMF to ONE session-0 terminal. Returns count."""
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "$p = Get-CimInstance Win32_Process -Filter \"Name='terminal64.exe'\" | "
             "Where-Object { $_.ExecutablePath -like '*MetaBuy*' -and $_.SessionId -ne 0 }; "
             "$p | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }; "
             "($p | Measure-Object).Count"],
            capture_output=True, text=True, timeout=30)
        out = (r.stdout or "").strip()
        return int(out) if out.isdigit() else 0
    except Exception:
        return 0


def main() -> None:
    log("=== copier watchdog START ===")
    alerted = False
    missing_streak = 0
    while True:
        # Guard: a session-1 MetaBuy (reopened TMF GUI) makes the copier read
        # cross-session and go blind -> close it immediately and warn.
        n_killed = kill_session1_metabuy()
        if n_killed:
            log(f"killed {n_killed} session-1 MetaBuy")
            telegram(f"closed a session-1 MetaBuy/TMF window — it would blind the copier. "
                     f"Watch TMF on the mobile app instead.")

        age = heartbeat_age()
        if age is None:
            missing_streak += 1
            log(f"heartbeat missing (streak {missing_streak})")
            if missing_streak >= 3:   # ~90s with no readable heartbeat
                telegram("copier heartbeat MISSING — restarting (copies may be unprotected!)")
                restart_copier()
                alerted = True
                missing_streak = 0
                time.sleep(20)
        elif age > MAX_STALE_SEC:
            missing_streak = 0
            log(f"heartbeat STALE {age:.0f}s -> alert + restart {SERVICE}")
            telegram(f"copier heartbeat stale {age:.0f}s — restarting (copies may be unprotected!)")
            restart_copier()
            alerted = True
            time.sleep(20)
        else:
            missing_streak = 0
            if alerted:
                log("heartbeat recovered")
                telegram("copier heartbeat recovered — back alive")
                alerted = False
        time.sleep(CHECK_SEC)


if __name__ == "__main__":
    main()
