import json, os
from datetime import datetime

# --- Files ---
MEMORY_FILE = "memory.json"
APPS_FILE = "apps.json"
TASKS_FILE = "tasks.json"
UPGRADES_FILE = "upgrades.json"
METRICS_FILE = "metrics.json"
LOG_FILE = "log.txt"

# --- Logging ---
def log(msg):
    line = f"[{datetime.utcnow()}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

# --- JSON helpers ---
def load_json(file, default):
    if not os.path.exists(file):
        log(f"⚠️ {file} missing, creating default")
        save_json(file, default)
        return default
    try:
        with open(file, "r") as f:
            return json.load(f)
    except Exception as e:
        log(f"⚠️ Failed to load {file}: {e}")
        save_json(file, default)
        return default

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

# --- VP Core ---
def vp_cycle(memory, apps, tasks, upgrades, metrics):
    log("🧠 Starting VP adaptive cycle...")

    # Safe increment of runs
    memory["runs"] = memory.get("runs", 0) + 1
    log(f"🔹 Incremented runs: {memory['runs']}")

    # Simulate generating upgrades
    new_upgrade_id = memory.get("upgrades_created", 0) + 1
    new_upgrade = {
        "id": new_upgrade_id,
        "description": f"Auto-upgrade generated at run {memory['runs']}",
        "priority": new_upgrade_id % 100
    }
    upgrades.append(new_upgrade)
    memory["upgrades_created"] = new_upgrade_id
    log(f"✨ Generated new upgrade: {new_upgrade['description']} (priority {new_upgrade['priority']})")

    # Apply upgrades
    applied_upgrades = 0
    for u in upgrades:
        if not u.get("applied", False):
            u["applied"] = True
            memory["upgrades_done"] = memory.get("upgrades_done", 0) + 1
            applied_upgrades += 1
    log(f"🔧 Applied {applied_upgrades} upgrades")

    # Complete tasks
    for t in tasks:
        if not t.get("completed", False):
            t["completed"] = True
            memory["apps"] = memory.get("apps", 0) + 1
    log(f"📌 Completed tasks, total apps: {memory['apps']}")

    # Update metrics
    metrics["last_run"] = str(datetime.utcnow())
    metrics["total_runs"] = memory["runs"]
    metrics["total_upgrades"] = memory["upgrades_done"]

    log("✅ VP cycle complete.")
    return memory, apps, tasks, upgrades, metrics

# --- Main ---
def main():
    # Required memory keys
    required_memory_keys = {
        "runs": 0,
        "apps": 0,
        "upgrades_done": 0,
        "upgrades_created": 0,
        "success_patterns": {},
        "learned_iterations": 0
    }

    # Load memory
    memory = load_json(MEMORY_FILE, required_memory_keys)
    for k, v in required_memory_keys.items():
        if k not in memory:
            log(f"⚠️ Key '{k}' missing, initializing")
            memory[k] = v

    # Load other JSON files
    apps = load_json(APPS_FILE, [])
    tasks = load_json(TASKS_FILE, [])
    upgrades = load_json(UPGRADES_FILE, [])
    metrics = load_json(METRICS_FILE, {})

    log(f"📝 Memory: {memory}")
    log(f"📝 Loaded {len(apps)} apps, {len(tasks)} tasks, {len(upgrades)} upgrades")

    # Run VP cycle
    memory, apps, tasks, upgrades, metrics = vp_cycle(memory, apps, tasks, upgrades, metrics)

    # Save all
    save_json(MEMORY_FILE, memory)
    save_json(APPS_FILE, apps)
    save_json(TASKS_FILE, tasks)
    save_json(UPGRADES_FILE, upgrades)
    save_json(METRICS_FILE, metrics)
    log("💾 All data saved successfully.")

if __name__ == "__main__":
    main()
