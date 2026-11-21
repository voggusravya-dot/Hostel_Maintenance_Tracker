import os
import json
from datetime import datetime, date, timedelta

# File name to save records locally
DATA_FILE = "hostel_records.json"

# Fixed lists for valid choices
CATEGORIES = ["Plumbing", "Electrical", "Carpentry", "Cleaning", "Wi-Fi/Internet", "Other"]
PRIORITIES = ["Low", "Medium", "High", "Critical"]
STATUSES = ["Pending", "In Progress", "Resolved"]


# --- 1. FILE HANDLING FUNCTIONS ---
def load_records():
    """Loads existing records from the JSON file. Returns an empty list if file doesn't exist."""
    if not os.path.exists(DATA_FILE):
        return []
    
    try:
        file = open(DATA_FILE, "r")
        data = json.load(file)
        file.close()
        return data
    except:
        print("\n[Warning] Could not read data file properly. Starting fresh.")
        return []


def save_records(records):
    """Saves the list of record dictionaries into the JSON file."""
    try:
        file = open(DATA_FILE, "w")
        json.dump(records, file, indent=4)
        file.close()
    except Exception as e:
        print("\n[Error] Could not save data:", e)


# --- 2. INPUT VALIDATION FUNCTIONS ---
def get_valid_text(prompt):
    """Keeps asking until the user enters non-empty text."""
    while True:
        text = input(prompt).strip()
        if len(text) > 0:
            return text
        print("  -> Error: This field cannot be empty. Please try again.")


def get_valid_choice(title, options_list):
    """Displays numbered options and returns the chosen option string."""
    print("\n" + title)
    for i in range(len(options_list)):
        print(f"  {i + 1}. {options_list[i]}")
        
    while True:
        choice = input("Enter option number: ").strip()
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(options_list):
                return options_list[index]
        print(f"  -> Error: Please enter a number between 1 and {len(options_list)}.")


# --- 3. CORE PROJECT FEATURES ---
def register_request(records):
    """Takes user input and adds a new maintenance request dictionary to the list."""
    print("\n--- Register New Maintenance Request ---")
    
    name = get_valid_text("Enter Student Name: ")
    room = get_valid_text("Enter Room Number (e.g., B-105): ").upper()
    category = get_valid_choice("Select Issue Category:", CATEGORIES)
    issue = get_valid_text("Describe the problem: ")
    priority = get_valid_choice("Select Priority Level:", PRIORITIES)
    
    # Generate a unique ID like REQ-101, REQ-102
    req_id = f"REQ-{100 + len(records) + 1}"
    
    today = date.today()
    
    # Decide deadline days based on priority
    if priority == "Critical":
        days = 1
    elif priority == "High":
        days = 2
    elif priority == "Medium":
        days = 4
    else:
        days = 7
        
    due_date = today + timedelta(days=days)
    
    # Store the entry as a standard Python dictionary
    new_entry = {
        "id": req_id,
        "student_name": name,
        "room": room,
        "category": category,
        "issue": issue,
        "priority": priority,
        "status": "Pending",
        "logged_date": str(today),
        "due_date": str(due_date)
    }
    
    records.append(new_entry)
    save_records(records)
    print(f"\n[Success] Request saved! Your Request ID is: {req_id}")


def update_request_status(records):
    """Finds a request by ID and updates its status."""
    if len(records) == 0:
        print("\nNo records found in the system.")
        return

    print("\n--- Update Request Status ---")
    search_id = get_valid_text("Enter Request ID (e.g., REQ-101): ").upper()
    
    found = False
    for req in records:
        if req["id"] == search_id:
            found = True
            print(f"Found: {req['issue']} (Room {req['room']}) | Current Status: {req['status']}")
            new_status = get_valid_choice("Select New Status:", STATUSES)
            req["status"] = new_status
            save_records(records)
            print(f"\n[Success] Status updated to '{new_status}'.")
            break
            
    if not found:
        print(f"\n[Error] Request ID '{search_id}' not found.")


def search_records(records):
    """Filters and displays records based on user choice."""
    if len(records) == 0:
        print("\nNo records available to search.")
        return

    print("\n--- Search & View Records ---")
    print("  1. View All Records")
    print("  2. Filter by Category")
    print("  3. Filter by Status")
    print("  4. Search by Keyword")
    
    choice = input("Choose option (1-4): ").strip()
    results = []
    
    if choice == "1":
        results = records
    elif choice == "2":
        cat = get_valid_choice("Choose Category:", CATEGORIES)
        for req in records:
            if req["category"] == cat:
                results.append(req)
    elif choice == "3":
        stat = get_valid_choice("Choose Status:", STATUSES)
        for req in records:
            if req["status"] == stat:
                results.append(req)
    elif choice == "4":
        keyword = get_valid_text("Enter keyword (name or issue): ").lower()
        for req in records:
            if keyword in req["student_name"].lower() or keyword in req["issue"].lower():
                results.append(req)
    else:
        print("Invalid option selected.")
        return

    display_table(results)


def display_table(records_list):
    """Prints a clean formatted table in the terminal."""
    if len(records_list) == 0:
        print("\nNo matching records found.")
        return

    print("\n" + "-" * 85)
    print(f"{'ID':<9} | {'Room':<7} | {'Category':<15} | {'Priority':<9} | {'Status':<12} | {'Due Date':<10}")
    print("-" * 85)
    
    for r in records_list:
        print(f"{r['id']:<9} | {r['room']:<7} | {r['category']:<15} | {r['priority']:<9} | {r['status']:<12} | {r['due_date']:<10}")
        
    print("-" * 85)
    print(f"Total records shown: {len(records_list)}")


def show_summary(records):
    """Calculates totals, counts by status, and checks for overdue issues."""
    if len(records) == 0:
        print("\nNo data available to generate summary.")
        return

    total = len(records)
    pending_count = 0
    in_progress_count = 0
    resolved_count = 0
    overdue_list = []
    
    today_str = str(date.today())

    for req in records:
        if req["status"] == "Pending":
            pending_count += 1
        elif req["status"] == "In Progress":
            in_progress_count += 1
        elif req["status"] == "Resolved":
            resolved_count += 1
            
        if req["status"] != "Resolved" and req["due_date"] < today_str:
            overdue_list.append(req)

    print("\n==============================================")
    print("        HOSTEL MAINTENANCE SUMMARY            ")
    print("==============================================")
    print(f"Total Requests Logged : {total}")
    print(f"Pending               : {pending_count}")
    print(f"In Progress           : {in_progress_count}")
    print(f"Resolved              : {resolved_count}")
    
    if total > 0:
        resolution_rate = (resolved_count / total) * 100
        print(f"Resolution Rate       : {resolution_rate:.1f}%")
    print("==============================================")

    if len(overdue_list) > 0:
        print(f"\n[WARNING] {len(overdue_list)} request(s) are OVERDUE:")
        for item in overdue_list:
            print(f"  - {item['id']} (Room {item['room']}): Due on {item['due_date']}")
    else:
        print("\n[OK] No overdue maintenance requests.")


def export_summary_file(records):
    """Exports all records to a readable text report file."""
    if len(records) == 0:
        print("\nNo records to export.")
        return

    filename = "maintenance_report.txt"
    try:
        file = open(filename, "w")
        file.write("HOSTEL MAINTENANCE TRACKER - AUDIT REPORT\n")
        file.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        file.write("=" * 60 + "\n\n")
        
        for r in records:
            file.write(f"ID       : {r['id']}\n")
            file.write(f"Student  : {r['student_name']} (Room: {r['room']})\n")
            file.write(f"Category : {r['category']} | Priority: {r['priority']}\n")
            file.write(f"Issue    : {r['issue']}\n")
            file.write(f"Status   : {r['status']} (Due: {r['due_date']})\n")
            file.write("-" * 60 + "\n")
            
        file.close()
        print(f"\n[Success] Report saved to '{filename}'.")
    except Exception as e:
        print("\n[Error] Failed to write report:", e)


# --- 4. MAIN MENU LOOP ---
def main():
    all_records = load_records()
    
    while True:
        print("\n==========================================")
        print("     HOSTEL MAINTENANCE TRACKER MENU      ")
        print("==========================================")
        print("  1. Register New Request")
        print("  2. Update Request Status")
        print("  3. Search & View Records")
        print("  4. View Executive Summary")
        print("  5. Export Report to Text File")
        print("  6. Exit")
        print("==========================================")
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == "1":
            register_request(all_records)
        elif choice == "2":
            update_request_status(all_records)
        elif choice == "3":
            search_records(all_records)
        elif choice == "4":
            show_summary(all_records)
        elif choice == "5":
            export_summary_file(all_records)
        elif choice == "6":
            print("\nExiting program. Goodbye!")
            break
        else:
            print("\n[Error] Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
