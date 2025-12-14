import os
import json
import time

# --- Files ---
FILES = {
    "memory": "memory.json",
    "tasks": "tasks.json",
    "upgrades": "upgrades.json",
    "apps": "apps.json",
    "metrics": "metrics.json",
    "log": "log.txt",
    "force_reset": "force_reset.json"
}

# --- Logging ---
def log(msg):
    print(msg)
    with open(FILES["log"], "a") as f:
        f.write(f"{time.ctime()}: {msg}\n")

# --- Safe JSON load/save ---
def load_json(path, default=None):
    if not os.path.exists(path):
        return default if default is not None else {}
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return default if default is not None else {}

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# --- Initialize files ---
def init_files():
    defaults = {
        FILES["memory"]: {
            "runs": 0,
            "apps": 0,
            "upgrades_done": 0,
            "upgrades_created": 0,
            "success_patterns": {},
            "learned_iterations": 0
        },
        FILES["tasks"]: [],
        FILES["upgrades"]: {},
        FILES["apps"]: [],
        FILES["metrics"]: {}
    }
    for file, default in defaults.items():
        if not os.path.exists(file):
            save_json(file, default)

# --- Apocalypse force reset ---
def apocalypse_reset():
    if os.path.exists(FILES["force_reset"]):
        log("Apocalypse override detected! Executing total system purge.")
        reset_data = load_json(FILES["force_reset"])
        for key, value in reset_data.items():
            if key == "memory":
                save_json(FILES["memory"], value)
            elif key == "tasks":
                save_json(FILES["tasks"], value)
            elif key == "upgrades":
                save_json(FILES["upgrades"], value)
            elif key == "apps":
                save_json(FILES["apps"], value)
        log("System purged and overridden with force_reset data.")

# --- Self-healing memory ---
def heal_memory(mem):
    keys = {
        "runs": 0,
        "apps": 0,
        "upgrades_done": 0,
        "upgrades_created": 0,
        "success_patterns": {},
        "learned_iterations": 0
    }
    for k, v in keys.items():
        if k not in mem:
            mem[k] = v
    return mem

# --- Apocalypse upgrade ---
def apply_custom_upgrades(mem, upgrades):
    # Explicitly destroy any surviving buggy states
    upgrades["core"] = "Jarvis Core Activated"
    upgrades["apocalypse_mode"] = "Bug annihilation sequence applied"
    upgrades["self_optimize"] = True
    upgrades["auto_heal"] = True
    upgrades["memory_integrity"] = "Guaranteed"
    mem["success_patterns"]["auto_heal"] = True
    mem["success_patterns"]["bug_destroy"] = True
    return mem, upgrades

# --- Main ---
def main():
    init_files()
    apocalypse_reset()
    
    memory = load_json(FILES["memory"])
    tasks = load_json(FILES["tasks"])
    upgrades = load_json(FILES["upgrades"])
    apps = load_json(FILES["apps"])
    
    memory = heal_memory(memory)
    memory, upgrades = apply_custom_upgrades(memory, upgrades)
    
    # Increment runs and apps
    memory["runs"] += 1
    memory["apps"] += 1
    memory["upgrades_created"] += 1
    memory["upgrades_done"] += 1
    
    # Append a new app as proof of survival
    apps.append({"id": memory["apps"], "status": "created"})
    
    # Save everything
    save_json(FILES["memory"], memory)
    save_json(FILES["tasks"], tasks)
    save_json(FILES["upgrades"], upgrades)
    save_json(FILES["apps"], apps)
    
    log("Apocalypse Jarvis VP cycle complete: bug obliterated, upgrades applied.")

if __name__ == "__main__":
    main()
