"""Verify MT5 terminal AutoTrading + try to enable via Win32 GUI automation.

Run on VPS. Checks:
  - mt5.terminal_info().trade_allowed
  - mt5.account_info().trade_allowed / trade_expert
  - order_check() smoke test to see if a real order would pass

If trade_allowed is False, sends Ctrl+E to MT5 terminal window to toggle
AutoTrading button.
"""
import sys
import time
from pathlib import Path

import MetaTrader5 as mt5


def diagnose():
    if not mt5.initialize():
        print(f"mt5.initialize() FAILED: {mt5.last_error()}")
        return False
    ti = mt5.terminal_info()
    ai = mt5.account_info()
    print("=== TERMINAL INFO ===")
    if ti:
        print(f"  trade_allowed     : {ti.trade_allowed}")
        print(f"  tradeapi_disabled : {ti.tradeapi_disabled}")
        print(f"  connected         : {ti.connected}")
        print(f"  build             : {ti.build}")
        print(f"  name              : {ti.name}")
        print(f"  path              : {ti.path}")
        print(f"  data_path         : {ti.data_path}")
    else:
        print("  None")
    print()
    print("=== ACCOUNT INFO ===")
    if ai:
        print(f"  login        : {ai.login}")
        print(f"  trade_allowed: {ai.trade_allowed}")
        print(f"  trade_expert : {ai.trade_expert}")
        print(f"  trade_mode   : {ai.trade_mode}  (0=demo, 1=contest, 2=real)")
        print(f"  balance      : ${ai.balance:.2f}")
        print(f"  margin_free  : ${ai.margin_free:.2f}")

    # Order check smoke test
    print()
    print("=== ORDER CHECK SMOKE TEST ===")
    si = mt5.symbol_info("EURUSD+")
    tick = mt5.symbol_info_tick("EURUSD+")
    if si and ai and tick:
        req = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": "EURUSD+",
            "volume": 0.01,
            "type": mt5.ORDER_TYPE_BUY_STOP,
            "price": round(tick.ask + si.point * 200, si.digits),
            "sl": 0.0, "tp": 0.0,
            "deviation": 10,
            "magic": 1338,
            "comment": "M|TEST|CHECK|TEST",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }
        r = mt5.order_check(req)
        if r:
            print(f"  retcode={r.retcode} ({r.comment})")
            print(f"  margin_required={r.margin}  margin_free_after={r.margin_free}")
            print(f"  --> retcode 0 means OK, 10027 means AutoTrading OFF")

    return ti, ai


def enable_autotrading_via_keystroke(term_path: str):
    """Try to enable AutoTrading by sending Ctrl+E to the MT5 terminal window."""
    print()
    print("=== Attempting to enable AutoTrading via Ctrl+E ===")
    try:
        import ctypes
        from ctypes import wintypes
        user32 = ctypes.windll.user32

        # Find MT5 terminal window by title pattern
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool,
                                              wintypes.HWND, wintypes.LPARAM)
        hwnd_found = []

        def callback(hwnd, lparam):
            length = user32.GetWindowTextLengthW(hwnd)
            buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buf, length + 1)
            title = buf.value
            if "MetaTrader 5" in title or "Vantage" in title:
                hwnd_found.append((hwnd, title))
            return True

        user32.EnumWindows(EnumWindowsProc(callback), 0)
        if not hwnd_found:
            print("  No MT5 window found — terminal may be running headless/service")
            return False
        for hwnd, title in hwnd_found:
            print(f"  Found window: hwnd={hwnd} title='{title}'")

        # Try sending Ctrl+E to the FIRST MT5 window
        hwnd, title = hwnd_found[0]
        # Bring to foreground first (best effort)
        user32.SetForegroundWindow(hwnd)
        time.sleep(0.3)

        # Send WM_COMMAND for Ctrl+E (toolbar AutoTrading toggle)
        # MT5 has a menu command for this — typically COMMAND_TOGGLE_AUTOTRADING.
        # Without exact ID we'll simulate Ctrl+E keystroke
        VK_CONTROL = 0x11
        VK_E = 0x45
        KEYEVENTF_KEYUP = 0x0002
        user32.keybd_event(VK_CONTROL, 0, 0, 0)
        time.sleep(0.05)
        user32.keybd_event(VK_E, 0, 0, 0)
        time.sleep(0.05)
        user32.keybd_event(VK_E, 0, KEYEVENTF_KEYUP, 0)
        time.sleep(0.05)
        user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)
        print("  Sent Ctrl+E to MT5 window")
        return True
    except Exception as e:
        print(f"  ERR: {e}")
        return False


def write_config(term_data_path: str):
    """Edit MT5 config to force AutoTrading enabled.

    MT5 stores config in <data_path>/config/common.ini and accounts.ini.
    The relevant flag is `Experts/Enabled=1` and `ExpertsDllImport=1`.
    """
    print()
    print("=== Forcing config files (best-effort) ===")
    if not term_data_path:
        print("  No data_path provided"); return False
    p = Path(term_data_path)
    common = p / "config" / "common.ini"
    accounts = p / "config" / "accounts.ini"
    found = []
    for f in (common, accounts):
        if f.exists():
            found.append(f)
            print(f"  Found: {f}")
    if not found:
        print("  No config files found in data_path")
        return False
    # Read+write to ensure Experts enabled
    for f in found:
        try:
            txt = f.read_text(encoding="utf-16-le", errors="ignore")
            # Inject ExpertsEnabled=1 under [Experts] section
            if "[Experts]" in txt:
                if "Enabled=0" in txt:
                    txt = txt.replace("Enabled=0", "Enabled=1")
                    f.write_text(txt, encoding="utf-16-le")
                    print(f"  Patched {f}: Enabled 0 -> 1")
        except Exception as e:
            print(f"  ERR on {f}: {e}")
    return True


def main():
    info = diagnose()
    if not info:
        return
    ti, ai = info
    if ti and ti.trade_allowed:
        print("\nAutoTrading is ON — no action needed.")
        mt5.shutdown()
        return
    print("\nAutoTrading is OFF — attempting to enable...")
    # Try keystroke
    enable_autotrading_via_keystroke(ti.path if ti else "")
    time.sleep(2)
    # Re-check
    ti2 = mt5.terminal_info()
    if ti2 and ti2.trade_allowed:
        print(f"\n✓ AutoTrading enabled via Ctrl+E (now trade_allowed={ti2.trade_allowed})")
    else:
        print(f"\n✗ Still OFF after Ctrl+E. trade_allowed={ti2.trade_allowed if ti2 else '?'}")
        # Try config file
        write_config(ti.data_path if ti else "")
    mt5.shutdown()


if __name__ == "__main__":
    main()
