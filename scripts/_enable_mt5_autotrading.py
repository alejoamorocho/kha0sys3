"""Enable MT5 AutoTrading without GUI access.

Strategy ladder (least → most disruptive):
  1. Send Ctrl+E keystroke to the MT5 terminal window (toggles AutoTrading
     button). Works headless — no visible RDP needed.
  2. If MT5 window not found, modify config file experts.ini /
     common.ini and restart the MT5 terminal process.
  3. Report failure if neither works.
"""
import subprocess
import time
import os
import sys

print("=== Step 1: locate MT5 terminal process + window ===")
# Get MT5 process
r = subprocess.run(
    ["powershell", "-Command",
     "Get-Process terminal64,terminal -ErrorAction SilentlyContinue | Select-Object Id,ProcessName,MainWindowTitle,MainWindowHandle | Format-Table -AutoSize | Out-String"],
    capture_output=True, text=True, timeout=20,
)
print(r.stdout)

print("=== Step 2: send Ctrl+E to MT5 window (toggles AutoTrading) ===")
# Use AppActivate + SendKeys (Ctrl+E is the AutoTrading toggle shortcut)
ps_script = r"""
Add-Type -AssemblyName System.Windows.Forms
$wshell = New-Object -ComObject wscript.shell

# Try by process name
$proc = Get-Process terminal64 -ErrorAction SilentlyContinue
if (-not $proc) { $proc = Get-Process terminal -ErrorAction SilentlyContinue }

if ($proc) {
    $title = $proc[0].MainWindowTitle
    Write-Output "Found MT5 process: PID=$($proc[0].Id) Title='$title'"
    if ($title) {
        $activated = $wshell.AppActivate($title)
        Write-Output "AppActivate returned: $activated"
        Start-Sleep -Milliseconds 500
        # Ctrl+E is the standard MT5 AutoTrading toggle shortcut
        [System.Windows.Forms.SendKeys]::SendWait("^e")
        Write-Output "Sent Ctrl+E"
        Start-Sleep -Milliseconds 1000
    } else {
        Write-Output "ERROR: MT5 window title is empty (window not visible/no UI session)"
    }
} else {
    Write-Output "ERROR: terminal64.exe not running"
}
"""
r = subprocess.run(
    ["powershell", "-Command", ps_script],
    capture_output=True, text=True, timeout=30,
)
print(r.stdout)
if r.stderr.strip():
    print("STDERR:", r.stderr.strip()[:500])

print()
print("=== Step 3: verify trade_allowed flipped ===")
time.sleep(2)
import MetaTrader5 as mt5
mt5.initialize()
ti = mt5.terminal_info()
print(f"  trade_allowed (terminal): {ti.trade_allowed}")
mt5.shutdown()

if ti.trade_allowed:
    print("\nSUCCESS: AutoTrading is now ON")
    sys.exit(0)
else:
    print("\nStep 1 did not work (likely no GUI session active). Trying config-file approach...")

# ─── Fallback: modify experts.ini and restart MT5 ─────────────────────
print()
print("=== Step 4: locate MT5 config files ===")
import MetaTrader5 as mt5
mt5.initialize()
ti = mt5.terminal_info()
data_path = ti.data_path
mt5.shutdown()
print(f"  MT5 data_path: {data_path}")

import glob
config_dir = os.path.join(data_path, "config")
candidates = []
for name in ("experts.ini", "common.ini", "terminal.ini"):
    p = os.path.join(config_dir, name)
    if os.path.exists(p):
        candidates.append(p)
        print(f"  found: {p}  ({os.path.getsize(p)} bytes)")

# Print current relevant settings without exposing the whole file
for path in candidates:
    try:
        with open(path, "r", encoding="utf-16", errors="ignore") as f:
            content = f.read()
    except UnicodeError:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    rel_lines = [l for l in content.splitlines()
                 if any(k in l for k in ("Expert", "AutoTrading", "Algo", "AllowLive"))]
    if rel_lines:
        print(f"\n  Relevant lines in {os.path.basename(path)}:")
        for l in rel_lines[:10]:
            print(f"    {l}")
