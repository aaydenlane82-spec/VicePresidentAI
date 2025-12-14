import json
import os

MEMORY_FILE = "memory.json"

DEFAULT_MEMORY = {
    "runs": 0,
    "apps": 0,
    "upgrades_done": 0,
    "upgrades_created": 0,
    "success_patterns": {},
    "learned_iterations": 0
}

def load_memory():
    # If file does not exist, create it
    if not os.path.exists(MEMORY_FILE):
        save_memory(DEFAULT_MEMORY.copy())
        return DEFAULT_MEMORY.copy()

    try:
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
    except Exception:
        # Corrupted or empty file → hard reset
        save_memory(DEFAULT_MEMORY.copy())
        return DEFAULT_MEMORY.copy()

    # 🔥 CRITICAL FIX: ensure ALL keys exist
    repaired = False
    for key, value in DEFAULT_MEMORY.items():
        if key not in data:
            data[key] = value
            repaired = True

    if repaired:
        save_memory(data)

    return data


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)
