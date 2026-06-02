"""Configure Windows autologon + at-logon MT5/AutoTrading setup.

Robust version (2026-06-02): reads VPS_PASS from .env ON the VPS inside the
PowerShell call so the password never crosses the command line (avoids
escaping issues with special characters that previously left
DefaultPassword empty and AutoAdminLogon reset to 0).

After this + a reboot:
  - Windows auto-logs-in Administrator to an interactive console session
  - the KhaosysOnLogon scheduled task runs on_logon_setup.py which launches
    MT5, enables AutoTrading (Ctrl+E works because the logon session has
    real focus), and restarts the bot services.
"""
import subprocess, sys

def ps(cmd, timeout=60):
    r = subprocess.run(["powershell","-NoProfile","-Command",cmd], capture_output=True, text=True, timeout=timeout)
    return r.stdout.strip(), r.stderr.strip()

# 1. Autologon registry — read password from .env inside PowerShell
reg_cmd = r'''
$reg='HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon'
$pw = ((Get-Content C:\Proyectos\kha0sys3\.env | Where-Object { $_ -match '^VPS_PASS=' }) -replace '^VPS_PASS=','').Trim()
if (-not $pw) { Write-Output 'ERROR: VPS_PASS empty'; exit 1 }
Set-ItemProperty -Path $reg -Name DefaultPassword   -Value $pw -Type String
Set-ItemProperty -Path $reg -Name AutoAdminLogon    -Value '1' -Type String
Set-ItemProperty -Path $reg -Name DefaultUserName   -Value 'Administrator' -Type String
Set-ItemProperty -Path $reg -Name DefaultDomainName -Value $env:COMPUTERNAME -Type String
Set-ItemProperty -Path $reg -Name DisableCAD        -Value 1 -Type DWord
$c = Get-ItemProperty -Path $reg
Write-Output "AutoAdminLogon=$($c.AutoAdminLogon) User=$($c.DefaultUserName) Domain=$($c.DefaultDomainName) PwLen=$($c.DefaultPassword.Length)"
'''
o,e = ps(reg_cmd)
print("registry:", o)
if e: print("  warn:", e[:200])

# 2. At-logon scheduled task
task_cmd = r'''
$task='KhaosysOnLogon'
Unregister-ScheduledTask -TaskName $task -Confirm:$false -ErrorAction SilentlyContinue
$action=New-ScheduledTaskAction -Execute 'C:\Python312\python.exe' -Argument 'C:\Proyectos\kha0sys3\scripts\on_logon_setup.py'
$trigger=New-ScheduledTaskTrigger -AtLogOn -User Administrator
$principal=New-ScheduledTaskPrincipal -UserId Administrator -LogonType Interactive -RunLevel Highest
$settings=New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Minutes 10)
$t=New-ScheduledTask -Action $action -Trigger $trigger -Principal $principal -Settings $settings
Register-ScheduledTask -TaskName $task -InputObject $t -Force | Out-Null
Write-Output 'at-logon task registered'
'''
o,e = ps(task_cmd)
print(o)
if e: print("  task warn:", e[:200])
print("DONE. Reboot to take effect.")
