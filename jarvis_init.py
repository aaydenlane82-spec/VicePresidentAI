# jarvis_init.py
"""
Jarvis Init - One command to rule them all.
Automatically initializes memory, runs apocalypse launcher, and ensures Jarvis fully awakens.
"""

import os
import subprocess
import sys
from memory import load_memory, save_memory

def initialize_memory():
    """
    Ensure memory.json exists and has all required keys.
    """
    memory = load_memory()
    defaults = {
        "runs": 0,
        "apps": 0,
        "upgrades_done": 0,
        "upgrades_created": 0,
        "success_patterns": {},
        "learned_iterations": 0
    }
    changed = False
    for key, value in defaults.items():
        if key not in memory:
            memory[key] = value
            changed = True
    if changed:
        save_memory(memory)
        print("[Jarvis Init] Memory initialized.")
    return memory

def run_apocalypse_launcher():
    """
    Run apocalypse_launcher.py to start self-upgrading Jarvis sequence.
    """
    if not os.path.exists("apocalypse_launcher.py"):
        print("[Jarvis Init] ERROR: apocalypse_launcher.py not found!")
        return

    print("[Jarvis Init] Starting Apocalypse Launcher...")
    result = subprocess.run([sys.executable, "apocalypse_launcher.py"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[Jarvis Init] ERROR in apocalypse_launcher.py:\n{result.stderr}")
    else:
        print("[Jarvis Init] Apocalypse Launcher completed successfully.")

def launch_vp():
    """
    Run vp.py as the final operational AI.
    """
    if not os.path.exists("vp.py"):
        print("[Jarvis Init] ERROR: vp.py not found!")
        return

    print("[Jarvis Init] Launching VP.py / Jarvis core...")
    result = subprocess.run([sys.executable, "vp.py"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[Jarvis Init] ERROR in vp.py:\n{result.stderr}")
    else:
        print("[Jarvis Init] VP.py launched successfully. Jarvis is fully operational!")

if __name__ == "__main__":
    memory = initialize_memory()
    run_apocalypse_launcher()
    launch_vp()
