import os
import json
import time
from threading import Thread
from vp import main as vp_main
from self_heal import self_heal_loop
from auto_upgrade import auto_upgrade_loop

MEMORY_FILE = "memory.json"
LOG_FILE = "log.txt"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"runs": 0, "errors": 0}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def log(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

def run_vp_loop():
    memory = load_memory()
    while True:
        try:
            log("Starting VP cycle...")
            vp_main()  # Runs the main VP code
            memory["runs"] = memory.get("runs", 0) + 1
            save_memory(memory)
            log(f"VP cycle complete. Total runs: {memory['runs']}")
        except Exception as e:
            memory["errors"] = memory.get("errors", 0) + 1
            save_memory(memory)
            log(f"Error in VP: {e}")
        time.sleep(5)  # Adjust interval as needed

def run_self_heal():
    try:
        log("Starting self-heal loop...")
        self_heal_loop()
    except Exception as e:
        log(f"Error in self-heal: {e}")

def run_auto_upgrade():
    try:
        log("Starting auto-upgrade loop...")
        auto_upgrade_loop()
    except Exception as e:
        log(f"Error in auto-upgrade: {e}")

if __name__ == "__main__":
    # Run VP, self-heal, and auto-upgrades in parallel threads
    Thread(target=run_vp_loop, daemon=True).start()
    Thread(target=run_self_heal, daemon=True).start()
    Thread(target=run_auto_upgrade, daemon=True).start()

    log("Launcher started. All systems are running.")
    while True:
        time.sleep(60)  # Keep main thread alive
