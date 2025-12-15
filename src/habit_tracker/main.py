import questionary
import db
import analyse
from habit import Habit

def cli():
    # Ensure tables exist
    db.create_tables()
    
    print("Welcome to the Habit Tracker!")
    
    stop = False
    while not stop:
        choice = questionary.select(
            "What do you want to do?",
            choices=["Create Habit", "Mark Habit Complete", "Analyze", "Exit"]
        ).ask()
        
        if choice == "Create Habit":
            name = questionary.text("What is the name of the habit?").ask()
            period = questionary.select("Periodicity?", choices=["Daily", "Weekly"]).ask()
            db.add_habit(name, period)
            print(f"Habit '{name}' created!")

        elif choice == "Mark Habit Complete":
            habits = analyse.get_all_habits()
            if not habits:
                print("No habits found.")
                continue
            name = questionary.select("Which habit did you complete?", choices=habits).ask()
            db.increment_habit(name)
            print(f"Marked {name} as complete!")
            
        elif choice == "Analyze":
            # Example usage of analytics
            habit, streak = analyse.get_longest_run_streak_all()
            print(f"\n--- Analytics Report ---")
            print(f"Longest Streak Overall: {habit} with {streak} completions")
            print("------------------------\n")
            
        elif choice == "Exit":
            print("Goodbye!")
            stop = True

if __name__ == "__main__":
    cli()