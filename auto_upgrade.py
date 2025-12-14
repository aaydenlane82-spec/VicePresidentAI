import json
import os
import time
from upgrades import apply_upgrades

MEMORY_FILE = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"upgrades_applied": 0}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def auto_upgrade_loop():
    memory = load_memory()
    while True:
        try:
            upgrades_applied = apply_upgrades()
            memory["upgrades_applied"] = memory.get("upgrades_applied", 0) + upgrades_applied
            save_memory(memory)
        except Exception as e:
            print(f"Error in auto-upgrade: {e}")
        time.sleep(10)  # Adjust interval for upgrades
