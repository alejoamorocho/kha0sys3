"""Verify only ONE AMO8 bot instance is running and not duplicated.

Checks:
  1. NSSM services with "Amo" or "A8" in the name
  2. Python processes running scripts containing amo / a8
  3. Open positions / pending orders on magic 8338 (per comment prefix)
  4. Magic numbers in current bot_config files
"""
import subprocess
import MetaTrader5 as mt5
from collections import Counter

# 1. Services
print("=== 1. NSSM/Windows services with 'amo'/'a8'/'kha0sys' in name ===")
try:
    r = subprocess.run(
        ["powershell", "-Command",
         "Get-Service | Where-Object { $_.Name -match 'kha0sys|amo|a8' } | Format-Table Name,Status,StartType -AutoSize | Out-String"],
        capture_output=True, text=True, timeout=30,
    )
    print(r.stdout)
except Exception as e:
    print(f"  error: {e}")

# 2. Python processes
print("=== 2. Python processes (any 'amo'/'a8'/'kha0sys' in cmdline) ===")
try:
    r = subprocess.run(
        ["powershell", "-Command",
         "Get-WmiObject Win32_Process -Filter \"Name = 'python.exe'\" | "
         "Where-Object { $_.CommandLine -match 'amo|a8|kha0sys' } | "
         "Select-Object ProcessId,CommandLine | Format-List | Out-String"],
        capture_output=True, text=True, timeout=30,
    )
    print(r.stdout if r.stdout.strip() else "  (none found)")
except Exception as e:
    print(f"  error: {e}")

# 3. MT5 positions + orders for magic 8338 with prefix counts
print("=== 3. MT5 magic=8338 open positions + pending orders (by comment prefix) ===")
mt5.initialize()
pos = mt5.positions_get() or []
ords = mt5.orders_get() or []
amo_pos = [p for p in pos if int(getattr(p, "magic", 0)) == 8338]
amo_ord = [o for o in ords if int(getattr(o, "magic", 0)) == 8338]
print(f"  open positions magic=8338: {len(amo_pos)}")
print(f"  pending orders  magic=8338: {len(amo_ord)}")
prefix_pos = Counter()
prefix_ord = Counter()
for p in amo_pos:
    com = (getattr(p, "comment", "") or "")
    prefix_pos[com.split("|")[0] if com else "(empty)"] += 1
    print(f"    POS ticket={p.ticket}  sym={p.symbol}  vol={p.volume}  comment='{com}'  open_time={p.time}")
for o in amo_ord:
    com = (getattr(o, "comment", "") or "")
    prefix_ord[com.split("|")[0] if com else "(empty)"] += 1
    print(f"    ORD ticket={o.ticket}  sym={o.symbol}  vol={o.volume_current}  comment='{com}'")
if amo_pos:
    print(f"  open-position prefix counts: {dict(prefix_pos)}")
if amo_ord:
    print(f"  pending-order prefix counts: {dict(prefix_ord)}")

mt5.shutdown()

# 4. Configs
print()
print("=== 4. Bot config files in repo (magic numbers used) ===")
import json
from pathlib import Path
for f in sorted(Path("src/execution").glob("bot_config_*.json")):
    try:
        c = json.loads(f.read_text())
        mg = c.get("magic_number") or c.get("magic")
        n = len(c.get("portfolio", []))
        print(f"  {f.name:<45}  magic={mg}  strategies={n}")
    except Exception:
        pass
