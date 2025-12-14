import threading
import time
import subprocess

# Functions to run your scripts
def run_vp():
    """Run the main VP script in a loop"""
    while True:
        try:
            subprocess.run(["python", "vp.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"VP crashed: {e}. Restarting...")
        time.sleep(1)  # small delay to avoid spamming

def run_auto_upgrade():
    """Run auto-upgrade continuously"""
    from auto_upgrade import run_auto_upgrade_loop
    while True:
        try:
            run_auto_upgrade_loop()
        except Exception as e:
            print(f"Auto-upgrade crashed: {e}. Restarting...")
        time.sleep(1)

def run_self_heal():
    """Run self-heal continuously"""
    from self_heal import run_self_heal_loop
    while True:
        try:
            run_self_heal_loop()
        except Exception as e:
            print(f"Self-heal crashed: {e}. Restarting...")
        time.sleep(1)

if __name__ == "__main__":
    # Create threads for each component
    vp_thread = threading.Thread(target=run_vp, daemon=True)
    upgrade_thread = threading.Thread(target=run_auto_upgrade, daemon=True)
    heal_thread = threading.Thread(target=run_self_heal, daemon=True)

    # Start all threads
    vp_thread.start()
    upgrade_thread.start()
    heal_thread.start()

    print("Launcher running all systems... Press Ctrl+C to stop.")

    # Keep main thread alive
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Launcher shutting down...")
