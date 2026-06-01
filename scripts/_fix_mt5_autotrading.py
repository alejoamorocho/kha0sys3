"""Enable MT5 AutoTrading by modifying common.ini and restarting terminal.

Sequenced carefully to avoid bot crashes:
  1. Stop the 3 trading bot services (they'll lose MT5 connection cleanly)
  2. Kill terminal64.exe
  3. Modify common.ini: [Experts] Enabled=0 → 1
  4. Relaunch terminal64.exe with /portable (preserves login)
  5. Wait up to 60s for MT5 to reconnect to broker
  6. Verify trade_allowed=True
  7. Restart the 3 trading bot services
"""
import subprocess
import time
import os
import sys
import MetaTrader5 as mt5
from pathlib import Path

def ps(cmd, timeout=30):
    r = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, timeout=timeout)
    return r.stdout.strip(), r.stderr.strip()

SERVICES = ["Kha0sysMathBot", "Kha0sysTradersBot", "Kha0sysAmo8"]

# Step 0: paths
mt5.initialize()
ti = mt5.terminal_info()
data_path = ti.data_path
exe_path = os.path.join(ti.path, "terminal64.exe")
mt5.shutdown()
common_ini = Path(data_path) / "config" / "common.ini"
print(f"common.ini: {common_ini}")

# Step 1: Stop bot services
print("\n=== Step 1: stop bot services ===")
for s in SERVICES:
    out, _ = ps(f"Stop-Service '{s}' -Force -ErrorAction SilentlyContinue; (Get-Service '{s}').Status")
    print(f"  {s}: {out}")

# Give them a moment to release MT5
time.sleep(3)

# Step 2: kill terminal64.exe
print("\n=== Step 2: kill terminal64.exe ===")
out, _ = ps("Stop-Process -Name terminal64 -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 2; (Get-Process terminal64 -ErrorAction SilentlyContinue | Measure-Object).Count")
print(f"  terminal64 processes left: {out}")

# Step 3: modify common.ini
print("\n=== Step 3: modify common.ini ===")
# Read with utf-16 (MT5 default)
raw = common_ini.read_bytes()
# Detect BOM
if raw[:2] == b"\xff\xfe":
    enc = "utf-16-le"
    bom = b"\xff\xfe"
elif raw[:2] == b"\xfe\xff":
    enc = "utf-16-be"
    bom = b"\xfe\xff"
else:
    enc = "utf-8"
    bom = b""

text = raw.decode(enc).lstrip("﻿")
# Patch [Experts] Enabled=0 → 1
new_text = []
in_experts = False
patched = False
for line in text.splitlines():
    stripped = line.strip()
    if stripped.startswith("["):
        in_experts = (stripped.lower() == "[experts]")
    if in_experts and stripped == "Enabled=0":
        new_text.append("Enabled=1")
        patched = True
        print(f"  PATCHED: [Experts] Enabled=0 -> Enabled=1")
    else:
        new_text.append(line)

if not patched:
    print(f"  WARNING: did not find [Experts] Enabled=0 — checking current state...")
    for i, line in enumerate(text.splitlines()):
        if "Enabled" in line and "Experts" in text.splitlines()[max(0,i-5):i][-1:][0] if i>0 else False:
            print(f"    line: {line}")

# Write back with same encoding + BOM
out_bytes = bom + ("\r\n".join(new_text) + "\r\n").encode(enc)
common_ini.write_bytes(out_bytes)
print(f"  wrote {len(out_bytes)} bytes to {common_ini}")

# Step 4: relaunch terminal64.exe
print("\n=== Step 4: relaunch terminal64.exe ===")
# Use Start-Process to avoid blocking
out, err = ps(f"Start-Process -FilePath '{exe_path}' -WindowStyle Hidden -PassThru | Select-Object -ExpandProperty Id")
print(f"  launched PID: {out}")

# Step 5: wait for MT5 to login + connect
print("\n=== Step 5: wait for MT5 to reconnect ===")
ok = False
for attempt in range(20):
    time.sleep(3)
    if not mt5.initialize():
        print(f"  [{attempt+1}/20] initialize() failed, retrying...")
        continue
    ti = mt5.terminal_info()
    ai = mt5.account_info()
    if ti and ai and ti.connected:
        print(f"  [{attempt+1}/20] connected={ti.connected}  login={ai.login}  trade_allowed_terminal={ti.trade_allowed}")
        if ti.trade_allowed:
            ok = True
            mt5.shutdown()
            break
    else:
        print(f"  [{attempt+1}/20] not ready yet")
    mt5.shutdown()

print()
if not ok:
    print("FAILED: MT5 did not enable trade_allowed within timeout.")
    print("        Restarting services anyway so they retry.")
else:
    print("SUCCESS: trade_allowed=True")

# Step 7: restart bot services
print("\n=== Step 7: restart bot services ===")
for s in SERVICES:
    out, _ = ps(f"Start-Service '{s}'; (Get-Service '{s}').Status")
    print(f"  {s}: {out}")

sys.exit(0 if ok else 1)
