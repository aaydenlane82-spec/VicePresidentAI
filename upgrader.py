import json
import os

UPGRADES_FILE = "upgrades.json"

# Ensure upgrades file exists
if not os.path.exists(UPGRADES_FILE):
    with open(UPGRADES_FILE, "w") as f:
        json.dump({"last_upgrade": 0}, f)

def get_upgrade_status():
    with open(UPGRADES_FILE, "r") as f:
        try:
            upgrades = json.load(f)
        except json.JSONDecodeError:
            upgrades = {"last_upgrade": 0}
    return upgrades

def apply_upgrade(level):
    upgrades = get_upgrade_status()
    if upgrades.get("last_upgrade", 0) < level:
        print(f"Applying upgrade {level}...")
        # Add real upgrade logic here
        upgrades["last_upgrade"] = level
        with open(UPGRADES_FILE, "w") as f:
            json.dump(upgrades, f, indent=2)

def check_and_apply_upgrades():
    upgrades = get_upgrade_status()
    current_level = upgrades.get("last_upgrade", 0)
    # Example: auto-apply next upgrade
    apply_upgrade(current_level + 1)
