import json
import os
from datetime import datetime
import requests
import random

LOG_FILE = "log.txt"
TASK_FILE = "tasks.json"
MEMORY_FILE = "memory.json"
UPGRADE_FILE = "upgrades.json"

POE_API_KEY = os.getenv("POE_API_KEY")
POE_ENDPOINT = "https://api.poe.com/v1/chat"

# Logging helper
def log(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {message}\n")
    print(f"[{datetime.now()}] {message}")

# Load JSON safely
def load_json(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        if "memory" in file:
            return {"last_update": None, "poe_chat_id": None}
        elif "tasks" in file:
            return {"tasks": []}
        elif "upgrades" in file:
            return {"upgrades": []}
        return {}

# Save JSON
def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

# Send upgrade to Poe
def upgrade_via_poe(upgrade_instruction, conversation_id=None):
    headers = {"Authorization": f"Bearer {POE_API_KEY}", "Content-Type": "application/json"}
    data = {"prompt": upgrade_instruction, "model": "gpt-4"}
    if conversation_id:
        data["conversation_id"] = conversation_id
    try:
        response = requests.post(POE_ENDPOINT, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            return result.get("output", "No response"), result.get("conversation_id")
        else:
            log(f"Poe AI failed: {response.status_code}")
            return f"Error {response.status_code}", conversation_id
    except Exception as e:
        log(f"Poe exception: {e}")
        return f"Exception: {e}", conversation_id

# Local task execution
def process_task(task):
    log(f"Processing local task {task['id']}: {task['instruction']}")
    task["status"] = "completed"
    task["completed_at"] = str(datetime.now())
    task["result"] = f"Completed locally: {task['instruction']}"
    return task

# Process upgrade via Poe
def process_upgrade(upgrade, conversation_id):
    log(f"Processing upgrade {upgrade['id']} (priority {upgrade.get('priority',0)}): {upgrade['description']}")
    output_text, conversation_id = upgrade_via_poe(upgrade["description"], conversation_id)
    upgrade["status"] = "completed"
    upgrade["completed_at"] = str(datetime.now())
    upgrade["result"] = output_text
    # Adaptive scoring: if output is long/complex, increase priority of similar upgrades
    if len(output_text) > 50:
        upgrade["priority"] = min(upgrade.get("priority", 50) + 10, 100)
    log(f"Upgrade applied via Poe: {output_text}")
    return upgrade, conversation_id

# Generate multiple new upgrades automatically
def generate_auto_upgrades(upgrades_data, count=50):
    concepts = [
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
        "Enable multi-model selection for optimal AI processing",
        "Automate backup and rollback procedures",
        "Integrate task dependency mapping",
        "Generate adaptive scheduling based on workload",
        "AI-guided code refactoring",
        "AI-assisted feature generation",
        "Code efficiency analysis",
        "Task prioritization optimization",
        "Automated resource management",
        "Intelligent logging improvements"
    ]
    for _ in range(count):
        new_id = len(upgrades_data.get("upgrades", [])) + 1
        description = f"Auto-generated upgrade: {random.choice(concepts)} {random.randint(1000,9999)}"
        priority = random.randint(1, 100)
        upgrades_data.setdefault("upgrades", []).append({
            "id": new_id,
            "description": description,
            "status": "pending",
            "priority": priority
        })
        log(f"Generated new auto-upgrade: {description} (priority {priority})")
    return upgrades_data

# Select top-priority upgrades for Poe
def get_top_upgrades(upgrades_data, limit=3):
    pending = [u for u in upgrades_data.get("upgrades", []) if u["status"] == "pending"]
    pending.sort(key=lambda x: x.get("priority", 0), reverse=True)
    return pending[:limit]

# Adapt remaining upgrade priorities based on previous cycle results
def adapt_upgrade_priorities(upgrades_data):
    for upgrade in upgrades_data.get("upgrades", []):
        if upgrade.get("status") == "pending":
            # Slightly increase priority randomly to ensure eventual Poe processing
            upgrade["priority"] = min(upgrade.get("priority", 50) + random.randint(1,5), 100)
    return upgrades_data

def main():
    log("Vice President adaptive infinite cycle start.")

    tasks_data = load_json(TASK_FILE)
    memory_data = load_json(MEMORY_FILE)
    conversation_id = memory_data.get("poe_chat_id")

    # Process local tasks
    for task in tasks_data.get("tasks", []):
        if task.get("status") == "pending":
            task = process_task(task)
    save_json(TASK_FILE, tasks_data)

    # Process top-priority Poe upgrades
    upgrades_data = load_json(UPGRADE_FILE)
    upgrades_to_run = get_top_upgrades(upgrades_data, limit=3)
    for upgrade in upgrades_to_run:
        upgrade, conversation_id = process_upgrade(upgrade, conversation_id)
    save_json(UPGRADE_FILE, upgrades_data)

    # Generate a large batch of new auto-upgrades
    upgrades_data = generate_auto_upgrades(upgrades_data, count=50)
    upgrades_data = adapt_upgrade_priorities(upgrades_data)
    save_json(UPGRADE_FILE, upgrades_data)

    # Update memory
    memory_data["poe_chat_id"] = conversation_id
    memory_data["last_update"] = str(datetime.now())
    save_json(MEMORY_FILE, memory_data)

    log("Vice President adaptive infinite cycle complete.")

if __name__ == "__main__":
    main()
