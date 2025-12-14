import json
import os
import time
from threading import Thread

CRITICAL_FILES = {
    "memory.json": {},
    "upgrades.json": {},
    "tasks.json": [],
    "metrics.json": {}
}

CHECK_INTERVAL = 30  # seconds

def ensure_file(filename, default_content):
    """Ensure the file exists and contains valid JSON."""
    if not os.path.exists(filename):
        print(f"[SelfHeal] {filename} missing. Recreating...")
        with open(filename, "w") as f:
            json.dump(default_content, f, indent=4)
        return

    try:
        with open(filename, "r") as f:
            json.load(f)
    except json.JSONDecodeError:
        print(f"[SelfHeal] {filename} corrupted. Resetting...")
        with open(filename, "w") as f:
            json.dump(default_content, f, indent=4)

def self_heal_loop():
    """Continuously check and repair critical files."""
    while True:
        for filename, default_content in CRITICAL_FILES.items():
            ensure_file(filename, default_content)
        time.sleep(CHECK_INTERVAL)

def start_self_heal():
    thread = Thread(target=self_heal_loop, daemon=True)
    thread.start()
    print("[SelfHeal] Self-heal monitoring started")

if __name__ == "__main__":
    start_self_heal()
    # Optional: keep alive for testing
    while True:
        time.sleep(30)
