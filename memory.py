# memory.py
"""
Memory Helper Module
Handles loading and saving memory.json safely.
Prevents KeyErrors by ensuring all default keys exist.
"""

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
    """
    Load memory.json. If it doesn't exist or is invalid, create a fresh one.
    """
    if not os.path.exists(MEMORY_FILE):
        print(f"[Memory] {MEMORY_FILE} not found. Creating a new one...")
        save_memory(DEFAULT_MEMORY)
        return DEFAULT_MEMORY.copy()
    
    try:
        with open(MEMORY_FILE, "r") as f:
            memory = json.load(f)
    except json.JSONDecodeError:
        print(f"[Memory] {MEMORY_FILE} is corrupted. Resetting...")
        save_memory(DEFAULT_MEMORY)
        return DEFAULT_MEMORY.copy()

    # Ensure all default keys exist
    updated = False
    for key, value in DEFAULT_MEMORY.items():
        if key not in memory:
            memory[key] = value
            updated = True

    if updated:
        print("[Memory] Added missing keys to memory.json")
        save_memory(memory)

    return memory

def save_memory(memory_data):
    """
    Save memory to memory.json
    """
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(memory_data, f, indent=4)
        # print("[Memory] Memory saved successfully.")
    except Exception as e:
        print(f"[Memory] Failed to save memory: {e}")
