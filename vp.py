from atomic_memory import tick

def main():
    mem = tick()
    print("VP OK")
    print("Runs:", mem["runs"])

if __name__ == "__main__":
    main()
