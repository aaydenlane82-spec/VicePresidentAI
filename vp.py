import json
import os
import sys
from auto_upgrade import run_upgrades
from self_heal import ensure_memory

# ----- Self-healing memory check -----
MEMORY_FILE = "memory.json"
memory = ensure_memory(MEMORY_FILE)

# ----- Apocalypse Launcher integration -----
try:
    import apocalypse_launcher
except ImportError:
    pass  # optional, just triggers apocalyptic upgrade events

# ----- Auto-upgrades -----
run_upgrades(memory)

# ----- Main VP logic -----
def main():
    memory["runs"] += 1
    print(f"Vice President has run {memory['runs']} times.")
    
    # Placeholder for core AI logic
    print("Jarvis-style VP operational.")
    
    # Save memory after run
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Critical VP error: {e}")
        sys.exit(1)
