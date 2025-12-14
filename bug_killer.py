import os
import json

MEMORY_FILE = "memory.json"

def heal_if_needed():
    # If memory.json is missing or corrupted, reset it
    if not os.path.exists(MEMORY_FILE):
        print("Memory missing, creating fresh memory.json...")
        with open(MEMORY_FILE, "w") as f:
            json.dump({"runs": 0}, f)
    else:
        try:
            with open(MEMORY_FILE, "r") as f:
                json.load(f)
        except json.JSONDecodeError:
            print("Memory corrupted, resetting...")
            with open(MEMORY_FILE, "w") as f:
                json.dump({"runs": 0}, f)
