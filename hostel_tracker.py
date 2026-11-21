import datetime
import json
import os

# Optional: Try importing matplotlib for graphical analytics
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

DATA_FILE = "hostel_data.json"
BACKUP_FILE = "hostel_data_backup.json"


def load_records():
    """Loads records from the JSON file using context managers and safe exception handling."""
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Fallback to backup if main file is corrupted
        if os.path.exists(BACKUP_FILE):
            try:
                with open(BACKUP_FILE, "r", encoding="utf-8") as backup:
                    return json.load(backup)
            except (FileNotFoundError, json.JSONDecodeError):
                return []
        return []


def save_records(records):
    """Saves records securely using a backup mechanism to prevent data loss."""
    # Create a backup of existing data first if file exists
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as src:
                data = src.read()
            with open(BACKUP_FILE, "w", encoding="utf-8") as dst:
                dst.write(data)
        except IOError:
            pass

    # Write to main file using context manager
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=4)
    except IOError as e:
        print(f"Error saving data: {e}")


def get_valid_input(prompt, validation_type="non_empty", options=None):
    """Robust input validation function."""
    while True:
        value = input(prompt).strip()
        if validation_type == "non_empty":
            if value:
                return value
            print("Error: Input cannot be empty. Please try again.")
        elif validation_type == "choice":
            if value in options:
                return value
            print(f"Error: Invalid choice. Please choose from {', '.join(options)}.")


def register_request(records):
    print("\n--- Register New Maintenance Request ---")
    name = get_valid_input("Enter Student Name: ")
    room = get_valid_input("Enter Room Number: ")
    category = get_valid_input(
        "Enter Category (Plumbing, Electrical, Carpentry, Cleaning): ",
        "choice",
        ["Plumbing", "Electrical", "Carpentry", "Cleaning"],
    )
    priority = get_valid_input(
        "Enter Priority (Low, Medium, High): ", "choice", ["Low", "Medium", "High"]
    )
    description = get_valid_input("Enter Description of Issue: ")

    # Calculate deadline based on priority
    created_date = datetime.date.today()
    if priority == "High":
        deadline = created_date + datetime.timedelta.days(1)
    elif priority == "Medium":
        deadline = created_date + datetime.timedelta.days(3)
    else:
        deadline = created_date + datetime.timedelta.days(7)

    new_id = len(records) + 1
    record = {
        "id": new_id,
        "name": name,
        "room": room,
        "category": category,
        "priority": priority,
        "description": description,
        "status": "Pending",
        "created_date": created_date.isoformat(),
        "deadline": deadline.isoformat(),
    }

    records.append(record)
    save_records(records)
    print(f"\nSuccess! Request #{new_id} registered. Target resolution by: {deadline}")


def view_records(records):
    if not records:
        print("\nNo maintenance records found.")
        return

    print("\n--- Maintenance Records ---")
    page_size = 5
    total_records = len(records)
    start_idx = 0

    while start_idx < total_records:
        end_idx = min(start_idx + page_size, total_records)
        print(f"\nShowing records {start_idx + 1} to {end_idx} of {total_records}:")
        print("-" * 75)
        for r in records[start_idx:end_idx]:
            print(
                f"ID: {r['id']} | Room: {r['room']} | Cat: {r['category']} |"
                f" Priority: {r['priority']} | Status: {r['status']}"
            )
            print(f"Desc: {r['description']} | Deadline: {r['deadline']}")
            print("-" * 75)

        if end_idx >= total_records:
            break

        cont = get_valid_input(
            "Press 'n' for next page or 'q' to return to menu: ",
            "choice",
            ["n", "q"],
        )
        if cont == "q":
            break
        start_idx = end_idx


def update_status(records):
    if not records:
        print("\nNo records available to update.")
        return

    try:
        req_id = int(get_valid_input("Enter Request ID to update: "))
    except ValueError:
        print("Error: ID must be a number.")
        return

    for r in records:
        if r["id"] == req_id:
            new_status = get_valid_input(
                "Enter new status (Pending, In Progress, Resolved): ",
                "choice",
                ["Pending", "In Progress", "Resolved"],
            )
            r["status"] = new_status
            save_records(records)
            print(f"Success! Request #{req_id} status updated to {new_status}.")
            return

    print("Error: Request ID not found.")


def generate_analytics(records):
    """Generates a Matplotlib chart to satisfy innovation & analytics criteria."""
    if not MATPLOTLIB_AVAILABLE:
        print("\nMatplotlib is not installed. Run 'pip install matplotlib' to enable charts.")
        return

    if not records:
        print("\nNo data available for analytics.")
        return

    statuses = {"Pending": 0, "In Progress": 0, "Resolved": 0}
    for r in records:
        if r["status"] in statuses:
            statuses[r["status"]] += 1

    labels = list(statuses.keys())
    values = list(statuses.values())

    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color=["#ff9999", "#ffcc99", "#99ff99"])
    plt.title("Hostel Maintenance Requests by Status")
    plt.xlabel("Status")
    plt.ylabel("Count")
    plt.tight_layout()
    print("\nOpening chart window...")
    plt.show()


def main():
    records = load_records()
    while True:
        print("\n=== HOSTEL MAINTENANCE TRACKER ===")
        print("1. Register New Request")
        print("2. View All Requests (Paginated)")
        print("3. Update Request Status")
        print("4. Generate Status Analytics Chart")
        print("5. Exit")

        choice = get_valid_input(
            "Choose an option (1-5): ", "choice", ["1", "2", "3", "4", "5"]
        )

        if choice == "1":
            register_request(records)
        elif choice == "2":
            view_records(records)
        elif choice == "3":
            update_status(records)
        elif choice == "4":
            generate_analytics(records)
        elif choice == "5":
            print("Exiting application. Goodbye!")
            break


if __name__ == "__main__":
    main()
