import subprocess
import time
import sys
import os

VP_SCRIPT = "vp.py"

def run_vp():
    while True:
        try:
            print("[Launcher] Starting VP...")
            # Run vp.py in a subprocess
            process = subprocess.Popen([sys.executable, VP_SCRIPT])

            # Wait for the process to finish
            process.wait()
            
            # Check exit code
            if process.returncode != 0:
                print(f"[Launcher] VP crashed with exit code {process.returncode}. Restarting in 5s...")
            else:
                print("[Launcher] VP exited normally. Restarting in 5s...")

        except Exception as e:
            print(f"[Launcher] Error running VP: {e}. Restarting in 5s...")

        time.sleep(5)

if __name__ == "__main__":
    # Optional: change working directory to script's location
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    run_vp()
