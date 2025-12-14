import json
import os
import time

MEMORY_FILE = "memory.json"

DEFAULT_MEMORY = {
    "runs": 0,
    "learned_iterations": 0,
    "errors_fixed": 0,
    "upgrades_applied": 0,
    "last_run": None
}

def load():
    if not os.path.exists(MEMORY_FILE):
        save(DEFAULT_MEMORY.copy())
        return DEFAULT_MEMORY.copy()

    try:
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
    except Exception:
        save(DEFAULT_MEMORY.copy())
        return DEFAULT_MEMORY.copy()

    for k, v in DEFAULT_MEMORY.items():
        if k not in data:
            data[k] = v

    return data

def save(mem):
    with open(MEMORY_FILE, "w") as f:
        json.dump(mem, f, indent=2)

def tick():
    mem = load()
    mem["runs"] += 1
    mem["learned_iterations"] += 1
    mem["last_run"] = time.time()
    save(mem)
    return mem
