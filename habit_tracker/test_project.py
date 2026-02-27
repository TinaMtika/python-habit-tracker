"""
test_project.py — Full Unit Test Suite for the Habit Tracker

Covers:
    1. Habit class (creation, mark_complete)
    2. Database operations (add, increment, delete, retrieve)
    3. Streak calculations with 4 weeks of predefined data
    4. Analytics module functions (filter by periodicity, longest streak)

Run with:
    pytest test_project.py -v
"""

import pytest
import os
from datetime import datetime, timedelta
from habit import Habit
import db
import analyse
from seed_data import BASE_DATE, generate_daily_dates, generate_weekly_dates

# ============================================================
# 1. Habit Class Tests
# ============================================================

def test_habit_creation():
    """Verify that a Habit object initialises with correct attributes."""
    habit = Habit("TestRun", "Daily")
    assert habit.name == "TestRun"
    assert habit.periodicity == "Daily"
    assert habit.completed_dates == []


def test_habit_mark_complete():
    """Verify that mark_complete() appends today's date exactly once."""
    habit = Habit("TestRun", "Daily")
    habit.mark_complete()
    assert len(habit.completed_dates) == 1


def test_habit_mark_complete_no_duplicates():
    """Verify that calling mark_complete() twice on the same day only logs once."""
    habit = Habit("TestRun", "Daily")
    habit.mark_complete()
    habit.mark_complete()
    assert len(habit.completed_dates) == 1


def test_habit_str():
    """Verify the string representation of a Habit."""
    habit = Habit("Meditate", "Weekly")
    assert str(habit) == "Meditate (Weekly)"


# ============================================================
# 2. Database Integration Tests
# ============================================================

TEST_DB = "test_habits.db"


@pytest.fixture
def setup_db():
    """Creates a clean test database before each test, removes it after."""
    db.create_tables(TEST_DB)
    yield
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_add_and_retrieve_habit(setup_db):
    """Ensure a habit can be saved and its tracked date retrieved."""
    db.add_habit("TestGym", "Weekly", TEST_DB)
    db.increment_habit("TestGym", "2024-01-01", TEST_DB)
    data = db.get_habit_data("TestGym", TEST_DB)
    assert "2024-01-01" in data


def test_add_habit_no_duplicate(setup_db):
    """Adding the same habit twice should not raise an error or create duplicates."""
    db.add_habit("NoDupe", "Daily", TEST_DB)
    db.add_habit("NoDupe", "Daily", TEST_DB)
    # Should still work — only one entry due to INSERT OR IGNORE
    data = db.get_habit_data("NoDupe", TEST_DB)
    assert data == []  # No completions logged, just confirming no crash


def test_delete_habit(setup_db):
    """Ensure a habit and its tracking data are fully removed on delete."""
    db.add_habit("TestRead", "Daily", TEST_DB)
    db.increment_habit("TestRead", "2024-01-05", TEST_DB)
    db.delete_habit("TestRead", TEST_DB)
    data = db.get_habit_data("TestRead", TEST_DB)
    assert len(data) == 0

def test_edit_habit(setup_db):
    """Ensure a habit's name and periodicity can be updated."""
    db.add_habit("OldName", "Daily", TEST_DB)
    db.increment_habit("OldName", "2024-01-01", TEST_DB)
    db.edit_habit("OldName", "NewName", "Weekly", TEST_DB)
    
    old_data = db.get_habit_data("OldName", TEST_DB)
    new_data = db.get_habit_data("NewName", TEST_DB)
    
    assert len(old_data) == 0
    assert "2024-01-01" in new_data

def test_increment_habit_multiple_dates(setup_db):
    """Ensure multiple completions are all stored correctly."""
    db.add_habit("Walk", "Daily", TEST_DB)
    dates = ["2024-01-01", "2024-01-02", "2024-01-03"]
    for d in dates:
        db.increment_habit("Walk", d, TEST_DB)
    data = db.get_habit_data("Walk", TEST_DB)
    assert len(data) == 3


# ============================================================
# 3. Streak Calculation Tests (4-Week Predefined Data)
# ============================================================

def test_calculate_streak_4_weeks_daily():
    """28 consecutive daily logs should produce a streak of 28."""
    four_weeks = generate_daily_dates(BASE_DATE, 28)
    streak = analyse.calculate_streak(four_weeks, periodicity="Daily")
    assert streak == 28


def test_calculate_streak_4_weeks_weekly():
    """4 weekly logs (one per week) should produce a streak of 4."""
    four_weeks = generate_weekly_dates(BASE_DATE, 4)
    streak = analyse.calculate_streak(four_weeks, periodicity="Weekly")
    assert streak == 4


def test_calculate_streak_daily_with_gap():
    """A gap in daily logs should reset the streak; longest segment wins."""
    # 28 days but skip days 10 and 11
    all_days = generate_daily_dates(BASE_DATE, 28)
    dates = [
        d for d in all_days
        if (datetime.strptime(d, "%Y-%m-%d") - BASE_DATE).days not in [9, 10]
    ]
    streak = analyse.calculate_streak(dates, periodicity="Daily")
    # Longest run is days 12–28 = 17 days
    assert streak == 17


def test_calculate_streak_weekly_with_gap():
    """A missing week should break the streak; best segment should be 2."""
    dates = generate_weekly_dates(BASE_DATE, 4)
    dates_with_gap = [d for i, d in enumerate(dates) if i != 2]  # Remove week 3
    streak = analyse.calculate_streak(dates_with_gap, periodicity="Weekly")
    assert streak == 2


def test_calculate_streak_empty():
    """An empty date list should return a streak of 0."""
    assert analyse.calculate_streak([], periodicity="Daily") == 0


def test_calculate_streak_single_entry():
    """A single date should return a streak of 1."""
    assert analyse.calculate_streak(["2024-01-01"], periodicity="Daily") == 1


def test_calculate_streak_duplicate_dates():
    """Duplicate dates in the list should not inflate the streak count."""
    dates = ["2024-01-01", "2024-01-01", "2024-01-02", "2024-01-03"]
    streak = analyse.calculate_streak(dates, periodicity="Daily")
    assert streak == 3


# ============================================================
# 4. Analytics Module Function Tests
# ============================================================

def test_get_habits_by_periodicity(setup_db, monkeypatch):
    """Verify filtering habits by periodicity using the test database."""
    db.add_habit("Read", "Daily", TEST_DB)
    db.add_habit("Walk", "Daily", TEST_DB)
    db.add_habit("Clean", "Weekly", TEST_DB)

    # Redirect analyse's db connection to the test DB
    import sqlite3
    monkeypatch.setattr(
        "analyse.get_db_connection", lambda: sqlite3.connect(TEST_DB)
    )

    daily = analyse.get_habits_by_periodicity("Daily")
    weekly = analyse.get_habits_by_periodicity("Weekly")

    assert "Read" in daily
    assert "Walk" in daily
    assert "Clean" in weekly
    assert "Clean" not in daily


def test_get_longest_run_streak_all(setup_db, monkeypatch):
    """Verify the analytics engine finds the habit with the longest overall streak."""
    db.add_habit("Exercise", "Daily", TEST_DB)
    db.add_habit("Read", "Daily", TEST_DB)

    # Exercise: 28-day streak
    for date in generate_daily_dates(BASE_DATE, 28):
        db.increment_habit("Exercise", date, TEST_DB)

    # Read: only 5 days
    for date in generate_daily_dates(BASE_DATE, 5):
        db.increment_habit("Read", date, TEST_DB)

    import sqlite3
    monkeypatch.setattr(
        "analyse.get_db_connection", lambda: sqlite3.connect(TEST_DB)
    )

    best_habit, best_streak = analyse.get_longest_run_streak_all()
    assert best_habit == "Exercise"
    assert best_streak == 28