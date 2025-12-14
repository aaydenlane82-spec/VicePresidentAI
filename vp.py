# vp.py
"""
Vice President (VP) AI Runner - fully upgraded
Central runner for Jarvis transformation and all associated scripts
"""

import sys
import os
from apocalypse_launcher import apocalypse_sequence
from memory import load_memory, save_memory

MEMORY_FILE = "memory.json"

def main():
    # Load memory
    memory = load_memory()

    # Increment runs safely
    memory["runs"] += 1
    print(f"[VP] Run #{memory['runs']} starting...")

    # Save early to prevent KeyError if something crashes
    save_memory(memory)

    try:
        # Launch the apocalypse sequence (Jarvis transformation)
        apocalypse_sequence()

        # Update memory after successful run
        memory["upgrades_done"] += 1
        save_memory(memory)

        print("[VP] Run complete. Jarvis is fully upgraded and operational!")
        sys.exit(0)

    except Exception as e:
        print(f"[VP] ERROR during run: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
