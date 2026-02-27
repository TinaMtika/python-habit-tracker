"""
seed_data.py — Predefined Test Data (Fixtures)

Populates the database with 4 weeks (28 days) of historical habit data.
This is used both for manual testing via the CLI and for unit test fixtures.

Includes:
- A habit with a perfect 28-day streak (Daily)
- A habit with an intentional gap mid-month (Daily)
- A habit with 4 consecutive weeks logged (Weekly)
- A habit with a missing week (Weekly)
"""

import db
from datetime import datetime, timedelta

# Anchor date — start of our 4-week window
BASE_DATE = datetime(2024, 1, 1)


def generate_daily_dates(start, num_days):
    """Returns a list of consecutive daily date strings starting from start."""
    return [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(num_days)]


def generate_weekly_dates(start, num_weeks):
    """Returns a list of weekly date strings (one per week) starting from start."""
    return [(start + timedelta(weeks=i)).strftime("%Y-%m-%d") for i in range(num_weeks)]


def seed_db(db_name="habits.db"):
    """
    Seeds the database with 4 predefined habits and 4 weeks of tracking data.
    Safe to run multiple times — uses INSERT OR IGNORE for habits.
    """
    db.create_tables(db_name)

    # --- Habit 1: Perfect Month (Daily, 28-day unbroken streak) ---
    db.add_habit("Exercise", "Daily", db_name)
    for date in generate_daily_dates(BASE_DATE, 28):
        db.increment_habit("Exercise", date, db_name)

    # --- Habit 2: Daily habit with a gap on day 10 and 11 ---
    db.add_habit("Read", "Daily", db_name)
    all_days = generate_daily_dates(BASE_DATE, 28)
    for date in all_days:
        d = datetime.strptime(date, "%Y-%m-%d")
        # Skip day 10 and 11 to create an intentional break
        day_num = (d - BASE_DATE).days
        if day_num not in [9, 10]:
            db.increment_habit("Read", date, db_name)

    # --- Habit 3: Weekly habit with 4 consecutive weeks logged ---
    db.add_habit("Meal Prep", "Weekly", db_name)
    for date in generate_weekly_dates(BASE_DATE, 4):
        db.increment_habit("Meal Prep", date, db_name)

    # --- Habit 4: Weekly habit with week 3 missing ---
    db.add_habit("Review Goals", "Weekly", db_name)
    weekly_dates = generate_weekly_dates(BASE_DATE, 4)
    for i, date in enumerate(weekly_dates):
        if i != 2:  # Skip week 3
            db.increment_habit("Review Goals", date, db_name)


if __name__ == "__main__":
    seed_db()
    print("✅ Seeded database with 4 weeks of predefined habit data.")