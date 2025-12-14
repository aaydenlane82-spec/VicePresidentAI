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

def log(msg):
    line = f"[{datetime.utcnow()}] {msg}"
    print(line)
    with open(LOG, "a") as f:
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

def ensure_memory_keys(memory):
    """Ensure all expected keys exist in memory to prevent KeyErrors"""
    defaults = {
        "runs": 0,
        "apps": 0,
        "upgrades_done": 0,
        "upgrades_created": 0,
        "success_patterns": {},
        "learned_iterations": 0
    }
    for key, value in defaults.items():
        memory.setdefault(key, value)
    return memory

# Add your other functions here (track_metrics, get_ai_suggestions, generate_upgrades, save_app, learn_from_completed, calculate_priority)
# Keep the logic from your previous vp.py intact

def main():
    # === LOAD STATE ===
    memory = load_json("memory.json", {})
    memory = ensure_memory_keys(memory)
    tasks = load_json("tasks.json", {"tasks": []})
    upgrades = load_json("upgrades.json", {"upgrades": []})
    apps = load_json("apps.json", {"apps": []})
    metrics = load_json("metrics.json", {"history": [], "summary": {}, "top_performers": []})

    # === INCREMENT RUN COUNTER ===
    memory["runs"] += 1
    log("="*70)
    log(f"🧠 VP ULTIMATE - RUN #{memory['runs']}")
    log("="*70)

    # === YOUR EXISTING PHASES 1-7 ===
    # Keep the same logic you already have for building apps, processing upgrades, saving metrics, etc.

    # === SAVE STATE ===
    save_json("memory.json", memory)
    save_json("tasks.json", tasks)
    save_json("upgrades.json", upgrades)
    save_json("apps.json", apps)
    save_json("metrics.json", metrics)

    log("="*70)
    log("🚀 VP run complete!")
    log("="*70)

if __name__ == "__main__":
    main()
