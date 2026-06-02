"""One-shot: consolidate to a single MT5 terminal in a console-active session
and enable AutoTrading.

  1. Kill ALL terminal64 (clean slate)
  2. tscon the Administrator (Session 2) to console -> becomes Active w/ focus
  3. Launch ONE terminal in that session
  4. Wait for broker login
  5. Toggle AutoTrading via in-session Ctrl+E (now focus works)
  6. Verify trade_allowed=True
"""
import subprocess, time, os, re

def ps(cmd, timeout=120):
    r = subprocess.run(["powershell","-NoProfile","-Command",cmd],
                       capture_output=True, text=True, timeout=timeout)
    return r.stdout.strip(), r.stderr.strip()

EXE = r"C:\Program Files\MetaTrader 5\terminal64.exe"

# 1. kill all terminals
print("[1] kill all terminal64")
ps("Get-Process terminal64 -ErrorAction SilentlyContinue | Stop-Process -Force")
time.sleep(3)

# 2. find Administrator session + tscon to console
print("[2] qwinsta + tscon admin -> console")
out,_ = ps("qwinsta")
print(out)
admin_id = None
for line in out.splitlines():
    if "Administrator" in line:
        m = re.search(r"\b(\d+)\b", line)
        if m: admin_id = m.group(1)
if admin_id:
    o,e = ps(f"tscon {admin_id} /dest:console")
    print(f"   tscon {admin_id}: {o} {e[:200]}")
else:
    print("   no Administrator session found; will rely on console session")
time.sleep(2)
out,_ = ps("qwinsta")
print(out)

# 3. launch ONE terminal in interactive session
print("[3] launch terminal in interactive session")
launch = r"""
$task='KhaosysMT5One'
Unregister-ScheduledTask -TaskName $task -Confirm:$false -ErrorAction SilentlyContinue
$action=New-ScheduledTaskAction -Execute 'C:\Program Files\MetaTrader 5\terminal64.exe'
$trigger=New-ScheduledTaskTrigger -At (Get-Date).AddSeconds(15) -Once
$principal=New-ScheduledTaskPrincipal -UserId Administrator -LogonType Interactive -RunLevel Highest
$t=New-ScheduledTask -Action $action -Trigger $trigger -Principal $principal
Register-ScheduledTask -TaskName $task -InputObject $t -Force | Out-Null
Start-ScheduledTask -TaskName $task
"""
ps(launch)
for i in range(12):
    time.sleep(5)
    out,_ = ps("Get-CimInstance Win32_Process -Filter \"Name='terminal64.exe'\" | ForEach-Object { \"$($_.ProcessId):$($_.SessionId)\" }")
    procs = [p for p in out.split() if ":" in p]
    if procs:
        print(f"   [{i+1}] {procs}")
        if any(int(p.split(':')[1])>0 for p in procs):
            break
ps("Unregister-ScheduledTask -TaskName KhaosysMT5One -Confirm:$false -ErrorAction SilentlyContinue")
print("   waiting 20s for broker login...")
time.sleep(20)

# 4+5. toggle AutoTrading in-session
print("[4] toggle AutoTrading")
toggle = r"""
$task='KhaosysATtog'
Unregister-ScheduledTask -TaskName $task -Confirm:$false -ErrorAction SilentlyContinue
$action=New-ScheduledTaskAction -Execute 'C:\Python312\python.exe' -Argument 'C:\Proyectos\kha0sys3\scripts\_toggle_autotrading_v2.py'
$trigger=New-ScheduledTaskTrigger -At (Get-Date).AddSeconds(12) -Once
$principal=New-ScheduledTaskPrincipal -UserId Administrator -LogonType Interactive -RunLevel Highest
$t=New-ScheduledTask -Action $action -Trigger $trigger -Principal $principal
Register-ScheduledTask -TaskName $task -InputObject $t -Force | Out-Null
Start-ScheduledTask -TaskName $task
Start-Sleep -Seconds 28
Unregister-ScheduledTask -TaskName $task -Confirm:$false -ErrorAction SilentlyContinue
Get-Content C:\Temp\autotrading_result.txt -ErrorAction SilentlyContinue
"""
o,_ = ps(toggle)
print(o)
