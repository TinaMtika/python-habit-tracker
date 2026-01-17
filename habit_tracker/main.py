"""
Main Entry Point for the Habit Tracker CLI.

Provides an interactive interface to manage habits, record completions,
and trigger the analytics engine to verify streaks and historical data.
"""

import questionary
import db
import analyse  # Assuming your analytics module is named 'analyse'
import seed_data  # The module we created to generate test data

def cli():
    """
    Runs the Habit Tracker command line interface.
    
    Ensures database initialization on startup and provides a loop for 
    user interaction via questionary prompts.
    """
    # Ensure tables exist
    db.create_tables()
    
    print("Welcome to the Habit Tracker!")
    
    stop = False
    while not stop:
        choice = questionary.select(
            "What do you want to do?",
            choices=[
                "Create Habit", 
                "Mark Habit Complete", 
                "Analyze (Verify 28-Day Streak)", 
                "Seed Test Data (Fixtures)", 
                "Exit"
            ]
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
            
        elif choice == "Analyze (Verify 28-Day Streak)":
            # This triggers the logic to prove the system identifies the "Perfect Month"
            habit, streak = analyse.get_longest_run_streak_all()
            
            if habit:
                print(f"\n--- Analytics Report ---")
                print(f"Longest Streak Overall: {habit}")
                print(f"Total Consecutive Days: {streak}")
                
                if streak >= 28:
                    print("✅ Verification: 28-day Perfect Month achieved!")
                else:
                    print("ℹ️ Note: No 28-day streak found yet.")
                print("------------------------\n")
            else:
                print("\n[!] No tracking data available. Try seeding the database.\n")

        elif choice == "Seed Test Data (Fixtures)":
            # This allows for immediate verification of the analytics engine
            # without waiting for real-time user data.
            seed_data.seed_db()
            print("\n✅ Database seeded with 4 weeks of historical logs.")
            print("   (Includes one 28-day streak and habits with intentional gaps)\n")
            
        elif choice == "Exit":
            print("Goodbye!")
            stop = True

if __name__ == "__main__":
    cli()