import json
import os
import subprocess
import time
from threading import Thread

UPGRADES_FILE = "upgrades.json"
VP_SCRIPT = "vp.py"
CHECK_INTERVAL = 60  # seconds

def load_upgrades():
    if not os.path.exists(UPGRADES_FILE):
        return {}
    with open(UPGRADES_FILE, "r") as f:
        return json.load(f)

def save_upgrades(upgrades):
    with open(UPGRADES_FILE, "w") as f:
        json.dump(upgrades, f, indent=4)

def apply_upgrade(upgrade_name, upgrade_command):
    try:
        print(f"[AutoUpgrade] Applying upgrade: {upgrade_name}")
        subprocess.run(upgrade_command, shell=True, check=True)
        upgrades = load_upgrades()
        upgrades[upgrade_name] = "applied"
        save_upgrades(upgrades)
        print(f"[AutoUpgrade] Upgrade {upgrade_name} applied successfully")
    except subprocess.CalledProcessError as e:
        print(f"[AutoUpgrade] Failed to apply {upgrade_name}: {e}")

def upgrade_loop():
    while True:
        upgrades = load_upgrades()
        for name, status in upgrades.items():
            if status != "applied" and "command" in upgrades[name]:
                apply_upgrade(name, upgrades[name]["command"])
        time.sleep(CHECK_INTERVAL)

def start_auto_upgrade():
    thread = Thread(target=upgrade_loop, daemon=True)
    thread.start()
    print("[AutoUpgrade] Auto-upgrade thread started")

if __name__ == "__main__":
    start_auto_upgrade()
    # Optional: keep the script alive for testing
    while True:
        time.sleep(30)
