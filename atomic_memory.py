import json
import threading

MEMORY_FILE = "memory.json"
_lock = threading.Lock()

def read_memory():
    with _lock:
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"runs": 0}

def write_memory(data):
    with _lock:
        with open(MEMORY_FILE, "w") as f:
            json.dump(data, f, indent=2)
