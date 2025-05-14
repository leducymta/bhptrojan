import os

def run(**args):
    print("[*] In dirlister module.")
    
    try:
        files = os.listdir(".")
        if not files:
            return "[*] No files found in current directory."
        
        result = "[*] Files in current directory:\n"
        result += "\n".join(f"- {f}" for f in files)
        return result
    except Exception as e:
        return f"[!] Error while listing files: {e}"

