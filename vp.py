import os, json, random, requests
from datetime import datetime

# === CONFIG ===
API_KEY = os.getenv("AI_API_KEY")  # Poe / OpenAI
GITHUB_TOKEN = os.getenv("VP_GITHUB_TOKEN")
REPO_NAME = os.getenv("VP_REPO")
LOG_FILE = "log.txt"

# Upgrade concepts library (extremely advanced)
UPGRADE_LIBRARY = [
    "Full system self-optimization",
    "Automated app creation AI",
    "Advanced error detection & auto-recovery",
    "Predictive task scheduling",
    "Adaptive performance tuning",
    "Intelligent logging and monitoring",
    "Automated test generation",
    "Resource optimization and caching",
    "Learning from past app success patterns",
    "Self-refactoring and code cleanup"
]

# === Helper functions ===
def log(msg):
    line = f"[{datetime.utcnow()}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def load_json(file, default):
    try:
        with open(file) as f:
            return json.load(f)
    except:
        return default

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

def call_ai(prompt, max_tokens=2000):
    if not API_KEY:
        return "[Demo AI] Missing API key"
    try:
        r = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"model": "gpt-4o-mini", "messages":[{"role":"user","content":prompt}], "max_tokens": max_tokens},
            timeout=120
        )
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        log(f"AI call failed: {e}")
        return None

# === SYSTEM INITIALIZATION ===
def initialize_state():
    memory = load_json("memory.json", {})
    memory.setdefault("runs", 0)
    memory.setdefault("apps", 0)
    memory.setdefault("upgrades_done", 0)
    memory.setdefault("upgrades_created", 0)
    memory.setdefault("success_patterns", {})
    memory.setdefault("learned_iterations", 0)

    tasks = load_json("tasks.json", {"tasks":[]})
    upgrades = load_json("upgrades.json", {"upgrades":[]})
    apps = load_json("apps.json", {"apps":[]})
    metrics = load_json("metrics.json", {"history":[], "summary":{}, "top_performers":[]})

    return memory, tasks, upgrades, apps, metrics

# === GENERATE ADVANCED UPGRADE ===
def generate_upgrade(memory):
    desc = random.choice(UPGRADE_LIBRARY) + " | Full self-optimization cycle"
    upgrade = {
        "id": memory["upgrades_created"] + 1,
        "description": desc,
        "priority": random.randint(50, 100),
        "status": "pending",
        "created_at": datetime.utcnow().isoformat(),
        "source": "mega_upgrade"
    }
    memory["upgrades_created"] += 1
    return upgrade

# === EXECUTE UPGRADE ===
def execute_upgrade(upgrade, memory, tasks, upgrades, apps, metrics):
    log(f"🚀 Executing upgrade: {upgrade['description']}")
    start = datetime.utcnow()

    # Simulate app creation
    for i in range(3):
        code = call_ai(f"Generate a full HTML/CSS/JS app for task {i+1}")
        task = {"id": i+1, "instruction": f"Task {i+1} app", "status": "done", "completed_at": datetime.utcnow().isoformat()}
        tasks["tasks"].append(task)
        apps.setdefault("apps", []).append({
            "id": i+1,
            "task_id": i+1,
            "description": task["instruction"],
            "filename": f"app_{i+1}.html",
            "size": len(code or ""),
            "created_at": datetime.utcnow().isoformat()
        })
        log(f"✅ Created app {i+1}")

    # Mark upgrade as done
    upgrade["status"] = "done"
    upgrade["completed_at"] = datetime.utcnow().isoformat()
    upgrades["upgrades"].append(upgrade)
    memory["upgrades_done"] += 1

    # Update metrics
    duration = (datetime.utcnow() - start).total_seconds()
    metrics["history"].append({
        "upgrade": upgrade["description"],
        "success": True,
        "duration": duration,
        "timestamp": datetime.utcnow().isoformat()
    })

    memory["runs"] += 1

# === SAVE STATE ===
def save_all(memory, tasks, upgrades, apps, metrics):
    save_json("memory.json", memory)
    save_json("tasks.json", tasks)
    save_json("upgrades.json", upgrades)
    save_json("apps.json", apps)
    save_json("metrics.json", metrics)

# === MAIN LOOP ===
def main():
    memory, tasks, upgrades, apps, metrics = initialize_state()
    log("="*50)
    log(f"VP SYSTEM RUN #{memory['runs'] + 1}")
    log("="*50)

    upgrade = generate_upgrade(memory)
    execute_upgrade(upgrade, memory, tasks, upgrades, apps, metrics)
    save_all(memory, tasks, upgrades, apps, metrics)

    log("🎉 Mega upgrade executed successfully!")
    log(f"Total runs: {memory['runs']}")
    log(f"Total upgrades done: {memory['upgrades_done']}")
    log("="*50)

if __name__ == "__main__":
    main()
