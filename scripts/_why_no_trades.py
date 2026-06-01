"""Diagnose why no trades are firing on the VPS right now.

Checks for each bot:
  - service running + process alive
  - last log line + timestamp (is bot still ticking?)
  - any unhandled errors recently
  - broker offset detected correctly
  - current open positions + pending orders per magic
  - recent trade activity (last 24h)
"""
import MetaTrader5 as mt5
import subprocess
import time as _t
from datetime import datetime, timezone, timedelta
from collections import Counter

# ─── 1. Services + processes ──────────────────────────────────────────
print("="*80)
print("1) SERVICES + PROCESSES")
print("="*80)
r = subprocess.run(
    ["powershell", "-Command",
     "Get-Service Kha0sysAmo8,Kha0sysMathBot,Kha0sysTradersBot,Kha0sysWatchdog3 -ErrorAction SilentlyContinue | Format-Table Name,Status,StartType -AutoSize | Out-String"],
    capture_output=True, text=True, timeout=30,
)
print(r.stdout)

# Python processes
r = subprocess.run(
    ["powershell", "-Command",
     "Get-WmiObject Win32_Process -Filter \"Name = 'python.exe'\" | "
     "Where-Object { $_.CommandLine -match 'amo|kha0sys|math|trader' } | "
     "Select-Object ProcessId,CreationDate,@{Name='WorkingSet_MB';Expression={[math]::Round($_.WorkingSetSize/1MB,1)}},CommandLine | "
     "Format-Table -AutoSize | Out-String"],
    capture_output=True, text=True, timeout=30,
)
print(r.stdout)

# ─── 2. Log freshness check ───────────────────────────────────────────
print("="*80)
print("2) LOG FRESHNESS (when was last write?)")
print("="*80)
logs = [
    (r"C:\ProgramData\Kha0sysAmo8\logs\amo8.log", "AMO8"),
    (r"C:\ProgramData\Kha0sysMath\logs\math_bot.log", "MATH"),
    (r"C:\ProgramData\Kha0sysTraders\logs\traders_bot.log", "TRADERS"),
]
for path, label in logs:
    r = subprocess.run(
        ["powershell", "-Command",
         f"Get-Item '{path}' -ErrorAction SilentlyContinue | Select-Object @{{Name='LastWrite';Expression={{$_.LastWriteTime}}}},@{{Name='SizeKB';Expression={{[math]::Round($_.Length/1KB,1)}}}} | Format-List | Out-String"],
        capture_output=True, text=True, timeout=20,
    )
    print(f"--- {label} ---")
    print(r.stdout.strip())
    print()

# ─── 3. Recent errors/non-heartbeat lines per bot ─────────────────────
print("="*80)
print("3) RECENT NON-HEARTBEAT LINES PER BOT")
print("="*80)
for path, label in logs:
    print(f"\n--- {label} (last 25 actionable lines) ---")
    r = subprocess.run(
        ["powershell", "-Command",
         f"Get-Content '{path}' -Tail 200 -ErrorAction SilentlyContinue | "
         f"Where-Object {{ ($_ -notmatch 'HEARTBEAT|balance:|equity:|magic:|active slots|open positions') -and ($_ -match '\\[' -or $_ -match 'error|fail|trace|ENGINE|MT5|ORDER|PLACED|connect|reject|tick|stale|skip|fired|broker_offset|setup|signal') }} | "
         f"Select-Object -Last 25 | Out-String"],
        capture_output=True, text=True, timeout=20,
    )
    print(r.stdout.strip())

# ─── 4. MT5 live state ─────────────────────────────────────────────────
print()
print("="*80)
print("4) MT5 LIVE STATE")
print("="*80)
mt5.initialize()
print(f"Connected: {mt5.terminal_info()}")
acc = mt5.account_info()
if acc:
    print(f"Account: login={acc.login}  balance=${acc.balance:.2f}  equity=${acc.equity:.2f}  margin_free=${acc.margin_free:.2f}")
    print(f"  Trade allowed: {acc.trade_allowed}  Trade expert: {acc.trade_expert}")

now_real = int(_t.time())
deltas = []
for s in ("EURUSD+","XAUUSD+","GBPUSD+","XAGUSD","NG-C","USOUSD","NAS100","UKOUSD"):
    t = mt5.symbol_info_tick(s)
    if t and int(t.time) > 0:
        d = int(t.time) - now_real
        deltas.append(d)
        print(f"  tick {s:<10} delta={d:+d}s = {d/3600:+.2f}h  bid={t.bid:.5f}  ask={t.ask:.5f}")
median_delta = sorted(deltas)[len(deltas)//2] if deltas else 0
print(f"\n  Median broker offset: {median_delta/3600:+.2f}h (should be +3h EEST)")

# Open positions + pending orders by magic
print()
positions = mt5.positions_get() or []
orders = mt5.orders_get() or []
mc = Counter(int(getattr(p,"magic",0)) for p in positions)
mo = Counter(int(getattr(o,"magic",0)) for o in orders)
MAGICS = {1338:"MATH", 1339:"SWING", 1340:"ORB", 8338:"AMO8"}
print(f"OPEN POSITIONS by magic: {dict(mc)}")
print(f"PENDING ORDERS  by magic: {dict(mo)}")
for mg, name in MAGICS.items():
    pos_n = mc.get(mg, 0); ord_n = mo.get(mg, 0)
    if pos_n or ord_n:
        print(f"  {name} ({mg}): {pos_n} positions, {ord_n} pending orders")
        for p in positions:
            if int(getattr(p,"magic",0)) == mg:
                print(f"    POS {p.symbol} vol={p.volume} sl={p.sl} tp={p.tp} comment='{p.comment}'")
        for o in orders:
            if int(getattr(o,"magic",0)) == mg:
                print(f"    ORD {o.symbol} vol={o.volume_current} price={o.price_open} comment='{o.comment}'")

# ─── 5. Trades last 24h ────────────────────────────────────────────────
print()
print("="*80)
print("5) TRADES LAST 24h")
print("="*80)
to = datetime.now(timezone.utc)
frm = to - timedelta(hours=24)
frm_b = frm + timedelta(hours=3); to_b = to + timedelta(hours=3)
deals = mt5.history_deals_get(frm_b, to_b) or []
print(f"Total deals last 24h: {len(deals)}")
by_magic = Counter(int(getattr(d, "magic", 0)) for d in deals if d.entry == 0)
for mg, name in MAGICS.items():
    print(f"  {name} ({mg}): {by_magic.get(mg, 0)} entries")

# ─── 6. Current UTC time + active schedule ────────────────────────────
print()
print("="*80)
print("6) TIME + EXPECTED ACTIVE WINDOWS")
print("="*80)
now_utc = datetime.now(timezone.utc)
print(f"Now UTC: {now_utc.strftime('%Y-%m-%d %H:%M:%S')}  ({now_utc.strftime('%A')})")
print(f"  AMO8 windows: 00:00 (Tokyo), 07:00 (London), 12:30 (NY pre-cash)")
print(f"  ORB windows: 07:30 (London for GBPAUD/GBPJPY), 13:30 (NY for NAS100)")
hour_min = now_utc.hour + now_utc.minute/60
in_amo_win = any(
    abs((h*60+m) - (now_utc.hour*60+now_utc.minute)) < 60 + 8*60  # within OR_close + 8h
    for h,m in [(0,0),(7,0),(12,30)]
)
print(f"  Currently in any AMO8 active window? {in_amo_win}")
print(f"  Is weekend? {now_utc.weekday() in (5,6)}")

mt5.shutdown()
