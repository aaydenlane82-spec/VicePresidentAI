import threading
import time
import subprocess
import sys
import os

# Get absolute paths to scripts (so it works from any directory)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VP_PATH = os.path.join(BASE_DIR, "vp.py")
AUTO_UPGRADE_PATH = os.path.join(BASE_DIR, "auto_upgrade.py")
SELF_HEAL_PATH = os.path.join(BASE_DIR, "self_heal.py")

# Function to run a script continuously
def run_script(path, name):
    while True:
        try:
            subprocess.run([sys.executable, path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"{name} crashed: {e}. Restarting...")
        except Exception as e:
            print(f"{name} unexpected error: {e}. Restarting...")
        time.sleep(1)

if __name__ == "__main__":
    threads = []

    # VP thread
    vp_thread = threading.Thread(target=run_script, args=(VP_PATH, "VP"), daemon=True)
    threads.append(vp_thread)

    # Auto-upgrade thread
    upgrade_thread = threading.Thread(target=run_script, args=(AUTO_UPGRADE_PATH, "Auto-Upgrade"), daemon=True)
    threads.append(upgrade_thread)

    # Self-heal thread
    heal_thread = threading.Thread(target=run_script, args=(SELF_HEAL_PATH, "Self-Heal"), daemon=True)
    threads.append(heal_thread)

    # Start all threads
    for t in threads:
        t.start()

    print("Offline Launcher running all systems locally. Ctrl+C to stop.")

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Offline Launcher shutting down...")
