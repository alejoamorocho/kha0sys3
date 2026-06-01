"""Kill the headless terminal64 (Session 0) and send Ctrl+E to the
interactive one (Session 2) to toggle AutoTrading.
"""
import subprocess
import time
import os
import MetaTrader5 as mt5

def ps(cmd, timeout=60):
    r = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, timeout=timeout)
    return r.stdout.strip(), r.stderr.strip()

# Step 1: identify terminal64 by session
print("=== Terminal64 processes by session ===")
out, _ = ps(r"Get-CimInstance Win32_Process -Filter \"Name='terminal64.exe'\" | Select-Object ProcessId,SessionId | Format-Table -AutoSize | Out-String")
print(out)

# Kill Session 0 ones, keep Session > 0
out, _ = ps(r"""
$procs = Get-CimInstance Win32_Process -Filter "Name='terminal64.exe'"
foreach ($p in $procs) {
    if ($p.SessionId -eq 0) {
        Write-Output "Killing terminal64 PID $($p.ProcessId) in Session 0"
        Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue
    } else {
        Write-Output "Keeping terminal64 PID $($p.ProcessId) in Session $($p.SessionId)"
    }
}
""")
print(out)
time.sleep(3)

# Step 2: find the interactive terminal64 and its window
print("\n=== Find interactive terminal64 window ===")
out, _ = ps(r"""
Add-Type @'
using System;
using System.Runtime.InteropServices;
using System.Collections.Generic;
public class W {
    [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr hWnd);
    [DllImport("user32.dll", EntryPoint="EnumWindows")] public static extern bool EnumWindows(EnumProc lpEnumFunc, IntPtr lParam);
    [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint lpdwProcessId);
    [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetClassName(IntPtr hWnd, System.Text.StringBuilder lpClassName, int nMaxCount);
    [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder lpString, int nMaxCount);
    public delegate bool EnumProc(IntPtr hWnd, IntPtr lParam);
}
'@
$pids = (Get-Process terminal64 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id)
Write-Output "terminal64 PIDs: $($pids -join ',')"
$callback = [W+EnumProc] {
    param($h, $l)
    $procId = 0
    [W]::GetWindowThreadProcessId($h, [ref]$procId) | Out-Null
    if ($script:pids -contains [int]$procId) {
        $cls = New-Object System.Text.StringBuilder 256
        [W]::GetClassName($h, $cls, 256) | Out-Null
        $title = New-Object System.Text.StringBuilder 512
        [W]::GetWindowText($h, $title, 512) | Out-Null
        if ($title.ToString() -or $cls.ToString()) {
            Write-Output "  hwnd=$h pid=$procId class='$($cls.ToString())' title='$($title.ToString())'"
        }
    }
    return $true
}
[W]::EnumWindows($callback, [IntPtr]::Zero) | Out-Null
""")
print(out[:3000])

# Step 3: send Ctrl+E via SendKeys to the active interactive session
print("\n=== Send Ctrl+E to MT5 via SendKeys (requires active session) ===")
out, _ = ps(r"""
Add-Type -AssemblyName System.Windows.Forms
$wshell = New-Object -ComObject wscript.shell
# Try to find MT5 by window title
$mt5 = Get-Process terminal64 -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle }
if ($mt5) {
    Write-Output "MT5 title: '$($mt5.MainWindowTitle)' PID $($mt5.Id)"
    $activated = $wshell.AppActivate($mt5.Id)
    Write-Output "AppActivate(PID=$($mt5.Id)) -> $activated"
    Start-Sleep -Milliseconds 800
    [System.Windows.Forms.SendKeys]::SendWait('^e')
    Write-Output "Sent Ctrl+E"
    Start-Sleep -Milliseconds 1500
} else {
    Write-Output "No MT5 with MainWindowTitle found (window not visible to this session)"
}
""")
print(out)

# Verify
time.sleep(3)
print("\n=== Verify trade_allowed ===")
for i in range(10):
    if mt5.initialize():
        ti = mt5.terminal_info()
        if ti:
            print(f"  [{i+1}/10] connected={ti.connected}  trade_allowed={ti.trade_allowed}")
            if ti.trade_allowed:
                mt5.shutdown()
                print("\n*** SUCCESS: AutoTrading is ON ***")
                break
        mt5.shutdown()
    time.sleep(2)
