# atomic_memory.py
import json
import os
from threading import Lock

MEMORY_FILE = "memory.json"
lock = Lock()

DEFAULT_MEMORY = {
    "runs": 0,
    "apps": 0,
    "upgrades_done": 0,
    "upgrades_created": 0,
    "success_patterns": {},
    "learned_iterations": 0
}

def load_memory():
    with lock:
        if not os.path.exists(MEMORY_FILE):
            save_memory(DEFAULT_MEMORY)
            return DEFAULT_MEMORY.copy()
        try:
            with open(MEMORY_FILE, "r") as f:
                memory = json.load(f)
        except Exception:
            memory = DEFAULT_MEMORY.copy()
        for key in DEFAULT_MEMORY:
            if key not in memory:
                memory[key] = DEFAULT_MEMORY[key]
        save_memory(memory)
        return memory

def save_memory(memory):
    with lock:
        tmp_file = MEMORY_FILE + ".tmp"
        with open(tmp_file, "w") as f:
            json.dump(memory, f, indent=4)
        os.replace(tmp_file, MEMORY_FILE)
