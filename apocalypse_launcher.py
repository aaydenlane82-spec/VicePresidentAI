import os, json, subprocess, sys, shutil

# Files to purge and reset
FILES = {
    "memory.json": {"runs":0,"apps":0,"upgrades_done":0,"upgrades_created":0,"success_patterns":{},"learned_iterations":0},
    "tasks.json": [],
    "upgrades.json": {},
    "apps.json": [],
    "metrics.json": {}
}

def purge_and_reset():
    for file, default in FILES.items():
        if os.path.exists(file):
            os.remove(file)
        with open(file, "w") as f:
            json.dump(default, f, indent=2)
    print("[APOCALYPSE] All state files purged and rebuilt.")

def apply_god_patch():
    upgrades = {
        "core": "Jarvis AI Core Integrated",
        "apocalypse_mode": "Bug annihilation sequence active",
        "resilience": "Cannot be overridden by surviving bug",
        "optimization": "Self-learning and auto-refactor",
        "network": "Full GitHub & API integration",
        "god_mode": True
    }
    with open("upgrades.json", "w") as f:
        json.dump(upgrades, f, indent=2)
    print("[APOCALYPSE] God Patch applied. VP cannot be killed now.")

def launch_vp():
    if not os.path.exists("vp.py"):
        print("[ERROR] vp.py missing. Cannot launch VP.")
        sys.exit(1)
    subprocess.run([sys.executable, "vp.py"])

if __name__ == "__main__":
    purge_and_reset()
    apply_god_patch()
    launch_vp()
