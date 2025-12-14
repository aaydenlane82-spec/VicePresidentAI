import json, os

FILES = ["memory.json", "tasks.json", "upgrades.json", "apps.json"]

def clean_data(file):
    if not os.path.exists(file):
        return
    with open(file, "r") as f:
        data = json.load(f)

    # Remove any invalid keys
    if file == "memory.json":
        valid_keys = ["runs","apps","upgrades_done","upgrades_created","success_patterns","learned_iterations"]
        data = {k:v for k,v in data.items() if k in valid_keys}

    elif file == "upgrades.json":
        # Remove old buggy upgrade states
        for k in ["legacy_bug_state","incomplete_upgrade"]:
            if k in data:
                del data[k]

    with open(file, "w") as f:
        json.dump(data, f, indent=2)

for f in FILES:
    clean_data(f)
