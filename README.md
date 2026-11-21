# Hostel Maintenance Tracker

A Python command-line application designed to register hostel maintenance requests, track their resolution status, view paginated records, and generate visual analytics charts.

## Features
- **Register Maintenance Requests**: Log student name, room number, category (Plumbing, Electrical, Carpentry, Cleaning), priority (Low, Medium, High), and issue description with automatic deadline calculation.
- **Paginated Viewing**: View records cleanly in pages of 5 items at a time.
- **Status Tracking**: Update requests across `Pending`, `In Progress`, and `Resolved` states.
- **Safe Data Persistence**: Uses context managers (`with open(...)`) and automatic JSON backups (`hostel_data_backup.json`) to prevent data loss.
- **Visual Analytics**: Generate status distribution bar charts using `matplotlib`.
- **Automated Unit Tests**: Built-in `unittest` suite (`test_tracker.py`) verifying file persistence and backup integrity.

## Setup & Usage
1. Install optional visualization library:
   ```bash
   pip install matplotlib
   ```
2. Run the application:
   ```bash
   python hostel_tracker.py
   ```
3. Run automated tests:
   ```bash
   python -m unittest test_tracker.py
   ```
