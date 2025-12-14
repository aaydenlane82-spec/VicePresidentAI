import time
from bug_killer import fix_bugs
from jarvis_runtime import check_system

def self_heal_loop():
    while True:
        try:
            # Check VP & system health
            check_system()
            
            # Attempt to fix persistent bugs
            fix_bugs()
        except Exception as e:
            print(f"Error in self-heal: {e}")
        time.sleep(15)  # Adjust interval for self-heal
