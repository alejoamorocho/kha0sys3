"""AutoTrading watchdog — keeps MT5 trade_allowed ON without manual help.

The autologon/on_logon setup only fixes AutoTrading at BOOT. But the toolbar
button can turn OFF in-session (RDP reconnect, broker reconnect, MT5 update).
This watchdog polls trade_allowed and re-enables it via an interactive
scheduled task (Ctrl+E in the session that owns the terminal) — the only
thing that works across the Session-0/Session-1 isolation.

Run as a long-lived NSSM service (Kha0sysATWatchdog). Self-heals:
  1. every CHECK_SEC, read terminal_info().trade_allowed
  2. if OFF for 2 consecutive checks, run the in-session toggle task
  3. verify; if still OFF, ensure common.ini Enabled=1 (next launch safe)
  4. log + optional telegram alert
"""
from __future__ import annotations
import sys, time, subprocess, os
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

CHECK_SEC = 180          # poll every 3 min
LOG = r"C:\ProgramData\Kha0sysMath\logs\at_watchdog.log"
COMMON_INI = r"C:\Users\Administrator\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\config\common.ini"

os.makedirs(os.path.dirname(LOG), exist_ok=True)
def log(m):
    line=f"{datetime.now(timezone.utc).isoformat()} {m}"
    print(line, flush=True)
    try:
        with open(LOG,"a",encoding="utf-8") as f: f.write(line+"\n")
    except Exception: pass

def ps(cmd, timeout=60):
    try:
        r=subprocess.run(["powershell","-NoProfile","-Command",cmd],capture_output=True,text=True,timeout=timeout)
        return r.stdout.strip(), r.stderr.strip()
    except Exception as e:
        return "", str(e)

def trade_allowed():
    try:
        import MetaTrader5 as mt5
        if not mt5.initialize():
            return None
        ti=mt5.terminal_info()
        v=bool(ti.trade_allowed) if ti else None
        mt5.shutdown()
        return v
    except Exception as e:
        log(f"check error: {e}")
        return None

def ensure_common_enabled():
    try:
        raw=open(COMMON_INI,"rb").read(); bom=raw[:2]
        enc="utf-16-le" if bom==b"\xff\xfe" else "utf-8"
        text=raw.decode(enc).lstrip("﻿"); out=[]; in_exp=False; changed=False
        for ln in text.splitlines():
            s=ln.strip()
            if s.startswith("["): in_exp=(s.lower()=="[experts]")
            if in_exp and s.startswith("Enabled="):
                out.append("Enabled=1"); changed=(s!="Enabled=1")
            else: out.append(ln)
        open(COMMON_INI,"wb").write(bom+("\r\n".join(out)+"\r\n").encode(enc))
        if changed: log("common.ini Enabled=1 set")
    except Exception as e:
        log(f"common.ini error: {e}")

def reactivate():
    """Run the in-session toggle (Ctrl+E) via interactive scheduled task,
    after making sure the Administrator session is attached to console so
    SetForegroundWindow works."""
    ensure_common_enabled()
    # 1) reconnect any disconnected Administrator session to console for focus
    qw,_=ps("qwinsta")
    admin_id=None
    for line in qw.splitlines():
        if "Administrator" in line:
            for tok in line.split():
                if tok.isdigit(): admin_id=tok; break
    if admin_id and admin_id!="1":
        ps(f"tscon {admin_id} /dest:console")
        time.sleep(2)
    # 2) interactive scheduled task runs the toggle script in the user session
    task=r"""
$t='KhaosysATfix'
Unregister-ScheduledTask -TaskName $t -Confirm:$false -ErrorAction SilentlyContinue
$a=New-ScheduledTaskAction -Execute 'C:\Python312\python.exe' -Argument 'C:\Proyectos\kha0sys3\scripts\_toggle_autotrading_v2.py'
$tr=New-ScheduledTaskTrigger -At (Get-Date).AddSeconds(8) -Once
$p=New-ScheduledTaskPrincipal -UserId Administrator -LogonType Interactive -RunLevel Highest
$task=New-ScheduledTask -Action $a -Trigger $tr -Principal $p
Register-ScheduledTask -TaskName $t -InputObject $task -Force | Out-Null
Start-ScheduledTask -TaskName $t
Start-Sleep -Seconds 22
Unregister-ScheduledTask -TaskName $t -Confirm:$false -ErrorAction SilentlyContinue
"""
    ps(task, timeout=60)

def main():
    log("=== AutoTrading watchdog START ===")
    off_count=0
    while True:
        ta=trade_allowed()
        if ta is True:
            if off_count>0: log("trade_allowed back ON")
            off_count=0
        elif ta is False:
            off_count+=1
            log(f"trade_allowed=OFF (count={off_count})")
            if off_count>=2:   # ~6 min OFF -> act
                log("reactivating AutoTrading...")
                reactivate()
                time.sleep(8)
                after=trade_allowed()
                log(f"after reactivation: trade_allowed={after}")
                if after is True:
                    off_count=0
                    # restart bots so they reconnect cleanly
                    ps("Restart-Service Kha0sysAmo8,Kha0sysTradersBot,Kha0sysMathBot -Force -ErrorAction SilentlyContinue", timeout=90)
                    log("bots restarted")
        else:
            log("trade_allowed=unknown (MT5 not reachable)")
        time.sleep(CHECK_SEC)

if __name__=="__main__":
    main()
