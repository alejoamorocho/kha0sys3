"""Configure Windows autologon + at-logon MT5/AutoTrading setup.

Reads VPS_PASS from C:\Proyectos\kha0sys3\.env (the Administrator password,
same one used for WinRM) and writes the autologon registry keys. Registers a
scheduled task that runs on_logon_setup.py at every Administrator logon.

After this + a reboot, the VPS will:
  - auto-login Administrator to an interactive console session
  - launch MT5, enable AutoTrading, restart bots — all unattended
"""
import os, subprocess, sys

def ps(cmd, timeout=60):
    r = subprocess.run(["powershell","-NoProfile","-Command",cmd], capture_output=True, text=True, timeout=timeout)
    return r.stdout.strip(), r.stderr.strip()

# read VPS_PASS from .env
pw = None
envp = r"C:\Proyectos\kha0sys3\.env"
for line in open(envp, encoding="utf-8"):
    if line.strip().startswith("VPS_PASS="):
        pw = line.split("=",1)[1].strip()
        break
if not pw:
    print("ERROR: VPS_PASS not found in .env"); sys.exit(1)
print("VPS_PASS loaded (hidden)")

# Hostname for DefaultDomainName
host,_ = ps("$env:COMPUTERNAME")
print(f"hostname: {host}")

# Set autologon registry keys
reg = r"HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"
cmds = [
    f"Set-ItemProperty -Path '{reg}' -Name AutoAdminLogon -Value '1' -Type String",
    f"Set-ItemProperty -Path '{reg}' -Name DefaultUserName -Value 'Administrator' -Type String",
    f"Set-ItemProperty -Path '{reg}' -Name DefaultPassword -Value '{pw}' -Type String",
    f"Set-ItemProperty -Path '{reg}' -Name DefaultDomainName -Value '{host}' -Type String",
    f"Set-ItemProperty -Path '{reg}' -Name AutoLogonCount -Value 0 -Type DWord -ErrorAction SilentlyContinue",
]
for c in cmds:
    o,e = ps(c)
    if e: print(f"  warn: {e[:150]}")
print("autologon registry set")

# Register at-logon scheduled task
task = r"""
$task='KhaosysOnLogon'
Unregister-ScheduledTask -TaskName $task -Confirm:$false -ErrorAction SilentlyContinue
$action=New-ScheduledTaskAction -Execute 'C:\Python312\python.exe' -Argument 'C:\Proyectos\kha0sys3\scripts\on_logon_setup.py'
$trigger=New-ScheduledTaskTrigger -AtLogOn -User Administrator
$principal=New-ScheduledTaskPrincipal -UserId Administrator -LogonType Interactive -RunLevel Highest
$settings=New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Minutes 10)
$t=New-ScheduledTask -Action $action -Trigger $trigger -Principal $principal -Settings $settings
Register-ScheduledTask -TaskName $task -InputObject $t -Force | Out-Null
Write-Output 'at-logon task registered'
"""
o,e = ps(task)
print(o)
if e: print(f"  task err: {e[:200]}")

# verify
o,_ = ps(r"Get-ItemProperty -Path '" + reg + r"' -Name AutoAdminLogon,DefaultUserName | Select-Object AutoAdminLogon,DefaultUserName | Format-List | Out-String")
print(o)
print("\nDONE. Reboot required to take effect.")
