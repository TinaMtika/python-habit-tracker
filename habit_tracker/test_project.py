import pytest
import os
from habit import Habit
import db
import analyse

# --- 1. Test the Habit Class ---
def test_habit_creation():
    habit = Habit("TestRun", "Daily")
    assert habit.name == "TestRun"
    assert habit.periodicity == "Daily"
    assert habit.completed_dates == []

def test_habit_mark_complete():
    habit = Habit("TestRun", "Daily")
    habit.mark_complete()
    # Check if the list now has 1 item
    assert len(habit.completed_dates) == 1

# --- 2. Test the Database (Integration Test) ---
# We use a temporary test database so we don't mess up your real data
TEST_DB = "test_habits.db"

@pytest.fixture
def setup_db():
    # Setup: Create a fresh test database
    db.create_tables(TEST_DB)
    yield
    # Teardown: Remove the test database file after tests run
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_add_and_retrieve_habit(setup_db):
    # Add a habit to the TEST database
    db.add_habit("TestGym", "Weekly", TEST_DB)
    
    # Verify it exists by trying to add a completion log to it
    # If the habit didn't exist, this might fail depending on foreign keys, 
    # but here we check if we can query it via the analytics module logic
    # (Note: we need to point analytics to the test DB to test this fully, 
    # but for now we test the DB function directly)
    
    db.increment_habit("TestGym", "2023-01-01", TEST_DB)
    data = db.get_habit_data("TestGym", TEST_DB)
    
    assert "2023-01-01" in data

# --- 3. Test Analytics (Functional Core) ---
def test_calculate_streak():
    # We pass a raw list of dates to the calculation engine
    dates = ["2023-10-01", "2023-10-02", "2023-10-03"]
    streak = analyse.calculate_streak(dates)
    
    # Based on your current simple logic (count of dates), this should be 3
    assert streak == 3

def test_calculate_streak_empty():
    dates = []
    streak = analyse.calculate_streak(dates)
    assert streak == 0