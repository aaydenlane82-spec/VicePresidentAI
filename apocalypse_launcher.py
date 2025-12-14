# apocalypse_launcher.py
"""
Apocalypse Launcher
Fully upgraded orchestrator to launch Jarvis,
self-heal, auto-upgrade, and eliminate lingering bugs.
"""

import time
import sys
import os

from memory import load_memory, save_memory
from auto_upgrade import perform_upgrades
from self_heal import self_heal_system
from bug_killer import kill_bugs

def init_environment():
    """
    Ensures all critical files exist and initializes memory.
    """
    memory = load_memory()
    print(f"[Launcher] Memory loaded. Runs so far: {memory['runs']}")
    return memory

def pre_launch_checks():
    """
    Perform self-healing and bug elimination before launch.
    """
    print("[Launcher] Performing pre-launch self-heal...")
    self_heal_system()
    print("[Launcher] Checking for bugs...")
    kill_bugs()
    print("[Launcher] Pre-launch checks complete.")

def launch_jarvis():
    """
    Launch VP/Jarvis main system.
    """
    print("[Launcher] Launching Jarvis...")
    try:
        import vp  # your main VP module
        vp.main()
    except Exception as e:
        print(f"[Launcher] Error during launch: {e}")
        print("[Launcher] Attempting emergency self-heal...")
        self_heal_system()
        time.sleep(1)
        print("[Launcher] Relaunching Jarvis...")
        import vp
        vp.main()

def post_launch_tasks(memory):
    """
    Increment run counters and perform upgrades after launch.
    """
    memory["runs"] += 1
    save_memory(memory)
    print("[Launcher] Triggering auto-upgrades...")
    perform_upgrades()
    print("[Launcher] Launch sequence complete.")

def main():
    print("[Launcher] Apocalypse Launcher initialized.")
    memory = init_environment()
    pre_launch_checks()
    launch_jarvis()
    post_launch_tasks(memory)
    print("[Launcher] Jarvis is fully operational. Apocalypse complete.")

if __name__ == "__main__":
    main()
