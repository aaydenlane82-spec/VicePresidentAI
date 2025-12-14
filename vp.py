import json
import os

MEMORY_FILE = "memory.json"

def main():
    print("VP ENTRYPOINT CONFIRMED")

    if not os.path.exists(MEMORY_FILE):
        memory = {"runs": 0}
    else:
        try:
            with open(MEMORY_FILE, "r") as f:
                memory = json.load(f)
        except Exception:
            memory = {"runs": 0}

    if "runs" not in memory:
        memory["runs"] = 0

    memory["runs"] += 1

    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

    print("RUN COUNT:", memory["runs"])
    print("VP EXIT CLEAN")

if __name__ == "__main__":
    main()
