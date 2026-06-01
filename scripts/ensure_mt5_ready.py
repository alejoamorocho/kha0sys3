"""Ensure MT5 is ready for bot trading.

Runs on the VPS (called by deploy/pull_and_restart.py before starting services).
Three responsibilities:

  1) common.ini patch: force [Experts] Enabled=1 so MT5 starts with the
     menu-level "Allow algorithmic trading" enabled. Without this every
     MT5 restart defaults Enabled=0 and the bots get retcode=10027.

  2) Kill any orphan terminal64.exe in Session 0. Multiple MT5 instances
     across sessions cause the bot API to attach to the wrong one and
     yields trade_allowed=False intermittently. We keep at most one
     terminal64 — the interactive one in the user's session if it exists,
     otherwise launch a fresh one.

  3) Verify trade_allowed via MT5 API. If False, print a clear instruction
     for the user to click Ctrl+E in the MT5 GUI. Exit 0 anyway so the
     deploy continues — the bots will retry order_send and skip silently
     until the user toggles AutoTrading.

Idempotent: safe to call on every restart.
"""
from __future__ import annotations
import os
import sys
import subprocess
import time
from pathlib import Path


COMMON_INI = (
    r"C:\Users\Administrator\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\config\common.ini"
)
MT5_EXE = r"C:\Program Files\MetaTrader 5\terminal64.exe"


def ps(cmd: str, timeout: int = 60) -> tuple[str, str]:
    r = subprocess.run(
        ["powershell", "-NoProfile", "-Command", cmd],
        capture_output=True, text=True, timeout=timeout,
    )
    return r.stdout.strip(), r.stderr.strip()


def patch_common_ini() -> bool:
    """Force [Experts] Enabled=1 in common.ini. Preserves UTF-16 LE + BOM.

    Returns True if file was modified, False if already correct or not found.
    """
    p = Path(COMMON_INI)
    if not p.exists():
        print(f"[ensure_mt5] common.ini not found at {p}")
        return False
    raw = p.read_bytes()
    if raw[:2] == b"\xff\xfe":
        bom = b"\xff\xfe"; text = raw[2:].decode("utf-16-le")
    elif raw[:2] == b"\xfe\xff":
        bom = b"\xfe\xff"; text = raw[2:].decode("utf-16-be")
    else:
        bom = b""; text = raw.decode("utf-8", errors="replace")

    new_lines = []
    in_experts = False
    patched = False
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("["):
            in_experts = (s.lower() == "[experts]")
        if in_experts and s == "Enabled=0":
            new_lines.append("Enabled=1")
            patched = True
        else:
            new_lines.append(line)

    if not patched:
        print("[ensure_mt5] common.ini already has Enabled=1 (or section not found)")
        return False

    # Write back preserving original encoding
    if bom:
        out = bom + ("\r\n".join(new_lines) + "\r\n").encode(
            "utf-16-le" if bom == b"\xff\xfe" else "utf-16-be"
        )
    else:
        out = ("\r\n".join(new_lines) + "\r\n").encode("utf-8")
    p.write_bytes(out)
    print("[ensure_mt5] patched common.ini: [Experts] Enabled=0 -> 1")
    return True


def cleanup_orphan_terminals() -> None:
    """Kill terminal64.exe processes in Session 0 (services session).

    Bot services run in Session 0 and try to attach to MT5. If there's a
    Session 0 terminal64 floating around (often spawned by service auto-
    start or MT5 broker autoupdate), the bots attach to THAT instance,
    which is headless / has no AutoTrading button accessible. We kill it
    so the bots attach to the interactive Session 2 MT5 instead.
    """
    out, _ = ps(
        'Get-CimInstance Win32_Process -Filter "Name=\'terminal64.exe\'" | '
        'Select-Object ProcessId,SessionId | ConvertTo-Json -Compress'
    )
    if not out or out == "null":
        print("[ensure_mt5] no terminal64.exe processes running, launching one")
        ps(f'Start-Process -FilePath "{MT5_EXE}" -WindowStyle Hidden')
        time.sleep(8)
        return

    import json
    procs = json.loads(out)
    if isinstance(procs, dict):
        procs = [procs]
    killed = 0
    kept = []
    for p in procs:
        pid = int(p["ProcessId"]); sid = int(p["SessionId"])
        if sid == 0:
            ps(f"Stop-Process -Id {pid} -Force -ErrorAction SilentlyContinue")
            killed += 1
            print(f"[ensure_mt5] killed orphan terminal64 PID={pid} Session=0")
        else:
            kept.append((pid, sid))
    print(f"[ensure_mt5] terminal64 kept: {kept}")
    if not kept:
        # No interactive terminal — launch one via scheduled task so it goes
        # into Administrator's interactive session (whichever is active).
        print("[ensure_mt5] no interactive MT5; launching via scheduled task")
        launch_mt5_interactive()


def launch_mt5_interactive() -> None:
    """Launch MT5 in Administrator's interactive session via Task Scheduler."""
    task_name = "Kha0sysMT5Boot"
    cmd = (
        f"Unregister-ScheduledTask -TaskName {task_name} -Confirm:$false -ErrorAction SilentlyContinue; "
        f"$action  = New-ScheduledTaskAction -Execute '{MT5_EXE}'; "
        "$trigger = New-ScheduledTaskTrigger -At (Get-Date).AddSeconds(10) -Once; "
        "$principal = New-ScheduledTaskPrincipal -UserId Administrator -LogonType Interactive -RunLevel Highest; "
        "$task = New-ScheduledTask -Action $action -Trigger $trigger -Principal $principal; "
        f"Register-ScheduledTask -TaskName {task_name} -InputObject $task -Force | Out-Null; "
        f"Start-ScheduledTask -TaskName {task_name}; "
        "Start-Sleep -Seconds 15; "
        f"Unregister-ScheduledTask -TaskName {task_name} -Confirm:$false -ErrorAction SilentlyContinue"
    )
    out, err = ps(cmd, timeout=60)
    if err:
        print(f"[ensure_mt5] launch_mt5_interactive stderr: {err[:300]}")


def verify_trade_allowed() -> bool:
    """Check MT5 API for trade_allowed flag and report status."""
    try:
        import MetaTrader5 as mt5  # type: ignore
    except ImportError:
        print("[ensure_mt5] MetaTrader5 module not importable")
        return False

    for attempt in range(6):
        if mt5.initialize():
            ti = mt5.terminal_info()
            ai = mt5.account_info()
            if ti and ai:
                if ti.trade_allowed and ai.trade_allowed:
                    print(f"[ensure_mt5] trade_allowed=True (terminal+account)")
                    mt5.shutdown()
                    return True
                else:
                    if attempt == 5:
                        print(
                            f"[ensure_mt5] WARNING trade_allowed=False "
                            f"(terminal={ti.trade_allowed}, account={ai.trade_allowed}). "
                            f"USER ACTION: connect via RDP and press Ctrl+E in MT5 "
                            f"toolbar to toggle AutoTrading button ON."
                        )
            mt5.shutdown()
        time.sleep(3)
    return False


def main() -> int:
    print("[ensure_mt5] Step 1: patch common.ini Enabled=1")
    patch_common_ini()

    print("[ensure_mt5] Step 2: cleanup orphan terminal64 in Session 0")
    cleanup_orphan_terminals()

    print("[ensure_mt5] Step 3: verify trade_allowed via API")
    verify_trade_allowed()

    # Always exit 0 — failing here would block deploy of working code.
    return 0


if __name__ == "__main__":
    sys.exit(main())
