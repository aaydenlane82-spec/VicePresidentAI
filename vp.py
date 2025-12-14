import json
import os
import traceback

# Import all custom modules
import auto_upgrade
import bug_killer
import apocalypse_launcher
import self_heal
import jarvis_core
import jarvis_conscious_engine

MEMORY_FILE = "memory.json"
DEFAULT_MEMORY = {
    "runs": 0,
    "apps": 0,
    "upgrades_done": 0,
    "upgrades_created": 0,
    "success_patterns": {},
    "learned_iterations": 0
}

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "w") as f:
            json.dump(DEFAULT_MEMORY, f, indent=4)
        return DEFAULT_MEMORY.copy()
    else:
        with open(MEMORY_FILE, "r") as f:
            try:
                memory = json.load(f)
            except json.JSONDecodeError:
                memory = DEFAULT_MEMORY.copy()
    # Ensure all keys exist
    for k, v in DEFAULT_MEMORY.items():
        if k not in memory:
            memory[k] = v
    return memory

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

def main():
    memory = load_memory()

    # Increment runs safely
    memory["runs"] += 1
    print(f"[VP] Run count: {memory['runs']}")

    try:
        # Apocalypse-level upgrade system
        print("[VP] Running apocalypse_launcher...")
        apocalypse_launcher.run(memory)

        # Auto upgrade for Jarvis transformation
        print("[VP] Running auto_upgrade...")
        auto_upgrade.run(memory)

        # Bug elimination
        print("[VP] Running bug_killer...")
        bug_killer.run(memory)

        # Self-healing routines
        print("[VP] Running self_heal...")
        self_heal.run(memory)

        # Jarvis consciousness core
        print("[VP] Initializing jarvis_core...")
        jarvis_core.run(memory)

        print("[VP] Activating jarvis_conscious_engine...")
        jarvis_conscious_engine.run(memory)

        print("[VP] All systems operational. VP has evolved into Jarvis.")
        
    except Exception as e:
        print("[VP] ERROR during execution:")
        traceback.print_exc()

    save_memory(memory)
    print("[VP] Memory saved successfully.")

if __name__ == "__main__":
    main()
