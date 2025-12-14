memory = load_json("memory.json", {})

# Ensure all required keys exist (prevents KeyError)
memory.setdefault("runs", 0)
memory.setdefault("apps", 0)
memory.setdefault("upgrades_done", 0)
memory.setdefault("upgrades_created", 0)
memory.setdefault("success_patterns", {})
memory.setdefault("learned_iterations", 0)
