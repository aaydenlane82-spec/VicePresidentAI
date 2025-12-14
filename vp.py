import json, os, requests, random
from datetime import datetime

# ====== CONFIG ======
API_KEY = os.getenv("AI_API_KEY")          # Your OpenAI / Poe API Key
GITHUB_TOKEN = os.getenv("VP_GITHUB_TOKEN")
GITHUB_REPO = os.getenv("VP_REPO")         # Format: "username/repo"
LOG_FILE = "log.txt"

UPGRADE_CONCEPTS = [
    "Improve AI task scheduling efficiency",
    "Enhance logging detail and structure",
    "Generate automated helper scripts",
    "Refactor existing modules for performance",
    "Create predictive analytics for task success",
    "Optimize resource usage in app modules",
    "Generate automated testing scenarios",
    "Suggest new modular app features",
    "Improve error detection and debugging",
    "Create self-improvement plan for VP",
    "Enable multi-model selection for optimal AI",
    "Automate backup and rollback procedures",
    "Integrate task dependency mapping",
    "Generate adaptive scheduling based on workload",
    "AI-guided code refactoring",
    "Implement intelligent caching system",
    "Build automated code review pipeline",
    "Create smart error recovery system",
    "Implement parallel task execution",
    "Build predictive failure detection",
    "Create automated documentation generator",
    "Implement smart resource allocation",
    "Build continuous performance monitoring",
    "Create adaptive learning from successes",
    "Implement intelligent upgrade prioritization",
    "Build automated security scanning",
    "Create smart API optimization",
    "Implement modular component system",
    "Build automated testing framework",
    "Create intelligent logging analysis"
]

# ====== UTILITY FUNCTIONS ======
def log(msg):
    line = f"[{datetime.utcnow()}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def load_json(file, default):
    try:
        with open(file) as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return default
            return data
    except:
        return default

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

def call_ai(prompt, max_tokens=2000):
    if not API_KEY:
        return "[Demo] Add AI_API_KEY"
    try:
        r = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}], "max_tokens": max_tokens},
            timeout=120
        )
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        log(f"API Error: {e}")
        return None

# ====== MEMORY INITIALIZATION ======
memory = load_json("memory.json", {
    "runs": 0,
    "apps": 0,
    "upgrades_done": 0,
    "upgrades_created": 0,
    "success_patterns": {},
    "learned_iterations": 0
})

# Ensure all keys exist
for key in ["runs", "apps", "upgrades_done", "upgrades_created", "success_patterns", "learned_iterations"]:
    memory.setdefault(key, 0 if key != "success_patterns" else {})

# ====== MAIN LOGIC ======
def main():
    global memory
    # Load state files
    tasks = load_json("tasks.json", {"tasks": []})
    upgrades = load_json("upgrades.json", {"upgrades": []})
    apps = load_json("apps.json", {"apps": []})
    metrics = load_json("metrics.json", {"history": [], "summary": {}, "top_performers": []})

    memory["runs"] += 1
    log("="*70)
    log(f"🧠 VP ULTIMATE + POE INTEGRATION - RUN #{memory['runs']}")
    log(f"   Apps: {memory['apps']} | Upgrades Done: {memory['upgrades_done']} | Patterns: {len(memory['success_patterns'])}")
    log("="*70)

    # === PHASE 1: Build Apps ===
    pending_tasks = [t for t in tasks["tasks"] if t.get("status") == "pending"][:2]
    for task in pending_tasks:
        log(f"📱 Building: {task.get('instruction','')[:50]}...")
        code = call_ai(f"Create complete HTML app: {task.get('instruction','')}. Return ONLY HTML with CSS/JS.", 3500)
        if code:
            if "```" in code:
                code = code.split("```")[1].split("```")[0]
                if code.startswith("html"): code = code[4:]
            os.makedirs("apps", exist_ok=True)
            filename = f"apps/app_{task['id']}.html"
            with open(filename, "w") as f:
                f.write(code.strip())
            task["status"] = "done"
            task["completed_at"] = datetime.utcnow().isoformat()
            memory["apps"] += 1
            apps.setdefault("apps", []).append({
                "id": len(apps.get("apps", [])) + 1,
                "task_id": task.get("id"),
                "description": task.get("instruction", "")[:100],
                "filename": filename,
                "size": len(code),
                "created_at": datetime.utcnow().isoformat()
            })
            log(f"✅ Saved: {filename}")

    # === PHASE 2: Learn from completed upgrades ===
    completed = [u for u in upgrades["upgrades"] if u.get("status") == "done" and u.get("result")]
    patterns = memory.get("success_patterns", {})
    for u in completed[-10:]:
        result = u.get("result", "")
        if result and len(result) > 100:
            for word in u.get("description", "").split():
                if len(word) > 4:
                    patterns[word.lower()] = patterns.get(word.lower(), 0) + 1
    memory["success_patterns"] = patterns
    memory["learned_iterations"] = memory.get("learned_iterations", 0) + 1

    # === PHASE 3: Generate new upgrades ===
    max_id = max([u.get("id", 0) for u in upgrades["upgrades"]] + [0])
    new_upgrades = []
    for i in range(50):
        concept = random.choice(UPGRADE_CONCEPTS)
        upg = {
            "id": max_id + i + 1,
            "status": "pending",
            "description": f"{concept} - v{random.randint(100,9999)}",
            "priority": random.randint(30, 80),
            "created_at": datetime.utcnow().isoformat(),
            "source": "auto_generated"
        }
        # Boost priority if pattern matches
        for pattern, count in memory["success_patterns"].items():
            if pattern in upg["description"].lower():
                upg["priority"] += min(count*2, 20)
        upg["priority"] = min(upg["priority"], 100)
        new_upgrades.append(upg)
    upgrades["upgrades"].extend(new_upgrades)
    memory["upgrades_created"] += len(new_upgrades)
    log(f"🧠 Generated {len(new_upgrades)} new upgrades")

    # === PHASE 4: Save all state files ===
    save_json("memory.json", memory)
    save_json("tasks.json", tasks)
    save_json("upgrades.json", upgrades)
    save_json("apps.json", apps)
    save_json("metrics.json", metrics)

    log(f"🚀 VP + Poe cycle complete. Run #{memory['runs']} finished.")
    log("="*70)

if __name__ == "__main__":
    main()
