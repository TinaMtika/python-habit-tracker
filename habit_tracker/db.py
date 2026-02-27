"""
db.py — Database Layer for Habit Tracker

Handles all SQLite interactions: creating tables, adding, editing,
deleting, and retrieving habits and their completion logs.
"""

import sqlite3
from datetime import datetime


def get_db(db_name="habits.db"):
    """Establishes and returns a connection to the SQLite database."""
    return sqlite3.connect(db_name)


# Alias for backwards compatibility with analyse.py
get_db_connection = get_db


def create_tables(db_name="habits.db"):
    """Initializes the database schemas for habits and tracking logs."""
    db = get_db(db_name)
    cursor = db.cursor()
    # Table to store the habit definitions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            name TEXT PRIMARY KEY,
            periodicity TEXT,
            creation_date TEXT
        )
    ''')
    # Table to store the individual completion logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracker (
            habitName TEXT,
            date TEXT,
            FOREIGN KEY (habitName) REFERENCES habits(name)
        )
    ''')
    db.commit()
    db.close()


def add_habit(name: str, periodicity: str, db_name="habits.db"):
    """Inserts a new habit into the database."""
    db = get_db(db_name)
    cursor = db.cursor()
    creation_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT OR IGNORE INTO habits VALUES (?, ?, ?)",
                   (name, periodicity, creation_date))
    db.commit()
    db.close()


def increment_habit(name: str, date=None, db_name="habits.db"):
    """Records a completion for a habit. Uses today's date if none provided."""
    db = get_db(db_name)
    cursor = db.cursor()
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO tracker VALUES (?, ?)", (name, date))
    db.commit()
    db.close()


def get_habit_data(name: str, db_name="habits.db"):
    """Returns a list of all completion dates for a given habit."""
    db = get_db(db_name)
    cursor = db.cursor()
    cursor.execute("SELECT date FROM tracker WHERE habitName=?", (name,))
    dates = [row[0] for row in cursor.fetchall()]
    db.close()
    return dates


def edit_habit(old_name: str, new_name: str, new_periodicity: str, db_name="habits.db"):
    """Updates the name and periodicity of an existing habit and its logs."""
    db = get_db(db_name)
    cursor = db.cursor()
    # Update the main habits table
    cursor.execute("UPDATE habits SET name=?, periodicity=? WHERE name=?",
                   (new_name, new_periodicity, old_name))
    # Update the foreign keys in the tracker table so history is preserved
    cursor.execute("UPDATE tracker SET habitName=? WHERE habitName=?",
                   (new_name, old_name))
    db.commit()
    db.close()


def delete_habit(name: str, db_name="habits.db"):
    """Permanently removes a habit and all associated tracking data."""
    db = get_db(db_name)
    cursor = db.cursor()
    cursor.execute("DELETE FROM habits WHERE name=?", (name,))
    cursor.execute("DELETE FROM tracker WHERE habitName=?", (name,))
    db.commit()
    db.close()