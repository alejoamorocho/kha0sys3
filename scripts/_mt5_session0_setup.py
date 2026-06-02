"""Definitive fix: run MT5 in Session 0 (same as the NSSM bot services) with
AutoTrading enabled via common.ini, so the bots connect to a terminal that
has trading allowed.

The previous problem: user enabled AutoTrading in the Session 2 (RDP) terminal,
but the bots run as services in Session 0 and connect to a DIFFERENT terminal
instance there (with AutoTrading OFF), hence retcode 10027.

Steps:
  1. Stop bot services
  2. Kill ALL terminal64 (both sessions)
  3. Patch common.ini [Experts] Enabled=1
  4. Restart bot services -> MathBot's mt5.initialize(login=) launches a
     terminal in Session 0. With Enabled=1, AutoTrading button starts ON.
  5. Verify trade_allowed from Session 0 (where bots live) -> should be True
"""
import subprocess, time, os

def ps(cmd, timeout=90):
    r = subprocess.run(["powershell","-Command",cmd], capture_output=True, text=True, timeout=timeout)
    return r.stdout.strip(), r.stderr.strip()

DATA = r"C:\Users\Administrator\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075"
ini = os.path.join(DATA, "config", "common.ini")
SERVICES = ["Kha0sysMathBot","Kha0sysTradersBot","Kha0sysAmo8"]

print("=== Step 1: stop bot services ===")
for s in SERVICES:
    out,_ = ps(f"Stop-Service '{s}' -Force -ErrorAction SilentlyContinue; (Get-Service '{s}').Status")
    print(f"  {s}: {out}")
time.sleep(3)

print("\n=== Step 2: kill ALL terminal64 ===")
out,_ = ps("Get-Process terminal64 -ErrorAction SilentlyContinue | Stop-Process -Force; Start-Sleep -Seconds 3; (Get-Process terminal64 -ErrorAction SilentlyContinue | Measure-Object).Count")
print(f"  remaining: {out}")

print("\n=== Step 3: patch common.ini Enabled=1 ===")
raw = open(ini,"rb").read()
bom = raw[:2]
enc = "utf-16-le" if bom==b"\xff\xfe" else "utf-8"
text = raw.decode(enc).lstrip("﻿")
lines, in_exp, patched = [], False, False
for line in text.splitlines():
    s = line.strip()
    if s.startswith("["): in_exp = (s.lower()=="[experts]")
    if in_exp and s.startswith("Enabled="):
        lines.append("Enabled=1"); patched=True
        print(f"  {s} -> Enabled=1")
    else:
        lines.append(line)
if patched:
    open(ini,"wb").write(bom + ("\r\n".join(lines)+"\r\n").encode(enc))
    print("  written")
else:
    print("  WARNING: Enabled= not found in [Experts]")

print("\n=== Step 4: restart bot services (MathBot launches terminal in Session 0) ===")
for s in SERVICES:
    out,_ = ps(f"Start-Service '{s}'; Start-Sleep -Seconds 2; (Get-Service '{s}').Status")
    print(f"  {s}: {out}")

print("\n=== Step 5: wait + verify terminal session + trade_allowed ===")
for i in range(12):
    time.sleep(5)
    out,_ = ps(r"Get-CimInstance Win32_Process -Filter \"Name='terminal64.exe'\" | Select-Object ProcessId,SessionId | Format-Table -AutoSize -HideTableHeaders | Out-String")
    print(f"  [{i+1}/12] terminal64: {out.strip().replace(chr(10),' | ')}")
    # check trade_allowed via API from this (Session 0) context
    chk,_ = ps(r"""$py=@'
import MetaTrader5 as mt5
mt5.initialize()
ti=mt5.terminal_info()
print('trade_allowed=%s connected=%s' % (ti.trade_allowed if ti else '?', ti.connected if ti else '?'))
mt5.shutdown()
'@; $py | & C:\Python312\python.exe -""", timeout=40)
    print(f"          {chk}")
    if "trade_allowed=True" in chk:
        print("\n*** SUCCESS: AutoTrading ON in Session 0 terminal — bots can trade ***")
        break
