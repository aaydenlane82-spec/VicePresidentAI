import json
import os
from launcher import run_launcher
from upgrader import run_upgrades

MEMORY_FILE = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"runs": 0}
    with open(MEMORY_FILE, "r") as f:
        try:
            memory = json.load(f)
        except json.JSONDecodeError:
            memory = {"runs": 0}
    # Make sure "runs" key exists
    if "runs" not in memory:
        memory["runs"] = 0
    return memory

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def main():
    memory = load_memory()
    memory["runs"] += 1
    save_memory(memory)

    print(f"[VP] Run count: {memory['runs']}")

    # Run the launcher and upgrades
    run_launcher()
    run_upgrades()

if __name__ == "__main__":
    main()
