"""Enable MT5 AutoTrading by modifying config files + restarting terminal.

Plan:
  1. Dump current relevant content of common.ini + terminal.ini
  2. Find the AutoTrading / Expert Advisors enable flag
  3. Modify it to enabled
  4. Kill + relaunch terminal64.exe (with same args as before)
  5. Verify trade_allowed=True
"""
import subprocess
import time
import os
import sys
import MetaTrader5 as mt5

# Locate paths
mt5.initialize()
ti = mt5.terminal_info()
data_path = ti.data_path
exe_path = os.path.join(ti.path, "terminal64.exe")
mt5.shutdown()
print(f"data_path: {data_path}")
print(f"exe_path:  {exe_path}")
print(f"exe exists: {os.path.exists(exe_path)}")

common_ini = os.path.join(data_path, "config", "common.ini")
terminal_ini = os.path.join(data_path, "config", "terminal.ini")

def read_ini(path):
    """Try utf-16 first (MT5 default), fall back to utf-8."""
    for enc in ("utf-16", "utf-16-le", "utf-8"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read(), enc
        except (UnicodeError, UnicodeDecodeError):
            continue
    with open(path, "r", encoding="latin-1") as f:
        return f.read(), "latin-1"

print()
print("=== common.ini RAW (relevant sections) ===")
content, enc = read_ini(common_ini)
print(f"(encoding: {enc})")
in_experts = False
for line in content.splitlines():
    stripped = line.strip()
    if stripped.startswith("["):
        in_experts = "expert" in stripped.lower() or "trade" in stripped.lower()
    if in_experts or any(k in stripped for k in ("Expert","Trad","Allow","Algo","Enable")):
        print(f"  {line}")

print()
print("=== terminal.ini RAW (relevant sections) ===")
content2, enc2 = read_ini(terminal_ini)
print(f"(encoding: {enc2})")
in_relevant = False
for line in content2.splitlines():
    stripped = line.strip()
    if stripped.startswith("["):
        in_relevant = any(k in stripped.lower() for k in ("expert","trad","common","algo"))
    if in_relevant or any(k in stripped for k in ("Expert","Trad","Allow","Algo","Enable","Last")):
        print(f"  {line}")
