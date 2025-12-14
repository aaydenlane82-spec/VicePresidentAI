import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ERROR_HANDLER_PATH = os.path.join(BASE_DIR, "error_handler.py")

if __name__ == "__main__":
    try:
        # Run the central error handler which monitors all scripts
        subprocess.run([sys.executable, ERROR_HANDLER_PATH], check=True)
    except KeyboardInterrupt:
        print("Offline Launcher exiting...")
    except subprocess.CalledProcessError as e:
        print(f"Error Handler exited with code {e.returncode}")
