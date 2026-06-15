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
TERMINAL_EXE = r"C:\Program Files\MetaTrader 5\terminal64.exe"

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

# Root cause of the weekend AutoTrading-off: MT5 re-authorizes the account
# repeatedly when the market is closed, and with [Experts] Account=1 / Profile=1
# it auto-disables AutoTrading on each "account/profile change". Force those OFF
# and keep Enabled ON so weekend reconnects no longer kill trading. (Read at
# terminal launch, so a change only takes effect after a terminal restart.)
EXPERTS_ENFORCE = {"Enabled": "1", "Account": "0", "Profile": "0"}

def ensure_common_enabled():
    try:
        raw=open(COMMON_INI,"rb").read(); bom=raw[:2]
        enc="utf-16-le" if bom==b"\xff\xfe" else "utf-8"
        text=raw.decode(enc).lstrip("﻿"); out=[]; in_exp=False; changed=[]
        for ln in text.splitlines():
            s=ln.strip()
            if s.startswith("["): in_exp=(s.lower()=="[experts]")
            key=s.split("=",1)[0] if "=" in s else ""
            if in_exp and key in EXPERTS_ENFORCE:
                want=f"{key}={EXPERTS_ENFORCE[key]}"
                if s!=want: changed.append(want)
                out.append(want)
            else: out.append(ln)
        open(COMMON_INI,"wb").write(bom+("\r\n".join(out)+"\r\n").encode(enc))
        if changed: log("common.ini enforced: "+", ".join(changed))
    except Exception as e:
        log(f"common.ini error: {e}")

def _admin_session():
    """Return (session_id, state) for the Administrator session, or (None, None).
    state is 'Active', 'Disc', or '?'."""
    qw,_=ps("qwinsta")
    for line in qw.splitlines():
        if "Administrator" in line:
            sid=next((t for t in line.split() if t.isdigit()), None)
            state="Active" if "Active" in line else ("Disc" if "Disc" in line else "?")
            return sid, state
    return None, None

def restart_terminal():
    """Session-independent fallback when the Ctrl+E toggle can't restore
    AutoTrading (RDP session disconnected -> no desktop focus). Relaunching MT5
    with common.ini [Experts] Enabled=1 brings AutoTrading back ON on startup,
    no foreground window required. MT5 auto-logins to the saved account."""
    ensure_common_enabled()
    log("restarting MT5 terminal (Enabled=1 -> AutoTrading ON on launch)")
    ps("Stop-Process -Name terminal64 -Force -ErrorAction SilentlyContinue", timeout=30)
    time.sleep(6)
    ps(f"Start-Process '{TERMINAL_EXE}'", timeout=30)
    time.sleep(45)  # allow auto-login + broker reconnect

def reactivate():
    """Run the in-session toggle (Ctrl+E) via interactive scheduled task,
    after making sure the Administrator session is attached to console so
    SetForegroundWindow works."""
    ensure_common_enabled()
    # 1) reconnect the Administrator session to console for focus.
    # The weekend RDP disconnect leaves the session in 'Disc' (session id is
    # usually 1) -> the toggle's SetForegroundWindow silently no-ops. Always
    # re-attach unless it is already Active on console. (Previously this was
    # skipped whenever admin_id=='1', which is exactly the broken weekend case.)
    sid, state = _admin_session()
    if sid and state != "Active":
        ps(f"tscon {sid} /dest:console")
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
    restarted=False   # terminal already restarted this outage? (rate-limit)
    while True:
        ta=trade_allowed()
        if ta is True:
            if off_count>0: log("trade_allowed back ON")
            off_count=0
            restarted=False
        elif ta is False:
            off_count+=1
            log(f"trade_allowed=OFF (count={off_count})")
            if off_count>=2:   # ~6 min OFF -> act
                log("reactivating AutoTrading...")
                reactivate()
                time.sleep(8)
                after=trade_allowed()
                log(f"after reactivation: trade_allowed={after}")
                if after is not True and not restarted:
                    # Ctrl+E toggle failed even after console attach -> escalate
                    # to a session-independent terminal restart, once per outage.
                    restart_terminal()
                    restarted=True
                    after=trade_allowed()
                    log(f"after terminal restart: trade_allowed={after}")
                if after is True:
                    off_count=0
                    restarted=False
                    # restart bots so they reconnect cleanly
                    ps("Restart-Service Kha0sysAmo8,Kha0sysTradersBot,Kha0sysMathBot -Force -ErrorAction SilentlyContinue", timeout=90)
                    log("bots restarted")
        else:
            log("trade_allowed=unknown (MT5 not reachable)")
        time.sleep(CHECK_SEC)

if __name__=="__main__":
    main()
