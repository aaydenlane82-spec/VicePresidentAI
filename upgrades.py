import json
import os

UPGRADES_FILE = "upgrades.json"
MEMORY_FILE = "memory.json"

def load_upgrades():
    if not os.path.exists(UPGRADES_FILE):
        return []
    with open(UPGRADES_FILE, "r") as f:
        return json.load(f)

def save_upgrades(upgrades):
    with open(UPGRADES_FILE, "w") as f:
        json.dump(upgrades, f, indent=2)

def apply_upgrades():
    """
    Apply available upgrades from upgrades.json.
    Returns number of upgrades applied this cycle.
    """
    upgrades = load_upgrades()
    if not upgrades:
        return 0

    applied_count = 0
    memory = {}
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            memory = json.load(f)

    for upgrade in upgrades:
        # Skip already applied upgrades
        if upgrade.get("applied", False):
            continue

        try:
            # Example: Upgrade logic (customize as needed)
            print(f"Applying upgrade: {upgrade.get('name', 'Unnamed')}")
            # Mark upgrade as applied
            upgrade["applied"] = True
            applied_count += 1
        except Exception as e:
            print(f"Failed to apply upgrade {upgrade.get('name')}: {e}")

    # Save upgrades back
    save_upgrades(upgrades)
    return applied_count
