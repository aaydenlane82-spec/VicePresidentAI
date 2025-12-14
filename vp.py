import json, os
from datetime import datetime

# --- Files ---
MEMORY_FILE = "memory.json"
APPS_FILE = "apps.json"
TASKS_FILE = "tasks.json"
UPGRADES_FILE = "upgrades.json"
METRICS_FILE = "metrics.json"
LOG_FILE = "log.txt"

# --- Logging ---
def log(msg):
    line = f"[{datetime.utcnow()}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

# --- JSON helpers ---
def load_json(file, default
