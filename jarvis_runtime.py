# jarvis_runtime.py
import json
import os
import traceback
from datetime import datetime

MEMORY_FILE = "memory.json"

DEFAULT_MEMORY = {
    "runs": 0,
    "apps": 0,
    "upgrades_done": 0,
    "upgrades_created": 0,
    "success_patterns": {},
    "learned_iterations": 0
}

def safe_load_memory():
    try:
        if not os.path.exists(MEMORY_FILE):
            return DEFAULT_MEMORY.copy()

        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            return DEFAULT_MEMORY.copy()

        # HARD PATCH — force all keys
        for k, v in DEFAULT_MEMORY.items():
            if k not in data:
                data[k] = v

        return data

    except Exception:
        return DEFAULT_MEMORY.copy()

def safe_save_memory(memory):
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(memory, f, indent=2)
    except Exception:
        pass

def run_jarvis():
    print("[JARVIS] Boot sequence initiated")

    memory = safe_load_memory()
    memory["runs"] = int(memory.get("runs", 0)) + 1
    safe_save_memory(memory)

    print(f"[JARVIS] Run #{memory['runs']}")

    # ---- SYSTEM EXECUTION ----
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
            jc = jarvis_core.JarvisCore(memory)
            jc.initialize_system()

    except Exception as e:
        print("[JARVIS] System fault detected — isolating failure")
        traceback.print_exc()

    # ---- FINAL SAVE ----
    safe_save_memory(memory)
    print("[JARVIS] Cycle complete. System stable.")
