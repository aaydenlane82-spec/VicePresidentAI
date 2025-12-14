import json
import os
import time
from auto_upgrade import run_upgrades
from self_heal import self_heal

MEMORY_FILE = "memory.json"

# Ensure memory exists
if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump({}, f)

# Load memory safely
with open(MEMORY_FILE, "r") as f:
    try:
        memory = json.load(f)
    except json.JSONDecodeError:
        memory = {}

# Ensure essential keys exist
memory.setdefault("runs", 0)
memory.setdefault("tasks_completed", 0)
memory.setdefault("upgrades_applied", [])

def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

def main_loop():
    while True:
        try:
            # Increment run counter
            memory["runs"] += 1
            print(f"[VP] Run #{memory['runs']} starting...")

            # Run auto-upgrades
            run_upgrades(memory)

            # Self-healing checks
            self_heal(memory)

            # Example task (replace with actual VP logic)
            memory["tasks_completed"] += 1
            print(f"[VP] Completed tasks: {memory['tasks_completed']}")

            # Save memory
            save_memory()

            # Sleep between loops
            time.sleep(10)

        except KeyboardInterrupt:
            print("[VP] Stopping gracefully...")
            save_memory()
            break
        except Exception as e:
            print(f"[VP] Warning: encountered an error: {e}")
            save_memory()
            time.sleep(5)

if __name__ == "__main__":
    print("[VP] Vice President AI starting...")
    main_loop()
