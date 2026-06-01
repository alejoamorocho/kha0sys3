"""Try alternative methods to enable MT5 AutoTrading runtime toggle.

Approaches:
  A) Registry inspection - check HKCU MetaQuotes for autotrading flag
  B) Inspect ALL .ini and .set files in MT5 data_path for "Enable" flags
  C) Try Win32 SendMessage to MT5 window (works even on minimized windows)
  D) Try Ctrl+E via Win32 PostMessage to terminal64 process
"""
import subprocess
import os
import sys
import MetaTrader5 as mt5

def ps(cmd, timeout=60):
    r = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, timeout=timeout)
    return r.stdout.strip(), r.stderr.strip()

mt5.initialize()
ti = mt5.terminal_info()
data_path = ti.data_path
mt5.shutdown()

# ─── A: Registry ──────────────────────────────────────────────────────
print("=== A: Registry search HKCU\\Software\\MetaQuotes ===")
out, _ = ps(r"""
$root = 'HKCU:\Software\MetaQuotes Software Corp'
if (Test-Path $root) {
    Get-ChildItem -Path $root -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
        $items = Get-ItemProperty -Path $_.PSPath -ErrorAction SilentlyContinue
        $items.PSObject.Properties | Where-Object { $_.Name -match 'Expert|Trade|Algo|AutoTrad|Allow|Enabled' } | ForEach-Object {
            "$($_.Name) = $($_.Value)  at $($items.PSPath -replace '.+::','')"
        }
    } | Select-Object -First 40
} else { Write-Output 'no HKCU MetaQuotes key' }
""")
print(out[:3000])

# ─── B: All .ini files ────────────────────────────────────────────────
print("\n=== B: Scan all .ini/.set files for Enable/Expert flags ===")
out, _ = ps(f"""
Get-ChildItem -Path '{data_path}' -Recurse -Include *.ini,*.set -ErrorAction SilentlyContinue | ForEach-Object {{
    $f = $_.FullName
    try {{
        $content = Get-Content $f -Raw -Encoding Unicode -ErrorAction Stop
    }} catch {{
        $content = Get-Content $f -Raw -ErrorAction SilentlyContinue
    }}
    if ($content -match 'Enabled=|AllowLive|AllowAlgo') {{
        Write-Output "FILE: $f"
        $content -split "`n" | Where-Object {{ $_ -match 'Enabled=|AllowLive|AllowAlgo|Expert' }} | Select-Object -First 8 | ForEach-Object {{ Write-Output "  $($_.Trim())" }}
    }}
}}
""")
print(out[:4000])

# ─── C: PostMessage Ctrl+E to terminal window ─────────────────────────
print("\n=== C: PostMessage WM_KEYDOWN Ctrl+E to terminal64 ===")
out, _ = ps(r"""
Add-Type @"
using System;
using System.Runtime.InteropServices;
using System.Diagnostics;
public class W {
    [DllImport("user32.dll")] public static extern bool PostMessage(IntPtr hWnd, uint Msg, IntPtr wParam, IntPtr lParam);
    [DllImport("user32.dll")] public static extern IntPtr FindWindow(string lpClassName, string lpWindowName);
    [DllImport("user32.dll", EntryPoint="EnumWindows")] public static extern bool EnumWindows(EnumProc lpEnumFunc, IntPtr lParam);
    [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint lpdwProcessId);
    [DllImport("user32.dll")] public static extern int GetClassName(IntPtr hWnd, System.Text.StringBuilder lpClassName, int nMaxCount);
    public delegate bool EnumProc(IntPtr hWnd, IntPtr lParam);
}
"@
$mt5_pid = (Get-Process terminal64 -ErrorAction SilentlyContinue).Id
Write-Output "MT5 PID: $mt5_pid"
# Find all top-level windows belonging to MT5 PID
$windows = @()
$callback = [W+EnumProc] {
    param($h, $l)
    $procId = 0
    [W]::GetWindowThreadProcessId($h, [ref]$procId) | Out-Null
    if ($procId -eq $mt5_pid) {
        $sb = New-Object System.Text.StringBuilder 256
        [W]::GetClassName($h, $sb, 256) | Out-Null
        $script:windows += @{hwnd=$h; class=$sb.ToString()}
    }
    return $true
}
[W]::EnumWindows($callback, [IntPtr]::Zero) | Out-Null
Write-Output "Windows under MT5 PID: $($windows.Count)"
foreach ($w in $windows) {
    Write-Output "  hwnd=$($w.hwnd)  class='$($w.class)'"
}
# Try posting Ctrl+E to the main window (MetaQuotes::MetaTrader main class)
$mainWin = $windows | Where-Object { $_.class -match 'MetaQuotes|MetaTrader' } | Select-Object -First 1
if ($mainWin) {
    $WM_KEYDOWN = 0x0100
    $WM_KEYUP = 0x0101
    $VK_CONTROL = 0x11
    $VK_E = 0x45
    [W]::PostMessage($mainWin.hwnd, $WM_KEYDOWN, [IntPtr]$VK_CONTROL, [IntPtr]0) | Out-Null
    [W]::PostMessage($mainWin.hwnd, $WM_KEYDOWN, [IntPtr]$VK_E, [IntPtr]0) | Out-Null
    Start-Sleep -Milliseconds 100
    [W]::PostMessage($mainWin.hwnd, $WM_KEYUP, [IntPtr]$VK_E, [IntPtr]0) | Out-Null
    [W]::PostMessage($mainWin.hwnd, $WM_KEYUP, [IntPtr]$VK_CONTROL, [IntPtr]0) | Out-Null
    Write-Output "Sent Ctrl+E to hwnd=$($mainWin.hwnd) class='$($mainWin.class)'"
}
""")
print(out[:2500])

# Verify
import time
time.sleep(3)
mt5.initialize()
ti = mt5.terminal_info()
print(f"\nAFTER ATTEMPTS — trade_allowed (terminal): {ti.trade_allowed}")
mt5.shutdown()
