import json
import os
import time

# ------------------------------
# Config
# ------------------------------
MEMORY_FILE = "memory.json"

# ------------------------------
# Safe Memory Loader
# ------------------------------
def safe_memory_load(file=MEMORY_FILE):
    defaults = {
        "runs": 0,
        "apps": 0,
        "upgrades_done": 0,
        "upgrades_created": 0,
        "success_patterns": {},
        "learned_iterations": 0
    }
    # Create file if it doesn't exist
    if not os.path.exists(file):
        memory = defaults.copy()
        with open(file, "w") as f:
            json.dump(memory, f, indent=2)
    else:
        with open(file, "r") as f:
            try:
                memory = json.load(f)
            except json.JSONDecodeError:
                memory = defaults.copy()
    # Ensure all keys exist
    for k, v in defaults.items():
        if k not in memory:
            memory[k] = v
    return memory

# ------------------------------
# Main VP Function
# ------------------------------
def main():
    memory = safe_memory_load()
    
    # Increment runs safely
    memory["runs"] += 1
    print(f"[VP] Run number: {memory['runs']}")

    # Simulate some operations for Jarvis
    print("[VP] Performing system upgrades and checks...")
    memory["upgrades_done"] += 1
    memory["learned_iterations"] += 1

    # Save memory
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

    print("[VP] Upgrade complete. Memory saved.")
    time.sleep(1)  # Simulate runtime

# ------------------------------
# Entry Point
# ------------------------------
if __name__ == "__main__":
    main()
