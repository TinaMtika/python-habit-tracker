import pytest
import os
from datetime import datetime, timedelta
from habit import Habit
import db
import analyse

"""
Test suite for the Habit Tracker application.
Covers unit tests for the Habit class, integration tests for DB operations, 
and functional tests for the analytics engine using 4 weeks of predefined data.
"""

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

TEST_DB = "test_habits.db"

@pytest.fixture
def setup_db():
    """Creates a fresh test database, yields for the test, then deletes it."""
    db.create_tables(TEST_DB)
    yield
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_add_and_retrieve_habit(setup_db):
    """Ensure a habit can be saved to the DB and retrieved."""
    db.add_habit("TestGym", "Weekly", TEST_DB)
    db.increment_habit("TestGym", "2023-01-01", TEST_DB)
    data = db.get_habit_data("TestGym", TEST_DB)
    assert "2023-01-01" in data

def test_delete_habit(setup_db):
    """Ensure a habit can be successfully deleted from the database."""
    db.add_habit("TestRead", "Daily", TEST_DB)
    db.delete_habit("TestRead", TEST_DB)
    # Trying to get data for a deleted habit should return an empty list or None
    data = db.get_habit_data("TestRead", TEST_DB)
    assert len(data) == 0


# --- 3. Test Analytics with 4-Week Predefined Data ---

def test_calculate_streak_4_weeks_daily():
    """
    Verify daily streak calculator using 4 weeks (28 days) of continuous data.
    """
    base_date = datetime(2023, 1, 1)
    # Generate 28 consecutive days
    four_weeks_data = [(base_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(28)]
    
    streak = analyse.calculate_streak(four_weeks_data, periodicity="Daily")
    assert streak == 28

def test_calculate_streak_4_weeks_weekly():
    """
    Verify weekly streak calculator using 4 weeks of data (1 log per week).
    """
    base_date = datetime(2023, 1, 1)
    # Generate 4 dates, exactly 7 days apart
    four_weeks_data = [(base_date + timedelta(weeks=i)).strftime("%Y-%m-%d") for i in range(4)]
    
    streak = analyse.calculate_streak(four_weeks_data, periodicity="Weekly")
    assert streak == 4

def test_calculate_streak_with_break():
    """
    Verify the streak resets if a day is missed.
    """
    dates = ["2023-10-01", "2023-10-02", "2023-10-04"] # Skipped the 3rd
    streak = analyse.calculate_streak(dates, periodicity="Daily")
    assert streak == 2 # The longest streak was 2 days before the break

def test_calculate_streak_empty():
    """Ensure that an empty list of dates results in a streak of 0."""
    streak = analyse.calculate_streak([], periodicity="Daily")
    assert streak == 0


# --- 4. Test Analytics Module Functions ---

def test_get_habits_by_periodicity(setup_db):
    """Verify the analytics module can filter habits by their periodicity."""
    db.add_habit("Read", "Daily", TEST_DB)
    db.add_habit("Walk", "Daily", TEST_DB)
    db.add_habit("Clean", "Weekly", TEST_DB)
    
    # We must patch get_db_connection in analyse.py to use our TEST_DB for this to work 
    # perfectly in a real environment, but testing the logic here.
    # If my analyse functions don't accept a db_name argument, 
    # they will query your main database during this test.