# apocalypse_launcher.py
"""
Apocalypse Launcher - fully integrates with VP system
Handles Jarvis transformation, auto-upgrades, bug extermination, and self-healing routines
"""

import os
import sys
import json
import time
from auto_upgrade import run as auto_upgrade_run
from bug_killer import run as bug_killer_run
from self_heal import run as self_heal_run
from jarvis_core import run as jarvis_core_run
from jarvis_conscious_engine import run as jarvis_conscious_run

MEMORY_FILE = "memory.json"

def load_memory():
    """Load memory from memory.json, initialize if missing keys"""
    if not os.path.exists(MEMORY_FILE):
        memory = {
            "runs": 0,
            "apps": 0,
            "upgrades_done": 0,
            "upgrades_created": 0,
            "success_patterns": {},
            "learned_iterations": 0
        }
        save_memory(memory)
        return memory

    with open(MEMORY_FILE, "r") as f:
        memory = json.load(f)

    # Ensure all keys exist
    defaults = {
        "runs": 0,
        "apps": 0,
        "upgrades_done": 0,
        "upgrades_created": 0,
        "success_patterns": {},
        "learned_iterations": 0
    }
    for k, v in defaults.items():
        memory.setdefault(k, v)

    return memory

def save_memory(memory):
    """Save memory back to file"""
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

def apocalypse_sequence():
    """Full Jarvis / VP apocalypse upgrade sequence"""
    memory = load_memory()
    memory["runs"] += 1
    print(f"[Apocalypse Launcher] Starting run #{memory['runs']}...")

    # Step 1: Kill all persistent bugs
    print("[Apocalypse Launcher] Running bug killer...")
    bug_killer_run(memory)

    # Step 2: Auto-upgrade everything
    print("[Apocalypse Launcher] Running auto-upgrades...")
    auto_upgrade_run(memory)

    # Step 3: Self-heal routines
    print("[Apocalypse Launcher] Running self-heal routines...")
    self_heal_run(memory)

    # Step 4: Upgrade Jarvis core
    print("[Apocalypse Launcher] Running Jarvis core...")
    jarvis_core_run(memory)

    # Step 5: Activate conscious engine
    print("[Apocalypse Launcher] Running Jarvis conscious engine...")
    jarvis_conscious_run(memory)

    # Final save
    save_memory(memory)
    print("[Apocalypse Launcher] Apocalypse sequence complete. Jarvis is fully operational!")

if __name__ == "__main__":
    try:
        apocalypse_sequence()
    except Exception as e:
        print(f"[Apocalypse Launcher] ERROR: {e}", file=sys.stderr)
        sys.exit(1)
