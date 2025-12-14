import json
import os

MEMORY_FILE = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        memory = {"runs": 0}
    else:
        try:
            with open(MEMORY_FILE, "r") as f:
                memory = json.load(f)
        except Exception:
            memory = {"runs": 0}
    # Ensure 'runs' key exists
    if "runs" not in memory:
        memory["runs"] = 0
    return memory

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def main():
    memory = load_memory()
    memory["runs"] += 1
    print(f"VP RUN COUNT: {memory['runs']}")
    save_memory(memory)
    print("VP RUN SUCCESSFUL")

if __name__ == "__main__":
    main()
