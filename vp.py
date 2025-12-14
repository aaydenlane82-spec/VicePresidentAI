import json
import os
from datetime import datetime

# =========================
# CONFIG
# =========================
MEMORY_FILE = "memory.json"
APPS_FILE = "apps.json"
TASKS_FILE = "tasks.json"
UPGRADES_FILE = "upgrades.json"
METRICS_FILE = "metrics.json"
LOG_FILE = "log.txt"

# =========================
# LOGGING
# =========================
def log(msg):
    line = f"[{datetime.utcnow().isoformat()}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

# =========================
# SAFE JSON IO
# =========================
def load_json_safe(path, default):
    if not os.path.exists(path):
        log(f"{path} missing → creating default")
        save_json_safe(path, default)
        return default.copy()

    try:
        with open(path, "r") as f:
            data = json.load(f)
            if not isinstance(data, type(default)):
                raise ValueError("Invalid JSON type")
            return data
    except Exception as e:
        log(f"{path} corrupted → reset ({e})")
        save_json_safe(path, default)
        return default.copy()

def save_json_safe(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# =========================
# MEMORY IMMUNITY LAYER
# =========================
def normalize_memory(mem):
    """
    This function is the god-slayer.
    No matter what memory.json looks like, this WILL NOT crash.
    """
    defaults = {
        "runs": 0,
        "apps": 0,
        "upgrades_done": 0,
        "upgrades_created": 0,
        "success_patterns": {},
        "learned_iterations": 0
    }

    if not isinstance(mem, dict):
        mem = {}

    for k, v in defaults.items():
        if k not in mem or not isinstance(mem[k], type(v)):
            mem[k] = v

    return mem

# =========================
# VP CORE
# =========================
def vp_cycle(memory, apps, tasks, upgrades, metrics):
    log("VP cycle starting")

    # Absolute safety increment
    memory["runs"] = int(memory.get("runs", 0)) + 1
    log(f"Runs = {memory['runs']}")

    # Generate upgrade
    upgrade_id = memory["upgrades_created"] + 1
    upgrades.append({
        "id": upgrade_id,
        "created_at": datetime.utcnow().isoformat(),
        "applied": True
    })

    memory["upgrades_created"] += 1
    memory["upgrades_done"] += 1

    # Simulate app completion
    memory["apps"] += len(tasks)

    metrics["last_run"] = datetime.utcnow().isoformat()
    metrics["total_runs"] = memory["runs"]
    metrics["total_upgrades"] = memory["upgrades_done"]

    log("VP cycle complete")

# =========================
# MAIN
# =========================
def main():
    log("BOOT")

    memory = load_json_safe(MEMORY_FILE, {})
    memory = normalize_memory(memory)

    apps = load_json_safe(APPS_FILE, [])
    tasks = load_json_safe(TASKS_FILE, [])
    upgrades = load_json_safe(UPGRADES_FILE, [])
    metrics = load_json_safe(METRICS_FILE, {})

    vp_cycle(memory, apps, tasks, upgrades, metrics)

    save_json_safe(MEMORY_FILE, memory)
    save_json_safe(APPS_FILE, apps)
    save_json_safe(TASKS_FILE, tasks)
    save_json_safe(UPGRADES_FILE, upgrades)
    save_json_safe(METRICS_FILE, metrics)

    log("SHUTDOWN OK")

if __name__ == "__main__":
    main()
