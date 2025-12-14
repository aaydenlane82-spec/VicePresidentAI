import subprocess
import time
import os
import sys
from threading import Thread

# Paths to scripts
VP_SCRIPT = "vp.py"
SELF_HEAL_SCRIPT = "self_heal.py"
AUTO_UPGRADE_SCRIPT = "auto_upgrade.py"

def run_script(script_name):
    """Run a Python script and restart it if it crashes."""
    while True:
        try:
            print(f"[Launcher] Starting {script_name}...")
            subprocess.run([sys.executable, script_name], check=True)
        except subprocess.CalledProcessError:
            print(f"[Launcher] {script_name} crashed. Restarting in 5s...")
            time.sleep(5)
        except Exception as e:
            print(f"[Launcher] Unexpected error in {script_name}: {e}")
            time.sleep(5)

def main():
    # Ensure the current directory is the repo root
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Start self_heal first
    Thread(target=run_script, args=(SELF_HEAL_SCRIPT,), daemon=True).start()
    time.sleep(2)  # Give self_heal a moment to initialize

    # Start auto_upgrade
    Thread(target=run_script, args=(AUTO_UPGRADE_SCRIPT,), daemon=True).start()
    time.sleep(2)  # Give upgrades a moment to start

    # Start VP (this one blocks main thread)
    run_script(VP_SCRIPT)

if __name__ == "__main__":
    main()
