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

# --- FIXED MEMORY LOADING ---
def load_memory():
    memory = load_json("memory.json", {})
    memory.setdefault("runs", 0)
    memory.setdefault("apps", 0)
    memory.setdefault("upgrades_done", 0)
    memory.setdefault("upgrades_created", 0)
    memory.setdefault("success_patterns", {})
    memory.setdefault("learned_iterations", 0)
    return memory

def main():
    memory = load_memory()
    memory["runs"] += 1
    log(f"🧠 VP RUN #{memory['runs']} STARTED")
    # ... rest of your main vp.py code continues as before ...
    # Make sure everywhere memory["runs"] or other keys are used, you have them set by default
    # You can copy the rest of your original main() content here

if __name__ == "__main__":
    main()
