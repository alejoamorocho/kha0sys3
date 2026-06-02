"""Ensure a single MT5 terminal is running in an INTERACTIVE session with
AutoTrading ON, so the Session-0 bot services can connect cross-session and
trade.

Key learnings (2026-06-02):
  - Bots run as NSSM services in Session 0. They connect cross-session to a
    terminal running in the user's interactive session (Session 2) — this
    WORKS (5 positions were opened this way).
  - The terminal must be in an interactive session because AutoTrading's
    toolbar button only initialises ON when launched interactively with
    common.ini [Experts] Enabled=1, and can be toggled via Ctrl+E.
  - DO NOT kill this terminal. Re-login by MathBot is avoided via the
    attach-first fix in mt5_client.py.

This script is idempotent. Run it after a reboot or if AutoTrading drops.
"""
import subprocess, time, os, sys

def ps(cmd, timeout=120):
    r = subprocess.run(["powershell","-NoProfile","-Command",cmd],
                       capture_output=True, text=True, timeout=timeout)
    return r.stdout.strip(), r.stderr.strip()

DATA = r"C:\Users\Administrator\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075"
INI = os.path.join(DATA, "config", "common.ini")
EXE = r"C:\Program Files\MetaTrader 5\terminal64.exe"

# 1. common.ini Enabled=1
print("[1] patch common.ini Enabled=1")
raw = open(INI,"rb").read()
bom = raw[:2]
enc = "utf-16-le" if bom == b"\xff\xfe" else "utf-8"
text = raw.decode(enc).lstrip("﻿")
lines, in_exp, patched = [], False, False
for line in text.splitlines():
    s = line.strip()
    if s.startswith("["): in_exp = (s.lower() == "[experts]")
    if in_exp and s.startswith("Enabled="):
        lines.append("Enabled=1"); patched = (s != "Enabled=1")
    else:
        lines.append(line)
open(INI,"wb").write(bom + ("\r\n".join(lines)+"\r\n").encode(enc))
print(f"    patched={patched}")

# 2. Is a terminal already running in an interactive session (>0)?
out,_ = ps(r"Get-CimInstance Win32_Process -Filter \"Name='terminal64.exe'\" | ForEach-Object { \"$($_.ProcessId):$($_.SessionId)\" }")
procs = [p for p in out.split() if ":" in p]
interactive = [p for p in procs if int(p.split(":")[1]) > 0]
print(f"[2] terminal64 procs: {procs or '(none)'}  interactive={interactive or '(none)'}")

if not interactive:
    print("[3] launching MT5 in interactive session via scheduled task")
    launch = r'''
$task = 'KhaosysMT5Boot'
Unregister-ScheduledTask -TaskName $task -Confirm:$false -ErrorAction SilentlyContinue
$action = New-ScheduledTaskAction -Execute 'C:\Program Files\MetaTrader 5\terminal64.exe'
$trigger = New-ScheduledTaskTrigger -At (Get-Date).AddSeconds(20) -Once
$principal = New-ScheduledTaskPrincipal -UserId Administrator -LogonType Interactive -RunLevel Highest
$t = New-ScheduledTask -Action $action -Trigger $trigger -Principal $principal
Register-ScheduledTask -TaskName $task -InputObject $t -Force | Out-Null
Start-ScheduledTask -TaskName $task
'''
    o, e = ps(launch)
    print(f"    {o} {e[:200]}")
    # wait for terminal to appear + login
    for i in range(15):
        time.sleep(5)
        out,_ = ps(r"Get-CimInstance Win32_Process -Filter \"Name='terminal64.exe'\" | ForEach-Object { \"$($_.ProcessId):$($_.SessionId)\" }")
        procs = [p for p in out.split() if ":" in p]
        if any(int(p.split(":")[1])>0 for p in procs):
            print(f"    [{i+1}] terminal up: {procs}")
            break
    ps("Unregister-ScheduledTask -TaskName KhaosysMT5Boot -Confirm:$false -ErrorAction SilentlyContinue")
    time.sleep(15)  # let it login to broker

# 4. Toggle AutoTrading ON from within the interactive session
print("[4] enable AutoTrading via in-session Ctrl+E")
toggle = r'''
$task = 'KhaosysAT'
Unregister-ScheduledTask -TaskName $task -Confirm:$false -ErrorAction SilentlyContinue
$action = New-ScheduledTaskAction -Execute 'C:\Python312\python.exe' -Argument 'C:\Proyectos\kha0sys3\scripts\_toggle_autotrading_v2.py'
$trigger = New-ScheduledTaskTrigger -At (Get-Date).AddSeconds(15) -Once
$principal = New-ScheduledTaskPrincipal -UserId Administrator -LogonType Interactive -RunLevel Highest
$t = New-ScheduledTask -Action $action -Trigger $trigger -Principal $principal
Register-ScheduledTask -TaskName $task -InputObject $t -Force | Out-Null
Start-ScheduledTask -TaskName $task
Start-Sleep -Seconds 25
Unregister-ScheduledTask -TaskName $task -Confirm:$false -ErrorAction SilentlyContinue
Get-Content C:\Temp\autotrading_result.txt -ErrorAction SilentlyContinue
'''
o,_ = ps(toggle)
print(o)

# 5. final state
print("[5] final terminal procs:")
out,_ = ps(r"Get-CimInstance Win32_Process -Filter \"Name='terminal64.exe'\" | Select-Object ProcessId,SessionId | Format-Table -AutoSize | Out-String")
print(out)
