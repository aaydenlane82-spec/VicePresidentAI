import json
import os

UPGRADES_FILE = "upgrades.json"

def run_upgrades(memory):
    # Ensure upgrades.json exists
    if not os.path.exists(UPGRADES_FILE):
        with open(UPGRADES_FILE, "w") as f:
            json.dump({"upgrades_done": 0, "upgrades_created": 0}, f, indent=2)

    # Load upgrades
    try:
        with open(UPGRADES_FILE, "r") as f:
            upgrades = json.load(f)
    except json.JSONDecodeError:
        upgrades = {"upgrades_done": 0, "upgrades_created": 0}

    # Apocalyptic upgrade logic
    if upgrades["upgrades_created"] < 5:
        print("Executing Jarvis-level system upgrades...")
        upgrades["upgrades_created"] += 1
        upgrades["upgrades_done"] += 1
        memory["upgrades_done"] = upgrades["upgrades_done"]
        memory["upgrades_created"] = upgrades["upgrades_created"]

    # Save upgrades file
    with open(UPGRADES_FILE, "w") as f:
        json.dump(upgrades, f, indent=2)
