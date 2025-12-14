import json
import os
from datetime import datetime

# Import custom upgrade modules
import apocalypse_launcher  # auto-apocalypse trigger
import auto_upgrade
import bug_killer
import self_heal
import jarvis_core

# File paths
MEMORY_FILE = "memory.json"
TASKS_FILE = "tasks.json"
METRICS_FILE = "metrics.json"
LOG_FILE = "log.txt"

# Utility functions
def load_json(file_path, default):
    if not os.path.exists(file_path):
        return default
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return default

def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

# Initialize memory safely
memory = load_json(MEMORY_FILE, {
    "runs": 0,
    "apps": 0,
    "upgrades_done": 0,
    "upgrades_created": 0,
    "success_patterns": {},
    "learned_iterations": 0
})

# Initialize metrics safely
metrics = load_json(METRICS_FILE, {})

# Main VP logic
def main():
    # Increment runs safely
    if "runs" not in memory:
        memory["runs"] = 0
    memory["runs"] += 1

    log_event(f"Vice President AI run #{memory['runs']} starting...")

    # Self-healing step
    self_heal.heal(memory, METRICS_FILE)

    # Apply auto upgrades
    auto_upgrade.run(memory)

    # Bug-killer sweep
    bug_killer.clean(memory)

    # Jarvis core functions
    jarvis_core.activate(memory)

    # Save memory and metrics after upgrades
    save_json(MEMORY_FILE, memory)
    save_json(METRICS_FILE, metrics)

    log_event("Vice President AI run complete.")

# Entrypoint
if __name__ == "__main__":
    main()
