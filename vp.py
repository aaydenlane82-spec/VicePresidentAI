import json
import os
from datetime import datetime

# Paths
MEMORY_FILE = "memory.json"
APPS_FILE = "apps.json"
UPGRADES_FILE = "upgrades.json"
METRICS_FILE = "metrics.json"
LOG_FILE = "log.txt"
TASKS_FILE = "tasks.json"

# Safe JSON load
def load_json_safe(file_path, default=None):
    if default is None:
        default = {}
    try:
        if not os.path.exists(file_path):
            return default
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        log(f"Error loading {file_path}: {e}")
        return default

# Safe JSON save
def save_json_safe(file_path, data):
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        log(f"Error saving {file_path}: {e}")

# Logging
def log(message):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    print(full_message)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(full_message + "\n")
    except:
        pass  # Never fail because of logging

# Initialize or repair memory
def init_memory():
    memory = load_json_safe(MEMORY_FILE, default={
        "runs": 0,
        "apps": 0,
        "upgrades_done": 0,
        "upgrades_created": 0,
        "success_patterns": {},
        "learned_iterations": 0
    })

    # Ensure all keys exist
    defaults = {
        "runs": 0,
        "apps": 0,
        "upgrades_done": 0,
        "upgrades_created": 0,
        "success_patterns": {},
        "learned_iterations": 0
    }
    for key, value in defaults.items():
        if key not in memory:
            memory[key] = value
    return memory

# Apocalyptic upgrade system
def run_upgrades(memory):
    upgrades = load_json_safe(UPGRADES_FILE, default={})
    for upgrade_name, upgrade_info in upgrades.items():
        if not upgrade_info.get("applied", False):
            log(f"Applying upgrade: {upgrade_name}")
            # Here you could dynamically call functions, download modules, etc.
            upgrade_info["applied"] = True
            memory["upgrades_done"] += 1
    save_json_safe(UPGRADES_FILE, upgrades)
    save_json_safe(MEMORY_FILE, memory)

# System metrics tracking
def update_metrics(memory):
    metrics = load_json_safe(METRICS_FILE, default={})
    metrics["last_run"] = datetime.utcnow().isoformat()
    metrics["total_runs"] = memory.get("runs", 0)
    metrics["total_upgrades_done"] = memory.get("upgrades_done", 0)
    save_json_safe(METRICS_FILE, metrics)

# Main VP execution
def main():
    log("=== Vice President AI Apocalypse Starting ===")
    memory = init_memory()
    memory["runs"] += 1
    log(f"Run #{memory['runs']} starting...")

    # Load tasks
    tasks = load_json_safe(TASKS_FILE, default=[])
    log(f"Loaded {len(tasks)} tasks.")

    # Apply upgrades
    run_upgrades(memory)

    # Update metrics
    update_metrics(memory)

    # Placeholder: execute tasks or AI logic here
    for i, task in enumerate(tasks):
        log(f"Executing task {i+1}: {task}")
        memory["apps"] += 1  # Simulate app creation

    save_json_safe(MEMORY_FILE, memory)
    log("=== Vice President AI Apocalypse Finished ===")

if __name__ == "__main__":
    main()
