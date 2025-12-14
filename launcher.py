import json
import subprocess
import os

MEMORY_FILE = "memory.json"

# Ensure memory.json exists and has a "runs" key
if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump({"runs": 0}, f)

with open(MEMORY_FILE, "r+") as f:
    try:
        memory = json.load(f)
    except json.JSONDecodeError:
        memory = {"runs": 0}

    # Ensure 'runs' key exists
    if "runs" not in memory:
        memory["runs"] = 0

    f.seek(0)
    json.dump(memory, f, indent=2)
    f.truncate()

# Run VP.py safely
subprocess.run(["python", "vp.py"])
