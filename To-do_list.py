import json
from datetime import datetime, timedelta

# File name for saving tasks
FILENAME = "tasks.json"

# --------------------------- FILE HANDLING ---------------------------
def load_tasks():
    """Load tasks from JSON file."""
    try:
        with open(FILENAME, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    """Save tasks to JSON file."""
    with open(FILENAME, "w") as file:
        json.dump(tasks, file, indent=4)

# --------------------------- ADD TASK ---------------------------
def add_task(tasks):
    """Add a new task to the list."""
    desc = input("Enter task description: ")
    due = input("Enter due date (YYYY-MM-DD) or press Enter to skip: ")

    if due.strip() == "":
        due_date = None
    else:
        try:
            datetime.strptime(due, "%Y-%m-%d")
            due_date = due
        except ValueError:
            print("Invalid date format ! Task not added. \n")
            return

    task = {
        "description": desc,
        "due_date": due_date,
        "completed": False
    }
    tasks.append(task)
    save_tasks(tasks)
    print("Task added successfully ! \n")

# --------------------------- VIEW TASKS ---------------------------
def view_tasks(tasks, filter_type="all"):
    """View all, completed, pending, or due soon tasks."""
    if not tasks:
        print("No tasks found. \n")
        return

    print("\n------ TASK LIST ------")

    today = datetime.now().date()
    count = 0

    for i, task in enumerate(tasks, start=1):
        due = task["due_date"]
        status = "DONE HO GAYA TASK" if task["completed"] else "PENDING HAI BHAAI TASK"

        if filter_type == "completed" and not task["completed"]:
            continue
        elif filter_type == "pending" and task["completed"]:
            continue
        elif filter_type == "due_soon" and due:
            due_date = datetime.strptime(due, "%Y-%m-%d").date()
            if due_date - today > timedelta(days=3):
                continue

        count += 1
        print(f"{i}. {task['description']} | Due: {due or 'N/A'} | Status: {status}")

    if count == 0:
        print("No tasks found for this filter.")
    print("------------------------\n")

# --------------------------- MARK COMPLETE ---------------------------
def mark_complete(tasks):
    """Mark a task as completed."""
    view_tasks(tasks, "pending")
    try:
        index = int(input("Enter task number to mark complete: ")) - 1
        if 0 <= index < len(tasks):
            tasks[index]["completed"] = True
            save_tasks(tasks)
            print("Task marked as completed....!\n")
        else:
            print("Invalid task number!\n")
    except ValueError:
        print("Invalid input!\n")

# --------------------------- EDIT TASK ---------------------------
def edit_task(tasks):
    """Edit task description or due date."""
    view_tasks(tasks)
    try:
        index = int(input("Enter task number to edit: ")) - 1
        if 0 <= index < len(tasks):
            new_desc = input("Enter new description (press Enter to skip): ")
            new_due = input("Enter new due date (YYYY-MM-DD) or press Enter to skip: ")

            if new_desc.strip():
                tasks[index]["description"] = new_desc
            if new_due.strip():
                try:
                    datetime.strptime(new_due, "%Y-%m-%d")
                    tasks[index]["due_date"] = new_due
                except ValueError:
                    print("Invalid date format! Skipped updating due date.")

            save_tasks(tasks)
            print("Task updated successfully!\n")
        else:
            print("Invalid task number!\n")
    except ValueError:
        print("Invalid input!\n")

# --------------------------- DELETE TASK ---------------------------
def delete_task(tasks):
    """Delete a task by number."""
    view_tasks(tasks)
    try:
        index = int(input("Enter task number to delete: ")) - 1
        if 0 <= index < len(tasks):
            deleted_task = tasks.pop(index)
            save_tasks(tasks)
            print(f"Deleted: {deleted_task['description']}\n")
        else:
            print("Invalid task number!\n")
    except ValueError:
        print("Invalid input!\n")

# --------------------------- MAIN MENU ---------------------------
def main():
    """Main function to run the To-Do List Manager."""
    tasks = load_tasks()

    while True:
        print("===== TO-DO LIST MANAGER =====")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. View Completed Tasks")
        print("4. View Pending Tasks")
        print("5. View Tasks Due Soon (3 days)")
        print("6. Mark Task as Completed")
        print("7. Edit Task")
        print("8. Delete Task")
        print("9. Exit")

        choice = input("Enter your choice (1-9): ")

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks, "all")
        elif choice == "3":
            view_tasks(tasks, "completed")
        elif choice == "4":
            view_tasks(tasks, "pending")
        elif choice == "5":
            view_tasks(tasks, "due_soon")
        elif choice == "6":
            mark_complete(tasks)
        elif choice == "7":
            edit_task(tasks)
        elif choice == "8":
            delete_task(tasks)
        elif choice == "9":
            print("Saving and exiting... Goodbye!")
            break
        else:
            print("Invalid choice! Try again.\n")

# --------------------------- ENTRY POINT ---------------------------
if __name__ == "__main__":
    main()