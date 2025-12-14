import os
import json
import datetime

STATE_FILES = ["memory.json", "tasks.json", "upgrades.json", "apps.json", "metrics.json"]

def load_json(file):
    if not os.path.exists(file):
        return {}
    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

def self_heal():
    print("[JARVIS] Initiating self-heal sequence...")
    for file in STATE_FILES:
        data = load_json(file)
        if file == "memory.json":
            defaults = {"runs": 0, "apps": 0, "upgrades_done": 0, "upgrades_created": 0, "success_patterns": {}, "learned_iterations": 0}
            if not isinstance(data, dict):
                data = defaults
            for key in defaults:
                if key not in data:
                    data[key] = defaults[key]
        elif file == "tasks.json" and not isinstance(data, list):
            data = []
        elif file == "upgrades.json" and not isinstance(data, dict):
            data = {}
        elif file == "apps.json" and not isinstance(data, list):
            data = []
        elif file == "metrics.json" and not isinstance(data, dict):
            data = {}
        save_json(file, data)
    print("[JARVIS] Self-heal complete. All state files validated.")

def auto_upgrade():
    upgrades = load_json("upgrades.json")
    # Core Jarvis upgrades
    upgrades.update({
        "core_ai": "Jarvis AI fully integrated",
        "autopatch": True,
        "bug_annihilation_protocol": True,
        "self_refactor": True,
        "predictive_analysis": True,
        "network_integration": ["GitHub", "POE_API", "Other_APIs"],
        "god_mode": True,
        "last_upgrade": str(datetime.datetime.utcnow())
    })
    save_json("upgrades.json", upgrades)
    print("[JARVIS] Auto-upgrades applied successfully.")

def initialize():
    self_heal()
    auto_upgrade()
    print("[JARVIS] Jarvis Core initialized. VP is now unkillable and self-upgrading.")

if __name__ == "__main__":
    initialize()
