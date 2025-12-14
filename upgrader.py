import json
import os

def run_upgrades():
    upgrades_file = "upgrades.json"

    # Load existing upgrades or create new
    if os.path.exists(upgrades_file):
        try:
            with open(upgrades_file, "r") as f:
                upgrades = json.load(f)
        except Exception as e:
            print(f"Error loading upgrades.json: {e}")
            upgrades = {}
    else:
        upgrades = {}

    # Example upgrade logic: increment total_upgrades counter
    if "total_upgrades" not in upgrades:
        upgrades["total_upgrades"] = 0
    upgrades["total_upgrades"] += 1

    # You can add other upgrades logic here, e.g., flags for modules, enhancements, etc.
    # Example:
    upgrades["last_upgrade_module"] = "upgrader.py"

    # Save upgrades back to file
    try:
        with open(upgrades_file, "w") as f:
            json.dump(upgrades, f, indent=4)
        print("Upgrades applied successfully.")
    except Exception as e:
        print(f"Error saving upgrades.json: {e}")

if __name__ == "__main__":
    run_upgrades()
