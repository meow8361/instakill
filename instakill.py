import keyboard
import subprocess
import time
import win32gui
import win32process
import psutil
import ctypes
import sys
import os

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    # Relaunch the script with admin rights
    script = os.path.abspath(sys.argv[0])
    params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)

def get_foreground_process_name():
    hwnd = win32gui.GetForegroundWindow()
    if hwnd == 0:
        return None

    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    try:
        process = psutil.Process(pid)
        return process.name()
    except psutil.NoSuchProcess:
        return None

def kill_foreground_process():
    process_name = get_foreground_process_name()
    if process_name:
        print(f"[!] Killing: {process_name}")
        try:
            subprocess.run(["taskkill", "/f", "/im", process_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"Failed to kill {process_name}: {e}")
    else:
        print("[-] No active window found.")

def main():
    print("[✔] Script is running. Press Alt+F4 to force-close the active window.")
    while True:
        if keyboard.is_pressed("alt+f4"):
            kill_foreground_process()
            time.sleep(1.5)

if __name__ == "__main__":
    if not is_admin():
        print("[🔐] Requesting admin privileges...")
        run_as_admin()
        sys.exit()

    main()
