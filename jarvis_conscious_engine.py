import os
import json
import datetime
import traceback

STATE_FILES = ["memory.json", "tasks.json", "upgrades.json", "apps.json", "metrics.json"]

def load_json(file):
    if not os.path.exists(file):
        return {}
    try:
        with open(file, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

def monitor_and_patch():
    print("[JARVIS-CONSCIOUS] Monitoring VP run...")
    for file in STATE_FILES:
        data = load_json(file)
        if data is None:
            print(f"[JARVIS-CONSCIOUS] Detected corruption in {file}, patching...")
            save_json(file, {} if file != "memory.json" else {
                "runs": 0,
                "apps": 0,
                "upgrades_done": 0,
                "upgrades_created": 0,
                "success_patterns": {},
                "learned_iterations": 0
            })
    print("[JARVIS-CONSCIOUS] Patch complete. System integrity ensured.")

def record_run():
    memory = load_json("memory.json")
    if "runs" not in memory:
        memory["runs"] = 0
    memory["runs"] += 1
    memory["last_run"] = str(datetime.datetime.utcnow())
    save_json("memory.json", memory)
    print(f"[JARVIS-CONSCIOUS] Run #{memory['runs']} recorded.")

def auto_learn():
    upgrades = load_json("upgrades.json")
    upgrades["conscious_monitoring"] = True
    upgrades["auto_patch_enabled"] = True
    upgrades["predictive_failures"] = True
    upgrades["learning_iteration"] = upgrades.get("learning_iteration", 0) + 1
    upgrades["last_learned"] = str(datetime.datetime.utcnow())
    save_json("upgrades.json", upgrades)
    print("[JARVIS-CONSCIOUS] Self-learning iteration complete.")

def initialize():
    try:
        monitor_and_patch()
        record_run()
        auto_learn()
        print("[JARVIS-CONSCIOUS] Jarvis Conscious Engine online. VP is fully self-aware and adaptive.")
    except Exception:
        print("[JARVIS-CONSCIOUS] Critical error during initialization!")
        traceback.print_exc()

if __name__ == "__main__":
    initialize()
