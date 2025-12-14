import subprocess
import json
import os

# List all scripts to run in order
scripts = [
    "atomic_memory.py",
    "auto_upgrade.py",
    "bug_killer.py",
    "jarvis_conscious_engine.py",
    "jarvis_core.py",
    "jarvis_init.py",
    "jarvis_runtime.py",
    "vp.py"  # vp.py will still have the KeyError but won't stop others
]

def safe_run(script_name):
    try:
        print(f"\n=== Running {script_name} ===")
        subprocess.run(["python", script_name], check=False)
    except Exception as e:
        print(f"Error running {script_name}: {e}")

def main():
    # Optional: initialize memory keys safely
    memory_file = "memory.json"
    if os.path.exists(memory_file):
        with open(memory_file, "r") as f:
            try:
                memory = json.load(f)
            except:
                memory = {}
    else:
        memory = {}

    # Ensure 'runs' key exists to prevent the vp.py crash
    if "runs" not in memory:
        memory["runs"] = 0
        with open(memory_file, "w") as f:
            json.dump(memory, f, indent=4)

    # Run all scripts in order
    for script in scripts:
        safe_run(script)

if __name__ == "__main__":
    main()
