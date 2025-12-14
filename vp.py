import json, os, requests, random
from datetime import datetime

API_KEY = os.getenv("AI_API_KEY")
LOG = "log.txt"

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

DEFAULT_MEMORY = {
    "runs": 0,
    "apps": 0,
    "upgrades_done": 0,
    "upgrades_created": 0,
    "success_patterns": {},
    "learned_iterations": 0
}

def log(msg):
    line = f"[{datetime.utcnow()}] {msg}"
    print(line)
    open(LOG, "a").write(line + "\n")

def load_json(file, default):
    try:
        with open(file) as f:
            data = json.load(f)
        # ensure all default keys exist
        for k, v in default.items():
            if k not in data:
                data[k] = v
        return data
    except FileNotFoundError:
        return default
    except json.JSONDecodeError:
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

# --- rest of your VP logic remains unchanged ---
# make sure all places where memory["runs"] is used are after loading memory

def main():
    # Load all state
    memory = load_json("memory.json", DEFAULT_MEMORY)
    tasks = load_json("tasks.json", {"tasks": []})
    upgrades = load_json("upgrades.json", {"upgrades": []})
    apps = load_json("apps.json", {"apps": []})
    metrics = load_json("metrics.json", {"history": [], "summary": {}, "top_performers": []})

    # Increment run count safely
    memory["runs"] = memory.get("runs", 0) + 1

    log("=" * 70)
    log(f"🧠 VP ULTIMATE + POE INTEGRATION - RUN #{memory['runs']}")
    log(f"   Apps: {memory.get('apps',0)} | Upgrades Done: {memory.get('upgrades_done',0)} | Patterns: {len(memory.get('success_patterns', {}))}")
    log("=" * 70)

    # --- rest of your main logic ---

    # Save everything at the end
    save_json("memory.json", memory)
    save_json("tasks.json", tasks)
    save_json("upgrades.json", upgrades)
    save_json("apps.json", apps)
    save_json("metrics.json", metrics)
    log("✅ VP run complete.")

if __name__ == "__main__":
    main()
