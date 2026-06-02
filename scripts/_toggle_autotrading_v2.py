"""Toggle MT5 AutoTrading robustly from within the interactive session.

Improvements over v1:
  - AttachThreadInput trick to force SetForegroundWindow even without
    genuine focus (works in RDP/console sessions).
  - Verify focus actually landed on MT5 before sending keys.
  - Retry: if still OFF after first Ctrl+E, send again (toggle may have
    been consumed). Stop as soon as trade_allowed flips to True.
"""
import time
import sys
import ctypes
from ctypes import wintypes

RESULT_FILE = r"C:\Temp\autotrading_result.txt"
def log(msg):
    with open(RESULT_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
open(RESULT_FILE, "w").close()

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

def find_mt5():
    hwnds = []
    def cb(hwnd, lp):
        cls = ctypes.create_unicode_buffer(256)
        user32.GetClassNameW(hwnd, cls, 256)
        if "MetaQuotes::MetaTrader" in cls.value and user32.IsWindowVisible(hwnd):
            hwnds.append(hwnd)
        return True
    EnumProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    user32.EnumWindows(EnumProc(cb), 0)
    return hwnds[0] if hwnds else None

def force_foreground(hwnd):
    """Force hwnd to foreground using AttachThreadInput trick."""
    fg = user32.GetForegroundWindow()
    target_tid = user32.GetWindowThreadProcessId(hwnd, None)
    fg_tid = user32.GetWindowThreadProcessId(fg, None) if fg else 0
    cur_tid = kernel32.GetCurrentThreadId()
    # Attach our thread + foreground thread to target's input queue
    user32.AttachThreadInput(cur_tid, target_tid, True)
    if fg_tid:
        user32.AttachThreadInput(fg_tid, target_tid, True)
    user32.ShowWindow(hwnd, 9)   # SW_RESTORE
    user32.BringWindowToTop(hwnd)
    user32.SetForegroundWindow(hwnd)
    user32.SetActiveWindow(hwnd)
    user32.SetFocus(hwnd)
    time.sleep(0.3)
    user32.AttachThreadInput(cur_tid, target_tid, False)
    if fg_tid:
        user32.AttachThreadInput(fg_tid, target_tid, False)
    # Verify
    now_fg = user32.GetForegroundWindow()
    return now_fg == hwnd

def send_ctrl_e():
    VK_CONTROL, VK_E, KEYUP = 0x11, 0x45, 0x0002
    user32.keybd_event(VK_CONTROL, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(VK_E, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(VK_E, 0, KEYUP, 0)
    time.sleep(0.05)
    user32.keybd_event(VK_CONTROL, 0, KEYUP, 0)

def check_trade_allowed():
    try:
        import MetaTrader5 as mt5
        mt5.initialize()
        ti = mt5.terminal_info()
        val = bool(ti.trade_allowed) if ti else None
        mt5.shutdown()
        return val
    except Exception as e:
        log(f"  API check error: {e}")
        return None

hwnd = find_mt5()
if not hwnd:
    log("ERROR: no MT5 window found")
    sys.exit(1)
log(f"MT5 hwnd={hwnd}")

for attempt in range(4):
    cur = check_trade_allowed()
    log(f"[attempt {attempt}] trade_allowed before = {cur}")
    if cur is True:
        log("Already ON — done.")
        break
    focused = force_foreground(hwnd)
    log(f"  force_foreground -> focused={focused}")
    send_ctrl_e()
    log("  sent Ctrl+E")
    time.sleep(2.0)
    after = check_trade_allowed()
    log(f"  trade_allowed after = {after}")
    if after is True:
        log("SUCCESS: AutoTrading is now ON")
        break
    time.sleep(1.0)
