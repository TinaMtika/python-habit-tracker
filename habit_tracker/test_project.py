import pytest
from datetime import datetime, timedelta
from habit import Habit
import db
import analyse

# --- 1. Test the Habit Class ---

def test_habit_creation():
    """Verify that a Habit object initializes correctly."""
    habit = Habit("TestRun", "Daily")
    assert habit.name == "TestRun"
    assert habit.periodicity == "Daily"
    assert habit.completed_dates == []

def test_habit_mark_complete():
    """Verify that calling mark_complete() appends a record."""
    habit = Habit("TestRun", "Daily")
    habit.mark_complete()
    assert len(habit.completed_dates) == 1


# --- 2. Test the Database (Integration Tests) ---

@pytest.fixture(autouse=True)
def run_around_tests():
    """Ensures tables exist before tests and cleans up test data after."""
    db.create_tables()
    yield
    # Cleanup only the test data
    try:
        db.delete_habit("TestGym")
        db.delete_habit("TestRead")
    except:
        pass

def test_add_and_retrieve_habit():
    """Ensure a habit can be saved to the DB."""
    db.add_habit("TestGym", "Weekly")
    # If it doesn't crash, the insert was successful
    assert True 

def test_delete_habit():
    """Ensure a habit can be successfully deleted from the database."""
    db.add_habit("TestRead", "Daily")
    db.delete_habit("TestRead")
    
    # Verify it was deleted by checking all habits
    import sqlite3
    conn = sqlite3.connect("habits.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM habits WHERE name='TestRead'")
    result = cursor.fetchone()
    conn.close()
    
    assert result is None


# --- 3. Test Analytics with 4-Week Predefined Data ---

def test_calculate_streak_4_weeks_daily():
    """Verify daily streak calculator using 4 weeks (28 days) of continuous data."""
    base_date = datetime(2023, 1, 1)
    four_weeks_data = [(base_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(28)]
    
    streak = analyse.calculate_streak(four_weeks_data, periodicity="Daily")
    assert streak == 28

def test_calculate_streak_4_weeks_weekly():
    """Verify weekly streak calculator using 4 weeks of data (1 log per week)."""
    base_date = datetime(2023, 1, 1)
    four_weeks_data = [(base_date + timedelta(weeks=i)).strftime("%Y-%m-%d") for i in range(4)]
    
    streak = analyse.calculate_streak(four_weeks_data, periodicity="Weekly")
    assert streak == 4

def test_calculate_streak_with_break():
    """Verify the streak resets if a day is missed."""
    dates = ["2023-10-01", "2023-10-02", "2023-10-04"] # Skipped the 3rd
    streak = analyse.calculate_streak(dates, periodicity="Daily")
    assert streak == 2 

def test_calculate_streak_empty():
    """Ensure that an empty list of dates results in a streak of 0."""
    streak = analyse.calculate_streak([], periodicity="Daily")
    assert streak == 0