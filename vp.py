import json
import os

MEMORY_FILE = "memory.json"

# --- Safe memory handling ---
if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump({"runs": 0}, f)

with open(MEMORY_FILE, "r+") as f:
    try:
        memory = json.load(f)
    except json.JSONDecodeError:
        memory = {"runs": 0}

    # Ensure critical keys exist
    if "runs" not in memory:
        memory["runs"] = 0

# --- Main logic ---
def main():
    memory["runs"] += 1
    print(f"VP has run {memory['runs']} times.")

    # Place all your VP logic here
    # Example: just a dummy loop
    for i in range(3):
        print(f"Running task {i + 1}...")

    # Save memory safely
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

if __name__ == "__main__":
    main()
