from datetime import datetime, timedelta
from db import get_db_connection

def get_all_habits():
    """
    Retrieves all habit names currently stored in the database.
    
    Returns:
        list: A list of strings containing habit names.
    """
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT name FROM habits")
    return [row[0] for row in cur.fetchall()]

def get_habit_history(name):
    """
    Retrieves all completion dates for a specific habit from the tracker table.
    
    Args:
        name (str): The name of the habit to look up.
        
    Returns:
        list: A list of date strings (YYYY-MM-DD).
    """
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT date FROM tracker WHERE habit_name=? ORDER BY date ASC", (name,))
    return [row[0] for row in cur.fetchall()]

def calculate_streak(date_strings):
    """
    Calculates the longest consecutive daily streak from a list of date strings.
    
    This logic verifies the 'Reliable Backend Testing' requirement by 
    identifying if dates are exactly one day apart. If a gap is found, 
    the current streak resets to zero.

    Args:
        date_strings (list): List of strings in 'YYYY-MM-DD' format.

    Returns:
        int: The maximum number of consecutive days recorded.
    """
    if not date_strings:
        return 0
    
    # Convert strings to datetime objects and ensure they are sorted
    dates = sorted([datetime.strptime(d, "%Y-%m-%d") for d in set(date_strings)])
    
    longest_streak = 0
    current_streak = 1
    
    for i in range(len(dates) - 1):
        # Check if the next date is exactly 1 day after the current date
        if dates[i+1] - dates[i] == timedelta(days=1):
            current_streak += 1
        else:
            # GAP DETECTED: Update longest_streak and reset current
            longest_streak = max(longest_streak, current_streak)
            current_streak = 1
            
    # Final check to see if the last streak was the longest
    return max(longest_streak, current_streak)

def get_longest_run_streak_all():
    """
    Analyzes all habits to find which one has the highest all-time streak.
    
    Purpose: Used to verify the 'Perfect Month' fixture (expecting 28).

    Returns:
        tuple: (habit_name, streak_count)
    """
    all_habits = get_all_habits()
    best_habit = None
    max_streak = 0
    
    for habit in all_habits:
        dates = get_habit_history(habit)
        streak = calculate_streak(dates)
        if streak > max_streak:
            max_streak = streak
            best_habit = habit
            
    return best_habit, max_streak