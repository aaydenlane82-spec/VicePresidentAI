import json, os, requests, random
from datetime import datetime
from github import Github, Auth

# Config
API_KEY = os.getenv("AI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("GITHUB_REPO")
LOG = "log.txt"

# GitHub setup (fixed deprecation warning)
github_client = None
repo = None
if GITHUB_TOKEN and REPO_NAME:
    github_client = Github(auth=Auth.Token(GITHUB_TOKEN))
    repo = github_client.get_repo(REPO_NAME)

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

def log(msg):
    line = f"[{datetime.utcnow()}] {msg}"
    print(line)
    open(LOG, "a").write(line + "\n")

def load_json(file, default):
    try:
        with open(file) as f:
            return json.load(f)
    except:
        return default

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

def commit_to_github(file_path, message):
    if not repo:
        return
    try:
        with open(file_path, "r") as f:
            content = f.read()
        try:
            gh_file = repo.get_contents(file_path)
            repo.update_file(file_path, message, content, gh_file.sha)
        except:
            repo.create_file(file_path, message, content)
        log(f"Committed {file_path} to GitHub.")
    except Exception as e:
        log(f"GitHub commit failed: {e}")

def call_ai(prompt, max_tokens=2000):
    if not API_KEY:
        return "[Demo] Add AI_API_KEY"
    try:
        r = requests.post("https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}], "max_tokens": max_tokens},
            timeout=120)
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        log(f"API Error: {e}")
        return None

def get_ai_suggestions(upgrades, metrics, memory):
    completed = [u for u in upgrades if u.get("status") == "done"][-20:]
    payload = {
        "completed_upgrades": len(completed),
        "total_upgrades": len(upgrades),
        "success_patterns": memory.get("success_patterns", {}),
        "metrics": metrics.get("summary", {})
    }
    prompt = f"""Analyze this VP system and suggest 5 high-impact upgrades:
{json.dumps(payload, indent=2)}
Return ONLY JSON array: [{{"description": "...", "priority": 1-100}}]"""
    result = call_ai(prompt, 1500)
    if result and "[" in result:
        try:
            return json.loads(result[result.index("["):result.rindex("]")+1])
        except:
            pass
    return []

def track_metrics(upgrade, start_time, success, metrics):
    duration = (datetime.utcnow() - start_time).total_seconds()
    entry = {"upgrade_id": upgrade.get("id"), "success": success, "duration": round(duration, 2), "timestamp": datetime.utcnow().isoformat()}
    metrics.setdefault("history", []).append(entry)
    if len(metrics["history"]) > 100:
        metrics["history"] = metrics["history"][-100:]
    all_durations = [m["duration"] for m in metrics["history"]]
    success_count = sum(1 for m in metrics["history"] if m["success"])
    metrics["summary"] = {
        "total_tracked": len(metrics["history"]),
        "success_rate": round(success_count / len(metrics["history"]) * 100, 1),
        "avg_duration": round(sum(all_durations) / len(all_durations), 2)
    }
    return metrics

def learn_from_completed(upgrades, memory):
    completed = [u for u in upgrades if u.get("status") == "done" and u.get("result")]
    patterns = memory.get("success_patterns", {})
    for u in completed[-10:]:
        result = u.get("result", "")
        if result and len(result) > 100:
            for word in u.get("description", "").split():
                if len(word) > 4:
                    patterns[word.lower()] = patterns.get(word.lower(), 0) + 1
    memory["success_patterns"] = patterns
    memory["learned_iterations"] = memory.get("learned_iterations", 0) + 1
    return memory

def calculate_priority(upgrade, memory):
    high_impact = ["parallel", "optimize", "ai", "automate", "predict", "intelligent", "self", "performance", "smart", "adaptive"]
    desc = upgrade.get("description", "").lower()
    score = upgrade.get("priority", 50)
    for kw in high_impact:
        if kw in desc:
            score += 15
    for pattern, count in memory.get("success_patterns", {}).items():
        if pattern in desc:
            score += min(count * 2, 20)
    return min(100, score)

def generate_upgrades(count, start_id, memory):
    upgrades = []
    for i in range(count):
        concept = random.choice(UPGRADE_CONCEPTS)
        upgrade = {"id": start_id + i, "status": "pending", "description": f"{concept} - v{random.randint(100, 9999)}", "priority": random.randint(30, 80), "created_at": datetime.utcnow().isoformat(), "source": "auto_generated"}
        upgrade["priority"] = calculate_priority(upgrade, memory)
        upgrades.append(upgrade)
    return upgrades

def save_app(task, code, apps):
    apps.setdefault("apps", []).append({"id": len(apps.get("apps", [])) + 1, "task_id": task.get("id"), "description": task.get("instruction", "")[:100], "filename": f"app_{task['id']}.html", "size": len(code), "created_at": datetime.utcnow().isoformat()})
    return apps

def main():
    memory = load_json("memory.json", {"runs": 0, "apps": 0, "upgrades_done": 0, "upgrades_created": 0, "success_patterns": {}, "learned_iterations": 0})
    tasks = load_json("tasks.json", {"tasks": []})
    upgrades = load_json("upgrades.json", {"upgrades": []})
    apps = load_json("apps.json", {"apps": []})
    metrics = load_json("metrics.json", {"history": [], "summary": {}, "top_performers": []})
    
    memory["runs"] += 1
    log("=" * 70)
    log(f"🧠 VP ULTIMATE - RUN #{memory['runs']}")
    log("=" * 70)
    
    # Build Apps
    for task in [t for t in tasks["tasks"] if t.get("status") == "pending"][:2]:
        log(f"📱 Building: {task['instruction'][:50]}...")
        code = call_ai(f"Create complete HTML app: {task['instruction']}. Return ONLY HTML.", 3500)
        if code and len(code) > 200:
            if "```" in code:
                code = code.split("```")[1].split("```")[0]
                if code.startswith("html"): code = code[4:]
            os.makedirs("apps", exist_ok=True)
            open(f"apps/app_{task['id']}.html", "w").write(code.strip())
            task["status"] = "done"
            memory["apps"] += 1
            apps = save_app(task, code, apps)
            log(f"✅ Saved: app_{task['id']}.html")
    
    memory = learn_from_completed(upgrades["upgrades"], memory)
    
    # AI Suggestions every 5 runs
    if memory["runs"] % 5 == 0:
        log("🤖 Getting AI suggestions...")
        suggestions = get_ai_suggestions(upgrades["upgrades"], metrics, memory)
        if suggestions:
            max_id = max([u.get("id", 0) for u in upgrades["upgrades"]] + [0])
            for i, s in enumerate(suggestions):
                upgrades["upgrades"].append({"id": max_id + i + 1, "status": "pending", "description": s.get("description", "AI upgrade"), "priority": s.get("priority", 80), "source": "ai_suggested", "created_at": datetime.utcnow().isoformat()})
            log(f"✅ Added {len(suggestions)} AI suggestions")
    
    # Process Top 5 Upgrades
    pending = [u for u in upgrades["upgrades"] if u.get("status") == "pending"]
    for u in pending:
        u["priority"] = calculate_priority(u, memory)
    pending.sort(key=lambda x: x.get("priority", 0), reverse=True)
    
    for upgrade in pending[:5]:
        start_time = datetime.utcnow()
        log(f"⚡ [{upgrade['priority']}pts] #{upgrade['id']}: {upgrade['description'][:40]}...")
        result = call_ai(f"Implement: {upgrade['description']}. Be specific.", 1000)
        success = result is not None and len(result) > 50
        upgrade["status"] = "done"
        upgrade["completed_at"] = datetime.utcnow().isoformat()
        upgrade["result"] = result[:600] if result else "Done"
        memory["upgrades_done"] += 1
        metrics = track_metrics(upgrade, start_time, success, metrics)
        log(f"✅ Done: #{upgrade['id']}")
    
    # Generate 50 New
    max_id = max([u.get("id", 0) for u in upgrades["upgrades"]] + [0])
    new_upgrades = generate_upgrades(50, max_id + 1, memory)
    upgrades["upgrades"].extend(new_upgrades)
    memory["upgrades_created"] += len(new_upgrades)
    log(f"🧠 Generated {len(new_upgrades)} new upgrades")
    
    # Boost old pending
    for u in upgrades["upgrades"]:
        if u.get("status") == "pending":
            u["priority"] = min(u.get("priority", 50) + random.randint(1, 3), 100)
    
    # Save all
    save_json("memory.json", memory)
    save_json("tasks.json", tasks)
    save_json("upgrades.json", upgrades)
    save_json("apps.json", apps)
    save_json("metrics.json", metrics)
    
    # Commit to GitHub
    commit_to_github("upgrades.json", f"VP Run #{memory['runs']}")
    
    pending_count = len([u for u in upgrades["upgrades"] if u.get("status") == "pending"])
    log("=" * 70)
    log(f"📊 Apps={memory['apps']} | Done={memory['upgrades_done']} | Created={memory['upgrades_created']} | Pending={pending_count}")
    log("=" * 70)

if __name__ == "__main__":
    main()
