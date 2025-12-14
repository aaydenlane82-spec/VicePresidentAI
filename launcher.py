import subprocess
import time

VP_SCRIPT = "vp.py"

def run_vp():
    while True:
        try:
            print("Launching VP...")
            subprocess.run(["python", VP_SCRIPT], check=True)
        except subprocess.CalledProcessError:
            print("VP crashed. Restarting in 2 seconds...")
            time.sleep(2)
        else:
            print("VP finished normally. Restarting in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    run_vp()
