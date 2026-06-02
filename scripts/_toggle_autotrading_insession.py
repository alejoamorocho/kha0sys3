"""Toggle MT5 AutoTrading by sending Ctrl+E FROM WITHIN the interactive session.

This script is meant to be launched via a scheduled task with LogonType
Interactive so it runs in the SAME Windows session as the MT5 terminal
(Session 2), bypassing the Session 0 isolation that blocks WinRM-driven
SendKeys.

It finds the MT5 main window, brings it to foreground, sends Ctrl+E, then
writes the resulting trade_allowed state to a result file that the caller
(in Session 0) can read.
"""
import time
import sys

RESULT_FILE = r"C:\Temp\autotrading_result.txt"

def log(msg):
    with open(RESULT_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

# Reset result file
open(RESULT_FILE, "w").close()

try:
    import win32gui
    import win32con
    import win32api
    HAVE_WIN32 = True
except ImportError:
    HAVE_WIN32 = False
    log("win32gui not available, will try ctypes")

import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32

# Find MT5 window by class name (MetaQuotes::MetaTrader::...)
hwnds = []
def enum_cb(hwnd, lParam):
    length = user32.GetWindowTextLengthW(hwnd)
    buf = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buf, length + 1)
    cls = ctypes.create_unicode_buffer(256)
    user32.GetClassNameW(hwnd, cls, 256)
    title = buf.value
    classname = cls.value
    if "MetaTrader" in title or "MetaQuotes" in classname or "MetaTrader" in classname:
        if user32.IsWindowVisible(hwnd):
            hwnds.append((hwnd, title, classname))
    return True

EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
user32.EnumWindows(EnumWindowsProc(enum_cb), 0)

log(f"Found {len(hwnds)} MT5 windows:")
for hwnd, title, cls in hwnds:
    log(f"  hwnd={hwnd} title='{title}' class='{cls}'")

if not hwnds:
    log("ERROR: no MT5 window found in this session")
    sys.exit(1)

# Use the first (main) window
hwnd = hwnds[0][0]

# Bring to foreground
user32.ShowWindow(hwnd, 9)  # SW_RESTORE
user32.SetForegroundWindow(hwnd)
time.sleep(1.0)

# Send Ctrl+E via keybd_event
VK_CONTROL = 0x11
VK_E = 0x45
KEYEVENTF_KEYUP = 0x0002

user32.keybd_event(VK_CONTROL, 0, 0, 0)          # Ctrl down
time.sleep(0.05)
user32.keybd_event(VK_E, 0, 0, 0)                # E down
time.sleep(0.05)
user32.keybd_event(VK_E, 0, KEYEVENTF_KEYUP, 0)  # E up
time.sleep(0.05)
user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)  # Ctrl up
log("Sent Ctrl+E to MT5 window")
time.sleep(2.0)

# Verify via MT5 API
try:
    import MetaTrader5 as mt5
    mt5.initialize()
    ti = mt5.terminal_info()
    log(f"AFTER Ctrl+E: trade_allowed={ti.trade_allowed}")
    mt5.shutdown()
except Exception as e:
    log(f"MT5 API check failed: {e}")
