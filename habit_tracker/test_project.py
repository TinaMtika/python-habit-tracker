import pytest
import os
from habit import Habit
import db
import analyse

"""
Test suite for the Habit Tracker application.
This module covers unit tests for the Habit class, integration tests 
for database operations, and functional tests for the analytics engine.
"""

# --- 1. Test the Habit Class ---

def test_habit_creation():
    """
    Verify that a Habit object initializes correctly with a name and periodicity.
    """
    habit = Habit("TestRun", "Daily")
    assert habit.name == "TestRun"
    assert habit.periodicity == "Daily"
    assert habit.completed_dates == []

def test_habit_mark_complete():
    """
    Verify that calling mark_complete() appends a record to the habit's history.
    """
    habit = Habit("TestRun", "Daily")
    habit.mark_complete()
    assert len(habit.completed_dates) == 1


# --- 2. Test the Database (Integration Test) ---

TEST_DB = "test_habits.db"

@pytest.fixture
def setup_db():
    """
    Pytest fixture to handle database lifecycle.
    Setup: Creates a fresh, empty test database.
    Teardown: Deletes the test database file after the test completes.
    """
    db.create_tables(TEST_DB)
    yield
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_add_and_retrieve_habit(setup_db):
    """
    Integration test to ensure a habit can be saved to the DB and 
    retrieved with its logged data.
    """
    db.add_habit("TestGym", "Weekly", TEST_DB)
    
    # Simulate logging a completion on a specific date
    db.increment_habit("TestGym", "2023-01-01", TEST_DB)
    data = db.get_habit_data("TestGym", TEST_DB)
    
    assert "2023-01-01" in data


# --- 3. Test Analytics (Functional Core) ---

def test_calculate_streak():
    """
    Verify that the streak calculator correctly counts a sequence of consecutive dates.
    """
    dates = ["2023-10-01", "2023-10-02", "2023-10-03"]
    streak = analyse.calculate_streak(dates)
    
    # Expecting 3 based on the number of consecutive entries provided
    assert streak == 3

def test_calculate_streak_empty():
    """
    Ensure that an empty list of dates results in a streak of 0.
    """
    dates = []
    streak = analyse.calculate_streak(dates)
    assert streak == 0
    
    