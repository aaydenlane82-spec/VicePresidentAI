import subprocess
import threading
import time
import sys
import os

# Absolute paths to all critical scripts
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = {
    "VP": os.path.join(BASE_DIR, "vp.py"),
    "Auto-Upgrade": os.path.join(BASE_DIR, "auto_upgrade.py"),
    "Self-Heal": os.path.join(BASE_DIR, "self_heal.py"),
    "Atomic-Memory": os.path.join(BASE_DIR, "atomic_memory.py"),
    "Bug-Killer": os.path.join(BASE_DIR, "bug_killer.py")
}

# Function to run a script and auto-restart on exit code 1
def run_script(name, path):
    while True:
        try:
            subprocess.run([sys.executable, path], check=True)
        except subprocess.CalledProcessError as e:
            if e.returncode == 1:
                print(f"[{name}] exited with code 1. Restarting...")
            else:
                print(f"[{name}] crashed with code {e.returncode}. Restarting...")
        except Exception as e:
            print(f"[{name}] unexpected error: {e}. Restarting...")
        time.sleep(1)

if __name__ == "__main__":
    threads = []
    for name, path in SCRIPTS.items():
        t = threading.Thread(target=run_script, args=(name, path), daemon=True)
        threads.append(t)
        t.start()

    print("Error Handler running all scripts. Ctrl+C to exit.")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Error Handler shutting down...")
