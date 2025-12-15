import db
import random
from datetime import datetime, timedelta

def seed_db():
    print("Seeding database...")
    
    # 1. Create the tables
    db.create_tables()
    
    # 2. Define 5 Predefined Habits
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
        
    # 4. Generate 4 weeks of fake tracking data
    # We go back 28 days and randomly "complete" habits
    today = datetime.now()
    
    for name, period in habits:
        for i in range(28):
            date_to_log = today - timedelta(days=i)
            date_str = date_to_log.strftime("%Y-%m-%d")
            
            # Randomly decide if we did the habit that day (60% chance)
            if random.choice([True, False, True]): 
                db.increment_habit(name, date_str)
                
    print("Database successfully seeded with 4 weeks of data!")

if __name__ == "__main__":
    seed_db()