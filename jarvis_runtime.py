# jarvis_runtime.py
import json
import os
from datetime import datetime
import traceback

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
    try:
        if not os.path.exists(MEMORY_FILE):
            return DEFAULT_MEMORY.copy()

        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            return DEFAULT_MEMORY.copy()

        for k, v in DEFAULT_MEMORY.items():
            data.setdefault(k, v)

        return data

    except Exception:
        return DEFAULT_MEMORY.copy()

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def run_jarvis():
    print("[JARVIS] booting")

    memory = load_memory()
    memory["runs"] = int(memory.get("runs", 0)) + 1
    save_memory(memory)

    try:
        import bug_killer
        import self_heal
        import auto_upgrade
        import jarvis_core

        if hasattr(bug_killer, "eliminate_bugs"):
            bug_killer.eliminate_bugs(memory)

        if hasattr(self_heal, "self_healing_system"):
            self_heal.self_healing_system(memory)

        if hasattr(auto_upgrade, "run_upgrades"):
            auto_upgrade.run_upgrades(memory)

        if hasattr(jarvis_core, "JarvisCore"):
            jarvis_core.JarvisCore(memory).initialize_system()

    except Exception:
        print("[JARVIS] caught internal error — system continues")
        traceback.print_exc()

    save_memory(memory)
    print("[JARVIS] cycle complete")
