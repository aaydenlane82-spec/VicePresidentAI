from memory import increment_runs, get_runs
from bug_killer import heal_if_needed
from upgrader import check_and_apply_upgrades

def main():
    # Step 1: Ensure memory is healthy
    heal_if_needed()

    # Step 2: Apply upgrades automatically
    check_and_apply_upgrades()

    # Step 3: Increment run counter
    current_run = increment_runs()
    print(f"VP is running. Total runs: {current_run}")

    # Step 4: Your main VP logic goes here
    # Example logic placeholder
    print("Vice President AI is operational. All systems nominal.")

if __name__ == "__main__":
    main()
