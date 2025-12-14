import json, os, time

FILES = ["memory.json", "tasks.json", "upgrades.json", "apps.json", "metrics.json"]

DEFAULTS = {
    "memory.json": {
        "runs": 0,
        "apps": 0,
        "upgrades_done": 0,
        "upgrades_created": 0,
        "success_patterns": {},
        "learned_iterations": 0
    },
    "tasks.json": [],
    "upgrades.json": {},
    "apps.json": [],
    "metrics.json": {}
}

def log(msg):
    print(f"[SELF-HEAL] {msg}")

for f in FILES:
    if not os.path.exists(f):
        log(f"{f} missing, regenerating...")
        with open(f, "w") as file:
            json.dump(DEFAULTS[f], file, indent=2)
    else:
        try:
            with open(f, "r") as file:
                data = json.load(file)
        except:
            log(f"{f} corrupted, restoring default.")
            with open(f, "w") as file:
                json.dump(DEFAULTS[f], file, indent=2)
