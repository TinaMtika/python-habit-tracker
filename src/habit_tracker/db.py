import sqlite3
from datetime import datetime

def get_db_connection(db_name="habits.db"):
    con = sqlite3.connect(db_name)
    return con

def create_tables(db_name="habits.db"):
    con = get_db_connection(db_name)
    cur = con.cursor()
    
    # Table for storing the Habits
    cur.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            name TEXT PRIMARY KEY,
            periodicity TEXT,
            creation_date TEXT
        )
    """)
    
    # Table for storing the specific dates a habit was completed
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tracker (
            date TEXT,
            habit_name TEXT,
            FOREIGN KEY (habit_name) REFERENCES habits(name)
        )
    """)
    
    con.commit()
    con.close()

def add_habit(name, periodicity, db_name="habits.db"):
    con = get_db_connection(db_name)
    cur = con.cursor()
    creation_date = datetime.now().strftime("%Y-%m-%d")
    # Using INSERT OR IGNORE to prevent crashing if habit exists
    cur.execute("INSERT OR IGNORE INTO habits VALUES (?, ?, ?)", 
                (name, periodicity, creation_date))
    con.commit()
    con.close()

def increment_habit(name, date=None, db_name="habits.db"):
    """
    Logs a completion for a specific date. 
    If date is None, uses today.
    """
    con = get_db_connection(db_name)
    cur = con.cursor()
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    cur.execute("INSERT INTO tracker VALUES (?, ?)", (date, name))
    con.commit()
    con.close()

def get_habit_data(name, db_name="habits.db"):
    con = get_db_connection(db_name)
    cur = con.cursor()
    cur.execute("SELECT date FROM tracker WHERE habit_name=?", (name,))
    dates = [row[0] for row in cur.fetchall()]
    con.close()
    return dates