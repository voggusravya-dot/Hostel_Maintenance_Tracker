# Hostel Maintenance Tracker

A Python command-line application designed to register hostel maintenance requests, track their resolution status, filter records, and generate summary reports.

## How to Run
1. Make sure Python 3 is installed on your computer.
2. Open your terminal or command prompt in this folder.
3. Run the program:
   ```bash
   python hostel_tracker.py
   ```

## Features
- **Register New Request**: Logs student name, room number, category, issue description, and priority level with automatic deadline calculation.
- **Update Request Status**: Update requests between `Pending`, `In Progress`, and `Resolved`.
- **Search & Filter**: View all records or filter by category, status, or keyword.
- **Executive Summary**: Displays total counts, resolution percentage, and alerts for overdue tasks.
- **Data Persistence**: Automatically saves all records to `hostel_records.json` and supports exporting reports to `maintenance_report.txt`.
