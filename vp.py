import json
import os

MEMORY_FILE = "memory.json"

# --- Load memory safely ---
if os.path.exists(MEMORY_FILE):
    try:
        with open(MEMORY_FILE, "r") as f:
            memory = json.load(f)
    except json.JSONDecodeError:
        memory = {}
else:
    memory = {}

# --- Ensure all required keys exist ---
defaults = {
    "runs": 0,
    "apps": 0,
    "upgrades_done": 0,
    "upgrades_created": 0,
    "success_patterns": {},
    "learned_iterations": 0
}
for k, v in defaults.items():
    memory.setdefault(k, v)

# --- Increment runs safely ---
memory["runs"] += 1

# --- Save memory back ---
with open(MEMORY_FILE, "w") as f:
    json.dump(memory, f, indent=2)

# --- Rest of your VP code continues here ---
