"""Runs automatically at Administrator logon (via scheduled task).

Because autologon creates a REAL interactive desktop session with focus,
SetForegroundWindow + Ctrl+E work reliably here (unlike WinRM Session 0).

Sequence:
  1. Wait for desktop to settle
  2. Ensure exactly ONE MT5 terminal is running in this session
  3. Wait for broker login
  4. Enable AutoTrading via Ctrl+E (focus works in logon session)
  5. Restart bot services so they attach to this terminal
  6. Log everything to C:\ProgramData\Kha0sysMath\logs\on_logon.log
"""
import time, os, subprocess, ctypes, sys
from datetime import datetime

LOG = r"C:\ProgramData\Kha0sysMath\logs\on_logon.log"
os.makedirs(os.path.dirname(LOG), exist_ok=True)
def log(m):
    line = f"{datetime.now().isoformat()} {m}"
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")

EXE = r"C:\Program Files\MetaTrader 5\terminal64.exe"
DATA = r"C:\Users\Administrator\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075"
INI = os.path.join(DATA, "config", "common.ini")

log("=== on_logon_setup START ===")
time.sleep(20)  # let desktop settle

# 1. common.ini Enabled=1
try:
    raw = open(INI,"rb").read()
    bom = raw[:2]; enc = "utf-16-le" if bom==b"\xff\xfe" else "utf-8"
    text = raw.decode(enc).lstrip("﻿")
    out, in_exp = [], False
    for ln in text.splitlines():
        s = ln.strip()
        if s.startswith("["): in_exp = (s.lower()=="[experts]")
        out.append("Enabled=1" if (in_exp and s.startswith("Enabled=")) else ln)
    open(INI,"wb").write(bom + ("\r\n".join(out)+"\r\n").encode(enc))
    log("common.ini Enabled=1 set")
except Exception as e:
    log(f"common.ini patch error: {e}")

# 2. Ensure ONE terminal in this session
def terminals():
    r = subprocess.run(["powershell","-NoProfile","-Command",
        "Get-CimInstance Win32_Process -Filter \"Name='terminal64.exe'\" | ForEach-Object { \"$($_.ProcessId):$($_.SessionId)\" }"],
        capture_output=True, text=True)
    return [p for p in r.stdout.split() if ":" in p]

my_sid = subprocess.run(["powershell","-NoProfile","-Command",
    "(Get-Process -Id $PID).SessionId"], capture_output=True, text=True).stdout.strip()
log(f"my session id = {my_sid}")

procs = terminals()
log(f"terminals at start: {procs}")
# kill terminals NOT in my session
for p in procs:
    pid, sid = p.split(":")
    if sid != my_sid:
        subprocess.run(["powershell","-NoProfile","-Command",f"Stop-Process -Id {pid} -Force -ErrorAction SilentlyContinue"])
        log(f"killed terminal {pid} (session {sid})")
time.sleep(2)
procs = terminals()
if not any(p.split(":")[1]==my_sid for p in procs):
    log("launching MT5 in this session")
    subprocess.Popen([EXE])
    for i in range(15):
        time.sleep(4)
        if any(p.split(":")[1]==my_sid for p in terminals()):
            log(f"terminal up after {(i+1)*4}s"); break
    time.sleep(20)  # broker login

# 3. Enable AutoTrading via Ctrl+E
def check_trade_allowed():
    try:
        import MetaTrader5 as mt5
        mt5.initialize()
        ti = mt5.terminal_info()
        v = bool(ti.trade_allowed) if ti else None
        mt5.shutdown()
        return v
    except Exception as e:
        log(f"  api err {e}"); return None

user32 = ctypes.windll.user32
def find_mt5():
    hwnds=[]
    def cb(h,l):
        cls=ctypes.create_unicode_buffer(256); user32.GetClassNameW(h,cls,256)
        if "MetaQuotes::MetaTrader" in cls.value and user32.IsWindowVisible(h): hwnds.append(h)
        return True
    EP=ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_void_p)
    user32.EnumWindows(EP(cb),0)
    return hwnds[0] if hwnds else None

for attempt in range(5):
    cur = check_trade_allowed()
    log(f"[AT attempt {attempt}] trade_allowed={cur}")
    if cur is True:
        log("AutoTrading already ON"); break
    h = find_mt5()
    if not h:
        log("  no MT5 window yet"); time.sleep(5); continue
    user32.ShowWindow(h,9); user32.SetForegroundWindow(h); user32.SetFocus(h)
    time.sleep(0.5)
    for vk in (0x11,0x45): user32.keybd_event(vk,0,0,0); time.sleep(0.05)
    for vk in (0x45,0x11): user32.keybd_event(vk,0,2,0); time.sleep(0.05)
    log("  sent Ctrl+E")
    time.sleep(2)
    if check_trade_allowed() is True:
        log("AutoTrading ON success"); break

# 4. Restart bot services
log("restarting bot services")
subprocess.run(["powershell","-NoProfile","-Command",
    "Restart-Service Kha0sysMathBot,Kha0sysTradersBot,Kha0sysAmo8 -Force -ErrorAction SilentlyContinue"])
log("=== on_logon_setup DONE ===")
