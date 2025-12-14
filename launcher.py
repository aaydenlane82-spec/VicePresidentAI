import subprocess
import time
import json
import os
from datetime import datetime

MEMORY_FILE = "memory.json"
VP_SCRIPT = "vp.py"
LOG_FILE = "launcher_log.txt"

# Ensure memory.json exists and has "runs" key
def init_memory():
    if not os.path.exists(MEMORY_FILE):
        memory = {"runs": 0}
        save_memory(memory)
    else:
        try:
            with open(MEMORY_FILE, "r") as f:
                memory = json.load(f)
            if "runs" not in memory:
                memory["runs"] = 0
                save_memory(memory)
        except json.JSONDecodeError:
            memory = {"runs": 0}
            save_memory(memory)
    return memory

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}"
    print(entry)
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")

def run_vp():
    try:
        result = subprocess.run(["python", VP_SCRIPT], capture_output=True, text=True, check=True)
        log(f"VP finished successfully:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        log(f"VP crashed with error:\n{e.stderr}")

def main():
    memory = init_memory()
    log(f"Launcher started. Current run count: {memory['runs']}")
    
    while True:
        memory['runs'] += 1
        save_memory(memory)
        log(f"Starting VP run #{memory['runs']}...")
        
        run_vp()
        
        log("VP run finished. Sleeping 5 seconds before next run...")
        time.sleep(5)  # Prevents super fast restart loops

if __name__ == "__main__":
    main()
