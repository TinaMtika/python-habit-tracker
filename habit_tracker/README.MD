# Habit Tracker 
**Student:** Tinashe Christopher Mtika  
**Student ID:** 102401222  

A Python-based habit tracking application that allows users to manage and analyze personal habits via a Command Line Interface (CLI). This project demonstrates the integration of Object-Oriented Programming (OOP) and Functional Programming (FP) principles.

## Features
- **Habit Management**: Create daily or weekly habits.
- **Data Persistence**: Uses a SQLite database to store habits and tracking logs.
- **Analytics Engine**: View current streaks, longest streaks, and filter habits by periodicity.
- **Automated Testing**: Comprehensive test suite using `pytest`.
- **Pre-defined Data**: Includes 4 weeks of sample tracking data for immediate analysis.

## Project Structure
- `main.py`: The entry point for the CLI application.
- `habit.py`: Contains the `Habit` class (OOP).
- `db_manager.py`: Handles all SQLite database interactions.
- `analytics.py`: Contains functions for calculating streaks and filtering data (FP).
- `test_habit_tracker.py`: The test suite.

## Installation
1. Ensure you have Python 3.7 or later installed.
2. Clone this repository:
   ```bash
git clone https://github.com/TinaMtika/python-habit-tracker.git 
please install the dependencies by running: 
pip install -r requirements.txt 
Then run the app with: python main.py