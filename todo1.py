import tkinter as tk
from tkinter import ttk
import csv
from datetime import datetime, timedelta

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ToDo List Application")

        # Create a list to hold tasks
        self.tasks = []

        # Create GUI components
        self.create_gui()

        # Load tasks from CSV file
        self.load_from_csv()

        # Display existing entries in the GUI
        self.update_treeview()

    def create_gui(self):
        # Create treeview to display tasks
        columns = ("Goal", "Duration", "Entry Time", "Deadlines", "Status", "Action")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)

        # Define a custom sort function for the "Duration" column
        self.tree.heading("Duration", text="Duration", command=lambda: self.sort_column("Duration", False))
        self.tree.column("Duration", width=80)

        # Entry widgets
        self.goal_entry = tk.Entry(self.root, width=30)
        self.goal_entry.insert(tk.END, "Task Goal")

        self.duration_var = tk.StringVar()
        durations = ["1 month", "3 months", "6 months", "1 year", "5 years"]
        duration_menu = ttk.Combobox(self.root, textvariable=self.duration_var, values=durations)
        duration_menu.set("1 month")

        self.status_var = tk.StringVar()
        status_menu = ttk.Combobox(self.root, textvariable=self.status_var, values=["Incomplete", "Complete"])
        status_menu.set("Incomplete")

        # Buttons
        add_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        update_status_button = tk.Button(self.root, text="Update Status", command=self.update_status)
        update_duration_button = tk.Button(self.root, text="Update Duration", command=self.update_duration)

        # Arrange components using grid
        self.tree.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

        # Row for entry widgets and comboboxes
        tk.Label(self.root, text="Task Goal:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.goal_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(self.root, text="Duration:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        duration_menu.grid(row=1, column=3, padx=5, pady=5)
        tk.Label(self.root, text="Status:").grid(row=1, column=4, padx=5, pady=5, sticky="e")
        status_menu.grid(row=1, column=5, padx=5, pady=5)

        # Row for buttons
        add_button.grid(row=2, column=1, pady=5, sticky="e")
        delete_button.grid(row=2, column=2, pady=5, sticky="e")
        update_status_button.grid(row=2, column=3, pady=5, sticky="e")
        update_duration_button.grid(row=2, column=4, pady=5, sticky="e")

        # Configure row and column weights for resizing
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def load_from_csv(self):
        # Load tasks from the CSV file
        filename = "todo_list.csv"
        try:
            with open(filename, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                self.tasks = [task for task in reader]
        except FileNotFoundError:
            # If the file doesn't exist, create an empty file
            with open(filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["Goal", "Duration", "Entry Time", "Deadlines", "Status"])
                writer.writeheader()

    def add_task(self):
        goal = self.goal_entry.get()
        duration = self.duration_var.get()
        status = self.status_var.get()

        # Calculate deadlines based on the selected duration
        duration_mapping = {"1 month": 30, "3 months": 90, "6 months": 180, "1 year": 365, "5 years": 1825}
        entry_time = datetime.now()
        deadline = entry_time + timedelta(days=duration_mapping[duration])

        # Add task to the list
        new_task = {"Goal": goal, "Duration": duration, "Entry Time": entry_time, "Deadlines": deadline, "Status": status}
        self.tasks.append(new_task)

        # Update the treeview
        self.update_treeview()

        # Save tasks to the CSV file (append mode)
        self.save_to_csv()

    def delete_task(self):
        # Get the selected item from the treeview
        selected_item = self.tree.selection()

        if selected_item:
            # Remove the selected task from the list and update the treeview
            index = self.tree.index(selected_item)
            del self.tasks[index]
            self.update_treeview()

            # Save the updated task list to the CSV file
            self.save_to_csv()

    def update_status(self):
        # Get the selected item from the treeview
        selected_item = self.tree.selection()

        if selected_item:
            # Toggle the status of the selected task between "Incomplete" and "Complete"
            index = self.tree.index(selected_item)
            current_status = self.tasks[index]["Status"]
            new_status = "Complete" if current_status == "Incomplete" else "Incomplete"
            self.tasks[index]["Status"] = new_status

            # Update the treeview
            self.update_treeview()

            # Save the updated task list to the CSV file
            self.save_to_csv()

    def update_duration(self):
        # Get the selected item from the treeview
        selected_item = self.tree.selection()

        if selected_item:
            # Update the duration of the selected task based on the chosen duration from the menu
            index = self.tree.index(selected_item)
            new_duration = self.duration_var.get()
            duration_mapping = {"1 month": 30, "3 months": 90, "6 months": 180, "1 year": 365, "5 years": 1825}
            entry_time = datetime.now()
            deadline = entry_time + timedelta(days=duration_mapping[new_duration])
            self.tasks[index]["Duration"] = new_duration
            self.tasks[index]["Deadlines"] = deadline

            # Update the treeview
            self.update_treeview()

            # Save the updated task list to the CSV file
            self.save_to_csv()

    def update_treeview(self):
        # Clear existing items in the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        print(self.tasks)
        # Sort tasks by duration and update the treeview
        sorted_tasks = sorted(self.tasks, key=lambda x: self.get_sort_value(x["Deadlines"]))
        
        for task in sorted_tasks:
            status_button_text = "Complete" if task["Status"] == "Complete" else "Incomplete"
            background_color = "lightgreen" if task["Status"] == "Complete" else "white"
            self.tree.insert("", tk.END, values=(task["Goal"], task["Duration"], task["Entry Time"], task["Deadlines"], task["Status"], status_button_text), tags=(status_button_text, ))
            self.tree.tag_configure(status_button_text, background=background_color)

        # Refresh the display
        self.tree.update()

    def get_sort_value(self, value):
        # Helper function to determine the sorting value
        if isinstance(value, datetime):
            return value
        try:
            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return value

    def save_to_csv(self):
        # Save tasks to a CSV file (overwrite mode)
        filename = "todo_list.csv"
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["Goal", "Duration", "Entry Time", "Deadlines", "Status"])
            writer.writeheader()
            writer.writerows(self.tasks)

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()
