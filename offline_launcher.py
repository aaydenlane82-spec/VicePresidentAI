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

# Settings
RESTART_LIMIT = 5      # max restarts within TIME_WINDOW seconds
TIME_WINDOW = 60       # window in seconds
COOLDOWN = 5           # seconds to wait after a crash before restarting

# Track restart history
restart_history = {}

def run_script(path, name):
    restart_history[name] = []

    while True:
        # Clean up old timestamps
        now = time.time()
        restart_history[name] = [t for t in restart_history[name] if now - t < TIME_WINDOW]

        if len(restart_history[name]) >= RESTART_LIMIT:
            print(f"{name} has reached the restart limit. Waiting {TIME_WINDOW} seconds before retrying...")
            time.sleep(TIME_WINDOW)
            restart_history[name] = []  # reset after waiting

        try:
            subprocess.run([sys.executable, path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"{name} crashed: {e}. Restarting in {COOLDOWN} seconds...")
        except Exception as e:
            print(f"{name} unexpected error: {e}. Restarting in {COOLDOWN} seconds...")
        finally:
            restart_history[name].append(time.time())
            time.sleep(COOLDOWN)

if __name__ == "__main__":
    threads = []

    modules = [
        (VP_PATH, "VP"),
        (AUTO_UPGRADE_PATH, "Auto-Upgrade"),
        (SELF_HEAL_PATH, "Self-Heal")
    ]

    for path, name in modules:
        t = threading.Thread(target=run_script, args=(path, name), daemon=True)
        threads.append(t)
        t.start()

    print("Offline Launcher running all systems locally. Ctrl+C to stop.")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Offline Launcher shutting down...")
