import json
import os
import shutil
from datetime import datetime
import vp  # your main AI module

LOG_FILE = "launcher_log.txt"
MEMORY_FILE = "memory.json"
PERSIST_DIR = "persisted_data"

# ----------------- Logging -----------------
def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {msg}"
    print(entry)
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")

# ----------------- Load Memory -----------------
if not os.path.exists(PERSIST_DIR):
    os.makedirs(PERSIST_DIR)

memory_path = os.path.join(PERSIST_DIR, MEMORY_FILE)
if os.path.exists(memory_path):
    with open(memory_path, "r") as f:
        memory = json.load(f)
    log("Loaded persisted memory.")
else:
    memory = {"runs": 0}
    log("Starting fresh memory.")

# ----------------- Run AI -----------------
try:
    memory["runs"] += 1
    log(f"Running VP AI - Run #{memory['runs']}")
    vp.main(memory)  # Pass memory to your VP AI

except Exception as e:
    log(f"ERROR: {e}")

finally:
    # Save memory locally and in persist folder for GitHub Actions artifact
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

    shutil.copy(MEMORY_FILE, os.path.join(PERSIST_DIR, MEMORY_FILE))
    log("Memory saved and persisted.")
