import os
import json
import requests
from github import Github
import time

# --- Files ---
MEMORY_FILE = "memory.json"
TASKS_FILE = "tasks.json"
UPGRADES_FILE = "upgrades.json"
APPS_FILE = "apps.json"
METRICS_FILE = "metrics.json"
LOG_FILE = "log.txt"
FORCE_RESET_FILE = "force_reset.json"

# --- Helpers ---
def log(message):
    print(message)
    with open(LOG_FILE, "a") as f:
        f.write(f"{time.ctime()}: {message}\n")

def load_json_safe(path, default=None):
    if not os.path.exists(path):
        return default if default is not None else {}
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return default if default is not None else {}

def save_json_safe(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def init_files():
    # Initialize all files with defaults if missing
    defaults = {
        MEMORY_FILE: {
            "runs": 0,
            "apps": 0,
            "upgrades_done": 0,
            "upgrades_created": 0,
            "success_patterns": {},
            "learned_iterations": 0
        },
        TASKS_FILE: [],
        UPGRADES_FILE: {},
        APPS_FILE: [],
        METRICS_FILE: {}
    }
    for file, default in defaults.items():
        if not os.path.exists(file):
            save_json_safe(file, default)

# --- Force reset override ---
if os.path.exists(FORCE_RESET_FILE):
    log("Force reset detected! Applying apocalypse mode.")
    force_reset = load_json_safe(FORCE_RESET_FILE, default={})
    if "memory" in force_reset:
        save_json_safe(MEMORY_FILE, force_reset["memory"])
    if "tasks" in force_reset:
        save_json_safe(TASKS_FILE, force_reset["tasks"])
    if "upgrades" in force_reset:
        save_json_safe(UPGRADES_FILE, force_reset["upgrades"])

init_files()

memory = load_json_safe(MEMORY_FILE)
tasks = load_json_safe(TASKS_FILE)
upgrades = load_json_safe(UPGRADES_FILE)
apps = load_json_safe(APPS_FILE)

# --- Ensure memory keys exist ---
for key, default in {
    "runs": 0,
    "apps": 0,
    "upgrades_done": 0,
    "upgrades_created": 0,
    "success_patterns": {},
    "learned_iterations": 0
}.items():
    if key not in memory:
        memory[key] = default

# --- Main loop ---
def main():
    log("Apocalyptic VP initiated!")
    
    # Count the run
    memory["runs"] += 1
    log(f"Run #{memory['runs']}")

    # Example upgrade logic
    memory["upgrades_created"] += 1
    upgrades[f"upgrade_{memory['upgrades_created']}"] = "God-level upgrade applied"
    memory["upgrades_done"] += 1

    # Example app creation
    apps.append({"id": memory["apps"] + 1, "status": "created"})
    memory["apps"] += 1

    # Save state
    save_json_safe(MEMORY_FILE, memory)
    save_json_safe(APPS_FILE, apps)
    save_json_safe(UPGRADES_FILE, upgrades)

    log("VP Apocalypse cycle complete. Everything upgraded and stabilized!")

if __name__ == "__main__":
    main()
