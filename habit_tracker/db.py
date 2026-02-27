import sqlite3
from datetime import datetime

def get_db():
    """Establishes and returns a connection to the SQLite database."""
    return sqlite3.connect("habits.db")

def create_tables():
    """Initializes the database schemas for habits and tracking logs."""
    db = get_db()
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

def add_habit(name: str, periodicity: str):
    """Inserts a new habit into the database."""
    db = get_db()
    cursor = db.cursor()
    creation_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT OR IGNORE INTO habits VALUES (?, ?, ?)", 
                   (name, periodicity, creation_date))
    db.commit()
    db.close()

def increment_habit(name: str):
    """Records a completion for a habit on the current date."""
    db = get_db()
    cursor = db.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO tracker VALUES (?, ?)", (name, today))
    db.commit()
    db.close()

def edit_habit(old_name: str, new_name: str, new_periodicity: str):
    """Updates the name and periodicity of an existing habit and its logs."""
    db = get_db()
    cursor = db.cursor()
    # Update the main habits table
    cursor.execute("UPDATE habits SET name=?, periodicity=? WHERE name=?", 
                   (new_name, new_periodicity, old_name))
    # Update the foreign keys in the tracker table so history isn't lost
    cursor.execute("UPDATE tracker SET habitName=? WHERE habitName=?", 
                   (new_name, old_name))
    db.commit()
    db.close()

def delete_habit(name: str):
    """Permanently removes a habit and all associated tracking data."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM habits WHERE name=?", (name,))
    cursor.execute("DELETE FROM tracker WHERE habitName=?", (name,))
    db.commit()
    db.close()