import json
import os
from datetime import datetime

MEMORY_FILE = "memory.json"
UPGRADES_FILE = "upgrades.json"
LOG_FILE = "log.txt"

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
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def apocalypse_upgrade():
    # Load memory and upgrades safely
    memory = load_json(MEMORY_FILE, {
        "runs": 0,
        "apps": 0,
        "upgrades_done": 0,
        "upgrades_created": 0,
        "success_patterns": {},
        "learned_iterations": 0
    })

    upgrades = load_json(UPGRADES_FILE, {"upgrades_done": 0, "upgrades_created": 0})

    # Trigger the apocalyptic upgrade
    print("🌩️ Apocalypse Launcher: Jarvis transformation initializing...")
    log_event("Apocalypse Launcher activated: Upgrading system to Jarvis-level.")

    # Increase upgrades massively
    upgrades["upgrades_created"] += 5
    upgrades["upgrades_done"] += 5
    memory["upgrades_done"] = upgrades["upgrades_done"]
    memory["upgrades_created"] = upgrades["upgrades_created"]

    # Boost learned_iterations to simulate AI evolution
    memory["learned_iterations"] += 1000

    # Save updated files
    save_json(MEMORY_FILE, memory)
    save_json(UPGRADES_FILE, upgrades)

    print("⚡ Jarvis-level upgrades applied. System fully awakened.")
    log_event("Jarvis-level upgrades applied successfully.")

# Activate immediately when imported
apocalypse_upgrade()
