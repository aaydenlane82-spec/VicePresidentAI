import json
from memory import load_memory, save_memory

UPGRADES_FILE = "upgrades.json"

def apply_all_upgrades(memory=None):
    """
    Apply all pending upgrades from upgrades.json
    """
    if memory is None:
        memory = load_memory()

    try:
        with open(UPGRADES_FILE, "r") as f:
            upgrades = json.load(f)
    except Exception as e:
        print(f"Failed to load upgrades.json: {e}")
        upgrades = []

    applied = memory.get("upgrades_applied", [])

    for upgrade in upgrades:
        if upgrade not in applied:
            print(f"Applying upgrade: {upgrade}")
            try:
                # Here you would put the upgrade logic, e.g., modify memory or scripts
                # For now, just mark it as applied
                applied.append(upgrade)
            except Exception as e:
                print(f"Failed to apply upgrade {upgrade}: {e}")

    memory["upgrades_applied"] = applied
    save_memory(memory)
    print("All upgrades applied.")
