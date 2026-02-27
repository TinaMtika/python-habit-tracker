"""
Database Seeding Module for Habit Tracker.
"""
import db
import random
import sqlite3
from datetime import datetime, timedelta

def seed_db():
    print("Seeding database...")
    db.create_tables()
    
    habits = [
        ("Drink Water", "Daily"),
        ("Read Book", "Daily"),
        ("Gym", "Weekly"),
        ("Code Python", "Daily"),
        ("Meditate", "Daily")
    ]
    
    for name, period in habits:
        db.add_habit(name, period)
        
    today = datetime.now()
    
    # Connect directly to insert historical dates
    conn = sqlite3.connect("habits.db")
    cursor = conn.cursor()
    
    for name, period in habits:
        for i in range(28):
            date_to_log = today - timedelta(days=i)
            date_str = date_to_log.strftime("%Y-%m-%d")
            
            if name == "Drink Water":
                is_completed = True
            else:
                is_completed = random.random() < 0.7
            
            if is_completed:
                cursor.execute("INSERT INTO tracker VALUES (?, ?)", (name, date_str))
                
    conn.commit()
    conn.close()
                
    print("✅ Database successfully seeded!")
    print(" -> 'Drink Water' contains a 28-day Perfect Month.")
    print(" -> Other habits contain gaps to verify streak reset logic.")

if __name__ == "__main__":
    seed_db()