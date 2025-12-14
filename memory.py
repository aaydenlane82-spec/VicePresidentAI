from atomic_memory import read_memory, write_memory

def increment_runs():
    memory = read_memory()
    memory["runs"] = memory.get("runs", 0) + 1
    write_memory(memory)
    return memory["runs"]

def get_runs():
    memory = read_memory()
    return memory.get("runs", 0)
