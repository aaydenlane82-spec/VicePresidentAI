def fix_critical_bugs(memory):
    """
    Fix known persistent bugs that crash VP
    """
    print("Running critical bug fixes...")

    # Ensure 'runs' key exists
    if "runs" not in memory:
        print("Fixing missing 'runs' key...")
        memory["runs"] = 0

    # Ensure 'tasks' key exists
    if "tasks" not in memory:
        print("Fixing missing 'tasks' key...")
        memory["tasks"] = []

    # Ensure 'metrics' key exists
    if "metrics" not in memory:
        print("Fixing missing 'metrics' key...")
        memory["metrics"] = {}

    print("Critical bugs fixed.")
