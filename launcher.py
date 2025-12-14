# launcher.py
from auto_upgrade import run_upgrades
from bug_killer import eliminate_bugs
from self_heal import self_healing_system

def launch_all(jarvis):
    print("[Launcher] Starting all systems...")
    eliminate_bugs(jarvis)
    self_healing_system(jarvis)
    run_upgrades(jarvis)
    print("[Launcher] All systems online and upgraded!")
