# apocalypse_launcher.py
"""
Apocalypse Launcher - fully upgraded
Automatically upgrades VP -> Jarvis, kills bugs, and ensures self-healing
"""

import subprocess
import sys
import os
from memory import load_memory, save_memory

MAX_UPGRADES = 10  # Example threshold for "fully Jarvis"

def apocalypse_sequence():
    memory = load_memory()
    print("[Apocalypse] Starting Jarvis transformation sequence...")

    # Step 1: Bug Kill
    run_script("bug_killer.py")

    # Step 2: Auto Upgrade
    run_script("auto_upgrade.py")

    # Step 3: Self Healing
    run_script("self_heal.py")

    # Step 4: Check memory upgrades
    memory["upgrades_done"] += 1
    save_memory(memory)
    print(f"[Apocalypse] Upgrades done: {memory['upgrades_done']}")

    # Step 5: Recursive check for full Jarvis
    if memory["upgrades_done"] < MAX_UPGRADES:
        print("[Apocalypse] Jarvis not fully operational yet. Relaunching VP...")
        relaunch_vp()
    else:
        print("[Apocalypse] Jarvis is fully awake. System stable and upgraded!")

def run_script(script_name):
    if not os.path.exists(script_name):
        print(f"[Apocalypse] WARNING: {script_name} not found. Skipping...")
        return
    print(f"[Apocalypse] Running {script_name}...")
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[Apocalypse] ERROR in {script_name}: {result.stderr}")
    else:
        print(f"[Apocalypse] {script_name} completed successfully.")
    return result.returncode

def relaunch_vp():
    """
    Relaunch VP.py safely to continue upgrades.
    """
    print("[Apocalypse] Relaunching VP.py...")
    result = subprocess.run([sys.executable, "vp.py"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[Apocalypse] ERROR relaunching VP.py: {result.stderr}")
    else:
        print("[Apocalypse] VP.py relaunch completed successfully.")

if __name__ == "__main__":
    apocalypse_sequence()
