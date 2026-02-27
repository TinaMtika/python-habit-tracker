"""
Main Entry Point for the Habit Tracker CLI.

Provides an interactive interface to manage habits, record completions,
and trigger the analytics engine to verify streaks and historical data.
"""

import questionary
import db
import analyse  
import seed_data  

def cli():
    """
    Runs the Habit Tracker command line interface.
    
    Ensures database initialization on startup and provides a loop for 
    user interaction via questionary prompts.
    """
    # Ensure tables exist before trying to read/write
    db.create_tables()
    
    print("\nWelcome to the Habit Tracker!\n")
    
    stop = False
    while not stop:
        choice = questionary.select(
            "What do you want to do?",
            choices=[
                "Create Habit", 
                "Mark Habit Complete", 
                "Edit Habit",           
                "Delete Habit",         
                "Analyze (Verify 28-Day Streak)", 
                "Seed Test Data (Fixtures)", 
                "Exit"
            ]
        ).ask()
        
        if choice == "Create Habit":
            name = questionary.text("What is the name of the habit?").ask()
            period = questionary.select("Periodicity?", choices=["Daily", "Weekly"]).ask()
            db.add_habit(name, period)
            print(f"✅ Habit '{name}' created!")

        elif choice == "Mark Habit Complete":
            habits = analyse.get_all_habits()
            if not habits:
                print("No habits found. Please create one first.")
                continue
            name = questionary.select("Which habit did you complete?", choices=habits).ask()
            db.increment_habit(name)
            print(f"✅ Marked {name} as complete!")
            
        elif choice == "Edit Habit":
            habits = analyse.get_all_habits()
            if not habits:
                print("No habits found to edit.")
                continue
            
            old_name = questionary.select("Which habit do you want to edit?", choices=habits).ask()
            new_name = questionary.text(f"Enter new name for '{old_name}' (or press Enter to keep it):").ask()
            new_period = questionary.select("Enter new periodicity:", choices=["Daily", "Weekly"]).ask()
            
            # Keep the old name if the user just pressed Enter
            final_name = new_name if new_name.strip() else old_name
            db.edit_habit(old_name, final_name, new_period)
            print(f"✅ Habit updated successfully to '{final_name}' ({new_period})!")

        elif choice == "Delete Habit":
            habits = analyse.get_all_habits()
            if not habits:
                print("No habits found to delete.")
                continue
            
            name = questionary.select("Which habit do you want to delete?", choices=habits).ask()
            confirm = questionary.confirm(f"⚠️ Are you sure you want to permanently delete '{name}' and all its data?").ask()
            
            if confirm:
                db.delete_habit(name)
                print(f"🗑️ Habit '{name}' deleted.")
            else:
                print("Deletion cancelled.")

        elif choice == "Analyze (Verify 28-Day Streak)":
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
            seed_data.seed_db()
            print("\n✅ Database seeded with 4 weeks of historical logs.")
            print("   (Includes one 28-day streak and habits with intentional gaps)\n")
            
        elif choice == "Exit":
            print("Goodbye!")
            stop = True

if __name__ == "__main__":
    cli()