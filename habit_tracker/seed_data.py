"""
Database Seeding Module for Habit Tracker.

This module populates the database with initial 'fixture' data. 
It generates 28 days of historical tracking to allow immediate testing 
of analytics, including streak calculations and reset logic.
"""

import db
import random
from datetime import datetime, timedelta

def seed_db():
    """
    Seeds the database with 5 predefined habits and 4 weeks of tracking data.
    
    Creates:
    - 1 habit with a perfect 28-day streak (to test 'Perfect Month' logic).
    - 4 habits with random gaps (to test streak reset and analytics accuracy).
    """
    print("Seeding database...")
    
    # 1. Create the tables (Ensure schema exists)
    db.create_tables()
    
    # 2. Define 5 Predefined Habits
    # Format: (Name, Periodicity)
    habits = [
        ("Drink Water", "Daily"),
        ("Read Book", "Daily"),
        ("Gym", "Weekly"),
        ("Code Python", "Daily"),
        ("Meditate", "Daily")
    ]
    
    # 3. Add habits to DB
    for name, period in habits:
        db.add_habit(name, period)
        
    # 4. Generate 28 days of historical data
    today = datetime.now()
    
    for name, period in habits:
        for i in range(28):
            # Calculate date for each day in the past 4 weeks
            date_to_log = today - timedelta(days=i)
            date_str = date_to_log.strftime("%Y-%m-%d")
            
            # LOGIC VALIDATION RULES:
            if name == "Drink Water":
                # FORCE a perfect 28-day streak for "Drink Water"
                is_completed = True
            else:
                # INTRODUCE GAPS for other habits to test streak resets
                # 70% chance of completion ensures gaps will exist
                is_completed = random.random() < 0.7
            
            if is_completed:
                db.increment_habit(name, date_str)
                
    print("Database successfully seeded!")
    print(" -> 'Drink Water' contains a 28-day Perfect Month.")
    print(" -> Other habits contain gaps to verify streak reset logic.")

if __name__ == "__main__":
    seed_db()