import os
import time
import subprocess
from auto_upgrade import apply_all_upgrades
from bug_killer import fix_critical_bugs
from memory import load_memory, save_memory

def self_heal():
    """
    Fix stuck memory keys, force upgrades, and critical bug fixes
    """
    print("Running self-heal sequence...")
    memory = load_memory()

    # Fix missing or corrupted keys
    if "runs" not in memory:
        memory["runs"] = 0
    if "upgrades_applied" not in memory:
        memory["upgrades_applied"] = []

    # Force bug fixes
    fix_critical_bugs(memory)

    # Apply all upgrades
    apply_all_upgrades(memory)

    save_memory(memory)
    print("Self-heal complete.")

def run_vp():
    """
    Runs the VP main script
    """
    while True:
        try:
            # First run self-heal
            self_heal()
            
            # Run main VP script
            subprocess.run(["python", "vp.py"], check=True)
        except Exception as e:
            print(f"VP crashed: {e}")
            print("Restarting in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    run_vp()
