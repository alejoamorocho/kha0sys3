"""Make MT5 AutoTrading state survive RDP disconnect.

Strategy:
  1. Kill the headless terminal64 (Session 0) — it interferes
  2. Move the disconnected RDP session to console session via tscon
     → console sessions don't go to 'Disconnected' state
  3. Verify MT5 in Session 1 (now console) keeps AutoTrading ON

If tscon trick works, the user can disconnect RDP without losing
AutoTrading. They can reconnect RDP later to take screenshots / interact.
"""
import subprocess
import time
import MetaTrader5 as mt5

def ps(cmd, timeout=60):
    r = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, timeout=timeout)
    return r.stdout.strip(), r.stderr.strip()

# Step 1: kill Session 0 terminal64 (the headless one)
print("=== Step 1: kill headless terminal64 (Session 0) ===")
out, _ = ps(r"""
$procs = Get-CimInstance Win32_Process -Filter "Name='terminal64.exe'"
foreach ($p in $procs) {
    if ($p.SessionId -eq 0) {
        Write-Output "  killing PID $($p.ProcessId) (Session 0)"
        Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue
    } else {
        Write-Output "  keeping PID $($p.ProcessId) (Session $($p.SessionId))"
    }
}
""")
print(out)
time.sleep(2)

# Step 2: list current sessions
print("\n=== Step 2: sessions before tscon ===")
out, _ = ps("qwinsta")
print(out)

# Find Administrator's session ID (the disconnected one)
admin_session_id = None
for line in out.splitlines():
    if "Administrator" in line:
        parts = line.split()
        # Format: SESSIONNAME USERNAME ID STATE TYPE DEVICE
        for p in parts:
            if p.isdigit():
                admin_session_id = int(p)
                break
        if admin_session_id is not None:
            break
print(f"Detected Administrator session ID: {admin_session_id}")

# Step 3: tscon to move the session to console (Session 1)
if admin_session_id and admin_session_id != 1:
    print(f"\n=== Step 3: tscon — move session {admin_session_id} to console (1) ===")
    # tscon requires SeTcbPrivilege; from elevated PowerShell it works
    out, err = ps(f"tscon {admin_session_id} /dest:console /password:''")
    if out: print(out)
    if err:
        print(f"tscon stderr: {err[:500]}")
        # Try without password
        out, err = ps(f"tscon {admin_session_id} /dest:console")
        if out: print(out)
        if err: print(f"retry stderr: {err[:500]}")
else:
    print(f"\n=== Step 3: session already console (1) or not found, skipping tscon ===")

time.sleep(3)

# Step 4: verify new session state
print("\n=== Step 4: sessions after tscon ===")
out, _ = ps("qwinsta")
print(out)

print("\n=== terminal64 processes ===")
out, _ = ps(r"Get-CimInstance Win32_Process -Filter \"Name='terminal64.exe'\" | Select-Object ProcessId,SessionId | Format-Table -AutoSize | Out-String")
print(out)

# Step 5: verify trade_allowed
print("\n=== Step 5: verify trade_allowed ===")
time.sleep(3)
for i in range(8):
    if mt5.initialize():
        ti = mt5.terminal_info()
        if ti:
            print(f"  [{i+1}/8] connected={ti.connected}  trade_allowed={ti.trade_allowed}")
            if ti.trade_allowed:
                mt5.shutdown()
                break
        mt5.shutdown()
    time.sleep(2)
