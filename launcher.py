import subprocess
import time

VP_SCRIPT = "vp.py"
RESTART_DELAY = 2  # seconds between restarts

def run_vp_loop():
    while True:
        try:
            print("Launching VP...")
            result = subprocess.run(["python", VP_SCRIPT], check=True)
        except subprocess.CalledProcessError as e:
            print(f"VP crashed with error: {e}. Restarting in {RESTART_DELAY} seconds...")
        except KeyboardInterrupt:
            print("Launcher stopped by user.")
            break
        time.sleep(RESTART_DELAY)

if __name__ == "__main__":
    run_vp_loop()
