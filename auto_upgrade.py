import json
import os

UPGRADES_FILE = "upgrades.json"

def check_and_apply_upgrades():
    if not os.path.exists(UPGRADES_FILE):
        with open(UPGRADES_FILE, "w") as f:
            json.dump({"last_upgrade": 0}, f)

    with open(UPGRADES_FILE, "r+") as f:
        try:
            upgrades = json.load(f)
        except json.JSONDecodeError:
            upgrades = {"last_upgrade": 0}

        # Example upgrade logic
        if upgrades.get("last_upgrade", 0) < 1:
            print("Applying first upgrade...")
            upgrades["last_upgrade"] = 1

        with open(UPGRADES_FILE, "w") as f:
            json.dump(upgrades, f, indent=2)
