"""Launch MT5 in Administrator's interactive session using PowerShell native
Register-ScheduledTask (handles paths with spaces correctly).

Also ensures MT5 is running even if interactive launch fails (fallback to
Session 0).
"""
import subprocess
import time
import os
import MetaTrader5 as mt5

def ps(cmd, timeout=60):
    r = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, timeout=timeout)
    return r.stdout.strip(), r.stderr.strip()

# Find MT5 exe via filesystem since MT5 is currently NOT running
exe_path = r"C:\Program Files\MetaTrader 5\terminal64.exe"
if not os.path.exists(exe_path):
    out, _ = ps(r"Get-ChildItem -Path 'C:\Program Files\' -Recurse -Filter terminal64.exe -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName")
    exe_path = out.strip()
print(f"MT5 exe: {exe_path}")
if not exe_path:
    print("ABORT: terminal64.exe not found")
    raise SystemExit(1)

# Check current sessions
print("\n=== Current sessions ===")
out, _ = ps("qwinsta")
print(out)

# Try interactive launch via PowerShell scheduled task
print("\n=== Approach 1: PowerShell native scheduled task (interactive) ===")
ps_cmd = f"""
$task_name = 'Kha0sysMT5Interactive'
Unregister-ScheduledTask -TaskName $task_name -Confirm:$false -ErrorAction SilentlyContinue
$action  = New-ScheduledTaskAction -Execute '{exe_path}'
$trigger = New-ScheduledTaskTrigger -At (Get-Date).AddSeconds(30) -Once
$principal = New-ScheduledTaskPrincipal -UserId Administrator -LogonType Interactive -RunLevel Highest
$task = New-ScheduledTask -Action $action -Trigger $trigger -Principal $principal
Register-ScheduledTask -TaskName $task_name -InputObject $task -Force | Out-Null
Write-Output 'Task registered'
Start-ScheduledTask -TaskName $task_name
Write-Output 'Task started'
Start-Sleep -Seconds 8
$procs = Get-CimInstance Win32_Process -Filter "Name='terminal64.exe'" | Select-Object ProcessId,SessionId
Write-Output ('terminal64 processes: ' + ($procs | Out-String))
Unregister-ScheduledTask -TaskName $task_name -Confirm:$false -ErrorAction SilentlyContinue
"""
out, err = ps(ps_cmd, timeout=120)
print(out)
if err:
    print(f"stderr: {err[:500]}")

# Verify
time.sleep(5)
print("\n=== Verify MT5 state ===")
out, _ = ps(r"Get-CimInstance Win32_Process -Filter \"Name='terminal64.exe'\" | Select-Object ProcessId,SessionId | Format-Table -AutoSize | Out-String")
print(out)

# If no MT5 in user session, fallback: launch in Session 0 (services)
if not out.strip() or "0\n" in out and "1\n" not in out and "2\n" not in out:
    print("\n=== Fallback: launching MT5 normally (Session 0) so bots can at least connect ===")
    out, _ = ps(f"Start-Process -FilePath '{exe_path}' -WindowStyle Hidden")
    time.sleep(8)
    out, _ = ps(r"Get-CimInstance Win32_Process -Filter \"Name='terminal64.exe'\" | Select-Object ProcessId,SessionId | Format-Table -AutoSize | Out-String")
    print(out)

# Final verify via MT5 API
print("\n=== Final MT5 API check ===")
for i in range(10):
    time.sleep(3)
    if mt5.initialize():
        ti = mt5.terminal_info()
        if ti and ti.connected:
            print(f"  [{i+1}/10] connected=True  trade_allowed={ti.trade_allowed}")
            mt5.shutdown()
            break
        else:
            print(f"  [{i+1}/10] not connected yet")
            mt5.shutdown()
    else:
        print(f"  [{i+1}/10] init failed")
