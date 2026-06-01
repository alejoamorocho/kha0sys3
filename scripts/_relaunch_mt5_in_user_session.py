"""Relaunch terminal64.exe in the Administrator's active RDP session.

The MT5 was launched at boot in Session 0 (services, headless), so no GUI is
accessible. Active interactive session is Session 2 (Administrator via RDP).

Uses 'schtasks /CREATE /RU Administrator /IT' trick: create a one-shot task
that runs interactively as Administrator, runs once, then deletes itself.

After relaunch:
  1. Stop bot services so they release the old terminal
  2. Kill terminal64 in Session 0
  3. Create + run scheduled task to start MT5 in Administrator session
  4. Wait for new terminal64 to come up
  5. Restart bot services (they re-attach to new terminal)
  6. User clicks AutoTrading button in their RDP session
  7. Verify trade_allowed=True
"""
import subprocess
import time
import os
import MetaTrader5 as mt5

SERVICES = ["Kha0sysMathBot", "Kha0sysTradersBot", "Kha0sysAmo8"]

def ps(cmd, timeout=60):
    r = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, timeout=timeout)
    return r.stdout.strip(), r.stderr.strip()

# Locate MT5 exe
mt5.initialize()
ti = mt5.terminal_info()
exe_path = os.path.join(ti.path, "terminal64.exe")
data_path = ti.data_path
mt5.shutdown()
print(f"MT5 exe: {exe_path}")

# Step 1: stop services
print("\n=== Step 1: stop bot services ===")
for s in SERVICES:
    out, _ = ps(f"Stop-Service '{s}' -Force -ErrorAction SilentlyContinue; (Get-Service '{s}').Status")
    print(f"  {s}: {out}")
time.sleep(3)

# Step 2: kill terminal64 in Session 0
print("\n=== Step 2: kill current terminal64 ===")
out, _ = ps("Get-Process terminal64 -ErrorAction SilentlyContinue | Stop-Process -Force; Start-Sleep -Seconds 2; (Get-Process terminal64 -ErrorAction SilentlyContinue | Measure-Object).Count")
print(f"  terminal64 processes left: {out}")

# Step 3: create scheduled task to launch MT5 in user session
print("\n=== Step 3: create scheduled task to launch in Administrator interactive session ===")
task_name = "Kha0sysMT5Launch"
# Delete any pre-existing version of the task
ps(f"schtasks /Delete /TN {task_name} /F 2>$null")

# Create task: runs as Administrator, in interactive logon session
# /RL HIGHEST = elevated  /IT = interactive (uses user's session)
# /SC ONCE /ST <past time> + /F = run immediately
create_cmd = f'schtasks /Create /TN {task_name} /TR "\\"{exe_path}\\"" /SC ONCE /ST 00:00 /RL HIGHEST /IT /RU Administrator /F'
out, err = ps(create_cmd)
print(f"  create: {out}")
if err:
    print(f"  err: {err[:300]}")

# Run the task immediately
print("\n=== Step 4: run task (launches MT5 in user session) ===")
out, err = ps(f"schtasks /Run /TN {task_name}")
print(f"  run: {out}")

# Wait + verify
print("\n=== Step 5: wait for new terminal64 + check session ===")
ok_session = False
for attempt in range(15):
    time.sleep(3)
    out, _ = ps(r"Get-CimInstance Win32_Process -Filter \"Name='terminal64.exe'\" | Select-Object ProcessId,SessionId | Format-Table -AutoSize -HideTableHeaders | Out-String")
    print(f"  [{attempt+1}/15] {out.strip()}")
    if "2" in out and "0" not in out.replace("terminal64",""):
        ok_session = True
        print("  Detected terminal64 in Session 2 (interactive)")
        break
    # also accept Session 1 (console)
    if " 1" in out and "terminal64" in out.lower() or True:
        # Just check by reading session ID
        for line in out.split("\n"):
            parts = line.strip().split()
            if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                sid = int(parts[1])
                if sid > 0:
                    ok_session = True
                    print(f"  Detected terminal64 in Session {sid} (interactive)")
                    break
        if ok_session:
            break

if not ok_session:
    print("  WARNING: could not confirm terminal64 in interactive session")

# Step 6: restart services
print("\n=== Step 6: restart bot services ===")
for s in SERVICES:
    out, _ = ps(f"Start-Service '{s}'; Start-Sleep -Seconds 2; (Get-Service '{s}').Status")
    print(f"  {s}: {out}")

# Clean up scheduled task
ps(f"schtasks /Delete /TN {task_name} /F")

# Final session report
print("\n=== Final state ===")
out, _ = ps("qwinsta")
print(out)
out, _ = ps(r"Get-CimInstance Win32_Process -Filter \"Name='terminal64.exe'\" | Select-Object ProcessId,SessionId,CommandLine | Format-List | Out-String")
print(out[:1000])

print()
print("="*70)
print("NEXT STEP FOR USER:")
print("  RDP into the VPS (Administrator). The MT5 window should now be")
print("  visible in your RDP session. Click the 'AutoTrading' button")
print("  (or press Ctrl+E) to toggle it green/ON.")
print("="*70)
