import json
import os
from auto_upgrade import check_and_apply_upgrades
from bug_killer import heal_if_needed

MEMORY_FILE = "memory.json"

# --- Initialize safe memory ---
if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump({"runs": 0}, f)

with open(MEMORY_FILE, "r+") as f:
    try:
        memory = json.load(f)
    except json.JSONDecodeError:
        memory = {"runs": 0}

    if "runs" not in memory:
        memory["runs"] = 0

# --- Main logic ---
def main():
    memory["runs"] += 1
    print(f"VP has run {memory['runs']} times.")

    # --- Run bug healer ---
    heal_if_needed()

    # --- Apply upgrades ---
    check_and_apply_upgrades()

    # --- Your main VP logic ---
    for i in range(3):
        print(f"Running task {i+1}...")

    # --- Save memory ---
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

if __name__ == "__main__":
    main()
