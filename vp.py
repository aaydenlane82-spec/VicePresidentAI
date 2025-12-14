from memory import load_memory, save_memory
import time
import sys

def main():
    # 🔒 ATOMIC, SELF-HEALING MEMORY LOAD
    memory = load_memory()

    # ✅ THIS CAN NEVER FAIL NOW
    memory["runs"] += 1

    # Example system behavior (safe placeholders)
    memory["learned_iterations"] += 1

    save_memory(memory)

    print("VP run successful.")
    print("Runs:", memory["runs"])

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("FATAL VP ERROR:", e)
        sys.exit(1)
