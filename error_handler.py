import subprocess
import sys
import os
import time

# Absolute paths to critical scripts
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VP_PATH = os.path.join(BASE_DIR, "vp.py")
AUTO_UPGRADE_PATH = os.path.join(BASE_DIR, "auto_upgrade.py")
SELF_HEAL_PATH = os.path.join(BASE_DIR, "self_heal.py")

# Function to run a script with exit code 1 recovery
def run_with_exit_code_fix(path, name):
    while True:
        try:
            subprocess.run([sys.executable, path], check=True)
        except subprocess.CalledProcessError as e:
            if e.returncode == 1:
                print(f"{name} exited with code 1. Attempting recovery...")
                # Attempt minimal recovery logic
                try:
                    subprocess.run([sys.executable, SELF_HEAL_PATH], check=True)
                    print(f"{name} recovery applied. Restarting...")
                except Exception as heal_err:
                    print(f"Self-heal failed: {heal_err}. Retrying in 5s...")
                    time.sleep(5)
            else:
                print(f"{name} crashed with code {e.returncode}. Restarting...")
        except Exception as e:
            print(f"{name} unexpected error: {e}. Restarting...")
        time.sleep(1)

if __name__ == "__main__":
    scripts = [
        (VP_PATH, "VP"),
        (AUTO_UPGRADE_PATH, "Auto-Upgrade")
    ]

    for path, name in scripts:
        # Run each script in a separate thread
        import threading
        t = threading.Thread(target=run_with_exit_code_fix, args=(path, name), daemon=True)
        t.start()

    print("Error Handler running. Monitoring scripts for exit code 1...")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Error Handler shutting down...")
