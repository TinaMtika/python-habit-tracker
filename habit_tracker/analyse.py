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

def get_habits_by_periodicity(periodicity):
    """
    Retrieves a list of habits filtered by their periodicity (e.g., Daily, Weekly).
    
    Args:
        periodicity (str): 'Daily' or 'Weekly'
        
    Returns:
        list: A list of strings containing habit names matching the periodicity.
    """
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT name FROM habits WHERE periodicity=?", (periodicity,))
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

def calculate_streak(date_strings, periodicity="Daily"):
    """
    Calculates the longest consecutive streak from a list of date strings.
    Respects whether the habit is Daily or Weekly.

    Args:
        date_strings (list): List of strings in 'YYYY-MM-DD' format.
        periodicity (str): 'Daily' or 'Weekly' to determine gap logic.

    Returns:
        int: The maximum number of consecutive periods recorded.
    """
    if not date_strings:
        return 0
    
    # Convert strings to datetime objects and ensure they are sorted
    dates = sorted([datetime.strptime(d, "%Y-%m-%d") for d in set(date_strings)])
    
    longest_streak = 0
    current_streak = 1
    
    for i in range(len(dates) - 1):
        if periodicity.lower() == "daily":
            # Check if the next date is exactly 1 day after the current date
            if dates[i+1] - dates[i] == timedelta(days=1):
                current_streak += 1
            else:
                longest_streak = max(longest_streak, current_streak)
                current_streak = 1
                
        elif periodicity.lower() == "weekly":
            # Compare ISO calendar weeks (Year, Week Number, Weekday)
            year1, week1, _ = dates[i].isocalendar()
            year2, week2, _ = dates[i+1].isocalendar()
            
            # Check if it's the very next week (handles end-of-year rollover)
            if (year2 == year1 and week2 == week1 + 1) or (year2 == year1 + 1 and week2 == 1):
                current_streak += 1
            elif year1 == year2 and week1 == week2:
                # Same week log, ignore and keep streak alive
                pass 
            else:
                # GAP DETECTED
                longest_streak = max(longest_streak, current_streak)
                current_streak = 1
            
    return max(longest_streak, current_streak)

def get_longest_run_streak_all():
    """
    Analyzes all habits to find which one has the highest all-time streak.
    
    Returns:
        tuple: (habit_name, streak_count)
    """
    con = get_db_connection()
    cur = con.cursor()
    # Need to fetch periodicity as well to calculate streaks properly
    cur.execute("SELECT name, periodicity FROM habits")
    all_habits = cur.fetchall()
    
    best_habit = None
    max_streak = 0
    
    for habit_name, periodicity in all_habits:
        dates = get_habit_history(habit_name)
        streak = calculate_streak(dates, periodicity)
        if streak > max_streak:
            max_streak = streak
            best_habit = habit_name
            
    return best_habit, max_streak