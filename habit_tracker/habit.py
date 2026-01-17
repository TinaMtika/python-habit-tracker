from datetime import datetime

class Habit:
    def __init__(self, name: str, periodicity: str):
        """
        Initialize a new Habit.
        :param name: The name of the habit (e.g., "Exercise")
        :param periodicity: The frequency (e.g., "Daily", "Weekly")
        """
        self.name = name
        self.periodicity = periodicity
        self.creation_date = datetime.now()
        # We will store completion dates as strings 'YYYY-MM-DD'
        self.completed_dates = [] 

    def mark_complete(self):
        """Marks the habit as complete for today."""
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in self.completed_dates:
            self.completed_dates.append(today)

    def __str__(self):
        return f"{self.name} ({self.periodicity})"