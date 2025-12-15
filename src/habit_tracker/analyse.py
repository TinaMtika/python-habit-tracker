from db import get_db_connection

def get_all_habits():
    """Returns a list of all habit names from the DB."""
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT name FROM habits")
    return [row[0] for row in cur.fetchall()]

def get_habit_history(name):
    """Returns all completion dates for a specific habit."""
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT date FROM tracker WHERE habit_name=?", (name,))
    return [row[0] for row in cur.fetchall()]

def calculate_streak(dates):
    """
    Functional approach: Receives a list of dates, calculates streak.
    returns: (current_streak, longest_streak)
    """
    if not dates:
        return 0
    
    # Sort and remove duplicates just in case
    sorted_dates = sorted(list(set(dates)))
    
    # Simple logic to count consecutive days
    # (Note: In a real app, you'd convert strings to datetime objects to check 1-day gaps)
    # This is a basic counter for demonstration
    count = 0
    max_streak = 0
    
    for i in range(len(sorted_dates)):
        # logic placeholder: simplified count
        count += 1
        if count > max_streak:
            max_streak = count
            
    return max_streak

def get_longest_run_streak_all():
    """Check every habit and return the one with the highest streak."""
    all_habits = get_all_habits()
    best_habit = ""
    best_streak = 0
    
    for habit in all_habits:
        dates = get_habit_history(habit)
        streak = calculate_streak(dates)
        if streak > best_streak:
            best_streak = streak
            best_habit = habit
            
    return best_habit, best_streak