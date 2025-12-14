import json
import os

def ensure_memory(file_path="memory.json"):
    default_memory = {
        "runs": 0,
        "apps": 0,
        "upgrades_done": 0,
        "upgrades_created": 0,
        "success_patterns": {},
        "learned_iterations": 0
    }
    
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump(default_memory, f, indent=2)
        return default_memory

    try:
        with open(file_path, "r") as f:
            memory = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        memory = default_memory

    # Ensure all keys exist
    for key, value in default_memory.items():
        if key not in memory:
            memory[key] = value

    with open(file_path, "w") as f:
        json.dump(memory, f, indent=2)
    
    return memory
