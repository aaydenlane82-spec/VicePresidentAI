import json
import time

# ----------------- VP Main -----------------
def main(memory=None):
    """
    memory: dict passed from launcher.py
    """
    if memory is None:
        memory = {"runs": 0}

    # Ensure 'runs' key always exists
    if "runs" not in memory:
        memory["runs"] = 0

    # Example AI loop (replace with your actual logic)
    try:
        print(f"[VP AI] Starting run #{memory['runs']}")
        # Simulate some work
        time.sleep(2)
        print(f"[VP AI] Finished run #{memory['runs']}")

        # Increment run counter
        memory["runs"] += 1

    except Exception as e:
        print(f"[VP AI ERROR]: {e}")

    # The memory dict is modified in-place and saved by launcher.py
    return memory
