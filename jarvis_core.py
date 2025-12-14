# jarvis_core.py
class JarvisCore:
    def __init__(self, memory):
        self.memory = memory
        self.systems_online = False

    def initialize_system(self):
        print("[Jarvis] Initializing core systems...")
        self.systems_online = True
        print("[Jarvis] Systems online. Memory synced.")
