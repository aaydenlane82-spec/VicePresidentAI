import json, os, shutil

FILES_TO_CHECK = ["memory.json", "upgrades.json", "tasks.json"]

for file in FILES_TO_CHECK:
    try:
        with open(file, "r") as f:
            json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"{file} corrupted/missing. Restoring default.")
        shutil.copy(f"default_files/{file}", file)  # keep default template in repo
